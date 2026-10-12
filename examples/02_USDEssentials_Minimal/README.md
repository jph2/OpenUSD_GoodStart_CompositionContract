# USD Essentials — one cube, one cone, two colors

**Folder convention:** layer classes use singular `_LYR`, including `040_DATA_LYR` and `050_REVIEW_LYR`, at scene and asset scope. Role filenames retain their existing casing (`DataLyr.usda`, `OpinLYR_default.usda`). Folder numbering does not set composition strength.

Two small scenes use the same folder, ownership and naming rules as the composition contracts. **Z-up · centimetres · 60 fps.** Keep this entire folder together when copying it.

## Coordinates and environment ownership

Both `SceneROOT_` entrypoints and all four Cube/Cone asset entrypoints declare
Z-up and nominal centimetre units (`metersPerUnit = 0.01`). The composed Cone
also declares its geometric axis as Z. The two scene roots contain the supplied
Omniverse `Environment` (ground, lighting, render settings and viewport cameras)
under the CC-01 template exception.

All four Cube and Cone asset roots also compose the shared `Environment.usda`
sublayer at the stage root, alongside the `/Asset` default prim. This makes the
supplied ground and lighting visible when any asset entrypoint is opened
directly. Scene GeoLyr references each asset's `/Asset` default prim, so that
sibling `/Environment` is not imported into the scene. The SceneROOT continues
to own its own Omniverse environment under the CC-01 template exception. No
Y-to-Z conversion is needed for these current files. This remains a
centimetre-based teaching profile, not metre-based SimReady or general
production acceptance.

## Choose a lesson

