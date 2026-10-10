# Initial review agenda

All questions remain open for collaborative review. The current CC rules are the author's working proposal.

1. Is rightful ownership plus technical role plus conditional/time context sufficient to classify opinions? What real projects break this model?
2. How strict should TransLyr separation be, and which domain profiles need different boundaries? Review CC-21's rig, animation and physics exceptions.
3. Which published asset controls should be exposed through lofting, and how do we keep the interface synchronized?
4. Which layer roles are essential for a minimal scene versus a workcell or commissioning profile? Avoid empty-layer bureaucracy.
5. How should a profile declare intentional property competition and active writers across animation, simulation and live data?
6. What can a deterministic inspector establish, and what needs human domain authority or application-specific evaluation?
7. Which existing AOUSD/industry patterns should we align with? Record sources and gaps without treating this proposal as an invented USD standard.
8. Could the private pipeline-nodes project provide optional execution infrastructure without limiting independent review or adoption?

## Decision record

- 2026-10-10 — Jan supplied ROOT_example.usda and selected that concrete Omniverse scene as the project's startup standard. Preserve its coordinate frame, environment, viewport cameras, render state and timeline; compose the existing assets under `/World`. The launcher now defaults to ROOT_example; World_Manual becomes an alias. The custom presentation layers were archived. CC-01 records an application-template exception for the supplied root content; new project opinions retain their existing role rules. No axis rotation or rescaling was added. Runtime/viewport acceptance remains pending.

- 2026-10-10 — Jan requested all persistent layers locked by default and Session Layer as the initial authoring target. CC-01 now allows temporary session work and reserves durable ownership for explicit persistence into the rightful layer/context. The generator and existing package gain saved Kit sublayer locks and a bundled startup helper/launcher. Anonymous authoring targets and root protection require runtime handling; this is a narrow startup helper, not the deferred ownership-routing extension. Kit execution remains unverified.

- 2026-10-10 — Jan requested a separate collaboration project and move of the composition contract only. Variant examples stay in TutorialBuilder. Harness and agent entry added. Pipeline-nodes repository recorded as a candidate, not selected infrastructure.
- 2026-10-10 — Jan requested a new example and folder structure informed by the predecessor VariantSetups, supplied schematic and `USD_GoodStart/_Generated_Test`. Draft 0.2 adds a self-contained local package and PROJECT_STRUCTURE.md. Existing CC-01–23 IDs are preserved; CC-24/25 define portable storage lifecycles and retained-source/public-interface boundaries.
- 2026-10-10 — Implementation choices for review: keep numbered storage lanes; put placement in TransLyr; use asset-owned Size/Finish, assembly-owned Palette and scene-owned Layout; keep manual/scenario controls in separate roots; compose explicit ReviewLyr conflicts only in named review roots. Use centimetres and Z-up for this new example, not the generated predecessor's Y-up. Keep simulation/runtime slots as documented directories until content exists. These choices implement the requested draft; they are not external acceptance.
- 2026-10-10 — A bounded OpenUSD 26.08 author and four default-entrypoint read-backs now exist. Generic inspection/repair, full variant acceptance and Omniverse observations remain pending. Public distribution, external review, payload profiles and private pipeline assessment remain undecided.
