# Resume state

## Publication checkpoint

Jan requested commit and push of the accumulated 0.1.1 work: contracts, roadmap, diagrams, direct SceneROOT entrypoints, launcher/generator updates and retained migration evidence. The raw direct_root_kit.log remains local; the research-paper edit belongs to its separate repository and is outside this commit. No tests were run for publication. See Git history for the resulting commit; push outcome is reported in the task.

## Asset-interface and acceptance requirements adopted

Jan approved the proposed integration. Extended CC-25 with a concrete asset-interface checklist (purpose, provenance, coordinates, dependencies, controls, simulation alternatives, writer/lifecycle and evidence) and clarified that imported packages need no forced internal rewrite or extra wrapper. Extended CC-12 with separate asset, independent-reuse, configuration, assembly and change-impact acceptance, including explicit not-evaluated outcomes. README links the requirements; DISCUSSION records the decision. Existing IDs, diagram, folders and scenes remain unchanged. Documentation only; no tests, implementation, commit or push. Applying the checklist to actual sample profiles and selecting a pinned SimReady robot/runtime remain future work.

## Incoming assets, SimReady and upstream priorities

Clarified Asset Structure 3.0 as incoming robot packaging preserved inside larger workcell/line/facility composition, in README, contract comparison and the previously authorized research §6.3.8. Added upper README context for SimReady, relevant OpenUSD developments and Jan's AOUSD/IEDT workcell discussions, with official status explicitly unconfirmed. Added bounded CC-12/24/25 evaluation implications and a roadmap priority table for UsdValidation, SimReady, profiles/capabilities, namespace editing, LOD, splines and nested bodies. Sources distinguish upstream status from local availability. No diagram/layout or USD edits, installations, tests, commit or push in this increment. Next: agree a pinned robot/workcell profile and supported runtime before implementing adapters or claiming conformance.

## Research integration and NVIDIA comparison

At Jan's explicit request, added §6.3.8 and the repository link to the sibling AAS_OPC_OpenUSD_INTEGRATION/docs/AAS_OPC_OpenUSD_RESEARCH_v14.md. Kept contract additions bounded: requirement-to-evidence/promotion in CC-12 and external-data lifecycle/consumer impact in CC-24. Added a sourced comparison with Isaac Sim Asset Structure 3.0 and DSX SimReady documentation, distinguishing domain profiles from our scene conventions. DSX scene files were not inspected; compatibility remains unverified. Documentation only, no tests or scene changes, no commit/push.

Refined README prominence following Jan's correction: purpose, requirements and composition evaluation lead again. Identifier separation and composable bindings remain linked near the introduction as industry-driven requirements for identity continuity, clear responsibilities and integration stability during development, rather than the project's headline objective.

README now leads with composition contracts for digital twins and physical AI, immediately followed by the linked identifier-separation proposal and Composable Bindings paper. Preserved the personal OpenUSD journey and evaluation framing below it; removed the duplicated upstream introduction from Working with agents. Documentation-only change.

## README upstream integration references

Read the full Composable Bindings v1.0 whitepaper (November 2025) and added both requested links to README: Aaron Luk's identifier-separation proposal #105 and the Microsoft/NVIDIA Composable Bindings paper, crediting Christoph Berlin and Aaron Luk. Clarified our intent to integrate these ideas and distinguished the paper's future declarative-config direction from Jan's more detailed proposed binding artifacts. Documentation only; no implementation or tests.

## Identity and composable bindings

Reviewed bounded sections of Jan's AAS_OPC_OpenUSD_RESEARCH_v14 and Aaron Luk's proposal #105/source draft. Added CC-27 for namespace/source/occurrence/physical-instance separation and ownership-level placement, and CC-28 for declarative bindings, execution artifacts, output routing and evaluation. Clarified the current example IDs as illustrative scene-occurrence fields, not mesh tags or an upstream standard. README/roadmap/source notes and chart identity hints updated. No asset IDs, binding engine, scene migration or tests were added; identifier encoding and pilot implementation remain open.

## SceneROOT naming adopted

Jan selected the exact repository-wide scene entrypoint convention SceneROOT_<Purpose>.usda, now CC-26. Renamed the five active example roots to SceneROOT_Example, SceneROOT_Manual, SceneROOT_Scenarios, SceneROOT_MaskedSize and SceneROOT_MaskedSelection. Updated active docs, profiles, generator and launcher references; retained original template/evidence filenames and the historical migration script. Existing open Kit sessions still refer to their previously opened paths and must be reopened via the updated launcher; do not save them back to the obsolete filenames. Prior manifest observations and hashes remain historical. No USD content changes or tests were required for the filename migration.

