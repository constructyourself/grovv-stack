# Knowledge Graph Engineering for Multi-Agentic Systems

An assessment of the knowledge-graph playbook and a scoped plan for absorbing it into gro\\/\\/ stack.

This file is the architecture note of record for the decision. `docs/architecture/` already exists and this document sits in it, so there is no separate ADR to write; the "What We Are Deliberately Not Doing" section below is the rejections record a future session should read before re-opening the new-step or seventh-agent options. Part One is a fidelity pass over the source. Part Two is the plan. Every repository count in Part Two was re-derived by grep against this repository on the date in the colophon, and each is cited with the paths that produced it.

Source document: "Knowledge Graph Engineering for Multi-Agentic Systems: The Anthropic Playbook," a 12-page independent synthesis compiled July 2026. It is not a publication of Anthropic and is not affiliated with or endorsed by Anthropic — it says so three times: on the cover page, in the acknowledgment that names its four Anthropic sources, and in the page-12 footer. It synthesizes Anthropic's public `claude-cookbooks` knowledge-graph material, "Building Effective Agents" (Schluntz and Zhang, Dec. 2024), a 2026 architecture-patterns document, and the Managed Agents writing. Its code is described as "adapted from the public cookbook for pedagogical clarity" — adapted, not byte-identical. Its measured results come from a six-document Wikipedia corpus, of which only two documents were scored. Treat it as a well-argued design note with a toy evaluation, not as a specification.

-----

## Summary

### The playbook in about 200 words

The problem it opens on: a pile of unstructured documents and questions that span them, where no single document contains the answer and RAG cannot chain facts across passages that share no similarity with the query or with each other.

Its answer collapses classical knowledge-graph construction — trained NER, a trained relation classifier, and hand-written entity-resolution heuristics — into four stages, three of them prompted, over a small set of Pydantic schemas. Extraction (Haiku, one call per document, structured output) returns typed entities and subject-predicate-object triples. Resolution (Sonnet, one call per entity type) clusters raw surface forms into canonical nodes using the one-line descriptions written during extraction. Assembly is deterministic; summarization (Sonnet) synthesizes profiles for high-degree hub nodes only. Querying serializes the k-hop neighborhood of a seed entity as triples and constrains the model to answer using only those edges, citing them.

The structural claim is that structured outputs make the interface between stages a type-checked contract rather than a parsing hope, which is what makes the pipeline viable at thousands of documents rather than ten. The multi-agent claim is that the graph is shared memory for orchestrator-workers, ground truth for an evaluator, and a world model that survives context flushes. An evaluation harness — hand-labelled gold set, precision and recall, rerun on every prompt change — is presented as the thing that separates a demo from a production system.

### The integration recommendation in about 150 words

Adopt the grounding discipline unconditionally; gate the graph itself.

The grounding discipline — factual claims cite a checkable locator, non-deterministic output is scored against a hand-labelled gold set rather than asserted with equality checks, every cross-agent artifact carries provenance — is roughly 55 lines across three existing files, needs no infrastructure, and improves every project grovv scaffolds. It also fixes an active defect that spans two files: `.claude/agents/testing.md:60` says "Tests must be deterministic — no flaky tests" and `.claude/agents/code-review.md:41` enforces the same rule as a blocking review checkbox, with no carve-out in either. That is wrong guidance for any project shipping a model-backed feature.

The graph itself becomes a conditional capability behind a two-condition gate evaluated at Step 6, with depth in one new prompt document. No new numbered pipeline step. No seventh agent. No row in any stack table. Appendix C of the source states that not every multi-agent system needs a graph and gives seven scenario rows, three of which resolve to RAG or a single agent. It is grovv's own judgment — not the source's — that the majority of projects grovv scaffolds land in those three rows, and that judgment is why the capability ships default-off.

-----

## Part One: What the Playbook Says

### The four-stage pipeline

| Stage | Model | Input | Output | Why this model |
|-------|-------|-------|--------|----------------|
| Extraction | Haiku 4.5 — the one stage the source pins to a version | One document at a time | Typed entities plus S-P-O triples, validated against `ExtractedGraph` | "High volume, schema-constrained; speed and cost dominate." Cost is linear in corpus size, so this stage must be the cheap one |
| Resolution | Sonnet, never versioned | All raw entities of one type, with descriptions | Alias map: canonical name plus every surface form | "Weighing conflicting evidence; reasoning quality dominates." One call per entity type per pass, not one per document |
| Assembly and summarization | None for assembly (deterministic); Sonnet for summarization | Canonicalized relations; then hub-node mentions plus neighborhood | `MultiDiGraph`; `EntityProfile` for high-degree nodes only | "Synthesizing across documents; nuance matters." Applied selectively, so total cost is sublinear in corpus size |
| Querying | Sonnet, referenced only as `SYNTHESIS_MODEL` and never bound | Question plus a serialized k-hop subgraph | Prose answer citing specific edges | "Multi-hop reasoning over serialized triples." Cost is proportional to subgraph size and dominates for a heavily-queried graph |

The two-model split is the cost argument. Extraction dominates for a large corpus; querying dominates for a heavily-queried one. Optimizing them independently is the stated reason the split matters.

The source is internally inconsistent about how many stages it is replacing: Section II.A says Claude "collapses it into three prompts" against classical NER, relation extraction, and entity resolution, while Section XI.A says the pipeline "replaces four distinct trained systems." Neither count is load-bearing; the four-stage figure is the one the pipeline diagram uses.

### The schemas

Reproduced from the source. The exact wording is the technique — the schema is described as "the training data for the extractor." Seven Pydantic models across three blocks.

```python
EntityType = Literal["PERSON", "ORGANIZATION",
                      "LOCATION", "EVENT", "ARTIFACT"]

class Entity(BaseModel):
    name: str
    type: EntityType
    description: str   # one-line, for disambiguation

class Relation(BaseModel):
    source: str
    predicate: str     # short verb phrase
    target: str

class ExtractedGraph(BaseModel):
    entities: list[Entity]
    relations: list[Relation]
```

```python
class Cluster(BaseModel):
    canonical: str       # most complete form
    aliases: list[str]   # all surface forms

class ResolvedClusters(BaseModel):
    clusters: list[Cluster]
```

```python
class TimeRange(BaseModel):
    start: str   # YYYY or "unknown"
    end: str     # YYYY or "ongoing"

class EntityProfile(BaseModel):
    summary: str          # 2-3 paragraphs
    key_facts: list[str]  # 3-5 atomic, traceable facts
    time_range: TimeRange
```

`EntityType` is a closed five-value literal. Widening it is the first thing a domain adaptation does, and the playbook's own worked example adds `PRICING`, `FEATURE`, and `FILING`.

### The three prompts

```python
EXTRACTION_PROMPT = """Extract a knowledge graph from
the document below.

<document>
{text}
</document>

Guidelines:
- Extract only entities that are central to what
  this document is about — skip incidental mentions.
- For each entity, write a one-sentence description
  grounded in this document. These descriptions are
  used later to disambiguate entities with similar
  names.
- Predicates should be short verb phrases
  ("commanded", "launched from", "part of").
- Every relation must connect two entities you
  extracted."""
```

Each guideline addresses a distinct failure mode. "Central only" controls recall and favours precision. The one-sentence descriptions are the disambiguation signal that resolution later depends on entirely. Short verb-phrase predicates keep the graph traversable — "was involved with" is too vague to reason over, "commanded" is not. The last guideline prevents dangling edges.

```python
RESOLVE_PROMPT = """Below are {entity_type} entities
extracted from several documents. Some are different
surface forms of the same real-world entity.

<entities>
{entity_list}
</entities>

Cluster them. Each input name must appear in exactly
one cluster's aliases list. Entities that are
genuinely distinct get their own single-element
cluster. Use the descriptions to avoid merging
entities that merely share a name. The canonical
name should be the most complete, unambiguous
form."""
```

Four constraints, four failure modes: every input name must appear (prevents silent loss); distinct entities get single-element clusters (prevents over-merging); descriptions must be used (prevents surface-form-only matching); canonical is the most complete form (downstream consumers see the most informative name).