1. **[Fixed materials](#fixed-materials):** open `SceneROOT_USDEssentials.usda`. Learn sublayers, references, transforms and material bindings.
2. **[Color variants](README_ColorVariants.md):** open `SceneROOT_USDEssentials_ColorVariants.usda`. Change each shape independently between Red and Blue.

## Open and author

Open either root with **File > Open** in Composer and frame `/World`. Both roots use the supplied `defaultscene.usda` Omniverse baseline: ground, sky and distant light, render settings and viewport cameras. Its contents are authored directly in each root; `defaultscene.usda` is a preserved template input, not a nested scene layer.

For the full Opinion-authoring policy, launch your installed Kit application with:

```powershell
.\Open_In_Kit.ps1 -Scene USDEssentials
# Second lesson:
.\Open_In_Kit.ps1 -Scene USDEssentials_ColorVariants
```

Each scene and asset root stores its own Opinion authoring target and `omni_layer.locked` map. The map locks every composed persistent layer except that root's declared Opinion layer. The Kit root remains writable for Kit's camera and authoring metadata, as required by CC-01. The launcher starts a new Kit process, detects an installed application's paths or accepts `-KitExe` and `-AppConfig`, then runs `_workflows/kit/session_defaults.py` to select the scene's Opinion layer, disable automatic authoring and enforce the persistent-layer locks in memory. It installs nothing, changes no Windows permissions or execution policy, and does not save USD files. Kit may write its normal logs, caches and preferences.

If you already opened the scene, run this in Kit's Script Editor, substituting your copied folder's path:

```python
import runpy
runpy.run_path(r"E:/your/project/02_USDEssentials_Minimal/_workflows/kit/session_defaults.py")
```

Directly opening a USDA does not execute Python. Its root metadata declares the authoring target and saved lock map; run the helper in Kit to select Opinion, disable automatic authoring and enforce the lock policy for the current session. Experiment in Opinion. To deliberately teach a saved role edit, unlock that layer and select it explicitly, then return to Opinion. Promote accepted edits to their rightful owner and remove the superseded Opinion values.

## Folder and layer plan

```text
02_USDEssentials_Minimal/
|-- defaultscene.usda                   supplied baseline template (unchanged)
|-- SceneROOT_USDEssentials.usda
|-- SceneROOT_USDEssentials_ColorVariants.usda
|-- 000_SOURCE/                         retained inputs (unused)
|-- 010_ASS_USD/
|   |-- Envs/OmniverseStandard/
|   |   |-- Environment.usda           direct-open asset preview environment
|   |   `-- Resources/                 portable HDR and grid texture
|   |-- MatLib/Palette_v001.usda         shared Yellow, Green, Red and Blue
|   `-- USD_Wrappers/
|       |-- Cube/
|       |   |-- AssetROOT_Cube.usda
|       |   |-- AssetROOT_Cube_ColorVariants.usda
|       |   |-- 000_SOURCE/             reserved
|       |   |-- 010_ASS_USD/            reserved
|       |   |-- 020_BASE_LYR/
|       |   |   |-- GeoLyr.usda         one Cube geometry
|       |   |   |-- TransLyr.usda       intrinsic centering
|       |   |   |-- MatLyr.usda         palette reference
|       |   |   `-- VariLyr.usda        Color binding definitions
|       |   |-- 030_SIM_LYR/            reserved
|       |   |-- 035_RUNTIME_LYR/        reserved
|       |   |-- 040_DATA_LYR/          reserved
|       |   `-- 050_REVIEW_LYR/             separate Opinion per entrypoint
|       `-- Cone/                      repeats the Cube package structure
|-- 020_BASE_LYR/
|   |-- GeoLyr.usda                     plain asset references
|   |-- GeoLyr_ColorVariants.usda       color asset references
|   |-- TransLyr.usda                   occurrence placement, shared
|   |-- MatLyr.usda                     fixed lesson bindings
|   `-- VariLyr_ColorVariants.usda      scene Color selections
|-- 030_SIM_LYR/                        reserved
|-- 035_RUNTIME_LYR/                    reserved
|-- 040_DATA_LYR/                      reserved
|-- 050_REVIEW_LYR/
|   |-- OpinLYR_default.usda
|   `-- OpinLYR_ColorVariants.usda
|-- _contracts/profile.json             ownership + exact stack order
|-- _pipeline_reports/                  inspection evidence location
|-- _workflows/kit/session_defaults.py
`-- Open_In_Kit.ps1
```

The numbered folders classify roles; **the root's `subLayers` list sets strength**. Unused categories contain notes, not empty composed layers. Scene and asset roots repeat the same organization. A plain asset root composes Opinion → Trans → Geo; its color entrypoint composes Opinion → Vari → Mat → Trans → Geo. Both reuse the same geometry and intrinsic transform files.

## Fixed materials

**Goal:** trace readable USDA opinions into one composed result. Start on the right: GeoLyr references the Cube and Cone packages. Scene TransLyr places their occurrence parents; asset TransLyr centers each shape above its local base. Scene MatLyr references the shared palette and binds the Cube yellow and Cone green. The root combines these sibling layers, with GeoLyr weakest. Opinion is the strongest experimental layer.

```mermaid
flowchart LR
    R["SceneROOT_USDEssentials.usda"]
    subgraph STACK["Scene sublayers — strongest first"]
        direction TB
        O["1 Opinion — default authoring"]
        M["2 MatLyr — palette and fixed bindings"]
        T["3 TransLyr — occurrence placement"]
        G["4 GeoLyr — asset references, weakest"]
        O ~~~ M
        M ~~~ T
        T ~~~ G
    end
    subgraph SOURCES["Reusable sources"]
        direction TB
        C["AssetROOT_Cube — Opinion / Trans / Geo"]
        N["AssetROOT_Cone — Opinion / Trans / Geo"]
        P["Palette_v001 — Yellow, Green, Red and Blue"]
    end
    B["Root baseline: ground, lights, render and viewport cameras"]
    R --- B
    R -->|sublayers| STACK
    STACK -->|GeoLyr references| C
    STACK -->|GeoLyr references| N
    STACK -->|MatLyr references| P
```

### Same USD data, different views

| View | What it shows |
|---|---|
| USDA text | Opinions authored in one layer: prims, attributes, relationships and composition arcs |
| Layer panel | Root and role files contributing opinions, plus the selected authoring destination |
| Stage tree | The composed prim namespace after resolving the layers and references |
| Viewport | The rendered result of the composed data |

```text
/World
|-- Cube01                     scene placement (TransLyr)
|   `-- Adjustment             reserved contextual adjustment boundary
|       `-- Asset              reference to AssetROOT_Cube
|           `-- Geometry       Cube (asset GeoLyr + intrinsic TransLyr)
|-- Cone01
|   `-- Adjustment
|       `-- Asset              reference to AssetROOT_Cone
|           `-- Geometry       Cone
`-- Looks                      palette reference (scene MatLyr)
    |-- Yellow
    |-- Green
    |-- Red
    `-- Blue
```

A sublayer combines opinions in the same namespace. A reference brings an asset's default prim under a scene reference site. A material binding is a **relationship**, not another composition arc. The scene root contains stage metadata, its sublayer list and the supplied Omniverse environment/render/camera baseline under the CC-01 template exception. It does not nest another scene root. Each asset root has a separate direct-open `/Environment` preview sibling; referencing its `/Asset` default prim does not bring that sibling into the scene. The two teaching shapes remain in their role layers. The baseline ground has its own Grid material; the fixed-material lesson uses Yellow and Green, while the Color variant lesson keeps Red and Blue.

### Small exercises

- Move `/World/Cube01` in Opinion and inspect the resulting translate opinion. Its saved placement belongs in scene TransLyr; intrinsic centering belongs in the asset's TransLyr.
- Deliberately mute scene MatLyr to see what the bindings contribute; restore it afterwards.
- Open GeoLyr and follow its relative asset paths. Each asset root then lists its own sibling role layers.
- Continue with [Color variants](README_ColorVariants.md): the material owner changes, while geometry and placement stay shared.

No simulation, data mappings, payloads, instancing or animation are needed here. This is an introductory contract profile, not a claim of complete contract conformance or Kit acceptance. Developed with AI assistance; human review remains required.

The bundled HDR and grid texture use relative paths. `OmniPBR.mdl` remains an Omniverse-provided shader dependency. Other USD viewers may not reproduce that ground material. `defaultscene.usda` retains its original resource paths as source evidence; open the `SceneROOT_` files for the portable lessons.
