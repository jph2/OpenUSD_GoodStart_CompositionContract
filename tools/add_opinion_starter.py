"""Bounded authoring update for the existing layered example; no acceptance tests."""
import json
from pathlib import Path
from pxr import Sdf
from build_example import Author, opinion_layer, starter, session_defaults


def main():
    package = Path(__file__).resolve().parents[1] / "examples/01_LayeredScene"
    a = Author(package)
    opinion = "050_REVIEW/OpinLYR_default.usda"
    if (package / opinion).exists() or (package / "SceneROOT_STARTER.usda").exists():
        raise RuntimeError("Opinion/starter already exists; refusing to overwrite authored work.")
    profile_path = package / "_contracts/profile.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    roots = {}
    for name, expected in profile["entrypoints_strongest_first"].items():
        layer = Sdf.Layer.FindOrOpen(str(package / name))
        if not layer or list(layer.subLayerPaths) != expected:
            raise RuntimeError(f"Unexpected existing stack: {name}")
        roots[name] = layer
    opinion_layer(a, opinion, "scene:LayeredScene@1")
    starter_stack = starter(a)
    roots["SceneROOT_STARTER.usda"] = Sdf.Layer.FindOrOpen(str(package / "SceneROOT_STARTER.usda"))
    for name, layer in roots.items():
        if name != "SceneROOT_STARTER.usda":
            layer.subLayerPaths = ["./" + opinion, *layer.subLayerPaths]
        data = dict(layer.customLayerData)
        data["cc:defaultAuthoring"] = "opinion"
        data["cc:opinionLayer"] = layer.subLayerPaths[0]
        data["cc:lockPersistentLayers"] = True
        omni = dict(data.get("omni_layer", {}))
        omni.pop("authoring_layer", None)
        locks = {} if name == "SceneROOT_STARTER.usda" else dict(omni.get("locked", {}))
        locks.update({path: path != layer.subLayerPaths[0] for path in layer.subLayerPaths})
        omni["locked"] = locks
        data["omni_layer"] = omni
        layer.customLayerData = data
        layer.Save()
        profile["entrypoints_strongest_first"][name] = list(layer.subLayerPaths)
    profile["roles"].extend(a.roles)
    a.roles = profile["roles"]
    session_defaults(a)
    profile["default_session"] = "Opinion is the default authoring target; other persistent layers locked"
    profile["starter_entrypoint"] = "SceneROOT_STARTER.usda; demo assets and independent work layers with optional authoring slots"
    profile["opinion_policy"] = "Samples share 050_REVIEW/OpinLYR_default.usda; Starter has its own. Strongest work sublayer, editable by default; Opinion is the authoring target. Promote reviewed fields then retire superseded opinions."
    a.json("_contracts/profile.json", profile)
    expected = json.loads((package / "_contracts/expected.json").read_text(encoding="utf-8"))
    expected["SceneROOT_STARTER.usda"] = "Omniverse baseline and Manual demo configuration; independent work layers plus optional empty role slots; Opinion authoring through launcher; other persistent layers locked"
    a.json("_contracts/expected.json", expected)
    print("Authored Opinion layers and independent starter; updated six root stacks and profile. No acceptance tests run.")


if __name__ == "__main__":
    main()
