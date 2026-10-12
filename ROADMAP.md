# Roadmap

**0.1 bootstrap — complete:** move the contract, establish agent entry/governance/workflow, record deterministic tooling requirements and private pipeline candidate. Variant scenes remain in TutorialBuilder.

## 1. Collaborative proposal review

Review DISCUSSION.md with intended collaborators when Jan chooses to share. Agree scope, vocabulary, ownership model and minimal profiles. Record objections and changes by CC ID. Decide repository hosting/access and licensing before distribution. No invitations or publication have occurred.

## 2. Minimal reference package

**Authored; acceptance pending.** Jan requested a new example and project layout using VariantSetups, the scene-layer schematic and `USD_GoodStart/_Generated_Test`. `examples/01_LayeredScene` now contains cube/cone packages, two cube occurrences, a reusable assembly, shared materials, placement, manual/scenario choices and separate property/selection conflicts. PROJECT_STRUCTURE.md records the revised storage model; CC-24/25 cover storage lifecycle and imported-source boundaries.

The USD-aware author records a default-entrypoint read-back; full variant, relocation, renderer and UI save/reopen acceptance remain open. Agree that acceptance scope before promoting the example to best-practice status. Historical TutorialBuilder examples stay in place.

## 3. Deterministic read-only core

Implement DT-01 through DT-03 and reporting portions of DT-09. Agree machine-readable profile and finding schemas. First useful outcome: explain an authored opinion, owner, variant context and conflict without modifying the stage.

## 4. Repair planning and evidence

Implement dry-run plans, candidate comparisons, concurrency checks, rollback and audit. Add execution only after its authorization and recovery model is explicit. Exercise the declared fixture matrix under a specifically authorized implementation/verification task.

## 5. Pipeline-backbone assessment

Review OpenUSD_GoodStart_Pipeline_nodes privately for interface compatibility and reuse. Record adopt/adapt/defer decision; expose a public adapter contract without requiring private access. Assess this before selecting an orchestration implementation.

## 6. Workcell and integration profiles

Identity and composable-binding work follows CC-27/28: preserve governing ERP/PLM or equivalent IDs at first intake/authoring, define scoped source/occurrence/physical-instance records and namespace-change behavior, and compare identifier storage candidates from proposal #105 without assuming standardization. Establish identity before dependent assembly publication or binding activation, including repeated-import reconciliation and a declared policy for provisional local IDs. Then specify BindingSpec/Plan/ChangeSet/receipt interfaces and deterministic resolution to layer/variant destinations. Pilot repeated assets and nested assemblies, ambiguous-ID checkpoints, one bounded external mapping, and recovery. DATA holds stable identity/context, SIM holds results and RUNTIME holds declared operational output. No integration engine or cross-system write-back is authorized by this roadmap.

Extend through rig/animation/physics boundaries, material ownership, PLM/UNS mappings, simulation/live authority and snapshots. Use workcell evidence to refine the proposal. Consider optional Omniverse interface and MCP adapters around the proven core.

## 7. Integration or transfer

Evaluate incorporation into GoodStart or a relevant collaborative effort on its merits. Repository ownership, standardization, licensing and stewardship require explicit decisions; no outcome is presumed.

## 8. Source editing and composition workbench

**Requested 2026-10-10; planned, not implemented.** These four features connect interactive authoring with the deterministic inspection and repair core. They elaborate CC-11/16–19/21/23–25 and DT-01–09. The UI and agents must use the same inventory, ownership decisions and move plans. The current temporary-file edit behavior is Jan's observation; its exact installed-application path still needs inspection.

