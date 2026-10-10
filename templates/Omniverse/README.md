# Omniverse starting scene

Jan supplied `examples/01_LayeredScene/ROOT_example.usda` and selected it as this project's standard starting scene. The generator uses this retained template for the standard and scenario entrypoints.

The template preserves `/World`, `/Environment`, `/Render`, the OmniverseKit viewport camera opinions, Z-up, the exact saved centimetre metric, 60 fps and the 0–100 timeline. Only its two texture asset paths were rebased into `Resources`. The generator copies those files into the example and adjusts their relative paths again; it adds the contracted scene sublayers and session/lock policy.

The resources were resolved from the supplied scene's references to installed `omni.kit.stage_templates` 2.0.3. `OmniPBR.mdl` and OmniRtx/viewport behavior remain supplied by the Omniverse runtime. This is a concrete application template, not a renderer-neutral scene or a claim that every Omniverse product uses identical defaults.

The untouched supplied file, resource identities and previous example versions are retained under `harness/evidence/standard_root_adoption`. No installed Kit files were edited. Source inclusion for local use does not establish redistribution rights; publication decisions remain with the project owner.
