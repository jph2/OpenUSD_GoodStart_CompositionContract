# Layered scene example

**CC-EXAMPLE-01/0.2 · Omniverse standard scene selected by Jan · centimetres · Z-up.** Start with [ROOT_example.usda](ROOT_example.usda). It preserves the supplied Omniverse starting scene and composes the example assets below `/World`. All referenced USD assets and the two template textures are bundled. The template's OmniPBR material and RTX/viewport features require a compatible Omniverse application.

The standard scene uses `/World` with no transform, `/Environment` and `/Render` as top-level siblings, and `/OmniverseKit_Persp` as the initial viewport camera. Its original `metersPerUnit = 0.009999999776482582`, Z-up, time codes 0–100 and 60 fps are preserved. This is effectively the same centimetre scale as the earlier example; no axis conversion or extra world transform was introduced. The custom Overview camera and earlier scene ground/lights have been retired from the active package.

## Default authoring state

**All persistent layers start locked; Session Layer is the default authoring target.** Launch with [Open_In_Kit.ps1](Open_In_Kit.ps1) to apply that state automatically:

```powershell
.\Open_In_Kit.ps1
# Choose another scene:
.\Open_In_Kit.ps1 -Scene Scenarios
```

The launcher opens `ROOT_example.usda` by default in a new Kit application using the executable and app configuration detected from an already running Kit instance. If none is running, supply `-KitExe <path-to-kit.exe> -AppConfig <path-to-composer.kit>`. It leaves the existing window and its unsaved session alone. `-Scene Standard` and `-Scene Manual` both select the standard root.

The bundled `_workflows/kit/session_defaults.py` helper selects the fresh session layer after opening a tagged project, shows it in the Layers panel and protects all loaded persistent layers, including referenced assets and the root. Auto Authoring and Specs Linking are disabled for this working mode. The helper acts once per stage open, so intentional persistent authoring remains possible. It does not save files or alter filesystem permissions.

Opening a USDA directly applies the supported saved Kit layer-lock metadata, but cannot persist or restore an anonymous session authoring target. The launcher is needed for the complete default. The installed Kit layer-lock utility also excludes the root; the helper protects it through USD's runtime edit permission. Root protection may appear differently from the ordinary sublayer lock icon.

For the current Kit window, execute the bundled Python file in its Script Editor. It applies to the current opted-in stage and subsequent opted-in stages for that application session. Its runtime behavior has not yet been exercised here in Kit.

Session edits are temporary and are not saved with the scene. To persist an edit, deliberately unlock its rightful contribution and select that layer/context. The helper's explicit escape hatch is `builtins.cc_session_defaults.unlock(layer.identifier)` in Kit Python; then select that layer as the edit target. Clear any competing preview opinion from the session once its intended persistent equivalent is authored. Return to the default by scheduling `builtins.cc_session_defaults.schedule()`. No automatic session merge is implemented.

Use the supplied Omniverse perspective viewport, `/OmniverseKit_Persp`, or frame `/World`. The camera settings, orthographic viewpoints, grid ground, sky, distant light and render state come from the supplied root. Its viewport cameras include application-managed `over` specs that Kit completes; a standalone USD reader is not a substitute for that runtime. Asset Finish appearance uses UsdPreviewSurface, while the standard ground uses OmniPBR. Rendering and viewport startup have not been inspected in Kit.

## Standard scene and companion entrypoints

| Open | What it demonstrates | Saved state / expected appearance |
|---|---|---|
| [ROOT_example.usda](ROOT_example.usda) | Standard Omniverse root with two independently configured Cube references, Cone and nested assembly | Red normal cube, blue tall cube, yellow cone; blue cube/cone pair behind |
| [World_Manual.usda](World_Manual.usda) | Compatibility alias of ROOT_example | Same standard scene |
| [World_Scenarios.usda](World_Scenarios.usda) | A scene-level Layout controls child selections and relative adjustments | Normal matches Manual; Exploded raises the tall cube by 80 cm, makes it red, makes Cube01 yellow and the pair Warm |
| [World_MaskedSize.usda](World_MaskedSize.usda) | Direct local scale masks an asset variant | Cube02 still selects Tall but resolves to scale one |
| [World_MaskedSelection.usda](World_MaskedSelection.usda) | Direct child selection masks a scene scenario | Cube01 remains Blue although the Normal branch selects Red |

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

- `000_SOURCE` retains original inputs; `010_ASS_USD/USD_Startpoint` retains imported USD. Both are unused by these procedural shapes.
- `010_ASS_USD/USD_Wrappers` holds published Cube/Cone packages; `Assemblies` holds DisplayPair; `MatLib` holds the asset material library; `Envs/OmniverseStandard/Resources` holds the supplied ground texture and sky HDR.
- `020_BASE_LYR` holds scene contributions. `040_DATA_LYRs` holds demo occurrence IDs and project context.
- `030_SIM_LYR` and `035_RUNTIME_LYR` reserve space for future published results and snapshots. Their READMEs do not compose any USD layers.
- `050_REVIEW` holds the two deliberate exceptions. `_contracts` stores the profile, ownership and expected results. `_pipeline_reports` stores evidence. `_workflows` reserves automation definitions.

The whole folder is the intended relocation unit. File references and the two texture paths point within it. `OmniPBR.mdl` and the supplied RTX/viewport schema behavior are resolved by the Omniverse installation. Relocation and renderer resource resolution have not been exercised as acceptance tests.

## Actual authoring evidence

The revised package contains 29 USD layers. The author ran with Python 3.13.3 and OpenUSD 26.08 and reopened the standard scene plus four companion entrypoints, with default time and an empty session. No composition errors were returned for those saved configurations. The recorded `/World` matrix is identity; all entries retain the supplied Z-up, centimetre scale, 60 fps, 0–100 range and bound viewport camera.

The recorded read-back found:

| Entry | Cube01 Finish / resolved material suffix | Cube02 Size / resolved scale |
|---|---|---|
| ROOT_example and Manual alias | Red / Looks/Red | Tall / (1, 1, 2) |
| Scenarios, Normal | Red / Looks/Red | Tall / (1, 1, 2) |
| MaskedSize | Red / Looks/Red | Tall / (1, 1, 1) |
| MaskedSelection, Normal | Blue / Looks/Blue | Tall / (1, 1, 2) |

See [build_manifest.json](_pipeline_reports/build_manifest.json) for file hashes, runtime and observations. This read-back covers the saved defaults and stage coordinates; it does not establish a full variant matrix, assembly behavior in all configurations, renderer appearance, physical simulation or UI persistence. No acceptance tests were run. [expected.json](_contracts/expected.json) records intended outcomes separately. The previous package and byte-exact supplied root are retained in the repository's `harness/evidence/standard_root_adoption` folder.

## Reproduce the authored fixture

From the parent repository root, with `uv` available:

```powershell
uv run --no-project --with usd-core==26.8 python tools/build_example.py --output examples/MyLayeredScene
```

The output must be a new or empty directory. The authoring script never overwrites an existing scene. It creates the USD, JSON and folder notes; this walkthrough and the repository-level design remain maintained documentation. The pinned [usd-core distribution](https://pypi.org/project/usd-core/26.8/) provides Python USD APIs, not an Omniverse installation or viewer.

Full variant checks, save/reopen behavior in the chosen application, relocation, material display and human acceptance are the next evaluation step. The example-specific JSON format is not yet a generic inspection or repair contract.
