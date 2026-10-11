"""Read saved USD scenes and document their composition; no acceptance tests."""
from pathlib import Path
import argparse
import subprocess
from pxr import Sdf, Usd

PACKAGE = Path(__file__).resolve().parents[1] / 'examples/01_LayeredScene'
START = '<!-- BEGIN EXACT SCENE GRAPHS -->'
END = '<!-- END EXACT SCENE GRAPHS -->'
MERMAID_LAYOUT = '%%{init: {"htmlLabels": false, "themeVariables": {"fontFamily": "Arial, sans-serif"}, "flowchart": {"htmlLabels": false, "padding": 20, "nodeSpacing": 200, "rankSpacing": 35, "diagramPadding": 20}}}%%'
# Mermaid 11.12.x can reject <br/> newlines in its SVG-label wrapping path.
# Use HTML labels inline; retain the SVG-export layout for rendered reuse views.
MERMAID_INLINE_LAYOUT = MERMAID_LAYOUT.replace('"htmlLabels": false', '"htmlLabels": true')
SCENES = {
    'Example': 'Manual published asset selections; the standard demonstration.',
    'Manual': 'Same stack and defaults as Example, with its own direct root. No nested scene root.',
    'Scenarios': 'VariLyr_Scenarios owns /World Layout: Normal or Exploded. Scenario adjustments stay on Adjustment prims; ordinary placement stays on occurrence parents.',
    'MaskedSize': 'ReviewLyr authors local Cube02/Adjustment/Asset scale=(1,1,1), masking the asset Size variant value even when Size=Tall. This is a deliberate conflict.',
    'MaskedSelection': 'ReviewLyr authors Cube01/Adjustment/Asset Finish=Blue locally, masking the selection inside either scene Layout branch. This is a deliberate conflict.',
    'STARTER': 'Independent starter Opinion, placement, variant and data layers; shared reusable source assets. Extra BASE, SIM and RUNTIME slots are empty and optional. Baseline environment/render/cameras still live in the root.',
    'Lofted': 'Five shapes with lightweight public variant declarations above asset and assembly payloads.',
    'Instanced': 'Native-instancing stress scene: 1,024 extra grid shapes plus the five teaching shapes, all shape Asset sites instanceable.',
    'Instanced_Wave': 'A signal-driven wave using all nine Size/Finish combinations on two shared shape sources.',
    'Instanced_Spiral': 'The same signal and shared sources arranged along a rising spiral.',
    'Instanced_Rings': 'The same signal and shared sources distributed across concentric rings.',
    'MotionGraphics': 'Animated MoGraph-style cloner: 1,024 points, six configurations and live JSON controls.',
}


WALKTHROUGHS = {'Example': '**Goal:** understand the basic ownership pattern. Start on the right with Cube, Cone and DisplayPair; GeoLyr references them into the scene. In the middle, TransLyr places occurrences and VariLyr selects their published Size, Finish and Palette controls. The root on the left composes these sibling layers. In the reuse graph, follow several occurrence arrows back to one source: reuse preserves a single authored implementation.', 'Manual': '**Goal:** work with explicit choices for individual occurrences. Follow the same source-to-GeoLyr-to-root route as Example; this separate entrypoint uses the same work layers and saved defaults, so it is not an independent project copy. Change selections through the rightful scene layer rather than editing reusable source definitions. There is no scene Layout switch here.', 'Scenarios': '**Goal:** switch coordinated scene arrangements. Follow GeoLyr to the shared assets, then locate VariLyr_Scenarios in the middle stack. Its /World Layout branches select asset controls and author scenario-relative adjustments on Adjustment prims; TransLyr retains ordinary placement on their parents. The paradigm is to keep conditional edits inside their owning branch while reusing the same asset packages.', 'MaskedSize': '**Goal:** recognise a deliberately broken variant result. Follow Cube02 to its shared Cube source, where Size=Tall defines scale. Then look at ReviewLyr in the scene stack: its unconditional scale on the same asset prim masks that variant value. Tall may remain selected while the cube resolves to unit scale. This demonstrates why layer order alone cannot resolve local-versus-variant conflicts.', 'MaskedSelection': '**Goal:** distinguish a variant selection from the branch that tries to drive it. Follow the scene Layout controls in VariLyr_Scenarios, then the stronger local Finish=Blue selection in ReviewLyr at Cube01/Adjustment/Asset. The local selection masks the branch selection, so the intended Layout-driven colour does not win. The asset material definitions remain shared; the conflict concerns who controls the selection.', 'STARTER': '**Goal:** begin a project with useful roles already available. Follow the shared assets on the right into the starter GeoLyr, then upward through its placement, variants, data and Opinion work layers. Extra role slots reserve places for later work; empty slots do not activate simulation or other systems. The root also supplies the visible environment and render baseline. Keep the roles you need and remove or disable the rest; the starter work layers are independent of the demo layers, while asset sources are still shared.'}