```python
SUMMARIZE_PROMPT = """Generate a knowledge-graph
profile for this entity.

Entity: {name} ({etype})

Source excerpts mentioning this entity:
{excerpts}

Known relations in the graph:
{relations}

Write a 2-3 paragraph factual summary synthesized
from the excerpts, resolving any contradictions by
preferring the most specific claim. Include 3-5
atomic key facts, each traceable to the sources.
For the time range, use YYYY or YYYY-MM format.
Do not invent facts not supported by the
excerpts."""
```

"Prefer the most specific claim" and "do not invent facts" are called the summarization analogues of an evaluator's "assume broken until proven otherwise" — both default to caution.

### Structured outputs as the enabling capability

The extraction call is five lines:

```python
def extract(text: str) -> ExtractedGraph:
    response = client.messages.parse(
        model=EXTRACTION_MODEL,
        max_tokens=2048,
        messages=[{"role": "user",
                   "content": EXTRACTION_PROMPT
                              .format(text=text)}],
        output_format=ExtractedGraph,
    )
    return response.parsed_output
```

The argument: without structured outputs the pipeline must parse free-form text, handle malformed JSON, and validate types at runtime — "each of these is a failure point that scales linearly with corpus size." With them, "the schema is the contract: the API call either returns a valid `ExtractedGraph` object or raises an error."

One scope limit the source overstates and this document corrects. The playbook says "the entire pipeline depends on" structured outputs, but the query stage deliberately uses a plain create call with free prose output and no schema. The defensible claim is that structured outputs are the ingest contract, not the answer contract. Answer verifiability comes from a different mechanism: the string-matchable citation format.

### Entity resolution, and why the descriptions carry it

The disambiguation power of resolution comes entirely from the one-line descriptions written during extraction. "Armstrong — first person to walk on the Moon" and "Armstrong — jazz trumpeter" are separable; "Armstrong" and "Armstrong" are not. An extraction prompt that skips descriptions collapses the whole approach back to the string-similarity failure mode it exists to avoid. The description is a first-class input to resolution, not metadata.

On the Apollo corpus, resolution compressed 24 unique surface forms to 22 canonical entities, catching "Edwin Aldrin" to "Buzz Aldrin" and "Neil Armstrong" to "Neil Alden Armstrong." That compression figure is the only quantitative evidence anywhere in the source that resolution did anything.

Two failure modes, both requiring spot-checking:

| Failure | Mechanism | Consequence |
|---------|-----------|-------------|
| Silent loss | A raw name is left out of every cluster, so the alias map has no entry for it | The node vanishes from the graph. A production resolver must fall back to a single-element cluster for unmatched names |
| Over-merging | A specific entity is folded into a broader one because their descriptions overlap | Precision loss. Distinct things become one node and their edges pool |

Resolution is framed as an agent in its own right: fixed prompt and schema, stateless over batches, parallelizable across entity types, deployable as a worker. Extraction, resolution, and summarization are "three independent agents coordinated by a simple sequential workflow."

### Assembly, hubs, summarization triggers, diagnostics

The graph is a `MultiDiGraph`. Multi- because two entities can be connected by several distinct predicates; di- because "Armstrong commanded Apollo 11" is not the same edge as its reverse. Nodes carry type, source documents, and mention count; edges carry predicate and provenance document.

Summarization is selective: profile the top-k nodes by degree, with a stated practical cutoff of degree at least 3 — mentioned in at least two documents from different directions. Below that, the single-document description is usually sufficient. This is what keeps summarization cost sublinear.

Three diagnostics are run before querying:

| Diagnostic | Healthy | What a deviation means |
|------------|---------|------------------------|
| Weakly connected components | One | More components reveals islands resolution left behind — variants that should have merged and did not |
| Degree distribution | Power-law-like: few high-degree, many low-degree | A flat distribution suggests a homogeneous corpus, or an extraction prompt treating all mentions equally instead of distinguishing central from peripheral |
| Edges/nodes ratio | Middle range | Below 1.0 is sparse (many isolated entities); above 2.0 is richly connected |

On the six-document Apollo corpus: 36 raw entities and 34 relations extracted (Table I), resolving to 22 nodes and 34 edges, one connected component, ratio 1.55, two hub nodes at degree 9. All of these numbers are toy-corpus observations, not thresholds.

### Multi-hop querying, and grounded versus ungrounded

```python
def serialize_subgraph(center: str, hops: int = 2
                       ) -> str:
    nodes = {center}
    frontier = {center}
    for _ in range(hops):
        nxt = set()
        for n in frontier:
            nxt |= set(G.successors(n))
            nxt |= set(G.predecessors(n))
        frontier = nxt - nodes
        nodes |= frontier
    sub = G.subgraph(nodes)
    lines = [
        f"({s}) --[{d['predicate']}]--> ({t})"
        for s, t, d in sub.edges(data=True)
    ]
    return "\n".join(sorted(set(lines)))
```

The BFS collects both successors and predecessors — undirected expansion over a directed graph. The grounding instruction is deliberately restrictive: "Answer using only the knowledge graph below. Cite the specific edges that support your answer."

That citation format produces answers of the form `(Armstrong) --[walked on]--> (Moon)` rather than prose claims, which makes verification a string match against the input.

The grounded-versus-ungrounded comparison is narrated, not scored. Without graph context the model produces a comprehensive, plausible answer from pretraining. With it, the answer is constrained to extracted edges and explicitly flags what the graph does not contain. The verdict: "less impressive but infinitely more useful... On a private corpus, only the second kind of answer works at all."

The k tradeoff: k=1 is fast and focused but misses indirect connections; k=2 is called the sweet spot for multi-hop questions; k=3 and beyond grows the subgraph rapidly and may exceed the context window. The only measured datapoint is that k=2 from any Apollo hub node captures nearly the whole 22-node, 34-edge graph in a single Sonnet call — a toy-corpus observation, not a budget. Overflow beyond k=2 is addressed in one clause (filter or summarize the serialized triples) with no token budget, no threshold, and no algorithm.

The production recommendation is to return the serialized subgraph alongside the answer, so the calling agent or human sees exactly which edges were available. That transparency is what the source says distinguishes graph-grounding from RAG-grounding: with RAG the context is a blob of retrieved text that may or may not contain the supporting evidence; with a graph the context is a set of explicit triples each carrying provenance.

### Section VII: the five agent patterns

This is the load-bearing section for grovv, and also the least evidenced. Anthropic documents five patterns; the source maps one graph role onto each. Table II has exactly five rows, and the source repeats the count three times — in Section II.B, immediately above Table II, and in the Conclusion, which enumerates "retrieval source, gate signal, classifier input, shared memory, and grounding layer."

| Pattern | Graph role | How it helps (source wording) |
|---------|-----------|--------------|
| Augmented LLM | Retrieval source | Graph traversal replaces vector search for multi-hop questions; the LLM queries the graph as a tool |
| Prompt chaining | Gate signal | Between chain steps, a graph query checks whether new entities conflict with existing nodes |
| Routing | Classifier input | Entity type and degree from the graph route a query to the right specialist without an LLM call |
| Orchestrator-workers | Shared memory | Workers read from and write to the graph; the orchestrator's window stays clean |
| Evaluator-optimizer | Grounding layer | The evaluator checks claims against graph edges with provenance |

Two observations belong to this document rather than the source: the routing row describes a deterministic, zero-token classifier signal, and the prompt-chaining row describes the graph acting as the programmatic gate that pattern already calls for. Both are fair readings; neither is the source's phrasing.

A sixth role — persistent world model for autonomous loops — appears in Sections II.C and VII.C as prose, not as a row in Table II. Autonomous loops are not one of Anthropic's five documented patterns. In that prose the graph "survives context-window flushes the way a state file survives a process restart — the agent forgets, the graph does not."

The orchestrator-workers argument is the sharpest: passing summaries through the orchestrator's window grows it linearly with worker count, whereas the graph is durable, append-only, and interrogable by slice. The source anchors this on an unsourced figure of its own: "internal research shows multi-agent systems outperform single agents by 90.2% on tasks requiring multiple independent directions — but they consume 10-15x more tokens and require careful context management." Both numbers arrive with no citation, benchmark, or task definition. The 10-15x token multiplier is the premise the whole shared-memory argument rests on and is the one figure here that bears directly on grovv's Step 7 economics; it is quotable as the source's premise, never as a benchmark.

