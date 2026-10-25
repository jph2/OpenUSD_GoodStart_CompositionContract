# Roadmap

**0.1 bootstrap — complete:** move the contract, establish agent entry/governance/workflow, record deterministic tooling requirements and define the optional pipeline-to-composition boundary. Variant scenes remain in TutorialBuilder.

## 1. Collaborative proposal review

Review DISCUSSION.md with intended collaborators when Jan chooses to share. Agree scope, vocabulary, ownership model and minimal profiles. Record objections and changes by CC ID. Decide repository hosting/access and licensing before distribution. No invitations or publication have occurred.

## 2. Minimal reference package

**Authored; acceptance pending.** Jan requested a new example and project layout using VariantSetups, the scene-layer schematic and `USD_GoodStart/_Generated_Test`. `examples/01_LayeredScene` now contains cube/cone packages, two cube occurrences, a reusable assembly, shared materials, placement, manual/scenario choices and separate property/selection conflicts. PROJECT_STRUCTURE.md records the revised storage model; CC-24/25 cover storage lifecycle and imported-source boundaries.

The USD-aware author records a default-entrypoint read-back; full variant, relocation, renderer and UI save/reopen acceptance remain open. Agree that acceptance scope before promoting the example to best-practice status. Historical TutorialBuilder examples stay in place.

## 3. Deterministic read-only core

Implement DT-01 through DT-03 and reporting portions of DT-09. Agree machine-readable profile and finding schemas. First useful outcome: explain an authored opinion, owner, variant context and conflict without modifying the stage.

## 4. Repair planning and evidence

Implement dry-run plans, candidate comparisons, concurrency checks, rollback and audit. Add execution only after its authorization and recovery model is explicit. Exercise the declared fixture matrix under a specifically authorized implementation/verification task.

## 5. Pipeline-generated USD startpoints and downstream composition