WALKTHROUGHS.update({
    'MotionGraphics': '**Goal:** animate a large clone field from a small, explicit control surface. Follow the two sources on the right through six prototype reference sites (Cube/Cone × Red/Blue/Yellow, Size=Normal) into one PointInstancer. GeoLyr owns its topology and stable IDs; VariLyr configures the prototypes. AnimLyr stores an eight-second clip of positions, rotations, scales and prototype indices, so Play works from the saved scene. DataLyr declares the JSON input and target. With the MotionGraphics launcher, a Python model reads that declaration and writes a temporary RUNTIME layer under Session; it overrides the baked arrays while keeping Opinion as the user authoring target. Saving JSON changes updates the live result. Turning live_preview off removes that contribution and reveals the baked clip. The lower graph shows six configurations converging on only two source assets and three shared materials. Point instances are array elements, not 1,024 individually editable prims; their colours switch through protoIndices, not per-point variant edits. Choose /World/MotionOverview as the viewport camera if the host does not restore it automatically.',
    'Lofted': '**Goal:** inspect asset controls without loading their implementation. Follow GeoLyr to the CubeLofted, ConeLofted and DisplayPairLofted interfaces. Each interface lists variant names and defaults; a payload leads to ContentsLyr, which composes the original role files. Empty interface branches advertise choices; values stay in the source VariLyr. Unloading Pair also hides its child occurrences, while its own Palette remains discoverable. This scene keeps the five-shape layout, with all shapes Blue/Normal for a simple comparison. It adds independent Opinion/Trans/Vari/Geo layers, and shares the original data and asset implementations.',
    'Instanced': '**Goal:** exercise extensive native reuse. Start at /World/InstanceGrid: a 32 by 32 grid adds 512 cubes and 512 cones. Including the teaching objects, there are 515 cube and 514 cone occurrence sites, each marked instanceable. GeoLyr links the same lofted packages; TransLyr positions occurrence parents, and VariLyr chooses matching Blue/Normal configurations. Compatible occurrences can share USD prototypes. DisplayPair stays non-instanceable so its child placement hierarchy remains editable. Select InstanceGrid and frame the selection in the viewport to see the full grid; the standard startup camera and ground cover only the original example area. No speed or memory gain has been benchmarked. To edit inside a shared shape, change its source, use its published variants, or deliberately make that occurrence non-instanceable first.',
})


for formation in ('Wave', 'Spiral', 'Rings'):
    WALKTHROUGHS['Instanced_' + formation] = (
        f'**Goal:** use incoming information to steer a {formation.lower()} formation without copying geometry. '
        'The driver reads 1,024 normalized JSON values. Each value selects one of nine Size/Finish combinations and controls height and heading; '
        'the selected formation determines horizontal placement. Follow the signal into TransLyr for placement and VariLyr for selections, '
        'then through the shared GeoLyr to payloaded instanceable assets. There are 512 grid cubes and 512 grid cones, plus the five teaching objects. '
        'This scene owns its generated role layers and Opinion; other formations are unchanged. Select /World/InstanceGrid and frame it to see the layout. '
        'These are deterministic static snapshots, not live telemetry, animation, physics or a performance benchmark. '
        'The reuse graph groups the 1,024 sites by source; each group contains mixed Size/Finish selections. '
        'Run the Python command in the driver section to change the input or regenerate this formation.'
    )


def label(value):
    return str(value).replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def relative(layer):
    return Path(layer.realPath).relative_to(PACKAGE).as_posix()


def open_relative(layer, path):
    return Sdf.Layer.FindOrOpenRelativeToLayer(layer, path)