| Feature | Proposed user action | Outcome |
|---|---|---|
| CW-01 — Open Original Layer Source | Layer context menu → Open Original USDA | Edit the actual resolved text source with an explicit save/reload workflow. |
| CW-02 — Open Referenced Asset With | Layer or stage-reference context menu → Open Asset With → application | Work on the asset in a separate application, preferably a lightweight custom Omniverse instance. |
| CW-03 — Opinion Inspector and Routing | Inspect an opinion layer → select authored changes → Assign to Layer | Understand each delta's role, owner and context before distributing edits. |
| CW-04 — Contract-Guided Bulk Migration | Select scope and rule → Preview Plan → Apply | Resolve declared composition conflicts through repeatable, recoverable USD-aware operations. |
| CW-05 — Embedded USDA Scene Editor | Layer context menu → Open in Scene Editor | Inspect and edit ASCII scene content in a dockable Omniverse panel. |

### CW-01 — Open Original Layer Source

Provide a layer context-menu action that opens the original resolved USDA in a configured text editor. Show the source identity and actual destination before editing so the user can distinguish the original file from a temporary textual representation or exported copy. Define eligibility by resolved file format and storage capabilities, including text USD stored with a `.usd` suffix.

Define before implementation:

- Resolver identifier, resolved location, file format, write permission and revision; distinguish disk content from dirty in-memory content.
- Handling for anonymous/session layers, binary layers, package members, remote or read-only resources. These need explicit save/export/checkout workflows when direct text editing is unavailable; never label a temporary conversion as the original source.
- Which editor opens the file and how arguments are passed; file paths and scene metadata must not become executable command strings.
- Save, syntax validation, reload and recovery behavior. Detect external changes and concurrent in-application edits before either overwrites the other. Retain recoverable content if an edit produces invalid USD.
- Interaction with the default persistent-layer locks. UI locks must not be treated as a complete external-editor permission policy; show the source-edit scope and apply the declared ownership/write policy.

**Side effects:** editing a shared source can affect multiple open stages and consumers. Reloading can discard unsaved in-memory work unless reconciled. A text editor's undo history and the application's undo history need an explicit boundary.

**Acceptance to define:** opening a supported text layer targets its exact resolved source; saving and reloading produces the intended change; dirty-state and external-revision conflicts preserve both versions; unsupported sources receive an accurate alternative action.

### CW-02 — Open Referenced Asset With

Offer an application picker from both the layer view and a referenced occurrence in the stage view. The preferred preset is a separate instance of our own Omniverse build with a lighter alternative to RTX; also allow usdview and configured authoring tools. Renderer availability, compatibility and efficiency remain to be assessed before selecting that build or promising a particular renderer.

Define before implementation:

- Resolve the selected composition arc to its source package, entry layer and referenced prim. A prim can have multiple contributing references; present the candidates with their authoring layer and owner instead of choosing an arbitrary source. Distinguish opening the selected layer from opening the asset package's intended entrypoint.
- An application registry with executable/build version, launch arguments, supported formats, resolver context, plugins, renderer preset and process-reuse policy. Launch a separate process when requested; do not replace the current scene.
- Two explicit contexts: source-asset authoring and occurrence preview. A standalone source may omit the scene's selections, overrides, placement, lights and materials. Any transferred preview context must remain identifiable and must not silently become source defaults.
- Shared-source editing versus creating an occurrence-specific derivative. Show known consumers and the selected revision; do not imply that editing the source affects only the clicked occurrence. Unknown consumers remain an explicit limitation.
- Return/reload coordination with CW-01: detect saved changes, report the revision, and reconcile the parent application's dirty state. Closing the child process alone does not prove that changes were saved.
- A lightweight viewing profile for camera framing, units, up axis, dependencies and lighting. Evaluate shader/schema support and visual differences under the alternative renderer; a different preview appearance must not trigger material conversion automatically.

**Side effects:** additional instances consume memory and other resources even with a lighter renderer. Missing plugins, resolver setup or materials can make a valid asset appear incomplete. Released or shared packages may require a new revision and deliberate consumer adoption rather than an in-place overwrite.

**Acceptance to define:** select a nested referenced asset, choose an application, open the correct source/prim in a separate instance, save a bounded change, and deliberately refresh the parent. Include multiple references, missing dependencies, dirty parent state and a renderer compatibility comparison.

### CW-03 — Opinion Inspector and Routing

