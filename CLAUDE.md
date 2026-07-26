Ask-first WARNINGS - 1 line(s), not build-failing:

.github/scripts/README.md:167: WARNING - names an exploratory artifact and a framework choice in one line without saying the ask-first rule still applies; a human should read it
    The second half is an **erosion heuristic**: text that puts a prototype or mockup in the same breath as a framework choice without stating that the rule still a

Each is a heuristic hit. If the line already makes plain that a prototype is not a framework decision it is a false positive - leave it; otherwise add that sentence.

Ask-first check FAILED - 2 missing statement(s):

CLAUDE.md:1: no sentence states the frontend-framework ask-first rule - nothing here carries an ask signal, the subject (framework / Astro / Next.js) and a precedence word together
    e.g. "Always ask which frontend framework - Astro + React or Next.js - before writing frontend code"
CLAUDE.md:1: no sentence states the playwright ask-first rule - nothing here carries an ask signal, the subject (Playwright / E2E / end-to-end) and a precedence word together
    e.g. "Always ask the user what Playwright should test before writing any Playwright tests"

Fix: restore the rule in the named file, in that file's own idiom, as ONE sentence carrying an ask signal (ask/discuss/confirm/agree, or the user choosing), the subject, and a word putting the ask ahead of the work (before/never/not/until/first/up front/in advance). Calling the rule "ask-first" does not state it. Both rules are non-negotiable.
