# Knowledge Graph Engineering for Multi-Agentic Systems

An assessment of the knowledge-graph playbook and a scoped plan for absorbing it into gro\\/\\/ stack.

Source document: "Knowledge Graph Engineering for Multi-Agentic Systems: The Anthropic Playbook," a 12-page independent synthesis compiled July 2026. It is not a publication of Anthropic and is not affiliated with or endorsed by Anthropic — it says so twice, on its cover page and in its page-12 footer. It synthesizes Anthropic's public `claude-cookbooks` knowledge-graph material, "Building Effective Agents" (Schluntz and Zhang, Dec. 2024), a 2026 architecture-patterns document, and the Managed Agents writing. Its code is described as "adapted from the public cookbook for pedagogical clarity" — adapted, not byte-identical. Its measured results come from a six-document Wikipedia corpus, of which only two documents were scored. Treat it as a well-argued design note with a toy evaluation, not as a specification.

-----

## Summary

### The playbook in about 200 words

The playbook collapses classical knowledge-graph construction — trained NER, a trained relation classifier, and hand-written entity-resolution heuristics — into four prompted stages over one Pydantic schema. Extraction (Haiku, one call per document, structured output) returns typed entities and subject-predicate-object triples. Resolution (Sonnet, one call per entity type) clusters raw surface forms into canonical nodes using the one-line descriptions written during extraction, catching cases with zero character overlap that string similarity cannot. Assembly is deterministic; summarization (Sonnet) synthesizes profiles for high-degree hub nodes only. Querying serializes the k-hop neighborhood of a seed entity as triples and constrains the model to answer using only those edges, citing them.

The structural claim is that structured outputs make the interface between stages a type-checked contract rather than a parsing hope, which is what makes the pipeline viable at thousands of documents rather than ten. The multi-agent claim is that the graph is shared memory for orchestrator-workers, ground truth for an evaluator, and a world model that survives context flushes. An evaluation harness — hand-labelled gold set, precision and recall, rerun on every prompt change — is presented as the thing that separates a demo from a production system.

### The integration recommendation in about 150 words

Adopt the grounding discipline unconditionally; gate the graph itself.

The grounding discipline — factual claims cite a checkable locator, non-deterministic output is scored against a hand-labelled gold set rather than asserted with equality checks, every cross-agent artifact carries provenance — is roughly 60 lines across four existing files, needs no infrastructure, and improves every project grovv scaffolds. It also fixes an active defect: `.claude/agents/testing.md` currently says "Tests must be deterministic — no flaky tests" with no carve-out, which is wrong guidance for any project shipping a model-backed feature.

The graph itself becomes a conditional capability behind a two-condition gate evaluated at Step 6, with depth in one new prompt document. No new numbered pipeline step. No seventh agent. No row in any stack table. The playbook's own decision table says most systems should not build a graph, and grovv should honour that by default.

-----

## Part One: What the Playbook Says

### The four-stage pipeline

| Stage | Model | Input | Output | Why this model |
|-------|-------|-------|--------|----------------|
| Extraction | Haiku (`claude-haiku-4-5`, the only concrete model id in the document) | One document at a time | Typed entities plus S-P-O triples, validated against `ExtractedGraph` | "High volume, schema-constrained; speed and cost dominate." Cost is linear in corpus size, so this stage must be the cheap one |
| Resolution | Sonnet (never versioned) | All raw entities of one type, with descriptions | Alias map: canonical name plus every surface form | "Weighing conflicting evidence; reasoning quality dominates." One call per entity type per pass, not one per document |
| Assembly and summarization | None for assembly (deterministic); Sonnet for summarization | Canonicalized relations; then hub-node mentions plus neighborhood | `MultiDiGraph`; `EntityProfile` for high-degree nodes only | "Synthesizing across documents; nuance matters." Applied selectively, so total cost is sublinear in corpus size |
| Querying | Sonnet (referenced only as `SYNTHESIS_MODEL`, never bound) | Question plus a serialized k-hop subgraph | Prose answer citing specific edges | "Multi-hop reasoning over serialized triples." Cost is proportional to subgraph size and dominates for a heavily-queried graph |

The two-model split is the cost argument. Extraction dominates for a large corpus; querying dominates for a heavily-queried one. Optimizing them independently is the stated reason the split matters.

### The schemas

Reproduced from the source. The exact wording is the technique — the schema is described as "the training data for the extractor."

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

`EntityType` is a closed five-value literal. Widening it is the first thing a domain adaptation does, and the playbook's own illustrative example adds `PRICING`, `FEATURE`, and `FILING`.

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
        model=EXTRACTION_MODEL,  # claude-haiku-4-5
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

On the six-document Apollo corpus: 22 nodes, 34 edges, one connected component, ratio 1.55, two hub nodes at degree 9. All of these numbers are toy-corpus observations, not thresholds.

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

That citation format is the point. It produces answers of the form `(Armstrong) --[walked on]--> (Moon)` rather than prose claims, which makes verification a string match against the input. This is what distinguishes graph-grounding from RAG-grounding: with RAG the context is a blob of retrieved text that may or may not contain the supporting evidence; with a graph the context is a set of explicit triples each carrying provenance.

