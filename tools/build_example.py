"""Author the bounded CC layered-scene example using OpenUSD 26.08.

Creates a new directory only. This is an example author, not a scene repair tool,
contract validator, or general project generator. No existing USD is modified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil

from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade, UsdUtils


PROFILE = "CC-EXAMPLE-01/0.1.1"
TEMPLATE = Path(__file__).resolve().parents[1] / "templates/Omniverse/ROOT_example.usda"
TEMPLATE_TEXTURES = {
    "/Environment/Sky.inputs:texture:file": "CarLight_512x256.hdr",
    "/Environment/Looks/Grid/Shader.inputs:diffuse_texture": "ov_uv_grids_basecolor_1024.png",
}
COLORS = {"Red": (0.65, 0.035, 0.025), "Blue": (0.025, 0.18, 0.65),
          "Yellow": (0.85, 0.52, 0.025), "Ground": (0.18, 0.2, 0.22)}
INSTANCES = {
    "Cube01": ("USD_Wrappers/AssetROOT_Cube.usda", (-220, 0, 0)),
    "Cube02": ("USD_Wrappers/AssetROOT_Cube.usda", (0, 0, 0)),
    "Cone01": ("USD_Wrappers/AssetROOT_Cone.usda", (220, 0, 0)),
    "Pair01": ("Assemblies/DisplayPair/AssetROOT_DisplayPair.usda", (0, 0, -260)),
}


class Author:
    def __init__(self, root: Path):
        self.root = root
        self.roles = []

    def path(self, relative):
        p = self.root / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def text(self, relative, value):
        self.path(relative).write_text(value.rstrip() + "\n", encoding="utf-8")

    def json(self, relative, value):
        self.text(relative, json.dumps(value, indent=2, sort_keys=True))

    def layer(self, relative, role, owner, context="unconditional"):
        stage = Usd.Stage.CreateNew(str(self.path(relative)))
        stage.GetRootLayer().customLayerData = {
            "cc:profile": PROFILE, "cc:role": role,
            "cc:owner": owner, "cc:context": context,
        }
        self.roles.append({"file": relative, "role": role, "owner": owner,
                           "context": context})
        return stage

    def root_layer(self, relative, default_prim, sublayers, owner):
        stage = self.layer(relative, "Root", owner)
        layer = stage.GetRootLayer()
        template = Sdf.Layer.FindOrOpen(str(TEMPLATE))
        layer.defaultPrim = default_prim
        layer.subLayerPaths = sublayers
        UsdGeom.SetStageMetersPerUnit(stage, template.pseudoRoot.GetInfo("metersPerUnit"))
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
        stage.SetTimeCodesPerSecond(60)
        if Path(relative).name.startswith("AssetROOT_"):
            preview_environment(self, stage)
        layer.Save()
        return stage



def preview_environment(a, entrypoint):
    """Compose portable preview content beside, never below, the default asset prim."""
    relative = "010_ASS_USD/Envs/OmniverseStandard/Environment.usda"
    target = a.path(relative)
    if not target.exists():
        source = Path(__file__).resolve().parents[1] / "examples/01_LayeredScene" / relative
        shutil.copyfile(source, target)
        resources = source.parent / "Resources"
        shutil.copytree(resources, target.parent / "Resources", dirs_exist_ok=True)
    layer = entrypoint.GetRootLayer()
    preview = Path(os.path.relpath(target, Path(layer.realPath).parent)).as_posix()
    if preview not in layer.subLayerPaths:
        layer.subLayerPaths.append(preview)


def save(stage):
    stage.GetRootLayer().Save()


def trs(stage, path, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
    xform = UsdGeom.Xformable(stage.OverridePrim(path))
    xform.AddTranslateOp().Set(Gf.Vec3d(*translate))
    xform.AddRotateXYZOp(UsdGeom.XformOp.PrecisionDouble).Set(Gf.Vec3d(*rotate))
    xform.AddScaleOp(UsdGeom.XformOp.PrecisionDouble).Set(Gf.Vec3d(*scale))


def select(stage, path, choices):
    prim = stage.OverridePrim(path)
    for name, choice in choices.items():
        prim.GetVariantSets().GetVariantSet(name).SetVariantSelection(choice)


def reference(stage, path, source, source_prim=None, type_name="Xform"):
    prim = stage.DefinePrim(path, type_name)
    if source_prim:
        prim.GetReferences().AddReference(source, source_prim)
    else:
        prim.GetReferences().AddReference(source)
    return prim


def material_library(a):
    stage = a.layer("010_ASS_USD/MatLib/Palette_v001.usda", "MatLyr", "library:Palette@1")
    UsdGeom.Scope.Define(stage, "/Materials")
    stage.SetDefaultPrim(stage.GetPrimAtPath("/Materials"))
    for name, color in COLORS.items():
        mat = UsdShade.Material.Define(stage, f"/Materials/{name}")
        shader = UsdShade.Shader.Define(stage, f"/Materials/{name}/Surface")
        shader.CreateIdAttr("UsdPreviewSurface")
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*color))
        shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.35)
        shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0)
        shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)
        mat.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
    save(stage)


def recursive_package_notes(a, prefix, owner):
    opinion_layer(a, f"{prefix}/050_OPINION_LYR/OpinLYR_default.usda", owner)
    for lane in ("000_SOURCE", "010_ASS_USD", "030_SIM_LYR", "035_RUNTIME_LYR", "040_DATA_LYR", "_contracts"):
        a.text(f"{prefix}/{lane}/README.md", f"# {lane}\n\nReserved at {owner} scope. Add content only when required; a folder does not create a composed layer.")
    a.text(f"{prefix}/README.md", f"# {owner}\n\nOpen AssetROOT_<Name>.usda. 020_BASE_LYR holds owned roles; 050_OPINION_LYR holds Opinion experiments. Package edits affect all consumers. Scene experiments belong in the scene Opinion. Other class directories are reserved. External asset/material dependencies retain relative links.")


def shape_asset(a, name):
    prefix = "010_ASS_USD/USD_Wrappers"
    owner = f"asset:{name}@1"
    base = f"/{name}"
    stage = a.layer(f"{prefix}/AssetROOT_{name}.usda", "Leaf", owner)
    root = UsdGeom.Xform.Define(stage, base).GetPrim()
    Usd.ModelAPI(root).SetKind("component")
    if name == "Cube":
        geom = UsdGeom.Cube.Define(stage, base + "/Geometry")
        geom.CreateSizeAttr(100)
    else:
        geom = UsdGeom.Cone.Define(stage, base + "/Geometry")
        geom.CreateHeightAttr(100)
        geom.CreateRadiusAttr(50)
        geom.CreateAxisAttr("Y")
    geom.CreateExtentAttr([Gf.Vec3f(-50, -50, -50), Gf.Vec3f(50, 50, 50)])
    save(stage)

    trs(stage, base + "/Geometry", translate=(0, 50, 0))
    save(stage)

    stage.OverridePrim(base)
    UsdGeom.Scope.Define(stage, base + "/Looks")
    for finish in ("Red", "Blue", "Yellow"):
        mat = UsdShade.Material.Define(stage, base + f"/Looks/{finish}")
        shader = UsdShade.Shader.Define(stage, base + f"/Looks/{finish}/Surface")
        shader.CreateIdAttr("UsdPreviewSurface")
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*COLORS[finish]))
        shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.35)
        mat.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

    save(stage)

    prim = stage.OverridePrim(base)
    sizes = prim.GetVariantSets().AddVariantSet("Size")
    for choice, scale in {"Normal": (1, 1, 1), "Large": (2, 2, 2), "Tall": (1, 1, 2)}.items():
        sizes.AddVariant(choice)
        sizes.SetVariantSelection(choice)
        with sizes.GetVariantEditContext():
            UsdGeom.Xformable(prim).AddScaleOp(UsdGeom.XformOp.PrecisionDouble).Set(Gf.Vec3d(*scale))
    sizes.SetVariantSelection("Normal")
    finishes = prim.GetVariantSets().AddVariantSet("Finish")
    for finish in ("Red", "Blue", "Yellow"):
        finishes.AddVariant(finish)
        finishes.SetVariantSelection(finish)
        with finishes.GetVariantEditContext():
            geometry = stage.OverridePrim(base + "/Geometry")
            # The leaf owns its material and conditional binding in this same file.
            UsdShade.MaterialBindingAPI.Apply(geometry)
            geometry.CreateRelationship("material:binding", custom=False).SetTargets(
                [Sdf.Path(base + f"/Looks/{finish}")])
    finishes.SetVariantSelection("Red" if name == "Cube" else "Yellow")
    save(stage)

    stage.SetDefaultPrim(root)
    preview_environment(a, stage)
    UsdGeom.SetStageMetersPerUnit(stage, 0.01)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    stage.SetTimeCodesPerSecond(60)
    save(stage)


def assembly(a):
    prefix = "010_ASS_USD/Assemblies/DisplayPair"
    owner = "assembly:DisplayPair@1"
    stage = a.layer(f"{prefix}/020_BASE_LYR/GeoLyr.usda", "GeoLyr", owner)
    root = UsdGeom.Xform.Define(stage, "/DisplayPair").GetPrim()
    Usd.ModelAPI(root).SetKind("assembly")
    for name, asset in (("CubePart", "Cube"), ("ConePart", "Cone")):
        base = f"/DisplayPair/{name}"
        UsdGeom.Xform.Define(stage, base)
        UsdGeom.Xform.Define(stage, base + "/Adjustment")
        reference(stage, base + "/Adjustment/Asset", f"../../../USD_Wrappers/AssetROOT_{asset}.usda")
    save(stage)
    stage = a.layer(f"{prefix}/020_BASE_LYR/TransLyr.usda", "TransLyr", owner)
    trs(stage, "/DisplayPair/CubePart", translate=(-70, 0, 0))
    trs(stage, "/DisplayPair/ConePart", translate=(70, 0, 0))
    save(stage)
    stage = a.layer(f"{prefix}/020_BASE_LYR/VariLyr.usda", "VariLyr", owner, "Palette branches")
    palette = stage.OverridePrim("/DisplayPair").GetVariantSets().AddVariantSet("Palette")
    for name, finishes in {"Warm": ("Red", "Yellow"), "Cool": ("Blue", "Blue")}.items():
        palette.AddVariant(name)
        palette.SetVariantSelection(name)
        with palette.GetVariantEditContext():
            for part, finish in zip(("CubePart", "ConePart"), finishes):
                select(stage, f"/DisplayPair/{part}/Adjustment/Asset", {"Finish": finish})
    palette.SetVariantSelection("Warm")
    save(stage)
    recursive_package_notes(a, prefix, owner)
    a.root_layer(f"{prefix}/AssetROOT_DisplayPair.usda", "DisplayPair",
                 ["./050_OPINION_LYR/OpinLYR_default.usda", "./020_BASE_LYR/VariLyr.usda", "./020_BASE_LYR/TransLyr.usda", "./020_BASE_LYR/GeoLyr.usda"], owner)


def standard_root(a, name, sublayers, include_template_prims=True):
    """Adopt the user's Kit starting scene without changing its coordinate setup."""
    source = Sdf.Layer.FindOrOpen(str(TEMPLATE))
    stage = a.layer(name, "Root", "scene:LayeredScene@1")
    layer = stage.GetRootLayer()
    cc_data = dict(layer.customLayerData)
    if include_template_prims:
        layer.TransferContent(source)
        for prop, filename in TEMPLATE_TEXTURES.items():
            destination = f"010_ASS_USD/Envs/OmniverseStandard/Resources/{filename}"
            shutil.copyfile(TEMPLATE.parent / "Resources" / filename, a.path(destination))
            layer.GetAttributeAtPath(prop).default = Sdf.AssetPath("./" + destination)
    else:
        UsdUtils.CopyLayerMetadata(source, layer, skipSublayers=True)
    data = dict(layer.customLayerData)
    data.update(cc_data)
    data["cc:startupTemplate"] = "ROOT_example supplied by Jan"
    layer.customLayerData = data
    layer.subLayerPaths = sublayers
    layer.Save()
    return stage