Provide a dedicated opinion view for Session, Opinion/Review and persistent layers. Show authored fields rather than only a generic delta marker. Users can inspect a row or context menu, filter/group changes, and assign selected contributions to their rightful layer through a previewed move plan.

Each row needs source layer and authored spec path; composed prim path when available; property/field; authored value or sample summary; category; owner and evidence; variant branch; current contribution/masking status; proposed destination; and the applicable CC rule. Separate authored data from the composed result. An opinion inventory is not automatically an edit history: showing what changed requires a recorded baseline/revision.

Use text labels and optional icons/colours for transforms, material bindings, shader inputs, animation, references, metadata and selections. Category and context are independent: a transform can be animated or inside a variant. Colour alone must never determine ownership or be the only way to understand a row. Support ambiguous classifications and unavailable dependencies explicitly.

Routing must retain related fields, such as transform operations and their order or material connections and their dependencies. Show destination collisions and any required layer creation. A move into a variant requires an exact owner, set and branch; selecting a layer named VariLyr is insufficient. Keep inspection read-only until the user invokes the migration workflow.

**Side effects:** inspecting inactive branches and large nested scenes can be expensive. Define pagination, scope limits, cancellation and stale-report detection. Filtering must not hide related opinions that a move needs to preserve.

**Acceptance to define:** an opinion layer containing cube/cone materials, transforms, animation and variant selections yields distinguishable records and explainable destinations. Routing only the cone binding leaves Cube → Blue intact; uncertain ownership remains unresolved rather than guessed.

### CW-04 — Contract-Guided Bulk Migration

Build reusable operations for moving selected authored fields between layers, separating mixed opinion layers, and promoting unconditional values into variant branches under CC-08a. Agents propose intent and explain ambiguity; deterministic USD-aware scripts construct and execute the same plans used by CW-03.

Every operation must declare source revisions, selected prims/fields, ownership/profile revision, exact destination/context, source disposition and expected behavior. Distinguish a behavior-preserving relocation from an intentional conflict correction. Plan destination authoring and source removal/exclusion together; a copy that leaves a masking source active does not complete a promotion.

Define before implementation:

- Recipes and boundaries: ordinary placement → rightful TransLyr; selected material bindings → rightful MatLyr; scenario-dependent values → specified variant branch; retain source snapshots and migration notes outside the active conflicting contribution.
- Coherent transforms: operation values/order, pivots, reset behavior, samples and parent context. Moving placement into a child adjustment transform is a different operation that may require conversion; do not treat it as a path-only move.
- Preserve relationship targets, connections, list operations, metadata and relative asset-path meaning. Evaluate resolved material bindings, including their hierarchy and purpose, rather than equating a shader value with a binding.
- Variant coverage, default scenario and fallback behavior; preserve unrelated properties and prims. A source layer may be excluded wholesale only after accounting for its remaining contributions. Define persisted exclusion and restoration.
- Destination collisions, missing owners, referenced instances, unloaded content and unsupported fields. Stop the affected operation with an explanation instead of guessing or silently skipping it.
- Dry-run reports, isolated candidates, revision checks, recoverable multi-file application, cancellation, audit and repeat-application behavior. Define the scope of an authorized batch and which changed inputs invalidate its plan.

**Acceptance to define:** promote the cone's Blue binding into Blue/Red/Green variants while retaining Cube → Blue; promote cone placement while retaining cube placement; distribute mixed opinion-layer edits without extracting animation or variant-dependent data into ordinary TransLyr. Evaluate declared variants, time samples and reopen behavior, including deliberate conflict and interrupted-application cases. Preserve authored provenance without keeping superseded competing fields active.

### CW-05 — Embedded USDA Scene Editor

**Implementation/functionality candidate: Monaco Editor.** The inspected AI Harness Control Center Studio File Editor uses Monaco through `@monaco-editor/react`; its side-by-side diff uses the separate `react-diff-viewer-continued` component and its inline review has custom implementation. These are references for editing and diff functionality, not an adopted dependency or permission to copy that application's code.