The evaluator-optimizer loop shape: generator produces content; a query stage serializes the k-hop neighborhood of every entity mentioned; the evaluator receives both, checks every claim against edges, and flags claims with no supporting edge; feedback names the contradicting evidence rather than saying "this is wrong"; a claim absent from the graph entirely is escalated to a human rather than silently accepted or rejected.

The worked fact-check — a generator claims "Armstrong commanded Gemini 12," an evaluator with graph access finds no such edge but does find `(Buzz Aldrin) --[flew on]--> (Gemini 12)` and `(Neil Alden Armstrong) --[commanded]--> (Apollo 11)` — is explicitly introduced as "consider a concrete example." It is a hand-constructed illustration, not a logged run. Its value is the shape of the feedback, not evidence that graph-grounded evaluators outperform ungrounded ones. No such comparison is measured anywhere in the document.

Section VII.D extends this to collaborative blackboard and hierarchical segmented-subgraph architectures. That section is one paragraph of assertion with no code, schema, or measurement behind it, and is the part of the document most likely to be over-read as a validated design pattern.

### Appendix B: the worked competitive-intelligence example

Two of the twelve pages, and the source's only worked multi-agent integration. One orchestrator, five specialist workers — pricing, product, financial, marketing, and a strategic synthesizer — over four numbered steps.

| Step | What happens |
|------|--------------|
| 1 — Parallel extraction | Each worker runs the extraction pipeline on its own corpus slice, using the same schema and prompt with only `EntityType` widened to domain types (`PRICING`, `FEATURE`, `FILING`). The schema is the contract that keeps all five workers' outputs compatible |
| 2 — Cross-worker resolution | The resolver runs once, over the combined entity lists from all five workers. The financial agent's "Acme Corp," the product agent's "ACME Corporation," and the pricing agent's "acme" must resolve to one canonical node. This is named the critical step: without it the synthesizer sees three disconnected nodes and the connection it exists to find does not exist |
| 3 — Graph assembly | Resolved entities and relations from all five workers load into one graph. Provenance records which worker extracted each edge, from which document — not just the document |
| 4 — Synthesis via traversal | The synthesizer never re-reads the source documents. It queries for everything within two hops of the canonical node and reasons over the serialized triples, citing worker and document per claim. The orchestrator's window never held five workers' raw outputs |

The source's own summary of why the pattern works is a three-term triad, and it is the most directly reusable framing in the document for grovv's Step 7: the graph is connecting (resolution links a company across workers that never communicated), compressing (the synthesizer reads roughly 50 triples, not five workers' documents), and grounding (every triple carries provenance, so the analysis traces to sources rather than to the synthesizer's imagination).

This appendix is narrative. There is no code, no measurement, and the acknowledgment explicitly flags the competitive-intelligence example as illustrative.

### Evaluation, and what the reported numbers mean

Quality is precision and recall against a hand-labelled gold set, scoring raw extractor output and the same entities after resolution.

| Document | Raw F1 | Precision | Recall | Resolved recall |
|----------|--------|-----------|--------|-----------------|
| Apollo 11 | 0.71 | 1.00 | 0.55 | 0.55 |
| Neil Armstrong | 0.55 | 1.00 | 0.38 | 0.38 |

Only two of the six corpus documents are scored. Perfect precision means the extractor is conservative — everything it finds is correct. The asymmetry argument is the load-bearing claim, and it is a reasoning argument rather than a measurement, which is why it survives the weak evidence: false positives are harder to detect and more damaging than false negatives, because a wrong entity spawns wrong relations that propagate through multi-hop reasoning. A missing entity produces an incomplete but correct graph; a wrong entity produces a graph that actively misleads.

The misses are not model failures. One category is entities mentioned only in passing, which the "central only" instruction correctly filtered. The other is entities from the gold set's broader cross-document scope that were not central to the document being scored — a scope mismatch, not an extraction failure.

Relation scoring is done on `(source, target)` pairs, ignoring predicate wording, because "commanded" and "led" and "was commander of" describe the same relation. That gives an upper bound on relation recall, and is judged sufficient to detect structural errors, which matter more than predicate-wording differences.

The alias-map artifact: when the resolver picks a canonical form the scorer does not recognize, resolved recall can drop. That is a scoring artifact, not a resolver bug, and the fix is to extend the alias map. Note that in both scored rows resolved recall exactly equals raw recall, so this artifact is argued in prose and never demonstrated in the data, and no measured recall improvement from resolution is shown anywhere. Resolution's one measured effect in the whole document is structural: 24 surface forms compressed to 22 canonical nodes.

The feedback loop is the stated point of the whole section: change the extraction prompt, rerun the scorer, watch the F1 move. "A team that ships the pipeline without the evaluation harness has no way to know whether prompt changes improve or degrade quality, and no way to catch the slow drift that occurs as the corpus evolves."

### Scaling and cost regimes

| Regime | Shape | Lever |
|--------|-------|-------|
| Extraction | Cheap per document, linear in corpus size | Prompt caching and the Batches API |
| Resolution | Moderate — Sonnet, one call per entity type per pass, not per document | Blocking before arbitration |
| Summarization | Expensive per entity, applied only to high-degree nodes, so sublinear overall | The degree cutoff |
| Querying | Per question, proportional to subgraph size | Pre-computed serialization for high-traffic seeds |

On the Batches lever the source is precise and the precision matters: "the Message Batches API gives 50% off for jobs that can tolerate up to 24 hours of latency." The discount is conditional on that latency tolerance, and any cost figure quoted at the batched rate has to be quoted with the condition attached.

Resolution at scale does not work by feeding ten thousand entities into one prompt. Block first — group candidates by cheap signals such as shared last name, overlapping tokens, or embedding similarity, implemented as an inverted index on name tokens with no model call — then let the model arbitrate within blocks of 50 to 100. The resolution prompt works unchanged on blocks. The generalized principle: keep the model for the parts that require judgment, use deterministic logic for everything else. The document concedes that the clustering prompt is universal but the blocking is not — blocking heuristics remain domain-dependent, and this is the one place a domain-specific engineering burden survives the move to LLMs.

Storage. NetworkX is stated as fine to a few hundred thousand edges. Beyond that, either a property graph or three Postgres tables:

```sql
entities(id, name, type, summary)
relations(source_id, target_id, predicate)
aliases(entity_id, alias)
```

with graph queries as recursive CTEs. "The extraction and resolution code does not change — only the persistence layer does." Sixty-odd words later, after the Neo4j-mapping and Postgres passages: "The choice between them is an infrastructure decision, not a pipeline decision."

Long documents must be chunked at section boundaries with one paragraph of overlap, so that entities and their relations fall within the same chunk. Naive token-count chunking splits entities from their context. The extraction prompt works unchanged on chunks; the extra step is deduplicating entities across chunks of the same document by exact string match before resolution.

Four production monitoring signals: extraction rate (a drop suggests a domain shift the prompt handles poorly, a spike suggests over-extraction of peripheral mentions); resolution compression ratio, defined as raw surface forms divided by canonical entities, where near 1.0 means the corpus names things consistently and resolution is doing little, and the source asserts — without measuring — that above 2.0 resolution is earning its cost; graph connectivity (a growing number of components suggests resolution is missing cross-document links); query latency.

### Operational discipline

Three practices, stated as required before shipping rather than after:

- A daily random-node sample. Pick a node, read its profile, check its edges against the source documents, verify the provenance chain. "The moment you cannot explain why a node has a particular edge, your understanding of the graph has fallen behind its contents."
- A per-run extraction cap on both documents processed and entities extracted, so that an ingestion error cannot produce a run of unbounded cost. It must exist before shipping.
- Schema versioning, where the extraction prompt counts as part of the schema. Entities extracted under different prompts must remain distinguishable, comparable, and re-extractable.

What the graph does not replace is judgment. "The graph is a structured fact store; it does not decide which facts matter, which entities to trust, or which actions to take... The graph moves the basis for these decisions from model estimation to extracted facts, but the decisions themselves remain with the agents — and ultimately with the human who designed them."

And the sharpest line in the document: "the pipeline is not done when it runs; it is done when you can tell, on any given morning, whether what it produced overnight was actually right."

### Appendix C: when not to build a graph

Appendix C opens with "not every multi-agent system needs a knowledge graph" and gives a seven-row decision table. Four of the seven rows point at a graph; three point away. The table is a matching exercise, not a discouragement.

