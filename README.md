# OpenUSD GoodStart Composition Contract

**Version 0.2.0 — independent work-in-progress proposal and local example · 2026-10-11**

This project grew out of my journey into OpenUSD. I have spent a lot of time thinking about asset structures, how they compose, and what makes them useful. That led me to a more precise starting point: **a structure needs a purpose, requirements and an evaluation standard before we can judge how well it works.**

The questions guiding this work are: **What is the structure for? What must it support? How will we know it still works as complexity grows?**

The goal is a scalable, ascending USD composition structure: assets form assemblies, assemblies nest inside larger assemblies, and scenes combine them. Each level keeps control close to the owner of the decision and exposes the controls its consumers need. We want to represent complex systems, reuse them across a wide range of scenarios, and preserve their intended behavior as they grow and change.

Industrial digital twins and physical AI bring important requirements to this work: identifiers must remain meaningful as structures change, responsibilities must stay clear across systems, and integrations must remain stable throughout development. We are exploring how to incorporate Aaron Luk's [Separation of Concerns for Identifiers in USD](https://github.com/PixarAnimationStudios/OpenUSD-proposals/pull/105) proposal and the Microsoft/NVIDIA [Composable Bindings](https://aka.ms/ComposableBindings) concepts, with contributors Christoph Berlin and Aaron Luk, into our contracts.

