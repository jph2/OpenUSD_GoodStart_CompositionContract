# Layered scene example

**CC-EXAMPLE-01/0.1.1 · Omniverse standard scene selected by Jan · centimetres · Z-up.** Start with [SceneROOT_Example.usda](SceneROOT_Example.usda). It preserves the supplied Omniverse starting scene and composes the example assets below `/World`. All referenced USD assets and the two template textures are bundled. The template's OmniPBR material and RTX/viewport features require a compatible Omniverse application.

The standard scene uses `/World` with no transform, `/Environment` and `/Render` as top-level siblings, and `/OmniverseKit_Persp` as the initial viewport camera. Its original `metersPerUnit = 0.009999999776482582`, Z-up, time codes 0–100 and 60 fps are preserved. This is effectively the same centimetre scale as the earlier example; no axis conversion or extra world transform was introduced. The custom Overview camera and earlier scene ground/lights have been retired from the active package.

## Starter master preset

For a fresh independent copy, use the repository's `starter/Composition_Starter_0.1.1` portable setup folder. Copy that whole folder into your chosen location and run `Create_Composition_Project.bat`. Its launcher defaults to STARTER; this source example's launcher still defaults to Example. The setup refuses file collisions and requires no Python or network connection.

[SceneROOT_STARTER.usda](SceneROOT_STARTER.usda) deliberately includes more than a minimal scene. It includes the Cube/Cone examples and DisplayPair assembly, shared asset materials, independent placement and variant selections, identity/context examples, and the supplied Omniverse environment, lights, cameras and render baseline. Its direct work sublayers are:

| Class | Included roles, strongest to weakest within the listed group |
|---|---|
| REVIEW | `Starter/OpinLYR_default.usda` — default editable experiment target |
| RUNTIME | `Starter/RuntimeLyr.usda` — optional empty slot |
| SIM | `Starter/SimLyr.usda` — optional empty result slot |
| DATA | `Starter/DataLyr.usda` with independent IdentityLyr and ContextLyr examples |
| BASE | EnvLyr, LightLyr, CamLyr, RenderLyr, AnimLyr, PhysicsLyr, RigLyr, MatLyr — optional empty work slots |
| BASE | TransLyr, VariLyr, GeoLyr — independent demo setup; GeoLyr at the bottom |

The optional slots provide destinations, not a running physics solver, animation, connector or simulation result. Asset material definitions and bindings already work through the linked packages; MatLyr is available for additional scene-owned work. Baseline environment/lights/cameras/render remain in the root under the existing template exception, so muting their empty work slots does not remove that baseline. This root has no nested SceneROOT.

Remove unneeded sublayers from a copied root or mute them for temporary exploration. Muting GeoLyr removes its linked demo assets; deleting a layer file can break other roots. The starter work layers are separate from the demo work layers, while reusable assets and textures are shared. For a new independent project, copy the package with its dependencies before editing; copying only the root preserves shared file links. Treat the master as a preset to copy.

## Default authoring state

**Opinion is the default editable authoring layer; all other persistent layers are protected.** The five demo roots share `050_REVIEW/OpinLYR_default.usda`; the starter has its own `050_REVIEW/Starter/OpinLYR_default.usda`. Both start empty. Demo Opinion edits affect all five demo roots, and its stronger opinions can mask the deliberate conflict fixtures.

```powershell
.\Open_In_Kit.ps1
.\Open_In_Kit.ps1 -Scene STARTER
.\Open_In_Kit.ps1 -Scene Scenarios
```

The launcher opens Example by default and detects the executable/app configuration from a running Kit instance, or accepts `-KitExe` and `-AppConfig`. Existing application windows are left alone. Standard and Manual select Example. The bundled `_workflows/kit/session_defaults.py` retains its historical filename but now selects the declared Opinion layer, unlocks it, protects the root and other loaded persistent layers, and disables Auto Authoring and Specs Linking. It does not save or route edits. Opening a USDA directly does not guarantee edit-target selection; use the launcher. Updated Kit runtime acceptance remains pending.

Saving Opinion persists experiments. Promote reviewed fields to their rightful owner/layer/variant branch, then remove only superseded opinions from Opinion. To edit another persistent layer, deliberately unlock and select it; the helper supports `builtins.cc_session_defaults.unlock(layer.identifier)`. Restore the default using `builtins.cc_session_defaults.schedule()`. Session remains available for transient edits; clear competing Session opinions when returning to Opinion authoring. No automatic promotion or cleanup is implemented.