| Scenario | Right tool | Why |
|----------|-----------|-----|
| Single-document QA | RAG or direct context | No multi-hop needed; the answer is in one chunk |
| Multi-document, single-hop | RAG with reranking | The answer spans documents but does not require chaining |
| Multi-document, multi-hop | Knowledge graph | Chaining facts across documents requires entity-level linking |
| Multi-agent, shared state | Knowledge graph | Workers need a shared world model outside context windows |
| Evaluator needs ground truth | Knowledge graph | Fact-checking requires structured, provenance-carrying facts |
| Overnight loop, persistent memory | Knowledge graph | Memory must survive context flushes across sessions |
| Simple classification or routing | Single agent | No cross-document reasoning needed |

The rule of thumb is symmetric: if agents need to chain facts across sources, share structured state, or ground judgments in traceable evidence, the graph is the right infrastructure; if they need to retrieve passages or classify inputs, simpler tools suffice. "The graph earns its complexity when the alternative — passing raw documents or summaries through context windows — either exceeds the window or loses the connections." RAG and graphs are complementary, not competing.

The source says nothing about how the population of real systems distributes across these seven rows. The judgment that most grovv projects land in the three non-graph rows is grovv's, argued in Part Two, and is not attributable to the playbook.

### Appendix D: production readiness checklist

| Element | Ask yourself | Failure if missing |
|---------|--------------|--------------------|
| Gold set | Is there a hand-labeled evaluation set for at least two representative documents? | No feedback loop; prompt changes are blind |
| Alias map | Does the scorer's alias map cover every canonical form the resolver produces? | Scoring artifacts — recall appears worse than it is |
| Schema version | Is the extraction schema versioned alongside the graph? | Incompatible entities from different prompt versions |
| Extraction cap | Is there a per-run limit on documents processed? | Unbounded cost from corpus ingestion errors |
| Resolution fallback | Do unmatched names get single-element clusters? | Silent entity loss — nodes disappear from the graph |
| Provenance tracking | Does every edge carry its source document and extraction timestamp? | Ungrounded answers; the evaluator cannot fact-check |
| Incremental update | Can new documents be added without rebuilding the entire graph? | Rebuild cost scales with corpus size, not delta size |
| Connectivity monitor | Do you check connected components after each resolution pass? | Fragmented graph — missed cross-document links |
| Summarization trigger | Is re-summarization triggered only when the source-document set changes? | Wasted Sonnet calls on unchanged entities |
| Human sample | Does someone read a random node profile each day? | Comprehension rot — the graph outgrows understanding |

The grouping matters for staging an adoption: the first two give the evaluation feedback loop; the next three prevent silent data corruption; the next three keep the graph structurally sound; the last two keep costs manageable and understanding current.

### What the playbook does not establish

Recorded plainly, because these limits shape the recommendation.

| Gap | Detail |
|-----|--------|
| Scale of evidence | Six Wikipedia summaries, 22 nodes, 34 edges. Every structural claim rests on that corpus. No production-scale evaluation appears anywhere |
| Relation quality | No relation-level precision or recall is reported, despite an extended discussion of relation scoring |
| Resolution effect | Both scored rows show resolution with exactly zero measured effect on recall. Its only measured effect anywhere is the 24-to-22 surface-form compression |
| Code coverage | Three executable functions across twelve pages: `extract` (III.D), `serialize_subgraph` and `ask` (both Appendix E). No resolver, summarizer, assembler, scorer, blocking, chunking, or persistence code. No error handling, retry, or transaction discipline anywhere |
| Unmeasured thresholds | Degree 3, k=2, blocks of 50-100, edges/nodes bands, the 2.0 compression-ratio band, "a few hundred thousand edges" — all asserted, none measured |
| Cost arithmetic | "Single-digit dollars for 10,000 documents" is stated with no rate table and no calculation. See the corrections below |
| Appendix B | The only worked multi-agent integration is a hand-constructed narrative: no code, no measurement, and flagged as illustrative in the acknowledgment |
| Section VII.D and XI.F | Collaborative blackboards, hierarchical subgraphs, temporal graphs, confidence scoring, graph-of-graphs — all proposals, no implementations |
| Unsourced figures | "Multi-agent systems outperform single agents by 90.2%" and "10-15x more tokens" both appear with no citation, benchmark, or task definition. Quotable as the source's premise, not as measurements |
| No reference list | Related Work discusses two decades of literature with zero citations. Only four Anthropic sources are named, in the acknowledgment |

-----

## Part Two: What This Means for gro\\/\\/ stack

### Four axes, kept strictly separate

grovv-stack is not an application. It is a prompt-driven scaffolding system shipped as a Claude Code plugin, whose only output is documents and configuration files written into other projects. It has no dependencies, no build step, and no runtime code, and must not gain any. "Integrating the playbook" therefore means exactly four things, and conflating them is the main way this goes wrong.

| Axis | Meaning | Verdict |
|------|---------|---------|
| A — Output | grovv gains the ability to scaffold a knowledge-graph subsystem into a target project: a conditional prompt document, a conditional skill, storage and guardrail patterns in the existing agents | Adopt, gated |
| B — Process | grovv's own pipeline and agent-team design absorb the ideas: grounding for the reviewer, gold-set scoring for the tester, shared-store data passing for the harness | Adopt, unconditional |
| C — Self | A graph over grovv-stack's own artifacts — spec to plan to issue to agent to skill | Decline. See the rejections |
| D — Housekeeping | Changes to grovv-stack's own memory and version metadata that any change of this size requires | Required, mechanical |

Every line of playbook code becomes reference code inside a generated prompt or skill, destined for the target project. None of it is committed to grovv-stack.

### The step decision

No new numbered pipeline step. The pipeline stays Steps 0-9. The capability is absorbed by Step 6 (skills-builder), which owns the gate and the generation, and Step 7 (team-design), which owns the downstream consequence. Depth lives in one new conditional prompt document that declares itself, in its own first paragraph, to be a conditional sub-step of Step 6 rather than a step.

The primary reason is semantic, not mechanical. A numbered step in `grovv-stack-scaffold.md` is a step every project runs; the directive is read end-to-end before any file is written, on every invocation, for every project. Giving a default-off capability its own number tells every future agent that a knowledge graph is part of the expected shape of a grovv project, which is precisely the reading the gate exists to prevent. A conditional branch inside Step 6 delivers the same capability and encodes the right default.

The mechanical cost is real but smaller than an earlier draft of this note claimed, and the corrected numbers are worth stating because the earlier ones were not derived.

| Claim | Verified value |
|-------|----------------|
| Step numbers referenced by number | `grep -rnE "[Ss]teps? [0-9]"` over Markdown and JSON, excluding the vendored harness tree and this file, returns 37 lines in 9 files. One of those, `docs/prompts/linear-tracking.md:34`, is that file's own internal workflow numbering and would not move under a pipeline renumber — leaving 36 lines across 8 files |
| Step headings | 10, all in `grovv-stack-scaffold.md` at `:152`, `:172`, `:198`, `:245`, `:270`, `:319`, `:370`, `:381`, `:396`, `:406` |
| Step-range expressions | 6, one per file: `MEMORY.md:36`, `CLAUDE.md:21`, `.claude/CLAUDE.md:21`, `.claude/skills/grovv/SKILL.md:20`, `.claude/agents/scaffold.md:25`, `grovv-stack-scaffold.md:546` |
| Step numbers in the JSON manifests | Zero. `grep -i step .claude-plugin/*.json settings.json .claude/settings.json` returns nothing. Neither manifest carries a step number, a step name, or a numbered pipeline description |
| Success Criteria | Carries no step-number reference. `grovv-stack-scaffold.md:555-573` enumerates artifacts, not steps |
| Prompt files carrying pipeline step numbers | Two: `docs/prompts/skills-builder.md:3` and `docs/prompts/team-design.md:3` and `:128`. `linear-tracking.md:3` states its position in prose only; `readme-generator.md` has none |

Two honest consequences of re-deriving these. First, the "two JSON manifests no Markdown grep will find" claim was false and is deleted; the manifests are step-agnostic, which makes a new step slightly cheaper than previously argued. Second, appending a Step 10 is cheaper than inserting one: the six range expressions and the `.claude/agents/scaffold.md:25-36` list would change, but the 30 remaining references to Steps 0 through 9 would still be correct. The mechanical argument is therefore a supporting argument, not the decision. The decision rests on what a number means to a reader of the directive.

