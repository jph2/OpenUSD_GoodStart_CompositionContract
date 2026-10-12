---
name: openusd-composition-contract
description: Apply the OpenUSD GoodStart Composition Contract when designing, reviewing, authoring or repairing layered USD assets, nested assemblies, digital twins and robotics scenes. Use for layer ownership, variants, transforms, asset-structure cleanup, shared resources, delivery packaging, reusable interfaces, stable identity, composable bindings and target readiness. Generic Kit UI work does not require this skill.
metadata:
  version: "0.2.9"
  source: "https://github.com/jph2/OpenUSD_GoodStart_CompositionContract"
---

# OpenUSD composition contract

Apply this independent draft proposal to the user's declared project/profile. Its rules describe an ownership and authoring convention built on OpenUSD. NVIDIA alignment supplies supporting evidence; it does not establish upstream endorsement or universal conformance.

The skill version equals the main contract version. [Source metadata](references/source.json) records the source content hash and packaged file hashes. [CompositionContract.md](references/CompositionContract.md) is a generated reference containing the full contract and its evidence links. Read only the relevant sections using the map below. Existing teaching profiles and observations retain their own versions and coverage.

When the source repository is available, its main `CompositionContract.md` owns the rules. Compare its version and UTF-8/LF-normalized content hash with the source metadata before applying it; the source repository's sync helper provides a read-only `--check` operation. Honor an explicitly pinned project revision; disclose a mismatch instead of silently combining revisions. Update this skill in its source repository, following that repository's AGENTS.md. The generated reference and installed copy are derived artifacts.

## Repository platform focus

The source repository primarily targets NVIDIA Omniverse and Kit. Its profiles,
example USD files, definitions and snippets intentionally include RTX render
settings, viewport cameras, environments, Kit authoring metadata and APIs. Preserve
these where selected; document runtime dependencies and version-specific limits.
Distinguish OpenUSD mechanics, project conventions and Omniverse implementation
behavior. Do not strip host-specific settings for presumed portability or claim
cross-application acceptance. When applying the skill elsewhere, honor that user's
declared platform rather than imposing the repository's Omniverse profile.

## Locate the applicable rules

Search the bundled contract for the CC IDs or section headings in this map; read the associated rule text and exceptions before deciding or editing.

| Task | Contract sections and rules |
|---|---|
| Root, authoring target, layer separation | §§2–3, CC-01/02; §20, CC-23 |
| Asset interfaces, payload discovery, native or point instancing | §4, CC-03–05d |
| Placement, selection, scenarios and promotion | §§5–6, CC-06–09 including CC-08a |
| Materials and nested ownership | §7, CC-10; §§11–13, CC-13–16 |
| Presenter, persistence and acceptance | §§8–10, CC-11/12 |
| Opinion inspection and repair | §§14–16, CC-17–19 |
| Rig, animation, physics, data and runtime writers | §§17–20, CC-20–23 |
| NVIDIA/SimReady comparison and industrial acceptance | §21; CC-12/24/25 |
| Naming, portable packages, imported sources, deployment | §22, CC-24–26 and asset-interface checklist |
| Governing-system IDs and composable bindings | §23, CC-27/28 |

## Establish scope and ownership

Identify whether the task requests explanation, design, inspection, authoring or repair. Use the existing project profile where supplied; otherwise record the proposed purpose, source revisions, consumer/runtime, supported configurations and expected behavior. Applying this skill does not by itself authorize a scene migration or a shared-source edit.

For each relevant contribution, determine:

- **Owner:** library, source asset, reusable assembly, scene occurrence or installation, with an explicit authority such as PLM/BOM, project requirement or responsible team.
- **Meaning:** geometry, ordinary placement, material, configuration, rig, animation, physics, identity, connection or operational data.
- **Context:** unconditional or exact variant branch; default or time samples; active writer/mode; persistence and permitted downstream overrides.
- **Destination:** package, layer, prim/property and edit context, with a CC rule explaining the choice.

Prim depth, filename, colour and property spelling alone do not determine ownership. Report ambiguity at the affected decision and continue independent work within the authorized scope. Assemblies can own reusable decisions while their children retain intrinsic choices.

## Preserve the composition invariants