The grounded-versus-ungrounded comparison is narrated, not scored. Without graph context the model produces a comprehensive, plausible answer from pretraining. With it, the answer is constrained to extracted edges and explicitly flags what the graph does not contain. The verdict: "less impressive but infinitely more useful... On a private corpus, only the second kind of answer works at all."

The k tradeoff: k=1 is fast and focused but misses indirect connections; k=2 is called the sweet spot for multi-hop questions; k=3 and beyond grows the subgraph rapidly and may exceed the context window. No token budget, measured subgraph size, or overflow strategy is given — the problem is named and left unsolved.

The production recommendation: return the serialized subgraph alongside the answer, so the calling agent or human sees exactly which edges were available.

### Section VII: the agent patterns table

This is the load-bearing section for grovv, and also the least evidenced.

| Pattern | Graph role | How it helps |
|---------|-----------|--------------|
| Augmented LLM | Retrieval source | Graph traversal replaces vector search for multi-hop questions; the LLM queries the graph as a tool |
| Prompt chaining | Gate signal | Between chain steps, a graph query checks whether new entities conflict with existing nodes. The graph is the programmatic gate |
| Routing | Classifier input | Entity type and degree route a query to the right specialist without an LLM call. Deterministic, zero tokens |
| Orchestrator-workers | Shared memory | Workers read the subgraph relevant to their task and write new entities and relations back. The orchestrator's context stays small; shared state lives in the graph |
| Evaluator-optimizer | Grounding layer | The evaluator queries for the specific triple the generator claims and checks whether it exists, with what predicate, from which source. Shifts the evaluator from reader to fact-checker |
| Autonomous loops | Persistent world model | The graph survives context-window flushes "the way a state file survives a process restart — the agent forgets, the graph does not" |

The orchestrator-workers argument is the sharpest: passing summaries through the orchestrator's window grows it linearly with worker count, whereas the graph is durable, append-only, and interrogable by slice.

The evaluator-optimizer loop shape: generator produces content; a query stage serializes the k-hop neighborhood of every entity mentioned; the evaluator receives both, checks every claim against edges, and flags claims with no supporting edge; feedback names the contradicting evidence rather than saying "this is wrong"; a claim absent from the graph entirely is escalated to a human rather than silently accepted or rejected.

The worked fact-check — a generator claims "Armstrong commanded Gemini 12," an evaluator with graph access finds no such edge but does find `(Buzz Aldrin) --[flew on]--> (Gemini 12)` and `(Neil Alden Armstrong) --[commanded]--> (Apollo 11)` — is explicitly introduced as "consider a concrete example." It is a hand-constructed illustration, not a logged run. Its value is the shape of the feedback, not evidence that graph-grounded evaluators outperform ungrounded ones. No such comparison is measured anywhere in the document.

Section VII.D extends this to collaborative blackboard and hierarchical segmented-subgraph architectures. That section is one paragraph of assertion with no code, schema, or measurement behind it, and is the part of the document most likely to be over-read as a validated design pattern.

### Evaluation, and what the reported numbers mean

Quality is precision and recall against a hand-labelled gold set, scoring raw extractor output and the same entities after resolution.

| Document | Raw F1 | Precision | Recall | Resolved recall |
|----------|--------|-----------|--------|-----------------|
| Apollo 11 | 0.71 | 1.00 | 0.55 | 0.55 |
| Neil Armstrong | 0.55 | 1.00 | 0.38 | 0.38 |

Only two of the six corpus documents are scored. Perfect precision means the extractor is conservative — everything it finds is correct. The asymmetry argument is the load-bearing claim, and it is a reasoning argument rather than a measurement, which is why it survives the weak evidence: false positives are harder to detect and more damaging than false negatives, because a wrong entity spawns wrong relations that propagate through multi-hop reasoning. A missing entity produces an incomplete but correct graph; a wrong entity produces a graph that actively misleads.

The misses are not model failures. One category is entities mentioned only in passing, which the "central only" instruction correctly filtered. The other is entities from the gold set's broader cross-document scope that were not central to the document being scored — a scope mismatch, not an extraction failure.

Relation scoring is done on `(source, target)` pairs, ignoring predicate wording, because "commanded" and "led" and "was commander of" describe the same relation. That gives an upper bound on relation recall, and is judged sufficient to detect structural errors, which matter more than predicate-wording differences.

The alias-map artifact: when the resolver picks a canonical form the scorer does not recognize, resolved recall can drop. That is a scoring artifact, not a resolver bug, and the fix is to extend the alias map. Note that in both scored rows resolved recall exactly equals raw recall, so this artifact is argued in prose and never demonstrated in the data, and no measured recall improvement from resolution is shown anywhere.

The feedback loop is the stated point of the whole section: change the extraction prompt, rerun the scorer, watch the F1 move. "A team that ships the pipeline without the evaluation harness has no way to know whether prompt changes improve or degrade quality, and no way to catch the slow drift that occurs as the corpus evolves."

### Scaling and cost regimes

| Regime | Shape | Lever |
|--------|-------|-------|
| Extraction | Cheap per document, linear in corpus size | Prompt caching and the Batches API |
| Resolution | Moderate — Sonnet, one call per entity type per pass, not per document | Blocking before arbitration |
| Summarization | Expensive per entity, applied only to high-degree nodes, so sublinear overall | The degree cutoff |
| Querying | Per question, proportional to subgraph size | Pre-computed serialization for high-traffic seeds |