The one enumeration that does change: the prompt-document set goes from five to six. That is eight locations, and only three of them currently say "five" — see the propagation checklist.

Adopt mode gets one carve-out, stated in the master directive rather than only in the prompt: when Step 0 has found an existing retrieval layer, the capability is an adoption-plan item, never a silent generation. See the ask-first script.

### Playbook default to grovv default

| Playbook default | grovv equivalent | Notes |
|------------------|------------------|-------|
| Pydantic `BaseModel` and `Literal` for the extraction schema | Zod schema with `z.enum([...])` | The structured-outputs JSON-Schema subset excludes recursive schemas and numeric or string constraints, and requires `additionalProperties: false` on every object. Semantic load therefore rides on description text rather than constraints. The playbook's `Entity`, `Relation`, and `ExtractedGraph` shapes are all within the subset |
| `client.messages.parse(..., output_format=...)` returning `parsed_output` | `client.messages.parse({ ..., output_config: { format: zodOutputFormat(Schema) } })` returning `response.parsed_output` | A real 1:1 mapping, not an approximation. `zodOutputFormat` comes from `@anthropic-ai/sdk/helpers/zod`. The TypeScript `parsed_output` is nullable; the Python one is not, so the reference code must handle null |
| Haiku 4.5 for extraction | Unchanged | The one stage the source pins to a version. Pin deliberately and confirm availability at implementation time |
| "Sonnet" for resolution, summarization, querying | A current Sonnet, pinned explicitly | The source never versions Sonnet and never binds `SYNTHESIS_MODEL`. This is a mapping decision, not a transcription. See the open questions on whether resolution warrants a more capable model |
| NetworkX `MultiDiGraph` in memory, Postgres as a scale-up path | PostgreSQL from day one, four tables not three | grovv already defaults background jobs to PostgreSQL-native rather than reaching for a specialist store. The source's three tables are insufficient: incremental update, the per-run cap, and provenance all require a document/ingest-cursor table it never mentions. Traversal as recursive CTEs with an explicit depth cap |
| "The cookbook's evaluation script" (no code shown) | Vitest, split in two | The scorer is a pure deterministic function over predicted, gold, and alias map, and is unit-tested in CI. The evaluation calls the live API, costs money, and runs on demand and on every prompt or model change — never on every push. This split is what makes the harness compatible with grovv's existing "no flaky tests" rule instead of contradicting it |
| "Extract, resolve against the existing canonical set, add new edges" | A PostgreSQL-native background job using `SKIP LOCKED` | Extraction results and the ingest-cursor advance commit in one transaction, matching grovv's zero-data-loss rule and its existing Lago same-transaction rule |
| Four monitoring signals described in prose | Four PostHog events with properties, one insight each | Straight mapping onto grovv's existing observability default. No new stack entry needed |
| Python throughout | TypeScript with Zod and the Anthropic TypeScript SDK | grovv's stack is TypeScript and Go, and production-first forbids pseudo-code. The source's Python is re-expressed, not copied |

The extraction call in grovv's own idiom, which is the shape the generated reference code takes:

```ts
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

// `client` is the configured Anthropic SDK client.
const response = await client.messages.parse({
  model: EXTRACTION_MODEL,
  max_tokens: 2048,
  messages: [{ role: "user", content: renderExtractionPrompt(text) }],
  output_config: { format: zodOutputFormat(ExtractedGraphSchema) },
});

if (response.stop_reason === "max_tokens" || response.parsed_output === null) {
  throw new ExtractionError(documentId, response.stop_reason);
}
return response.parsed_output;
```

Two API details the source predates and the reference code must respect. The top-level `output_format` parameter is deprecated API-wide; `output_config.format` is the canonical form on `messages.create()`. The playbook's Python survives unchanged only because it calls `messages.parse()`, which still accepts `output_format` as a convenience. And a new schema incurs a one-time compilation cost followed by a 24-hour schema cache, so a large backfill should warm the schema on one document before fanning out. Structured outputs are also incompatible with citations and with message prefilling.

### Three corrections to the source

These are not stylistic. Propagating them unchanged would ship wrong guidance.

Cost. The source says "for a corpus of 10,000 documents averaging 2,000 tokens each, the extraction cost at Haiku rates is measured in single-digit dollars." That is off by roughly an order of magnitude. Ten thousand documents at 2,000 tokens is 20 MTok of input; at the published Haiku 4.5 input rate of $1 per MTok that is $20 before a single output token. Structured extraction output of a few hundred tokens per document adds several MTok at $5 per MTok, putting the realistic total in the tens of dollars, roughly halved by the Batches API. The generated prompt must show this arithmetic and instruct recomputation against current published rates rather than repeating either figure.

Prompt caching. The source says "cache the system prompt and schema, pay full price only for the document text," on a pipeline whose extraction stage runs on Haiku 4.5. On that model the advice silently does nothing. The minimum cacheable prefix is model-dependent and not monotonic across generations:

| Model | Minimum cacheable prefix |
|-------|--------------------------|
| Opus 5, Fable 5 | 512 tokens |
| Opus 4.8, Sonnet 5, Sonnet 4.6 | 1024 tokens |
| Opus 4.7 | 2048 tokens |
| Haiku 4.5 | 4096 tokens |

The playbook's extraction prompt plus its schema is a few hundred tokens — far below Haiku 4.5's 4096-token floor. Nothing raises an error; `cache_creation_input_tokens` is simply 0. Verify with `usage.cache_read_input_tokens` across repeated calls: if it stays at 0, the prefix is too short or a silent invalidator is present. Caching begins to pay only once the shared prefix genuinely exceeds the floor — a long domain preamble or a few-shot block will do it — and then the economics are cache reads at roughly 0.1x base input against writes at 1.25x (5-minute TTL) or 2x (1-hour TTL), breaking even at two requests and three requests respectively.

That leaves Batches as the only extraction-cost lever on this pipeline that works as advertised: a confirmed 50% reduction on all token usage, conditional on tolerating up to 24 hours of latency, with most batches finishing inside an hour. Batch results arrive in any order and must be keyed by `custom_id`; a batch holds up to 100,000 requests or 256 MB and results stay available for 29 days. Two things are rejected on Batches and matter here: the `fallbacks` parameter, and `max_tokens: 0` cache pre-warming.

Resolution's motivating example. The source says string similarity "fails on 'Edwin Aldrin' vs. 'Buzz Aldrin' — two names with zero character overlap." The two strings share the token "Aldrin," and four pages later the same document recommends blocking on "same last name," a cheap deterministic signal that would group exactly this pair. The accurate claim is narrower: first-name variants defeat given-name matching and edit-distance thresholds tuned for typos. The case for LLM resolution is unaffected — Section X already rests it on nicknames, abbreviations, and cross-lingual variants — but the "zero character overlap" framing must not travel into a generated skill's rationale.

### The ask-first script

Two stages. Stage 1 spends no user turn.

Stage 1, evaluated silently by the agent at Step 6 against `docs/product-spec.md` and `docs/tech-spec.md`, both of which already exist by then:

1. Does the product ingest a body of documents, records, or sources that users or agents ask questions about? Not "does it have a database" — does it have a corpus. If no, stop. Generate nothing, ask nothing, move on.
2. Given yes, does at least one of these hold? Answers require chaining facts across two or more documents, where neither alone contains the answer. Or multiple agents need a shared world model that outlives their context windows, or an evaluator needs traceable facts to check against. If neither holds, stop — record the alternative (RAG, RAG with reranking, or direct context) and why. A corpus alone is not sufficient reason; single-hop retrieval over a corpus is RAG's job.

In adopt mode the specs at Step 6 were written minutes earlier from an existing codebase, so Stage 1 gains a third question, evaluated from the Step 0 assessment: what retrieval does this project already have? If a vector store, a RAG layer, or a graph is already in place and working, the capability stops being a generation decision and becomes an adoption-plan item. It goes to the user as a proposal with its interaction with the existing layer stated, and nothing is generated until the plan is approved. This is the repo's standing never-overwrite-working-code rule applied to a subsystem that is easy to duplicate by accident.