def scene(a):
    owner = "scene:LayeredScene@1"
    stage = a.layer("020_BASE_LYR/GeoLyr.usda", "GeoLyr", owner)
    UsdGeom.Xform.Define(stage, "/World")
    for name, (asset, _) in INSTANCES.items():
        base = f"/World/{name}"
        UsdGeom.Xform.Define(stage, base)
        UsdGeom.Xform.Define(stage, base + "/Adjustment")
        reference(stage, base + "/Adjustment/Asset", f"../010_ASS_USD/{asset}")
    save(stage)

    stage = a.layer("020_BASE_LYR/TransLyr.usda", "TransLyr", owner)
    for name, (_, position) in INSTANCES.items():
        trs(stage, f"/World/{name}", translate=position)
    save(stage)

    stage = a.layer("020_BASE_LYR/VariLyr.usda", "VariLyr", owner, "manual selections")
    for name, choices in {
        "Cube01": {"Finish": "Red", "Size": "Normal"},
        "Cube02": {"Finish": "Blue", "Size": "Tall"},
        "Cone01": {"Finish": "Yellow", "Size": "Normal"},
        "Pair01": {"Palette": "Cool"},
    }.items():
        select(stage, f"/World/{name}/Adjustment/Asset", choices)
    save(stage)

    stage = a.layer("020_BASE_LYR/VariLyr_Scenarios.usda", "VariLyr", owner, "Layout branches")
    layout = stage.OverridePrim("/World").GetVariantSets().AddVariantSet("Layout")
    for choice in ("Normal", "Exploded"):
        layout.AddVariant(choice)
        layout.SetVariantSelection(choice)
        exploded = choice == "Exploded"
        with layout.GetVariantEditContext():
            for name in INSTANCES:
                offset = (0, 0, 80) if exploded and name == "Cube02" else (0, 0, 0)
                trs(stage, f"/World/{name}/Adjustment", translate=offset)
            for name, choices in {
                "Cube01": {"Finish": "Yellow" if exploded else "Red", "Size": "Normal"},
                "Cube02": {"Finish": "Red" if exploded else "Blue", "Size": "Tall"},
                "Cone01": {"Finish": "Yellow", "Size": "Normal"},
                "Pair01": {"Palette": "Warm" if exploded else "Cool"},
            }.items():
                select(stage, f"/World/{name}/Adjustment/Asset", choices)
    layout.SetVariantSelection("Normal")
    save(stage)

