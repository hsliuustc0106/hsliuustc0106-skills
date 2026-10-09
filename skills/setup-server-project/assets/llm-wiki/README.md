# Personal LLM wiki

Start with the [index](wiki/index.md). Agent behavior is defined in
[AGENTS.md](AGENTS.md); setup and later activity appear in the [log](wiki/log.md).

Add a document to `raw/`, open your agent in this directory, and ask:

- "Ingest raw/my-paper.md using AGENTS.md."
- "What evidence do we have for this question? Cite the supporting pages."
- "Lint this wiki and report findings."

The wiki starts empty. Directory names and these prompts are local defaults,
not requirements imposed by the linked design pattern. No service needs to run.
