# Resume state

Updated 2026-10-10 after adopting Jan's supplied Omniverse root. Draft 0.2.

## Version control handoff

Jan requested commit and push on 2026-10-10. The repository already contained initial commit `0ea84b4` on `main` and the configured origin `https://github.com/jph2/OpenUSD_Composition_Contracts.git`. At preparation, GitHub reported the repository private and fetching origin found no incoming changes. The requested commit includes the draft, example, template, startup tools, composition chart and retained evidence. `.gitattributes` preserves their recorded byte identities across Git checkouts; ordinary prose uses LF. Exact intended paths and sizes are enumerated before committing. Git history and the remote branch record the resulting commit and push; no tests were requested or run for this handoff.

## Current starting scene

`examples/01_LayeredScene/ROOT_example.usda` is now the standard scene and launcher default. It retains the supplied `/World`, `/Environment`, `/Render` and OmniverseKit camera opinions, Z-up, exact saved centimetre metric, 60 fps and time codes 0–100. The original assets compose under `/World` via DataLyr, TransLyr, VariLyr and GeoLyr. World_Manual is a compatibility alias; the scenario and conflict entries use the same baseline. Session authoring and persistent-layer protection remain the requested default through the launcher/helper.

The supplied root and prior package versions were preserved in `harness/evidence/standard_root_adoption`. The reusable template and two locally copied Kit texture dependencies live in `templates/Omniverse`; generated texture copies live under `010_ASS_USD/Envs/OmniverseStandard/Resources`. The previous scene Env/Mat/Cam/Light/Render layers and Ground asset files were retired to evidence. The active package now has 29 USD layers. No installed Kit or sibling project files changed.

Actual checks: a fresh candidate was authored using OpenUSD 26.08 before applying the bounded replacement. Initial authoring exposed a temporary Sdf layer handle lifetime issue; the generator now retains that handle and completed the fresh build. USD read-back covers five saved entrypoints and records identity `/World`, unchanged asset configuration, Z-up, the exact supplied units, 60 fps, 0–100 and `/OmniverseKit_Persp`. No coordinate conversion was needed or introduced. Kit material/viewport behavior, runtime session defaults and full variant acceptance remain untested. The supplied ground collider is retained; no simulation result is claimed.

## Previous session-default increment

Jan requested all persistent layers locked on open, Session Layer selected for authoring. CC-01 and the example guide distinguish default temporary session work from deliberate persistence. `tools/build_example.py` applies Kit lock metadata to package/scene roots and ships `Open_In_Kit.ps1` plus `_workflows/kit/session_defaults.py`. The helper protects loaded persistent layers including the root and selects the fresh session after the Layers UI initializes; it acts only on roots declaring `cc:defaultAuthoring = session`. No filesystem permissions or installed Kit app configuration are changed.

Installed `omni.kit.usd.layers` 2.7.2 and `omni.kit.widget.layers` 1.9.3 source inspection established that saved authoring-layer metadata skips anonymous targets and the usual lock helper excludes the root. Therefore direct USDA opening alone cannot guarantee the full requested default. Use the bundled launcher, or run the helper in the current Kit Script Editor. Helper execution and UI behavior have not been tested; no existing live Kit session was switched or discarded by this task.

Actual follow-up checks: the Python helper/generator and PowerShell launcher parsed successfully. USD read-back found the session policy in all four scene roots, 28 saved dependency locks in each baseline root and 30 in each review root, with zero composition errors for their saved defaults. Eight scene/asset entrypoints received policy metadata. Root edit protection is supplied by the runtime helper rather than the saved dependency lock map. The prior build manifest is retained at `harness/evidence/build_before_session_defaults.json`; the current manifest records the updated files and metadata. No tests were run.

## Exists