def project_data(a):
    owner = "scene:LayeredScene@1"
    stage = a.layer("040_DATA_LYR/Data/IdentityLyr.usda", "DataLyr", owner)
    for name in INSTANCES:
        stage.OverridePrim(f"/World/{name}").CreateAttribute(
            "cc:occurrenceId", Sdf.ValueTypeNames.String).Set(f"example-01/{name}")
    save(stage)
    stage = a.layer("040_DATA_LYR/Data/ContextLyr.usda", "DataLyr", owner)
    prim = stage.OverridePrim("/World")
    prim.CreateAttribute("cc:projectId", Sdf.ValueTypeNames.String).Set("CC-EXAMPLE-01")
    prim.CreateAttribute("cc:purpose", Sdf.ValueTypeNames.String).Set("Composition ownership demonstration")
    save(stage)
    stage = a.layer("040_DATA_LYR/DataLyr.usda", "DataLyr", owner)
    stage.GetRootLayer().subLayerPaths = ["./Data/IdentityLyr.usda", "./Data/ContextLyr.usda"]
    save(stage)


def opinion_layer(a, relative, owner):
    stage = a.layer(relative, "OpinionLyr", owner, "explicit temporary experiments")
    stage.GetRootLayer().documentation = (
        "Empty by default; default editable authoring layer for experiments. "
        "Promote reviewed fields to their rightful owner/layer/variant branch, "
        "then remove only superseded opinions. Saving persists these experiments."
    )
    save(stage)