Assess a Kit extension hosting a web frontend containing Monaco, with an explicit bridge to USD-aware layer inspection, validation, Apply and Save. This architecture is a candidate: verify the target Kit build's supported web embedding surface, JavaScript/worker loading, offline packaging, focus/keyboard handling, docking, lifecycle, performance and distribution requirements before choosing it. Monaco supplies text editing; USDA language support and composition-contract diagnostics need their own integration. Compare diff options separately, including Monaco's diff functionality and the inspected application's approach. If web embedding is unsuitable, retain Monaco as a functionality reference for another implementation. No working Omniverse integration is claimed.

Provide a dockable ASCII scene editor inside Omniverse, inspired by the internal scene-code view Jan described in Houdini. Open it from a selected layer, with optional navigation from a selected prim/property to its authored spec. This panel edits USDA scene description; it does not execute Python or serve as a script console. Integrate it with CW-03 so an opinion can be traced from the inspector to its authored text.

Define before implementation:

- Clearly identify the selected layer, resolved source, revision, dirty state, edit permission and displayed context. Default to that layer's authored content; any composed/flattened inspection view must be separately labelled and must not save over the source layer.
- Syntax highlighting, line numbers, search and replace, prim/property navigation and useful parse diagnostics. Search/replace supports current selection or the current layer buffer, next/previous match, replace one and replace all, case sensitivity, whole-word matching and optional regular expressions. Preview matches and replacement counts before Replace All; keep it undoable and subject to the same Apply validation. Cross-layer replacement requires a separate explicit scope and reviewed batch plan. Text replacement does not perform a semantic prim rename or automatically repair relationship targets, connections or asset paths. Preserve variant paths and distinguish selected scene occurrences from their source specs when navigating through references.
- Buffer, Apply and Save semantics: typing changes the editor buffer; Apply parses and validates a candidate before changing the in-memory layer; Save deliberately persists the applied layer. Show unapplied text and unsaved layer changes separately. Define how Session/anonymous content is deliberately persisted.
- Synchronization with viewport/UI edits and external editors. Detect stale buffers and changed revisions before applying or saving; offer a reviewable reconciliation instead of overwriting newer work. Define undo/redo across text application and ordinary scene edits, retaining recoverable prior content.
- Persistent layers start protected under the existing authoring policy. Editing a shared asset source must identify that scope and follow its ownership/write policy. Invalid text must leave the last valid layer intact, with diagnostics and the user's buffer preserved.
- For binary USD, package members or remote sources, identify whether the panel shows a generated ASCII representation and which apply/save operations are supported. Never silently change file format or present generated text as original on-disk USDA. Reuse CW-01's source-resolution and permissions model.
- Applying a text edit can change arbitrary composition arcs, paths, metadata and dependencies. Show a change summary and route applicable contract findings through the inspector; define bounded parsing/refresh for large layers so each keystroke does not recompose the stage.

**Side effects:** text application can affect multiple consumers, invalidate selected prim paths, or conflict with another editor's unsaved changes. Define handling of comments and formatting before round-tripping through USD serialization; authored semantic preservation and exact text preservation need separate acceptance criteria.

**Acceptance to define:** open a layer in the docked panel, navigate to a variant/property, edit valid USDA, apply it to the intended in-memory layer, save and reopen with the expected result. Cover invalid text, locked layers, stale buffers, undo, anonymous layers, binary representations and concurrent external/UI edits. No script execution is part of this feature.

### CW-04a — Clean leaf assets and shared resources

**Status: planned; not implemented as a reusable cleanup tool.** The composition skill already defines the workflow under “Clean up asset structures and resource ownership”; this roadmap item tracks building the reusable execution support (CC-00–00d, CC-18/19; DT-01–09).

**User outcome:** ask an agent to “clean up this asset folder using our conventions,” or use a future workbench action. Users should not need to type terminal commands. Agent, script and eventual UI entrypoints use the same bounded implementation.

