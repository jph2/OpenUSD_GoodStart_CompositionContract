"""Author the bounded Essentials package using USD parsing; no Kit launch or tests."""
from pathlib import Path
import argparse
import shutil
import re
from pxr import Sdf

REPO = Path(__file__).resolve().parents[1]
DEST = REPO / 'examples/02_USDEssentials_Minimal'
FILES = {}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--replace-authored', action='store_true', help='Replace generated USD role/root files; preserve existing Opinions and documentation.')
parser.add_argument('--roots-only', action='store_true', help='Update scene roots from defaultscene.usda without reauthoring role files.')
args = parser.parse_args()
if DEST.exists() and any(DEST.glob('SceneROOT_*.usda')) and not args.replace_authored:
    parser.error('Existing package: use --replace-authored after reviewing local edits.')

def layer(path, body='', sublayers=(), root=False, opinion=None, owner='scene:USDEssentials', role=None):
    metadata = ['    defaultPrim = "World"' if root else '    defaultPrim = "Asset"'] if root or str(path).split('/')[-1].startswith('AssetROOT_') else []
    if root or str(path).split('/')[-1].startswith('AssetROOT_'):
        metadata += ['    metersPerUnit = 0.01', '    upAxis = "Z"', '    timeCodesPerSecond = 60', '    framesPerSecond = 60']
    if sublayers:
        metadata += ['    subLayers = [\n' + ',\n'.join('        @./' + s + '@' for s in sublayers) + '\n    ]']
    role = role or Path(path).stem
    custom = f'        string "cc:owner" = "{owner}"\n        string "cc:role" = "{role}"\n        string "cc:context" = "unconditional"'
    if opinion:
        custom += f'\n        string "cc:defaultAuthoring" = "opinion"\n        bool "cc:lockPersistentLayers" = 1\n        string "cc:opinionLayer" = "./{opinion}"\n        dictionary omni_layer = {{\n            string authoring_layer = "./{opinion}"\n        }}'
    metadata += ['    customLayerData = {\n' + custom + '\n    }']
    FILES[path] = '#usda 1.0\n(\n' + '\n'.join(metadata) + '\n)\n\n' + body + '\n'

for shape in ('Cube', 'Cone'):
    base = f'010_ASS_USD/USD_Wrappers/{shape}/'
    owner = f'asset:{shape}'
    geometry = 'def Cube "Geometry" {\n        double size = 100\n    }' if shape == 'Cube' else 'def Cone "Geometry" {\n        double height = 100\n        double radius = 50\n        uniform token axis = "Z"\n    }'
    layer(base+'020_BASE_LYR/GeoLyr.usda', 'def Xform "Asset" {\n    '+geometry+'\n}', owner=owner, role='GeoLyr')
    layer(base+'020_BASE_LYR/TransLyr.usda', 'over "Asset" {\n    over "Geometry" {\n        double3 xformOp:translate = (0, 0, 50)\n        uniform token[] xformOpOrder = ["xformOp:translate"]\n    }\n}', owner=owner, role='TransLyr')
    layer(base+'020_BASE_LYR/MatLyr.usda', 'over "Asset" {\n    def Scope "Looks" (prepend references = @../../../MatLib/Palette_v001.usda@) {}\n}', owner=owner, role='MatLyr')
    branches = '\n'.join(f'        "{color}" {{\n            over "Geometry" (prepend apiSchemas = ["MaterialBindingAPI"]) {{\n                rel material:binding = </Asset/Looks/{color}>\n            }}\n        }}' for color in ('Red','Blue'))
    layer(base+'020_BASE_LYR/VariLyr.usda', 'over "Asset" (\n    prepend variantSets = "Color"\n    variants = { string Color = "Red" }\n) {\n    variantSet "Color" = {\n'+branches+'\n    }\n}', owner=owner, role='VariLyr')
    for suffix in ('', '_ColorVariants'):
        op = f'050_REVIEW_LYR/OpinLYR_{"default" if not suffix else "ColorVariants"}.usda'
        layer(base+op, owner=owner, role='Opinion')
        roles = (['020_BASE_LYR/VariLyr.usda','020_BASE_LYR/MatLyr.usda'] if suffix else []) + ['020_BASE_LYR/TransLyr.usda','020_BASE_LYR/GeoLyr.usda']
        layer(base+f'AssetROOT_{shape}{suffix}.usda', sublayers=[op]+roles, opinion=op, owner=owner, role='Root')

palette = 'def Scope "Palette" {\n'
for color, rgb in [('Red','0.8, 0.08, 0.06'),('Blue','0.04, 0.22, 0.8')]:
    palette += f'    def Material "{color}" {{\n        token outputs:surface.connect = </Palette/{color}/Surface.outputs:surface>\n        def Shader "Surface" {{\n            uniform token info:id = "UsdPreviewSurface"\n            color3f inputs:diffuseColor = ({rgb})\n            float inputs:roughness = 0.45\n            token outputs:surface\n        }}\n    }}\n'