def starter(a):
    owner = "scene:Starter@1"
    opinion = "050_OPINION_LYR/Starter/OpinLYR_default.usda"
    opinion_layer(a, opinion, owner)
    layers = ["./" + opinion]
    # Ready-to-use examples plus explicit optional slots; preserve source assets.
    for relative, role in (
        ("035_RUNTIME_LYR/Starter/RuntimeLyr.usda", "RuntimeLyr"),
        ("030_SIM_LYR/Starter/SimLyr.usda", "SimLyr"),
        ("040_DATA_LYR/Starter/DataLyr.usda", "DataLyr"),
        *((f"020_BASE_LYR/{role}_Starter.usda", role) for role in (
            "EnvLyr", "LightLyr", "CamLyr", "RenderLyr", "AnimLyr",
            "PhysicsLyr", "RigLyr", "MatLyr")),
        ("020_BASE_LYR/TransLyr_Starter.usda", "TransLyr"),
        ("020_BASE_LYR/VariLyr_Starter.usda", "VariLyr"),
        ("020_BASE_LYR/GeoLyr_Starter.usda", "GeoLyr"),
    ):
        stage = a.layer(relative, role, owner)
        layer = stage.GetRootLayer()
        metadata = dict(layer.customLayerData)
        if role in ("GeoLyr", "TransLyr", "VariLyr"):
            source = a.root / f"020_BASE_LYR/{role}.usda"
            with Sdf.ChangeBlock():
                layer.TransferContent(Sdf.Layer.FindOrOpen(str(source)))
                UsdUtils.ModifyAssetPaths(layer, lambda path: Path(os.path.relpath(
                    (source.parent / path).resolve(), a.path(relative).parent)).as_posix() if path.startswith(".") else path)
            layer.customLayerData = metadata
        elif role == "DataLyr":
            for data_role in ("IdentityLyr", "ContextLyr"):
                child = a.layer(f"040_DATA_LYR/Starter/{data_role}.usda", data_role, owner)
                child_data = dict(child.GetRootLayer().customLayerData)
                child.GetRootLayer().TransferContent(Sdf.Layer.FindOrOpen(str(
                    a.root / f"040_DATA_LYR/Data/{data_role}.usda")))
                child.GetRootLayer().customLayerData = child_data
                save(child)
            layer.subLayerPaths = ["./IdentityLyr.usda", "./ContextLyr.usda"]
        else:
            layer.documentation = (
                f"Optional {role} authoring slot; no active behavior authored. "
                "Remove or mute when unused. Supplied environment, lights, cameras and render baseline remain in the root. "
                "Declare ownership and writer authority before adding animation, physics, simulation or live state."
            )
        save(stage)
        layers.append("./" + relative)
    stage = standard_root(a, "SceneROOT_STARTER.usda", layers)
    data = dict(stage.GetRootLayer().customLayerData)
    data["cc:owner"] = owner
    stage.GetRootLayer().customLayerData = data
    a.roles[-1]["owner"] = owner
    save(stage)
    return layers


