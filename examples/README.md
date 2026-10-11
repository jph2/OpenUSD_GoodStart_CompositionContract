# Composition Contract examples

This folder contains the original, canonical composition-arc example packages
for the OpenUSD GoodStart Composition Contract proposal:

- [Layered scene](01_LayeredScene/README.md): assets and assemblies, scene
  composition, variants, instancing, and authoring examples.
- [USD Essentials Minimal](02_USDEssentials_Minimal/README.md): an introductory
  cube-and-cone scene with fixed materials and color variants.

These examples demonstrate the proposal and retain their own declared profile
versions and acceptance status. They are not, by themselves, a certification of
general OpenUSD, NVIDIA SimReady, Isaac Sim, or production readiness.

## Downstream tutorial copies

TutorialBuilder contains teaching copies and adaptations of both packages at
`020_Tutorials/Upskill_OmniStream/1.x_OpenUSD/050_LearnMat/`:

- `01_LayeredScene` corresponds to this repository's `01_LayeredScene`.
- `02_USDEssentials_Minimal` corresponds to this repository's
  `02_USDEssentials_Minimal`.

The copies are intentionally redundant and can diverge. When a source example or
its tutorial adaptation changes, compare the counterpart and reconcile whichever
side needs the change. Preserve tutorial-specific material; do not overwrite it
blindly from the canonical example. Synchronization is currently a manual review
and update process, not an automated pipeline. Record any intentional difference
in the relevant example README when it would otherwise be confusing.
