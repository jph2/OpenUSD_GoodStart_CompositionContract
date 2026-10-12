"""Author two bounded scalability examples from our existing sources; no tests.

Run on an existing example package. Reuses identical outputs; refuses changed ones.
Kitchen Set informed the packaging pattern; no Kitchen Set content is copied.
"""
from pathlib import Path
import argparse
import json
import os

from pxr import Gf, Sdf


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parents[1] / 'examples/01_LayeredScene')
    parser.add_argument('--replace-generated', action='store_true', help='Replace only this script\'s named outputs, including their authored edits')
    args = parser.parse_args()
    package = args.package.resolve()
    pending = {}
    sources = {}

    def layer(relative, owner, role, context='unconditional'):
        destination = package / relative
        result = Sdf.Layer.CreateAnonymous('.usda')
        result.customLayerData = {'cc:owner': owner, 'cc:role': role,
                                  'cc:context': context, 'cc:profile': 'CC-SCALE-01/0.1.1'}
        pending[relative] = result
        return result

    def link(from_path, to_path):
        return './' + os.path.relpath(package / to_path, (package / from_path).parent).replace('\\', '/')

    def settings(result, prim):
        result.defaultPrim = prim
        for name, value in [('upAxis', 'Z'), ('metersPerUnit', 0.01), ('timeCodesPerSecond', 60.0)]:
            result.pseudoRoot.SetInfo(name, value)

    def source(relative):
        if relative in sources:
            return sources[relative]
        result = Sdf.Layer.FindOrOpen(str(package / relative))
        if result is None:
            raise RuntimeError(f'Missing source {relative}')
        sources[relative] = result
        return result

    interfaces = {}
    for name, family in [('Cube', 'USD_Wrappers'), ('Cone', 'USD_Wrappers'), ('DisplayPair', 'Assemblies')]:
        owner = f'asset:{name}Lofted@1' if family == 'USD_Wrappers' else 'assembly:DisplayPairLofted@1'
        original = f'010_ASS_USD/{family}/{name}'
        folder = original + 'Lofted'
        root_path = f'{folder}/AssetROOT_{name}Lofted.usda'
        contents_path = f'{folder}/020_BASE_LYR/ContentsLyr.usda'
        opinion_path = f'{folder}/050_OPINION_LYR/OpinLYR_default.usda'
        root = layer(root_path, owner, 'Root', 'public interface above payload')
        settings(root, name)
        if name != 'Cube':
            layer(opinion_path, owner, 'Opinion', 'empty experiments; promote explicitly')
            root.subLayerPaths = [link(root_path, opinion_path)]
        root.subLayerPaths = list(root.subLayerPaths) + [link(root_path, '010_ASS_USD/Envs/OmniverseStandard/Environment.usda')]
        prim = Sdf.CreatePrimInLayer(root, '/' + name)
        prim.specifier = Sdf.SpecifierDef
        prim.typeName = 'Xform'
        prim.SetInfo('kind', 'component' if family == 'USD_Wrappers' else 'assembly')
        prim.SetInfo('assetInfo', {'name': name + 'Lofted', 'identifier': Sdf.AssetPath('./' + Path(root_path).name)})
        prim.payloadList.prependedItems = [Sdf.Payload(link(root_path, contents_path), '/' + name)]
        # Publish names/defaults only; all branch values stay in the source VariLyr.
        leaf_path = f'010_ASS_USD/USD_Wrappers/AssetROOT_{name}.usda'
        variant_path = leaf_path if family == 'USD_Wrappers' else f'{original}/020_BASE_LYR/VariLyr.usda'
        original_vari = source(variant_path).GetPrimAtPath('/' + name)
        prim.variantSetNameList.prependedItems = list(original_vari.variantSets.keys())
        for key, value in original_vari.variantSelections.items():
            prim.variantSelections[key] = value
        for key, variants in original_vari.variantSets.items():
            target_set = Sdf.VariantSetSpec(prim, key)
            for choice in variants.variants.keys():
                Sdf.VariantSpec(target_set, choice)
        if family == 'USD_Wrappers':
            prim.payloadList.prependedItems = [Sdf.Payload(link(root_path, leaf_path), '/' + name)]
        else:
            contents = layer(contents_path, owner, 'PayloadContents', 'assembly contributions')
            settings(contents, name)
            contents.subLayerPaths = [link(contents_path, f'{original}/020_BASE_LYR/{role}.usda') for role in ('VariLyr', 'TransLyr')]
        if family == 'Assemblies':
            geo_path = f'{folder}/020_BASE_LYR/GeoLyr.usda'
            geo = layer(geo_path, owner, 'GeoLyr')
            geo.TransferContent(source(f'{original}/020_BASE_LYR/GeoLyr.usda'))
            geo.customLayerData = {'cc:owner': owner, 'cc:role': 'GeoLyr', 'cc:profile': 'CC-SCALE-01/0.1.1'}
            for child, shape in [('CubePart', 'Cube'), ('ConePart', 'Cone')]:
                site = geo.GetPrimAtPath(f'/DisplayPair/{child}/Adjustment/Asset')
                site.referenceList.prependedItems = [Sdf.Reference(link(geo_path, interfaces[shape]))]
            contents.subLayerPaths = list(contents.subLayerPaths) + [link(contents_path, geo_path)]
        if name != 'Cube':
            root.customLayerData = {**root.customLayerData, 'cc:defaultAuthoring': 'opinion',
                'cc:lockPersistentLayers': True, 'cc:opinionLayer': link(root_path, opinion_path),
                'omni_layer': {'authoring_layer': link(root_path, opinion_path),
                              'locked': {link(root_path, opinion_path): False, link(root_path, leaf_path if family == 'USD_Wrappers' else contents_path): True}}}
        interfaces[name] = root_path

    new_entries = {}
    for purpose in ('Lofted', 'Instanced'):
        owner = f'scene:{purpose}@1'
        opinion_path = f'050_OPINION_LYR/{purpose}/OpinLYR_default.usda'
        layer(opinion_path, owner, 'Opinion')
        for role in ('TransLyr', 'VariLyr', 'GeoLyr'):
            path = f'020_BASE_LYR/{role}_{purpose}.usda'
            target = layer(path, owner, role)
            target.TransferContent(source(f'020_BASE_LYR/{role}.usda'))
            target.customLayerData = {'cc:owner': owner, 'cc:role': role, 'cc:profile': 'CC-SCALE-01/0.1.1'}
            if role == 'VariLyr':
                for occurrence in ('Cube01', 'Cube02', 'Cone01'):
                    spec = target.GetPrimAtPath(f'/World/{occurrence}/Adjustment/Asset')
                    spec.variantSelections['Finish'] = 'Blue'
                    spec.variantSelections['Size'] = 'Normal'
            if role == 'GeoLyr':
                for occurrence, name in [('Cube01', 'Cube'), ('Cube02', 'Cube'), ('Cone01', 'Cone'), ('Pair01', 'DisplayPair')]:
                    spec = target.GetPrimAtPath(f'/World/{occurrence}/Adjustment/Asset')
                    spec.referenceList.prependedItems = [Sdf.Reference(link(path, interfaces[name]))]
                    if purpose == 'Instanced' and name != 'DisplayPair':
                        spec.instanceable = True
                if purpose == 'Instanced':
                    for child in ('CubePart', 'ConePart'):
                        Sdf.CreatePrimInLayer(target, f'/World/Pair01/Adjustment/Asset/{child}/Adjustment/Asset').instanceable = True
            if purpose == 'Instanced':
                for row in range(32):
                    for column in range(32):
                        occurrence = f'/World/InstanceGrid/Shape_r{row:02d}_c{column:02d}'
                        asset = occurrence + '/Adjustment/Asset'
                        if role == 'GeoLyr':
                            for prim_path in ('/World/InstanceGrid', occurrence, occurrence + '/Adjustment', asset):
                                prim = Sdf.CreatePrimInLayer(target, prim_path)
                                prim.specifier = Sdf.SpecifierDef
                                prim.typeName = 'Xform'
                            shape = 'Cube' if (row + column) % 2 == 0 else 'Cone'
                            prim.referenceList.prependedItems = [Sdf.Reference(link(path, interfaces[shape]))]
                            prim.instanceable = True
                        elif role == 'TransLyr':
                            prim = Sdf.CreatePrimInLayer(target, occurrence)
                            Sdf.AttributeSpec(prim, 'xformOp:translate', Sdf.ValueTypeNames.Double3).default = Gf.Vec3d((column - 15.5) * 120, 400 + row * 120, 0)
                            Sdf.AttributeSpec(prim, 'xformOpOrder', Sdf.ValueTypeNames.TokenArray, Sdf.VariabilityUniform).default = ['xformOp:translate']
                        else:
                            prim = Sdf.CreatePrimInLayer(target, asset)
                            prim.variantSelections['Size'] = 'Normal'
                            prim.variantSelections['Finish'] = 'Blue'
        root_path = f'SceneROOT_{purpose}.usda'
        root = layer(root_path, owner, 'Root')
        root.TransferContent(source('SceneROOT_Example.usda'))
        root.subLayerPaths = ['./' + opinion_path, './040_DATA_LYR/DataLyr.usda'] + [
            f'./020_BASE_LYR/{role}_{purpose}.usda' for role in ('TransLyr', 'VariLyr', 'GeoLyr')]
        data = dict(root.customLayerData)
        data.update({'cc:owner': owner, 'cc:profile': 'CC-SCALE-01/0.1.1', 'cc:opinionLayer': './' + opinion_path})
        locks = {path: True for path in root.subLayerPaths}
        locks['./' + opinion_path] = False
        data['omni_layer'] = {'authoring_layer': './' + opinion_path, 'locked': locks}
        root.customLayerData = data
        new_entries[root_path] = list(root.subLayerPaths)

    contract_path = package / '_contracts/scalability.json'
    if contract_path.exists() and not args.replace_generated:
        raise RuntimeError(f'Refusing to overwrite {contract_path}')
    for path, result in pending.items():
        destination = package / path
        if destination.exists() and not args.replace_generated and source(path).ExportToString() != result.ExportToString():
            raise RuntimeError(f'Refusing to overwrite changed output {destination}')
    # All output paths were checked before any write. Source layers stay untouched.
    for path, result in pending.items():
        destination = package / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        if args.replace_generated or not destination.exists():
            result.Export(str(destination))
    contract_path.write_text(json.dumps({
        'profile': 'CC-SCALE-01/0.1.1', 'status': 'authored; acceptance pending',
        'entrypoints_strongest_first': new_entries, 'interfaces': interfaces,
        'purpose': 'five-shape payload interface example plus a native-instancing stress scene with 1024 extra occurrences',
        'expected': {
            'LoadNone': 'direct Size/Finish and assembly Palette names remain discoverable; payload geometry absent; local instanceability overs may be visible for nested children even before their definitions load',
            'LoadAll': 'Lofted/base Instanced teaching shapes are Blue/Normal. Driven scenes retain them and vary all 1024 additional grid occurrences.',
            'Instanced': '1029 shape Asset sites instanceable (515 Cube, 514 Cone); Pair stays editable; 32 by 32 grid adds 1024 Blue Normal shapes; compatible occurrences may share prototypes',
            'variant_context': 'names/defaults above payload; values and bindings stay in owning source VariLyr branches',
        },
        'ownership': 'independent scene Opinion/Trans/Vari/Geo; shared Data and source role files; asset Opinion above payload; source demo Opinions excluded',
        'generated_formations': {
            f'SceneROOT_Instanced_{name}.usda': {
                'input': '_workflows/inputs/instance_signal.json',
                'driver': f'_workflows/arrange_instances.py --shape {name.lower()} --apply',
                'grid_occurrences': 1024,
                'configurations': '2 shape types x 3 sizes x 3 finishes; generated selections use all 18',
                'snapshot': 'offline; no live telemetry or animation',
                'layers': [f'050_OPINION_LYR/Instanced_{name}/OpinLYR_default.usda',
                           f'020_BASE_LYR/TransLyr_Instanced_{name}.usda',
                           f'020_BASE_LYR/VariLyr_Instanced_{name}.usda'],
                'shared': ['020_BASE_LYR/GeoLyr_Instanced.usda', '040_DATA_LYR/DataLyr.usda', 'lofted source interfaces'],
            } for name in ('Wave', 'Spiral', 'Rings')
        },
        'limitations': ['no benchmark', 'no physics or robot readiness', 'no cached extentsHint', 'no live binding implementation', 'Kit lock/edit-target and load/unload acceptance pending'],
        'acceptance_to_run': ['unloaded interface discovery', 'all Size/Finish/Palette branches after load', 'prototype sharing and independent placement', 'save/reopen and source-path portability', 'Omniverse authoring defaults and later payload-load protection'],
        'roles': [{'file': path, **{key: value for key, value in result.customLayerData.items()
                                  if key in ('cc:owner', 'cc:role', 'cc:context')}} for path, result in pending.items()],
    }, indent=2), encoding='utf-8')
    print(f'Authored {len(pending)} new USD files and scalability profile. No acceptance tests run.')


if __name__ == '__main__':
    main()