def layer_label(layer):
    result = relative(layer)
    if layer.subLayerPaths:
        result += '<br/>Own sublayers, strongest first:'
        for index, path in enumerate(layer.subLayerPaths, 1):
            result += f'<br/>{index}. {label(path)}'
    return result


def diagram(root):
    if Path(root.realPath).stem == 'SceneROOT_MotionGraphics':
        return motion_diagram(root)
    scalable = Path(root.realPath).stem == 'SceneROOT_Lofted' or Path(root.realPath).stem.startswith('SceneROOT_Instanced')
    lines = ['```mermaid', MERMAID_INLINE_LAYOUT, 'flowchart LR',
             '    subgraph ENTRY["ROOT · left"]', '        direction TB',
             f'        R["{label(Path(root.realPath).name)}<br/>/World · cm · Z-up · 60 fps"]',
             '        B["Authored in this root<br/>/Environment: Sky, DistantLight, Looks/Grid, ground, groundCollider<br/>/Render: viewport product, settings and LdrColor<br/>/OmniverseKit_Persp, Front, Right, Top"]',
             '        R ~~~ B', '    end',
             '    subgraph STACK["DIRECT SCENE SUBLAYERS · strongest at top"]', '        direction TB']
    for i, path in enumerate(root.subLayerPaths):
        layer = open_relative(root, path)
        text = f'{i+1}. {layer_label(layer)}'
        if 'OpinLYR' in path: text += '<br/>Default authoring target · empty initially'
        if '_Starter' in path and not layer.rootPrims: text += '<br/>Empty optional slot'
        if i == len(root.subLayerPaths)-1: text += '<br/>BOTTOM / WEAKEST'
        lines.append(f'        L{i}["{text}"]')
        if i: lines.append(f'        L{i-1} ~~~ L{i}')
    lines.extend(['    end', '    subgraph SOURCES["REFERENCED PACKAGES · right"]', '        direction TB'])
    assets = [('PAIR','Assemblies/DisplayPair/AssetROOT_DisplayPair.usda'),
              ('CUBE','USD_Wrappers/Cube/AssetROOT_Cube.usda'),
              ('CONE','USD_Wrappers/Cone/AssetROOT_Cone.usda')]
    for node,path in assets:
        if scalable:
            family, name, _ = path.split('/')
            path = f'{family}/{name}Lofted/AssetROOT_{name}Lofted.usda'
        layer=Sdf.Layer.FindOrOpen(str(PACKAGE/'010_ASS_USD'/path))
        controls='Palette: Warm / Cool' if node=='PAIR' else 'Size: Normal / Large / Tall · Finish: Red / Blue / Yellow'
        lines.append(f'        {node}["{layer_label(layer)}<br/>Public controls: {controls}"]')
        if scalable:
            contents = Sdf.Layer.FindOrOpen(str(Path(layer.realPath).parent / '020_BASE_LYR/ContentsLyr.usda'))
            lines.append(f'        {node}C["{layer_label(contents)}"]')
            lines.append(f'        {node} -->|"payload; empty interface variants above this boundary"| {node}C')
    lines.extend([
        '        MAT["010_ASS_USD/MatLib/Palette_v001.usda<br/>/Materials/Red, Blue, Yellow, Ground<br/>Each material owns Surface shader"]',
        '        RES["Baseline resources<br/>010_ASS_USD/Envs/OmniverseStandard/Resources/<br/>CarLight_512x256.hdr · ov_uv_grids_basecolor_1024.png<br/>OmniPBR.mdl: external MDL search identifier"]',
        '        PAIR -->|"GeoLyr: CubePart/Adjustment/Asset"| CUBE',
        '        PAIR -->|"GeoLyr: ConePart/Adjustment/Asset"| CONE',
        '        CUBE -->|"MatLyr references Red, Blue, Yellow"| MAT',
        '        CONE -->|"MatLyr references Red, Blue, Yellow"| MAT',
        '        MAT ~~~ RES', '    end',
        '    ENTRY -->|"root subLayers list; sibling layers"| STACK',
        '    STACK -->|"GeoLyr: Cube01 and Cube02 → Cube; Cone01 → Cone; Pair01 → DisplayPair"| SOURCES',
        '    STACK -.->|"VariLyr selects public controls; definitions stay in packages"| SOURCES',
        '    ENTRY -.->|"root Sky/Grid resource dependencies"| SOURCES',
        '    classDef ccRoot fill:#fde8df,stroke:#d99b84,color:#17212b',
        '    classDef layer fill:#dceef9,stroke:#91bfd8,color:#17212b',
        '    classDef asset fill:#ffffff,stroke:#9db9c8,color:#17212b',
        '    class R,B ccRoot',
        '    class '+','.join(f'L{i}' for i in range(len(root.subLayerPaths)))+' layer',
        '    class PAIR,CUBE,CONE,MAT,RES asset', '```'])
    result = '\n'.join(lines)
    if scalable:
        result = result.replace('PAIR -->|"GeoLyr:', 'PAIRC -->|"GeoLyr:')
        result = result.replace('CUBE -->|"MatLyr', 'CUBEC -->|"MatLyr').replace('CONE -->|"MatLyr', 'CONEC -->|"MatLyr')
        if Path(root.realPath).stem.startswith('SceneROOT_Instanced'):
            result = result.replace('Cube01 and Cube02 → Cube; Cone01 → Cone; Pair01 → DisplayPair', 'teaching objects + InstanceGrid (512 Cube + 512 Cone); shape sites instanceable')
    return result


