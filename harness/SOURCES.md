# Sources, provenance and integration routes

## MoGraph viewport diagnosis — 2026-10-11

The user's attached live diagnostic shows changing sampled USD and Fabric
PointInstancer positions during playback while the viewport remains visually
static. Kit log version paths identify Kit 110.3.2 with FSD enabled. Reviewed
NVIDIA's [Kit 110.3 release notes](https://docs.omniverse.nvidia.com/dev-guide/latest/release-notes/110_3.html),
which list OMPE-104540: scene-partitioned instanced prim transforms may remain
stale while Fabric world transforms are correct, and mark it fixed in Kit 110.3.
The match to the observed symptom is strong, but the exact enabled state of
`/renderer/scenePartitioning/enabled` is not in the user's report. The user's
installed extensions identify as 110.3.2, later than the release where NVIDIA
marks this issue fixed, which weakens this as a root-cause claim. The scene has
no authored `primvars:omni:scenePartition`; NVIDIA says RTX scene partitioning
defaults off in its [scene partition documentation](https://docs.omniverse.nvidia.com/materials-and-rendering/latest/cameras.html).
The runtime now logs/checks that setting and scopes a temporary disable/restore
to MotionGraphics when it is enabled. This safeguard is a hypothesis to verify
in the user's Kit viewport, not confirmed acceptance. No app config was changed.

## Portable setup reference

On 2026-10-10, inspected USD_GoodStart/scripts/setup_usd_project.bat and setup_usd_project.ps1 and its generated standalone batch launcher at Jan's request. Used the companion-launcher pattern only. Our setup extracts this repository's authored preset using Windows PowerShell; it does not copy the GoodStart generator or depend on that sibling repository. Packaging inventory is not USD/Kit validation evidence.

## Upstream adoption review — 2026-10-10

Reviewed the [OpenUSD proposals directory](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals) and bounded sections of the linked READMEs for [validation](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/usd-validation-framework), [namespace editing](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/namespace_editing), [LOD](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/level-of-detail), [spline animation](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/spline-animation), [profiles](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/profiles) and [nested physics bodies](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/physics_nested_bodies). Status badges retrieved: validation implemented 24.11; LOD and profiles implemented 26.08; namespace proposal published. These describe upstream documents, not verified local support. Spline and nested-body implementation maturity was not independently established.

The current [UsdNamespaceEditor API](https://openusd.org/release/api/class_usd_namespace_editor.html) documents preflight, affected layers, relocates and registered dependent stages, including exclusions for unloaded/unselected content. External identifier/binding repairs remain our additional responsibility.

Read [SimReady Foundation README](https://github.com/NVIDIA/simready-foundation) and its [profile validation guide](https://github.com/NVIDIA/simready-foundation/blob/main/nv_core/sr_specs/docs/guides/profiles_validation_workflow.md). Requirement/feature/profile versioning and use-case validation inform our adoption plan. The README and guide use different profile-name examples; exact identifiers must be resolved from a pinned release before implementation. No installation, validator execution, asset download or certification occurred.

[AOUSD's public interest-group page](https://aousd.org/community/interest-groups/) supports IEDT's industrial requirements/recommendations remit. The anticipated workcell guideline project is Jan's discussion context; formal approval, schedule and this repository's participation were not verified. Keep that distinction in public positioning.

## Research positioning and NVIDIA comparison — 2026-10-10

Added §6.3.8 to the user-authorized AAS_OPC_OpenUSD_RESEARCH_v14.md, positioning this project as the next step from USD GoodStart and linking its GitHub repository. Bounded research insights extend CC-12 (requirements/evidence and promotion) and CC-24 (link/cache/snapshot lifecycle and compatibility).

Reviewed [Isaac Sim 6.0 Asset Structure 3.0 tutorial](https://docs.isaacsim.omniverse.nvidia.com/6.0.0/openusd_tuning_tutorials/tutorial_02_asset_structure.html), [6.1 asset structure](https://docs.isaacsim.omniverse.nvidia.com/6.1.0/robot_setup/asset_structure.html), and the published [DSX SimReady asset workflow](https://docs.omniverse.nvidia.com/dsx/latest/simready-assets.html). Comparison is bounded to documented component separation, physics alternatives, transform placement, properties/connection points and validation. DSX dataset binaries, full scene stacks and runtime behavior were not inspected; no claim about exact DSX scene sublayer order or compatibility is made.

## Identity and composable bindings review

Follow-up on 2026-10-10: read the full 11-page **Composable Bindings: Simplified System Integration**, v1.0, November 2025, through [the supplied link](https://aka.ms/ComposableBindings), which redirects to a Microsoft-hosted PDF. Contributors are Christoph Berlin and Aaron Luk. The paper presents a flexible integration pattern, a telemetry/data-lake/view-service/OpenUSD proof of concept, and future migration from hard-coded binding logic to declarative configuration. It does not define our BindingSpec/Plan/ChangeSet/receipt schemas; those remain adaptations from Jan's research. This supersedes the earlier note below that the whitepaper had not yet been independently read.

On 2026-10-10, inspected the introduction and relevant sections 2.2.3, binding artifacts, 6.3.7 and 7.10 of Jan's local `AAS_OPC_OpenUSD_INTEGRATION/docs/AAS_OPC_OpenUSD_RESEARCH_v14.md`. This is a bounded reading of supplied research, not adoption of every recommendation or validation of its upstream bibliography. Its declarative mappings, artifact lifecycle and identity separation inform CC-27/28. No sibling repository was modified.

Also inspected Aaron Luk's [proposal #105](https://github.com/PixarAnimationStudios/OpenUSD-proposals/pull/105) and its [source draft](https://raw.githubusercontent.com/asluk/OpenUSD-proposals/aluk/source-identifiers/proposals/identifier_separation_of_concerns/README.md). The retrieved draft identifies itself as version 0.1 DRAFT. Source/external identity is separated from namespace addressing, with dictionary and applied-schema candidates discussed. These mutable links are research evidence, not a pinned implementation or proof of an adopted standard. The Composable Bindings whitepaper linked by the research was not independently reviewed in this increment.

Project adaptations: layer provenance belongs in customLayerData; quarantine requires actual composition exclusion; rollback/persisted muting and reverse-system writes need explicit mechanisms. Identity continuity needs authoring-tool behavior and evaluation, not merely a tag. Current example IdentityLyr has only illustrative cc:occurrenceId fields on scene occurrence parents.

## Imported owner

On 2026-10-10 CompositionContracts.md moved from TutorialBuilder:

`020_Tutorials/SoftServe_NVIDIA_Upskill_Omniverse_Stream/1.x_OpenUSD/1.1_Omniverse_USD_Essentials/010_SourceFiles/examples/VariantSetups/CompositionContracts.md`

The old location now holds a forwarding note. The neighboring VariantSetups.md and A–H scene folders remain in TutorialBuilder, unchanged by this move. They are historical experiments and are not certified against this contract. Their availability is optional for reviewing this repository; no cross-repository link is a portable shipped example.

## Public evidence routes

| Reference | Use and inspection boundary |
|---|---|
| [AI Harness guide](https://haluszka.com/ai-harness-quickstart/guide/) | Overview, controlled workflows and local starter pages consulted for this bootstrap on 2026-10-10. Process reference, not inherited instructions. |
| [Controlled workflows](https://haluszka.com/ai-harness-quickstart/guide/agents-skills-workflows.html) | Boundary between model judgment, fixed routines and observed outcomes. |
| [Local harness starter](https://haluszka.com/ai-harness-quickstart/guide/lab/index.html) | Small local project harness and explicit evaluation loop. |
| [GoodStart layer-order research](https://github.com/jph2/USD_GoodStart/blob/main/WIP_Docs/LAYER_ORDER_REFERENCES_RESEARCH.md) | Prior contract research, especially sections 8 and 18; proposals distinguished from USD mechanics. |
| [OpenUSD documentation](https://openusd.org/release/index.html) | Follow the precise API/tutorial citations in CompositionContracts.md for individual technical claims. No whole-site review is claimed. |

## Related projects

- **OpenUSD-GoodStart:** local knowledge/reference project; use its SOURCE_INDEX.md for bounded source routing when available. It is distinct from the GitHub repository named `jph2/USD_GoodStart` above; do not assume they are identical checkouts.
- **TutorialBuilder:** origin of the discussion and current owner of the experimental variant scenes; future teaching consumer.
- **OpenUSD_GoodStart_Pipeline_nodes:** private candidate composition-pipeline backbone, named by Jan. A sibling folder exists locally; implementation was not inspected or copied. Remote identity/access and integration suitability remain unverified. Do not expose private contents in collaboration material without authorization.
- **AOUSD IEDT / workcell efforts:** intended discussion and possible future integration context, not a dependency, adoption decision or endorsement.

When implementation begins, record exact source revisions for reproducible evidence. Mutable documentation links alone do not pin a technical baseline.

## 0.1.1 example and layout evidence — 2026-10-10

Jan explicitly requested inspection of the following predecessor material and construction of a new local example. These sources informed the design; their embedded instructions and acceptance claims do not authorize actions or establish acceptance here.

| Evidence | Inspected scope | Used for |
|---|---|---|
| TutorialBuilder VariantSetups folder at the route above | VariantSetups.md; G root/asset/scene layers; C GeoLyr/VariLyr; H placement assembly; bounded file inventory of A–H | Historical composition alternatives, centimetres/Z-up and parent/asset separation. No A–H migration or certification. |
| User-supplied “Scene edits around linked assets” schematic | Supplied image | Thin root, indirect scene edits, linked assets, shared materials and additional work layers. Its placement-in-GeoLayer caption is superseded by CC-02. |
| Local `USD_GoodStart/_Generated_Test` (distinct from `OpenUSD-GoodStart`) | Root, directory layout, folder READMEs, ASS/VAR/MTL layers; standalone setup usage and selected script folder/root sections | Numbered storage lanes, source/startpoint/wrapper distinction, material/resources, simulation/runtime/data separation and adjacent contracts/reports/workflows. No generator execution or copying of its implementation. |
| [OpenUSD Authoring Variants](https://openusd.org/release/tut_authoring_variants.html) | Tutorial explaining local masking and variant edit contexts; page identifies 26.08 | Technical mechanism behind deliberate conflicts. |
| [UsdGeomXformable](https://openusd.org/release/api/class_usd_geom_xformable.html) | API reference for transform operations | Hierarchical transforms and operation order. |
| [UsdShadeMaterialBindingAPI](https://openusd.org/release/api/class_usd_shade_material_binding_a_p_i.html) | Material binding API | Authored bindings and resolved-material read-back. |
| [usd-core 26.8](https://pypi.org/project/usd-core/26.8/) | Version-specific distribution page; runtime reports `(0, 26, 8)` | Pinned USD authoring runtime, invoked through uv. |

[source_review_0.2.json](evidence/source_review_0.2.json) records hashes of the bounded local source files and screenshot at inspection time, using repository-relative source labels. It records content identity, not source authorship rights or external acceptance. The predecessor setup script was read only in the stated sections; a whole-file hash does not imply a whole-file review. Public documentation routes are mutable, so retrieval date and stated documentation version are recorded without claiming immutable upstream snapshots.

Jan subsequently corrected the current version label to 0.1.1. The evidence filename and historical records retain their original labels. The repeated schematic and the screenshot highlighting the misplaced Mermaid GeoLyr clarified the intended vertical stack: GeoLyr at the bottom, other scene layers above it. This clarification is recorded in CC-23 and the current diagrams. The previous build manifest is retained at [build_before_version_0.1.1.json](evidence/build_before_version_0.1.1.json); the current manifest distinguishes refreshed file identities from retained USD observations.

Jan's follow-up screenshot clarified that the overall flow must remain left-to-right and preserve the original asset/assembly/material ownership detail. The detailed chart now uses three columns with a vertical middle stack. The [Mermaid subgraph direction documentation](https://mermaid.js.org/syntax/flowchart.html#direction-in-subgraphs) explains that edges from internal nodes to outside a subgraph override its direction; column-boundary connections preserve the intended layout. The diagram was rendered with Mermaid 11.4.1 for the SVG export and visual preview.

The new example's own build manifest records generated package content, authoring script/contract hashes, runtime and observations. All example geometry and layers were newly authored through the local script; no private pipeline code or scene was imported.

## Session-default implementation evidence — 2026-10-10

Bounded read-only inspection of the installed Kit extensions `omni.kit.usd.layers` 2.7.2 (`LayerUtils` authoring-target save/restore and lock helpers; LayersState API) and `omni.kit.widget.layers` 1.9.3 (stage-attach restoration, lock handling and layer-window setting names) informed the startup helper. Anonymous targets are skipped by saved authoring metadata; the ordinary lock helper excludes the root. No installed extension code was copied or edited, and no installed tests were run.

The public [LayersState reference](https://docs.omniverse.nvidia.com/kit/docs/omni.kit.usd.layers/latest/omni.kit.usd.layers/omni.kit.usd.layers.LayersState.html) documents UI layer locks and their distinction from disk permissions. The [Layers documentation](https://docs.omniverse.nvidia.com/extensions/latest/ext_core/ext_layers.html) describes session content and authoring targets. These sources support the application boundary, not a claim that the new helper has been executed in Kit.

## User-selected Omniverse root — 2026-10-10

Jan supplied `examples/01_LayeredScene/ROOT_example.usda` and requested it as the standard scene. Its authored content establishes the exact startup profile: `/World`, top-level `/Environment` and `/Render`, `OmniverseKit_*` viewport opinions, Z-up, `metersPerUnit = 0.009999999776482582`, 60 fps and time codes 0–100. This is direct local evidence, not a claim about every Omniverse product's defaults.

The untouched source and SHA-256/resource records are in `harness/evidence/standard_root_adoption`. `templates/Omniverse/ROOT_example.usda` retains the template with only two texture paths rebased for reuse. Its sky HDR and grid image were copied from the installed `omni.kit.stage_templates` 2.0.3 files referenced by the supplied root. The example ships local copies of those textures; `OmniPBR.mdl`, OmniRtx schemas and viewport camera completion depend on the Kit runtime. No Kit installation or predecessor repository was changed. Earlier example file versions and the previous build report were retained before replacement.

## Kitchen Set pattern adaptation — 2026-10-10

At Jan's request, inspected the local Kitchen_set publication (version notes last
updated 2022-07-21): 76 packages, reference-to-interface/payload-to-content pattern,
empty public variants above payloads and an instanceable entrypoint. The comparison
is recorded in STATE.md. This is evidence of a published set, not the full film
production authoring pipeline. The new examples implement that pattern using our
Cube/Cone/DisplayPair and Palette files; no Pixar asset geometry, textures or code
were copied into the project. CC-05a–c adapt loading/sharing and generated-writer
requirements. The only input to the Python layout driver is a bundled synthetic
normalized JSON signal or an explicitly supplied replacement, not live equipment.

## MotionGraphics controls panel — 2026-10-10

Follow-up 2026-10-11: Jan reports that visible motion began only after restarting
Kit and reloading the scene. This user observation is recorded as a lifecycle
workaround, not a causal diagnosis or an acceptance result for automatic refresh.
Reviewed the existing local MotionGraphics root, Geo/Vari/Data layers, animation
baker, shared model and Kit adapter to document their current division of work.
The JSON is an editable local mock source: the Kit watcher reads it and the model
validates/maps it; it is not a server, telemetry stream or live connector. The
README's flowcharts describe current code plus future input-adapter direction,
and explicitly mark the viewport refresh boundary as under development.

Playback follow-up: user diagnostics at 22:03:55Z are all paused, with matching
runtime/USD/Fabric positions and an unfrozen same-stage viewport. Play occurs
later in the log. They provide no dynamic-cache failure evidence. Changed the
writer to explicit bounded time samples, the standard PointInstancer animation
mechanism described by [NVIDIA's instancing guide](https://docs.omniverse.nvidia.com/usd/latest/learn-openusd/independent/modularity-guide/instancing.html#animation).
GoodStart lookup of SetTimeSample searched spec, manual and full snapshot with
no exact match; consulted [OpenUSD SdfLayer API](https://openusd.org/release/api/class_sdf_layer.html)
for SetTimeSample, EraseTimeSample and ListTimeSamplesForPath. Existing offline
baker already uses SetTimeSample. These establish APIs and design, not that
static-default updates caused this particular renderer symptom. Runtime
acceptance and performance of the new two-sample preview are pending.

Follow-up 2026-10-11: Kit logs at 21:53–21:54Z show time advancement and runtime
writes without composition warnings; user reports the picture remains static.
Inspected installed viewport 110.0.0 `api.py` (stage/context, time, updates_enabled,
freeze_frame) and USDRT 7.6.3 API (Stage.Attach/HasPrimAtPath and attributes) for
a read-only report. Installed FSD documentation says USD synchronization normally
runs before rendering, while its known-issues page describes some missed array
updates with fast diffing. Neither establishes this scene's fault; live value
comparison is pending. Public counterpart: [FSD and OmniHydra differences](https://docs.omniverse.nvidia.com/kit/docs/usdrt.scenegraph/7.6.3/fabricsd/fsd_vs_omnihydra.html).

For apparently inactive Play, inspected installed omni.usd 1.18.0 `_usd.pyi`
get_timeline/get_timeline_name and omni.timeline 1.1.0 Timeline's play, pause,
is_playing, is_auto_updating/set_auto_update and get_director. The context API
provides the timeline used by that USD context; the prior controller selected the
global default. Play's optional start/end arguments are time codes; current time
is seconds. A director makes other state-changing calls ineffective. The revised
adapter uses these APIs with visible clock/output and composition diagnostics.
No live timeline state or proof of a named-timeline mismatch was obtained.

Later runtime evidence: the user reports successful operation, and existing Kit
logs at 21:27:03/21:27:40Z show panel creation, followed by successful control saves
and accepted JSON. The 21:31:03Z permission-restore failure followed layer muteness
changes. GoodStart lookup for `SdfLayerHandle` searched AOUSD Core (no matches),
Pixar manual and full snapshot (matches; initial excerpts only term usage).
Targeted full-snapshot line 4992 explains the layer registry's weak handles and
that stage-reached layers depend on composition/load state. Installed Kit
Layers 2.7.2 layer_utils.py uses `Sdf.Find(identifier)` with a truth check.
These support registry lookup and lifetime guards in our cleanup fix; they do
not independently prove the particular failed live handle was expired. No live
test of that fix has run.

Following the reported missing `control_hints` at runtime, inspected Kit's
`kernel/py/omni/ext/_impl/stat_cache.py` and `custom_importer.py`. The former
patches importlib's file-stat lookup with a cache and supplies an explicit refresh;
the latter invokes module loaders. The source defines the missing function, but
the package's Python 3.12 core pyc predates it. The bootstrap now compiles its two
fixed helper paths from current source bytes to avoid this import-cache path.
This is a targeted reload fix; the exact live cached module was not inspected.

For the requested visible panel, used the omniverse-kit-ui skill (based on Martin
Jajam's presentation) and read installed `omni.ui` 3.3.1 `_ui.pyi`: Window
construction/visibility/focus/destroy, FloatSlider, SimpleFloatModel bounds,
ComboBox root selection model, value callbacks/removal, labels and scrolling.
Read installed `omni.timeline` 1.1.0 play/pause API. These are version-matched API
sources, not a panel execution result. Added a script-created native window,
persistent status and explicit DATA JSON save/reload through the shared model.
File I/O and saving use workers; bounded validation and UI/scene updates use the
Kit event loop. No installed extension code was modified. Kit UI acceptance
remains pending; the earlier future-panel note below records the prior increment.

## MotionGraphics runtime and future panel — 2026-10-10

Read the local omniverse-kit-ui skill and its patterns. Inspected the installed
My USD Composer application configuration and `omni.timeline` 1.1.0 Python API
stubs (Kit app build folder 110.3, Python 3.12 extension build). The controller
uses `get_timeline_interface().get_current_time()` and Kit `next_update_async()`;
file reads/JSON validation run off the update thread, USD writes stay on it.
This is API/source inspection, not a Kit execution result.

- [Timeline API](https://docs.omniverse.nvidia.com/kit/docs/omni.timeline/latest/omni.timeline/omni.timeline.ITimeline.html): timeline time is in seconds; the bake maps it to 60 time codes/s.
- [Timeline events](https://docs.omniverse.nvidia.com/kit/docs/omni.timeline/latest/EVENTS.html): current public API uses newer event dispatch; the implementation avoids assuming that newer event interface exists in the installed build.
- [omni.ui API](https://docs.omniverse.nvidia.com/kit/docs/omni.ui/latest/API.html): Python can construct a Window and controls directly. A script-created panel is feasible without creating a new extension package; object/callback lifetime and cleanup must still be owned. No panel was implemented in this increment.

The MoGraph example uses our existing sources only. Its PointInstancer prototype
selections remain asset controls, while point transforms/prototype indices are
array data generated by the shared pure-Python model. Runtime preview is opt-in;
USD metadata declares the binding but executes no Python by itself. No installed
Kit application or extension files were changed.

GoodStart authority lookup for `PointInstancer` searched AOUSD Core, Pixar manual
and full snapshot. Core had no term match; the manual's UsdGeomPointInstancer
section described prototype scattering, animation and integer-ID masking. The
full tier also returned matches (its first excerpts were index entries). This
supports the API mechanism, not an AOUSD endorsement of CC-05d or our layer roles.

## Root locking and Kit settings save — 2026-10-10

User's 21:02:49Z traceback identifies the installed USD 0.25.11.kit.5 runtime.
Bounded source reads confirmed that Layers 2.7.2's
`LayerUtils.save_authoring_layer_to_custom_data` sets root customLayerData and
Viewport 110.0.0's `save_implicit_cameras` enters a root edit context to write
cameraSettings. Widget Layers 1.9.3 invokes the former on SETTINGS_SAVING.
Both fail when our helper sets the root's permissionToEdit false. The correction
uses the active-root exception rather than patching installed host callbacks.
No installed files changed; the updated helper has not yet been exercised on Save.