Stage 2, reached only when the conditions hold. This is the one confirmation turn the capability ever costs.

1. Orient against the decision table: name the corpus, name the multi-hop or shared-state need, and name the row it matches.
2. Corpus and volume: roughly how many documents, and how do they arrive — a fixed set, a steady trickle, or a bulk backfill followed by incremental updates? This sizes the per-run cap and decides whether the Batches path is needed.
3. Cost envelope, with real numbers: extraction is roughly one model call per document, ongoing; querying costs per question. State the computed unbatched figure. Quote the batched figure only after confirming the ingest can tolerate up to 24 hours of latency — if it cannot, the 50% discount does not apply and the unbatched figure is the one to agree to. Then ask whether that envelope is acceptable and whether there is a monthly ceiling to encode as a cap.
4. The honest out, asked last and asked plainly: the alternative is RAG over the same corpus — cheaper, simpler, no ingest pipeline to operate, no evaluation harness to maintain. It cannot chain facts across documents and cannot give an evaluator traceable ground truth. If the multi-hop need is a nice-to-have rather than core, RAG is the better call. Which is it?

On yes, proceed to the guardrails: API key available, per-run cap agreed on both documents and entities, schema version pinned, and a hand-labelled gold set for at least two representative documents committed to before the first production ingest.

On no at any point after condition 1 has passed, record one line in the tech spec naming the alternative and why, tick the Step 6 checklist item, and return. Declining is a successful outcome of this step, not a skipped one. The line is what makes a wrong decline visible to a human later; where there is no corpus at all, condition 1 fails silently and nothing is written.

Step 7 asks a different, narrower question during team design, phrased to consume the Step 6 outcome rather than re-litigate it: do the workers need to chain facts across sources, refer to the same real-world entities under different names, or share structured state that outlives their own context windows — or is passing results through the orchestrator sufficient? Sufficient is the usual answer.

### Artifacts

| Path | New or edit | Axis | Purpose | Size |
|------|-------------|------|---------|------|
| `.claude/agents/testing.md` | Edit | B | Rewrite `:60` (literal text in Phase 1 below) plus a new section on evaluating non-deterministic output: gold set, precision and recall, prompt as unit under test, regression gate rather than absolute threshold, scorer-in-CI versus evaluation-on-demand. One Testing Tools row | +18 on 95 |
| `.claude/agents/code-review.md` | Edit | B | Rewrite `:41` so it does not contradict the testing agent (literal text in Phase 1 below), plus a new `### Grounding` checklist group: claims cite a checkable locator; the locator is opened and checked; a claim with no supporting artifact is flagged unverified and escalated; contradictions name the contradicting evidence. Unconditional, mentions no graph. One Review Style bullet | +10 on 79 |
| `docs/prompts/team-design.md` | Edit | B | The shared-state question in Ask Before Generating (`:45-49`); a Data-Passing Between Agents section naming a shared store as a fifth strategy alongside harness's four, with the three-condition promotion rule stated below; provenance on every cross-agent artifact; three checklist items at `:112-122` | +28 on 131 |
| `docs/prompts/skills-builder.md` | Edit | A | A `## Conditional Skills` tier whose first sentence is "the default is not generated," carrying the gate; two Covers-column cells; a third embedded ask-first rule at `:119-124`; one checklist item | +18 on 201 |
| `docs/prompts/knowledge-graph.md` | New | A | The whole output axis: decision table, four stages, reference code, storage DDL, guardrails modelled on linear-tracking's, evaluation harness, four production signals, a heuristics-not-defaults quarantine table, deliverable checklist | ~210 |
| `grovv-stack-scaffold.md` | Edit | A | Step 5 subsection for the new prompt (placed last, after `:366`); a conditional-skill paragraph after the baseline table at `:340`; tree and reference-table rows; one Step 7 data-passing sentence; the adopt-mode carve-out; Success Criteria count and one conditional item | +24 on 576 |
| `CLAUDE.md` | Edit | A | The new default-off non-negotiable; a Repository Map row; one clause on the Step 6 gloss. The "Steps 1-9" range at `:21` is unchanged | +4 on 137 |
| `.claude/CLAUDE.md` | Edit | A | Tree entry at `:82-88`; extend Prompt Execution Order item 2 at `:120` rather than adding a sixth item; a Key Directives mirror; `ANTHROPIC_API_KEY` in the env reference | +7 on 259 |
| `README.md` | Edit | A | The inline prompt list at `:52`; one gloss sentence; one non-negotiable bullet. The arrow chain at `:60` is unchanged | +3 on 89 |
| `.claude/skills/grovv/SKILL.md` | Edit | A | One gloss sentence after the arrow chain. The chain, the step range, and the frontmatter description are unchanged | 1 line |
| `.claude/agents/database.md` | Edit | A | Four schema principles: graph-shaped data normalizes to a small set of tables with recursive CTEs under a depth cap; provenance on derived rows; version the extraction schema alongside its data; resolution writes to an alias table rather than mutating canonical rows | +5 on 67 |
| `.claude/agents/backend.md` | Edit | A | Two Key Rules: model-backed ingest runs as a PostgreSQL-native job with a per-run cap on both documents and records, existing before the first production run; extraction results and the cursor advance commit in one transaction | +3 on 77 |
| `docs/prompts/linear-tracking.md` | Edit | B | One conditional bracketed line in the MEMORY.md template's Current State at `:126-128`, plus one maintenance sentence stating that a graph is a project artifact, not a third memory tier | +3 on 224 |
| `.claude-plugin/plugin.json` | Edit | D | Version 0.3.0 to 0.4.0 at `:5`; repair the `:6` description, which omits Linear and MEMORY.md; add a keyword. The `agents` array at `:29-36` is untouched | 3 lines |
| `.claude-plugin/marketplace.json` | Edit | D | Drift repair only: `:14` omits the Linear tracking that `:8` includes | 1-2 lines |
| `MEMORY.md` | Edit | D | Version at `:35`; a two-line dated Decision Log entry referencing the Linear issue by identifier; add the new prompt to the propagation grep list at `:55`. Line `:36` ("Steps 0-9") is deliberately unchanged | +4 on 69 |

### Propagation checklist

Required edits:

- Prompt-document set, five to six, in eight enumerations. Three currently hold exactly five: `grovv-stack-scaffold.md:103-107` (directory sub-tree, bare fence — match it), `grovv-stack-scaffold.md:564` (Success Criteria), `README.md:52`. Two hold six because they also list `tech-spec-template.md`: `CLAUDE.md:37-42`, `.claude/CLAUDE.md:83-88`. One is the five-item Prompt Execution Order at `.claude/CLAUDE.md:119-123`, where the new prompt extends item 2 rather than becoming item 6. One is the five `####` subsections under Step 5 at `grovv-stack-scaffold.md:323`, `:354`, `:358`, `:362`, `:366`, which gains a sixth placed last. One is not a count at all: the File and Folder Reference table at `grovv-stack-scaffold.md:129-146` lists only two prompt files, `:140` and `:141`, and a third row is optional there.
- Baseline skill enumerations, four locations. `grovv-stack-scaffold.md:329-340` (Step 5 baseline table) and `docs/prompts/skills-builder.md:62-73` (baseline skill table) each gain a pointer to the conditional tier below the table. The two directory trees — `grovv-stack-scaffold.md:111-120` and `docs/prompts/skills-builder.md:14-45` — are verified unchanged: they depict the baseline, and the conditional skill is by definition not part of it. State that decision in the tier's own text so the next reader does not treat the trees as stale.
- The new non-negotiable in all three mirrors, written to each list's own idiom: `CLAUDE.md:88-96`, `README.md:75-80`, `.claude/CLAUDE.md:208-217`. Plus embedded as an inherited rule at `docs/prompts/skills-builder.md:119-124`.
- Glosses only, never the chains. The arrow chains at `.claude/skills/grovv/SKILL.md:48` and `README.md:60` stay identical in shape to each other and are not edited.
- Version in two places, same session: `.claude-plugin/plugin.json:5` and the prose mirror at `MEMORY.md:35`.
- `ANTHROPIC_API_KEY` added to the env block at `.claude/CLAUDE.md:221-256`. This is not a repo-wide gap — `docs/prompts/tech-spec.md:290` already carries it under an `# AI Services (as needed)` header at `:289`. It is drift between two of the repo's three env references, and this closes it.
- JSON drift repair while those files are open: `plugin.json:6` omits Linear and MEMORY.md; `marketplace.json:14` omits Linear tracking that `:8` includes.