**Boundary defined in contract 0.2.15; implementation compatibility and acceptance remain open.** The composition contract is the policy/evaluation owner. A source pipeline is a replaceable producer of versioned USD startpoints, asset packages, manifests and provenance. Omniverse/Kit or another declared consumer composes those outputs and authors its own purpose-specific USD layers. The producer graph, composition rules and consumer runtime remain distinct but exchange persisted, inspectable USD and versioned handoff evidence under [CC-29](CompositionContract.md#24-pipeline-generated-startpoints-and-target-authoring).

The optional `OpenUSD_GoodStart_Pipeline_nodes` project is a candidate producer, not a contract dependency. Its own graph implementation and delivery lifecycle remain owned there. The bounded source review found a Composition Pipeline vision and a BRep research/roadmap item; it did not inspect or execute the full node implementation or validate cross-repository compatibility. Required next steps are:

1. Define/version the source-to-startpoint manifest: source IDs/revisions, identity authority, transformation/runtime versions, target profile, units/up-axis, output paths/hashes, dependency closure, layer/prim mappings and report locations.
2. Map each output by semantic owner. Compose peer pipeline contributions as explicitly ordered layers where appropriate; reference/payload reusable asset packages through their public asset sites rather than turning every asset into a sublayer.
3. Prove source immutability, repeatable output identity, regenerated-startpoint diffing, preserved Omniverse-layer edits, conflict reporting, and saved-stage read-back on a bounded fixture.
4. Add a target adapter for Omniverse and separately named renderer/consumer profiles only after support and acceptance are demonstrated. Keep the USD output usable and inspectable without ComfyUI.

**BRep is a pipeline capability, not a layer role.** The sibling pipeline research proposes a focused USD BRep Tessellate node first, with Primitive and Boolean nodes gated on pilot evidence. NVIDIA USD BRep uses an `omniSolid` schema plugin; treat native solid/NURBS data as a declared plugin-dependent representation and mesh output as a distinct derived target. Do not imply universal OpenUSD or renderer support. Pipeline WP-E108 remains deferred in its owning repository; this roadmap does not authorize implementation there.

## 6. Workcell and integration profiles

Identity and composable-binding work follows CC-27/28: preserve governing ERP/PLM or equivalent IDs at first intake/authoring, define scoped source/occurrence/physical-instance records and namespace-change behavior, and compare identifier storage candidates from proposal #105 without assuming standardization. Establish identity before dependent assembly publication or binding activation, including repeated-import reconciliation and a declared policy for provisional local IDs. Then specify BindingSpec/Plan/ChangeSet/receipt interfaces and deterministic resolution to layer/variant destinations. Pilot repeated assets and nested assemblies, ambiguous-ID checkpoints, one bounded external mapping, and recovery. DATA holds stable identity/context, SIM holds results and RUNTIME holds declared operational output. No integration engine or cross-system write-back is authorized by this roadmap.

Extend through rig/animation/physics boundaries, material ownership, PLM/UNS mappings, simulation/live authority and snapshots. Use workcell evidence to refine the proposal. Consider optional Omniverse interface and MCP adapters around the proven core.

## 7. Integration or transfer

Evaluate incorporation into GoodStart or a relevant collaborative effort on its merits. Repository ownership, standardization, licensing and stewardship require explicit decisions; no outcome is presumed.

## 8. Source editing and composition workbench

**Requested 2026-10-10; planned, not implemented.** These five features connect interactive authoring with the deterministic inspection and repair core. They elaborate CC-11/16–19/21/23–25 and DT-01–09. The UI and agents must use the same inventory, ownership decisions and move plans. The current temporary-file edit behavior is Jan's observation; its exact installed-application path still needs inspection.

| Feature | Proposed user action | Outcome |
|---|---|---|
| CW-01 — Open Original Layer Source | Layer context menu → Open Original USDA | Edit the actual resolved text source with an explicit save/reload workflow. |
| CW-02 — Open Referenced Asset With | Layer or stage-reference context menu → Open Asset With → application | Work on the asset in a separate application, preferably a lightweight custom Omniverse instance. |
| CW-03 — Opinion Inspector, Routing and Contract-Guided Migration | Inspect → classify → preview destinations and changes → apply selected plan | Understand each opinion and safely route or repair it through one staged workflow backed by the shared USD-aware core. |
| CW-05 — Embedded USDA Scene Editor | Layer context menu → Open in Scene Editor | Inspect and edit ASCII scene content in a dockable Omniverse panel. |
| CW-06 — Publish Selected Prim as an Asset | Prim context menu → Composition Contract → Publish Prim… | Create a reusable composition-preserving asset, explicit flattened snapshot, or validated USDZ delivery package, then optionally recompose it. |

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

Offer a source-aware application picker from the layer view and from a composed prim's context menu. Support configured Omniverse builds, usdview and DCC applications such as 3ds Max, Maya and Houdini; Blender and ShapeFX Loki are optional adapters only when installed and their USD support is verified. The preferred preset may be a separate instance of our own Omniverse build with a lighter renderer, subject to compatibility and efficiency assessment. The menu must identify whether it will open a source layer, asset entrypoint, selected referenced prim, package member or a composed-occurrence preview. Renderer/application availability is profile-dependent; do not imply a plugin or format capability that has not been verified.

Define before implementation:

- Resolve the selected composition arc to its source package, entry layer and referenced prim. A prim can have multiple contributing references; present candidates with authoring layer, owner and arc type instead of choosing an arbitrary source. A layer-stack sublayer row opens that source layer; a referenced/payload occurrence opens its selected source arc. Distinguish source editing from a composed-occurrence preview and from opening the asset package's intended entrypoint.
- An application registry with executable/build version, launch arguments, supported formats, USD feature coverage, resolver context, required plugins/extensions, renderer preset and process-reuse policy. Launch a separate process when requested; do not replace the current scene. Preserve resolver context and package-member identity where the adapter supports them.
- Two explicit contexts: source-asset authoring and occurrence preview. A standalone source may omit the scene's selections, overrides, placement, lights and materials. Any transferred preview context must remain identifiable and must not silently become source defaults.
- Shared-source editing versus creating an occurrence-specific derivative. Show known consumers and the selected revision; do not imply that editing the source affects only the clicked occurrence. Unknown consumers remain an explicit limitation.
- Return/reload coordination with CW-01: detect saved changes, report the source revision, and reconcile the parent application's dirty state. Closing the child process alone does not prove that changes were saved. Do not assume every DCC can round-trip arbitrary USD schemas, composition arcs or Omniverse-specific materials.
- A lightweight viewing profile for camera framing, units, up axis, dependencies and lighting. Evaluate shader/schema support and visual differences under the alternative renderer; a different preview appearance must not trigger material conversion automatically.

**Side effects:** additional instances consume memory and other resources even with a lighter renderer. Missing plugins, resolver setup or materials can make a valid asset appear incomplete. Released or shared packages may require a new revision and deliberate consumer adoption rather than an in-place overwrite.

**Acceptance to define:** select a nested referenced asset or layer-stack sublayer, choose an available application, open the correct source/layer/prim in a separate process, save a bounded change, and deliberately refresh the parent. Include multiple arcs, package members, missing dependencies, dirty parent state, one app without full schema support, and a renderer compatibility comparison. App-specific acceptance must name tested builds and plugins.

### CW-03 — Opinion Inspector, Routing and Contract-Guided Migration

**Status: requirements being defined; planned and not implemented.** This combines the previously separate Opinion Inspector/Routing and Bulk Migration features into one user capability. It is delivered in gated stages: read-only inspection first, previewable plans second, and explicitly authorized application after recovery and behavior checks are established. The Omniverse extension is the interactive front end; it and any CLI/IDE adapter call the same deterministic USD-aware core (DT-01–09).

**1. Show authored opinions clearly.** Inspect Session, Opinion/Review and selected persistent layers. Keep authored layer/spec data distinct from the composed result. Each finding identifies the source layer and authored path, composed path when resolvable, field/property and value or sample summary, category, variant branch, owner/evidence, current contribution or masking state, applicable CC rule, proposed destination and uncertainty. Label transforms and their operations (translate, rotate, scale), material bindings, shader inputs, animation, references, metadata and variant selections. Icons or colours may reinforce the labels; text and accessible non-colour distinctions remain. A property name or value type indicates data kind, not necessarily rightful ownership. Without a recorded before-state, report an authored-opinion inventory, not an edit history.

**2. Suggest and preview routing.** Derive destination suggestions from explicit ownership/profile mappings and variant context, not from filenames, property spelling or category alone. Ordinary occurrence placement may route to the rightful TransLyr; a scene-owned material assignment may route to MatLyr; variant-dependent values remain in their exact owner/set/branch; scene-level selections may intentionally remain in Opinion. Show the proposed fields, destination/context, any layer creation, source disposition, collisions, variant/load/sample coverage and expected composed effect before application. Treat related transform ops/order/pivots/samples and material relationships/connections as coherent units. Resolve material bindings through their actual targets and purpose. Unknown ownership, incomplete context, unsupported fields or unresolved conflicts produce a scoped decision request, not a guessed destination.

**3. Apply only a reviewed plan.** Build candidate layer edits and source removal/exclusion together; copying an opinion while leaving a masking source active is not a completed move. Pin source revisions and contract/profile revision, recheck them before apply, preserve unrelated fields and relative paths, compare the candidate's composed behavior across declared variants and time samples, and provide cancellation, rollback/recovery and an audit record. Report deliberate behavior changes separately from behavior-preserving relocation. Inspection stays read-only until the user selects and authorizes a plan. A Kit UI and standalone IDE/CLI entry point use the same core and plan format.

**4. Keep Opinion a safe, intentional authoring target.** On stage open, show the active edit target and confirm the profile's Opinion layer is selected and empty when expected; make a wrong or unavailable target obvious before the user edits. Opinion remains a valid home for deliberate scene selections and experiments. Do not automatically clear it after inspection or routing; retire only the specific superseded contribution authorized by the plan. Kit layer-lock state is a UI guardrail, not a filesystem ACL, so show lock/write status and detect external revision changes rather than promising that other tools cannot write.

**GeoLyr cleanup action.** Provide a separate, opt-in audit/action such as **“Remove accidental neutral transform opinions from GeoLyr reference sites.”** Preview the exact specs first. It may remove Kit-authored identity transform ops/order, reset-stack opinions or accidental invisible visibility only when the profile confirms they are unintended. Keep the required transformable Xform reference-site type. Never delete non-neutral placement or intentional intrinsic transforms with this checkbox; route a non-neutral value through the normal ownership plan or leave it unresolved. Variant-controlled values must stay in their branch. The checkbox is not a blanket “remove transforms” operation.

**Side effects:** full composition, inactive-variant and time-sample inspection can be expensive. Define scope limits, pagination, cancellation and stale-report detection; filtering must not hide related opinions required by a move. A layer or prim can have several contributors, and a proposed move can change strength even when the authored numeric value is unchanged.

**Acceptance to define:** a mixed Opinion/Session fixture with cube/cone transforms, bindings, animation and variant selections yields distinguishable, attributable records. Moving only Cone → Blue leaves Cube → Blue intact; relocating ordinary cone placement preserves cube placement and all declared variants; animation and variant-dependent transforms do not leak into unconditional TransLyr. The neutral GeoLyr cleanup removes only listed accidental opinions and leaves Xform type, deliberate transforms and composed behavior intact. Ambiguous destinations remain unresolved; stale inputs, apply failure and cancellation preserve recoverable sources. Verify stage reopen and candidate-vs-source behavior. No claim of implementation or acceptance until these checks are run.

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

### CW-06 — Publish Selected Prim as an Asset

**Status: requirements being defined; planned, not implemented.** Add a dedicated **Composition Contract** section to the prim context menu, with a guided **Publish Prim…** workflow. It turns an authored/composed result into an owned, reviewable asset or delivery output without silently replacing source content. Reuse the shared DT-01–09 inventory, source-resolution, dependency, identity and revision model.

The wizard separates two independent choices: (1) how to represent composition and authored alternatives, and (2) the file/package encoding. Provide these explicit output intents:

- **Composition-preserving asset:** author an owned entrypoint for the selected prim/subtree while preserving the required references, payloads, sublayers, variants and dependency relationships. Report what is retained, transformed or unsupported; do not call it preserving if the dependency graph or authored alternatives are lost.
- **Flattened snapshot:** make a deliberate snapshot of the selected composed result. Show the chosen variant selections, payload/load state, time range, session/edit-target contributions and other included sources. Flattening can remove composition arcs and edit boundaries, so label the output as a snapshot and retain source provenance; do not imply that it remains an editable modular package.
- **USDZ package:** optionally package a selected entrypoint and its supported dependency closure after localization and package validation. USDZ is a constrained, uncompressed USD package, not a generic ZIP filename. Ordinary ZIP may be offered only as transport with an explicit unpack-before-use expectation. A `.usd`, `.usda` or `.usdc` encoding choice does not itself mean flattened or packaged.

Recomposition is a separate, optional final step. For an asset entrypoint prim, offer **Add as Reference** or **Add as Payload** with target prim, destination layer, namespace, load state and identifier/dependency plan visible. A **sublayer** combines a whole layer stack, not a selected prim into a chosen namespace; therefore it is not a peer insertion choice for this prim-level action. If the user chooses a full-layer contribution workflow, route to a separate operation that inserts an explicitly authored layer into the declared LayerStack. Reference, payload and sublayer semantics must remain distinct.

The guided workflow must:

- Inventory the exact selected prim and contributing authored specs, references/payloads/sublayers, variant selections/branches, dependencies, materials/relationships, samples/time range, units/upAxis and load rules. Report incomplete or ambiguous source coverage instead of guessing. For sub-root references, warn about ancestor opinions/arcs that may not come along as expected.
- Capture identity at publication. Preserve governing ERP/PLM or equivalent identifiers and their authority/scope; allocate provisional IDs only under the project's declared policy. Keep asset/type identity, occurrence identity and physical-instance identity distinct, and preserve composable bindings or report exactly what must be remapped.
- Select a versioned **target-paradigm profile** (registry below). The profile declares output recipe, interface requirements, composition choices, package rules, resolver/runtime, validator and acceptance evidence. A profile is a target-specific interpretation, not a universal schema; report readiness only against its pinned requirements and evidence.
- Offer **Publish only** by default. Optionally **Publish and add to current scene** after candidate output is reopened and compared with the declared result. Never overwrite the source or replace the selected occurrence without a reviewed plan, explicit authorization, revision check and recoverable rollback.
- Produce an auditable report with source revision, selected prim/path, identity, profile/version, output files/hashes, dependency closure, retained/lost capabilities, validator results, unresolved decisions and any behavior change. Keep the editable authoring source and published/deployment artifact separately identifiable.

#### Target-paradigm profile registry

The registry is an extensible selector for publish recipes, not a claim that the approaches share one structure or are mutually equivalent. Each entry needs a stable ID, exact name, source URL/revision/date, maturity and intended domain, supported output operations, required metadata/interfaces, resolver/runtime and validators, test evidence, known exclusions, and a status such as **available**, **candidate** or **not evaluated**. Do not expose an enabled publish action until its recipe and acceptance boundary are defined.

Seed the registry with these evidenced labels:

| Profile entry | Initial status and scope |
|---|---|
| **Kitchen Set — film/animation scene and reusable asset packages** | Published production scene/package example; not a universal normative standard. |
| **USD WG `intent-vfx` — supplementary VFX workflow guide** | Supplementary VFX workflow example in the linked research, not one of its four primary approaches or a normative specification. |
| **NVIDIA DSX — AI-factory digital twin and SimReady delivery pipeline** | Pin the applicable product/document revision and validator before claiming readiness. |
| **NVIDIA Isaac Sim Asset Structure 3.0 — configurable robot asset** | Versioned robotics asset target; pin Isaac Sim build and acceptance requirements. |
| **OpenUSD GoodStart Composition Contract project/sample set 0.2.0 — nested scene and assembly authoring** | Exact comparison-paper label. It describes that paper's comparison snapshot; the current maintained contract profile is version 0.2.15. |

Use the comparison-paper labels verbatim in menus, reports and registry entries; do not invent shortened or rebranded names. The linked Section 21 paper identifies these four primary approaches and separately labels USD WG `intent-vfx` as supplementary. It is WIP research, not an external standard. Intent Gaming was mentioned as a possible future paradigm but is outside the paper's comparison; keep it in a separate future-candidates list until a source, version, requirements and acceptance evidence are defined.

**Side effects:** publishing can change namespace, omit inactive/unloaded content or sever external links; flattening changes editability and configuration behavior; packaging can fail to contain unsupported dependencies; recomposition can alter load performance and composition strength. Present these as explicit decisions in the plan.

**Acceptance to define:** publish a selected nested asset into the GoodStart profile in composition-preserving and flattened forms; inspect exact source coverage and preserved IDs/bindings; validate a dependency-complete USDZ separately from ordinary ZIP; reopen outputs and compare declared composed behavior; recompose one output as a reference and one as a payload; verify that sublayer is not offered as per-prim insertion. Cover unloaded payloads, inactive variants, external resolver dependencies, sub-root ancestor opinions, stale source revisions, cancellation and rollback. Add target-specific acceptance fixtures before enabling DSX, Isaac, VFX or Gaming profiles. No extension, publisher, paradigm registry or runtime validation is implemented.

### CW-04a — Clean leaf assets and shared resources

**Status: planned; not implemented as a reusable cleanup tool.** The composition skill already defines the workflow under “Clean up asset structures and resource ownership”; this roadmap item tracks building the reusable execution support (CC-00–00d, CC-18/19; DT-01–09).

**User outcome:** ask an agent to “clean up this asset folder using our conventions,” or use a future workbench action. Users should not need to type terminal commands. Agent, script and eventual UI entrypoints use the same bounded implementation.

**First delivery:** inspect selected local asset entrypoints and produce a readable proposed layout and dependency/move report without changing files. Then support recoverable application of that plan: place independent leaves together where appropriate, reuse compatible shared MatLib and texture resources, retain private resources when justified, remove redundant folder nesting, and update references, resource paths and authoring/lock metadata. Preserve direct-open preview environments outside default asset prims. Do not remove the deliberately retained teaching scaffold without a cleanup request.

**Acceptance:** cover variants, unloaded payloads and preview dependencies; preserve asset interfaces, bindings and resource interpretation; report unknown consumers; reject stale/conflicting plans; keep rollback data; repeated application must not introduce further changes. Require visual/runtime evaluation only as explicitly selected acceptance work, and report missing coverage. Do not merge resources based on filenames or visual similarity alone.

**Later optional delivery:** dependency-complete USDZ export for a declared supported consumer, preserving editable sources and authored alternatives. Ordinary ZIP remains an unpack-before-use transport option. Packaging and performance evaluation are separate from the first cleanup delivery.

### Reusable cleanup scripts and decision checkpoints

Bulk execution is a primary delivery surface for the integrated CW-03 workflow. Build a versioned catalogue of bounded USD-aware cleanup scripts/recipes against the composition contract, usable from the command line, agents and the workbench. Initial candidates are distributing a mixed Opinion/Session layer by declared ownership, relocating ordinary transforms, routing material bindings, promoting selected properties into scenarios, and retiring only superseded source opinions. Executable commands and script filenames remain to be defined during implementation.

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
| First: [Namespace Editing](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/namespace_editing) | Safe rename/reparent operations through CW-03, alongside stable identifiers and bindings. | Use the supported UsdNamespaceEditor API, preflight and declare layers/dependent stages affected. Account separately for unloaded payloads, unselected variants and external binding systems. A path change must not create a new physical identity. Resolve permissions and retain recovery evidence. |
| Next: [Level of Detail](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/level-of-detail) | Scale workcell/facility viewing through asset-owned representations and public controls. | Declare domain, heuristic, fallback and consumer support. Visual simplification must not silently change collision/physics fidelity or remove required identifiers/ports. Evaluate nested LOD and unsupported-consumer behavior. README marks implementation in 26.08; renderer support needs separate evidence. |
| Next: [VFI deployment tradeoffs](https://docs.omniverse.nvidia.com/vfi/latest/guide/asset-structure-optimizations-and-tradeoffs.html) | Retain modular authoring packages and generate a target-specific deployment representation under CC-24. | Define publication layouts, source/output ownership and identity mappings, supported controls/load states, behavioral equivalence and allowed reductions. Measure cold/warm loading, memory and target throughput against declared budgets. No general deployment generator or factory-scale benchmark exists here. |
| Next: [Spline Animation](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/spline-animation) | Preserve editable authored curves in the rightful AnimLyr and variant branch. | Confirm supported attribute types and spline APIs in each consumer. Specify time units, interpolation/extrapolation, offsets and any intentional bake. Evaluate overlaps with defaults/time samples and solver/runtime writers. Curves do not make every animated value a TransLyr responsibility; baked simulation remains SIM. |
| Watch: [Physics Nested Bodies](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals/physics_nested_bodies) | Preserve meaningful articulated robot hierarchy where supported. | Check schema, validator and solver agreement on nesting, mass, coordinate frames and kinematic/dynamic boundaries. Do not change imports based solely on proposed behavior. |

**Bounded future pilot:** follow the contract's [industrial acceptance pilot](CompositionContract.md#proposed-industrial-acceptance-pilot): one pinned robot with gripper/sensor/fixture, two independent occurrences, a reusable workcell repeated in a line, and a small DSX/AIF equipment case. Include identity from governing systems at intake, namespace/binding continuity, source-update impact and generated-deployment acceptance. Add LOD and spline fixtures only for consumers with demonstrated support. Record asset-level and assembly-level results separately, including skipped coverage and measured performance. The AOUSD/IEDT workcell discussions are a candidate source of requirements and review; no official adoption or approved guideline status is assumed.

### Delivery order and open decisions

Start with a shared source-identity/resolution model and the DT-01–03 inventory. CW-01 and CW-02 can then be developed as bounded launch/reload adapters. CW-05 can begin with read-only authored-text viewing; enable editing after buffer/apply/save, validation and synchronization semantics are established. Deliver CW-03 read-only inspection first; enable previewable routing and application only when DT-04–07 planning, recovery and evaluation exist. Build CW-06 after source/dependency inventory and identity handling, then enable each publish profile only when its recipe, validator and acceptance evidence are pinned. Pipeline and agent adapters use this same core.

Agree the first supported storage/resolver environment, application builds/editor presets, lightweight renderer candidate, ownership mappings, report/plan schemas, external-edit synchronization policy and fixture coverage. Measure launch time and resource use before choosing the asset-viewing preset. These roadmap items authorize no implementation, scene migration, application installation or source cleanup by themselves.