Resolution at scale does not work by feeding ten thousand entities into one prompt. Block first — group candidates by cheap signals such as shared last name, overlapping tokens, or embedding similarity, implemented as an inverted index on name tokens with no model call — then let the model arbitrate within blocks of 50 to 100. The resolution prompt works unchanged on blocks. The generalized principle: keep the model for the parts that require judgment, use deterministic logic for everything else. The document concedes that the clustering prompt is universal but the blocking is not — blocking heuristics remain domain-dependent, and this is the one place a domain-specific engineering burden survives the move to LLMs.

Storage. NetworkX is stated as fine to a few hundred thousand edges. Beyond that, either a property graph or three Postgres tables:

```sql
entities(id, name, type, summary)
relations(source_id, target_id, predicate)
aliases(entity_id, alias)
```

with graph queries as recursive CTEs. "The extraction and resolution code does not change — only the persistence layer does. The choice between them is an infrastructure decision, not a pipeline decision."

Long documents must be chunked at section boundaries with one paragraph of overlap, so that entities and their relations fall within the same chunk. Naive token-count chunking splits entities from their context. The extraction prompt works unchanged on chunks; the extra step is deduplicating entities across chunks of the same document by exact string match before resolution.

Four production monitoring signals: extraction rate (a drop suggests a domain shift the prompt handles poorly, a spike suggests over-extraction of peripheral mentions); resolution compression ratio (near 1.0 means resolution is doing little, high means it is earning its cost); graph connectivity (a growing number of components suggests resolution is missing cross-document links); query latency.

### Operational discipline

Three practices, stated as required before shipping rather than after:

- A daily random-node sample. Pick a node, read its profile, check its edges against the source documents, verify the provenance chain. "The moment you cannot explain why a node has a particular edge, your understanding of the graph has fallen behind its contents."
- A per-run extraction cap on both documents processed and entities extracted, so that an ingestion error cannot produce a run of unbounded cost. It must exist before shipping.
- Schema versioning, where the extraction prompt counts as part of the schema. Entities extracted under different prompts must remain distinguishable, comparable, and re-extractable.

What the graph does not replace is judgment. "The graph is a structured fact store; it does not decide which facts matter, which entities to trust, or which actions to take... The graph moves the basis for these decisions from model estimation to extracted facts, but the decisions themselves remain with the agents — and ultimately with the human who designed them."

And the sharpest line in the document: "the pipeline is not done when it runs; it is done when you can tell, on any given morning, whether what it produced overnight was actually right."

### Appendix C: when not to build a graph

This is the honest part of the document, and the reason grovv can adopt the capability without adopting it by default.

| Scenario | Right tool | Why |
|----------|-----------|-----|
| Single-document QA | RAG or direct context | No multi-hop needed; the answer is in one chunk |
| Multi-document, single-hop | RAG with reranking | The answer spans documents but does not require chaining |
| Multi-document, multi-hop | Knowledge graph | Chaining facts across documents requires entity-level linking |
| Multi-agent, shared state | Knowledge graph | Workers need a shared world model outside context windows |
| Evaluator needs ground truth | Knowledge graph | Fact-checking requires structured, provenance-carrying facts |
| Overnight loop, persistent memory | Knowledge graph | Memory must survive context flushes across sessions |
| Simple classification or routing | Single agent | No cross-document reasoning needed |

The rule of thumb: if agents need to chain facts across sources, share structured state, or ground judgments in traceable evidence, the graph is the right infrastructure. If they need to retrieve passages or classify inputs, simpler tools suffice. "The graph earns its complexity when the alternative — passing raw documents or summaries through context windows — either exceeds the window or loses the connections." RAG and graphs are complementary, not competing.

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
| Resolution effect | Both scored rows show resolution with exactly zero measured effect on recall |
| Code coverage | Two executable functions across twelve pages. No resolver, summarizer, assembler, scorer, blocking, chunking, or persistence code. No error handling, retry, or transaction discipline anywhere |
| Unmeasured thresholds | Degree 3, k=2, blocks of 50-100, edges/nodes bands, compression-ratio bands, "a few hundred thousand edges" — all asserted, none measured |
| Cost arithmetic | "Single-digit dollars for 10,000 documents" is stated with no rate table and no calculation. See the corrections below |
| Section VII.D and XI.F | Collaborative blackboards, hierarchical subgraphs, temporal graphs, confidence scoring, graph-of-graphs — all proposals, no implementations |
| Unsourced figure | "Multi-agent systems outperform single agents by 90.2%" appears with no citation, benchmark, or task definition. Do not repeat it |
| No reference list | Related Work discusses two decades of literature with zero citations. Only four Anthropic sources are named, in the acknowledgment |

-----

## Part Two: What This Means for gro\\/\\/ stack

### Three axes, kept strictly separate

grovv-stack is not an application. It is a prompt-driven scaffolding system shipped as a Claude Code plugin, whose only output is documents and configuration files written into other projects. It has no dependencies, no build step, and no runtime code, and must not gain any. "Integrating the playbook" therefore means exactly three things, and conflating them is the main way this goes wrong.