## Grouped class boxes

Refined the README, contract and project-structure Mermaid charts to four class boxes containing role lists: BASE, SIM, RUNTIME and DATA. Preserved root-left / stack-middle / assets-right, asset/assembly details and bottom GeoLyr. REVIEW remains an optional annotation/contribution. Regenerated the SVG successfully. Class boxes do not create USD aggregate layers or prescribe optional-class strength. Naming remains under discussion: recommend ROOT_<Purpose>.usda for this project; no files renamed. Official NVIDIA asset-structure guidance uses root layer as a role and treats /World as an agreed prim namespace, not a required filename; no evidence establishes a universally most-common filename convention.

## Naming and diagram classifications

Adopted Root / ROOT_<Purpose>.usda as entrypoint terminology, with scene reserved for the composed result. Existing World_* filenames are explicitly legacy pending coordinated migration; this documentation task does not rename live scene files. Added ASSET USD, BASE, SIM, RUNTIME, DATA and REVIEW class labels to the existing Mermaid nodes in README, CompositionContracts and PROJECT_STRUCTURE, preserving edges, columns and GeoLyr's bottom position. Added the storage/class/role mapping and distinguished BASE physics setup from SIM results. SVG is regenerated from the detailed contract chart. No USD changes or tests are part of this increment.

## Direct scene root correction

Opened the corrected World_Manual in a separate existing-build Kit 110.3 Composer process using the session-default startup helper. Runtime log at 2026-10-10T11:19:08Z reports: `CC: Session Layer selected; 22 persistent layers protected.` This covers loaded persistent layers including the root; visual UI acceptance and subsequently loaded dependencies were not checked. Existing application windows and their unsaved edits were left open. The application also reported remote sample-thumbnail upload errors. No test suite was run.

Jan's screenshots exposed an unintended root-within-root structure in Manual and review entrypoints. Updated the generator and migrated World_Manual, World_MaskedSize and World_MaskedSelection through Sdf: each now owns the supplied startup baseline and directly composes its work layers, with optional ReviewLyr strongest and GeoLyr weakest. Original wrappers/profile/expected/report are retained in evidence/before_direct_scene_roots. Updated profile stacks and marked the previous manifest observations/file inventory historical. No scene flattening or asset hierarchy migration was used. Persistent lock metadata and session authoring policy remain; Kit runtime confirmation is pending. Screenshots show unsaved application edits; disk correction does not incorporate those live edits.

Updated 2026-10-10 after adding the source-editing and composition-workbench roadmap. Draft 0.1.1.

## Composition workbench roadmap

Recorded Monaco Editor as an implementation/functionality candidate for CW-05 after bounded source inspection of AI Harness Control Center's Studio File Editor. Its separate diff library/custom inline review are distinguished from Monaco. A proposed Kit web-panel/bridge architecture requires an embedding feasibility assessment; no integration, dependency adoption or source-code copying has occurred.

CW-05 also includes requested search and replace: selection/current-buffer scope, single/all replacement, case/word/regex options, match preview and undo. Cross-layer replacements need an explicit batch plan; text substitution is distinguished from semantic namespace editing.

Added CW-05 Embedded USDA Scene Editor at Jan's request: a dockable internal ASCII scene panel, inspired by his Houdini comparison, with authored-layer navigation and editing. The roadmap defines buffer/Apply/Save states, parsing, revision reconciliation, locks, undo, representation/format boundaries and proposed acceptance. This is scene-description editing, not a script console. Documentation only; no application implementation or tests were performed.

Jan further requested bulk cleanup scripts with confirmation breakpoints when moves are unclear. The roadmap and tooling requirements now specify versioned recipes, authorized bulk execution for explicit mappings, scoped decision checkpoints for ambiguous groups, resumable plans, stale-input checks and unattended needs-decision reports. No cleanup scripts have been implemented in this documentation increment.

