# Resume state

## 2026-10-11 — User-authorized commit and push scope

Jan requested committing and pushing the completed work on main: contract 0.2.0
and NVIDIA/identity evidence, the reusable composition skill and synchronization
workflow, and the LayeredScene Mermaid rendering fix. The selected set contains
16 files, enumerated with sizes before staging. Origin/main matched HEAD after
fetching; skill synchronization reported zero drift for the repository and the
personal installation. No additional rule or skill-guidance change was needed.

The pre-existing motion_graphics.json control edits, deletion of the Essentials
defaultscene.usda and untracked direct_root_kit.log are outside this commit scope
and remain local. Historical acceptance limits remain unchanged. Commit identity
and publication state are recorded by Git; no tests were run for this operation.

## 2026-10-11 — LayeredScene README Mermaid preview fix

Jan supplied a Markdown preview screenshot showing Mermaid 11.12.2's
`splitLineToFitWidth does not support newlines in the line` error and repeated
syntax-error panels. Updated all 15 inline Mermaid blocks in
`examples/01_LayeredScene/README.md` to use HTML labels at both root and flowchart
configuration scope. The MotionGraphics runtime feedback edge retains its arrow
toward ENTRY but is declared ENTRY-to-SRC to preserve root/layers/sources ordering.

Updated `tools/document_scene_graphs.py` to emit the same inline configuration and
feedback edge on regeneration. Existing reuse SVGs and their export configuration
were preserved. No USD scene or runtime adapter changed.

Actual document preview: rendered all 15 inline diagrams successfully with the
exact Mermaid 11.12.2 browser bundle; visually inspected the motion data-flow and
final MotionGraphics composition diagrams. Temporary SVG/PNG previews are outside
the repository. The user's VS Code preview was not directly controlled; reopening
it may be necessary to clear error panels from the previous failed render. No USD
acceptance tests or repository test suite ran.

Skill impact review: this fixes Markdown presentation and its generator; CC rules,
profiles and reusable skill guidance are unchanged. Contract and skill remain 0.2.0.
Refreshed the managed skill installation and checked synchronization with no drift.

## 2026-10-11 — Reusable composition skill and required synchronization

Jan requested a skill derived from the composition contract and an AGENTS.md rule
requiring skill maintenance when this repository changes, with matching versions.

Created `skills/openusd-composition-contract/SKILL.md` and `agents/openai.yaml` as
the maintained package. The skill routes tasks to the relevant CC sections and
preserves ownership/context rules, Opinion and host exceptions, conditional values,
instancing boundaries, imported packages, early ERP/PLM identity, composable bindings,
readiness evidence and authoring/deployment separation. Its normal discovery mode
is enabled by default. It adds guidance, not USD enforcement.

`tools/sync_composition_skill.py` derives the version from the main paper, generates
the full reference with portable companion links and records normalized source/file
hashes plus all 33 CC definitions in `references/source.json`. It supports read-only
`--check` and bounded `--install`; it preserves unrelated files and refuses to
overwrite a foreign or locally modified managed installation. Human review of
semantic skill changes remains required; regeneration cannot perform that review.

Installed the four package files in
`C:/Users/jan/.codex/skills/openusd-composition-contract` at version **0.2.0**, equal
to the contract. The source contract's requirements and version were unchanged by
this task. This host uses the `.codex/skills` catalog; `--skills-root` supports other
configured locations without editing application configuration.

AGENTS.md and WORKFLOW.md now require skill impact review on every repository change,
instruction updates where affected, reference/version refresh on every contract
edit, personal-installation sync and a recorded outcome. README documents invocation
and maintenance; DISCUSSION and SOURCES record the decision and packaging provenance.

Actual checks: skill-creator's static metadata validator passed; the sync helper's
read-only comparison found zero stale repository/installed files. Whitespace diff
review passed. No behavioral eval, USD test, scene repair, commit or publication was
performed. Prior unrelated edits and historical example evidence remain untouched.
Future contract changes must use this synchronization workflow; runtime and industrial
acceptance work remains as recorded below.

## 2026-10-11 — NVIDIA findings and early identity adopted in draft 0.2.0

Jan requested the NVIDIA architecture conclusion and nesting/performance explanation
in README.md with evidence links, and the remaining assessment in CompositionContract.md.
He additionally required stronger emphasis on stable unique identifiers, introduced
as early as possible from governing ERP/PLM or equivalent systems, and Composable Bindings.

Actual documentation changes:

- README now cites both VFI guides, explains modular authoring and deployment, and
  foregrounds early authoritative identity as a foundation of dependable digital twins.
- CompositionContract.md is draft 0.2.0 with existing CC-01–28 IDs preserved. Section 21
  records NVIDIA alignment, specific SimReady packaging/units/geometry gaps, robotics
  and industrial-schema requirements, evidence limits and a bounded industrial pilot.
  CC-12 adds versioned profile/results requirements; CC-24/25/26 distinguish maintained
  authoring conventions from traceable generated target packages and measured deployment.
- CC-27 requires identity at intake/first authoring, authority and uniqueness scope,
  separate type/occurrence/physical-instance identity, repeated-import continuity,
  controlled local allocation when external identity is absent, and reconciliation.
  CC-28 resolves bindings through those identities and blocks unresolved affected targets.
  Direct links to Aaron Luk's draft and the Composable Bindings PDF accompany the policy.
- DISCUSSION.md records the adopted decisions; ROADMAP.md reflects early identity,
  the industrial pilot and deployment work; SOURCES.md records the review boundaries.
  A stale README starter-guide anchor discovered during link review was corrected.

Documentation review covered local Markdown destinations/heading anchors, unchanged
CC rule definitions and whitespace diffs. No scene changes, generator execution,
validator, runtime acceptance or test suite were part of this documentation update.
Existing motion-control edits, deleted Essentials source and untracked Kit log were
preserved. No sibling repository edits, commit, push or publication occurred.

The earlier assessment below remains historical evidence; its recommended policies
are now adopted only to the extent specified in the 0.2.0 text. Existing 0.1.1 sample
profiles, starter copies, inventories and recorded hashes retain their original
baseline and have not acquired 0.2.0 acceptance. Remaining work: define machine-readable
identity/profile/result schemas, preserve source IDs in fixtures, implement binding
resolution and validation, then evaluate the proposed industrial/deployment pilot
under a separate implementation or verification request.

## 2026-10-11 — NVIDIA industrial twin and robotics alignment review

Jan requested a repository assessment against NVIDIA guidance, using the executive
summary links in USD_GoodStart/WIP_Docs/LAYER_ORDER_REFERENCES_RESEARCH.md (1.12.0).
Reviewed the current CC text, entry docs, roadmap, tooling requirements, example
profile, selected asset/layer sources and existing evidence limitations. Project
README is labelled 0.2.0; the contract and example profile remain 0.1.1, and the
profile's rule range stops at CC-26 although the prose includes CC-27/28.

Assessment: recursive ownership, public interfaces, preservation of imported
packages, conditional authoring and separate asset/assembly acceptance provide a
credible composition foundation. Universal readiness and NVIDIA conformance are
not demonstrated. Recommendations below are review findings, not adopted changes
to CC rules or authorization to implement a migration.

