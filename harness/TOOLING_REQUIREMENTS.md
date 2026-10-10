# Deterministic tooling requirements

**Draft 0.1. All capabilities below are planned, not implemented.**

The 0.2 example adds `tools/build_example.py`, a bounded author for a new fixture directory. It uses OpenUSD 26.08, refuses nonempty output, records files/hashes and reads back the four saved default entrypoints. This supplies preliminary fixture evidence for DT-01; it does not implement the general DT-01–09 core, enumerate inactive opinions, classify arbitrary scenes or certify the fixture. Example-specific JSON documents are draft inputs, not an accepted general schema.

We need repeatable scripts as the execution foundation. An LLM may explain findings or propose an ownership decision; it must not improvise USD repair operations for each run. A UI, MCP bridge or pipeline node should call the same core.

| ID | Requirement | Future acceptance evidence |
|---|---|---|
| DT-01 | Reproducible inputs: identify stage, contract/profile revision, USD version, resolver, dependencies, load rules, variants, session state and time range. | Same declared inputs produce equivalent stable reports, with volatile run metadata separate. |
| DT-02 | Read-only inventory through USD/Sdf APIs: authored specs and composed contributions, fields, selections, variant context, operation order, bindings, samples and provenance. | Inventory covers supplied fixtures; unavailable dependencies and excluded states are explicit. |
| DT-03 | Rule classification: apply CC IDs and explicit ownership/profile mappings; ambiguity becomes a finding, not a guessed repair. | Each finding identifies source, destination if known, rule, evidence and uncertainty. |
| DT-04 | Dry-run plan: exact field-level changes, affected dependencies, expected effect, conflict handling and preconditions; no source mutation. | Source content stays unchanged and a reviewer can reconstruct the proposed edits. |
| DT-05 | USD-aware candidate repair: preserve variant context, relative path anchoring, metadata/list operations and coherent transform operations/order. Create/register the rightful TransLyr when required. | Candidate and source-removal effects considered together; no flattening or collateral field deletion. |
| DT-06 | Explicit execution authorization; revision checks, rollback and audit for multi-file edits. | Interrupted/conflicting operations leave recoverable state; repeat application is idempotent. |
| DT-07 | Compare expected composed behavior across declared configurations, samples and load contexts. | Transforms, selections and resolved materials match expected outcomes or documented intentional changes; incomplete coverage is visible. |
| DT-08 | Shared core independent of Omniverse UI, agents and private pipeline backend. | Local standalone invocation and adapter invocation use the same input/output contract. |
| DT-09 | Bounded operation and reporting: deterministic ordering, explicit limits/errors, machine-readable findings plus readable summaries. | No silent skipped assets, swallowed failures or accidental whole-repository scans. |

These requirements elaborate CC-17 through CC-23. Future fixtures should include direct local opinions masking variants, parent/child placement, inactive branches, missing dependencies, referenced relative paths, animation ownership and conflicting destination fields. Tests are planned work requiring an implementation task; none are claimed here.

## Candidate pipeline backbone

`OpenUSD_GoodStart_Pipeline_nodes` is a private repository identified by Jan as a potential foundation. Its code/API, dependency model, licensing and execution guarantees have not been assessed for this project.

Assess whether its nodes can represent inventory -> classify -> plan -> compare -> apply -> report without coupling the public contract to a private runtime. Require explicit typed/versioned artifacts between steps, error propagation, provenance, cancellation/recovery and a read-only mode. A node graph schedules operations; it does not establish USD correctness by itself.

Adopt or adapt it only after a bounded compatibility review. If suitable, implement an optional adapter; if unavailable, the standalone core and proposal remain usable. No private code, nodes or credentials are imported by this bootstrap.