Added four requested features to ROADMAP.md: CW-01 Open Original Layer Source, CW-02 Open Referenced Asset With, CW-03 Opinion Inspector and Routing, and CW-04 Contract-Guided Bulk Migration. Each includes user actions, definitions still needed, side effects and proposed acceptance. The preferred asset editor is a separate custom Omniverse instance with a lighter alternative renderer; no renderer/build has been selected or verified. Source identity, dirty-state reconciliation, shared-source impact, semantic delta classification, exact variant destinations, selective moves, recovery and evaluation are explicit requirements. TOOLING_REQUIREMENTS.md links these adapters to DT-01–09.

This increment changes roadmap documentation only. No implementation, source cleanup, tests or application checks were performed. Next planning work is to agree source/resolver support, application presets, inventory/plan schemas and bounded acceptance fixtures before implementing these features.

## Purpose and shared evaluation

Jan requested that README.md introduce the project through his OpenUSD journey and its purpose, replacing the opening focus on named reviewers. It now defines scalable composition from assets into nested assemblies and scenes, with control at the rightful ownership level. Jan clarified that the contract itself is the eval for agents and other humans: compare results against the applicable contract/profile, then revise the work until it fits. The README records that loop, maps the stated requirements to existing CC/DT provisions, and explains its role in consistent work across tasks, projects, repositories and agents. The compact paradigm diagram and version 0.1.1 remain.

Concept review used the current ownership/interface rules, CC-12 acceptance requirements, CC-17–19 deterministic execution/evidence requirements, CC-20–25 profiles and boundaries, the DT requirements, and the example's profile/expected outcomes. These support the stated direction. Remaining work is to define scenario-specific evaluation inputs, pass/fail criteria and scale/performance limits, then implement and execute the agreed evaluations. The existing example/default observations do not establish broad scalability or automated conformance. This was a documentation and concept review; no USD/code changes, tests or new acceptance runs were made in this step.

## README paradigm overview

Jan requested a simpler version of the paradigm in README.md. A new section near the top gives the core idea, a compact left-to-right Mermaid chart (root → vertical scene layers → reusable sources), the bottom GeoLyr position, session-authoring/persistence guidance, and links to the detailed ownership diagram and project structure. The detailed charts retain their full content. The README diagram was rendered with Mermaid 11.4.1 and visually inspected; no USD files, runtime behavior or acceptance results changed in this documentation step. No tests were run.

## Current version and stack clarification

Jan corrected the current version to **0.1.1** and confirmed the root-plus-stack paradigm: GeoLyr is the bottom (weakest) scene sublayer, with other scene contributions above it. Jan then clarified that the overall diagram must remain left-to-right and retain the original explanatory detail. The Mermaid charts in CompositionContracts.md and PROJECT_STRUCTURE.md now show three columns: root/authoring, vertical scene stack, and reusable sources. They restore asset geometry/intrinsic transforms/materials/variants, assembly-owned child choices, material-library links, optional work roles, review exceptions and owner/variant-context guidance. The existing DataLyr → TransLyr → VariLyr → GeoLyr order is numbered; optional and review roles use dashed rows. CC-23 records the bottom-GeoLyr convention; the profile still declares the relative order above it.

The SVG memory chart is exported from the detailed Mermaid source. A headless Mermaid 11.4.1 render was visually inspected: root left, vertical stack middle with GeoLyr lowest, reusable sources right, and all column titles and role descriptions visible. Edges connect the column subgraphs to preserve their independent vertical layout; their labels name the actual contributing layer. This is diagram preview evidence, not USD or Kit acceptance.

Current prose, generator/profile labels and the `cc:profile` custom metadata in all 29 active USD layers now use 0.1.1. USD metadata was updated through Sdf APIs; sublayer order, geometry, transforms, variants, template content and session defaults were retained. The current build manifest refreshes file identities and explicitly carries forward its earlier USD observations. Its original bytes are preserved in `harness/evidence/build_before_version_0.1.1.json`; earlier evidence, including `source_review_0.2.json`, keeps its original labels. No tests, new stage read-back or Kit/renderer acceptance were run for this correction.

## Version control handoff

Jan requested commit and push on 2026-10-10. The repository already contained initial commit `0ea84b4` on `main` and the configured origin `https://github.com/jph2/OpenUSD_Composition_Contracts.git`. At preparation, GitHub reported the repository private and fetching origin found no incoming changes. The requested commit includes the draft, example, template, startup tools, composition chart and retained evidence. `.gitattributes` preserves their recorded byte identities across Git checkouts; ordinary prose uses LF. Exact intended paths and sizes are enumerated before committing. Git history and the remote branch record the resulting commit and push; no tests were requested or run for this handoff.

