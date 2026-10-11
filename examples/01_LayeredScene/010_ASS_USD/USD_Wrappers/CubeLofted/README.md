# CubeLofted

Published entry: `AssetROOT_CubeLofted.usda`, default prim `/Cube`.
Z-up, centimetres, 60 fps. Public controls: **Size: Normal / Large / Tall; Finish: Red / Blue / Yellow**.

The root advertises empty variant branches and payloads `020_BASE_LYR/ContentsLyr.usda`.
ContentsLyr composes the original Cube role files, preserving one implementation.
DisplayPair's lofted form substitutes its own GeoLyr to link lofted child shapes.
Defaults and variant names were derived from the source VariLyr by the authoring tool;
source interface changes require republishing these declarations.

`050_REVIEW_LYR/OpinLYR_default.usda` is the package's own experimental authoring layer.
It is above the payload. Original demo asset Opinions are excluded from ContentsLyr.
Changes to shared source role files affect every consumer. Scene placement belongs
on an occurrence parent; instancing policy is declared by the consuming scene.
The source package is a required relative dependency: copy the complete example,
not this folder alone. No bounds cache, physics readiness or performance claim.

See the example package's `_contracts/scalability.json` and scene README for
load behavior, ownership, driver scenes and pending acceptance.
