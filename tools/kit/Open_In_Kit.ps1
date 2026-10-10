param(
    [ValidateSet('Standard', 'Manual', 'Scenarios', 'MaskedSize', 'MaskedSelection', 'STARTER')]
    [string]$Scene = 'Standard',
    [string]$KitExe,
    [string]$AppConfig
)
$ErrorActionPreference = 'Stop'
# Reuse the installed application's location, without modifying its configuration.
if (-not $KitExe -or -not $AppConfig) {
    $runningKit = Get-CimInstance Win32_Process -Filter "name='kit.exe'" |
        Select-Object -First 1
    if ($runningKit) {
        if (-not $KitExe) { $KitExe = $runningKit.ExecutablePath }
        if (-not $AppConfig -and $runningKit.CommandLine -match '"([^"\r\n]+\.kit)"') {
            $AppConfig = $Matches[1]
        }
    }
}
if (-not $KitExe -or -not $AppConfig) {
    throw 'Provide -KitExe <kit.exe> and -AppConfig <composer.kit>, or run while your Kit application is open.'
}
$kitPath = (Resolve-Path -LiteralPath $KitExe).Path
$appPath = (Resolve-Path -LiteralPath $AppConfig).Path
$startupScript = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '_workflows/kit/session_defaults.py')).Path
$sceneFile = if ($Scene -in @('Standard', 'Manual')) { 'SceneROOT_Example.usda' } else { "SceneROOT_$Scene.usda" }
$stagePath = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot $sceneFile)).Path
& $kitPath $appPath '--enable' 'omni.kit.usd.layers' '--exec' "`"$startupScript`"" "--/cc/sessionDefaults/stage=$stagePath"