## Current starting scene

`examples/01_LayeredScene/ROOT_example.usda` is now the standard scene and launcher default. It retains the supplied `/World`, `/Environment`, `/Render` and OmniverseKit camera opinions, Z-up, exact saved centimetre metric, 60 fps and time codes 0–100. The original assets compose under `/World` via DataLyr, TransLyr, VariLyr and GeoLyr. World_Manual is a compatibility alias; the scenario and conflict entries use the same baseline. Session authoring and persistent-layer protection remain the requested default through the launcher/helper.

The supplied root and prior package versions were preserved in `harness/evidence/standard_root_adoption`. The reusable template and two locally copied Kit texture dependencies live in `templates/Omniverse`; generated texture copies live under `010_ASS_USD/Envs/OmniverseStandard/Resources`. The previous scene Env/Mat/Cam/Light/Render layers and Ground asset files were retired to evidence. The active package now has 29 USD layers. No installed Kit or sibling project files changed.

Actual checks: a fresh candidate was authored using OpenUSD 26.08 before applying the bounded replacement. Initial authoring exposed a temporary Sdf layer handle lifetime issue; the generator now retains that handle and completed the fresh build. USD read-back covers five saved entrypoints and records identity `/World`, unchanged asset configuration, Z-up, the exact supplied units, 60 fps, 0–100 and `/OmniverseKit_Persp`. No coordinate conversion was needed or introduced. Kit material/viewport behavior, runtime session defaults and full variant acceptance remain untested. The supplied ground collider is retained; no simulation result is claimed.

## Previous session-default increment

Jan requested all persistent layers locked on open, Session Layer selected for authoring. CC-01 and the example guide distinguish default temporary session work from deliberate persistence. `tools/build_example.py` applies Kit lock metadata to package/scene roots and ships `Open_In_Kit.ps1` plus `_workflows/kit/session_defaults.py`. The helper protects loaded persistent layers including the root and selects the fresh session after the Layers UI initializes; it acts only on roots declaring `cc:defaultAuthoring = session`. No filesystem permissions or installed Kit app configuration are changed.

Installed `omni.kit.usd.layers` 2.7.2 and `omni.kit.widget.layers` 1.9.3 source inspection established that saved authoring-layer metadata skips anonymous targets and the usual lock helper excludes the root. Therefore direct USDA opening alone cannot guarantee the full requested default. Use the bundled launcher, or run the helper in the current Kit Script Editor. Helper execution and UI behavior have not been tested; no existing live Kit session was switched or discarded by this task.

Actual follow-up checks: the Python helper/generator and PowerShell launcher parsed successfully. USD read-back found the session policy in all four scene roots, 28 saved dependency locks in each baseline root and 30 in each review root, with zero composition errors for their saved defaults. Eight scene/asset entrypoints received policy metadata. Root edit protection is supplied by the runtime helper rather than the saved dependency lock map. The prior build manifest is retained at `harness/evidence/build_before_session_defaults.json`; the current manifest records the updated files and metadata. No tests were run.

## Exists

- CompositionContracts.md moved here as the authoritative draft, with CC-01 through CC-23 preserved.
- README, AGENTS, governance, workflow, tooling requirements, source routes, roadmap and review agenda.
- HANDOVER.md records the brief history and working decisions; AGENTS.md routes incoming agents to it. Added at Jan's request after bootstrap.
- TutorialBuilder source location replaced by a forwarding note; variant scene folders left in place.
- PROJECT_STRUCTURE.md records the revised diagram, numbered folder layout, ownership boundaries, explicit stack order and edit destinations. The user-supplied schematic, bounded VariantSetups reads and `USD_GoodStart/_Generated_Test` informed it.
- `examples/01_LayeredScene` contains 29 active USD layers: Cube/Cone packages, two standalone cube occurrences, DisplayPair, shared asset materials, supplied Omniverse startup content, project data, standard/scenario entrypoints and two deliberate review conflicts. The earlier 35-layer layout is preserved in evidence.
- `tools/build_example.py` authors this bounded fixture into a new/empty folder through OpenUSD APIs. It refuses nonempty output and is pinned to OpenUSD 26.08. It is not a general inspector or repair tool.
- `_contracts` in the example contains draft profile, ownership and expected-outcome JSON. `_pipeline_reports/build_manifest.json` records file hashes, script/contract identity, runtime and default-entrypoint read-back. `harness/evidence/source_review_0.2.json` records bounded predecessor source identities.

