# Project structure and the revised scene paradigm

**Draft 0.2 · 2026-10-10.** This design develops Jan's scene-layer schematic, TutorialBuilder's VariantSetups exploration and the inspected `USD_GoodStart/_Generated_Test` folder. [CompositionContracts.md](CompositionContracts.md) owns the rules. The [local example](examples/01_LayeredScene/README.md) implements a bounded static profile; acceptance remains pending.

## The authoring model

Open `ROOT_example.usda`, the supplied Omniverse starting scene, with all persistent layers locked and the session layer selected for temporary edits. The supplied environment, viewport camera and render specs remain its declared application baseline. When persisting a project change, deliberately unlock and edit the contribution that owns it. GeoLyr links published assets; TransLyr places occurrences; VariLyr selects configurations and owns scene scenarios. Material roles remain available when the scene has additional material responsibilities. Each referenced assembly or asset repeats this separation for its own decisions.

```mermaid
flowchart LR
    Root["ROOT_example.usda / World_Scenarios.usda"]
    subgraph Scene["Scene-owned contributions — edit the responsible layer"]
        Geo["GeoLyr — hierarchy and asset references"]
        Trans["TransLyr — occurrence placement"]
        Vari["VariLyr — selections OR scene scenarios"]
        Other["DataLyr — occurrence identity and context"]
    end
    Root -->|sublayer| Geo
    Root -->|sublayer| Trans
    Root -->|sublayer| Vari
    Root -->|sublayer| Other
    Geo -->|reference| Cube["Cube public interface"]
    Geo -->|reference| Cone["Cone public interface"]
    Geo -->|reference| Pair["DisplayPair public interface"]
    Pair -->|owned GeoLyr references| Cube
    Pair -->|owned GeoLyr references| Cone
    Cube -->|owned MatLyr references| Library["Palette_v001 material library"]
    Cone -->|owned MatLyr references| Library
    Root -->|"supplied root specs"| Startup["Omniverse Environment · Render · viewport cameras"]
```

Arrows show composition dependencies, not strength order or movement of edits into the source. Selection opinions target the composed public asset prim. Referencing an asset does not require changing its source file when configuring a scene occurrence.

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
| Generated root carries Kit locks and a root edit target | Persistent layer locks plus a scoped Kit helper selecting Session Layer | Session is the default working target; durable destinations still follow ownership |
| `_comfyui_workflows` | `_workflows`, with optional application subfolders | Keep the base package usable without a selected pipeline runtime |

The inspected setup script and its generated output are separate evidence. Script comments about locking or default asset locations do not establish what is in the saved scene. This example is newly authored; predecessor files remain historical evidence.

## Storage layout

The example folder is the portable unit. The complete folder includes all USD dependencies; moving an individual root does not preserve its relative dependencies. Numeric prefixes organize storage and carry **no USD strength semantics**.

```text
examples/01_LayeredScene/
  ROOT_example.usda                 standard Omniverse root + direct scene selections
  World_Manual.usda                 compatibility alias of ROOT_example
  World_Scenarios.usda              scene Layout variant
  World_MaskedSize.usda             deliberate property conflict
  World_MaskedSelection.usda        deliberate selection conflict
  Open_In_Kit.ps1                   launch with locked layers and session authoring
  000_SOURCE/                      retained CAD/DCC originals; unused here
  010_ASS_USD/
    USD_Startpoint/                retained imported USD; unused here
    USD_Wrappers/
      Cube/Cube.usda               published asset entrypoint
        layers/{Geo,Trans,Mat,Vari}Lyr.usda
      Cone/Cone.usda
        layers/{Geo,Trans,Mat,Vari}Lyr.usda
    Assemblies/
      DisplayPair/DisplayPair.usda
        layers/{Geo,Trans,Vari}Lyr.usda
    MatLib/Palette_v001.usda        shared material definitions
    Envs/OmniverseStandard/Resources/ supplied sky HDR and ground texture
    tex/                           shared texture slot; unused here
  020_BASE_LYR/
    GeoLyr.usda                    occurrence hierarchy and references
    TransLyr.usda                  occurrence placement only
    VariLyr.usda                   direct selections, manual mode only
    Scenarios/VariLyr.usda          Layout definitions/selections, scenario mode only
  030_SIM_LYR/                     reserved; no result layer composed
  035_RUNTIME_LYR/                 reserved; no live state or snapshot composed
  040_DATA_LYRs/
    DataLyr.usda                   thin data aggregate
    Data/IdentityLyr.usda
    Data/ContextLyr.usda
  050_REVIEW/
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
    /Asset                           scene GeoLyr: reference to Cube.usda
      [Size, Finish public controls] asset VariLyr: intrinsic alternatives
      /Geometry                      asset GeoLyr: cube; TransLyr: center at z=50
      /Looks                         asset MatLyr: references to shared materials
```