FILES['010_ASS_USD/MatLib/Palette_v001.usda'] = '#usda 1.0\n( defaultPrim = "Palette" )\n'+palette+'}\n'
for suffix in ('', '_ColorVariants'):
    geo = 'def Xform "World" {\n'
    for shape in ('Cube','Cone'):
        geo += f'    def Xform "{shape}01" {{\n        def Xform "Adjustment" {{\n            def Xform "Asset" (prepend references = @../010_ASS_USD/USD_Wrappers/{shape}/AssetROOT_{shape}{suffix}.usda@) {{}}\n        }}\n    }}\n'
    layer('020_BASE_LYR/GeoLyr'+suffix+'.usda', geo+'}', role='GeoLyr')
    op = '050_REVIEW_LYR/OpinLYR_'+('ColorVariants' if suffix else 'default')+'.usda'
    layer(op, role='Opinion')
    roles = [op, '020_BASE_LYR/TransLyr.usda', '020_BASE_LYR/VariLyr_ColorVariants.usda','020_BASE_LYR/GeoLyr_ColorVariants.usda'] if suffix else [op,'020_BASE_LYR/MatLyr.usda','020_BASE_LYR/TransLyr.usda','020_BASE_LYR/GeoLyr.usda']
    layer('SceneROOT_USDEssentials'+suffix+'.usda', sublayers=roles, root=True, opinion=op, role='Root')
layer('020_BASE_LYR/TransLyr.usda','over "World" {\n'+ '\n'.join(f'    over "{shape}01" {{\n        double3 xformOp:translate = ({x}, 0, 0)\n        uniform token[] xformOpOrder = ["xformOp:translate"]\n    }}' for shape,x in [('Cube',-75),('Cone',75)])+'\n}', role='TransLyr')
layer('020_BASE_LYR/MatLyr.usda','over "World" {\n    def Scope "Looks" (prepend references = @../010_ASS_USD/MatLib/Palette_v001.usda@) {}\n'+ '\n'.join(f'    over "{shape}01" {{\n        over "Adjustment" {{\n            over "Asset" {{\n                over "Geometry" (prepend apiSchemas = ["MaterialBindingAPI"]) {{\n                    rel material:binding = </World/Looks/{color}>\n                }}\n            }}\n        }}\n    }}' for shape,color in [('Cube','Red'),('Cone','Blue')])+'\n}', role='MatLyr')
layer('020_BASE_LYR/VariLyr_ColorVariants.usda','over "World" {\n'+ '\n'.join(f'    over "{shape}01" {{\n        over "Adjustment" {{\n            over "Asset" (variants = {{ string Color = "{color}" }}) {{}}\n        }}\n    }}' for shape,color in [('Cube','Red'),('Cone','Blue')])+'\n}', role='VariLyr')

# Preserve the supplied Omniverse baseline in each root (CC-01). It is a
# template input, never another sublayer/root in the scene composition.
template_path = DEST / 'defaultscene.usda'
template_text = template_path.read_text(encoding='utf-8-sig')
resources = {}
for asset in re.findall(r'@([^@]+)@', template_text):
    if asset == 'OmniPBR.mdl':
        continue  # Resolved by the installed Omniverse MDL search path.
    source = (template_path.parent / asset).resolve()
    if not source.is_file():
        # A relocated package already carries these exact template resources.
        source = DEST / '010_ASS_USD/Envs/OmniverseStandard/Resources' / Path(asset).name
    if not source.is_file():
        raise FileNotFoundError(f'Missing template resource: {asset}')
    relative = '010_ASS_USD/Envs/OmniverseStandard/Resources/' + source.name
    resources[relative] = source.read_bytes()
    template_text = template_text.replace('@' + asset + '@', '@./' + relative + '@')
for name in list(FILES):
    if not name.startswith('SceneROOT_'):
        continue
    authored = Sdf.Layer.CreateAnonymous('.usda')
    authored.ImportFromString(FILES[name])
    baseline = Sdf.Layer.CreateAnonymous('.usda')
    baseline.ImportFromString(template_text)
    baseline.subLayerPaths = list(authored.subLayerPaths)
    custom = dict(baseline.customLayerData)
    authored_custom = dict(authored.customLayerData)
    omni = dict(custom.get('omni_layer', {}))
    omni.update(authored_custom.pop('omni_layer', {}))
    custom.update(authored_custom)
    custom['omni_layer'] = omni
    custom['cc:startupTemplate'] = 'defaultscene.usda supplied Omniverse baseline'
    baseline.customLayerData = custom
    FILES[name] = baseline.ExportToString()
if args.roots_only:
    FILES = {name: text for name, text in FILES.items() if name.startswith('SceneROOT_')}
for relative, data in resources.items():
    target = DEST / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)

# Parse before replacing any authored file; preserve readable USDA formatting.
for name, content in FILES.items():
    parsed = Sdf.Layer.CreateAnonymous('.usda')
    if not parsed.ImportFromString(content):
        raise ValueError(name)
for name, content in FILES.items():
    target = DEST / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if '050_REVIEW_LYR' in target.parts and target.exists():
        continue  # Preserve authored experiments across rebuilds.
    target.write_bytes(content.encode('utf-8'))
helper = DEST / '_workflows/kit/session_defaults.py'
helper.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(REPO/'tools/kit/session_defaults.py', helper)
print(f'Authored {len(FILES)} USDA layers in {DEST}')
