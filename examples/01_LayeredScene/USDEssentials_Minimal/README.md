# OpenUSD Essentials: one scene, three views

Open [`SceneROOT_USDEssentials.usda`](SceneROOT_USDEssentials.usda) in Omniverse
USD Composer. It composes one red cube and one blue cone from a small set of
readable USDA files. Open the same files in a text editor while the scene is
open in Composer.

## What you are looking at

USD is the scene description system and data model. USDA is its human-readable
text file format. Composer shows the composed stage: it resolves the root,
layers and asset references, then displays the result. Those are views of the
same authored USD data at different levels; the viewport is the resolved result,
while each USDA file shows the opinions authored in that file.

| In Composer | In the files | Meaning |
|---|---|---|
| Stage tree | `/World`, `Cube01`, `Cone01`, `Geometry` | The composed prim hierarchy |
| Layer panel | `SceneROOT` with `MatLyr`, `TransLyr`, `GeoLyr` as sublayers | The scene's layer stack and its edit locations |
| Viewport | One red cube and one blue cone | The result after USD composition and rendering |
| Open USDA text | Authored prims, properties, arcs and relationships | The readable contents of each layer |

## Follow the composition

```text
SceneROOT_USDEssentials.usda
├── sublayers (strongest first)
│   ├── MatLyr.usda   material definitions reference + scene bindings
│   ├── TransLyr.usda scene placement transforms
│   └── GeoLyr.usda   scene hierarchy + asset references
└── World
    ├── Cube01 ──reference──> Assets/Cube.usda ──geometry──> Geometry
    ├── Cone01 ──reference──> Assets/Cone.usda ──geometry──> Geometry
    └── Looks ───reference──> Assets/Palette.usda
         ├── Red
         └── Blue
```

The root is intentionally thin: it names the default prim and assembles the
scene's sublayers. `GeoLyr` creates the scene occurrences and references reusable
asset roots. `TransLyr` owns where those occurrences sit in this scene. `MatLyr`
references the shared material palette and binds one material to each geometry
prim. The shape files do not contain scene placement or color opinions.

The root's sublayer list is strongest-first. That ordering matters when layers
author competing opinions for the same property at the same composed prim; it
does not mean that a stronger layer replaces all content from weaker layers.
Here the three layers own different kinds of opinions, so they cooperate.

The sublayer entries are layer composition arcs. The `references` in `GeoLyr`
and `MatLyr` are reference composition arcs that bring prims from other files
into the stage. `material:binding` is a relationship connecting a geometry prim
to a material; it is not another geometry copy or a reference arc.

## A short inspection loop

1. Open the root file in Composer and locate `/World/Cube01/Geometry` and
   `/World/Cone01/Geometry` in the Stage tree.
2. In the Layer panel, select each scene layer and compare it with the matching
   file in a text editor. Notice that the Stage tree is composed, while the
   individual files contain only their authored contributions.
3. Find `prepend references` in `GeoLyr.usda`; follow the relative asset path
   to the `defaultPrim` in each asset file.
4. Find each translate in `TransLyr.usda`, then each `material:binding` in
   `MatLyr.usda`. Follow those material paths to the Red and Blue definitions in
   `Palette.usda`.
5. Save and reopen the root. A layer file by itself is a contribution, not the
   complete scene entry point.

## Basic habits this example demonstrates

- Open the root scene to inspect the complete composition.
- Put an edit in the layer that owns that kind of information.
- Keep reusable geometry and shared material definitions in their own files.
- Use relative paths so the example stays portable as a folder.
- Check both the edit target and the USDA file when something in the viewport
  differs from your expectation.
- Keep the scene small enough that each opinion and composition arc is easy to
  trace.

There is deliberately no floor, camera rig, environment, variant set or extra
geometry in this example. It is a first-reading scene, not a production starter.

## Teaching profile and provenance

This self-contained copy comes from TutorialBuilder's `USDEssentials_Minimal`
example. Keep this folder together when copying it. It uses centimetres, **Y-up
and 24 fps**; the larger examples beside it use Z-up and 60 fps. Open it as its
own stage rather than sublayering it into those scenes.

This introductory profile demonstrates Geo/Trans/Mat ownership, relative
references and scene-owned material bindings. It deliberately omits Opinion,
DATA, SIM and RUNTIME layers and the full starter folder taxonomy. Select the
appropriate scene layer explicitly before editing; this scene does not install
an authoring helper or automatically lock layers. A direct open uses the host's
edit-target behavior. Use a copy for experiments, select TransLyr to move a shape,
or MatLyr to change a binding, and save that layer. Frame `/World` in the viewport
and use the application's preview lighting if needed: no light is authored here.

These are declared teaching simplifications, not full composition-contract
conformance. Continue with the [larger scene guide](../README.md) to learn Opinion
authoring, variants, payloads and instancing. No PowerPoint content is part of this
copy. Developed with AI assistance; application review remains required.

## Next lesson

Continue with [color variants](README_ColorVariants.md): keep the same two shapes
and two materials, publish Red/Blue alternatives on each asset, and select them
independently from the scene.