| Axis | Meaning | Verdict |
|------|---------|---------|
| A — Output | grovv gains the ability to scaffold a knowledge-graph subsystem into a target project: a conditional prompt document, a conditional skill, storage and guardrail patterns in the existing agents | Adopt, gated |
| B — Process | grovv's own pipeline and agent-team design absorb the ideas: grounding for the reviewer, gold-set scoring for the tester, shared-store data passing for the harness | Adopt, unconditional |
| C — Self | A graph over grovv-stack's own artifacts — spec to plan to issue to agent to skill | Decline. See the rejections |

Every line of playbook code becomes reference code inside a generated prompt or skill, destined for the target project. None of it is committed to grovv-stack.

### The step decision

No new numbered pipeline step. The pipeline stays Steps 0-9. The capability is absorbed by Step 6 (skills-builder), which owns the gate and the generation, and Step 7 (team-design), which owns the downstream consequence. Depth lives in one new conditional prompt document that declares itself, in its own first paragraph, to be a conditional sub-step of Step 6 rather than a step.

The justification is arithmetic. Step numbers are referenced by number in at least fifteen locations across nine files: ten step headings, cross-references at `grovv-stack-scaffold.md:184` and `:360`, the "Steps 2-9" range at `:546`, the Success Criteria, `CLAUDE.md:21` and `:61`, `.claude/CLAUDE.md:21`, `.claude/skills/grovv/SKILL.md:20` and `:26-33`, `.claude/agents/scaffold.md:23-36` (already off-by-one against the real numbering), `MEMORY.md:36`, and the preambles and After-This-Step sections of three prompt files. Two of those are JSON manifests no Markdown grep will find. That is a full-day mechanical edit with a high miss rate, in a repo that has demonstrably missed this class of propagation at least three times already, spent to give a dedicated confirmation gate to a capability the playbook's own Appendix C says most systems should not have. A conditional branch inside Step 6 delivers identical capability for three lines in the master directive.

A new numbered step would also permanently lengthen a directive that is read end-to-end before any file is written, on every invocation, for every project — including the large majority that will decline.

The one thing that does change: the prompt-document count goes from five to six in seven enumerations, plus the Step 5 subsection, plus the version bump.

### Playbook default to grovv default

| Playbook default | grovv equivalent | Notes |
|------------------|------------------|-------|
| Pydantic `BaseModel` and `Literal` for the extraction schema | Zod schema with `z.enum([...])` | Zod is a weaker contract here than Pydantic: the supported JSON-Schema subset excludes numeric bounds, string-length constraints, and recursive schemas, so semantic load must ride on description text rather than constraints. Say so rather than papering over it |
| `client.messages.parse(..., output_format=...)` returning `parsed_output` | The TypeScript SDK equivalent | @TODO Verify the exact parameter name, the Zod-to-output-format helper, and the nullability of the parsed result against the current SDK reference before writing any reference code. Do not copy the source's call shape — it is from a July 2026 document and the parameter naming has moved. No signature is asserted in this document |
| `claude-haiku-4-5` for extraction | Unchanged | The only concrete model id in the source. Pin deliberately and verify availability before writing |
| "Sonnet" for resolution, summarization, querying | A current Sonnet, pinned explicitly | The source never versions Sonnet and never binds `SYNTHESIS_MODEL`. This is a mapping decision, not a transcription. See the open questions on whether resolution warrants a more capable model |
| NetworkX `MultiDiGraph` in memory, Postgres as a scale-up path | PostgreSQL from day one, four tables not three | grovv already defaults background jobs to PostgreSQL-native rather than reaching for a specialist store. The source's three tables are insufficient: incremental update, the per-run cap, and provenance all require a document/ingest-cursor table it never mentions. Traversal as recursive CTEs with an explicit depth cap |
| "The cookbook's evaluation script" (no code shown) | Vitest, split in two | The scorer is a pure deterministic function over predicted, gold, and alias map, and is unit-tested in CI. The evaluation calls the live API, costs money, and runs on demand and on every prompt or model change — never on every push. This split is what makes the harness compatible with grovv's existing "no flaky tests" rule instead of contradicting it |
| "Extract, resolve against the existing canonical set, add new edges" | A PostgreSQL-native background job using `SKIP LOCKED` | Extraction results and the ingest-cursor advance commit in one transaction, matching grovv's zero-data-loss rule and its existing Lago same-transaction rule |
| Four monitoring signals described in prose | Four PostHog events with properties, one insight each | Straight mapping onto grovv's existing observability default. No new stack entry needed |
| Python throughout | TypeScript with Zod and the Anthropic TypeScript SDK | grovv's stack is TypeScript and Go, and production-first forbids pseudo-code. The source's Python is re-expressed, not copied |

### Two corrections to the source

These are not stylistic. Propagating them unchanged would ship wrong guidance.

