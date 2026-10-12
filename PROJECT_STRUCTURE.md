# Project structure and the revised scene paradigm

## Selection and configuration naming

Store saved scene selections in the existing `050_OPINION_LYR/OpinLYR_Scene<SceneName>.usda`
by default. Use `OpinLYR_SceneDefault.usda` and
`OpinLYR_SceneColorVariants.usda` for the Essentials scenes. For intentionally
shared Opinion layers omit `Scene`, use `OpinLYR_<Purpose>.usda`, and document
their consumers.
Session is for transient previews. Add `020_BASE_LYR/ConfigLyr.usda` only for
independent reuse, ownership, versioning or switching; use `ConfigLyr_<Purpose>.usda`
when naming several configurations. Keep the extension lowercase. Author/team identifiers are optional and omitted by default. When used, append `.name.usda`, for example `OpinLYR_SceneDefault.jph2.usda`. ConfigLyr
selects existing asset variants; VariLyr defines variants/scenarios and their
conditional contents. Saved Opinion selections do not require promotion.
Existing examples using VariLyr for direct selections are legacy layouts, not a
requirement to create that layer in new scenes. This rule update does not rename
or migrate those files automatically.


**Asset grouping (CC-00b):** a team may store independent asset entrypoints beside each other. Essentials uses four files directly in `010_ASS_USD`. Use separate folders when resources, ownership, revision/publication or navigation benefit; no fixed threshold applies.

**Preview requirement (CC-00a):** all asset entrypoints load basic environment lighting for direct inspection, including leaves. A shared preview layer places `/Environment` beside the default asset prim; it introduces no asset-internal role stack. Scene references target only the asset prim. Package preview resources with portable paths.

## Scaffold and stopping rule (contract 0.2.1)

Self-contained leaves need only their asset file, including any intrinsic transforms, materials and variants. Composed assets/scenes start from the full conventional folder and role-layer scaffold; remove unused categories and contributions after tailoring it. Clear incoming arcs and stale authoring/lock metadata before removing a layer. Teaching examples keep the full folder catalogue at scene scope. Nested compositions use only their needed categories. Cube and Cone now end recursion in standalone files; DisplayPair keeps its assembly layers, and lofted wrappers retain their purposeful payload boundary. Older role diagrams below describe the available catalogue, not required leaf internals.

**Draft 0.1.1 · 2026-10-10.** This design develops Jan's scene-layer schematic, TutorialBuilder's VariantSetups exploration and the inspected `USD_GoodStart/_Generated_Test` folder. [CompositionContract.md](CompositionContract.md) owns the rules. The [local example](examples/01_LayeredScene/README.md) implements a bounded static profile; acceptance remains pending.

## Directory naming convention

Use these exact class folders at scene, asset and assembly scope:

```text
000_SOURCE/
010_ASS_USD/
020_BASE_LYR/
030_SIM_LYR/
035_RUNTIME_LYR/
040_DATA_LYR/
050_OPINION_LYR/
```

The `_LYR` suffix is singular for every layer class. DATA uses `040_DATA_LYR`; OPINION uses `050_OPINION_LYR`. Keep role filenames such as `DataLyr.usda` and `OpinLYR_default.usda` unchanged. Folder numbers classify storage; each root's `subLayers` list declares strength. These names also apply to generators, relative paths, authoring-target metadata and starter packages. [CC-26](CompositionContract.md#naming-and-classification) owns this convention.

## The authoring model

Open `SceneROOT_Example.usda`, the supplied Omniverse starting scene, with Opinion selected and editable and persistent work/source layers locked. The supplied environment, viewport camera and render specs remain its declared application baseline. When persisting a project change, deliberately unlock and edit the contribution that owns it. GeoLyr links published assets; TransLyr places occurrences; VariLyr selects configurations and owns scene scenarios. Material roles remain available when the scene has additional material responsibilities. Each referenced assembly or asset repeats this separation for its own decisions.