## Actual observations and limitations

- Authoring ran with Python 3.13.3 and OpenUSD 26.08 through `uv run --no-project --with usd-core==26.8`.
- The five current saved entrypoints reopened with default selections, default time, LoadAll and an empty session; no composition errors were returned. Cube01/Cube02 selections, resolved scale and bound material paths were read back.
- Manual and Normal-scenario entries resolve Cube02 Tall to scale `(1,1,2)`. The masked-size entry keeps Tall selected but resolves `(1,1,1)`. The masked-selection entry resolves Cube01 Finish and material to Blue despite the Normal scenario's Red selection.
- No acceptance tests, complete variant sweep, relocation trial, viewport rendering or Omniverse save/reopen review were run. Exploded, all assembly configurations and other intended behaviors remain expected outcomes awaiting that evaluation. No general conformance claim is made.

## Does not exist yet

No executable general inspector/repair pipeline, accepted conformance verdict, test suite/results, Omniverse extension, MCP integration or pipeline-nodes adapter. The bootstrap and example-authoring work did not initialize Git or publish the project; the subsequent commit/push request uses the existing private remote recorded above. No collaborator invitation or public release is part of this handoff. No license has been selected. The private pipeline repository has not been assessed.

## Next useful task

Open `examples/01_LayeredScene/ROOT_example.usda`, using Open_In_Kit.ps1 for the complete session-authoring defaults. Review the supplied viewport/environment behavior and the CC-01 template exception, then agree acceptance for variants, assembly choices, relocation and target-application persistence. Separately agree a general read-only inspector input/output contract for DT-01–03; the example JSON is a starting fixture, not an accepted general schema. If asked to share, establish hosting/access and source-resource distribution rights deliberately.

## Decisions in this increment

- Preserve CC-01–23; add CC-24 for portable storage/lifecycles and CC-25 for retained-source and published-interface boundaries.
- Keep familiar numeric directories but no numeric strength semantics. Reuse 010_ASS_USD, USD_Startpoint and USD_Wrappers; add Assemblies and 050_REVIEW; use generic `_workflows`. Reserved slots have READMEs instead of empty composed USD layers.
- Place ordinary transforms in the rightful owner's TransLyr, including asset geometry centering and scene camera/light poses. Keep variant-dependent scale/order and scene adjustment operations inside their branches.
- Use separate manual/scenario entrypoints, explicit review exceptions, asset Size/Finish and assembly Palette interfaces. Materials reference a bundled versioned library. The initial scene MatLyr ground binding was later retired when adopting the supplied root.
- Added CC-08a and a CC-23 clarification for the placement-to-scenario promotion lifecycle: preserve the original TransLyr for provenance, author complete layouts in variants, exclude only superseded unconditional placement opinions, preserve unrelated transforms, document the migration, and evaluate every promoted variant after reopen. The contract permits profile-declared exclusion, persistent muting, or layer splitting; it does not treat a note or mute alone as proof of a complete migration.
- Extended CC-08a with a selective ownership example: a shared MatLyr can retain Cube → Blue while Cone material bindings move into Cone VariLyr (Blue/Red/Green), with only the active unconditional Cone binding cleared, excluded or split. The same prim/property-level rule applies to transforms; whole-layer disabling is reserved for fully superseded layers.
- Use centimetres, Z-up and `/World` for the new example. The inspected generated predecessor uses Y-up and `/world`; it was not converted or edited.
- Keep predecessor projects and the initial HANDOVER.md intact. New USD content and the authoring script were created here; no private pipeline content was accessed or copied.
- `.gitignore` excludes Python caches and local virtual environments. Shell policy rejected deletion of the generated `tools/__pycache__` cache; it was left ignored. A concurrently present `COMPOSITION_MEMORY_CHART.svg` was preserved and is not attributed to this task.

## Continuity

The origin was a TutorialBuilder discussion of local opinions masking variants. It developed into explicit ownership at asset/assembly/scene scopes, separate layer roles and deterministic inspection/repair requirements. The independent project enables focused feedback from Nandu, Dylan and the AOUSD IEDT group while leaving future GoodStart/workcell integration open. Their review or acceptance has not occurred here.
