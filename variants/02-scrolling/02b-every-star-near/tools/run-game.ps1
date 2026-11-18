param(
    [ValidateSet('Build','Play','PlayTest')][string]$Mode = 'Play',
    [ValidateSet('6581','8580')][string]$Model = '6581',
    [switch]$RealLoad,
    [string]$Python = '',
    [string]$Assembler = '',
    [string]$Vice = ''
)
# Starbraze II: build the program and run it in VICE. Run it from
# this folder's parent (the project) or from anywhere:
#   Build   write the data (game/assets/build_assets.py), check that no
#           line of the sources is longer than 60 characters
#           (tools/check_lines.py) and assemble with 64tass into
#           game/build: starbraze2.prg, .lst, .lbl and main.inc (its
#           labels); all twice: game/build, the game; game/build/test,
#           the test build (-D TEST_BUILD=1, which the program does not
#           read here), its own program;
#   Play    build, then start the program in VICE (x64sc): a PAL C64
#           with the SID chosen by -Model, a 1541 emulated as hardware
#           (the program loads in warp, as VICE's autostart does, or
#           with -RealLoad at its real speed), joystick 2 on the keypad;
#   PlayTest the same with the test build's program;
# 64tass, x64sc and python are looked for on the PATH; -Assembler,
# -Vice and -Python give their full paths instead.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent

function Find-Tool([string]$Given, [string[]]$Names, [string]$Switch) {
    if ($Given) {
        if (!(Test-Path -LiteralPath $Given)) { throw "Not found: $Given" }
        return $Given
    }
    foreach ($name in $Names) {
        $found = Get-Command $name -CommandType Application -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($found) { return $found.Source }
    }
    throw "$($Names[0]) is not on the PATH: add its folder to the PATH, or give its full path with $Switch."
}

function Build {
    & $Python 'game/assets/build_assets.py'
    if ($LASTEXITCODE -ne 0) { throw 'The data of game/assets could not be built: see the message above.' }
    & $Python 'tools/check_lines.py'
    if ($LASTEXITCODE -ne 0) { throw 'A line of the sources is longer than 60 characters.' }
    # the game, then the test build (TEST_BUILD)
    foreach ($b in @(@{ Dir = 'game/build'; Define = @() },
                     @{ Dir = 'game/build/test'; Define = @('-D', 'TEST_BUILD=1') })) {
        $d = $b.Dir
        $define = $b.Define
        New-Item -ItemType Directory -Force -Path $d | Out-Null
        & $Assembler --cbm-prg -Wall -Werror @define --vice-labels-numeric -l "$d/starbraze2.lbl" --normal-labels -l "$d/main.inc" -L "$d/starbraze2.lst" -o "$d/starbraze2.prg" game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw "64tass stopped ($d): its message names the file and the line." }
    }
}

$Python = Find-Tool $Python @('python', 'python3', 'py') '-Python'
$Assembler = Find-Tool $Assembler @('64tass') '-Assembler'
if ($Mode -ne 'Build') { $Vice = Find-Tool $Vice @('x64sc') '-Vice' }
else { try { $Vice = Find-Tool $Vice @('x64sc') '-Vice' } catch { $Vice = '' } }
$env:PYTHONDONTWRITEBYTECODE = '1'
Push-Location $root
try {
    New-Item -ItemType Directory -Force -Path 'game/build','evidence' | Out-Null
    Build
    if ($Mode -eq 'Play' -or $Mode -eq 'PlayTest') {
        $engine = @{ '6581' = '256'; '8580' = '257' }[$Model]
        $disk = if ($Mode -eq 'PlayTest') { 'game/build/test/starbraze2.prg' } else { 'game/build/starbraze2.prg' }
        $warp = if ($RealLoad) { '+autostart-warp' } else { '-autostart-warp' }
        $arguments = @('-default','-pal','-sound','-sidenginemodel',$engine,'+VICIIvcache',
            '-drive8type','1541','-drive8truedrive','+busdevice8',$warp,
            '-joydev2','1','-autostart',$disk)
        Start-Process -FilePath $Vice -ArgumentList $arguments -WorkingDirectory $root
    }
} finally {
    Pop-Location
}
