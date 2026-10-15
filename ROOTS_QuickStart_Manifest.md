# Good ROOTS: the one-minute composition handout

**Root it. Own it. Organize it. Trim it. See it work.**

Use this five-word check when starting or reviewing a USD scene. The links below are a small route into the examples and tools—not a substitute for the full contract.

## The ROOTS check

- **R — Root it.** Let the scene root assemble the work layers in deliberate strength order. Keep composition structure as simple as the real ownership and collaboration needs allow.
- **O — Own it.** Put each edit in the layer owned by the responsible scene, assembly, or asset. In the layered profile, `GeoLyr` carries hierarchy and composition; ordinary placement transforms belong in `TransLyr`.
- **O — Organize it.** Keep reusable content and its choices with the asset; let the parent place occurrences and select through the asset's intended interface. A reference is not automatically an instance.
- **T — Trim it.** Start a composed scene or asset from the full scaffold, then remove roles it does not need. Keep simple leaf assets simple and self-contained where practical.
- **S — See it work.** Check the composed result for its declared purpose, profile, and target application. A file opening or a static inspection alone is not runtime acceptance.

## Start here

| Need | Open or run |
| --- | --- |
| Generate the legacy GoodStart project scaffold (folders, layer files, and sample scene/assets) | [Legacy setup script](https://github.com/jph2/USD_GoodStart/blob/main/scripts/setup_usd_project.py) · [Windows launcher](https://github.com/jph2/USD_GoodStart/blob/main/scripts/setup_usd_project.bat) · [Linux/macOS launcher](https://github.com/jph2/USD_GoodStart/blob/main/scripts/setup_usd_project.sh) |
| Author a bounded layered-scene example in a new or empty output folder | [Contract example builder](tools/build_example.py) · [Layered-scene guide](examples/01_LayeredScene/README.md) |
| Study minimal USD Essentials leaves | [Minimal example guide](examples/02_USDEssentials_Minimal/README.md) · [Cube](examples/02_USDEssentials_Minimal/010_ASS_USD/Cube.usda) · [Cone](examples/02_USDEssentials_Minimal/010_ASS_USD/Cone.usda) |
| Compare layered scene entrypoints | [Starter](examples/01_LayeredScene/SceneROOT_STARTER.usda) · [Example](examples/01_LayeredScene/SceneROOT_Example.usda) · [Scenarios](examples/01_LayeredScene/SceneROOT_Scenarios.usda) · [Instanced Rings](examples/01_LayeredScene/SceneROOT_Instanced_Rings.usda) |
| Read the full, evolving proposal | [Composition Contract](CompositionContract.md) |

**Tooling note:** the `USD_GoodStart` setup script creates the older project-template scaffold; it is not a generator for the current Composition Contract profile. The Contract builder is bounded to the layered-scene example, requires OpenUSD 26.08, and should write to a new or empty directory. Its reproduction alignment with every currently edited example scene is not established; do not use it to overwrite the checked-in example package.

**Status:** OpenUSD GoodStart Composition Contract **0.2.11** is an independent, evolving proposal, primarily scoped to Omniverse/Kit workflows. It is not an AOUSD or OpenUSD standard. Follow the full contract and the target project's accepted profile when they give more specific direction.