| Source claim | Correction |
|--------------|------------|
| "For a corpus of 10,000 documents averaging 2,000 tokens each, the extraction cost at Haiku rates is measured in single-digit dollars" | Off by roughly an order of magnitude. At published Haiku 4.5 rates the input alone is about 20 MTok, and output at a few hundred tokens per document adds a comparable amount — on the order of tens of dollars, roughly halved with the Batches API. The generated prompt must show the arithmetic and instruct recomputation against current pricing rather than repeating either figure. @TODO Confirm current per-MTok rates at implementation time |
| "Cache the system prompt and schema, pay full price only for the document text" | Silently does nothing on Haiku 4.5, whose minimum cacheable prefix is larger than a short extraction prompt plus schema. It fails with no error — just a zero cache-creation count. Caching only pays once the shared prefix genuinely exceeds the minimum, for example with few-shot examples or a long domain preamble. Batches is the extraction-cost lever that works as advertised. @TODO Re-verify the per-model cache minimum before writing the reference code, since it is not monotonic across model generations |

### The ask-first script

Two stages. Stage 1 spends no user turn.

Stage 1, evaluated silently by the agent at Step 6 against `docs/product-spec.md` and `docs/tech-spec.md`, both of which already exist by then:

1. Does the product ingest a body of documents, records, or sources that users or agents ask questions about? Not "does it have a database" — does it have a corpus. If no, stop. Generate nothing, ask nothing, move on. This alone eliminates most products.
2. Given yes, does at least one of these hold? Answers require chaining facts across two or more documents, where neither alone contains the answer. Or multiple agents need a shared world model that outlives their context windows, or an evaluator needs traceable facts to check against. If neither holds, stop — record the alternative (RAG, RAG with reranking, or direct context) and why. A corpus alone is not sufficient reason; single-hop retrieval over a corpus is RAG's job.

Stage 2, reached only when both conditions hold. This is the one confirmation turn the capability ever costs.

1. Orient against the decision table: name the corpus, name the multi-hop or shared-state need, name the row it matches, and say that this is one of the few cases where a graph earns its complexity over RAG.
2. Corpus and volume: roughly how many documents, and how do they arrive — a fixed set, a steady trickle, or a bulk backfill followed by incremental updates? This sizes the per-run cap and decides whether the Batches path is needed.
3. Cost envelope, with real numbers: extraction is roughly one model call per document, ongoing; querying costs per question. State the computed figure and the batched figure, then ask whether that envelope is acceptable and whether there is a monthly ceiling to encode as a cap.
4. The honest out, asked last and asked plainly: the alternative is RAG over the same corpus — cheaper, simpler, no ingest pipeline to operate, no evaluation harness to maintain. It cannot chain facts across documents and cannot give an evaluator traceable ground truth. If the multi-hop need is a nice-to-have rather than core, RAG is the better call. Which is it?

On yes, proceed to the guardrails: API key available, per-run cap agreed on both documents and entities, schema version pinned, and a hand-labelled gold set for at least two representative documents committed to before the first production ingest.

On no at any point, record one line in the tech spec naming the alternative and why, tick the Step 6 checklist item, and return. Declining is a successful outcome of this step, not a skipped one — say so in one sentence so the user knows the option was considered rather than missed.

Step 7 asks a different, narrower question during team design, phrased to consume the Step 6 outcome rather than re-litigate it: do the workers need to chain facts across sources, refer to the same real-world entities under different names, or share structured state that outlives their own context windows — or is passing results through the orchestrator sufficient? Sufficient is the usual answer.

### Artifacts

| Path | New or edit | Axis | Purpose | Size |
|------|-------------|------|---------|------|
| `.claude/agents/testing.md` | Edit | B | New section on evaluating non-deterministic output: hand-labelled gold set, precision and recall, prompt as unit under test, regression gate rather than absolute threshold, scorer-in-CI versus evaluation-on-demand. Scopes against the existing "no flaky tests" rule so the two do not contradict. One Testing Tools row | +18 on 95 |
| `.claude/agents/code-review.md` | Edit | B | New `### Grounding` checklist group: claims cite a checkable locator; the locator is actually opened and checked; a claim with no supporting artifact is flagged unverified and escalated; contradictions name the contradicting evidence. Unconditional, mentions no graph. One Review Style bullet | +10 on 79 |
| `docs/prompts/team-design.md` | Edit | B | The shared-state question in Ask Before Generating; a Data-Passing Between Agents section naming a shared store as a fifth strategy alongside harness's four, with a three-condition promotion rule; provenance on every cross-agent artifact; three checklist items | +28 on 131 |
| `docs/prompts/skills-builder.md` | Edit | A | A `## Conditional Skills` tier whose first sentence is "the default is not generated," carrying the gate; two Covers-column cells; a third embedded ask-first rule; one checklist item | +18 on 201 |
| `docs/prompts/knowledge-graph.md` | New | A | The whole output axis: decision table, four stages, reference code, storage DDL, guardrails modelled on linear-tracking's, evaluation harness, four production signals, a heuristics-not-defaults quarantine table, deliverable checklist | ~210 |
| `grovv-stack-scaffold.md` | Edit | A | Step 5 subsection for the new prompt (placed last); a conditional-skill paragraph after the baseline table; tree and reference-table rows; one Step 7 data-passing sentence; Success Criteria count and one conditional item | +22 on 576 |
| `CLAUDE.md` | Edit | A | The new default-off non-negotiable; a Repository Map row; one clause on the Step 6 gloss. The "Steps 1-9" range is unchanged | +4 on 137 |
| `.claude/CLAUDE.md` | Edit | A | Tree entry; extend Prompt Execution Order item 2 rather than adding a sixth item; a Key Directives mirror; `ANTHROPIC_API_KEY` in the env reference, closing a real pre-existing gap | +7 on 259 |
| `README.md` | Edit | A | The inline prompt list; one gloss sentence; one non-negotiable bullet. The arrow chain is unchanged | +3 on 89 |
| `.claude/skills/grovv/SKILL.md` | Edit | A | One gloss sentence after the arrow chain. The chain, the step range, and the frontmatter description are unchanged | 1 line |
| `.claude/agents/database.md` | Edit | A | Four schema principles: graph-shaped data normalizes to a small set of tables with recursive CTEs under a depth cap; provenance on derived rows; version the extraction schema alongside its data; resolution writes to an alias table rather than mutating canonical rows | +5 on 67 |
| `.claude/agents/backend.md` | Edit | A | Two Key Rules: model-backed ingest runs as a PostgreSQL-native job with a per-run cap on both documents and records, existing before the first production run; extraction results and the cursor advance commit in one transaction | +3 on 77 |
| `docs/prompts/linear-tracking.md` | Edit | B | One conditional bracketed line in the MEMORY.md template's Current State, plus one maintenance sentence stating that a graph is a project artifact, not a third memory tier | +3 on 224 |
| `.claude-plugin/plugin.json` | Edit | A | Version to 0.4.0; repair the description, which already omits Linear and MEMORY.md; add a keyword. The agents array is untouched | 3 lines |
| `.claude-plugin/marketplace.json` | Edit | A | Drift repair only: line 14 omits Linear tracking that line 8 includes | 1-2 lines |
| `MEMORY.md` | Edit | C | Version at line 35; a two-line dated Decision Log entry referencing the Linear issue by identifier; add the new prompt to the propagation grep list at line 55. Line 36 ("Steps 0-9") is deliberately unchanged | +4 on 69 |
| `docs/architecture/` ADR | New | C | Records the decision and, more usefully, the rejections — so a future session does not re-litigate the new-step or seventh-agent option. Also settles the ADR format by example | ~95 |

