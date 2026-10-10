param([string]$Destination = $PSScriptRoot)
$ErrorActionPreference = 'Stop'
try {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archivePath = Join-Path $PSScriptRoot 'Composition_Starter.zip'
    if (-not (Test-Path -LiteralPath $archivePath -PathType Leaf)) {
        throw 'Keep the BAT, PS1 and Composition_Starter.zip together.'
    }
    $targetRoot = [IO.Path]::GetFullPath($Destination)
    $targetPrefix = $targetRoot.TrimEnd('\') + '\'
    $archive = [IO.Compression.ZipFile]::OpenRead($archivePath)
    try {
        $planned = @()
        $seen = @{}
        foreach ($entry in $archive.Entries) {
            $relative = $entry.FullName.Replace('/', '\')
            if ([IO.Path]::IsPathRooted($relative) -or $relative.Contains(':')) {
                throw "Unsupported archive path: $relative"
            }
            $target = [IO.Path]::GetFullPath((Join-Path $targetRoot $relative))
            if (-not $target.StartsWith($targetPrefix, [StringComparison]::OrdinalIgnoreCase)) {
                throw "Archive entry escapes destination: $relative"
            }
            if ($seen.ContainsKey($target)) { throw "Duplicate archive entry: $relative" }
            $seen[$target] = $true
            # Reject junction/symlink ancestors; no writes outside the selected directory.
            $ancestor = $target
            while ($ancestor) {
                if (Test-Path -LiteralPath $ancestor) {
                    $item = Get-Item -LiteralPath $ancestor -Force
                    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                        throw "Linked destination is unsupported: $ancestor"
                    }
                }
                $ancestor = [IO.Path]::GetDirectoryName($ancestor)
            }
            if ($entry.Name -eq '') { continue }
            if (Test-Path -LiteralPath $target) { throw "File already exists; nothing overwritten: $target" }
            $planned += @{ Entry = $entry; Target = $target }
        }
        foreach ($plan in $planned) {
            [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($plan.Target)) | Out-Null
            $inputStream = $plan.Entry.Open()
            try {
                $outputStream = [IO.File]::Open($plan.Target, [IO.FileMode]::CreateNew)
                try { $inputStream.CopyTo($outputStream) } finally { $outputStream.Dispose() }
            } finally { $inputStream.Dispose() }
        }
        Write-Host "Created $($planned.Count) preset files in $targetRoot"
        Write-Host 'Open SceneROOT_STARTER.usda through Open_In_Kit.ps1 for Opinion authoring and layer protection.'
        Write-Host 'Optional layers are authoring slots; simulation/runtime integrations are not installed.'
    } finally { $archive.Dispose() }
    exit 0
} catch {
    Write-Error "Setup stopped: $_. No existing files were overwritten. If extraction had started, new partial files may remain." -ErrorAction Continue
    exit 1
}