These ideas help us specify identity continuity and adaptable connections between systems, then evaluate whether a composition preserves them through change. Their integration into this project is ongoing; see [CC-27/28](CompositionContract.md#23-identity-and-composable-bindings) for the current requirements and implementation boundaries.

### Industry requirements and reusable assets

A robot packaged using NVIDIA's [Asset Structure 3.0](https://docs.isaacsim.omniverse.nvidia.com/6.0.0/openusd_tuning_tutorials/tutorial_02_asset_structure.html) enters our composition **as a reusable asset**. Its internal geometry, materials and physics configuration stay with that package. Our focus is the larger digital twin: robot → workcell → production line → facility, with clear interfaces and control at each level.

[SimReady Foundation](https://github.com/NVIDIA/simready-foundation) supplies use-case requirements for incoming simulation assets. Our [asset-interface checklist](CompositionContract.md#asset-interface-checklist) now requires purpose, entrypoint, coordinates, dependencies, public controls and evidence, including selected simulation profiles where applicable. [Asset and assembly acceptance](CompositionContract.md#asset-and-assembly-acceptance) evaluates both incoming packages and their composed use. Asset readiness alone does not establish workcell readiness; automated integration remains planned.

We also track [OpenUSD proposals](https://github.com/PixarAnimationStudios/OpenUSD-proposals/tree/main/proposals), especially validation, profiles/capabilities, namespace editing, LOD and spline animation. Their practical implications and adoption gates are in the [roadmap](ROADMAP.md#upstream-integration-priorities).

This work is informed by discussions around the **AOUSD Industrial and Engineering Digital Twin (IEDT) workcell effort**, which Jan expects to develop into a guideline project. The public [AOUSD interest-group remit](https://aousd.org/community/interest-groups/) supports industrial requirements and recommendations; the workcell's formal status and this project's participation remain to be confirmed. This repository is an independent proposal.

For a concrete comparison, see Nandu Vellal's [Workcell Digital Twin](https://github.com/nAurava-Technologies/Workcell-DigitalTwin) project and [Naurava Technologies](https://www.naurava.com/). We propose evaluating the current workcell against this composition contract: what its structure could look like under the proposed paradigm, how its current approach differs, and which requirements should be adapted. The workcell project is likely to move to AOUSD's GitHub in the near future; this is an anticipated move, not a confirmed transfer or endorsement of this proposal.

## The contract is the eval

Composition contracts define **what we want, why we want it, and how the result must behave**. They connect requirements to ownership, public interfaces, authoring rules and expected outcomes.

**The contract is the shared evaluation standard for agents and humans.** We compare the result against the applicable contract and project profile, identify mismatches, and revise the work until it fits, or works. A profile states which scenarios, operating modes and requirements apply to that project.

**Purpose → requirements → contract → compose or change → evaluate → revise until the contract is met.**

When the purpose or requirements change, revise the contract explicitly and evaluate the affected results again. A change to the evaluation standard should be traceable, just like a change to the scene.

## The paradigm

**The root combines the layers. Scene layers place and configure linked assets. Assets own their reusable content.**

```mermaid
%%{init: {"flowchart": {"wrappingWidth": 280, "nodeSpacing": 20, "rankSpacing": 24}}}%%
flowchart LR
    accTitle: OpenUSD GoodStart Composition Contract 0.2.0 - The paradigm
    accDescr: Root on the left, vertical scene layers in the middle with GeoLyr at the bottom, and reusable assemblies, assets and materials on the right.
    R["SceneROOT_Example.usda<br/>Combines the scene layers"]

    subgraph STACK["SCENE LAYER CLASSES"]
        direction TB
        RT["RUNTIME LAYER<br/>RuntimeLyr · operational snapshots<br/>Optional live-state contribution"]
        S["SIM LAYER<br/>SimLyr · published simulation results"]
        D["DATA LAYERS<br/>DataLyr · IdentityLyr · ContextLyr<br/>Optional UNSMappingLyr"]
        BASE["BASE LAYER<br/>MatLyr · materials<br/>TransLyr · placement<br/>VariLyr · choices and scenarios<br/>Optional Env / Light / Cam / Render / Anim / Physics / Rig roles<br/>GeoLyr · asset links · BOTTOM"]
        RT ~~~ S
        S ~~~ D
        D ~~~ BASE
    end

    subgraph SRC["ASSET USD · reusable sources"]
        direction TB
        B["Assemblies<br/>Arrange and configure child assets"]
        A["Assets<br/>Own geometry, materials and variants"]
        M["Material libraries<br/>Shared shader definitions"]
        B -->|reference| A
        A -->|reuse| M
    end

    R -->|sublayers| STACK
    STACK -->|"GeoLyr references assets / assemblies"| SRC

    classDef root fill:#fde8df,stroke:#d99b84,color:#17212b,stroke-width:2px
    classDef layer fill:#dceef9,stroke:#91bfd8,color:#17212b
    classDef optional fill:#f4f9fc,stroke:#91bfd8,color:#334155,stroke-dasharray:6 4
    classDef base fill:#dceef9,stroke:#1685bd,color:#17212b,stroke-width:3px
    classDef asset fill:#ffffff,stroke:#9db9c8,color:#17212b
    class R root
    class D layer
    class RT,S optional
    class BASE base
    class B,A,M asset
    style STACK fill:#f8fcff,stroke:#84c83d,stroke-width:3px
```

Read **left to right**. Four class boxes list their layer types; they do not introduce aggregate USD layers. SIM and RUNTIME are optional, with strength set by the profile. The baseline remains DataLyr → TransLyr → VariLyr → GeoLyr, with **GeoLyr at the bottom**. An optional REVIEW / ReviewLyr contribution holds explicit experiments above that baseline.

**Work in Opinion by default**, with persistent work/source layers locked, using the [Kit launcher](examples/01_LayeredScene/Open_In_Kit.ps1). Saving Opinion retains experiments; promote accepted fields to their rightful owner and variant branch, then retire superseded opinions.

The active root remains writable for Kit's camera and authoring-target metadata;
it is not the default editing destination. See the [CC-01 host exception](CompositionContract.md#3-file-ownership-contract).

See the [detailed ownership diagram](CompositionContract.md#composition-memory-chart) and [project structure](PROJECT_STRUCTURE.md) for the full responsibilities and example setup.

## Requirements and evaluation

Our entrypoint term is **Root** (`SceneROOT_<Purpose>.usda`); **scene** means its composed result. All active scene entrypoints now follow this convention (CC-26). The diagrams use the same classes as storage: **ASSET USD** for reusable packages, **BASE** for authored setup, **SIM** for simulation results, **RUNTIME** for live state/snapshots, **DATA** for identity/context, and **REVIEW** for experiments. Inside those classes, role names remain `GeoLyr`, `TransLyr`, `VariLyr`, etc. Class labels add no layers and impose no strength order. See the [classification table](CompositionContract.md#naming-and-classification). Use the exact directory names `040_DATA_LYR` for DATA and `050_REVIEW_LYR` for REVIEW. All layer-class folders use singular `_LYR`; this convention repeats inside locally authored assets and assemblies and in starter packages.

The current concept supports this direction through recursive ownership, published interfaces, explicit layer responsibilities and recorded expected behavior. These are the connections we need to evaluate:

| Requirement | Existing contract basis | Evidence needed |
|---|---|---|
| Represent nested, reusable structures | CC-03/04/13/14: asset interfaces and assembly ownership | Repeated assets and nested assemblies keep their controls working at the intended scope. |
| Keep control close to its rightful owner | CC-02/06–11/16/21: role, owner and variant context | Placement, configuration and material changes reach the intended owner; independent occurrences and variant behavior remain intact. |
| Reuse the approach across scenarios | CC-20/23–25: required roles, profiles and dependency boundaries | Each supported scenario declares its writers, overlaps and dependencies, and produces its specified result. |
| Preserve intended behavior through edits | CC-01/12/19: persistence, acceptance and controlled changes | Edits reach the intended layer/context, survive deliberate save/reopen, and produce the declared before/after behavior. |
| Make work repeatable across agents and people | CC-17–19 and DT-01–09: deterministic inspection, execution and evidence | The same declared inputs yield consistent findings; changes and their evaluation results can be traced to a contract revision. |

Each evaluation case needs named inputs, the applicable contract/profile revision, the expected outcome and a clear pass/fail criterion. Scalability also needs agreed nesting depths, asset counts, load states and performance limits for the intended applications. These criteria turn the shared contract into something people can review and tools can check repeatedly.

**The design fits this purpose; broad validation remains open.** The current example supplies a small nested assembly, independent asset occurrences, expected outcomes and deliberate conflicts. Its recorded observations cover saved defaults. Complete variant and persistence evaluation, larger nesting/scale cases, other operating profiles and repeatable automated evaluation remain to be established. See [sample acceptance](CompositionContract.md#9-harness-and-sample-acceptance) and the [expected outcomes](examples/01_LayeredScene/_contracts/expected.json).

## Working with agents

**Identity and integration:** IdentityLyr records who an occurrence represents, usually on its placement prim rather than every mesh. Asset source IDs, assembly/scene occurrence IDs and physical-instance IDs have different owners and scopes. Composable bindings use those identities to map external data to explicit USD properties and authoring contexts. See [CC-27/28](CompositionContract.md#23-identity-and-composable-bindings) for placement guidance, examples and planned evaluation; no binding engine or standardized identifier schema is implemented here.

The same contract gives different agents and human contributors a common basis for work across tasks, projects and repositories. Each task can identify its purpose, applicable profile, permitted scope, required outputs and evaluation criteria. The result carries evidence that another agent or person can review, and work continues until the applicable criteria are satisfied.

The intended workflow combines model interpretation with deterministic USD-aware operations and recorded evaluation results. General inspection, repair and workflow automation remain planned capabilities; the [tooling requirements](harness/TOOLING_REQUIREMENTS.md) describe the execution and reporting needed to maintain quality as this expands.

## Start here

- [Composition contracts](CompositionContract.md): the evolving proposal and stable CC rule IDs.
- [Open the example guide](examples/01_LayeredScene/README.md): manual configuration, scene scenarios and two deliberate conflicts.
- [Animated MoGraph proof of concept](examples/01_LayeredScene/README.md#play-and-control-the-mograph-scene): under development. Follow the Mermaid data/runtime/USD/render flow, saved-clip fallback and current reload limitation; JSON is a local mock source for a future incoming-data adapter.
- [Project structure and diagram](PROJECT_STRUCTURE.md): the revised paradigm, storage layout and edit destinations.
- [Open questions](DISCUSSION.md): the first review agenda.
- [Roadmap](ROADMAP.md): from discussion to deterministic inspection and pipeline experiments.
- [Agent entry](AGENTS.md): bounded context and working instructions.
- [Next-agent handover](harness/HANDOVER.md): brief history, working decisions and implementation boundaries.
- [Harness governance](harness/GOVERNANCE.md) and [workflow](harness/WORKFLOW.md).
- [Deterministic tooling requirements](harness/TOOLING_REQUIREMENTS.md).
- [Source and dependency routes](harness/SOURCES.md).
- [Resume state](harness/STATE.md): what exists and the next useful step.

## Starter master preset

The same package layout repeats inside locally authored assets and assemblies. Open `AssetROOT_Cube.usda`, `AssetROOT_Cone.usda` or `AssetROOT_DisplayPair.usda` to work at that owner's scope: BASE roles remain in `020_BASE_LYR`, and each package has its own Opinion in `050_REVIEW_LYR`. A building used in a city is also an asset; object type does not change the root naming rule. Working scenes use `SceneROOT_<Purpose>.usda`. See [recursive package rules](CompositionContract.md#recursive-package-layout).

**Copy-and-run setup:** copy the entire [portable setup folder](starter/Composition_Starter_0.1.1/README_SETUP.md) into your destination and double-click `Create_Composition_Project.bat`. It expands the bundled scenes, assets, layers and launch helper into that folder. Windows PowerShell is sufficient; setup needs no Python or network access. Existing files are never overwritten. Omniverse remains a separately installed prerequisite for the Kit launcher.

[SceneROOT_STARTER.usda](examples/01_LayeredScene/SceneROOT_STARTER.usda) is deliberately generous: demo assets, independent placement/variant/data layers, an Opinion layer, and optional material, environment, lighting, camera, render, animation, rig, physics, simulation and runtime slots. Remove or disable unused contributions. Launch with `Open_In_Kit.ps1 -Scene STARTER`. See the [starter guide](examples/01_LayeredScene/README.md#starter-master-preset).

## Current scope

The contract was moved from TutorialBuilder. Its VariantSetups paper and A–H scenes remain there; they are exploratory evidence, not conforming examples shipped by this project. See [provenance](harness/SOURCES.md). The new `examples/01_LayeredScene` package develops those experiments and the numbered storage structure inspected in `USD_GoodStart/_Generated_Test`.

Start with [SceneROOT_Example.usda](examples/01_LayeredScene/SceneROOT_Example.usda), Jan's supplied Omniverse starting scene with the example assets composed under `/World`. The package contains demo and starter layers, Cube/Cone packages, a nested DisplayPair assembly, shared asset materials, scene contributions, data, explicit review exceptions and draft JSON contracts. The supplied environment, viewport cameras and render state remain the startup baseline. Its two textures are bundled; OmniPBR and RTX features require a compatible Omniverse application. `SceneROOT_Manual.usda` is an independent root with the same direct work-layer stack.

[tools/build_example.py](tools/build_example.py) reproduces this setup from the retained [Omniverse template](templates/Omniverse/README.md) through OpenUSD 26.08 APIs. Default-entrypoint read-back is recorded; full acceptance and Omniverse review are pending. No general inspector, repair engine, ownership-routing extension or pipeline integration is implemented.

### Payload interfaces and extensive instancing

The [scene guide](examples/01_LayeredScene/README.md#choose-a-scene) now includes **Lofted**, **Instanced**, **Instanced_Wave**, **Instanced_Spiral** and **Instanced_Rings**. Lightweight public variants sit above payloads; shape contents reuse our existing Cube/Cone implementations. Instanced scenes contain 1,029 shape occurrences. The three driven formations map JSON inputs to placement and nine Size/Finish combinations per shape type. Each scene owns its Opinion and generated work layers; root files directly compose those layers.

These examples adapt the Kitchen Set's packaging ideas using our own sources. CC-05a–c define loading, instancing boundaries and input-driven ownership. The bundled Python driver shows its plan before an explicit apply and preserves backups. This demonstrates authoring patterns; measured performance, physics readiness and Kit acceptance remain pending.

The default working state selects the editable Opinion layer and locks persistent work/source layers. Use [Open_In_Kit.ps1](examples/01_LayeredScene/Open_In_Kit.ps1) for edit-target selection and layer protection. The updated startup behavior awaits Kit acceptance.

OpenUSD-GoodStart remains a knowledge reference and potential consumer. TutorialBuilder remains a teaching consumer. The private `OpenUSD_GoodStart_Pipeline_nodes` repository is a candidate backbone for a future composition pipeline, subject to interface and suitability review. This project must remain understandable and eventually inspectable without that private dependency.

## AI assistance disclosure

This project was developed with the assistance of AI tools, including OpenAI Codex, for research support, drafting and refining documentation, and developing code and examples. Human contributors remain responsible for project decisions, review and verification. AI-assisted content may contain errors or omissions; claims and examples should be evaluated against the cited sources and composition contracts. Only explicitly recorded checks should be treated as verified results.

## Participation

Propose changes with a purpose, requirements, the relevant CC rules, an example and criteria for evaluating the result. Compare alternatives against those criteria and record evidence, uncertainty and counterexamples. Feedback from people exploring different OpenUSD workflows will help refine both the contracts and their evaluations. See [contribution guidance](CONTRIBUTING.md).

Remote hosting, access grants, licensing and any future transfer to a group or workcell project remain to be decided. Local project creation does not publish this material or grant rights to external source content.