def entrypoints(a):
    owner = "scene:LayeredScene@1"
    opinion_layer(a, "050_OPINION_LYR/OpinLYR_default.usda", owner)
    stacks = {}
    for name, variant_layer in (("SceneROOT_Example.usda", "VariLyr.usda"), ("SceneROOT_Scenarios.usda", "VariLyr_Scenarios.usda")):
        layers = ["./050_OPINION_LYR/OpinLYR_default.usda", "./040_DATA_LYR/DataLyr.usda"] + [f"./020_BASE_LYR/{name}" for name in (
            "TransLyr.usda", variant_layer, "GeoLyr.usda")]
        standard_root(a, name, layers)
        stacks[name] = layers
    # Keep existing links useful while making the supplied root the canonical entrypoint.
    standard_root(a, "SceneROOT_Manual.usda", stacks["SceneROOT_Example.usda"])
    stacks["SceneROOT_Manual.usda"] = list(stacks["SceneROOT_Example.usda"])

    stage = a.layer("050_OPINION_LYR/MaskedSize/ReviewLyr.usda", "ReviewLyr", owner, "intentional masking demonstration")
    stage.OverridePrim("/World/Cube02/Adjustment/Asset").CreateAttribute(
        "xformOp:scale", Sdf.ValueTypeNames.Double3, custom=False).Set(Gf.Vec3d(1, 1, 1))
    save(stage)
    stage = a.layer("050_OPINION_LYR/MaskedSelection/ReviewLyr.usda", "ReviewLyr", owner, "intentional masking demonstration")
    select(stage, "/World/Cube01/Adjustment/Asset", {"Finish": "Blue"})
    save(stage)
    for mode, review, baseline in (
        ("MaskedSize", "MaskedSize", "SceneROOT_Example.usda"),
        ("MaskedSelection", "MaskedSelection", "SceneROOT_Scenarios.usda"),
    ):
        name = f"SceneROOT_{mode}.usda"
        layers = [stacks[baseline][0], f"./050_OPINION_LYR/{review}/ReviewLyr.usda", *stacks[baseline][1:]]
        standard_root(a, name, layers)
        stacks[name] = layers
    stacks["SceneROOT_STARTER.usda"] = starter(a)
    return stacks