```mermaid
%%{init: {"flowchart": {"wrappingWidth": 380, "nodeSpacing": 22, "rankSpacing": 28}}}%%
flowchart LR
    accTitle: OpenUSD GoodStart Composition Contract 0.1.1 - Root, scene stack and reusable sources
    accDescr: Left to right, the root assembles a vertical scene layer stack with GeoLyr at the bottom. Reusable assets, assemblies and materials retain their own implementation and variant context.
    %% Connect the column subgraphs, keeping their internal TB layout intact.
    subgraph ENTRY["ROOT + AUTHORING · 0.1.1"]
        direction TB
        Session["Opinion Layer<br/>Default editable target<br/>Work/source layers start locked"]
        R["SceneROOT_Example.usda<br/>Stage metadata and sublayer assembly<br/>SceneROOT_Manual is an independent manual root"]
        Startup["Supplied Omniverse baseline in the root<br/>Environment · Render · viewport cameras<br/>Z-up · centimetres · identity World · 60 fps"]
        Session ~~~ R
        R ~~~ Startup
        Review["Optional OPINION · 050_OPINION_LYR<br/>ReviewLyr · explicit experiments above the base stack<br/>Declare owner, purpose and removal route"]
        Startup ~~~ Review
    end

    subgraph STACK["SCENE LAYER CLASSES"]
        direction TB
        RT["RUNTIME LAYER · 035_RUNTIME_LYR<br/>RuntimeLyr · deliberate operational snapshots<br/>Live values may remain in session / external storage<br/>Declare writer authority and persistence"]
        S["SIM LAYER · 030_SIM_LYR<br/>SimLyr · published solver results<br/>Record scenario, solver, time and provenance"]
        D["DATA LAYERS · 040_DATA_LYR<br/>DataLyr · project identity and context<br/>IdentityLyr · scoped occurrence / external IDs<br/>ContextLyr · installation context<br/>Bindings resolve identities to explicit targets<br/>UNSMappingLyr · optional integration mappings"]
        BASE["BASE LAYER · 020_BASE_LYR<br/>MatLyr · scene resources and assignments; respect asset Finish<br/>TransLyr · ordinary placement on occurrence parents<br/>Opinion · saved selections<br/>ConfigLyr · optional managed selections<br/>VariLyr · Layout scenarios<br/>Relative adjustments stay in their scenario branch<br/>Optional: EnvLyr · LightLyr · CamLyr · RenderLyr<br/>AnimLyr · PhysicsLyr · RigLyr as the profile requires<br/>GeoLyr · hierarchy and asset references · BOTTOM / WEAKEST<br/>Linked packages retain their own implementation"]
        RT ~~~ S
        S ~~~ D
        D ~~~ BASE
    end

    subgraph SRC["ASSET USD · 010_ASS_USD"]
        direction TB
        B["Nested assembly interface · DisplayPair<br/>Own GeoLyr + TransLyr + VariLyr<br/>Palette variants coordinate child Finish selections<br/>Scene selects the assembly's public interface"]
        A["Published asset interfaces · Cube and Cone<br/>Own GeoLyr + TransLyr + MatLyr + VariLyr<br/>Source identity belongs at the asset/component scope<br/>Asset-owned geometry, intrinsic transforms and materials<br/>Reusable Size / Finish definitions remain in the asset"]
        Library["Shared material library · Palette_v001<br/>Reusable material definitions and shader values<br/>Asset MatLyr references the required materials<br/>Library revisions are adopted deliberately"]
        Context["Preserve owner and variant context<br/>Asset / assembly changes belong in that package<br/>Variant-dependent values stay in their owning branch<br/>Scene choices do not duplicate asset implementations"]
        B -->|"assembly GeoLyr references Cube and Cone"| A
        A -->|"asset MatLyr references shared definitions"| Library
        Library ~~~ Context
    end

    ENTRY -->|"Root composes sibling sublayers"| STACK
    STACK -->|"GeoLyr references assets and assemblies"| SRC
    STACK -.->|"VariLyr selects published controls"| SRC
    STACK -.->|"Scene MatLyr links materials when needed"| SRC

    classDef root fill:#fde8df,stroke:#d99b84,color:#17212b,stroke-width:2px
    classDef layer fill:#dceef9,stroke:#91bfd8,color:#17212b,stroke-width:1.5px
    classDef optional fill:#f4f9fc,stroke:#91bfd8,color:#334155,stroke-width:1.5px,stroke-dasharray:6 4
    classDef base fill:#dceef9,stroke:#1685bd,color:#17212b,stroke-width:3px
    classDef asset fill:#ffffff,stroke:#9db9c8,color:#17212b,stroke-width:1.5px
    classDef note fill:#f5f8fa,stroke:#cbd6dc,color:#334155
    class R root
    class D layer
    class RT,S,Review optional
    class BASE base
    class B,A,Library asset
    class Session,Startup,Context note
    style STACK fill:#f8fcff,stroke:#84c83d,stroke-width:3px
```