def motion_diagram(root):
    lines = ['```mermaid', MERMAID_INLINE_LAYOUT, 'flowchart LR',
        '    subgraph ENTRY["ROOT · left"]', '        direction TB',
        '        SESSION["Optional Session sublayer<br/>CC_MotionGraphics_Runtime · anonymous<br/>Generated arrays override saved animation<br/>Not the user authoring target"]',
        '        R["SceneROOT_MotionGraphics.usda<br/>Z-up · cm · 60 fps · time codes 0–480<br/>Standard environment/render baseline"]',
        '        SESSION ~~~ R', '    end',
        '    subgraph STACK["DIRECT SUBLAYERS · strongest at top"]', '        direction TB']
    for i, path in enumerate(root.subLayerPaths):
        text = f'{i+1}. {layer_label(open_relative(root, path))}'
        if 'OpinLYR' in path: text += '<br/>Default authoring target'
        if 'DataLyr' in path: text += '<br/>/World/MotionGraphControls · input and target declaration'
        if 'AnimLyr' in path: text += '<br/>241 samples · positions / orientations / scales / protoIndices / extent'
        if 'CamLyr' in path: text += '<br/>/World/MotionOverview'
        if 'TransLyr' in path: text += '<br/>Placement of the whole cloner'
        if 'VariLyr' in path: text += '<br/>Six prototype Finish choices · Size=Normal'
        if 'GeoLyr' in path: text += '<br/>PointInstancer · IDs 0–1023 · six references · BOTTOM'
        lines.append(f'        L{i}["{text}"]')
        if i: lines.append(f'        L{i-1} ~~~ L{i}')
    lines.extend(['    end', '    subgraph SRC["REUSABLE SOURCES + CONTROL INPUT · right"]', '        direction TB'])
    for name in ('Cube', 'Cone'):
        root_asset = Sdf.Layer.FindOrOpen(str(PACKAGE / f'010_ASS_USD/USD_Wrappers/{name}Lofted/AssetROOT_{name}Lofted.usda'))
        contents = Sdf.Layer.FindOrOpen(str(Path(root_asset.realPath).parent / '020_BASE_LYR/ContentsLyr.usda'))
        lines.extend([f'        {name}["{layer_label(root_asset)}<br/>Public Size / Finish interface"]',
                      f'        {name}C["{layer_label(contents)}"]', f'        {name} -->|payload| {name}C'])
    lines.extend([
        '        MAT["010_ASS_USD/MatLib/Palette_v001.usda<br/>One definition each: Red / Blue / Yellow<br/>Ground unused by these sources"]',
        '        CubeC -->|MatLyr references| MAT', '        ConeC -->|MatLyr references| MAT',
        '        JSON["040_DATA_LYR/Controls/motion_graphics.json<br/>layout · wave · scale · rotation · falloff · colour"]',
        '        RES["Baseline: bundled HDR and grid texture<br/>OmniPBR.mdl from Kit"]',
        '        MAT ~~~ JSON', '        JSON ~~~ RES', '    end',
        '    ENTRY -->|root sublayers| STACK',
        '    STACK -->|GeoLyr references three configurations of each shape| SRC',
        '    STACK -.->|DATA declares JSON; VariLyr selects public controls| SRC',
        '    ENTRY <-.-|optional Python model writes Session runtime arrays| SRC',
        '    classDef ccRoot fill:#fde8df,stroke:#d99b84,color:#17212b',
        '    classDef layer fill:#dceef9,stroke:#91bfd8,color:#17212b',
        '    class R ccRoot', '    class '+','.join(f'L{i}' for i in range(len(root.subLayerPaths)))+' layer', '```'])
    return '\n'.join(lines)