### Propagation checklist

Required edits:

- Prompt-document count, five to six, in seven locations: `grovv-stack-scaffold.md:564` (Success Criteria), the new Step 5 subsection, the `docs/prompts/` sub-tree at `:102-107` (bare fence, no language hint — match it), the File and Folder Reference table at `:129-146`, `CLAUDE.md:30-46` (Repository Map, placed after the team-design row to preserve pipeline order), `.claude/CLAUDE.md:81-89`, `README.md:52`.
- The new non-negotiable in all three mirrors, written to each list's own idiom: `CLAUDE.md:88-96`, `README.md:75-80`, `.claude/CLAUDE.md:208-217`. Plus embedded as an inherited rule at `docs/prompts/skills-builder.md:119-124`.
- Glosses only, never the chains. The arrow chains at `.claude/skills/grovv/SKILL.md:48` and `README.md:60` stay identical in shape to each other and are not edited.
- Version in two places, same session: `.claude-plugin/plugin.json:5` and the prose mirror at `MEMORY.md:35`.
- `ANTHROPIC_API_KEY` added to `.claude/CLAUDE.md:223-256`, closing a gap that predates this work.
- JSON drift repair while those files are open: `plugin.json:6` omits Linear and MEMORY.md; `marketplace.json:14` omits Linear tracking that `:8` includes.

Verify unchanged, edit nothing:

- Step numbering, fifteen locations. If any needs changing, the implementation has drifted from this plan — re-examine rather than patch. Leave `.claude/agents/scaffold.md:23-36`'s pre-existing off-by-one alone; that is a separate commit.
- Agent roster, ten enumerations plus five prose counts of "six." No agent is added.
- Stack tables, eight tables plus two prose copies invisible to a table-shaped grep (`grovv-stack-scaffold.md:347` and `skills-builder.md:114`). No Knowledge Graph row anywhere. Only `testing.md`'s Testing Tools table gains a row, and that is a tool, not a stack default.
- The two legacy-idiom files, `docs/prompts/tech-spec.md` and `docs/prompts/tech-spec-template.md`, are deliberately untouched.

Forbidden:

- No file under `.claude/skills/harness/` may be edited. It is vendored verbatim under Apache-2.0 at a pinned commit and its `ATTRIBUTION.md` states the workflow body and references must not be hand-edited. The temptation is acute — its data-passing section enumerates exactly the four strategies a shared store would extend. The extension goes in `docs/prompts/team-design.md`, which designates itself as the place to extend harness behavior. Run `git status` before committing and confirm nothing under that directory appears in the diff.

Convention checks before commit: horizontal rules are exactly five dashes; directory trees use bare fences while code fences always carry a language hint; no emoji in headings; the wordmark takes doubled backslashes in prose and single backslashes inside code fences. The two files most likely to get the wordmark wrong are the new prompt (if it carries any fenced template) and `linear-tracking.md`, whose MEMORY.md template fence already carries the single-backslash form and must not be "corrected."

### Phased rollout

