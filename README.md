# OpenUSD Composition Contracts

**Version 0.1 — independent work-in-progress proposal · 2026-10-10**

Explore how teams can agree who owns an authored opinion, where it belongs, how it composes, and how tools can explain and enforce that agreement. The starting paradigm is layered scene assembly with published asset interfaces: scene roots compose workstream sublayers; geometry layers reference reusable assets; asset-specific variants remain with their rightful asset or assembly owner.

Prepared for discussion with the AOUSD IEDT group, including Nandu and Dylan. This is not an AOUSD standard, endorsed specification, or record of their agreement. Review and experimentation may change the proposal substantially.

## Start here

- [Composition contracts](CompositionContracts.md): the evolving proposal and stable CC rule IDs.
- [Open questions](DISCUSSION.md): the first review agenda.
- [Roadmap](ROADMAP.md): from discussion to deterministic inspection and pipeline experiments.
- [Agent entry](AGENTS.md): bounded context and working instructions.
- [Next-agent handover](harness/HANDOVER.md): brief history, working decisions and implementation boundaries.
- [Harness governance](harness/GOVERNANCE.md) and [workflow](harness/WORKFLOW.md).
- [Deterministic tooling requirements](harness/TOOLING_REQUIREMENTS.md).
- [Source and dependency routes](harness/SOURCES.md).
- [Resume state](harness/STATE.md): what exists and the next useful step.

## Current scope

The contract was moved from TutorialBuilder. Its VariantSetups paper and A–H scenes remain there; they are exploratory evidence, not conforming examples shipped by this project. See [provenance](harness/SOURCES.md). This project currently contains documentation only. No inspector, repair engine, extension, automated enforcement or pipeline integration is implemented.

OpenUSD-GoodStart remains a knowledge reference and potential consumer. TutorialBuilder remains a teaching consumer. The private `OpenUSD_GoodStart_Pipeline_nodes` repository is a candidate backbone for a future composition pipeline, subject to interface and suitability review. This project must remain understandable and eventually inspectable without that private dependency.

## Participation

Propose changes by identifying a CC rule, the intended use case, competing approaches, an example and expected composition behavior. Distinguish OpenUSD mechanics, externally published patterns and our conventions. Record uncertainty and counterexamples. See [contribution guidance](CONTRIBUTING.md).

Remote hosting, access grants, licensing and any future transfer to a group or workcell project remain to be decided. Local project creation does not publish this material or grant rights to external source content.