def contracts(a, stacks):
    template = Sdf.Layer.FindOrOpen(str(TEMPLATE))
    a.json("_contracts/profile.json", {
        "schema": "cc-example-profile/0.1", "profile": PROFILE,
        "contract": "CompositionContract.md 0.1.1; CC-01 through CC-26",
        "status": "authored example; acceptance pending", "usd_authoring_version": "26.08",
        "units": {"metersPerUnit": template.pseudoRoot.GetInfo("metersPerUnit"), "upAxis": "Y"},
        "timeline": {"startTimeCode": 0, "endTimeCode": 100, "timeCodesPerSecond": 60},
        "standard_scene": "SceneROOT_Example.usda; user-supplied Omniverse starting scene",
        "manual_entrypoint": "SceneROOT_Manual.usda; independent root with direct scene sublayers",
        "starter_entrypoint": "SceneROOT_STARTER.usda; demo assets and independent work layers with optional authoring slots",
        "opinion_policy": "Samples share 050_OPINION_LYR/OpinLYR_default.usda; Starter has its own. Strongest work sublayer, editable by default; Opinion is the authoring target. Promote reviewed fields then retire superseded opinions.",
        "resolver": "ArDefaultResolver; relative package paths; no search path required",
        "composition": "references; no payloads; no native instancing; default time",
        "entrypoints_strongest_first": stacks,
        "root_fields": ["stage metadata", "sublayer list", "defaultPrim", "supplied Environment/Render/OmniverseKit camera specs"],
        "root_exception": "CC-01 application-template baseline; supplied startup content stays in root",
        "writer_mode": "static authored scene; no solver or live writer",
        "default_session": "Opinion is the default authoring target; persistent work/source layers locked",
        "kit_startup": "Open_In_Kit.ps1 enables _workflows/kit/session_defaults.py; launcher selects declared Opinion target",
        "persistent_authoring": "explicitly unlock the rightful layer, choose its edit/variant context, save, retire superseded Opinion fields and return to Opinion",
        "dependencies": "bundled assets, Palette_v001 and two Kit template textures; OmniPBR.mdl and OmniRtx schemas require compatible Omniverse",
        "ordinary_instance_transform": ["translate", "rotateXYZ", "scale"],
        "reset_xform_stack": False,
        "roles": a.roles,
        "intentional_overlaps": [
            "Scene selection overrides referenced asset default selection.",
            "DisplayPair Palette selects child Finish through the published interface.",
            "Review overlays mask Size or nested Finish only in the named conflict entrypoints."
        ],
        "excluded_acceptance": ["Omniverse UI/persistence", "renderer appearance", "payload lofting",
                                "animation", "physics", "live integration", "general conformance"],
    })
    a.json("_contracts/ownership.json", {
        "schema": "cc-example-ownership/0.1", "authority": "Project-authored demo design, revision 0.1.1",
        "team": "Example maintainer (role placeholder; no external acceptance)",
        "common_policy": {
            "persistence": "explicit save to declared file; static authored data",
            "source_authority": "This example design; no PLM or external engineering authority",
            "conflict": "report undeclared overlap; no automatic routing or repair",
            "lifecycle": "draft local example", "evidence": "expected.json; build_manifest.json; manual UI review pending",
        },
        "owners": [
            {"id": "library:Palette@1", "package": "010_ASS_USD/MatLib/Palette_v001.usda",
             "public": "/Materials/{Red,Blue,Yellow,Ground}", "fields": "UsdPreviewSurface shader values",
             "role": "MatLyr", "override": "new reviewed library revision; no scene shader edits"},
            *[{"id": f"asset:{name}@1", "package": f"010_ASS_USD/USD_Wrappers/AssetROOT_{name}.usda",
               "public": f"/{name}", "variants": {"Size": ["Normal", "Large", "Tall"], "Finish": ["Red", "Blue", "Yellow"]},
               "defaults": {"Size": "Normal", "Finish": "Red" if name == "Cube" else "Yellow"},
               "pivot": "base center; Y-up; 100 cm height in Normal",
               "private": [f"/{name}/Geometry", f"/{name}/Looks"],
               "fields": "geometry; intrinsic placement; branch scale/order; branch material binding",
               "edit_targets": "Standalone leaf entrypoint; keep conditional values inside variants",
               "override": "downstream selects public variants; private edits only in explicit review fixture"}
              for name in ("Cube", "Cone")],
            {"id": "assembly:DisplayPair@1", "package": "010_ASS_USD/Assemblies/DisplayPair/AssetROOT_DisplayPair.usda",
             "public": "/DisplayPair", "variants": {"Palette": ["Warm", "Cool"]}, "defaults": {"Palette": "Warm"},
             "fields": "child references; child placement; Palette branch child Finish selections",
             "edit_targets": "020_BASE_LYR/GeoLyr, TransLyr, VariLyr.usda according to role",
             "override": "scene selects Palette; child paths remain assembly implementation"},
            {"id": "application:OmniverseStandard", "package": "SceneROOT_Example.usda",
             "public": ["/Environment", "/Render", "/OmniverseKit_*"],
             "fields": "supplied ground/collider, lighting, viewport cameras, materials and render state",
             "role": "Root application-template baseline (CC-01 exception)",
             "override": "preserve the user-selected startup scene; explicit later changes only"},
            {"id": "scene:LayeredScene@1", "public": "/World",
             "fields": "occurrence hierarchy, placement, selections, scenario adjustments and project identity",
             "edit_targets": "role registry in profile.json; manual/scenario VariLyr are mutually exclusive",
             "variants": {"Layout": ["Normal", "Exploded"]}, "defaults": {"Layout": "Normal"},
             "override": "named ReviewLyr exceptions only; remove its sublayer to restore baseline"},
        ],
        "review_exceptions": [
            {"file": "050_OPINION_LYR/MaskedSize/ReviewLyr.usda", "reason": "reproduce original local-versus-variant failure",
             "target": "/World/Cube02/Adjustment/Asset.xformOp:scale", "supersedes": "Size=Tall scale",
             "disposition": "teaching fixture only; exclude from normal root"},
            {"file": "050_OPINION_LYR/MaskedSelection/ReviewLyr.usda", "reason": "show direct child selection masking scene scenario",
             "target": "/World/Cube01/Adjustment/Asset Finish selection", "supersedes": "Layout branch Finish",
             "disposition": "teaching fixture only; exclude from normal root"},
        ],
    })
    a.json("_contracts/expected.json", {
        "status": "expected outcomes; not executed acceptance results",
        "SceneROOT_Example.usda": {
            "Cube01": {"Finish": "Red", "Size": "Normal", "height_cm": 100, "base_cm": [-220, 0, 0]},
            "Cube02": {"Finish": "Blue", "Size": "Tall", "height_cm": 200, "base_cm": [0, 0, 0]},
            "Cone01": {"Finish": "Yellow", "Size": "Normal", "height_cm": 100, "base_cm": [220, 0, 0]},
            "Pair01": {"Palette": "Cool", "child_finishes": ["Blue", "Blue"], "base_cm": [0, 0, -260]},
        },
        "SceneROOT_Manual.usda": "independent manual root; same baseline and direct stack as SceneROOT_Example.usda",
        "SceneROOT_STARTER.usda": "Omniverse baseline and Manual demo configuration; independent work layers plus optional empty role slots; Opinion authoring through launcher; persistent work/source layers locked",
        "SceneROOT_Scenarios.usda": {
            "Normal": "same visible configuration as Manual; explicit neutral Adjustment operations",
            "Exploded": "Cube02 base y=80 cm, height=200 cm, Red; Cube01 Yellow; Pair01 Warm (Red/Yellow); other placements unchanged",
        },
        "SceneROOT_MaskedSize.usda": "Cube02 Size reads Tall, resolved asset scale=(1,1,1), height=100 cm",
        "SceneROOT_MaskedSelection.usda": "Cube01 Finish remains Blue under either Layout branch",
        "material_resolution": "Geometry binds to its remapped Asset/Looks/<Finish>; pair children bind to their own Looks",
        "manual_acceptance": ["all listed variant choices", "placement and scenario independence", "save/reopen VariLyr",
                              "source hashes unchanged by scene edits", "relocation of complete folder",
                              "resolved materials in target renderer", "remove review overlay to restore expected behavior"],
    })


