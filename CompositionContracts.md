# Scene composition contracts

**Status:** version 0.1, independent work-in-progress proposal, 2026-10-10. This is the author's working baseline for collaborative review, not an AOUSD standard or group-approved specification. Automated enforcement and a conforming reference sample are not yet implemented. Moved from TutorialBuilder on 2026-10-10; this project now owns the contract. It supersedes conflicting conventions in the earlier VariantSetups exploration; those A–H folders remain experimental evidence in TutorialBuilder. See [provenance and source routes](harness/SOURCES.md).

## 1. Purpose and scope

Our approach is **layered USD scene assembly with published asset interfaces**. A scene root assembles layers with explicit responsibilities. Geometry enters through references to reusable assets. Asset-specific alternatives remain defined within those assets; the scene stores selections and scene-specific adjustments.

These are project authoring conventions built on OpenUSD, not additional USD composition rules or a universal Pixar/NVIDIA standard. Requirements below define the intended harness; documentation alone does not enforce them.

## 2. Why local opinions do not prevent this design

Distinguish three different authored contributions:

| Contribution | Example | Intended result |
|---|---|---|
| Variant selection metadata | Scene chooses `Finish = "Red"` on an asset instance | Overrides the asset's default selection and activates its Red branch. |
| Attribute or relationship opinion | Scene authors a colour or binding on a prim controlled by Finish | May mask the selected branch; prohibited unless it is an explicit override. |
| Transform on a separate scene parent | Scene places an instance at `(100, 200, 0)` | Contributes through transform hierarchy without competing with asset-internal properties. |

“Local wins” concerns competing opinions for particular data. It does not mean a local variant selection suppresses all content of that variant. Selection chooses a branch; the branch's properties then participate in composition. [OpenUSD variant selection API](https://openusd.org/release/api/class_usd_variant_set.html)

For example, VariLyr can contain this selection without copying the asset's variant implementation:

```usda
#usda 1.0
over "World"
{
    over "Cube01"
    {
        over "Adjustment"
        {
            over "Asset" (
                variants = { string Finish = "Red" }
            )
            {
            }
        }
    }
}
```