def motion_reuse():
    return '\n'.join(['```mermaid', MERMAID_LAYOUT, 'flowchart LR',
        '    R["SceneROOT_MotionGraphics.usda"]',
        '    P["ONE PointInstancer<br/>/World/MotionGraphics/Cloner<br/>1,024 stable IDs · 512 Cube + 512 Cone"]',
        '    R --> P',
        '    JSON["JSON controls via DATA<br/>Saved changes accepted after validation"]',
        '    MODEL["Shared Python motion model<br/>Grid / rings / spiral<br/>Plane / radial / swirl waves<br/>Scale, spin, tilt, noise, falloff"]',
        '    BAKE["AnimLyr · saved 8-second clip<br/>Explicit offline bake"]',
        '    LIVE["RUNTIME · temporary Session sublayer<br/>Timeline seconds · no disk writes<br/>Remove overlay to restore bake"]',
        '    JSON --> MODEL', '    MODEL --> BAKE', '    MODEL --> LIVE',
        '    BAKE -->|sampled arrays| P', '    LIVE -->|stronger current arrays| P',
        '    PC["Three Cube prototype sites<br/>Finish=Red / Blue / Yellow<br/>Size=Normal"]',
        '    PN["Three Cone prototype sites<br/>Finish=Red / Blue / Yellow<br/>Size=Normal"]',
        '    P -->|protoIndices 0–2| PC', '    P -->|protoIndices 3–5| PN',
        '    C["ONE Cube source<br/>AssetROOT_CubeLofted.usda<br/>Payload to original Cube role files"]',
        '    N["ONE Cone source<br/>AssetROOT_ConeLofted.usda<br/>Payload to original Cone role files"]',
        '    PC -->|three references| C', '    PN -->|three references| N',
        '    CM["Cube MatLyr references materials<br/>Finish branch binds Geometry"]',
        '    NM["Cone MatLyr references materials<br/>Finish branch binds Geometry"]',
        '    C --> CM', '    N --> NM',
        '    subgraph LIB["ONE shared Palette_v001 library"]', '        direction TB',
        '        RED["/Materials/Red<br/>ONE Material + Surface definition"]',
        '        BLUE["/Materials/Blue<br/>ONE Material + Surface definition"]',
        '        YELLOW["/Materials/Yellow<br/>ONE Material + Surface definition"]',
        '        GROUND["/Materials/Ground · unused here"]',
        '        RED ~~~ BLUE', '        BLUE ~~~ YELLOW', '        YELLOW ~~~ GROUND', '    end',
        '    CM --> RED', '    CM --> BLUE', '    CM --> YELLOW',
        '    NM --> RED', '    NM --> BLUE', '    NM --> YELLOW',
        '    ENV["Root baseline environment and rendering<br/>Grid material separate from Palette"]',
        '    R --> ENV', '```'])