- **Opinion naming:** identifiers are optional and omitted by default. If requested, use the dot-separated `<base>.name.usda` form, for example `OpinLYR_SceneDefault.jph2.usda`; do not invent a name or use an underscore identifier suffix. The identifier marks contributor scope, not permissions. use `OpinLYR_Scene<SceneName>.usda` for a specific scene (Essentials: `OpinLYR_SceneDefault.usda`, `OpinLYR_SceneColorVariants.usda`). For intentional sharing omit `Scene` and use `OpinLYR_<Purpose>.usda`; document consumers and compatibility. When renaming, update incoming arcs and authoring/lock metadata. Filenames indicate intended ownership, not automatic sharing or compatibility.
- **Selection destinations (CC-08/11):** save ordinary scene variant selections in the existing Opinion layer. Accepted selections can remain there; promotion is not mandatory. Session is for transient previews with explicit persistence. Create `020_BASE_LYR/ConfigLyr.usda` or `ConfigLyr_<Purpose>.usda` only for independent reuse, ownership, versioning or switching. ConfigLyr selects existing choices; VariLyr defines variants/scenarios and their conditional contents. Declare strength and disclose Opinion overrides that mask a selected preset. Do not create an extra layer just to store a few choices.

- **Minimum necessary composition (CC-00):** self-contained leaves are normal, not exceptions. Inline geometry, intrinsic transforms, materials and variants in a leaf; edit its file directly. For scenes/composed assets create the conventional full scaffold, then retain only useful categories/role layers. Remove dependencies and stale authoring/lock metadata before deleting unused files. Teaching scenes may retain empty category folders for discovery. Nested assets do not imply identical nested stacks; preserve purposeful payload boundaries.

- **Preview environment (CC-00a):** every asset, including leaves, loads basic direct-open environment lighting outside its default asset prim. A portable shared preview layer is allowed; keep asset content inline. Reference/payload only the asset prim in consumers. Preview content must not change asset transforms, materials or variants. Verify visual lighting and reference isolation only when evaluation is requested; do not infer acceptance from authored files.
- **Asset grouping (CC-00b):** independent named assets may share a directory. Do not add one-folder-per-asset nesting without a purpose; use team ownership, dependencies, versioning/publication and navigation to choose boundaries. Update relative paths and saved lock/authoring metadata when relocating files.
- **Root and Opinion (CC-01):** use `050_OPINION_LYR` when an Opinion workflow is needed. Simple payload/interface wrappers may omit Opinion; do not recreate a redundant layer during cleanup or regeneration. composed-package roots assemble work layers and stage metadata. Use the declared Opinion layer for experiments; retain saved scene selections there; deliberately promote only contributions whose ownership or independent management requires a move, and retire superseded fields. Preserve the declared Kit root-writability and supplied-template exceptions only in profiles where they apply. Layer/UI locks do not provide field-level protection.
- **Geometry and transforms (CC-02/21), within composed packages:** scene GeoLyr defines hierarchy and references published packages. It contains no authored transform operations/order or variant definitions/selections. Ordinary transforms belong in the rightful owner's TransLyr; create/register it when needed. Native geometry may live in an owned asset GeoLyr.
- **Semantic exceptions (CC-21):** variant-dependent transforms stay in their variant branch; authored motion belongs to AnimLyr, skeleton rest/bind data to RigLyr, joint/mass frames to PhysicsLyr, published solver results to SimLyr, and live measurements to the declared runtime mechanism. Keep coherent transform operations and their order together.
- **Reusable controls (CC-03–05/09/14):** define intrinsic choices in the owning asset/assembly and select its public interface from the parent. Preserve imported internal structure. Loft required discovery information above payloads where used; keep it synchronized with implementation.
- **Placement and scenarios (CC-06–08a):** preserve the declared placement/adjustment/asset hierarchy and coordinate semantics. Keep manual selections and scenarios mutually exclusive for the same control. Scenario promotion preserves provenance while excluding only the superseded unconditional opinions. Clearing an authored selection differs from authoring an empty selection that blocks weaker values.
- **Materials (CC-10/15):** preserve asset finish controls, shared-library dependencies and variant-owned bindings. Resolve the actual material binding; a shader colour alone does not identify an engineering material or prove a binding result. Record library revision/adoption policy.
- **Instancing (CC-05a–d):** declare load states, instanceable sites and required editable descendants. References alone do not establish native instancing; configuration differences can create more prototypes. Respect instance-proxy editing limits. PointInstancer IDs and prototype indices have their declared topology/scope; they are not automatically physical IDs or variant selections.
- **Strength and writers (CC-22/23):** GeoLyr is the weakest work sublayer in the adopted authoring profile; explicitly declare the rest of the stack and any overlapping fields. Role names do not change USD strength. Define active writers and handoff between authored playback, simulation and live modes, including external runtime writers.

## Establish digital-twin identity at intake