| Phase | Delivers | Size |
|-------|----------|------|
| 1 — Grounding discipline | Edits only, four existing files: `testing.md`, `code-review.md`, `team-design.md`, and two small `skills-builder.md` changes. Zero new files, zero enumeration edits, no cascade | ~60 lines, half a day |
| 2 — The gate and the prompt document | New `docs/prompts/knowledge-graph.md`; the Conditional Skills tier; the master-directive edits; the new non-negotiable in three mirrors; the seven-location count; the version bump and JSON repairs; the MEMORY.md entry | ~210 new lines plus ~40 lines of edits across 9 files, one to two days |
| 3 — Reference payload and agent patterns | The references the prompt points at, written into target projects: pipeline, evaluation, storage. Plus `database.md`, `backend.md`, and the `linear-tracking.md` pointer | ~600-800 lines generated into targets plus ~11 lines of edits, three to five days |
| 4 — The ADR (droppable) | The architecture decision record, which also creates `docs/architecture/` and settles the ADR format by example | ~95 lines |

Phase 1 stands alone. It could ship before Phase 2, or instead of it. It converts the code-review agent from a plausibility judge into a fact-checker; it gives the testing agent vocabulary it entirely lacks for scoring model output, fixing an active defect where a "no flaky tests" rule is applied to output that is non-deterministic by construction; and it forces every generated orchestrator to name and justify its data-passing strategy with provenance on cross-agent artifacts. Every line of it applies to every project grovv scaffolds, including every project that will correctly decline a graph forever. It is also the best value-to-blast-radius ratio available: about 60 lines against zero cascade risk, zero new files, zero renumbering, zero manifest changes. If exactly one phase is approved, approve this one.

Phase 3 carries the largest quality risk, because it means writing a resolver, summarizer, assembler, and scorer that the source never shows, in a language it never uses, to a bar that forbids pseudo-code.

-----

## What We Are Deliberately Not Doing

| Rejected | Why |
|----------|-----|
| A new numbered pipeline step | Fifteen-plus locations across nine files, two of them JSON no Markdown grep finds, in a repo that has missed this class of propagation at least three times already. Spent on a capability the source's own decision table says most systems should not have. A conditional branch inside Step 6 delivers the same thing for three lines |
| A seventh baseline agent | Ten roster enumerations, five prose "six" to "seven" changes, plus the explicit agents array in `plugin.json`. And doctrinally wrong: the vendored harness guidance holds that skills are how and agents are who, and a four-stage extraction pipeline is overwhelmingly how. There is no distinct who to add — schema is already database's, ingest jobs are backend's, scoring is testing's, claim-checking is code-review's |
| A Knowledge Graph row in the stack tables | Correctness before cost. Those tables are defaults, and every other row is something a typical grovv project actually uses. Listing a graph there tells every future agent that a graph is part of the expected shape of a grovv project — exactly the failure the gate exists to prevent. Separately, the repo demonstrably cannot keep eight parallel stack tables in sync: `scaffold.md` is already missing its Linear row, and `skills-builder.md:114` hides a ninth copy as prose. A ninth row on a known-broken surface has negative expected value |
| An eleventh row in the baseline skill table | It would silently invert the gate. `skills-builder.md:191` already sanctions dropping baseline skills that are irrelevant, so a baseline row makes the graph opt-out — generated unless actively declined. A separate tier whose first sentence is "the default is not generated" makes it opt-in |
| Hiding the depth under `.claude/skills/grovv/references/` | Cheaper — skills register by directory path, so zero manifest edits. But it conflates the kickoff skill's own depth with instructions for generating target-project artifacts, invents a directory that does not exist today, and rests discovery on a single soft pointer with no error signal if a future edit orphans it. Seven bounded, greppable enumeration edits beat an unbounded orphaning risk |
| Amending the vendored harness data-passing table | Forbidden outright, and the most natural-looking edit in the repo — that table is exactly one row short of the point. Vendored verbatim under Apache-2.0; editing it breaks the vendoring contract and would be silently reverted by the next re-vendor |
| A graph over grovv-stack's own artifacts | The clearest no. The corpus is around 30 files and 5,700 lines, the largest single chunk of which is a vendored third-party skill nobody would want indexed. It fits in one context window. Every cross-reference is already an explicit Markdown link or path. Grep answers every traversal question a graph would, deterministically and for free. And building it requires exactly the dependency this repo forbids. By the source's own criterion — the graph earns its complexity when the alternative exceeds the window or loses the connections — neither condition holds. Revisit only if the repo outgrows what a single session can hold |
| A SessionStart hook surfacing a graph digest | The hook slot exists, which makes it tempting, but it implies a queryable store, which implies a runtime and a dependency inside grovv-stack. Wrong shape even in a target project: a digest computed at every session start is a cost paid whether or not the session touches the graph, and a digest is a summary — precisely the fragile summary-passing the source diagnoses |
| The graph as an unconditional third memory tier | Taxes every project for the benefit of the few with both a graph and an overnight loop. The two-way split — Linear owns the backlog, MEMORY.md owns context — was a deliberate dated decision taken to stop duplication and is restated in four files. MEMORY.md also has a hard line budget. What a fresh session needs is that the store exists and which schema version it is on: one conditional line |
| Copying the source's Python verbatim | Violates the TypeScript-and-Go stack and the production-first no-pseudo-code bar at once. The source contains two executable functions across twelve pages, with no error handling and no transaction discipline anywhere, and its call shape is from a dated document |
| Repeating the source's cost estimate and caching advice | Both fail on contact with current published rates. See the corrections table |
| Shipping the source's numeric thresholds as validated defaults | Degree 3, k=2, blocks of 50-100, the density and compression bands, "a few hundred thousand edges" — every one asserted, none measured, all observed on a 22-node corpus. They ship in a clearly-labelled heuristics section with tuning notes. Presenting them as defaults would launder a toy result into production guidance across every project grovv scaffolds |
| Quoting the reported F1 and precision numbers as benchmarks | Two of six documents scored, no relation-level numbers, no resolved F1, and resolution showing exactly zero measured effect in both rows. The precision-over-recall asymmetry argument is kept, because it is a reasoning argument rather than a measurement, and is attributed as such |
| A third universal ask-first rule | It would spend a conversation turn on every project to reach an answer the agent can already infer from specs it wrote minutes earlier. The two existing ask-first rules earn universality because nothing in a spec tells you Astro versus Next.js, or which flows deserve E2E coverage. A spec does tell you whether there is a corpus and whether questions chain across it. Hence a default-off rule with conditional confirmation |
| A `scripts/` directory holding a runnable scorer | Sanctioned by harness as a skill sub-directory, so it would look correct — but it is executable code with dependencies in a repo whose output is documents. The scorer belongs in the target project |
| Conditional placeholders in the tech-spec prompts | Taxes every project's spec template for a subsystem most decline, and both files are legacy-idiom, so editing them invites either style drift or an out-of-scope modernization. The target's graph schema goes to an ADR instead |
| Temporal graphs, edge confidence scoring, graph-of-graphs | The source explicitly flags all three as future directions that were not built. Shipping them as guidance in a production-first scaffolding system would present speculation as pattern |
| Knowledge-graph trigger phrases in the kickoff skill's frontmatter | The description is the skill's only trigger mechanism and its job is routing. A graph is an output of the pipeline, not an entry point to it. Adding those phrases would pull unrelated requests into a full scaffolding workflow |
| Fixing the unrelated drift discovered while surveying | `scaffold.md`'s missing Linear stack row, its off-by-one scaffolding order, and `linear-tracking.md`'s bare `cat MEMORY.md` hook are real bugs and none of them belong in this change. The two JSON description drifts are repaired only because the propagation grep forces those files open anyway |

