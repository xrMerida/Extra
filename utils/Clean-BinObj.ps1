Get-ChildItem -Directory | ForEach-Object {
    $dirs = @("bin", "obj", ".vs")
    $path = $_.FullName
    $dirs | ForEach-Object {
        $target = Join-Path $path $_
        if (Test-Path $target) {
            Remove-Item -Recurse -Force $target
            Write-Host "Deleted: $target"
        }
    }
}