Apply CC-27 when an entity first enters the pipeline or is first authored, before dependent publication or binding activation. Preserve existing ERP, PLM, CAD/BIM, equipment-registry or equivalent IDs verbatim with authority, kind, uniqueness scope and provenance. Keep revision/configuration context explicit.

Distinguish shared part/type identity, assembly/scene occurrence identity and the identity of an actual physical object. Allocate occurrence identity at creation; assign a physical identity when the real object is known. Repeating an assembly requires scoped child IDs qualified by stable parent identity or an installation mapping. Renaming or reparenting the same entity preserves its identity; duplication and replacement follow separate policies.

If authoritative identity is absent, a designated owner may allocate a durable local key with explicit status and a reconciliation policy. Preserve its mapping when an external identifier arrives. Never replace an available governing ID with an untracked importer UUID or infer equivalence from similar strings.

Under CC-28, bindings resolve these identities to the current stage/profile revision and the rightful property/layer/variant context. Record units, conversions, time, permitted writers and lifecycle. Reject ambiguous targets or unintended collisions; declare fan-out when one type maps to several occurrences. Invalidate/re-resolve mappings after relevant changes. BindingSpec, BindingPlan, BindingChangeSet and provenance receipts are project design requirements; USD composition alone does not execute an integration engine.

## Inspect and change through evidence

For inspection, use available USD/Sdf-aware tooling to examine authored specs and composed results: source layer/spec, owner, fields, variant context, strength, transform order, bindings, relationships, samples and dependencies. Include inactive branches and unloaded content in the coverage statement; unavailable data remains unassessed. Read-only inspection is not permission to repair.

For an authorized repair, follow CC-18/19: capture revisions and relevant unsaved state, make a field-level plan, preserve conditional context and relative-path meaning, and consider destination authoring together with removal/exclusion of the source opinions. Keep unrelated fields and recoverable source evidence. Use revision/conflict checks and rollback information. Distinguish a behavior-preserving move from an intentional correction. Run tests or runtime evaluation only when requested; missing required acceptance remains pending and cannot become a conformance claim.

For new packages, follow the selected maintained-authoring conventions: `SceneROOT_<Purpose>.usda`, `AssetROOT_<Name>.usda`, numbered class folders for composed packages as needed, singular `_LYR`, and explicitly composed role layers. Refer to §22 for exact names. Unused categories do not require empty layers. Preserve third-party packaging behind its declared interface; target deployment outputs may use a different explicitly declared layout under CC-24/25/26.

## Clean up asset structures and resource ownership

Apply CC-00–00d and CC-18/19 when the user requests simplification, regrouping, deduplication or packaging. This is a workflow for using available USD-aware tools, not a claim that a general cleanup executable exists.

For explicitly self-contained leaf deliverables, include all required asset and preview content inside the file/package. For dependency-free procedural delivery, use inline materials and texture-free preview lighting when no specific preview has been selected; do not introduce shared MatLib/Envs dependencies. For the Essentials minimal Omniverse profile, preserve the supplied `geoANDenvEXAMPLE.usda` Environment/Render/viewport-camera baseline inline outside `/Asset`, with the four leaf files directly in `010_ASS_USD`. Its declared Kit HDR/grid and OmniPBR dependencies are permitted for that runtime profile; do not replace its appearance with a generic preview or call it dependency-free. See the contract’s “Minimal Omniverse setup” section. Shared-resource authoring remains an option only for a declared dependent asset/library workflow, not a claim of an independently self-contained leaf.

### Resource roles for clean leaves

These are ownership roles, not mandatory files, layers or extra folders. Follow the team's existing names; create a shared directory only when it has content.

| Role | Responsibility | Typical location |
|---|---|---|
| Leaf asset | Geometry, intrinsic transforms, public variants and asset-owned bindings | Adjacent `AssetROOT_<Name>.usda` files |
| Shared material library | Reusable material/shader definitions with explicit revision ownership | `MatLib/` or the team's material library folder |
| Shared texture resources | Common image files, preserving texture interpretation and usage metadata | `tex/` or `textures/` |
| Private resources | Dependencies whose ownership or release lifecycle is specific to one asset | An asset-specific folder only when useful |
| Preview environment | Shared direct-open lighting outside each default asset prim | `Envs/` |
| Delivery package | Optional contained distribution with all required dependencies accounted for | Explicitly selected delivery location |

For new leaves, first look for suitable existing material/texture resources in the authorized library scope. Reuse compatible governed resources, introduce private resources when justified, and keep bindings/variants owned by the leaf. A shared material library owns shader definitions; the asset still owns its material choices. Sharing image bytes does not require sharing material parameters. Never merge material identities just because their current colors or texture files match.