If another scene opinion directly forces the controlled material or colour, the selection can still read Red while the visible result differs. The harness must inspect both selection and resolved effect. The same issue can arise inside an asset if its own unconditional opinions mask its variants. [Authoring Variants](https://openusd.org/release/tut_authoring_variants.html)

## 3. File ownership contract

**CC-01 — Root assembly.** The root establishes stage metadata and includes scene sublayers. Keep routine instance edits out of the root and session layer. Environment and camera content remaining in earlier teaching samples is a historical simplification; new conforming packages use the roles in section 17.

| Owner | Allowed responsibility | Excluded from normal authoring |
|---|---|---|
| `GeoLyr.usda` | Define instance hierarchy and reference published asset entrypoints; asset-internal geometry layers may own native geometry | All authored transform operations/order; variant definitions/selections; copied asset geometry in scene layers |
| `TransLyr.usda` at the owning scope | Ordinary transforms: scene placement, assembly placement or asset-internal transforms according to ownership | Transforms owned by another package; variant definitions; conditional transform values extracted from variants |
| `VariLyr.usda` | Scene selections of asset variants; scene scenario definitions; relative scene adjustments inside those scenarios | Duplicated asset variant implementations; arbitrary edits to private asset properties |
| `MatLyr.usda`, when needed | Scene material resources and explicitly assigned scene material responsibilities | Unconditional binding or shader overrides that silently defeat asset finish variants |
| Asset package | Geometry, intrinsic transforms, materials, reusable variants and their public interface, generally loaded as Payload/Reference                | Placement of a particular instance in a particular scene |

**CC-02 — Mandatory transform separation.** GeoLyr contains no variant definitions, selections, or authored transform operations. Ordinary transforms belong in the rightful owner's TransLyr. If a transform needs authoring and that owner has no TransLyr, create it and include it in that owner's layer stack. Missing TransLyr is never permission to put transforms in GeoLyr. This includes operation values, time samples, pivots, `xformOpOrder` and reset-stack tokens. Defining an Xform prim or storing mesh points is not itself authoring transform operations. Variant-dependent transform contributions remain inside the rightful owner's variant context in VariLyr, as defined by CC-07/09; never extract them into unconditional TransLyr opinions. File names are conventions; future checks must inspect authored content.

## 4. Asset interface and lofting contract

**CC-03 — Asset-owned alternatives.** A choice meaningful independently of a particular scene belongs in the asset: finish, detail, configuration or intrinsic articulation. Define it once in the asset package's variant layer at the hierarchy level that owns the choice. Assemblies are assets too: a robot-wide finish can belong to the robot assembly, while its hand or screw has separate intrinsic defaults. The scene selects a published choice rather than copying its implementation. Apply the role separation recursively within authored asset and assembly packages.

**CC-04 — Public interface.** Publish stable entrypoint paths, variant-set names, available choices, defaults, supported parameters, units, up-axis and origin/pivot conventions. Identify private implementation paths. An asset's default values must not accidentally mask its own variants. Interface changes require an explicit compatibility decision.

**CC-05 — Lofting location.** Keep lofted information in the asset interface, above a payload when a payload is used. This can advertise lightweight variant information while heavy implementation remains behind the payload. A separate asset-owned interface/loft layer is optional. No scene LoftLyr is required merely to discover referenced variants.

Lofting is a publishing pattern, not a new composition arc and not automatic promotion to `/World`. A scene-parent control driving several asset choices must be authored explicitly as a scene scenario. Lofted declarations must stay synchronized with the published asset. Small assets may expose their interface directly without a payload. [NVIDIA asset interfaces and lofting](https://docs.omniverse.nvidia.com/usd/latest/learn-openusd/independent/asset-structure-principles.html#reference-payload-pattern)

## 5. Transform contract

**CC-06 — Separate base placement, scene adjustment and asset internals.** Use this baseline hierarchy for each independently placed instance:

```text
/World/Cube01                 TransLyr: base placement values
    /Adjustment              VariLyr: relative scene adjustments
        /Asset               GeoLyr: reference to the asset interface
            ...              Asset-owned implementation
```

GeoLyr defines the placement/adjustment structure; the indicated layers supply its values. Intrinsic asset transforms remain in the asset. This is a proposed baseline for new samples, not a description of every existing A–H scene.

**CC-07 — Relative adjustment semantics.** Scene adjustments combine with placement. Translation is an offset in the placement parent's coordinate frame, rotation is relative, and scale is multiplicative. Define the adjustment pivot at the agreed instance origin, rotation order XYZ, and the operation list `[translate, rotateXYZ, scale]`. Neutral values are translation zero, rotation zero and scale one. Do not use a reset transform stack in this baseline profile.

A placement translation `(100, 200, 0)` and adjustment `(0, 0, 10)` yield `(100, 200, 10)` when placement rotation and scale are identity. A rotated or scaled placement also rotates or scales that offset. A world-space offset is a different profile and must be labelled explicitly.

Normal and other scene adjustment presets must supply their intended adjustment operations, values and order inside the scenario context. Do not create an unconditional competing adjustment value elsewhere in the scene stack. When no scenario contributes an adjustment, an empty adjustment transform is neutral. [OpenUSD transform operations](https://openusd.org/release/api/class_usd_geom_xformable.html)

## 6. Selection and scenario contract

**CC-08 — Two explicit authoring modes.**

- **Manual configuration:** VariLyr stores direct selection metadata on referenced asset instances. Selecting Finish=Red writes that selection, not a copy of Red's material values.
- **Scene scenario:** VariLyr defines a scene-level variant whose contents select asset configurations and supply relative adjustments. The child selections belong inside that scenario's edit context.

Do not leave a direct local selection on a child while expecting a scene scenario to control the same selection. Such a selection can mask the scenario's nested choice. Clear the competing selection opinion from its actual owning layer; do not equate clearing with writing an empty-string selection, which can block weaker selections. [UsdVariantSet selection and blocking](https://openusd.org/release/api/class_usd_variant_set.html)

**CC-09 — Ownership of deltas.** A variant dropdown change normally creates selection metadata. Editing the contents of a variant is a different operation. Asset-specific variant-content changes require an asset-authoring workflow and versioned publication. A scene-specific extension must be explicitly classified and authored under scene ownership, rather than silently rewriting or duplicating an asset alternative.

Independent scene variant sets should control disjoint properties. Coordinating overlapping choices requires an explicit scenario owner and precedence rule.

## 7. Material contract

**CC-10 — Asset finish ownership.** Asset finish variants own their documented material changes or bindings at the hierarchy level with rightful ownership. That level's MatLyr owns fixed material assignments, material resources and non-variant material work. Variant-dependent bindings, selections or shader opinions belong inside that level's VariLyr context. Scene MatLyr may supply unrelated scene materials and resources. It must not write competing values on finish-controlled targets as a routine default.

A deliberate scene material override is a separate, labelled mode. State which finish behavior it supersedes and how to remove it. Material binding has its own resolution rules, including hierarchy and binding strength; evaluate the resolved material, not only the layer list. A material change may select a binding or change shader inputs, depending on the asset interface. Neither is automatically an additive blend. [Material binding API](https://openusd.org/release/api/class_usd_shade_material_binding_a_p_i.html)

## 8. Presenter and persistence contract

**CC-11 — Discovery is separate from authoring destination.** Variant Presenter can list sets on referenced prims, display selections and provide controls. It does not enforce our role-based file ownership merely because a file is called VariLyr. [Variant Presenter](https://docs.omniverse.nvidia.com/extensions/latest/ext_variant-presenter.html)

Required tool behavior:

1. Identify whether the user is changing a direct asset selection, a scenario selection, or scenario contents.
2. Route the change to VariLyr and the appropriate authoring context.
3. Preserve asset files and unrelated scene layers.
4. Save VariLyr deliberately and report unsaved/session-only state.
5. Flag a stronger opinion that masks the intended configuration.

USD's selection API writes to the stage's current edit target. For a manual workflow, select the intended scene authoring layer and confirm the actual authored destination in the installed application. Guaranteed automatic routing requires a configured tool or adapter and acceptance evidence. The stock Presenter's precise write behavior in this installed Kit build has not been inspected here. No automatic routing or autosave is claimed as implemented.

## 9. Harness and sample acceptance

**CC-12 — Evidence before best-practice status.** Each approved sample must identify its contract/profile, supported controls, expected results, source versions and application observations. Keep API composition checks separate from viewport/UI observations.

Planned acceptance criteria:

- Layer responsibilities match CC-01/02; geometry remains referenced.
- Asset variants and public interface conform to CC-03/04/05.
- Two references to the same asset support different scene selections without changing the source asset.
- Placement changes preserve the intended asset configuration; relative offsets obey CC-06/07.
- Manual selection and scenario mode behave as CC-08 specifies, including the conflict case.
- Material selections resolve as CC-10 specifies.
- Presenter changes persist to the intended scene layer and survive reopening; source assets remain unchanged.
- Relative dependencies resolve after relocating a complete sample folder.
- For a payload profile, published controls remain discoverable while the payload is unloaded.

These are requirements for future checks, not tests added or run by this document.

## 10. First conforming sample and progression

Start with one cube asset publishing a Finish set and a clearly defined intrinsic configuration, referenced through GeoLyr. Add TransLyr placement, VariLyr selection, and then a scene scenario with a small relative offset. Use a material layer only when it has a distinct responsibility. Demonstrate the masked-property failure separately.

Next introduce a second reference to the same asset. Add payload packaging and lofting only after the basic selection and persistence workflow is understood. Extend to animation, simulation and instancing with explicit profiles rather than treating the baseline as universal.

The old A–H examples remain useful mechanism experiments. G is closest to asset-owned variant selection; C illustrates transform separation. B and F place scene variant definitions in GeoLyr and therefore violate CC-02. None is automatically certified against this new contract. Future revisions should preserve those experiments and clearly identify new conforming samples.

## 11. Rightful ownership across nested assets

**CC-13 — Determine owner before destination layer.** Every adjustment has two independent classifications: its semantic owner (library, part, subassembly, product, or scene occurrence) and its technical role (geometry, transform, material, variant, or another explicit domain). Project requirements and the responsible team define ownership. Prim depth, file name, current selection, and current edit target are not sufficient evidence of ownership.

The routing question is first “whose decision is this?” and then “which layer and authoring context does that owner use?” A product-level material choice belongs to the product's MatLyr or VariLyr, not automatically the scene's similarly named file.

| Decision | Candidate rightful owner, subject to project requirements | Destination |
|---|---|---|
| Shared definition of stainless steel appearance | Material-library maintainer | Versioned library material definition |
| A screw's standard material/grade | Screw part definition | Screw asset's material configuration and product metadata |
| Screw options: black steel, stainless steel, copper | Screw family if reusable; otherwise the assembly configuration selecting the screw | Owning asset's variants or assembly selections |
| White glossy finish across robot body panels | Humanoid product assembly | Assembly MatLyr if fixed; assembly VariLyr if selectable |
| A reusable anodized finish on an aluminium component | Component family or product assembly, according to the finish specification | Owning level's material/variant configuration |
| Placement of the left hand within an arm assembly | Arm assembly | Arm assembly TransLyr |
| Placement of robot instance 17 in a factory | Factory scene occurrence | Scene TransLyr |

**CC-14 — Assemblies coordinate through declared interfaces.** A humanoid may reference torso, hips, legs, arms and hands, each containing further assets. Its product finish should target declared finish controls or named surface groups, rather than arbitrary private mesh paths. Options include selecting published child finish variants, driving a documented material parameter, or applying a governed binding to an advertised collection. Record which mechanism is chosen and why.

For example, a BodyFinish choice may apply to the white exterior panels while leaving stainless fasteners and copper conductors unchanged. Do not infer membership from current colour. Declare stable roles or collections such as body panels and fasteners. A parent binding does not automatically defeat every child binding; account for binding inheritance, collection membership, purpose and strength, and inspect the resolved result. [USD material binding](https://openusd.org/release/api/class_usd_shade_material_binding_a_p_i.html)

An assembly selection does not rewrite the referenced component's source defaults. Persistent component changes are published by the component owner. A documented assembly override is not automatically a misplaced opinion merely because it affects a descendant.

## 12. Shared material libraries and controlled propagation

**CC-15 — Share definitions, record dependencies.** Reuse governed material definitions through compositional links or an agreed library interface. Do not duplicate shader values merely to distribute a common appearance. A derived finish should preserve its relationship to the base material and identify its intentional differences. USD references and, where appropriate, material specialization can support this; the chosen profile must define the actual pattern. [OpenUSD specializes example](https://openusd.org/release/glossary.html#usdglossary-specializes)

A library change reaches consumers only when they resolve to the changed dependency and do not mask the changed properties with stronger opinions. A copied material, a pinned older version or a local override can retain an older result. “Change steel once and everything updates” is therefore a dependency/version policy, not an unconditional USD guarantee.

Choose and record whether a project follows an approved evolving library revision or pins a released revision. Publish library updates with affected-consumer information and a controlled adoption process. Do not overwrite all historical products to force a new appearance.

Distinguish engineering material identity, surface treatment and render appearance. Changing a shader to look like copper does not update a part's engineering specification, mass properties or bill of materials. Those mappings require explicit authoritative data.

## 13. Project, team and PLM authority

**CC-16 — Record the ownership decision.** Maintain an ownership register with at least:

- Stable asset/product/material identifier and revision; occurrence identifier when instance-specific.
- Semantic owner, responsible team and scope of the decision.
- Source requirement, specification, BOM/PLM record or team decision establishing that ownership.
- Public prim/parameter/variant interface and affected property or surface group.
- Destination package, layer role and conditional authoring context.
- Permitted downstream overrides and their precedence; material/dependency version policy.

PLM, manufacturing and order/configuration systems may provide the authoritative product structure, permitted finishes and defaults. USD is their mapped scene representation, not automatically their replacement. Connector/resolver mappings, stable IDs and synchronization behavior must be specified. Changes with missing or conflicting authority are reported for resolution rather than assigned an owner from visual appearance or an LLM guess.

## 14. Inspect authored opinions, not only visual delta markers

**CC-17 — Structured opinion inventory.** The future harness must report actual authored fields and their composition context. A generic UI delta marker is not enough. Inspect both layer specifications and the composed stage; include inactive variant branches and report unavailable or unloaded dependencies explicitly.

Each record should show source layer, authored spec path, composed prim path where available, variant context, field/property, default/time-sample/relationship/list-edit type, owning package, intended owner, strength/contributing opinions, and proposed disposition. Surface material bindings, shader inputs, asset links, selection metadata and transform operations as distinct categories.

“Variant” and “transform” are not mutually exclusive delta types: a scale opinion can be authored inside a variant. Likewise, selecting a variant and editing its contents are different records. Preserve both the property's role and its conditional context.

This requirement addresses the user's reported difficulty understanding deltas in the Omniverse UI. It is not a claim that every Kit version lacks property inspection or movement tools.

## 15. Deterministic repair with AI assistance

**CC-18 — Separate discovery, decision and execution.** Use a deterministic USD-aware inspector and policy engine for classification and moves where ownership is explicit. An LLM may explain conflicts, interpret project requirements and propose mappings. It must not silently invent an owner, infer material identity from colour, or promote a scene-specific change into a shared asset or library. MCP can expose these capabilities; it is a tool interface, not the ownership policy itself.

An automatic mode may execute a specifically authorized policy for unambiguous repairs. Ambiguous ownership, destination conflicts and intentional behavior changes require a reviewable decision. Prevent wrong-layer writes through edit routing where possible; cleanup is the recovery path.

**CC-19 — Preserve authored meaning during repair.** A layer move can change strength, asset-path anchoring, variant context and resulting behavior. Distinguish a behavior-preserving relocation from a correction intended to change the result; record the expected difference for the latter.

Required repair sequence:

1. Snapshot the source revision, relevant layer content and in-memory/session state. Detect concurrent edits before applying a patch.
2. Produce a field-level move plan: contract rule, rightful owner, source/destination/context, dependency changes, conflicts and expected behavior.
3. Create the rightful owner's TransLyr if needed, and explicitly register its sublayer position. Do not choose the scene package when the assembly or asset owns the change.
4. Use USD-aware edits, preserving defaults, time samples, variant paths, connections, relationships, list operations, metadata, relative asset paths and required ancestor specs. Move related transform operations and their order coherently.
5. Evaluate the proposed destination changes and removal of source opinions together on an isolated candidate. A copied destination opinion alone can appear ineffective while the stronger source still exists.
6. Compare the declared behavior across affected variants, instances, time samples and load contexts. Check transforms, resolved materials and dependencies as applicable; incomplete coverage is reported, not called equivalent.
7. Apply the planned change transactionally with revision/conflict checks and rollback information. Remove only the source fields covered by the accepted plan; do not delete unrelated prim content or overwrite existing destination opinions silently.
8. Record an audit report containing changes, ownership authority, before/after results and unresolved issues. Repeating a completed cleanup should propose no additional changes unless inputs changed.

Do not flatten the stage as a cleanup shortcut: the authoring structure and its ownership must survive. Do not save an asset-source edit merely because its reference is visible in a scene. [USD edit-target mapping](https://openusd.org/release/api/class_usd_edit_target.html)

## 16. Next harness increments

1. Establish the ownership register and recursive layer-role rules, including the mandatory TransLyr rule.
2. Build a read-only opinion report that explains category, owner and context.
3. Add dry-run repair proposals for misplaced ordinary transforms; include missing TransLyr creation.
4. Add candidate comparison, audit and rollback before enabling automatic repair.
5. Extend to material bindings, asset selections, nested assembly ownership and PLM-driven defaults.
6. Add LLM/MCP assistance for interpreting and reviewing difficult cases, with the same deterministic execution and evidence requirements.

These are planned capabilities. This contract update does not install a cleanup service, run migrations, connect to PLM, or modify the existing sample scenes.

## 17. Layer-role catalogue

**CC-20 — Define roles, instantiate only required contributions.** The following catalogue extends our agreed paradigm. Roles apply recursively to scenes, assemblies and assets at their rightful ownership level. A role is not necessarily one file: a team may split a contribution into bounded sublayers with named owners. Create files when content requires them, rather than generating every possible empty layer. The mandatory TransLyr rule still applies when ordinary transforms are needed.

This table defines responsibilities, **not strongest-to-weakest order**. Proposed filenames are project conventions, not registered USD layer types.

| Role / proposed filename | Owns | Boundary |
|---|---|---|
| Root / package interface | Stage/package metadata, composition entrypoints and sublayer assembly; published asset interface | Routine authoring stays in the relevant contribution; lightweight lofted declarations are allowed at the asset interface. |
| Geometry — `GeoLyr.usda` | Scene hierarchy and references to public asset interfaces; native geometry inside its owning asset | No transform operations, variant definitions or selections. |
| Transforms — `TransLyr.usda` | Ordinary base placement, alignment, pivots and transform operation order at the rightful scope | Conditional, animated and simulation-controlled contributions follow CC-21. |
| Materials — `MatLyr.usda` | Shading networks/resources and bindings owned at this scope | Shared definitions come from material libraries; variant-dependent bindings stay in their variant context. Physical friction/restitution belong to physics, even when represented through a material prim. |
| Variants — `VariLyr.usda` | Owned alternatives, scene scenarios and selections of published asset choices | Asset-specific definitions remain asset-owned; scene selections do not copy their contents. |
| Rig — `RigLyr.usda` | Skeleton structure, rest/bind data and skinning bindings; declared rig interfaces | No assumption that USD contains an executable DCC control rig. Robot physics joints and articulations follow Physics. |
| Animation — `AnimLyr.usda` | Authored motion, animation bindings/clips and intended time-varying property animation | Separate from rig structure, solver predictions and live measured state. |
| Environment — `EnvLyr.usda` | Environment assembly, backdrop/ground resources and environment-specific settings | Reference reusable environment assets; separate light definitions, material work and ordinary placement into their roles. |
| Cameras — `CamLyr.usda` | Camera prim definitions, optics and camera-specific settings | Base pose uses TransLyr; authored camera motion uses AnimLyr. Render-camera selection belongs to Render. |
| Lighting — `LightLyr.usda` | Light prim definitions, intensity, colour, light linking and light-specific resources | Base pose uses TransLyr; animated values use AnimLyr. A dome light, including its environment texture, belongs here. |
| Physics — `PhysicsLyr.usda` | Bodies, collision, mass/inertia, joints, limits, drives, physics materials and simulation setup | Intrinsic setup stays in the asset; scene integration stays in the scene. Solver outputs are separate. Backend-specific contributions need explicit profiles. |
| Behavior — `BehaviorLyr.usda` | Declared controller/behavior connections and application graph configuration | Action graphs are one implementation. Execution needs a compatible runtime; layer composition alone does not execute logic. |
| Simulation results — `SimLyr.usda` | Deliberately published solver results and result overlays | Record scenario, solver/configuration, time and provenance. Large/transient results may remain external. |
| Project data — `DataLyr.usda` | Project/occurrence IDs, integration mappings and stable or slowly changing contextual facts | No second owner for intrinsic product facts; no telemetry history by default. May aggregate project-specific sublayers. |
| Runtime snapshot — `RuntimeLyr.usda` | Explicitly persisted operational snapshots | Live state may stay in external/runtime/session storage. Never silently save it into asset source or base transforms. |
| Properties / semantics — `PropertiesLyr.usda` | Intrinsic product facts, classifications and supported capabilities at their owning package | Project mappings belong in Data. Schema and source authority must be declared. |
| Connection interfaces — `PortsLyr.usda` | Reusable asset-owned ports, attachment interfaces and their semantic definitions | Ordinary port placement follows TransLyr; schema-specific frame data follows its declared semantic owner. |
| Assembly topology — `ConnectionsLyr.usda` | Connections between public ports of composed instances | Does not duplicate ports; physics constraints belong to Physics. Declare which representation owns each relationship. |
| Render / presentation — `RenderLyr.usda` | Render settings, products/outputs and active camera relationships | Renderer/application-specific settings need a supported profile. Does not own light or camera pose. |
| Sensors — `SensorLyr.usda`, optional | Sensor definitions, calibration parameters and sensor-specific configuration | Useful for commissioning/robotics; camera optics can remain Cam-owned. Explicitly assign overlapping fields; live readings belong to runtime/data services. |
| Review overrides — `ReviewLyr.usda`, optional | Explicit, temporary review exceptions with owner, reason and disposition | Never a permanent catch-all or a hidden replacement for VariLyr/TransLyr/MatLyr. |

The additional roles most relevant beyond the user's initial list are **physics, behavior, simulation results, runtime snapshots, intrinsic properties, connection interfaces/topology and render settings**. Sensors and review overrides are optional project capabilities.

## 18. Rig, animation and transform ownership

**CC-21 — Route by meaning and context, not property spelling alone.** The expanded catalogue refines CC-02: GeoLyr still contains no authored transform operations, but not every matrix or time sample belongs in TransLyr.

| Contribution | Destination |
|---|---|
| Ordinary asset/assembly/scene placement | Rightful owner's TransLyr; create it if absent. |
| Variant-dependent transform alternative | Rightful owner's VariLyr, inside its branch. |
| Authored moving-camera path or object motion | AnimLyr, with declared operation and time ownership. |
| Skeleton rest/bind transforms and skinning data | RigLyr. |
| Physics joint frames, mass-frame data and constraints | PhysicsLyr. |
| Published solver pose/result | SimLyr. |
| Current measured pose | Declared runtime mechanism; RuntimeLyr only for deliberate persistence. |

**Differentiate rig and animation.** Rig describes the structure and binding that can be animated; animation supplies motion. OpenUSD distinguishes skeleton/binding data and skeletal animation. It does not make every DCC rig portable as executable controls. A mechanical robot may instead use rigid-body articulation and controller configuration, so do not require a skeletal RigLyr for every robot. See [UsdSkel](https://openusd.org/release/api/usd_skel_page_front.html) and [UsdPhysics](https://openusd.org/release/api/usd_physics_page_front.html).

For ordinary placement plus animation, prefer separately owned parent/child transforms or explicitly named operations with one declared owner for the complete operation order. If animation replaces a base pose on the same property, declare that competition and its intended strength. A stronger default can mask weaker animation; splitting values into differently named files does not solve it.

Conditional content remains conditional: a variant choosing an animation, physics backend or rig configuration lives in VariLyr and can reference the appropriate contribution. Cleanup must preserve that context rather than making the selected contribution unconditional.

## 19. Project data and runtime integration

**CC-22 — Data aggregation with bounded responsibilities.** Use DataLyr as a thin project-data aggregate when several sources or owners justify subdivision. A possible commissioning profile is:

```text
DataLyr.usda                 # composes project-data contributions
  Data/IdentityLyr.usda      # occurrence IDs and system-to-USD mappings
  Data/UNSMappingLyr.usda    # namespace/tag -> target property contract
  Data/ContextLyr.usda       # approved installation/project context
```

These are sublayers, not child prims or external message queues. Nested sublayers remain in the same local layer stack. Their order resolves conflicts only where authored fields overlap; ideally their contracted ownership is disjoint. Relative paths are anchored to the layer containing them.

OPC UA and MQTT are integration mechanisms, not ownership levels. A project may split mappings by connector or domain when different teams maintain them, but each target property still needs one authority. UNS mappings should identify source identity, target prim/property, units/conversion, coordinate frame, timestamps/time basis, quality/staleness handling, update policy, permitted writer and persistence policy. Keep credentials and transport execution outside authored scene data.

Separate three lifecycles:

1. **Configuration:** which source supplies which property — DataLyr and external connector configuration.
2. **Live state:** incoming measurements — runtime/session/external storage as the application requires.
3. **Published evidence:** a deliberate snapshot or solver result — RuntimeLyr or SimLyr with provenance and time semantics.

Variants express discrete supported configurations; they are not a high-frequency telemetry mechanism. Selecting a commissioning scenario may choose mappings/controllers, but does not subscribe to MQTT or run a controller by itself.

The user's “Fabric Azure” integration needs its project-specific service contract recorded before implementation. Microsoft Fabric/Azure services and NVIDIA Omniverse Fabric must not be treated as interchangeable. This catalogue does not select or implement either integration.

## 20. Strength, operating modes and contract profiles

**CC-23 — Explicit conflict and writer policy per profile.** A layer catalogue does not define one universal stack order. Each scene/package profile must state its actual sublayer order, allowed overlapping fields and reasons for those overlaps. Ordinary local property opinions can still mask variants; moving them to TransLyr or MatLyr does not weaken them automatically.

For competing animation, simulation and live updates, define a mode such as authored playback, simulation or live commissioning. Specify which writer owns each controlled property in that mode, how other writers are disabled and how state is restored when leaving it. Do not allow three independent writers to race and rely on whichever layer happens to be strongest. Runtime data outside USD composition requires runtime authority controls as well.

Each role declaration needs: owning scope/team; source authority; allowed prims/fields; unconditional or variant context; edit target; persistence and update frequency; dependencies; allowed overrides; conflict policy; lifecycle; and planned acceptance evidence. Contracts/validation reports belong alongside the package, not in a fictional validation layer expected to enforce itself.

## 21. Reference basis and future interface

The requested [GoodStart layer-order research](https://github.com/jph2/USD_GoodStart/blob/main/WIP_Docs/LAYER_ORDER_REFERENCES_RESEARCH.md) was consulted on 2026-10-10, particularly sections 8 and 18. It compares alternative pipelines and treats GoodStart's order as a proposal, not a universal OpenUSD rule. Its separation of stable project data, runtime state, simulation and reusable asset publication informs this catalogue. Our explicit TransLyr and separate lighting roles refine its broader asset/environment lanes.

Related local GoodStart references consulted: `docs/best-practices/layer-stacking-workstreams.md`, `docs/learning-path/07-layer-profiles-project-structure/layer-lanes-write-targets.md`, and `docs/learning-path/05-layering-asset-structure/layer-order-research-breakout.md`. These are reference evidence; OpenUSD_Composition_Contracts now owns the conventions defined here. TutorialBuilder retains the earlier experimental scenes.

An Omniverse extension with an ownership-aware interface is a possible later delivery surface. First define the contracts and a read-only inspector, then repair planning and routing. Keep the policy/inspection core independent of UI and MCP adapters so several tools can use the same rules. Extension implementation and technology selection remain deferred. This update changes documentation only; existing example scenes have not been migrated or certified against this catalogue.
