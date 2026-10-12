# LayeredScene — composition without unnecessary nesting

**Layout convention 0.2.9 · Omniverse/Kit · Z-up · centimetres.**
Simple leaves keep their asset content inline. Assemblies keep meaningful work
layers. Each scene owns a named Opinion file; an identifier is optional and uses
`OpinLYR_SceneExample.name.usda` when needed.

**Motion graphics: [Open the controls and start steering](MotionGraphics_QUICKSTART.md).**

## Choose a scene

| Open | Purpose |
|---|---|
| `SceneROOT_Example.usda` | Cube/Cone leaves and a nested DisplayPair assembly |
| `SceneROOT_Manual.usda` | Same base assembly, independently saved selections |
| `SceneROOT_STARTER.usda` | Minimal active starting stack; folder catalogue remains visible |
| `SceneROOT_Scenarios.usda` | Normal/Exploded scenario definitions |
| `SceneROOT_MaskedSize.usda` | Deliberate local-scale masking conflict |
| `SceneROOT_MaskedSelection.usda` | Deliberate selection masking conflict |
| `SceneROOT_Lofted.usda` | Discover public choices while payload content is unloaded |
| `SceneROOT_Instanced.usda` | Matching-configuration native instances |
| `SceneROOT_Instanced_Wave.usda` | Generated Wave placement/configuration |
| `SceneROOT_Instanced_Spiral.usda` | Generated Spiral placement/configuration |
| `SceneROOT_Instanced_Rings.usda` | Generated Rings placement/configuration |
| `SceneROOT_MotionGraphics.usda` | Experimental animation and live JSON controls |

Open a scene in Kit, or use `Open_In_Kit.ps1 -Scene Example` with an installed
compatible application. The launcher starts a new Kit process and selects that
scene's Opinion target; it does not save USD changes automatically. Directly
opening USD does not execute the startup helper. See [quickstart and operation details](MotionGraphics_QUICKSTART.md)
for instancing scripts, motion controls and their known runtime limitations.

## Small asset catalogue

```text
010_ASS_USD/
  AssetROOT_Cube.usda
  AssetROOT_Cone.usda
  AssetROOT_CubeLofted.usda
  AssetROOT_ConeLofted.usda
  Assemblies/
    DisplayPair/          assembly Geo / Trans / variant definitions
    DisplayPairLofted/    meaningful assembly payload contents
  Envs/                  shared preview resources for scenes/assemblies
```

Cube and Cone contain geometry, intrinsic centering, materials and Size/Finish
variants. Each shape file also contains the selected Omniverse environment,
render and viewport-camera preview outside its default asset prim. That preview
uses installed Kit texture/shader resources; these are not portable,
dependency-free deliveries. The two lofted interfaces directly payload their
corresponding leaf; there is no forwarding ContentsLyr or empty asset Opinion.
DisplayPairLofted retains ContentsLyr because it combines assembly contributions.

## Where edits belong

| Contribution | File |
|---|---|
| Saved scene choices/working edits | `050_OPINION_LYR/OpinLYR_Scene<Name>.usda` |
| Transient preview | Session, explicitly persisted only when wanted |
| Generated independent configurations | `020_BASE_LYR/ConfigLyr_<Purpose>.usda` |
| Normal/Exploded definitions and conditional contents | `020_BASE_LYR/VariLyr_Scenarios.usda` |
| Placement | Scene/assembly TransLyr |
| Asset references | Scene/assembly GeoLyr |
| Intentional conflict demonstrations | `050_OPINION_LYR/ReviewLyr_SceneMasked*.usda` |

Ordinary selections moved to each scene's Opinion. Generated Instanced and
MotionGraphics presets retain ConfigLyr because their scripts own and regenerate
those configurations independently. Opinion may override them deliberately.
Scenario-controlled child selections must not be masked unintentionally by
unconditional Opinion selections. The two Masked scenes intentionally demonstrate
such conflicts; their review overlays remain separate.

The scene roots retain their Omniverse startup settings. Named Opinion files are
independent even where scene base layers are shared, so editing Manual choices
does not silently change Example or Scenarios. Existing motion-graphics Opinion
edits and JSON controls were preserved.

## Scaffold and cleanup

The numbered scene folders remain visible as a teaching catalogue. Empty Starter
USD placeholders and unused nested assembly scaffold folders were removed.
Add layers only when their contribution is needed. No shared palette file is
required by the active shape leaves; materials remain inline.

The current root stacks are listed in [_contracts/profile.json](_contracts/profile.json).
The migration record is [_contracts/cleanup_0_2_9.json](_contracts/cleanup_0_2_9.json),
including the full pre-cleanup backup location. Existing `_pipeline_reports` are
historical evidence, not acceptance of the new layout.

## Reproduction and evidence limits

The bundled arrangement and motion scripts have been updated to the current
paths, Opinion names and ConfigLyr roles. Repository-level historical bootstrap
builders may describe earlier scaffolds; do not use them to overwrite this edited
package. They require a separate regeneration-alignment task before claiming
reproducibility of every current scene. No builder was executed during cleanup.

USD stages were opened to reconstruct dependency/lock metadata. No acceptance
tests, Kit visual review or performance measurements were run. MotionGraphics
remains an experimental feature with the limitations recorded in MotionGraphics_QUICKSTART.md.