The cube's Size branch owns scale and its complete operation order on Asset. Its fixed geometry-centering transform belongs to the cube's TransLyr. Scene placement and adjustment affect different prims, so they combine through hierarchy. A direct scale on Asset would compete with Size even if placed in a differently named scene layer.

The DisplayPair assembly follows the same arrangement for CubePart and ConePart. Its Palette variant selects child Finish controls. The scene selects Palette on the assembly interface; it does not reach through the assembly to recolor private meshes. The example uses regular references, not native USD instancing or payloads.

The material library is pinned by a versioned bundled filename. Each consumer references a material subtree. No scene or asset layer repeats the library's shader inputs. A new material revision requires an explicit adoption decision; these paths are not a production asset resolver or publishing service.

## Strength and edit destinations

Both baseline scene roots list, strongest first:

1. DataLyr (IdentityLyr before ContextLyr).
2. TransLyr.
3. Exactly one VariLyr: direct selections or scene scenarios.
4. GeoLyr.

The supplied root's environment/render/viewport specs remain local root content by the explicit CC-01 application-template exception. They do not author transforms on `/World` or the example occurrences. The earlier presentation layers and Ground package were archived outside the active example. `World_Manual.usda` sublayers the standard root as a compatibility alias; it has no independent scene content.

Most contributions own different fields. This ordering documents the example; it is not a universal recommendation. Asset roots list VariLyr, MatLyr where needed, TransLyr where needed, then GeoLyr. Review entrypoints compose their exception above the corresponding baseline root.

| Intended edit | Destination | Context |
|---|---|---|
| Move Cube02 in the scene | Scene TransLyr, `/World/Cube02` | Unconditional base placement |
| Choose Cube02 Finish in manual mode | Scene VariLyr, `/World/Cube02/Adjustment/Asset` | Direct selection metadata |
| Choose a scene Layout | Scenarios/VariLyr, `/World` | Layout selection metadata |
| Change the Exploded offset | Scenarios/VariLyr, Cube02/Adjustment | Inside Layout=Exploded |
| Change what Tall means for every cube | Cube package VariLyr | Inside Size=Tall; asset revision decision |
| Change distance between pair components | DisplayPair TransLyr | Assembly-owned placement |
| Change the shared Blue shader | Material-library revision | Library-owned definition |
| Add a temporary masked-scale experiment | Dedicated ReviewLyr | Declared exception with removal route |

The table gives persistent destinations. By default, temporary edits go into the session while all persistent layers are protected. The supplied launcher runs a scoped Kit startup helper because a fresh anonymous session layer has no portable saved identifier. Deliberate persistence requires unlocking the rightful layer and choosing its edit target. Scene scenario contents also require the correct variant edit context. This helper sets the opening state; it does not classify or route individual edits.

## Reproduction and evidence

The repository includes a bounded [USD-aware authoring script](tools/build_example.py). It creates this fixture in a new or empty folder, refuses to overwrite existing content, and records a default-entrypoint read-back. It does not inspect arbitrary projects or repair existing opinions. See the [example guide](examples/01_LayeredScene/README.md) for the actual command and recorded results.

The JSON contracts are example-specific drafts. They make owner, role, context, dependency, order and expected result reviewable; no generic validator enforces them yet. Full variant coverage, relocation and host UI acceptance remain follow-up work.