For maintenance, use the following workflow to simplify existing layouts. It applies to cleanup requests and to the bounded files created during an authorized authoring task; it does not authorize unsolicited library-wide reorganizations.

1. **Discover:** identify exact packages, owners, public entrypoints and consumers; inventory sublayers, references, payloads, variant branches, textures, material networks, preview environments and resolver/runtime dependencies. Include unloaded/inactive content; record inaccessible consumers and unsaved edits.
2. **Classify:** choose self-contained leaf versus composed asset, shared library versus private resources, editable source versus delivery artifact. Assets may sit side by side; `MatLib`, `tex`/`textures` and equivalent team conventions are valid shared folders. A leaf may reference shared resources without needing a Geo/Trans/Mat/Variant stack.
3. **Plan:** enumerate old/new paths and exact removals, incoming arcs, shader asset paths and authoring/lock/profile metadata affected. Deduplicate only after comparing content plus semantics (color space, shader settings, intended usage, owner and revision policy). A hash match alone does not prove two independently governed resources should be coupled. Preserve stable interfaces or explicitly migrate consumers.
4. **Execute within authorization:** preserve recoverable originals and current edits, use USD/Sdf-aware operations, re-anchor relative dependencies from each authoring layer, and preserve variant contexts and bindings. Remove only proven-unused files in the bounded scope; inactive variants and unloaded payloads are not evidence of disuse. Do not recreate empty leaf folder stacks.
5. **Package only when requested:** use USDZ as an optional signal of a self-contained delivery artifact only after confirming required file dependencies are contained across supported configurations and compatible with the declared consumer. The extension alone proves nothing; a single-file package may contain multiple layers/resources. Retain editable sources separately. Ordinary ZIP is transport with unpacking; USDZ is a distinct uncompressed/aligned runtime package. Use USD-aware packaging, preserve editable sources and variants, and account for private/shared textures and preview dependencies. Check supported file types and shaders in the target consumer; do not assume HDR/OmniPBR is portable. Do not relabel ZIP as USDZ or claim a package is self-contained while omitting dependencies. Sharing resources across assets and independently self-contained archives are different delivery choices.
6. **Report:** give the changed interfaces/dependencies, backup/rollback location, unresolved consumers and actual inspection coverage. Run tests or performance benchmarks only when requested. Separate packaging success, composition evidence and visual/runtime acceptance; never infer speed from the extension.

### Skill decisions and deterministic scripts

Use the skill to choose scope, owners, grouping and the intended dependency graph; use bounded USD-aware scripts for repeatable inventory, path rewriting, resource comparisons and migration. Separate discovery/planning from mutation. A reusable helper should accept explicit entrypoints and an allowed root, produce a dry-run old-to-new path map and dependency report, and apply only the planned changes with revision checks and recoverable originals. Its stopping condition is the requested layout with accounted-for dependencies and no unexplained changes, not the smallest possible file count. Report unresolved edges; never compensate by deleting more content or flattening away authored choices.

The current skill supplies this procedure; a general-purpose cleanup tool is not implemented. Its implementation is tracked in the source repository’s `ROADMAP.md`, item **CW-04a — Clean leaf assets and shared resources**. The intended user interaction is a natural-language request or future workbench action; terminal use is not required. Do not imply automatic background maintenance, a scheduled service or runtime verification. When building a helper is requested, implement only the bounded operation needed and document its actual supported scope.

## Evaluate the declared use

Use CC-12 and the asset-interface checklist for purpose, coordinates, public controls, identity, dependencies, load/instancing behavior, writer policy, publication and evidence. Pin applicable external profiles/features/requirements together with validators and runtimes before making readiness claims. Recheck affected requirements after overrides or dependency changes.

For robotics, include attachment frames, articulation, joints, collision, units/mass/inertia, backend isolation, sensors and writer-mode transitions. Industrial properties and ports require actual domain schemas and consumer behavior. Assess individual assets and their assembled use separately.

Nesting is normal. Treat performance as measured layer/dependency/loading/instancing/configuration behavior. A generated deployment package needs source/output identity and interface mappings, supported states, declared reductions, behavioral acceptance and measured budgets. Preserve the maintained authoring source.

Report the contract/profile revision, applicable CC IDs, evidence locations, actual coverage, findings and unresolved ownership. Use pass, fail, permitted not-applicable with reason, or not evaluated. Keep static observations, runtime acceptance and performance results distinct. This skill provides guidance and the contract reference; it supplies no general USD validator, repair engine, binding engine or deployment generator.
