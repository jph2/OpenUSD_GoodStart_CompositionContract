# Handover to the next agent

**2026-10-10 · Initial project bootstrap · Draft 0.1**

## Brief history

The discussion began in TutorialBuilder while developing an Omniverse/OpenUSD course. A small cube example exposed a composition issue: a directly authored local scale opinion masked the scale inside a variant. Reordering or nesting sublayers did not remove that local-versus-variant conflict. Several alternative scene structures were explored in TutorialBuilder's VariantSetups folders.

Jan wanted to retain a clear paradigm: a thin root assembles workstream sublayers, and geometry layers bring reusable assets into the scene through references. The discussion therefore moved from individual fixes to a composition contract: who owns each property, which layer authors it, which alternatives belong to assets, and when scene edits should combine with or override an asset's behavior.

The scope then expanded to nested product ownership, shared materials, PLM-driven defaults, animation/rig/physics boundaries and project data versus runtime state. Jan's practical concern is that teams often author on the wrong layer and UI delta markers do not adequately explain what changed. Explicit contracts should support deterministic inspection and repair, with agents helping interpret ambiguous cases.

We initially considered a section inside OpenUSD-GoodStart. Jan instead chose this independent project to share a focused WIP proposal with Nandu, Dylan and the AOUSD IEDT group. Future GoodStart, AOUSD or workcell integration is possible, not decided. No group review or endorsement is claimed.

## Working decisions to preserve

- **One contract owner:** CompositionContract.md here, preserving CC-01 through CC-23. Its former TutorialBuilder location is a forwarding note.
- **Geometry versus placement:** GeoLyr owns hierarchy/asset references, not transform operations or variants. Ordinary transforms belong in the rightful owner's TransLyr; create it when needed.
- **Semantic exceptions matter:** variant-dependent transforms remain in their variant context; animation, rig bind/rest data, physics frames and solver/runtime poses follow CC-21. Do not route every matrix into TransLyr.
- **Asset-owned alternatives:** define reusable variants at their rightful asset/assembly level. Publish their interface, lofting above payloads when appropriate. Scene VariLyr selects published choices or defines scene scenarios; it does not copy asset implementations.
- **Ownership before file choice:** choose the asset, assembly or scene that owns the change, then its technical role. Hierarchy depth alone cannot determine ownership.
- **Strength remains USD strength:** role names and sublayer organization do not prevent local opinions from masking variants. Declare intentional overlaps and writer authority. There is no universal layer order.
- **Deterministic execution:** scripts should inspect, classify, plan and eventually repair through USD-aware APIs. LLMs explain and propose; MCP/UI/pipeline adapters expose the core rather than replace it.

These are Jan's working conventions for review, not an industry standard. Consult the full contract before applying them.

## What exists and what stayed behind

This folder contains the proposal, agent entry, governance, workflow, tooling requirements DT-01 through DT-09, roadmap, discussion agenda and source routes. It currently has documentation only; no Git initialization or remote setup was performed during bootstrap, and no commits or publication were made.

The VariantSetups paper and A–H example folders remain in TutorialBuilder at the location recorded in SOURCES.md. They reflect earlier experiments, including conventions superseded by the current contract. Do not move them, silently normalize them or label them conforming without a new request and appropriate evidence.

No inspector, repair engine, conforming example in this project, automated test evidence, Omniverse extension, MCP adapter or pipeline integration exists yet. Documentation does not establish runtime behavior.

## Related projects and evidence

- **OpenUSD-GoodStart:** sibling knowledge project and source-navigation reference. Distinguish it from the supplied GitHub research repository `jph2/USD_GoodStart`; do not assume identical contents.
- **OpenUSD_GoodStart_Pipeline_nodes:** Jan's private candidate backbone for a composition pipeline. Its existence was observed; its implementation and suitability were not assessed. Do not copy private content into this collaboration project or require access for basic use.
- **AI Harness Quickstart:** the supplied guide informed the small harness structure and the separation of model judgment, fixed procedures and evidence. Precise links and inspection scope are in SOURCES.md.

## Next-agent starting point

Read the entry files, this handover and the current STATE.md; then follow the user's next task. For proposal work, start with DISCUSSION.md and relevant CC rules. For a requested implementation, first agree a minimal example and a read-only inventory/report contract (DT-01 through DT-03). Do not jump directly to automatic cleanup or a full extension.

Open decisions include external review, minimal profiles/examples, machine-readable contracts, pipeline-backbone suitability, repository hosting/access and licensing. Do not infer any of these decisions from the roadmap. Keep ongoing progress in STATE.md; preserve this handover as the origin and initial decision context.