Read the diagram **left to right**: the root assembles the scene layer stack, which uses reusable assets, assemblies and materials. Inside the middle column, **GeoLyr is at the bottom**, beneath the other scene contributions. Numbered solid rows give the active standard-scene order: DataLyr → TransLyr → VariLyr → GeoLyr. Dashed rows retain the optional work roles and the explicit Review role; the profile declares their order when included.

The root's sublayers are siblings. GeoLyr references Cube, Cone and DisplayPair; TransLyr places occurrences; VariLyr selects published controls and keeps scenario-relative adjustments in their branches. DisplayPair's own GeoLyr references Cube and Cone, and its Palette variants coordinate child Finish choices. Cube/Cone keep their geometry, intrinsic transforms, materials and Size/Finish implementations in their own package. Their simple material definitions are inline; scene/assembly material libraries may still be shared. The supplied environment/render/camera content stays in the root under CC-01. See the [composition contract](CompositionContract.md#composition-memory-chart) for the corresponding ownership and persistence guidance.

## Changes from the two predecessors

| Observed predecessor | New project decision | Reason / rule |
|---|---|---|
| Screenshot: GeoLayer links assets and places them | GeoLyr owns links/hierarchy; TransLyr owns ordinary placement | Preserve independent transform ownership, CC-02/06 |
| Screenshot: Opinion_Jan holds experiments | Named ReviewLyr exceptions, composed only by review entrypoints | Record owner, reason, affected fields and disposition, CC-20/23 |
| Screenshot: MatLayer links shared material libraries | Asset MatLyr imports its required materials; supplied root retains its OmniPBR grid material | Asset Finish retains its binding authority, CC-10/15; CC-01 template exception |
| Screenshot: additional physics/environment/light/animation lanes | Explicit role catalogue, instantiated when there is content | Avoid placeholder layers implying active capabilities, CC-20/21 |
| VariantSetups C and G: parent placement and referenced variants | Placement → Adjustment → Asset; recursively owned asset layers | Separate ordinary, scene-conditional and intrinsic transforms, CC-03/06/07 |
| VariantSetups H: additional assembly reference boundary | Reusable DisplayPair assembly with its own placement and Palette interface | Demonstrate genuine assembly ownership, CC-13/14 |
| Generated `ASS_LYR` currently contains native mesh and transforms | Scene GeoLyr references authored packages | Native geometry belongs to the asset; transforms to its TransLyr |
| Generated numbered storage lanes | Keep 000, 010, 020, 030, 035, 040; add 050 review | Preserve familiar storage while making lifecycle explicit, CC-24 |
| Generated `USD_Startpoint` and `USD_Wrappers` slots | Keep import evidence separate from owned package layers | Explicit source boundary, CC-25 |
| Generated root is Y-up, `/world`, centimetres | Preserve the supplied ROOT_example: Z-up, `/World`, centimetres, 60 fps, 0–100 | The user-selected Omniverse scene now establishes startup conventions |
| Earlier example had a custom Overview camera, ground and lights | Keep the supplied top-level Environment/Render and OmniverseKit viewport cameras | Remove alternate starting conditions; preserve identity world coordinates |
| Generated root carries Kit locks and a root edit target | Work/source layers locked; scoped helper selects Opinion | Opinion is the default working target; reviewed destinations follow ownership |
| `_comfyui_workflows` | `_workflows`, with optional application subfolders | Keep the base package usable without a selected pipeline runtime |

The inspected setup script and its generated output are separate evidence. Script comments about locking or default asset locations do not establish what is in the saved scene. This example is newly authored; predecessor files remain historical evidence.

## Storage layout

Use Root for entrypoint naming (`SceneROOT_<Purpose>.usda`) and scene for the composed result. All active scene entrypoints follow CC-26. Diagram class labels map to the [contract classification table](CompositionContract.md#naming-and-classification): ASSET USD, BASE, SIM, RUNTIME, DATA and REVIEW. These classify package/layer purpose; mixed-case names inside them identify technical roles. No additional aggregate layers are implied.

The example folder is the portable unit. The complete folder includes all USD dependencies; moving an individual root does not preserve its relative dependencies. Numeric prefixes organize storage and carry **no USD strength semantics**.

```text
examples/01_LayeredScene/
  SceneROOT_Example.usda                 standard Omniverse root + direct scene selections
  SceneROOT_Manual.usda                 independent manual root matching ROOT_example
  SceneROOT_Scenarios.usda              scene Layout variant
  SceneROOT_MaskedSize.usda             deliberate property conflict
  SceneROOT_MaskedSelection.usda        deliberate selection conflict
  Open_In_Kit.ps1                   launch with protected layers and Opinion authoring
  000_SOURCE/                      retained CAD/DCC originals; unused here
  010_ASS_USD/
    USD_Startpoint/                retained imported USD; unused here
    USD_Wrappers/
      Cube/AssetROOT_Cube.usda               published asset entrypoint
        020_BASE_LYR/{Geo,Trans,Mat,Vari}Lyr.usda
      Cone/AssetROOT_Cone.usda
        020_BASE_LYR/{Geo,Trans,Mat,Vari}Lyr.usda
    Assemblies/
      DisplayPair/AssetROOT_DisplayPair.usda
        020_BASE_LYR/{Geo,Trans,Vari}Lyr.usda
    MatLib/Palette_v001.usda        shared material definitions
    Envs/OmniverseStandard/Resources/ supplied sky HDR and ground texture
    tex/                           shared texture slot; unused here
  020_BASE_LYR/
    GeoLyr.usda                    occurrence hierarchy and references
    TransLyr.usda                  occurrence placement only
    VariLyr.usda                   direct selections, manual mode only
    VariLyr_Scenarios.usda          Layout definitions/selections, scenario mode only
  030_SIM_LYR/                     reserved; no result layer composed
  035_RUNTIME_LYR/                 reserved; no live state or snapshot composed
  040_DATA_LYR/
    DataLyr.usda                   thin data aggregate
    Data/IdentityLyr.usda
    Data/ContextLyr.usda
  050_OPINION_LYR/
    MaskedSize/ReviewLyr.usda
    MaskedSelection/ReviewLyr.usda
  _contracts/                     profile, ownership and expected outcomes
  _pipeline_reports/              build evidence
  _workflows/                     automation definitions when needed
```

Reserved directories contain a short README explaining their use. Empty USD contributions are not added to the stage. Physics, animation, rigging, ports, behaviors and sensors can be added under their owning package when a profile needs them. The catalogue does not require every project to contain every role.

## Package and occurrence boundaries

```text
/World/Cube02                         scene TransLyr: base placement
  /Adjustment                        scene Layout branch: relative offset
    /Asset                           scene GeoLyr: reference to AssetROOT_Cube.usda
      [Size, Finish public controls] asset VariLyr: intrinsic alternatives
      /Geometry                      asset GeoLyr: cube; TransLyr: center at z=50
      /Looks                         asset MatLyr: references to shared materials
```

The cube's Size branch owns scale and its complete operation order on Asset. Its fixed geometry-centering transform belongs to the cube's TransLyr. Scene placement and adjustment affect different prims, so they combine through hierarchy. A direct scale on Asset would compete with Size even if placed in a differently named scene layer.

The DisplayPair assembly follows the same arrangement for CubePart and ConePart. Its Palette variant selects child Finish controls. The scene selects Palette on the assembly interface; it does not reach through the assembly to recolor private meshes. The original teaching roots use regular references. Lofted adds public asset interfaces and payload ContentsLyr aggregates; the Instanced roots additionally use native shape instancing. The assembly stays non-instanceable. Wave, Spiral and Rings own separate TransLyr/VariLyr/Opinion layers while sharing the Instanced GeoLyr and source packages.

The material library is pinned by a versioned bundled filename. Each consumer references a material subtree. No scene or asset layer repeats the library's shader inputs. A new material revision requires an explicit adoption decision; these paths are not a production asset resolver or publishing service.

## Strength and edit destinations

Both baseline scene roots list, strongest first:

1. DataLyr (IdentityLyr before ContextLyr).
2. TransLyr.
3. Exactly one VariLyr: direct selections or scene scenarios.
4. GeoLyr.

The supplied root's environment/render/viewport specs remain local root content by the explicit CC-01 application-template exception. They do not author transforms on `/World` or the example occurrences. The earlier presentation layers and Ground package were archived outside the active example. Every scene entrypoint owns its startup content and directly lists its work layers. Manual and review entrypoints never sublayer another scene root; review layers sit directly above the baseline work layers.

Most contributions own different fields. GeoLyr at the bottom is this project's scene convention; the profile declares the order above it. Asset roots likewise list VariLyr, MatLyr where needed, TransLyr where needed, then GeoLyr. Review entrypoints compose their exception above the corresponding baseline work layers.

| Intended edit | Destination | Context |
|---|---|---|
| Move Cube02 in the scene | Scene TransLyr, `/World/Cube02` | Unconditional base placement |
| Choose Cube02 Finish in manual mode | Scene VariLyr, `/World/Cube02/Adjustment/Asset` | Direct selection metadata |
| Choose a scene Layout | Scenarios/VariLyr, `/World` | Layout selection metadata |
| Change the Exploded offset | Scenarios/VariLyr, Cube02/Adjustment | Inside Layout=Exploded |
| Change what Tall means for every cube | Cube leaf entrypoint, Size variant | Inside Size=Tall; asset revision decision |
| Change distance between pair components | DisplayPair TransLyr | Assembly-owned placement |
| Change the shared Blue shader | Material-library revision | Library-owned definition |
| Add a temporary masked-scale experiment | Dedicated ReviewLyr | Declared exception with removal route |

The table gives reviewed destinations. Experiments start in the declared editable Opinion layer; persistent work/source layers are locked. Saving Opinion retains experiments. The launcher selects the target and keeps the root writable for Kit settings; it does not classify, promote or save edits. Choose the correct role and variant branch when promoting accepted fields.

## Reproduction and evidence

The repository includes a bounded [USD-aware authoring script](tools/build_example.py). It creates this fixture in a new or empty folder, refuses to overwrite existing content, and records a default-entrypoint read-back. It does not inspect arbitrary projects or repair existing opinions. See the [example guide](examples/01_LayeredScene/README.md) for the actual command and recorded results.

The JSON contracts are example-specific drafts. They make owner, role, context, dependency, order and expected result reviewable; no generic validator enforces them yet. Full variant coverage, relocation and host UI acceptance remain follow-up work.

## Recursive asset packages

Keep scene `020_BASE_LYR` flat: use role filenames with `_Starter` or `_Scenarios` purpose suffixes for alternative contributions. These filenames distinguish independent work layers without nesting class folders further. Sublayer lists still declare actual strength.

Cube, Cone and DisplayPair repeat the same numbered class folders as the scene. Each has an AssetROOT_<Name>.usda, owned roles in 020_BASE_LYR and its own Opinion in 050_OPINION_LYR. Other classes are reserved with notes. See CC-25/26 for the distinction between scene entrypoints, reusable packages and preserved third-party imports. Object type does not change this convention: a building used in a city is an asset.

## Scalability samples

`SceneROOT_Lofted.usda` and the four `SceneROOT_Instanced*.usda` roots directly compose scene role layers. `CubeLofted`, `ConeLofted` and `DisplayPairLofted` packages repeat the BASE/REVIEW structure for their active roles. Their `AssetROOT_*Lofted.usda` files expose empty variant declarations and payload `020_BASE_LYR/ContentsLyr.usda`. Each shape ContentsLyr loads its standalone leaf entrypoint, preserving one geometry/material/variant implementation. DisplayPairLofted's own GeoLyr links the lofted shapes; its original placement and Palette definitions remain shared. Source demo Opinion layers are excluded behind these payloads; each published interface has its own Opinion above the payload.

The `_workflows/arrange_instances.py` driver maps a normalized JSON signal to independently saved Wave/Spiral/Rings scenes. Only instance placement and public selection metadata vary. Prototype counts depend on composed configurations, not just source-file counts. See the sample README and `_contracts/scalability.json` for scope and acceptance requirements.

## Animated point-instancing profile

`SceneROOT_MotionGraphics.usda` is a separate direct root with its own Opinion,
DATA declaration, Geo/Vari/Trans/Cam roles and baked AnimLyr. It uses 1,024 stable
point IDs and six prototype reference sites, sharing the existing CubeLofted and
ConeLofted implementations and Palette materials. It does not repeat the five
teaching objects. Per-point motion belongs to AnimLyr; ordinary whole-cloner
placement belongs to TransLyr.

`040_DATA_LYR/Controls/motion_graphics.json` supplies validated controls through
the DATA-declared path. `_workflows/motion_graphics_core.py` is shared by the
offline author/baker and the opt-in Kit runtime. Live output is an anonymous
RUNTIME sublayer under Session, not an automatically saved file in
`035_RUNTIME_LYR`. The runtime owns only instancer arrays and derived bounds;
Opinion remains the user's authoring target. Removal restores the saved animation.
The profile records timing, input failure handling, precedence and pending Kit
acceptance. The script-created `Motion Graphics Controls` panel uses the same
validation and ranges, writes only the DATA JSON on explicit Apply & Save, and
retains prior bytes. It shows persistent input errors and detects stale drafts.
It does not bake or save USD. Panel startup and control saves were observed in
Kit; the user reported successful operation. Lifecycle fixes and full acceptance
remain pending.

## Standalone Essentials package

`examples/02_USDEssentials_Minimal/` repeats this layout at scene and asset scope with only one cube, one cone and two colors. Its two roots demonstrate fixed scene bindings and asset-owned Color variants. See its README and `_contracts/profile.json`. Reserved categories do not require empty composed layers. The portable starter bundles this self-contained package as `USDEssentials_Minimal/`.

## Shared resources and optional archives

CC-00c/00d permit adjacent asset files sharing MatLib and tex/textures folders.
Private resources may stay with their asset. Cleanup inventories all relevant
variants, payloads and consumers before re-anchoring dependencies and removing
unused files. Ordinary ZIP is an unpack-before-use transport; USDZ is optional
runtime delivery, requiring supported dependencies and consumer compatibility.
Retain editable originals. Packaging each leaf independently may duplicate shared
resources; teams decide the delivery boundary. No packaging or performance result
is implied by the convention.