- CompositionContracts.md moved here as the authoritative draft, with CC-01 through CC-23 preserved.
- README, AGENTS, governance, workflow, tooling requirements, source routes, roadmap and review agenda.
- HANDOVER.md records the brief history and working decisions; AGENTS.md routes incoming agents to it. Added at Jan's request after bootstrap.
- TutorialBuilder source location replaced by a forwarding note; variant scene folders left in place.
- PROJECT_STRUCTURE.md records the revised diagram, numbered folder layout, ownership boundaries, explicit stack order and edit destinations. The user-supplied schematic, bounded VariantSetups reads and `USD_GoodStart/_Generated_Test` informed it.
- `examples/01_LayeredScene` contains 29 active USD layers: Cube/Cone packages, two standalone cube occurrences, DisplayPair, shared asset materials, supplied Omniverse startup content, project data, standard/scenario entrypoints and two deliberate review conflicts. The earlier 35-layer layout is preserved in evidence.
- `tools/build_example.py` authors this bounded fixture into a new/empty folder through OpenUSD APIs. It refuses nonempty output and is pinned to OpenUSD 26.08. It is not a general inspector or repair tool.
- `_contracts` in the example contains draft profile, ownership and expected-outcome JSON. `_pipeline_reports/build_manifest.json` records file hashes, script/contract identity, runtime and default-entrypoint read-back. `harness/evidence/source_review_0.2.json` records bounded predecessor source identities.

## Actual observations and limitations

- Authoring ran with Python 3.13.3 and OpenUSD 26.08 through `uv run --no-project --with usd-core==26.8`.
- The five current saved entrypoints reopened with default selections, default time, LoadAll and an empty session; no composition errors were returned. Cube01/Cube02 selections, resolved scale and bound material paths were read back.
- Manual and Normal-scenario entries resolve Cube02 Tall to scale `(1,1,2)`. The masked-size entry keeps Tall selected but resolves `(1,1,1)`. The masked-selection entry resolves Cube01 Finish and material to Blue despite the Normal scenario's Red selection.
- No acceptance tests, complete variant sweep, relocation trial, viewport rendering or Omniverse save/reopen review were run. Exploded, all assembly configurations and other intended behaviors remain expected outcomes awaiting that evaluation. No general conformance claim is made.

## Does not exist yet

No executable general inspector/repair pipeline, accepted conformance verdict, test suite/results, Omniverse extension, MCP integration or pipeline-nodes adapter. The bootstrap and example-authoring work did not initialize Git or publish the project; the subsequent commit/push request uses the existing private remote recorded above. No collaborator invitation or public release is part of this handoff. No license has been selected. The private pipeline repository has not been assessed.

## Next useful task

Open `examples/01_LayeredScene/ROOT_example.usda`, using Open_In_Kit.ps1 for the complete session-authoring defaults. Review the supplied viewport/environment behavior and the CC-01 template exception, then agree acceptance for variants, assembly choices, relocation and target-application persistence. Separately agree a general read-only inspector input/output contract for DT-01–03; the example JSON is a starting fixture, not an accepted general schema. If asked to share, establish hosting/access and source-resource distribution rights deliberately.

## Decisions in this increment

- Preserve CC-01–23; add CC-24 for portable storage/lifecycles and CC-25 for retained-source and published-interface boundaries.
- Keep familiar numeric directories but no numeric strength semantics. Reuse 010_ASS_USD, USD_Startpoint and USD_Wrappers; add Assemblies and 050_REVIEW; use generic `_workflows`. Reserved slots have READMEs instead of empty composed USD layers.
- Place ordinary transforms in the rightful owner's TransLyr, including asset geometry centering and scene camera/light poses. Keep variant-dependent scale/order and scene adjustment operations inside their branches.
- Use separate manual/scenario entrypoints, explicit review exceptions, asset Size/Finish and assembly Palette interfaces. Materials reference a bundled versioned library. The initial scene MatLyr ground binding was later retired when adopting the supplied root.
- Use centimetres, Z-up and `/World` for the new example. The inspected generated predecessor uses Y-up and `/world`; it was not converted or edited.
- Keep predecessor projects and the initial HANDOVER.md intact. New USD content and the authoring script were created here; no private pipeline content was accessed or copied.
- `.gitignore` excludes Python caches and local virtual environments. Shell policy rejected deletion of the generated `tools/__pycache__` cache; it was left ignored. A concurrently present `COMPOSITION_MEMORY_CHART.svg` was preserved and is not attributed to this task.

## Continuity

The origin was a TutorialBuilder discussion of local opinions masking variants. It developed into explicit ownership at asset/assembly/scene scopes, separate layer roles and deterministic inspection/repair requirements. The independent project enables focused feedback from Nandu, Dylan and the AOUSD IEDT group while leaving future GoodStart/workcell integration open. Their review or acceptance has not occurred here.