def folder_notes(a):
    notes = {
        "000_SOURCE/README.md": "# Original sources\n\nStore CAD/DCC originals and conversion provenance here. This procedural example has no external originals. New geometry is authored by tools/build_example.py in the parent repository.",
        "010_ASS_USD/USD_Startpoint/README.md": "# Imported USD startpoints\n\nStore retained CAD/DCC USD exports here. A wrapper may reference an imported subtree; record any source transforms or variants as imported content with an explicit boundary. The procedural Cube and Cone in this example are authored directly in their package layers. This slot is unused.",
        "010_ASS_USD/tex/README.md": "# Shared textures\n\nShared textures belong here; asset-specific textures can travel inside their package. This example uses texture-free UsdPreviewSurface materials.",
        "030_SIM_LYR/README.md": "# Published simulation results\n\nReserved for explicit, versioned solver results with provenance and time semantics. No simulation result or SimLyr is present or composed in this static profile.",
        "035_RUNTIME_LYR/README.md": "# Runtime snapshots\n\nReserved for deliberately saved operational snapshots. Live measurements normally stay in session/runtime/external storage. No connector, credentials, runtime writer or RuntimeLyr is present.",
        "040_DATA_LYR/README.md": "# Project data\n\nDataLyr aggregates IdentityLyr and ContextLyr. These demo custom cc attributes describe scene occurrences and project purpose. They are not a standardized schema or an external system integration.",
        "050_OPINION_LYR/README.md": "# Review demonstrations\n\nEach exception has an owner, reason, affected field and removal route in _contracts/ownership.json. Only the SceneROOT_MaskedSize and SceneROOT_MaskedSelection entrypoints compose these files. Baseline roots exclude them.",
        "_workflows/README.md": "# Reproduction and workflow files\n\nReproduction uses the parent repository's tools/build_example.py. kit/session_defaults.py is the scoped Kit startup helper used by Open_In_Kit.ps1: persistent work/source layers are protected and Opinion becomes the edit target. It does not route or persist edits. Optional pipeline or ComfyUI definitions can be added here when needed; none is installed.",
        "_pipeline_reports/README.md": "# Evidence\n\nbuild_manifest.json records runtime, file identities and the saved defaults of SceneROOT_Example plus four companion entrypoints. It includes stage metrics, the World matrix, camera choice and cube opinions. This is not a conformance verdict or a variant-matrix test. Expected outcomes live in _contracts/expected.json. Kit UI and rendering acceptance are pending.",
        "_contracts/README.md": "# Example contracts\n\nprofile.json declares package roles and actual scene orders. ownership.json declares public interfaces, writer scope and review exceptions. expected.json states intended outcomes. These versioned example-specific JSON documents are design inputs; no generic validator or accepted contract schema exists yet. The parent repository's CompositionContract.md owns CC semantics.",
    }
    for name, note in notes.items():
        a.text(name, note)


