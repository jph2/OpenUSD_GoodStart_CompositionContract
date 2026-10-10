# MotionGraphics runtime

Live motion uses an **anonymous layer under Session** with role `RuntimeLyr`.
No generated per-frame USD file is saved here. The helper owns only the
PointInstancer's positions, orientations, scales, protoIndices and derived extent.
Its layer deliberately overrides the saved animation. Disable `live_preview` or
stop the helper to remove that contribution; Opinion remains the authoring target.

The preview writes time samples at the current timeline time and one time code
ahead, using the stage's time-code rate. Only these two samples are retained for
each controlled array. There are no live static defaults and no accumulating
animation history. Scrubbing or changing accepted controls reevaluates the window.
Play automatically reads back three advancing snapshots of USD/Fabric positions;
the panel and log distinguish changing data from unverified visible rendering.

Controls and the binding declaration live in DATA. Persistent animation lives in
BASE `AnimLyr_MotionGraphics.usdc`; changing it requires explicit rebaking.
See the [scene guide](../README.md#play-and-control-the-mograph-scene).
