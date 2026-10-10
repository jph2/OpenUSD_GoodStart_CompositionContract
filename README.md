# OpenUSD Composition Contracts

**Version 0.2 — independent work-in-progress proposal and local example · 2026-10-10**

Explore how teams can agree who owns an authored opinion, where it belongs, how it composes, and how tools can explain and enforce that agreement. The starting paradigm is layered scene assembly with published asset interfaces: scene roots compose workstream sublayers; geometry layers reference reusable assets; asset-specific variants remain with their rightful asset or assembly owner.

Prepared for discussion with the AOUSD IEDT group, including Nandu and Dylan. This is not an AOUSD standard, endorsed specification, or record of their agreement. Review and experimentation may change the proposal substantially.

## Start here

- [Composition contracts](CompositionContracts.md): the evolving proposal and stable CC rule IDs.
- [Open the example guide](examples/01_LayeredScene/README.md): manual configuration, scene scenarios and two deliberate conflicts.
- [Project structure and diagram](PROJECT_STRUCTURE.md): the revised paradigm, storage layout and edit destinations.
- [Open questions](DISCUSSION.md): the first review agenda.
- [Roadmap](ROADMAP.md): from discussion to deterministic inspection and pipeline experiments.
- [Agent entry](AGENTS.md): bounded context and working instructions.
- [Next-agent handover](harness/HANDOVER.md): brief history, working decisions and implementation boundaries.
- [Harness governance](harness/GOVERNANCE.md) and [workflow](harness/WORKFLOW.md).
- [Deterministic tooling requirements](harness/TOOLING_REQUIREMENTS.md).
- [Source and dependency routes](harness/SOURCES.md).
- [Resume state](harness/STATE.md): what exists and the next useful step.

## Current scope

The contract was moved from TutorialBuilder. Its VariantSetups paper and A–H scenes remain there; they are exploratory evidence, not conforming examples shipped by this project. See [provenance](harness/SOURCES.md). The new `examples/01_LayeredScene` package develops those experiments and the numbered storage structure inspected in `USD_GoodStart/_Generated_Test`.

Start with [ROOT_example.usda](examples/01_LayeredScene/ROOT_example.usda), Jan's supplied Omniverse starting scene with the example assets composed under `/World`. The package contains 29 USD layers, Cube/Cone packages, a nested DisplayPair assembly, shared asset materials, scene contributions, data, explicit review exceptions and draft JSON contracts. The supplied environment, viewport cameras and render state remain the startup baseline. Its two textures are bundled; OmniPBR and RTX features require a compatible Omniverse application. `World_Manual.usda` is a compatibility alias.

[tools/build_example.py](tools/build_example.py) reproduces this setup from the retained [Omniverse template](templates/Omniverse/README.md) through OpenUSD 26.08 APIs. Default-entrypoint read-back is recorded; full acceptance and Omniverse review are pending. No general inspector, repair engine, ownership-routing extension or pipeline integration is implemented.

The default working state locks all persistent layers and selects Session Layer. Use [Open_In_Kit.ps1](examples/01_LayeredScene/Open_In_Kit.ps1) to run the bundled startup helper: a USDA file alone cannot restore a fresh anonymous session target. Persistent edits require deliberately unlocking the rightful contribution. See the example guide for startup and persistence details; Kit execution remains pending.

OpenUSD-GoodStart remains a knowledge reference and potential consumer. TutorialBuilder remains a teaching consumer. The private `OpenUSD_GoodStart_Pipeline_nodes` repository is a candidate backbone for a future composition pipeline, subject to interface and suitability review. This project must remain understandable and eventually inspectable without that private dependency.

## Participation

Propose changes by identifying a CC rule, the intended use case, competing approaches, an example and expected composition behavior. Distinguish OpenUSD mechanics, externally published patterns and our conventions. Record uncertainty and counterexamples. See [contribution guidance](CONTRIBUTING.md).

Remote hosting, access grants, licensing and any future transfer to a group or workcell project remain to be decided. Local project creation does not publish this material or grant rights to external source content.