Use the supplied Omniverse perspective viewport, `/OmniverseKit_Persp`, or frame `/World`. The camera settings, orthographic viewpoints, grid ground, sky, distant light and render state come from the supplied root. Its viewport cameras include application-managed `over` specs that Kit completes; a standalone USD reader is not a substitute for that runtime. Asset Finish appearance uses UsdPreviewSurface, while the standard ground uses OmniPBR. Rendering and viewport startup have not been inspected in Kit.

## Standard scene and companion entrypoints

Each entrypoint now has one root with direct scene work sublayers. `World_Manual`, `World_MaskedSize` and `World_MaskedSelection` no longer wrap another scene root. The supplied startup content is adopted into each root. Prior build observations below are historical; this structural correction has not received a new full acceptance run. Original wrappers and the prior report are preserved in `harness/evidence/before_direct_scene_roots`.

| Open | What it demonstrates | Saved state / expected appearance |
|---|---|---|
| [SceneROOT_Example.usda](SceneROOT_Example.usda) | Standard Omniverse root with two independently configured Cube references, Cone and nested assembly | Red normal cube, blue tall cube, yellow cone; blue cube/cone pair behind |
| [SceneROOT_Manual.usda](SceneROOT_Manual.usda) | Independent manual root matching ROOT_example | Same standard scene |
| [SceneROOT_Scenarios.usda](SceneROOT_Scenarios.usda) | A scene-level Layout controls child selections and relative adjustments | Normal matches Manual; Exploded raises the tall cube by 80 cm, makes it red, makes Cube01 yellow and the pair Warm |
| [SceneROOT_MaskedSize.usda](SceneROOT_MaskedSize.usda) | Direct local scale masks an asset variant | Cube02 still selects Tall but resolves to scale one |
| [SceneROOT_MaskedSelection.usda](SceneROOT_MaskedSelection.usda) | Direct child selection masks a scene scenario | Cube01 remains Blue although the Normal branch selects Red |

