# Evidence

The retained build_manifest.json predates Opinion layers and the expanded SceneROOT_STARTER preset. Its hashes, inventory and startup-policy observations are historical; they do not validate the current Opinion default or starter. No acceptance tests or Kit runtime check were run for these additions.

build_manifest.json records runtime, file identities and saved defaults of SceneROOT_Example plus four companion entrypoints. It includes stage metrics, the World matrix, camera choice and cube opinions. Expected outcomes live in _contracts/expected.json. This is not a full acceptance test; Kit runtime and viewport observations remain pending.
