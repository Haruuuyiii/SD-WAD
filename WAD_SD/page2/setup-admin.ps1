# ═══════════════════════════════════════════════════════════════
# CozMoz Admin Setup - PowerShell Version
# ═══════════════════════════════════════════════════════════════

Write-Host "`n$(('=')*60)"
Write-Host "  CozMoz Admin Setup"
Write-Host "$(('=')*60)`n"

# Read the SQL file
$sqlFile = "$PSScriptRoot\setup-admin.sql"

if (-not (Test-Path $sqlFile)) {
    Write-Host "[ERROR] setup-admin.sql not found`n"
    exit 1
}

Write-Host "[1] Reading SQL script...`n"
$sqlContent = Get-Content $sqlFile -Raw

Write-Host "[2] Executing SQL commands...`n"

# Try to find mysql executable
$mysqlPaths = @(
    "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe",
    "C:\xampp\mysql\bin\mysql.exe",
    "mysql"
)

$mysqlFound = $false
$mysqlExe = $null

foreach ($path in $mysqlPaths) {
    if (Test-Path $path) {
        $mysqlExe = $path
        $mysqlFound = $true
        break
    }
    
    try {
        $cmd = Get-Command $path -ErrorAction SilentlyContinue
        if ($cmd) {
            $mysqlExe = $cmd.Path
            $mysqlFound = $true
            break
        }
    } catch {
        # Continue
    }
}

if (-not $mysqlFound) {
    Write-Host "[ERROR] MySQL not found in PATH or common locations`n"
    Write-Host "   Please ensure MySQL is installed and added to PATH`n"
    exit 1
}

Write-Host "   Found MySQL: $mysqlExe`n"

# Execute SQL
try {
    $process = Start-Process -FilePath $mysqlExe -ArgumentList "-u", "root", "-h", "localhost" -NoNewWindow -RedirectStandardInput $null -PassThru -Wait
    $sqlContent | & $mysqlExe -u root -h localhost 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[SUCCESS] Admin user setup completed!`n"
        Write-Host "$(('=')*60)"
        Write-Host "  Setup Complete!"
        Write-Host "$(('=')*60)`n"
        Write-Host "Login credentials:"
        Write-Host "  Username: admin"
        Write-Host "  Password: admin123`n"
    } else {
        Write-Host "[ERROR] SQL execution failed`n"
        exit 1
    }
} catch {
    Write-Host "[ERROR] $_`n"
    exit 1
}