The two masked entrypoints are deliberate counterexamples. Their ReviewLyr files are excluded from the baseline roots. They reproduce the distinction between selecting a variant and obtaining its intended result. Local opinions masking variant opinions are illustrated in the upstream [OpenUSD variant tutorial](https://openusd.org/release/tut_authoring_variants.html).

## Choose configurations

In manual mode, preview selections in the session layer. For a saved configuration, deliberately unlock `020_BASE_LYR/VariLyr.usda` and make it the edit target. Both Cube and Cone publish Size = Normal / Large / Tall and Finish = Red / Blue / Yellow. These choices target the referenced root prim:

| Instance | Prim containing the controls | Initial selection |
|---|---|---|
| Cube01 | `/World/Cube01/Adjustment/Asset` | Normal, Red |
| Cube02 | `/World/Cube02/Adjustment/Asset` | Tall, Blue |
| Cone01 | `/World/Cone01/Adjustment/Asset` | Normal, Yellow |
| DisplayPair | `/World/Pair01/Adjustment/Asset` | Palette=Cool |

DisplayPair publishes Palette = Cool (Blue/Blue) or Warm (Red/Yellow). Its own VariLyr selects the child Finish variants. The same Cube package supplies the two standalone cubes and the cube inside this assembly.

In scenario mode, select `/World` and preview Layout = Normal or Exploded in the session. For persistence, unlock and use `020_BASE_LYR/Scenarios/VariLyr.usda`. That root does not include the manual selection layer. To edit a scenario's contents, enter its variant edit context. A direct child selection outside the scenario would create the conflict shown by World_MaskedSelection.

Save the intended layer deliberately. A session-only change may disappear on reopening or mask saved selections. The package contains no automatic edit routing or autosave extension.

## Place an occurrence

Preview placement on the occurrence parent in the session, for example `/World/Cube02`. To persist placement, unlock and edit `020_BASE_LYR/TransLyr.usda`. Each parent has translate, rotateXYZ and scale in that order. The next child, Adjustment, is reserved for the scene scenario's relative transform; its values and order stay inside each Layout branch. The Asset child's intrinsic size belongs to the referenced asset.

With the supplied identity placement rotation and scale, the Exploded offset raises Cube02 from z=0 to z=80 cm. If placement is rotated or scaled, the same offset follows that placement frame. See [UsdGeomXformable](https://openusd.org/release/api/class_usd_geom_xformable.html).

## Where files belong

See the repository's [project structure and diagram](../../PROJECT_STRUCTURE.md). Within this folder:

The root's scene sublayers form this vertical stack, strongest at the top:

```text
DataLyr
TransLyr
VariLyr        (manual OR scenario contribution)
GeoLyr         BOTTOM / WEAKEST — references Cube, Cone and DisplayPair
```

All four are sibling sublayers of the root. Additional scene roles are stacked above GeoLyr when needed; their relative order is declared by the profile. Referenced source assets remain outside this scene sublayer stack.

- `000_SOURCE` retains original inputs; `010_ASS_USD/USD_Startpoint` retains imported USD. Both are unused by these procedural shapes.
- `010_ASS_USD/USD_Wrappers` holds published Cube/Cone packages; `Assemblies` holds DisplayPair; `MatLib` holds the asset material library; `Envs/OmniverseStandard/Resources` holds the supplied ground texture and sky HDR.
- `020_BASE_LYR` holds scene contributions. `040_DATA_LYRs` holds demo occurrence IDs and project context.
- `030_SIM_LYR` and `035_RUNTIME_LYR` reserve space for future published results and snapshots. Their READMEs do not compose any USD layers.
- `050_REVIEW` holds the two deliberate exceptions. `_contracts` stores the profile, ownership and expected results. `_pipeline_reports` stores evidence. `_workflows` reserves automation definitions.

The whole folder is the intended relocation unit. File references and the two texture paths point within it. `OmniPBR.mdl` and the supplied RTX/viewport schema behavior are resolved by the Omniverse installation. Relocation and renderer resource resolution have not been exercised as acceptance tests.

## Actual authoring evidence

The historical build covered 29 USD layers, before the Opinion/starter additions. The author ran with Python 3.13.3 and OpenUSD 26.08 and reopened the standard scene plus four companion entrypoints, with default time and an empty session. No composition errors were returned for those saved configurations. The recorded `/World` matrix is identity; all entries retain the supplied Z-up, centimetre scale, 60 fps, 0–100 range and bound viewport camera.

The recorded read-back found:

| Entry | Cube01 Finish / resolved material suffix | Cube02 Size / resolved scale |
|---|---|---|
| ROOT_example and Manual root | Red / Looks/Red | Tall / (1, 1, 2) |
| Scenarios, Normal | Red / Looks/Red | Tall / (1, 1, 2) |
| MaskedSize | Red / Looks/Red | Tall / (1, 1, 1) |
| MaskedSelection, Normal | Blue / Looks/Blue | Tall / (1, 1, 2) |

See [build_manifest.json](_pipeline_reports/build_manifest.json) for file hashes, runtime and observations. This read-back covers the saved defaults and stage coordinates; it does not establish a full variant matrix, assembly behavior in all configurations, renderer appearance, physical simulation or UI persistence. No acceptance tests were run. [expected.json](_contracts/expected.json) records intended outcomes separately. The previous package and byte-exact supplied root are retained in the repository's `harness/evidence/standard_root_adoption` folder.

The 0.1.1 correction updates the current version/profile labels and diagrams. File hashes were refreshed; the USD observations above were retained from the earlier build and were not rerun. Their original report is preserved at `harness/evidence/build_before_version_0.1.1.json`, and the current manifest records that provenance.

## Reproduce the authored fixture

From the parent repository root, with `uv` available:

```powershell
uv run --no-project --with usd-core==26.8 python tools/build_example.py --output examples/MyLayeredScene
```

The output must be a new or empty directory. The authoring script never overwrites an existing scene. It creates the USD, JSON and folder notes; this walkthrough and the repository-level design remain maintained documentation. The pinned [usd-core distribution](https://pypi.org/project/usd-core/26.8/) provides Python USD APIs, not an Omniverse installation or viewer.

Full variant checks, save/reopen behavior in the chosen application, relocation, material display and human acceptance are the next evaluation step. The example-specific JSON format is not yet a generic inspection or repair contract.
