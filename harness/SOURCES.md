# Sources, provenance and integration routes

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

## 0.2 example and layout evidence — 2026-10-10

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

The new example's own build manifest records generated package content, authoring script/contract hashes, runtime and observations. All example geometry and layers were newly authored through the local script; no private pipeline code or scene was imported.

## Session-default implementation evidence — 2026-10-10

Bounded read-only inspection of the installed Kit extensions `omni.kit.usd.layers` 2.7.2 (`LayerUtils` authoring-target save/restore and lock helpers; LayersState API) and `omni.kit.widget.layers` 1.9.3 (stage-attach restoration, lock handling and layer-window setting names) informed the startup helper. Anonymous targets are skipped by saved authoring metadata; the ordinary lock helper excludes the root. No installed extension code was copied or edited, and no installed tests were run.

The public [LayersState reference](https://docs.omniverse.nvidia.com/kit/docs/omni.kit.usd.layers/latest/omni.kit.usd.layers/omni.kit.usd.layers.LayersState.html) documents UI layer locks and their distinction from disk permissions. The [Layers documentation](https://docs.omniverse.nvidia.com/extensions/latest/ext_core/ext_layers.html) describes session content and authoring targets. These sources support the application boundary, not a claim that the new helper has been executed in Kit.

## User-selected Omniverse root — 2026-10-10

Jan supplied `examples/01_LayeredScene/ROOT_example.usda` and requested it as the standard scene. Its authored content establishes the exact startup profile: `/World`, top-level `/Environment` and `/Render`, `OmniverseKit_*` viewport opinions, Z-up, `metersPerUnit = 0.009999999776482582`, 60 fps and time codes 0–100. This is direct local evidence, not a claim about every Omniverse product's defaults.

The untouched source and SHA-256/resource records are in `harness/evidence/standard_root_adoption`. `templates/Omniverse/ROOT_example.usda` retains the template with only two texture paths rebased for reuse. Its sky HDR and grid image were copied from the installed `omni.kit.stage_templates` 2.0.3 files referenced by the supplied root. The example ships local copies of those textures; `OmniPBR.mdl`, OmniRtx schemas and viewport camera completion depend on the Kit runtime. No Kit installation or predecessor repository was changed. Earlier example file versions and the previous build report were retained before replacement.