-----

## Open Questions

- @TODO Is a silent false negative on the gate acceptable? Because the agent evaluates the two conditions itself rather than asking, a project that would genuinely benefit may never hear the option exists. A false positive costs one confirmation turn and is trivially reversible; a false negative is invisible to everyone. The alternative — a one-line "considered and declined a knowledge graph because X" note in every tech spec — makes the decision visible at the cost of a line in every project.
- @TODO Should the roughly 210-line prompt document ship to targets that declined? Step 5 copies the prompt set into every target project. Shipping unconditionally means the decision table travels with the project and the choice can be revisited later; not shipping means less bloat for the majority but complicates Step 5's otherwise simple contract. Currently: ships unconditionally.
- @TODO Which model for resolution? The source never versions Sonnet. Resolution is where errors are hardest to detect and most damaging — silent node loss and over-merging both fail quietly — which argues for a more capable model there specifically. But the source's entire cost argument rests on the cheap-extraction, capable-synthesis split. Recommend a split, or keep the two-model story?
- @TODO How is the reference TypeScript validated before it ships? Phase 3 requires four production-grade pipeline stages the source never shows, in a language it never uses, to a bar that forbids pseudo-code — and grovv-stack has no test infrastructure and cannot gain any. Options: validate in a throwaway scratch project and paste in verified code; ship it explicitly marked as unvalidated reference; or narrow Phase 3 to schemas, prompts, and decision rules only. Decide before Phase 3 starts.
- @TODO Does a Conditional Skills tier of one justify itself as a precedent? With a single entry it is obviously right. With four it becomes a second baseline set with its own drift surface and its own gating logic. Should whoever adds the second entry be required to re-argue the tier rather than inherit it, and should that requirement be written into `skills-builder.md` now, while there is exactly one?
- @TODO Should the ADR define the ADR format for target projects too, or only for grovv-stack? Creating the repo's first ADR forces inventing a format the repo has never defined. One template serving both is tidier but is scope creep on a knowledge-graph decision. Currently: grovv-stack only, gap flagged.
- @TODO How should the corrected cost figure be published? Stating the arithmetic and the rate inputs is the most honest and the most verbose; stating only the method forces a lookup; stating the figure with a dated verification caveat ages badly. Currently: arithmetic shown plus a recompute instruction.
- @TODO Should the generated skill carry removal instructions? The gate governs generation, not deletion. A project that generates the skill and later abandons the idea keeps a several-hundred-line skill whose pushy trigger description will keep firing. A one-line note about removing it cleanly would help, but skill-removal guidance is a pattern the repo has never used anywhere else.

-----

## Colophon

| Field | Value |
|-------|-------|
| Version | 0.1.0 |
| Last Updated | 2026-07-25 |
| Status | Draft |
| Author(s) | grovv stack scaffolding agent |
| Model | Claude (Claude Code) |

-----
gro\\/\\/ stack — Knowledge Graph Engineering