**First delivery:** inspect selected local asset entrypoints and produce a readable proposed layout and dependency/move report without changing files. Then support recoverable application of that plan: place independent leaves together where appropriate, reuse compatible shared MatLib and texture resources, retain private resources when justified, remove redundant folder nesting, and update references, resource paths and authoring/lock metadata. Preserve direct-open preview environments outside default asset prims. Do not remove the deliberately retained teaching scaffold without a cleanup request.

**Acceptance:** cover variants, unloaded payloads and preview dependencies; preserve asset interfaces, bindings and resource interpretation; report unknown consumers; reject stale/conflicting plans; keep rollback data; repeated application must not introduce further changes. Require visual/runtime evaluation only as explicitly selected acceptance work, and report missing coverage. Do not merge resources based on filenames or visual similarity alone.

**Later optional delivery:** dependency-complete USDZ export for a declared supported consumer, preserving editable sources and authored alternatives. Ordinary ZIP remains an unpack-before-use transport option. Packaging and performance evaluation are separate from the first cleanup delivery.

### Reusable cleanup scripts and decision checkpoints

Bulk execution is a primary delivery surface for CW-04. Build a versioned catalogue of bounded USD-aware cleanup scripts/recipes against the composition contract, usable from the command line, agents and the workbench. Initial candidates are distributing a mixed Opinion/Session layer by declared ownership, relocating ordinary transforms, routing material bindings, promoting selected properties into scenarios, and retiring only superseded source opinions. Executable commands and script filenames remain to be defined during implementation.

Each recipe declares applicable CC rules, profile version, supported fields/contexts, preconditions, input scope, expected changes and evaluation coverage. Support preview and authorized application. Explicit, unambiguous mappings can be applied in bulk within that authorization; do not require confirmation for every field or silently expand the batch.

Pause at a **decision checkpoint** whenever ownership, destination, variant branch, destination collision or intended behavior cannot be established from the contract and declared inputs. This is a contract/precondition decision, not an LLM confidence percentage. Show affected source fields, candidate destinations and contexts, applicable rules, expected effects, and why a decision is needed. Allow choosing a destination, supplying a bounded mapping, deferring the affected group, or cancelling. Never treat silence as approval.

Group checkpoints by dependencies: one decision may cover equivalent edits, but unrelated unresolved edits must not inherit it. Record decision scope and provenance. Rebuild and evaluate the affected plan after the answer; the chosen destination must still satisfy structural requirements or be recorded as an explicit contract/profile exception. Keep unresolved groups unapplied. Declare whether independent groups may complete first, and report completed, pending and deferred groups separately.

Persist resumable plans with source revision checks so a pause or application restart does not lose decisions. Changed inputs invalidate the affected plan and require inspection again. Unattended runs return a structured needs-decision result instead of guessing or waiting indefinitely. Record recovery information for each completed group and make batch recovery boundaries visible before execution.

**Acceptance to define:** a mixed batch applies authorized unambiguous edits, pauses on an ambiguous owner or branch with a useful explanation, resumes after a scoped decision, rejects stale input, and leaves deferred/unrelated fields intact. Repeating a completed recipe yields no additional changes for unchanged inputs.

## Upstream integration priorities

These are planned integrations with our CC evaluation, not implemented capabilities. Pin upstream revisions and the target USD/Kit/runtime before adoption; a proposal's status does not establish support in our installed application.