def session_defaults(a):
    """Persist supported Kit locks and ship the declared-target runtime hook."""
    templates = Path(__file__).resolve().parent / "kit"
    for source, destination in (("session_defaults.py", "_workflows/kit/session_defaults.py"),
                                ("Open_In_Kit.ps1", "Open_In_Kit.ps1")):
        shutil.copyfile(templates / source, a.path(destination))
    for record in a.roles:
        if record["role"] != "Root":
            continue
        path = a.root / record["file"]
        stage = Usd.Stage.Open(str(path))
        root = stage.GetRootLayer()
        data = dict(root.customLayerData)
        data["cc:defaultAuthoring"] = "opinion"
        data["cc:opinionLayer"] = root.subLayerPaths[0]
        data["cc:lockPersistentLayers"] = True
        omni = dict(data.get("omni_layer", {}))
        # Kit restores this standard field on direct open; cc metadata alone is not enough.
        omni["authoring_layer"] = data["cc:opinionLayer"]
        locks = {}  # Recompute for the actual dependency graph; discard retired destinations.
        for layer in stage.GetUsedLayers():
            if layer.anonymous or layer == root:
                continue
            relative = Path(os.path.relpath(layer.realPath, path.parent)).as_posix()
            relative = relative if relative.startswith(".") else "./" + relative
            locks[relative] = relative != root.subLayerPaths[0]
        if locks:
            omni["locked"] = locks
        data["omni_layer"] = omni
        root.customLayerData = data
        root.Save()


def record_build(a, stacks):
    observations = {}
    for name in stacks:
        stage = Usd.Stage.Open(str(a.root / name), load=Usd.Stage.LoadAll)
        if not stage:
            raise RuntimeError(f"Could not reopen authored entrypoint: {name}")
        errors = stage.GetCompositionErrors()
        if errors:
            raise RuntimeError(f"Composition errors in {name}: {errors}")
        cubes = {}
        for instance in ("Cube01", "Cube02"):
            base = f"/World/{instance}/Adjustment/Asset"
            prim = stage.GetPrimAtPath(base)
            material, _ = UsdShade.MaterialBindingAPI(stage.GetPrimAtPath(base + "/Geometry")).ComputeBoundMaterial()
            cubes[instance] = {
                "selections": {v: prim.GetVariantSets().GetVariantSet(v).GetVariantSelection() for v in ("Finish", "Size")},
                "resolved_scale": list(prim.GetAttribute("xformOp:scale").Get()),
                "resolved_material": str(material.GetPath()) if material else None,
            }
        root_data = stage.GetRootLayer().customLayerData
        observations[name] = {"default_prim": str(stage.GetDefaultPrim().GetPath()),
                              "composition_errors": [], "cubes": cubes,
                              "up_axis": UsdGeom.GetStageUpAxis(stage),
                              "meters_per_unit": UsdGeom.GetStageMetersPerUnit(stage),
                              "time_codes_per_second": stage.GetTimeCodesPerSecond(),
                              "time_range": [stage.GetStartTimeCode(), stage.GetEndTimeCode()],
                              "bound_camera": root_data.get("cameraSettings", {}).get("boundCamera"),
                              "world_matrix": [list(row) for row in UsdGeom.XformCache().GetLocalToWorldTransform(stage.GetPrimAtPath("/World"))],
                              "saved_authoring_policy": root_data.get("cc:defaultAuthoring"),
                              "saved_lock_count": len(root_data.get("omni_layer", {}).get("locked", {})),
                              "kit_startup_execution": "not exercised by this USD read-back"}
    files = [{"path": p.relative_to(a.root).as_posix(), "bytes": p.stat().st_size,
              "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
             for p in sorted(a.root.rglob("*")) if p.is_file()
             and p.relative_to(a.root).as_posix() != "_pipeline_reports/build_manifest.json"]
    a.json("_pipeline_reports/build_manifest.json", {
        "schema": "cc-example-build/0.1", "profile": PROFILE,
        "generator": "tools/build_example.py", "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256((Path(__file__).resolve().parents[1] / "CompositionContract.md").read_bytes()).hexdigest(),
        "startup_template_sha256": hashlib.sha256(TEMPLATE.read_bytes()).hexdigest(),
        "python": platform.python_version(), "usd": list(Usd.GetVersion()),
        "scope": "authoring and default-entrypoint read-back only; no acceptance tests run",
        "load": "LoadAll", "time": "default", "session": "empty",
        "observations": observations, "package_files_at_recording": files,
        "human_acceptance": "pending", "tests": "not run",
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New or empty output directory")
    args = parser.parse_args()
    root = args.output.resolve()
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        parser.error("Output must be a new or empty directory; existing files are never overwritten.")
    if Usd.GetVersion() != (0, 26, 8):
        parser.error("This example author is pinned to OpenUSD 26.08 (usd-core==26.8).")
    root.mkdir(parents=True, exist_ok=True)
    a = Author(root)
    material_library(a)
    shape_asset(a, "Cube")
    shape_asset(a, "Cone")
    assembly(a)
    scene(a)
    project_data(a)
    stacks = entrypoints(a)
    contracts(a, stacks)
    folder_notes(a)
    session_defaults(a)
    record_build(a, stacks)
    print(f"Authored {len(a.roles)} USD layers in {root}")
    print("Default-entrypoint read-back recorded; acceptance tests and UI review are pending.")


if __name__ == "__main__":
    main()