Followed the research's public NVIDIA routes: Isaac Asset Structure, SimReady
Foundation, DSX and its Generic CDU source, and VFI. The supplied Isaac 6.0.1 URL
was inaccessible through the web tool; used the accessible official
[6.0.0 asset structure page](https://docs.isaacsim.omniverse.nvidia.com/6.0.0/robot_setup/asset_structure.html)
and its tuning tutorial. SimReady requirement comparisons use the accessible
[2026.08.0 documentation](https://nvidia.github.io/simready-foundation/2026.08.0/),
including FET_001_STANDARD 1.0.1, Robot-Body, ISA.001, RV.011, NP.002/003/005,
non-visual materials and AIF-Entity. These are retrieved documentation baselines,
not installed or executed validator versions. Robot-Body documentation itself
notes a composition-document/validator naming disagreement; pin the actual
manifests and implementation before any conformance decision.

Concrete findings and proposed next work:

- Example Cube/Cone assets and SceneROOT_Example use approximately 0.01 metres
  per unit. The selected minimal SimReady feature requires UN.007 (1.0), and
  VG.MESH.001 requires mesh geometry; the asset examples use native Cube/Cone.
  These are demonstrated data differences against selected requirements, not a
  validator execution or a defect in their declared teaching scope. Use a
  separate simulation publication profile with deliberate dimensional conversion.
- CC-25 preserves incoming NVIDIA packages appropriately. For locally authored
  outgoing assets, explicitly resolve CC-26 naming/layout and role conventions
  against selected packaging features. NP.005 defines a particular asset folder
  layout; ISA.001 selects base-layer arcs/layouts. Our generic layer layout does
  not itself establish compliance. Keep authoring and delivery contracts distinct.
- CC-12/24/25 already require readiness evidence. Materialize the checklist into
  versioned profiles, selected upstream requirement/feature IDs, supported
  configurations and per-requirement results. No general inspector or SimReady
  validation integration exists; PhysicsLyr_Starter is an empty authoring slot.
- Define robotics acceptance for placement/attachment frames, articulation and
  collision behavior, units/mass/time, runtime isolation, sensors and applicable
  semantic/non-visual materials. CC-05b/21/23 provide ownership boundaries; their
  implementation and composed runtime behavior require a real robot fixture.
- DSX Properties/Ports/Connections roles can carry domain data, but domain schemas
  and consumer behavior remain unspecified. AIF-Entity versions even differ in
  connection-point representation; preserve the selected version explicitly.
- Add a generated deployment contract under CC-24, with source/output mapping,
  preserved composition behavior and measured cold/warm load, memory and runtime
  performance. [VFI deployment guidance](https://docs.omniverse.nvidia.com/vfi/latest/guide/asset-structure-optimizations-and-tradeoffs.html)
  distinguishes modular authoring from runtime packaging. Existing instance counts
  are not a factory-scale benchmark.
- CC-27/28 specify identity/binding continuity, but example occurrence IDs and the
  mock MoGraph adapter do not demonstrate industrial integration. Include repeated
  assemblies, rename/reparent, source updates and binding invalidation in acceptance.

Proposed bounded pilot: one pinned robot plus gripper/sensor/fixture, two independently
configured occurrences, a reusable workcell repeated in a line, and a small DSX/AIF
equipment case for a second domain. Pin target runtimes and profiles first. Evaluate
asset rules and composed behavior separately, including change impact and generated
deployment equivalence. Define measurable tolerances and performance budgets before
running. This pilot remains proposed.

Actual inspection: read-only Usd.Stage/Sdf-backed opening of Cube, Cone and
SceneROOT_Example with usd-core 26.8, LoadNone, saved default selections. All three
reported zero composition errors; metrics and geometry types are recorded with 28
input hashes in [the inventory](evidence/nvidia_alignment_inventory_2026-10-11.json).
This does not cover renderer resources, variants, physics, persistence or throughput.
No SimReady validator, Isaac/Kit runtime, benchmark or test suite ran. GoodStart
authority lookup searched spec, manual and full for `instancing` and `metersPerUnit`;
matches establish occurrence, with the physics units discussion supporting explicit
conversion. No formal universal layer-order definition or absence claim was inferred.

Only this review record and its JSON evidence were added. Existing README, motion
controls, deleted Essentials source and untracked Kit log changes were preserved.
No scene repair, contract revision, sibling-repository edit, commit or push.

## 2026-10-11 - repository identity renamed

GitHub repository rename completed through authenticated gh CLI:
jph2/OpenUSD_Composition_Contracts -> jph2/OpenUSD_GoodStart_CompositionContract.
Verified GitHub reports the new public repository URL. Local origin fetch/push
URLs now point to the new slug; fetch completed and main tracks origin/main.
Renamed authoritative document to CompositionContract.md and updated active
repo/docs/scripts/archive references and display titles. Starter ZIP now contains
_contracts/reference/CompositionContract.md and refreshed inventory. Historical
evidence retains the name in effect when captured.

Jan manually renamed the local checkout to
E:/SynologyDrive/9999_LocalRepo/OpenUSD_GoodStart_CompositionContract and reopened
it here. Verified that the new path exists, the old path is absent, the Git root
resolves to the new directory, and origin fetch/push both use the renamed GitHub
repository. No commit/push of accumulated working-tree changes was requested.


## 2026-10-11 - naming convention made explicit in CC-26

Documented exact class-directory names and singular _LYR under existing CC-26,
including canonical 040_DATA_LYR and 050_REVIEW_LYR. Clarified recursive scope,
unchanged role filenames, explicit sublayer strength, coordinated path/metadata
updates, and imported/historical evidence exceptions. Updated project structure,
root README and both example guides. Synced shipped Markdown and ZIP inventory.
Documentation/package update only; no new scene edits or tests. Prior retained
legacy DATA folder exception remains recorded below. No commit/push requested.


## 2026-10-11 — DATA and REVIEW folder naming standardized

Adopted 040_DATA_LYR and 050_REVIEW_LYR throughout active contract/layout docs,
scene/asset roots, profiles, workflow scripts, generators and diagram labels.
Renamed role directories in both examples and nested asset packages; Essentials
scene-level directories had already been renamed by the user. Updated starter ZIP
entry names and text references and regenerated its hash inventory. Existing
archived motion control values preserved; local user controls copied intact.
Historical reports/raw logs and older STATE entries retain their original paths.

Exception: Windows denied renaming examples/01_LayeredScene/040_DATA_LYRs.
Automatic approval review blocked the follow-up move/remove command (no specific
reason supplied beyond policy). Copied its contents to 040_DATA_LYR instead;
all current scene/script references use the new directory. The old directory is
retained as a redundant copy; starter builder explicitly excludes it. Remove it
later after releasing its lock, with user authorization. Reload open Kit scenes
and rerun helpers before editing so in-memory stages stop using old paths.
No tests or Kit acceptance executed. No commit or push requested.


## 2026-10-11 — Essentials uses supplied Omniverse default scene

User renamed the package to examples/02_USDEssentials_Minimal and supplied
its defaultscene.usda. Rebuilt both SceneROOTs by copying that baseline's
root specs/metadata and merging each lesson's direct sublayer list plus Opinion
policy. No nested defaultscene sublayer/reference. Environment, ground, lights,
render settings and viewport-camera settings retained under CC-01. Original
source file unchanged. HDR/grid texture copied from its referenced Kit template
resources into the package and root asset paths made relative; OmniPBR.mdl still
requires Omniverse's shader search path. Role layers and Opinions preserved.
Builder now uses this template on future regeneration and supports --roots-only.
Updated new-location links, READMEs/diagrams/profile and portable starter ZIP.
Unrelated motion controls and raw Kit log remain untouched. USD parsing/export
performed during authoring; no tests or Kit viewport acceptance performed.
No commit/push requested.


## 2026-10-11 — Essentials rebuilt at standalone location

User moved the teaching package to examples/USDEssentials_Minimal and requested
contract-aligned structure. Replaced legacy Assets/Layers with numbered role
categories, recursive Cube/Cone packages and AssetROOT entrypoints. Plain and
ColorVariants asset roots share GeoLyr/TransLyr; only color roots compose asset
MatLyr/VariLyr. Scene roots directly compose sibling roles and independent
Opinions; GeoLyr remains weakest. Stage metrics are Z-up/cm/60 fps. Scene
placement uses occurrence parents; intrinsic centering belongs to asset TransLyr.
Reserved SOURCE/SIM/RUNTIME/DATA categories contain notes, no empty USD roles.

Added portable Kit launcher and existing session_defaults helper, ownership/stack
profile, two updated teaching guides and diagrams, and bounded USD author
tools/build_essentials.py (explicit replacement flag, existing Opinions retained).
Updated larger example links, contract teaching profile and project structure.
Starter builder now includes sibling Essentials as a portable subpackage and
rewrites its README links. Refreshed archive Essentials/docs/inventory selectively
so unrelated user motion_graphics.json changes are not silently packaged.
Legacy moved files were removed only after comparing their bytes with HEAD.
TutorialBuilder and PowerPoint were not changed.

Actual readback with usd-core 26.8: both roots load with Z/cm/60 fps; each composes
one Cube and one Cone with resolved Red/Blue bindings at the intended sites.
USDA parsed during authoring; git diff --check clean. No test suite, variant sweep,
Mermaid rendering or Kit UI/viewport acceptance ran. Opinion helper behavior is
reused, not newly observed in this package. No commit/push requested this turn.
Unrelated motion JSON edit and harness/evidence/direct_root_kit.log remain intact.


## 2026-10-11 — second Essentials lesson: color variants

Added SceneROOT_USDEssentials_ColorVariants under USDEssentials_Minimal with
independent asset-owned Color=Red/Blue choices. Two lightweight interfaces reuse
the original Cube/Cone geometry and common asset Mat/Vari layers referencing the
original palette. Scene Geo/Vari files reuse existing placement. The original
scene's fixed binding layer is excluded only from the new root. Added a tutorial,
Mermaid diagram, main README navigation and explicit teaching-profile exceptions.
Read back all four color combinations with usd-core 26.8 in a temporary Session;
resolved material paths matched each selection. No files saved by read-back and
no Kit viewport inspection. Updated ZIP documentation, new files and inventory;
unrelated local motion controls and shipped settings preserved. The subsequent
user request authorizes committing and pushing this lesson and its package.


## 2026-10-11 — README Mermaid rendering repairs

Replaced invalid labeled reverse arrows in all generated scene diagrams with
consumer-to-dependency arrows, retaining the root/layers/sources layout intent.
Renamed the reserved-looking root style class to ccRoot; MotionGraphics namespace
styles now have unique motion prefixes and explicitly unfilled connectors.
Consolidated its six long VariLyr selection arrows into one labeled site-control
edge and increased spacing. Updated the generator and README arrow legend.
All 16 README Mermaid blocks rendered successfully with the cached Mermaid CLI;
inspected the namespace PNG and confirmed the oversized filled shapes are gone.
GitHub's deployed renderer was not directly exercised. Updated the starter ZIP
README and inventory only, preserving other packaged contents and new local
motion-control edits. No USD scene/runtime changes.


## 2026-10-11 — remaining tracked changes prepared for publication

Retained the user-edited MotionGraphics controls and rebuilt the starter ZIP
from the current example folder so its controls and documentation agree with
the repository. Included the earlier comparative-research handoff note in this
repository; the research paper itself remains in the separate USD_GoodStart
checkout. The generated direct_root_kit.log remains local and untracked.
Packaging and diff checks only; no new Kit execution or runtime acceptance.


## 2026-10-11 — USD Essentials minimal teaching scene copied here

Added the self-contained TutorialBuilder USDEssentials_Minimal scene under
examples/01_LayeredScene, preserving all seven USDA files byte-for-byte. Added
README navigation, a composition Mermaid and opening/editing walkthrough, plus
a declared teaching profile in CompositionContract.md. Explicitly documents
Y-up/24 fps, manual edit targets, no automatic locks or Opinion layer, and the
simplified Assets/Layers folders. The tutorial source and slides are untouched.
Updated the portable ZIP and its inventory with these files and documentation;
other packaged bytes, including shipped motion controls, were preserved.
Source-copy and ZIP byte/dependency checks plus diff review performed; no Kit
execution, rendering or USD acceptance tests. Prepared a scoped commit excluding
the existing motion-control edits, Kit log and earlier research state note.


## 2026-10-11 — comparative composition research updated

Updated the existing local draft in `USD_GoodStart/WIP_Docs/LAYER_ORDER_REFERENCES_RESEARCH.md`
from its pre-existing uncommitted 1.10.0 draft to 1.11.0, preserving the 1.10.0
profiles/composition-contracts edits. Added Section 21 with a quick comparison table
for the locally inspected Kitchen Set, NVIDIA DSX, Isaac Sim Asset Structure 3.0,
and the OpenUSD GoodStart Composition Contract project/sample set labelled 0.2.0. The table
compares scope, composition center, specialization/benefit, and fit/boundary; the
follow-up explains how the patterns can compose instead of treating them as rival
universal structures.

Important version finding: the Composition Contracts project README says 0.2.0,
while `CompositionContract.md` still labels its normative working text 0.1.1.
The research therefore describes 0.2.0 as the current project/example state, not
as a released 0.2.0 contract specification. Kitchen evidence is attributed to a
bounded read-only local audit (425 reference sites, 76 packages, 425 instanceable
sites, 114 prototypes; stage layer counts 230 LoadAll / 78 LoadNone including the
anonymous session layer). Explicitly states these are not performance benchmarks.
The local MotionGraphics and general conformance work remain under development.

Reviewed official NVIDIA DSX SimReady asset-journey and system-architecture pages;
the Asset Structure 3.0 section already links and analyzes NVIDIA's published
robot-package guidance. Checks: `git diff --check` on the research paper and
targeted `rg` inspection of version/section routes. No USD, Kit, benchmark, test,
or validator ran. No commit/push. The target GoodStart checkout already had an
uncommitted paper edit to 1.10.0 and an unrelated untracked `_Generated_Test/`;
both were preserved, and only the requested paper was edited there.

## 2026-10-11 — README version label updated

Updated the repository README project version from 0.1.1 to 0.2.0, including
the Mermaid diagram title. Kept the `Composition_Starter_0.1.1` package path
unchanged because it identifies the existing starter bundle, not the project
version. No scene or package contents changed; no tests or USD validation ran.

## 2026-10-11 — MotionGraphics marked as under-development proof of concept

Jan reports that MotionGraphics remained visually inactive after the runtime and
read-back changes, then began working after restarting Kit and reloading the
scene. This is evidence that a manual lifecycle reset restored the visible
result in that session; it does not identify the cause or prove automatic
refresh/rebind behavior.

Expanded the sample README with three Mermaid diagrams and an implementation
walkthrough: local JSON mock input versus future publishers; DATA declaration;
shared validation/evaluation model; Kit watcher/panel/timeline; direct root
sublayers and PointInstancer namespace; saved AnimLyr fallback; temporary
anonymous Session overlay and its five arrays; USD-to-Fabric-to-renderer path;
stop/reload lifecycle and current stale-viewport boundary. Marked the sample as
an under-development proof of concept in both the sample and repository READMEs.
Updated the machine-readable profile with the reload observation and clarified
that JSON is a local file, not a server/live connector.

No scene or runtime implementation changed. Rebuilt the portable starter ZIP
(173 files), then read back its README and MotionGraphics profile: three or more
Mermaid diagrams, proof-of-concept status, mock-source description and reload
observation are present and the packaged profile matches the source JSON. No
tests or Kit execution ran. Resume with automatic viewport refresh/rebind still
open; this documentation and package update does not fix it.

## 2026-10-11 — Live arrays reach Fabric; renderer-specific safeguard added

The newest attached auto-diagnostic has six playback snapshots: timeline seconds
advance, sampled USD `positions` change, `positions_time_varying=true`, and Fabric
`positions` match USD and change at each sample. The viewport remains bound to the
same stage with updates enabled and no freeze frame. The user's image is still
visually static. This localizes the remaining failure after USD-to-Fabric value
sync; position authoring is not the current suspect. The Kit log identifies the
host as Kit 110.3.2, FSD enabled, with `usdrt.scenegraph` 7.6.3.

NVIDIA Kit 110.3 release notes document an FSD defect where scene-partitioned
instanced prim transforms could remain visually stationary while Fabric world
transforms were correct (OMPE-104540). The MotionGraphics USD does not author
`primvars:omni:scenePartition`; RTX scene partitioning is disabled by default, so
the user's effective app setting was not established by the prior diagnostic.
NVIDIA's release notes mark the cited defect fixed in Kit 110.3, while the user's
installed extensions identify as 110.3.2; this match alone therefore does not
establish that the older defect is present in their build.
Added that setting to playback read-back. The helper now temporarily disables
`/renderer/scenePartitioning/enabled` only when the host reports it true, and
restores true on controller detach; it does not edit the app config or scene.
This is a targeted compatibility guard, not yet confirmed as the cause/fix.

README and source provenance updated; portable starter ZIP rebuilt. No tests or
Kit execution ran here. Next: rerun the main MotionGraphics bootstrap, inspect
the panel/log for the scene-partitioning warning and visible playback. If it was
already disabled and the render is still static, the next decisive A/B is to
disable Fabric Scene Delegate in the app's Rendering preferences and reopen the
scene, comparing OmniHydra rendering. Do not change scene geometry or writer
again until that renderer comparison is known.

## 2026-10-11 — Paused read-back received; live writer now uses time samples

User supplied three diagnostics with playing=false, seconds=3.3666667 (frame
202), updates=1. All three sampled positions match between runtime default,
composed USD and Fabric; viewport uses the same stage, updates=true and
freeze_frame=false. Log confirms Play at 22:04:04Z occurred AFTER diagnostics
at 22:03:55Z, followed by advancing time/counters; later Pause was explicit.
This proves a paused pose reached Fabric, not dynamic propagation or rendering.
Requested a viewport/panel screenshot during Play; none received at edit time.

Changed live writer from default replacement to a rolling two-sample window at
current time and one stage time code ahead, evaluated with identical accepted
controls. Set overlay timeCodesPerSecond to stage rate; prune old samples within
the change block. Same five arrays, anonymous layer, precedence and cleanup;
no scene/control files or renderer settings changed. This makes the live arrays
explicitly time-varying for imaging; it is a candidate playback repair, not a
proven explanation for the earlier static image. It evaluates twice per update;
throughput and shutter-time behavior outside the narrow window remain unmeasured.

Controller loads the diagnostic from current source and runs it on attach/Play.
It waits up to 60 seconds for three advancing playback snapshots, reports
time-varying state/sample times, and exposes USD/Fabric position-change results
in a separate panel label. Paused captures no longer stand in for moving data.
Tasks cancel on detach/reconnect; standalone diagnostic remains read-only.
README, runtime note, machine profile, source evidence and ZIP updated. No tests
or new Kit execution ran by the agent. Next: rerun MAIN motion_graphics.py (not
the diagnostic), press Play and leave running. Inspect automatic report and
viewport. Actual resolution remains pending; do not call this confirmed fixed.

## 2026-10-11 — Timeline and writer active; visible motion still unresolved

User confirms Play/Pause work but there is no animation or error. Read the live
Kit log: 21:53:46–21:54:59Z reports advancing seconds and runtime update counts,
successful Reconnect and accepted JSON, without masking/visibility warnings.
The context timeline is the default empty-name timeline. This does not prove
the values change in composed USD or that rendering consumes them. The earlier
timeline-binding improvement did not resolve the reported symptom.

Added `_workflows/kit/diagnose_motion_graphics.py`: three read-only snapshots
0.37 seconds apart, logging selected positions from the controller's layer,
composed USD and an already-present Fabric prim, plus layer sources and viewport
stage/time/updates/freeze state. It does not force synchronization, mutate scene
or render settings, change playback or write report files. Requested that Jan
run it once while playing; the output can be read from the existing Kit log.
No response or diagnostic output received at this update. No speculative
render-setting changes or motion-writer changes applied. README and ZIP include
the diagnostic. No tests or Kit execution ran by the agent.

Read installed USDRT 7.6.3 FSD comparison/known-issues and viewport 110.0.0 API.
FSD normally synchronizes USD before rendering; general documentation of array
diffing limitations is not proof of this fault. Next: inspect the three live
reports, then repair the specific failed boundary. Do not claim animation fixed
based on counters alone or switch render delegates without evidence.

## 2026-10-10 — Visible panel with apparently inactive playback

User reports Play has no visible effect or errors although widgets work. Existing
log through 21:43:29Z shows successful restart after cleanup, stage attachment,
accepted valid JSON and subsequent saves. Current controls are the visible-wave
preset (live=true, strength=1, amplitude=600, wavelength=1800, speed=0.5). These
establish input connectivity, not timeline advancement or composed motion. Asked
for panel status/screenshot; no answer yet at implementation time. Current live
timeline state and masking opinions have not been inspected directly.

Replaced global-default timeline use with UsdContext.get_timeline/name (installed
omni.usd 1.18.0 API). Play/Pause now have explicit controller callbacks, logging,
readiness/range/director checks and visible failures. Play uses stage time-code
range and enables auto advancement if disabled, retaining/restoring its prior
state on detach. Changed callbacks so cancelled tasks from Reconnect cannot
detach the new run. Reconnect restarts only this controller, discards panel draft,
reloads saved controls and recreates its anonymous overlay; no other scene
layers are unmuted or edited.

Added a separate half-second runtime status with live/baked, playing/paused,
seconds and output-update count. It diagnoses stalled clocks, detached/muted
overlay, missing/invisible PointInstancer and stronger authored opinions for the
five controlled arrays. Diagnostic errors are isolated from the motion writer;
state changes and Play clicks are logged. Input status remains separate.

README/profile/source evidence and portable ZIP updated. No saved controls or USD
scene files modified by this repair. No tests or live Kit execution ran. Context
timeline binding fixes a real implementation weakness, but a different timeline
has not been proven to be the cause in the user's current session. Next evidence:
rerun bootstrap, Play, inspect advancing seconds/update count and any named
blocking opinion in the panel. Actual playback resolution is still unconfirmed.

## 2026-10-10 — Restart cleanup after expired USD layer handles

User reports the panel ran nicely before an ArgumentError in old
session_defaults.restore at 21:31:03Z. Existing Kit log confirms panel opening
at 21:27:03/21:27:40Z, repeated successful DATA JSON saves/acceptance through
21:30:01Z, then layer muteness changes before the failed restart. The failure
calls SetPermissionToEdit on a saved Sdf layer handle; an expired handle is
consistent with this trace and the composition changes. No direct live-object
inspection was performed. Panel startup/control-save evidence is now recorded;
this is not full rendering or lifecycle acceptance.

Updated both session_defaults.py copies: capture identifier, instance handle and
original permission; registry-find the same surviving instance for restoration;
skip expired/replaced handles without opening files. Consume cleanup records
before processing, isolate/log each restore failure and continue UI-setting
restoration. Stop is repeatable, subscriptions/tasks are released, and stopped
helpers cannot reschedule. Crucially, bootstrap invokes the new stop_helper on
the previous object rather than its old stop/restore methods, supporting the
already-running helper's legacy two-field permission records. Motion bootstrap
now runs authoring-helper recovery before stopping the prior motion controller.

README/profile/project structure and source evidence updated; starter ZIP rebuilt.
Control values, scene USD files and installed Kit code unchanged. Read-only
inspection and source edits only; no tests or Kit script execution ran. User
must rerun the same bootstrap. Cleanup after muting/unloading, scene changes and
subsequent reruns still needs observation in the running Kit instance.

## 2026-10-10 — Panel startup loaded an outdated motion model

User's Kit traceback at 21:25:21Z reports missing cc_motion_model.control_hints
in panel construction. The function exists in the current core source. Read-only
inspection found the Kit/Python 3.12 core pyc still dated 20:59 local, predating
the panel changes, while the newer authoring runtime's pyc was updated. Installed
Kit kernel stat_cache.py patches importlib's file-stat lookup with a cache whose
refresh is explicit. This supports a stale import-cache explanation; no live
module introspection or cache-invalidation experiment was performed.

Changed the bootstrap's two fixed local helper loads to read source bytes and
compile into fresh ModuleType namespaces. This bypasses loader/pyc/stat caching
without changing global import hooks, sys.modules, installed files or caches.
Startup logs the source path/hash and checks required model functions/attributes
before stopping the previous controller or creating the panel. Panel construction
now releases partially built UI on errors; stop is idempotent for repeated runs.
README updated and starter ZIP rebuilt. Control JSON and scene assets unchanged.
No tests or Kit execution ran; user must rerun the same runpy bootstrap once.
Panel display and interactions remain pending acceptance in the running Kit app.

## 2026-10-10 — Ranges beside controls and visible native Kit panel

User asked for ranges/comments, understandable rejection reasons and the missing
Script Editor UI. Added optional `_comment_<control>` strings immediately above
each JSON value, with units, limits and useful examples. The shared core owns
these hints, validation and the IDE schema; annotation strings are excluded from
evaluation. Existing plain controls remain supported. Syntax errors now include
nearby text as well as line/column. A single invalid value still rejects input.

Added `_workflows/kit/motion_graphics_panel.py`: Motion Graphics Controls opens
with the existing bootstrap, with bounded sliders, choice lists, explanations,
persistent accepted/rejected/draft states, Apply & Save JSON, Reload JSON,
Visible wave preset and Play/Pause. Panel edits wait for explicit Apply; saves
validate, detect stale disk revisions, preserve original bytes under ignored
motion_graphics/panel_save_* and atomically replace only the DATA JSON. Reload
discards a draft for valid disk values; invalid disk input can be repaired from
the displayed controls with an explicit Save and backup. No USD bake/save is
performed. Controller owns the window/listeners and releases them on rerun/stop;
stage changes rebind it. A dispatched disk save finishes for its original path
even if the scene closes, without later UI/USD callbacks into that scene.

Fresh input was valid JSON but speed_hz=500. Changed only that control to 0.5;
preserved spacing=100, wavelength=111 and all other numeric/choice values.
Original bytes are under panel_save_08df78fbdb584444865e97742fba582e. The existing
writer validated the candidate as part of applying this repair; no tests or
rebake ran. Short wavelength relative to spacing may still look irregular; the
panel's Visible wave preset offers an explicit alternative.

Updated scene guide, project structure, workflow notes, motion profile and source
evidence. Starter ZIP is rebuilt from these files. Inspected installed omni.ui
3.3.1 and timeline 1.1.0 APIs; did not execute the new panel or visually verify
playback in Kit. User must rerun the bootstrap once to replace their old in-memory
controller: it cannot read the new comment fields or show the panel. UI, closing,
reload, external-edit conflicts and root-save acceptance remain pending in Kit.
No commit/push or installed application modifications.

## 2026-10-10 — Kit root save compatibility and more visible motion

User supplied SETTINGS_SAVING exceptions: root customLayerData/cameraSettings
writes failed because our helper hard-locked the root. Inspected installed Layers
2.7.2, Widget Layers 1.9.3 and Viewport 110.0.0 source; the active Kit traceback
reports USD 0.25.11.kit.5. Updated both session_defaults.py copies to keep the
active root API-writable while protecting other persistent work/source layers and
retaining Opinion authoring. Record/restore prior permissions on teardown. This
is a host exception, not metadata-only write protection. CC-01, diagrams' lock
label, profiles/expected text, generator text, READMEs, PROJECT_STRUCTURE and the
decision record now say so. No installed code, root USD files or geometry changed.
The running helper needs one rerun; updated settings-save behavior is unverified.

User also reported little visible reaction. Latest JSON had broken layout and
missing commas, wavelength_cm=6 outside limits, and amplitude_cm=20. Repaired it
and installed an explicit visible rings preset: amplitude 600 cm, wavelength
1800 cm, speed 0.5 Hz, base scale 1, scale wave 0.8, tilt 60 degrees, spin 45 deg/s,
falloff radius 12000 cm; retained spacing 200 and other values. Original bytes and
changes retained under ignored motion_graphics/visible_preset_fef36514b0364d2fa11ba6ddbfa8449c.
Candidate was parsed/validated as part of authoring. Existing Kit log at 21:05:31Z
confirms accepted controls and recovered input. No visual playback inspection,
tests or bake ran. README distinguishes JSON edits in the IDE from the one-time
Python bootstrap in Kit and explains falloff. Portable ZIP refreshed with the
current helper/docs/controls; saved animation still reflects its original bake.

## 2026-10-10 — Corrected latest live control edit

After repeated watcher rejections and the interrupted turn, inspected the latest
file rather than replaying the old repair. spacing_cm was already 160 and speed_hz
already 1; the remaining issues were a missing comma after spacing_cm and
scale_wave=8. Added the comma and changed scale_wave to 0.8, preserving all other
values. Parsed and validated the candidate as part of the repair before atomic
replacement. Original bytes retained in ignored motion_graphics/repair_cde856268d004bc696f86f73bd560e49.
No USD edits, tests or rebake. This repairs the active local control file, not the
previously shipped preset. Existing Kit log records "accepted saved JSON controls"
and "control input recovered" at 20:58:13Z after this repair. Live input acceptance
is therefore observed; viewport response was not visually inspected.

## 2026-10-10 — Live watcher reports a new malformed save

User supplied the running helper's JSON syntax warning at 18:59:35Z; this confirms
the watcher is now active, not viewport correctness. Inspected current controls:
missing commas after spacing_cm=5000 and speed_hz=2000. Added only those commas,
retaining every control value and a prior-byte backup under the ignored motion
repair folder. JSON parses after the repair. Range validation will still reject
spacing_cm=5000 (50–500), speed_hz=2000 (−2–2), and scale_wave=22 (0–0.9).
These newly chosen values were preserved for user correction rather than silently
normalized again. No tests, USD edits or archive refresh; the shipped preset was
left with its previously valid controls. Live viewport response remains unverified.

## 2026-10-10 — JSON changes appeared ineffective

User reported editing motion_graphics.json without a scene response. Read the
saved JSON, running Kit command line and its existing direct_root_kit.log. Kit
loaded SceneROOT_MotionGraphics at 18:47:30Z, but this process was launched with
session_defaults.py only; there were no CC motion startup/accepted-input messages.
It was displaying the bake without the live adapter. The JSON also had an
unterminated swirl string, missing speed comma and four unsupported values.

Repaired syntax and normalized those four fields to their declared maxima:
strength 10→1, spacing_cm 1160→500, speed_hz 22→2, color_cycle_hz 11.375→2.
Preserved other controls, including swirl/noise/spin edits. Exact original bytes
and field-change record retained under ignored _pipeline_reports/motion_graphics/
repair_d452904c10b948179c0b7f5ee41cd8ae. The repair invokes the existing validator
before writing; no test suite or Kit playback check ran. Runtime still rejects
out-of-range saves rather than automatically clamping user input.

Added syntax line/column and aggregated numeric diagnostics. Kit adapter now
posts optional host notifications for accepted/rejected JSON and runtime/watcher
failures; inspected installed notification_manager 1.0.16's public API. README
includes one-time runpy activation in the already-open scene, required success
messages and common range/syntax pitfalls. No script was injected into the running
Kit process, no new Kit process launched, and no USD layer saved. Activation in
the user's existing window remains the next step. Refreshed the portable ZIP;
notifications and live playback remain application acceptance work.

## 2026-10-10 — Animated cloner and live JSON controls

Added independent `SceneROOT_MotionGraphics.usda`: one PointInstancer, 1024 fixed
IDs (32 x 32), six Cube/Cone × Red/Blue/Yellow prototypes with Size=Normal. Uses
existing lofted sources and materials; no Kitchen content copied. Root retains
the standard cm/Z-up/identity-World baseline and directly lists its own Opinion,
DATA, Anim, Cam, Trans, Vari and Geo roles. DATA declares the local JSON input and
cloner target. BASE AnimLyr_MotionGraphics.usdc stores 241 samples over 0–480 at
60 time codes/s (eight seconds). Whole-cloner placement remains in TransLyr;
CamLyr supplies /World/MotionOverview. No prior scenes were replaced.

Portable motion_graphics_core.py supplies validated controls and deterministic
grid/rings/spiral, plane/radial/swirl waves, scale, tilt/spin, noise, falloff and
colour cycling. Controls sit at the top of DATA/Controls/motion_graphics.json;
adjacent JSON Schema provides ranges for IDEs. Fixed IDs/topology remain stable.
build_motion_graphics.py defaults to a plan; --apply creates only new named files.
--rebake changes only the clip, retaining prior bytes, exact input and provenance
with stale-input/output checks and atomic single-file replacement. Backup records
are ignored by Git and excluded from packaging. Rebaking was not exercised.

Launcher option MotionGraphics activates the existing Opinion/lock helper and a
new opt-in Kit controller. The latter uses timeline seconds, asynchronously reads
JSON about every 250 ms, and writes the five declared arrays into its own anonymous
RUNTIME sublayer of Session on Kit's update thread. It does not save files or change
the user's edit target. Invalid input holds the last valid controls; before any
valid input the bake remains visible. live_preview=false removes the overlay.
Stage close/replacement, rerun and explicit stop release owned tasks/layers. No UI
panel was built: Jan's follow-up asked whether script-created omni.ui panels are
possible; explained that they are, with explicit lifetime/cleanup, and that the
same model can support a later panel or packaged extension.

Added CC-05d, motion profile, README instructions/ownership table and the twelfth
scene's Mermaid/SVG diagrams. Updated project structure and launcher. Authoring
ran with usd-core 26.8; an Sdf constructor keyword error was fixed before outputs
were written. References are authored as Sdf specs to avoid anonymous-layer path
resolution warnings. Documentation extraction opened saved stages at LoadAll;
Mermaid CLI rendered 12 reuse SVGs. No tests, Kit launch/playback, live reload,
renderer/camera/lock acceptance or performance measurements ran. These remain
required application acceptance, including interruption and malformed-input cases.
The 4.94 MB clip uses USDC to keep sample storage manageable. No installed Kit
files changed, no commits or pushes. Rebuilt portable ZIP with 171 files, including
controls/schema, bake, runtime helper, source model, updated guide and diagrams.

## Standalone SVG label compatibility

Jan reported missing text when opening the full-size SVG despite visible inline labels. Disabled Mermaid HTML labels globally and for flowcharts, regenerated all six reuse SVGs, and inspected the Example raster preview. Each SVG now contains 43 native text elements and zero foreignObject elements, removing the embedded-HTML dependency. Rebuilt ZIP with corrected SVGs and sources. No USD changes or Kit execution.

## Fixed-layout reuse SVGs

Jan's screenshots showed unchanged layout despite Mermaid spacing directives. Replaced the six inline reuse Mermaid renders with generated SVG embeds and full-size links, retaining .mmd sources under examples/01_LayeredScene/diagrams. tools/document_scene_graphs.py accepts --mermaid-cli to regenerate them. Rendered all six with mmdc and visually inspected the Example PNG preview: tall layout with separated rows; SVG viewBox is 3063.94 × 1692. Markdown host handling of Mermaid directives is no longer responsible for reuse-view spacing. Rebuilt ZIP to include SVG/source files. No scene edits, acceptance tests, commit or push.

## Vertical diagram spacing correction

Jan clarified that diagrams need more separation top-to-bottom, not extra width. Changed LR flowchart nodeSpacing to 200 (vertical separation) and rankSpacing to 35 (horizontal separation), with modest internal padding. Regenerated README diagrams and portable ZIP. No scene changes or tests.

## Diagram spacing

Increased Mermaid node padding and node/column spacing for all per-scene composition and reuse diagrams at Jan's request. Updated the shared diagram generator, regenerated README diagrams and refreshed the portable ZIP. Layout-only change; no tests or scene edits.

## Source reuse diagrams corrected

Replaced expanded composed namespace trees with source-reuse graphs in all six README sections. One Cube, one Cone and one definition each for Red/Blue/Yellow now have converging reference edges from their consumers; scene occurrences retain their selections. Distinguishes ordinary references from native instancing and source definitions from composed prims. Explicitly separates the unused Palette Ground entry and the baseline Grid ground material. Updated diagram generator and rebuilt ZIP. Documentation only; no scene edits, tests, commit or push.

## Concise sample README

Removed sample README origin attribution, migration narrative, historical layer counts and old read-back tables at Jan's request. Kept a short launch guide, six-scene chooser, practical authoring rules, folder mapping and current limitations. Preserved all per-scene composition/namespace diagrams and rebuilt the portable ZIP. History remains in harness evidence rather than the user guide. Documentation only; no tests, commit or push.

## Per-scene composition and namespace diagrams

Added six Mermaid composition diagrams and six collapsible composed prim-hierarchy diagrams to examples/01_LayeredScene/README.md using tools/document_scene_graphs.py. Read actual saved root/asset sublayers and composed default prim trees through USD; this is documentation extraction, not acceptance testing. Root-left / stack-middle / assets-right layout includes numbered stack order, nested Data layers, recursive asset stacks, shared material/resource routes and scenario/review distinctions. Scene graphs include saved selections and all traversed prims, not every variant branch or property connection. Rendered outcomes to the left of root remain deferred per Jan. Rebuilt portable ZIP with updated README. No Kit render, tests, commit or push.

## Portable delivery refresh

At Jan's request, refreshed the BAT/PowerShell companions and rebuilt the ZIP from the current corrected sample. Setup notes identify the flat BASE layout, recursive AssetROOT packages, Opinion target metadata and material-path correction. Existing extracted projects are not automatically migrated; use a fresh destination. No installer or Kit execution, no commit/push.

## Ground material path and flat scene BASE storage

Jan reported a red ground and unnecessary nesting in 020_BASE_LYR. Found that the previous recursive path migration had anchored the OmniPBR.mdl search identifier as ./OmniPBR.mdl. Restored the search identifier in all roots and guarded that migration against modifying unanchored search paths. Flattened Starter role layers to <Role>_Starter.usda and scenario variants to VariLyr_Scenarios.usda, updating references, lock metadata, profiles, generator and docs. tools/simplify_base_layout.py records the bounded USD-aware migration. Rebuilt portable bundle. No tests or Kit rendering check; ground appearance after reloading remains unverified. No changes to unsaved application edits, no commit/push.

## Recursive asset package layout

Portable bundle rebuilt with 95 files. Automatic approval review blocked removal of the three obsolete empty layers/ directories; left them on disk. They contain no USD files, are not composed, and Git does not track empty directories.

Jan requested the same readable folder/layer pattern at asset scope. Migrated Cube, Cone and DisplayPair from named .usda roots and layers/ into AssetROOT_<Name>.usda and 020_BASE_LYR. Added package-owned Opinion and reserved class folders with notes. tools/adopt_recursive_asset_layout.py updates USD asset paths, lock metadata and profile/ownership references; tools/build_example.py reproduces the layout and standalone Opinion policy. Scene roots lock referenced asset Opinions; opening an asset itself selects its own Opinion. Updated CC-25/26, docs and portable bundle. Original prim paths and variant implementations retained; no tests or Kit runtime verification. Historical evidence keeps old filenames. No commit/push. AssetROOT is role-based, including reusable buildings/workcells; SceneROOT remains the working-scene convention. External imported packages are not automatically normalized.

## Opinion target restoration fix

Jan reported Opinion was not the default authoring layer. Inspected installed omni.kit.usd.layers 2.7.2 layer_utils.py: Kit restores omni_layer.authoring_layer via a root-relative path. Our generator/migration incorrectly removed that field from the former Session workflow. Added it to all six scene roots, generator and migration script, leaving Opinion unlocked. Helper now uses Kit's set_edit_target_by_identifier and checks the resulting target. Rebuilt portable preset with corrected roots/helper. Source inspection and USD-aware metadata authoring only; no tests or Kit runtime execution. Existing open stages or previously extracted copies need the updated files reopened; unsaved work was not touched. No commit/push.

## Starter publication checkpoint

Jan requested commit/push of the Opinion authoring change, generous starter master and portable setup bundle. Include their source scripts, authored layers, profile/expected records and documentation; retain the raw Kit log locally. Packaging completed, but installer execution, generator acceptance and updated Kit startup remain untested. Git history records the publication commit; push outcome is reported in the task.

## Portable project setup

Inspected only USD_GoodStart's supplied batch/PowerShell launchers as requested. Added our own Windows BAT/PowerShell setup and tools/build_starter_bundle.py, which packages authored sample/starter files and dependencies into starter/Composition_Starter_0.1.1/Composition_Starter.zip. The portable folder can be copied to a destination and run offline without Python; extraction preflights collisions and destination paths, never overwrites existing files and installs no applications. Bundled launcher defaults to STARTER. Historical acceptance manifests are excluded and replaced by a packaging-only inventory. Packaging executed; installer, updated generator and Kit runtime were not tested. No commit/push. The companion BAT, PS1 and ZIP must remain together.

## Opinion authoring and generous starter master

Jan confirmed normalized OpinLYR_default.usda and SceneROOT_STARTER.usda names, requested a deliberately generous starter, and superseded Session-default authoring with editable Opinion plus all other persistent layers protected. Added shared Opinion to five demo roots and independent Starter work layers: copied demo references/placement/variants/data, optional BASE roles plus SIM/RUNTIME slots, supplied Omniverse baseline in the root. Relative references were reanchored through USD APIs; authoring emitted transient warnings before reanchoring, and the generator now groups those mutations in Sdf.ChangeBlock. Updated generator, bounded migration script, launcher, profile, expected outcomes, CC-01 and docs. Startup helper selects the declared Opinion with legacy session-policy support. Existing build reports are historical. No tests or Kit launch, no conformance claim, no commit/push. Runtime target/lock UI acceptance remains pending; copying the whole package is required for independent projects.

## AI assistance disclosure

Added a README disclosure at Jan's request acknowledging AI tools, including OpenAI Codex, in research support, documentation, code and examples. It retains human responsibility and distinguishes recorded checks from unverified content. Documentation only; no tests, commit or push in this increment.

## Publication checkpoint

Jan requested commit and push of the accumulated 0.1.1 work: contracts, roadmap, diagrams, direct SceneROOT entrypoints, launcher/generator updates and retained migration evidence. The raw direct_root_kit.log remains local; the research-paper edit belongs to its separate repository and is outside this commit. No tests were run for publication. See Git history for the resulting commit; push outcome is reported in the task.

## Asset-interface and acceptance requirements adopted

Jan approved the proposed integration. Extended CC-25 with a concrete asset-interface checklist (purpose, provenance, coordinates, dependencies, controls, simulation alternatives, writer/lifecycle and evidence) and clarified that imported packages need no forced internal rewrite or extra wrapper. Extended CC-12 with separate asset, independent-reuse, configuration, assembly and change-impact acceptance, including explicit not-evaluated outcomes. README links the requirements; DISCUSSION records the decision. Existing IDs, diagram, folders and scenes remain unchanged. Documentation only; no tests, implementation, commit or push. Applying the checklist to actual sample profiles and selecting a pinned SimReady robot/runtime remain future work.

## Incoming assets, SimReady and upstream priorities

Clarified Asset Structure 3.0 as incoming robot packaging preserved inside larger workcell/line/facility composition, in README, contract comparison and the previously authorized research §6.3.8. Added upper README context for SimReady, relevant OpenUSD developments and Jan's AOUSD/IEDT workcell discussions, with official status explicitly unconfirmed. Added bounded CC-12/24/25 evaluation implications and a roadmap priority table for UsdValidation, SimReady, profiles/capabilities, namespace editing, LOD, splines and nested bodies. Sources distinguish upstream status from local availability. No diagram/layout or USD edits, installations, tests, commit or push in this increment. Next: agree a pinned robot/workcell profile and supported runtime before implementing adapters or claiming conformance.

## Research integration and NVIDIA comparison

At Jan's explicit request, added §6.3.8 and the repository link to the sibling AAS_OPC_OpenUSD_INTEGRATION/docs/AAS_OPC_OpenUSD_RESEARCH_v14.md. Kept contract additions bounded: requirement-to-evidence/promotion in CC-12 and external-data lifecycle/consumer impact in CC-24. Added a sourced comparison with Isaac Sim Asset Structure 3.0 and DSX SimReady documentation, distinguishing domain profiles from our scene conventions. DSX scene files were not inspected; compatibility remains unverified. Documentation only, no tests or scene changes, no commit/push.

Refined README prominence following Jan's correction: purpose, requirements and composition evaluation lead again. Identifier separation and composable bindings remain linked near the introduction as industry-driven requirements for identity continuity, clear responsibilities and integration stability during development, rather than the project's headline objective.

README now leads with composition contracts for digital twins and physical AI, immediately followed by the linked identifier-separation proposal and Composable Bindings paper. Preserved the personal OpenUSD journey and evaluation framing below it; removed the duplicated upstream introduction from Working with agents. Documentation-only change.

## README upstream integration references

Read the full Composable Bindings v1.0 whitepaper (November 2025) and added both requested links to README: Aaron Luk's identifier-separation proposal #105 and the Microsoft/NVIDIA Composable Bindings paper, crediting Christoph Berlin and Aaron Luk. Clarified our intent to integrate these ideas and distinguished the paper's future declarative-config direction from Jan's more detailed proposed binding artifacts. Documentation only; no implementation or tests.

## Identity and composable bindings

Reviewed bounded sections of Jan's AAS_OPC_OpenUSD_RESEARCH_v14 and Aaron Luk's proposal #105/source draft. Added CC-27 for namespace/source/occurrence/physical-instance separation and ownership-level placement, and CC-28 for declarative bindings, execution artifacts, output routing and evaluation. Clarified the current example IDs as illustrative scene-occurrence fields, not mesh tags or an upstream standard. README/roadmap/source notes and chart identity hints updated. No asset IDs, binding engine, scene migration or tests were added; identifier encoding and pilot implementation remain open.

## SceneROOT naming adopted

Jan selected the exact repository-wide scene entrypoint convention SceneROOT_<Purpose>.usda, now CC-26. Renamed the five active example roots to SceneROOT_Example, SceneROOT_Manual, SceneROOT_Scenarios, SceneROOT_MaskedSize and SceneROOT_MaskedSelection. Updated active docs, profiles, generator and launcher references; retained original template/evidence filenames and the historical migration script. Existing open Kit sessions still refer to their previously opened paths and must be reopened via the updated launcher; do not save them back to the obsolete filenames. Prior manifest observations and hashes remain historical. No USD content changes or tests were required for the filename migration.

## Grouped class boxes

Refined the README, contract and project-structure Mermaid charts to four class boxes containing role lists: BASE, SIM, RUNTIME and DATA. Preserved root-left / stack-middle / assets-right, asset/assembly details and bottom GeoLyr. REVIEW remains an optional annotation/contribution. Regenerated the SVG successfully. Class boxes do not create USD aggregate layers or prescribe optional-class strength. Naming remains under discussion: recommend ROOT_<Purpose>.usda for this project; no files renamed. Official NVIDIA asset-structure guidance uses root layer as a role and treats /World as an agreed prim namespace, not a required filename; no evidence establishes a universally most-common filename convention.

## Naming and diagram classifications

Adopted Root / ROOT_<Purpose>.usda as entrypoint terminology, with scene reserved for the composed result. Existing World_* filenames are explicitly legacy pending coordinated migration; this documentation task does not rename live scene files. Added ASSET USD, BASE, SIM, RUNTIME, DATA and REVIEW class labels to the existing Mermaid nodes in README, CompositionContracts and PROJECT_STRUCTURE, preserving edges, columns and GeoLyr's bottom position. Added the storage/class/role mapping and distinguished BASE physics setup from SIM results. SVG is regenerated from the detailed contract chart. No USD changes or tests are part of this increment.

## Direct scene root correction

Opened the corrected World_Manual in a separate existing-build Kit 110.3 Composer process using the session-default startup helper. Runtime log at 2026-10-10T11:19:08Z reports: `CC: Session Layer selected; 22 persistent layers protected.` This covers loaded persistent layers including the root; visual UI acceptance and subsequently loaded dependencies were not checked. Existing application windows and their unsaved edits were left open. The application also reported remote sample-thumbnail upload errors. No test suite was run.

Jan's screenshots exposed an unintended root-within-root structure in Manual and review entrypoints. Updated the generator and migrated World_Manual, World_MaskedSize and World_MaskedSelection through Sdf: each now owns the supplied startup baseline and directly composes its work layers, with optional ReviewLyr strongest and GeoLyr weakest. Original wrappers/profile/expected/report are retained in evidence/before_direct_scene_roots. Updated profile stacks and marked the previous manifest observations/file inventory historical. No scene flattening or asset hierarchy migration was used. Persistent lock metadata and session authoring policy remain; Kit runtime confirmation is pending. Screenshots show unsaved application edits; disk correction does not incorporate those live edits.

Updated 2026-10-10 after adding the source-editing and composition-workbench roadmap. Draft 0.1.1.

## Composition workbench roadmap

Recorded Monaco Editor as an implementation/functionality candidate for CW-05 after bounded source inspection of AI Harness Control Center's Studio File Editor. Its separate diff library/custom inline review are distinguished from Monaco. A proposed Kit web-panel/bridge architecture requires an embedding feasibility assessment; no integration, dependency adoption or source-code copying has occurred.

CW-05 also includes requested search and replace: selection/current-buffer scope, single/all replacement, case/word/regex options, match preview and undo. Cross-layer replacements need an explicit batch plan; text substitution is distinguished from semantic namespace editing.

Added CW-05 Embedded USDA Scene Editor at Jan's request: a dockable internal ASCII scene panel, inspired by his Houdini comparison, with authored-layer navigation and editing. The roadmap defines buffer/Apply/Save states, parsing, revision reconciliation, locks, undo, representation/format boundaries and proposed acceptance. This is scene-description editing, not a script console. Documentation only; no application implementation or tests were performed.

Jan further requested bulk cleanup scripts with confirmation breakpoints when moves are unclear. The roadmap and tooling requirements now specify versioned recipes, authorized bulk execution for explicit mappings, scoped decision checkpoints for ambiguous groups, resumable plans, stale-input checks and unattended needs-decision reports. No cleanup scripts have been implemented in this documentation increment.

Added four requested features to ROADMAP.md: CW-01 Open Original Layer Source, CW-02 Open Referenced Asset With, CW-03 Opinion Inspector and Routing, and CW-04 Contract-Guided Bulk Migration. Each includes user actions, definitions still needed, side effects and proposed acceptance. The preferred asset editor is a separate custom Omniverse instance with a lighter alternative renderer; no renderer/build has been selected or verified. Source identity, dirty-state reconciliation, shared-source impact, semantic delta classification, exact variant destinations, selective moves, recovery and evaluation are explicit requirements. TOOLING_REQUIREMENTS.md links these adapters to DT-01–09.

This increment changes roadmap documentation only. No implementation, source cleanup, tests or application checks were performed. Next planning work is to agree source/resolver support, application presets, inventory/plan schemas and bounded acceptance fixtures before implementing these features.

## Purpose and shared evaluation

Jan requested that README.md introduce the project through his OpenUSD journey and its purpose, replacing the opening focus on named reviewers. It now defines scalable composition from assets into nested assemblies and scenes, with control at the rightful ownership level. Jan clarified that the contract itself is the eval for agents and other humans: compare results against the applicable contract/profile, then revise the work until it fits. The README records that loop, maps the stated requirements to existing CC/DT provisions, and explains its role in consistent work across tasks, projects, repositories and agents. The compact paradigm diagram and version 0.1.1 remain.

Concept review used the current ownership/interface rules, CC-12 acceptance requirements, CC-17–19 deterministic execution/evidence requirements, CC-20–25 profiles and boundaries, the DT requirements, and the example's profile/expected outcomes. These support the stated direction. Remaining work is to define scenario-specific evaluation inputs, pass/fail criteria and scale/performance limits, then implement and execute the agreed evaluations. The existing example/default observations do not establish broad scalability or automated conformance. This was a documentation and concept review; no USD/code changes, tests or new acceptance runs were made in this step.

## README paradigm overview

Jan requested a simpler version of the paradigm in README.md. A new section near the top gives the core idea, a compact left-to-right Mermaid chart (root → vertical scene layers → reusable sources), the bottom GeoLyr position, session-authoring/persistence guidance, and links to the detailed ownership diagram and project structure. The detailed charts retain their full content. The README diagram was rendered with Mermaid 11.4.1 and visually inspected; no USD files, runtime behavior or acceptance results changed in this documentation step. No tests were run.

## Current version and stack clarification

Jan corrected the current version to **0.1.1** and confirmed the root-plus-stack paradigm: GeoLyr is the bottom (weakest) scene sublayer, with other scene contributions above it. Jan then clarified that the overall diagram must remain left-to-right and retain the original explanatory detail. The Mermaid charts in CompositionContract.md and PROJECT_STRUCTURE.md now show three columns: root/authoring, vertical scene stack, and reusable sources. They restore asset geometry/intrinsic transforms/materials/variants, assembly-owned child choices, material-library links, optional work roles, review exceptions and owner/variant-context guidance. The existing DataLyr → TransLyr → VariLyr → GeoLyr order is numbered; optional and review roles use dashed rows. CC-23 records the bottom-GeoLyr convention; the profile still declares the relative order above it.

The SVG memory chart is exported from the detailed Mermaid source. A headless Mermaid 11.4.1 render was visually inspected: root left, vertical stack middle with GeoLyr lowest, reusable sources right, and all column titles and role descriptions visible. Edges connect the column subgraphs to preserve their independent vertical layout; their labels name the actual contributing layer. This is diagram preview evidence, not USD or Kit acceptance.

Current prose, generator/profile labels and the `cc:profile` custom metadata in all 29 active USD layers now use 0.1.1. USD metadata was updated through Sdf APIs; sublayer order, geometry, transforms, variants, template content and session defaults were retained. The current build manifest refreshes file identities and explicitly carries forward its earlier USD observations. Its original bytes are preserved in `harness/evidence/build_before_version_0.1.1.json`; earlier evidence, including `source_review_0.2.json`, keeps its original labels. No tests, new stage read-back or Kit/renderer acceptance were run for this correction.

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

- CompositionContract.md moved here as the authoritative draft, with CC-01 through CC-23 preserved.
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
- Added CC-08a and a CC-23 clarification for the placement-to-scenario promotion lifecycle: preserve the original TransLyr for provenance, author complete layouts in variants, exclude only superseded unconditional placement opinions, preserve unrelated transforms, document the migration, and evaluate every promoted variant after reopen. The contract permits profile-declared exclusion, persistent muting, or layer splitting; it does not treat a note or mute alone as proof of a complete migration.
- Extended CC-08a with a selective ownership example: a shared MatLyr can retain Cube → Blue while Cone material bindings move into Cone VariLyr (Blue/Red/Green), with only the active unconditional Cone binding cleared, excluded or split. The same prim/property-level rule applies to transforms; whole-layer disabling is reserved for fully superseded layers.
- Use centimetres, Z-up and `/World` for the new example. The inspected generated predecessor uses Y-up and `/world`; it was not converted or edited.
- Keep predecessor projects and the initial HANDOVER.md intact. New USD content and the authoring script were created here; no private pipeline content was accessed or copied.
- `.gitignore` excludes Python caches and local virtual environments. Shell policy rejected deletion of the generated `tools/__pycache__` cache; it was left ignored. A concurrently present `COMPOSITION_MEMORY_CHART.svg` was preserved and is not attributed to this task.

## Continuity

The origin was a TutorialBuilder discussion of local opinions masking variants. It developed into explicit ownership at asset/assembly/scene scopes, separate layer roles and deterministic inspection/repair requirements. The independent project enables focused feedback from Nandu, Dylan and the AOUSD IEDT group while leaving future GoodStart/workcell integration open. Their review or acceptance has not occurred here.

## 2026-10-10 — Authority terminology routing

Authorized cross-repository routing improvement after the manual-only lofting
lookup missed Pixar's full API snapshot. GoodStart's authority router now offers
`lookup TERM`, bounded excerpts across spec/manual/full, per-source counts and
hashes, and a retrieval-hint index containing payload lofting. The route fallback
and both repositories' agent guidance now include unresolved terminology.
Hints record term occurrence separately from formal definition; no new normative
vocabulary or AOUSD conformance claim was introduced. Existing unrelated
GoodStart changes were preserved. Source/diff inspection only; no tests or
execution of the new lookup command performed. Runtime validation remains
pending. No scene, diagram, bundle, commit or publication changes in this task.

## 2026-10-10 — Launcher explanation
Added a brief explanation beside the sample README launch command: new Kit process, bundled Python helper, Opinion target, in-memory layer protection, UI setting changes/restoration, no automatic USD save or Windows policy change, ordinary Kit logs/caches/preferences, and direct-open alternative. Read both launcher and helper; neither executed. No tests run.

## 2026-10-10 — Setup and project README separation
Outer README_SETUP.md now documents manual extraction/copy, direct PowerShell setup and batch setup, destinations and process-only execution-policy bypass. Canonical setup text lives in tools/setup/README_SETUP.md and is copied by the builder. Inner README.md covers opening/using scenes and distinguishes setup from Kit launch. Removed generated START_HERE.md from new archives. Rebuilt the portable ZIP (106 files); inspected archive entry names and confirmed its README bytes match the example README. No installer, Kit or tests run. Previously extracted folders are not changed and may retain their old START_HERE.md.

## 2026-10-10 — Scene guide navigation and walkthroughs
Numbered the three project setup options in the scene README, changed the scene chooser to internal heading links, and replaced the folder table with an ASCII directory tree. Added goal/ownership/graph walkthroughs for all six scenes in the documentation generator so regeneration preserves them. Regenerated documentation from saved USD and rebuilt the 106-file portable ZIP. Mermaid/SVG presentation retained. No tests or Kit run.

## 2026-10-10 — Extracted-project README scope correction
Removed extraction/setup options and setup cross-instructions from the inner scene README. It now starts with choosing among existing scenes and opening them in Kit. Outer README_SETUP.md retains all three setup options. Rebuilt the portable ZIP with the corrected README. No tests or Kit execution.

## 2026-10-10 — Kitchen Set comparison (read-only)

Inspected the user-supplied Kitchen_set package using Sdf across 230 USD files
(76 asset packages) and Usd.Stage with LoadNone/LoadAll for both entrypoints.
Each root has 425 reference sites, 76 unique asset targets, no sublayers and
placement authored directly alongside references/variant selections. The
instanced entrypoint has 425 instanceable sites and composed 114 prototypes.
Observed 21 asset interfaces with variant sets; Nail publishes empty NailA/NailB
branches above its payload while geometry supplies implementation. Unloaded
stages retain the variant names: actual payload lofting. Both roots used 78
layers with LoadNone and 230 with LoadAll, including the anonymous session.
These are composition observations, not memory/speed benchmarks. No Physics
attributes/applied schemas, Material/Shader prim types, or time samples were
found in the authored-file scan; displayColor supplies appearance (Book sampled).
Roots author Z-up but omit metersPerUnit; USD resolved fallback 0.01. Geometry
includes legacy export IDs/primvars; no industrial identity-binding contract
was established. Reader emitted crate 0.7.0 deprecation warnings. No migration,
rendering, simulation, edits to Kitchen_set or acceptance tests occurred.

Interpretation: published visual set demonstrates reference/payload interfaces,
lofting and optional instancing beyond our starter's current implementation.
Our role separation adds authoring ownership and proposed identity/runtime
contracts; reserved role layers do not establish robotics readiness. Recommend
preserving imported internals and adding purpose-specific integration layers;
selective instancing/payload boundaries should follow required access and
physics topology. No contract changes adopted by this analysis. GoodStart's
new lookup was used for lofting: spec/manual no match, full one term occurrence;
this establishes a successful lookup observation, not a router test suite.

## 2026-10-10 — Lofting, extensive instancing and driven formations

User authorized new samples/contracts from the Kitchen comparison, then requested
extensive instancing, variant diversity and separate code-driven formation scenes.
Added SceneROOT_Lofted, Instanced, Instanced_Wave, Instanced_Spiral and Instanced_Rings.
Each is a direct root with its own Opinion; the three formations own Trans/Vari
and share Instanced Geo plus original Data. Lofted contains five shapes; each
Instanced scene adds 1024 sites (32 x 32, half Cube/half Cone), for 1029 shape sites.
Shape Asset prims are instanceable; assembly and occurrence parents stay editable.
Three new lightweight interfaces payload ContentsLyr aggregates referencing our
existing role files; the original source variants/geometry/materials stay shared.
Source demo Opinion layers are excluded; lofted interfaces have their own Opinions.
No Kitchen assets or code were copied, migrated or modified.

Added tools/add_scalable_examples.py (bounded USD author, explicit replacement flag)
and portable _workflows/arrange_instances.py. The latter maps 1024 JSON values in
[0,1] to TransLyr placement/heading and VariLyr Size/Finish choices. Default is plan
only; --apply writes the named derived scene, two roles and preserved/new Opinion.
It keeps prior bytes plus input/plan locally and attempts rollback on ordinary write
errors. Backups are ignored by Git and excluded from the portable archive. Hard
process termination is not a cross-file transaction; backups support recovery.
The bundled signal is synthetic; all 18 shape/size/finish configurations were emitted
by each formation run. These are static snapshots, not animation/live integration.

Expanded CC-05 with CC-05a/b/c (load evidence, native sharing boundaries, generated
writer/input contracts) and the asset-interface checklist; updated both READMEs,
PROJECT_STRUCTURE, profile links and launcher scene choices. Added exact diagrams
and walkthroughs for all 11 scenes; instancing graphs aggregate the 1024 sites into
two explicitly counted groups. README remains Mermaid/SVG. Rebuilt starter ZIP
with all new scenes, driver and data (154 files; inventory is packaging evidence).

Executed authors/driver with usd-core 26.8 and generated documentation by opening
saved stages at default LoadAll; Mermaid CLI rendered all 11 reuse SVGs. Authoring
API and profile-serialization errors were corrected while generating; no original
source-role files were changed. No tests, variant sweep, benchmark, Kit viewport,
new-scene unloaded inspection or robotics validation ran. Scene placement extends
beyond the standard camera/ground; frame /World/InstanceGrid in Kit. Prototype
counts/performance are not claimed. Load/unload locks, source-interface sync,
relative-path relocation and host authoring persistence remain acceptance work.
