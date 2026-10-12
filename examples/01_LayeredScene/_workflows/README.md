# Reproduction and workflow files

Reproduction uses the parent repository's tools/build_example.py. kit/session_defaults.py is the scoped Kit startup helper used by Open_In_Kit.ps1: persistent work/source layers are protected and Opinion becomes the edit target. It does not route or persist edits. Optional pipeline or ComfyUI definitions can be added here when needed; none is installed.

For MotionGraphics, run `kit/motion_graphics.py` using `runpy.run_path()` in Kit's
Script Editor (see the parent README). This starts the JSON watcher and the native
Motion Graphics Controls panel. `motion_graphics_core.py` owns ranges, validation,
comment strings, backed-up JSON saves and motion evaluation; the panel has no USD
authoring logic. Apply & Save writes the DATA JSON; rebaking is a separate explicit
operation. Rerun the bootstrap after updating these Python files.