def namespace(stage):
    scalable = Path(stage.GetRootLayer().realPath).stem == 'SceneROOT_Lofted' or Path(stage.GetRootLayer().realPath).stem.startswith('SceneROOT_Instanced')
    instanced = Path(stage.GetRootLayer().realPath).stem.startswith('SceneROOT_Instanced')
    def controls(path):
        choices=stage.GetPrimAtPath(path).GetVariantSets().GetAllVariantSelections()
        return label(', '.join(f'{key}={value}' for key,value in sorted(choices.items())))
    lines=['```mermaid',MERMAID_LAYOUT,'flowchart LR',
           '    ROOT["'+label(Path(stage.GetRootLayer().realPath).name)+'"]',
           '    WORLD["/World · scene hierarchy"]', '    ROOT --> WORLD']
    for node, occurrence, source in [('C1','Cube01','CUBE'),('C2','Cube02','CUBE'),('N1','Cone01','CONE'),('P1','Pair01','PAIR')]:
        path=f'/World/{occurrence}/Adjustment/Asset'
        lines.extend([f'    {node}["{occurrence}/Adjustment/Asset<br/>{controls(path)}"]',
                      f'    WORLD --> {node}',f'    {node} -->|"reference"| {source}'])
    lines.extend([
        '    PAIR["ONE assembly source<br/>AssetROOT_DisplayPair.usda"]',
        '    PC["CubePart/Adjustment/Asset<br/>'+controls('/World/Pair01/Adjustment/Asset/CubePart/Adjustment/Asset')+'"]',
        '    PN["ConePart/Adjustment/Asset<br/>'+controls('/World/Pair01/Adjustment/Asset/ConePart/Adjustment/Asset')+'"]',
        '    PAIR --> PC', '    PAIR --> PN',
        '    PC -->|"reference"| CUBE', '    PN -->|"reference"| CONE',
        '    CUBE["ONE Cube source<br/>AssetROOT_Cube.usda<br/>GeoLyr defines Cube geometry once<br/>3 scene occurrences"]',
        '    CONE["ONE Cone source<br/>AssetROOT_Cone.usda<br/>GeoLyr defines Cone geometry once<br/>2 scene occurrences"]',
        '    CM["Cube MatLyr<br/>Looks/Red, Blue, Yellow are reference sites<br/>Finish variant binds Geometry to selected Looks material"]',
        '    NM["Cone MatLyr<br/>Looks/Red, Blue, Yellow are reference sites<br/>Finish variant binds Geometry to selected Looks material"]',
        '    CUBE --> CM', '    CONE --> NM',
        '    subgraph LIB["ONE shared library · Palette_v001.usda"]',
        '        RED["/Materials/Red<br/>one Material + Surface shader definition"]',
        '        BLUE["/Materials/Blue<br/>one Material + Surface shader definition"]',
        '        YELLOW["/Materials/Yellow<br/>one Material + Surface shader definition"]',
        '        GROUND["/Materials/Ground<br/>defined but unused by these assets"]',
        '    end',
        '    CM -->|"reference /Materials/Red"| RED',
        '    CM -->|"reference /Materials/Blue"| BLUE',
        '    CM -->|"reference /Materials/Yellow"| YELLOW',
        '    NM -->|"reference /Materials/Red"| RED',
        '    NM -->|"reference /Materials/Blue"| BLUE',
        '    NM -->|"reference /Materials/Yellow"| YELLOW',
        '    ENV["Root baseline<br/>Environment: ground, collider, sky, light<br/>Render settings and viewport cameras"]',
        '    GRID["/Environment/Looks/Grid<br/>separate ground material + shader<br/>OmniPBR.mdl + grid texture"]',
        '    ROOT --> ENV', '    ENV -->|"ground material binding"| GRID',
        '```'])
    if scalable:
        extra = [
            '    CPAY["Cube payload ContentsLyr<br/>original VariLyr + MatLyr + TransLyr + GeoLyr"]',
            '    NPAY["Cone payload ContentsLyr<br/>original VariLyr + MatLyr + TransLyr + GeoLyr"]',
            '    PPAY["DisplayPair payload ContentsLyr<br/>original Palette and placement<br/>GeoLyr references lofted Cube/Cone"]',
            '    CUBE -->|"payload"| CPAY', '    CONE -->|"payload"| NPAY', '    PAIR -->|"payload"| PPAY',
        ]
        if instanced:
            extra += [
                '    GRIDC["InstanceGrid: 512 Cube occurrence sites<br/>Blue / Normal; instanceable<br/>individual placement on parents"]',
                '    GRIDN["InstanceGrid: 512 Cone occurrence sites<br/>Blue / Normal; instanceable<br/>individual placement on parents"]',
                '    WORLD --> GRIDC', '    WORLD --> GRIDN',
                '    GRIDC -->|"512 references to one interface"| CUBE',
                '    GRIDN -->|"512 references to one interface"| CONE',
            ]
        lines[-1:-1] = extra
    result = '\n'.join(lines)
    if scalable:
        for name in ('Cube', 'Cone', 'DisplayPair'):
            result = result.replace(f'AssetROOT_{name}.usda', f'AssetROOT_{name}Lofted.usda')
        result = result.replace('GeoLyr defines Cube geometry once', 'Size / Finish names above payload').replace('GeoLyr defines Cone geometry once', 'Size / Finish names above payload')
        result = result.replace('PAIR --> PC', 'PPAY --> PC').replace('PAIR --> PN', 'PPAY --> PN')
        result = result.replace('CUBE --> CM', 'CPAY --> CM').replace('CONE --> NM', 'NPAY --> NM')
        if instanced:
            result = result.replace('3 scene occurrences', '515 instanceable occurrences').replace('2 scene occurrences', '514 instanceable occurrences')
    if Path(stage.GetRootLayer().realPath).stem.startswith('SceneROOT_Instanced_'):
        result = result.replace('Blue / Normal; instanceable', '9 Size / Finish combinations; instanceable')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mermaid-cli', help='Path to mmdc for rendering fixed-layout reuse SVGs')
    args = parser.parse_args()
    chunks=[START, '## Exact composition diagrams for every scene',
            'Read from the saved USD files. **Layout: root left, ordered scene layers middle, reusable sources right.** Solid arrows point from each consumer to its composition dependencies; dashed arrows describe control selection or baseline resources. Internal stack order is numbered strongest first; invisible layout links do not create sublayer nesting. Asset boxes list their own exact sublayers. DataLyr boxes list their nested data contributions.',
            'The reuse views draw each source definition once: one Cube, one Cone and one shared definition each for Red, Blue and Yellow. The teaching layout has five shapes (three cubes, two cones); each Instanced scene adds 1,024 occurrences, shown as two counted groups. MotionGraphics instead has one PointInstancer with 1,024 points and six prototype configurations. Reference arrows are composition arcs, not copies. Saved selections appear on reference sites.',
            'These are source/dependency views, not expanded stage trees or rendered results. The Instanced scenes enable native instancing. Lofted and Instanced introduce payload boundaries and public interface declarations while sharing the original role files. Palette also contains an unused Ground definition; the visible ground uses its separate Grid material. Rendered outcomes remain deferred.']
    for name,description in SCENES.items():
        filename=f'SceneROOT_{name}.usda'
        root=Sdf.Layer.FindOrOpen(str(PACKAGE/filename))
        stage=Usd.Stage.Open(root)
        source = motion_reuse() if name == 'MotionGraphics' else namespace(stage)
        diagram_dir = PACKAGE / 'diagrams'
        diagram_dir.mkdir(exist_ok=True)
        stem = f'SceneROOT_{name}_reuse'
        mmd = diagram_dir / (stem + '.mmd')
        svg = diagram_dir / (stem + '.svg')
        mmd.write_text(source.removeprefix('```mermaid\n').removesuffix('\n```')+'\n', encoding='utf-8')
        if args.mermaid_cli:
            subprocess.run([args.mermaid_cli, '-i', str(mmd), '-o', str(svg), '-b', 'white'], check=True)
        if not svg.exists():
            raise RuntimeError('Render reuse SVGs with --mermaid-cli before updating the README.')
        chunks.extend([f'### {filename}',description,WALKTHROUGHS[name],diagram(root),
                       '<details>\n<summary>USD source reuse — each definition shown once</summary>\n',
                       f'![{name}: shared USD sources with vertical spacing](diagrams/{stem}.svg)',
                       f'[Open full-size SVG](diagrams/{stem}.svg) · [Mermaid source](diagrams/{stem}.mmd)',
                       '\n</details>'])
    chunks.append(END)
    path=PACKAGE/'README.md'; text=path.read_text(encoding='utf-8')
    block='\n\n'.join(chunks)+'\n'
    if START in text:
        begin=text.index(START); end=text.index(END)+len(END)
        text=text[:begin]+block+text[end:]
    else:
        marker='## Reproduce the authored fixture'
        text=text.replace(marker,block+'\n'+marker)
    path.write_text(text,encoding='utf-8')
    print(f'Documented {len(SCENES)} composition stacks and source-reuse graphs; no acceptance tests run.')


if __name__=='__main__': main()