| Priority / upstream reference | Application here | Definitions and evaluation needed |
|---|---|---|
| First: [USD Validation Framework](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/usd-validation-framework) | Use UsdValidation as the planned framework for CC validators, with stable rule IDs and authored-layer/composed-stage findings. | Map CC rules to custom validators and suites; retain owner, layer, prim/property, branch and evidence. Declare payload/variant/time coverage. Keep repair planning and confirmation separate from validation. Proposal marks implementation in 24.11; local availability is unverified. |
| First: [SimReady Foundation](https://github.com/NVIDIA/simready-foundation) | Evaluate incoming robot/prop packages against selected simulation profiles, then evaluate the assembled workcell. | Pin profile, features, libraries and runtime; preserve per-requirement results. Its validator stack and UsdValidation need an explicit adapter/result mapping, not an assumption that their plugins are interchangeable. Recheck scene overrides and combined behavior. No packages installed or samples certified. |
| First: [Profiles and Capabilities](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/profiles) | Express what imported content needs and what consumers support. | Distinguish upstream capability claims, SimReady requirement profiles and our ownership profiles. Scope claims to selected variants/loaded payloads; cached summaries need provenance. Define refusal versus allowed degradation. README marks implementation in 26.08; application support remains unverified. |
| First: [Namespace Editing](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/namespace_editing) | Safe rename/reparent operations for CW-04, alongside stable identifiers and bindings. | Use the supported UsdNamespaceEditor API, preflight and declare layers/dependent stages affected. Account separately for unloaded payloads, unselected variants and external binding systems. A path change must not create a new physical identity. Resolve permissions and retain recovery evidence. |
| Next: [Level of Detail](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/level-of-detail) | Scale workcell/facility viewing through asset-owned representations and public controls. | Declare domain, heuristic, fallback and consumer support. Visual simplification must not silently change collision/physics fidelity or remove required identifiers/ports. Evaluate nested LOD and unsupported-consumer behavior. README marks implementation in 26.08; renderer support needs separate evidence. |
| Next: [VFI deployment tradeoffs](https://docs.omniverse.nvidia.com/vfi/latest/guide/asset-structure-optimizations-and-tradeoffs.html) | Retain modular authoring packages and generate a target-specific deployment representation under CC-24. | Define publication layouts, source/output ownership and identity mappings, supported controls/load states, behavioral equivalence and allowed reductions. Measure cold/warm loading, memory and target throughput against declared budgets. No general deployment generator or factory-scale benchmark exists here. |
| Next: [Spline Animation](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/spline-animation) | Preserve editable authored curves in the rightful AnimLyr and variant branch. | Confirm supported attribute types and spline APIs in each consumer. Specify time units, interpolation/extrapolation, offsets and any intentional bake. Evaluate overlaps with defaults/time samples and solver/runtime writers. Curves do not make every animated value a TransLyr responsibility; baked simulation remains SIM. |
| Watch: [Physics Nested Bodies](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/physics_nested_bodies) | Preserve meaningful articulated robot hierarchy where supported. | Check schema, validator and solver agreement on nesting, mass, coordinate frames and kinematic/dynamic boundaries. Do not change imports based solely on proposed behavior. |

**Bounded future pilot:** follow the contract's [industrial acceptance pilot](CompositionContract.md#proposed-industrial-acceptance-pilot): one pinned robot with gripper/sensor/fixture, two independent occurrences, a reusable workcell repeated in a line, and a small DSX/AIF equipment case. Include identity from governing systems at intake, namespace/binding continuity, source-update impact and generated-deployment acceptance. Add LOD and spline fixtures only for consumers with demonstrated support. Record asset-level and assembly-level results separately, including skipped coverage and measured performance. The AOUSD/IEDT workcell discussions are a candidate source of requirements and review; no official adoption or approved guideline status is assumed.

### Delivery order and open decisions

Start with a shared source-identity/resolution model and the DT-01–03 inventory. CW-01 and CW-02 can then be developed as bounded launch/reload adapters. CW-05 can begin with read-only authored-text viewing; enable editing after buffer/apply/save, validation and synchronization semantics are established. Deliver CW-03 inspection before routing; enable its assignment actions and CW-04 only once DT-04–07 planning, recovery and evaluation exist. Pipeline and agent adapters use this same core.

Agree the first supported storage/resolver environment, application builds/editor presets, lightweight renderer candidate, ownership mappings, report/plan schemas, external-edit synchronization policy and fixture coverage. Measure launch time and resource use before choosing the asset-viewing preset. These roadmap items authorize no implementation, scene migration, application installation or source cleanup by themselves.