Verify unchanged, edit nothing:

- Step numbering. 36 lines across 8 files, plus 1 line of file-internal numbering at `docs/prompts/linear-tracking.md:34` that is unrelated. Zero in JSON. If any needs changing, the implementation has drifted from this plan — re-examine rather than patch. Leave `.claude/agents/scaffold.md:25-36`'s pre-existing off-by-one (a "Steps 0–9" heading over a list numbered 1 to 10) alone; that is a separate commit.
- Agent roster. Seven explicit enumerations — `.claude-plugin/plugin.json:29-36`, `.claude/CLAUDE.md:71-77` (tree), `.claude/CLAUDE.md:102-109` (table), `CLAUDE.md:43`, `README.md:70`, `docs/prompts/team-design.md:31`, `grovv-stack-scaffold.md:385` — plus a prose count of "six" on twelve lines (thirteen instances; `.claude/CLAUDE.md:111` carries two): `MEMORY.md:38`, `README.md:54`, `README.md:60`, `CLAUDE.md:122`, `.claude/skills/grovv/SKILL.md:48`, `.claude/CLAUDE.md:111`, `docs/prompts/team-design.md:31`, `:33`, `:49`, `:113`, `grovv-stack-scaffold.md:356`, `:385`. No agent is added, so none of these move. Do not confuse them with `team-design.md:5`, `:66` and `:77`, which count harness's six architecture patterns.
- Stack tables. Fifteen, plus two prose copies invisible to a table-shaped grep (`grovv-stack-scaffold.md:347` and `docs/prompts/skills-builder.md:114`). Nine describe grovv's own defaults: `grovv-stack-scaffold.md:451-465`, `CLAUDE.md:69-84`, `.claude/CLAUDE.md:42-57`, `.claude/agents/scaffold.md:52-63`, `backend.md:15-27`, `database.md:15-21`, `testing.md:33-38`, and `frontend.md:28-35` and `:48-55` (the Astro and Next.js options). Six are target-project templates inside the generator prompts: `docs/prompts/tech-spec.md:106-112`, `:116-122`, `:126-134`, `:138-142`, `:146-155`, and `docs/prompts/readme-generator.md:122-128`. No Knowledge Graph row anywhere. Only `testing.md`'s Testing Tools table gains a row, and that is a tool, not a stack default.
- Env-variable reference blocks. Three: `.claude/CLAUDE.md:221-256` (edited above), `docs/prompts/tech-spec.md:244-292` (already correct), and `docs/prompts/readme-generator.md:131-163`. The last is verified unchanged by decision: it is the template for a generated project's README, which should document only the keys that project actually uses.
- The two legacy-idiom files, `docs/prompts/tech-spec.md` and `docs/prompts/tech-spec-template.md`, are otherwise deliberately untouched.

Forbidden:

- No file under `.claude/skills/harness/` may be edited. `ATTRIBUTION.md:15` pins the upstream commit and `:35` states that the workflow body and the `references/` files must not be hand-edited; `:41-48` records the only two deliberate localizations, both in `SKILL.md` frontmatter and preamble. The workflow body and every `references/` file are verbatim, which is exactly what the data-passing table at `SKILL.md:228-233` falls under. The temptation is acute — that table is one row short of the point. The extension goes in `docs/prompts/team-design.md`, which designates itself as the place to extend harness behavior. Run `git status` before committing and confirm nothing under that directory appears in the diff.

Convention checks before commit: horizontal rules are exactly five dashes; directory trees use bare fences while code fences always carry a language hint; no emoji in headings; the wordmark takes doubled backslashes in prose and single backslashes inside code fences. The two files most likely to get the wordmark wrong are the new prompt (if it carries any fenced template) and `docs/prompts/linear-tracking.md`, whose MEMORY.md template fence already carries the correct single-backslash form at `:149` and must not be "corrected."

### Phased rollout

| Phase | Delivers | Size |
|-------|----------|------|
| 1 — Grounding discipline | Edits only, three existing files: `.claude/agents/testing.md`, `.claude/agents/code-review.md`, `docs/prompts/team-design.md`. Zero new files, zero enumeration edits, no cascade | ~55 lines, half a day |
| 2 — The gate and the prompt document | New `docs/prompts/knowledge-graph.md`; the Conditional Skills tier and the rest of the `skills-builder.md` edit; the master-directive edits including the adopt-mode carve-out; the new non-negotiable in three mirrors; the eight prompt-set enumerations; the two baseline-table pointers; the version bump and JSON repairs; the MEMORY.md entry | ~210 new lines plus ~45 lines of edits across 9 files, one to two days |
| 3 — Reference payload and agent patterns | The references the prompt points at, written into target projects: pipeline, evaluation, storage. Plus `database.md`, `backend.md`, and the `linear-tracking.md` pointer | ~600-800 lines generated into targets plus ~11 lines of edits, three to five days |

Phase 1 stands alone and is startable as written. It could ship before Phase 2, or instead of it. Every line of it applies to every project grovv scaffolds, including every project that will correctly decline a graph forever, and it is the best value-to-blast-radius ratio available: about 55 lines against zero cascade risk, zero new files, zero renumbering, zero manifest changes. If exactly one phase is approved, approve this one. Its three deliverables are specified to the line below.

Deliverable 1 — replace `.claude/agents/testing.md:60`:

```markdown
- Tests must be deterministic — no flaky tests. Deterministic units get equality
  assertions. Model-backed output is scored instead: a hand-labelled gold set,
  precision and recall, and a gate on no regression against the last recorded
  score rather than an absolute threshold. The scorer is a pure function of
  (predicted, gold, alias map) and is unit-tested in CI; the evaluation itself
  calls the live API and runs on demand and on every prompt or model change,
  never on every push.
```

Deliverable 2 — replace `.claude/agents/code-review.md:41`, which today carries the same rule as a blocking review checkbox and would otherwise flag the evaluations the testing agent has just been licensed to write:

```markdown
- [ ] Tests are deterministic and not flaky — or, for model-backed output, scored
      against a hand-labelled gold set with a no-regression gate, with the scorer
      itself unit-tested
```

