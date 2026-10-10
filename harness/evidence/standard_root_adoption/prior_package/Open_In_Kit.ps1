param(
    [ValidateSet('Manual', 'Scenarios', 'MaskedSize', 'MaskedSelection')]
    [string]$Scene = 'Manual',
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
$stagePath = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "World_$Scene.usda")).Path
& $kitPath $appPath '--enable' 'omni.kit.usd.layers' '--exec' "`"$startupScript`"" "--/cc/sessionDefaults/stage=$stagePath"
