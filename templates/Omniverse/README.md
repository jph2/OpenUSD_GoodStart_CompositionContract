# Omniverse starting scene

Jan supplied `examples/01_LayeredScene/ROOT_example.usda` and selected it as this project's standard starting scene. The generator uses this retained template for the standard and scenario entrypoints.

The template preserves `/World`, `/Environment`, `/Render` and the OmniverseKit viewport camera opinions, converted to Y-up while retaining the saved centimetre metric, 60 fps and the 0–100 timeline. Its ground plane, collider, camera transforms and environment frame were converted with the axis metadata. The two texture asset paths are rebased into `Resources`; the generator copies them into the example and adjusts their relative paths, then adds the contracted scene sublayers and session/lock policy.

The resources were resolved from the supplied scene's references to installed `omni.kit.stage_templates` 2.0.3. `OmniPBR.mdl` and OmniRtx/viewport behavior remain supplied by the Omniverse runtime. This is a concrete application template, not a renderer-neutral scene or a claim that every Omniverse product uses identical defaults.

The untouched supplied file, resource identities and previous example versions are retained under `harness/evidence/standard_root_adoption`. No installed Kit files were edited. Source inclusion for local use does not establish redistribution rights; publication decisions remain with the project owner.