Deliverable 3 — the data-passing extension in `docs/prompts/team-design.md`. The vendored harness table at `.claude/skills/harness/SKILL.md:228-233` enumerates four strategies: message-based (`SendMessage` between team members, team mode), task-based (`TaskCreate` and `TaskUpdate` carrying shared task state, team mode), file-based (write and read at agreed paths, both modes), and return-value-based (the `Agent` tool's return message, sub-agent mode). The new section names a fifth — a shared store outside any context window, queried by slice — and gates promotion to it on all three of the following holding at once:

1. Three or more agents must read state that another agent produced, not merely report it upward to the orchestrator.
2. The state outlives a single agent's context window: a later phase, a later run, or a later session reads it.
3. Consumers need provenance — which agent wrote a fact, from which artifact, and when — in order to act on it.

Fewer than all three, and file-based passing plus return values is sufficient and cheaper. All three, and the orchestrator must name the store, its schema, and its provenance fields in the generated orchestrator skill. The connecting, compressing, grounding triad from Appendix B is the rationale to carry into that section: a shared store earns its cost when it links entities across agents that never communicated, when it lets a synthesizer read structured facts instead of raw outputs, and when every fact it holds traces to a source.

Phase 3 carries the largest quality risk, because it means writing a resolver, summarizer, assembler, and scorer that the source never shows, in a language it never uses, to a bar that forbids pseudo-code. The SDK call shape is now verified; the four missing stages are not.

-----

## What We Are Deliberately Not Doing

| Rejected | Reason |
|----------|--------|
| A new numbered pipeline step | A number in the master directive means "every project runs this," which is the wrong default. See below |
| A seventh baseline agent | Seven roster enumerations, thirteen prose counts of "six," and the `agents` array in `plugin.json` — one JSON file, not two. Doctrinally wrong besides: harness holds that skills are how and agents are who (`SKILL.md:179`), and a four-stage extraction pipeline is overwhelmingly how |
| A Knowledge Graph row in the stack tables | Those tables are defaults. A row there tells every future agent a graph is part of a grovv project's expected shape. See below |
| An eleventh row in the baseline skill table | It silently inverts the gate. `skills-builder.md:60` and `:191` already sanction dropping irrelevant baseline skills, so a baseline row makes the graph opt-out. A separate tier whose first sentence is "the default is not generated" makes it opt-in |
| Hiding the depth under `.claude/skills/grovv/references/` | Conflates the kickoff skill's own depth with instructions for generating target-project artifacts, and rests discovery on one soft pointer with no error signal if a future edit orphans it |
| Amending the vendored harness data-passing table | Breaks the vendoring contract at `ATTRIBUTION.md:35` and would be silently reverted by the next re-vendor. The extension belongs in `team-design.md` |
| A graph over grovv-stack's own artifacts | The corpus fits in one context window and grep already answers every traversal question. See below |
| A SessionStart hook surfacing a graph digest | Implies a queryable store, therefore a runtime and a dependency. Wrong shape in a target project too: a digest is a cost paid on every session and is exactly the fragile summary the source diagnoses |
| The graph as an unconditional third memory tier | Taxes every project for the few with both a graph and an overnight loop. The Linear/MEMORY.md split is a dated decision restated in four files, and MEMORY.md has a hard line budget. One conditional line covers what a fresh session needs |
| Shipping the source's numeric thresholds as validated defaults, or its unbuilt extensions as patterns | Degree 3, k=2, blocks of 50-100, the density and compression bands, "a few hundred thousand edges" — all asserted, none measured, with the Apollo corpus supplying a single density datapoint. Temporal graphs, edge confidence scoring, and graph-of-graphs are flagged by the source itself as unbuilt future directions. Thresholds ship in a clearly-labelled heuristics section; the extensions do not ship at all |
| Quoting the reported F1 and precision numbers as benchmarks | Two of six documents scored, no relation-level numbers, no resolved F1, and resolution showing zero measured effect on recall in both rows. The precision-over-recall asymmetry argument is kept and attributed as a reasoning argument, not a measurement |
| A third universal ask-first rule | The two existing rules earn universality because nothing in a spec tells you Astro versus Next.js, or which flows deserve E2E coverage. A spec does tell you whether there is a corpus and whether questions chain across it |
| A `scripts/` directory holding a runnable scorer | Sanctioned by harness at `SKILL.md:127` as a skill sub-directory, so it would look correct — but it is executable code with dependencies in a repo whose output is documents. The scorer belongs in the target project |
| Conditional placeholders in the tech-spec prompts | Taxes every project's spec template for a subsystem most decline, and both files are legacy-idiom, so editing them invites style drift or an out-of-scope modernization |
| Knowledge-graph trigger phrases in the kickoff skill's frontmatter | The description is the skill's only trigger mechanism and its job is routing. A graph is an output of the pipeline, not an entry point to it |
| Fixing the unrelated drift discovered while surveying | `scaffold.md`'s missing stack rows, its off-by-one scaffolding order, and `linear-tracking.md:165`'s bare `cat MEMORY.md` hook are real bugs and none belong in this change. The two JSON description drifts are repaired only because the propagation work forces those files open anyway |

The three longest arguments, in prose rather than in cells.

A new numbered pipeline step. The decisive objection is semantic. `grovv-stack-scaffold.md` is read end-to-end before any file is written, on every invocation, for every project — including the large majority that will decline a graph. A numbered step is a promise that the step runs, and a permanent lengthening of a document whose cost is paid by every project. The mechanical cost is a supporting argument only, and smaller than it first appears: appending a Step 10 would touch six step-range expressions and one agent list, not all 36 numbered references, and the JSON manifests carry no step numbers at all. A conditional branch inside Step 6 delivers identical capability, encodes the right default, and costs three lines in the master directive.

A Knowledge Graph row in the stack tables. Correctness before cost. Every other row in those tables is something a typical grovv project actually uses; listing a graph among them contradicts the gate in the same repository that defines it. The cost argument is secondary but real, and larger than an earlier draft claimed: fifteen stack tables plus two prose copies, and the repo demonstrably cannot keep them in sync. `.claude/agents/scaffold.md:52-63` is already missing three rows against `grovv-stack-scaffold.md:451-465` — Project Tracking, Background Jobs, and Dev Environment — and `docs/prompts/skills-builder.md:114` hides another copy as prose where no table-shaped grep will find it. A sixteenth row on a known-broken surface has negative expected value.

A graph over grovv-stack's own artifacts. The clearest no. Excluding this document, the corpus is eighteen Markdown files and about 3,500 lines, plus two small JSON manifests; the vendored harness tree adds another 2,300 lines of third-party skill nobody would want indexed. It fits in one context window. Every cross-reference is already an explicit Markdown link or path, and grep answers every traversal question a graph would, deterministically and for free. Building it requires exactly the dependency this repo forbids. By the source's own criterion — the graph earns its complexity when the alternative exceeds the window or loses the connections — neither condition holds. Revisit only if the repo outgrows what a single session can hold.

-----

## Open Questions

- Is a silent false negative on the gate acceptable? Because the agent evaluates the conditions itself rather than asking, a project that would genuinely benefit may never hear the option exists. A false positive costs one confirmation turn and is trivially reversible; a false negative is invisible to everyone. Currently: a one-line "considered a knowledge graph and chose X because Y" note is required in the tech spec whenever the product has a corpus at all, which is where the misjudgement can occur. Products with no corpus produce no line.
- Should the roughly 210-line prompt document ship to targets that declined? Step 5 copies the prompt set into every target project. Shipping unconditionally means the decision table travels with the project and the choice can be revisited later; not shipping means less bloat for the majority but complicates Step 5's otherwise simple contract. Currently: ships unconditionally.
- Which model for resolution? The source never versions Sonnet. Resolution is where errors are hardest to detect and most damaging — silent node loss and over-merging both fail quietly — which argues for a more capable model there specifically. But the source's entire cost argument rests on the cheap-extraction, capable-synthesis split. Currently: keep the two-model story, and flag resolution as the first place to spend on a more capable model if spot-checks find over-merging.
- How is the reference TypeScript validated before it ships? The SDK call shape is verified, but Phase 3 still requires a resolver, summarizer, assembler, and scorer the source never shows, in a language it never uses, to a bar that forbids pseudo-code — and grovv-stack has no test infrastructure and cannot gain any. Currently: narrow Phase 3 to schemas, prompts, storage DDL, and decision rules, and mark any full-stage implementation explicitly as unvalidated reference until it has been run in a throwaway project.
- Does a Conditional Skills tier of one justify itself as a precedent? With a single entry it is obviously right. With four it becomes a second baseline set with its own drift surface and its own gating logic. Currently: the tier's own text requires whoever adds the second entry to re-argue the tier rather than inherit it, and that requirement is written into `skills-builder.md` now, while there is exactly one.
- Should grovv define an ADR format for target projects? This document settles the format for `docs/architecture/` here by example, but `grovv-stack-scaffold.md:129-146` promises target projects an ADR folder without ever defining what goes in it. Currently: grovv-stack only, gap flagged; a target-project ADR template is out of scope for a knowledge-graph decision.
- How should the corrected cost figure be published? Stating the arithmetic and the rate inputs is the most honest and the most verbose; stating only the method forces a lookup; stating the figure with a dated verification caveat ages badly. Currently: arithmetic shown, with the rate inputs named and a recompute instruction attached.
- Should the generated skill carry removal instructions? The gate governs generation, not deletion. A project that generates the skill and later abandons the idea keeps a several-hundred-line skill whose pushy trigger description will keep firing. Currently: a one-line removal note ships with the skill, accepting that skill-removal guidance is a pattern the repo has not used anywhere else.
- @TODO Confirm current per-MTok rates and the Haiku extraction model's availability at implementation time, immediately before the cost arithmetic and the model pin are written into `docs/prompts/knowledge-graph.md`. The rates used above are the published figures at the date in the colophon.

-----

## Colophon

| Field | Value |
|-------|-------|
| Version | 0.2.0 |
| Last Updated | 2026-07-25 |
| Status | Draft |
| Author(s) | grovv stack scaffolding agent |
| Model | Claude (Claude Code) |

-----
gro\\/\\/ stack — Knowledge Graph Engineering
