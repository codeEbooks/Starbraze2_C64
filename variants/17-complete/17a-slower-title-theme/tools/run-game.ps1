param(
    [ValidateSet('Build','Play','PlayTest','Verify','Games','Record')][string]$Mode = 'Play',
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
#           labels, for the modules); the modules by themselves, each
#           its .bin, .lst and .lbl: the GRAVEYARD WARDEN
#           (game/src/warden.asm, at $f000), the VARKON CORVETTE
#           (corvette.asm, at the same place), the station's module
#           (station.asm, at $e000), the DEFENSE TURRET ARRAY
#           (defense.asm, at $f000), the SUPER-COMPUTER VARKON
#           (supercomp.asm, from SC_AT, below $f000), the escape's code
#           (escape.asm, at SC_AT: level 6's file packs it); the disk,
#           game/build/starbraze2.d64 (tools/make_disk.py, with VICE's
#           c1541, next to x64sc): the program and the game's files
#           (PHASE1 (levels 1 and 2, the title's module), LEVEL3 with
#           the WARDEN, LEVEL4 with the CORVETTE, LEVEL5 with the
#           station's module, its theme and the DEFENSE TURRET ARRAY,
#           LEVEL6 with the station's module, the SUPER-COMPUTER VARKON
#           and the escape); all twice: game/build, the game on the
#           disk, without the keys I and L (the author, 11 November);
#           game/build/test, the test build (-D TEST_BUILD=1: the keys I
#           and L in it), its own program, modules, files and disk (the
#           modules read their build's labels: -I);
#   Play    build, then start the game from its disk in VICE (x64sc): a
#           PAL C64 with the SID chosen by -Model, a 1541 emulated as
#           hardware (the program loads in warp, as VICE's autostart
#           does, or with -RealLoad at its real speed, about two
#           minutes; the game's files load from the disk at their real
#           speed), joystick 2 on the keypad;
#   PlayTest the same with the test build's disk: the keys I and L in
#           it;
#   Verify  build, then run the test (tests/verify_game.py): a pilot
#           flies level 1 twice with the three ships and their twelve
#           weapons, taking the capsules, in the four sound modes, and
#           against the boss; then levels 2 to 6, each from its file
#           from level 3 on, with their bosses, the escape and the
#           victory; the title, the choice of the ship, the pause, GAME
#           OVER; the keys I and L; frame by frame against the models
#           and the reference pictures, about forty minutes (on the test
#           build); then the levels' checks (tests/levels.py), the
#           keyboard's (tests/keys.py, both builds) and the game's disk
#           (tests/disk.py);
#   Games   build, then four whole games on the game's disk
#           (tests/whole_games.py): LOAD"*",8,1 and RUN typed and
#           measured, the pilot to the victory with the three ships,
#           then a GAME OVER in level 5; frame by frame as Verify, about
#           two hours;
#   Record  build, then assemble the programs for the recordings (-D
#           RECORD_THEME=1: MUSIC at the start; -D RECORD_GAME=1: MUSIC
#           + FX with Fire held; -D RECORD_SFX=1: the effects one after
#           the other; -D RECORD_GAME=1 with -D RECORD_MUTE=4, the music
#           alone, and =3, the effects alone; -D RECORD_THEME=1 with -D
#           RECORD_SONG=1, the theme of space, and =3, 2, 4, 5, 6, the
#           title's theme, the bosses' and the three jingles; -D
#           RECORD_THEME=1 -D RECORD_LEVEL=5, the station's theme, level
#           5's file from the disk) and record them from VICE's SID,
#           6581 and 8580 (tools/record_music.py), then the effects
#           against the music in MUSIC + FX (tools/sound_balance.py); in
#           real time, about twenty-five minutes:
#           evidence/starbraze2-*.wav, sound-*.json, game/build/*.mp3.
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
    # the game on the disk, then the test build (TEST_BUILD)
    foreach ($b in @(@{ Dir = 'game/build'; Define = @() },
                     @{ Dir = 'game/build/test'; Define = @('-D', 'TEST_BUILD=1') })) {
        $d = $b.Dir
        $define = $b.Define
        New-Item -ItemType Directory -Force -Path $d | Out-Null
        & $Assembler --cbm-prg -Wall -Werror @define --vice-labels-numeric -l "$d/starbraze2.lbl" --normal-labels -l "$d/main.inc" -L "$d/starbraze2.lst" -o "$d/starbraze2.prg" game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw "64tass stopped ($d): its message names the file and the line." }
        $modules = [ordered]@{ 'warden' = 'the GRAVEYARD WARDEN'; 'corvette' = 'the VARKON CORVETTE';
            'station' = 'the station''s module'; 'defense' = 'the DEFENSE TURRET ARRAY';
            'supercomp' = 'the SUPER-COMPUTER VARKON'; 'escape' = 'the escape' }
        foreach ($m in $modules.Keys) {
            & $Assembler --nostart -Wall -Werror -I $d --vice-labels-numeric -l "$d/$m.lbl" -L "$d/$m.lst" -o "$d/$m.bin" "game/src/$m.asm"
            if ($LASTEXITCODE -ne 0) { throw "64tass stopped on $($modules[$m]) (game/src/$m.asm, $d): its message names the file and the line." }
        }
        if ($Vice) { & $Python 'tools/make_disk.py' --build $d --vice $Vice } else { & $Python 'tools/make_disk.py' --build $d }
        if ($LASTEXITCODE -ne 0) { throw "The disk could not be made ($d): see the message above (c1541 is next to x64sc)." }
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
    if ($Mode -eq 'Verify') {
        & $Python 'tests/verify_game.py' --vice $Vice
        if ($LASTEXITCODE -ne 0) { throw 'The test failed: see evidence/game-test.json.' }
        & $Python 'tests/levels.py'
        if ($LASTEXITCODE -ne 0) { throw 'The checks of the levels failed: see evidence/levels.json.' }
        & $Python 'tests/keys.py'
        if ($LASTEXITCODE -ne 0) { throw 'The check of the keyboard failed: see evidence/keys.json.' }
        & $Python 'tests/disk.py'
        if ($LASTEXITCODE -ne 0) { throw 'The check of the game''s disk failed: see evidence/disk.json.' }
    } elseif ($Mode -eq 'Games') {
        & $Python 'tests/whole_games.py' --vice $Vice
        if ($LASTEXITCODE -ne 0) { throw 'The whole games failed: see evidence/whole-games.json.' }
    } elseif ($Mode -eq 'Record') {
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_THEME=1 -o game/build/starbraze2-theme.prg game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of the theme.' }
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_THEME=1 -D RECORD_SONG=1 -o game/build/starbraze2-space.prg game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of the theme of space.' }
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_THEME=1 -D RECORD_LEVEL=5 -o game/build/starbraze2-station.prg game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of the station''s theme.' }
        $songs = @{ 'boss' = 2; 'title' = 3; 'clear' = 4; 'over' = 5; 'win' = 6 }
        foreach ($what in 'title', 'boss', 'clear', 'over', 'win') {
            & $Assembler --cbm-prg -Wall -Werror -D RECORD_THEME=1 -D "RECORD_SONG=$($songs[$what])" -o "game/build/starbraze2-$what.prg" game/src/main.asm
            if ($LASTEXITCODE -ne 0) { throw "64tass stopped on the program for the recording of the song $what." }
        }
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_GAME=1 -o game/build/starbraze2-game.prg game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of the game.' }
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_SFX=1 -o game/build/starbraze2-sfx.prg game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of the effects.' }
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_GAME=1 -D RECORD_MUTE=4 -o game/build/starbraze2-game-music.prg game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the music alone.' }
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_GAME=1 -D RECORD_MUTE=3 -o game/build/starbraze2-game-fx.prg game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the effects alone.' }
        foreach ($what in 'theme', 'space', 'station', 'title', 'boss', 'clear', 'over', 'win', 'game', 'sfx') {
            foreach ($chip in '6581', '8580') {
                & $Python 'tools/record_music.py' --vice $Vice --model $chip --what $what
                if ($LASTEXITCODE -ne 0) { throw "The recording failed ($what, $chip): see evidence/." }
            }
        }
        foreach ($chip in '6581', '8580') {
            & $Python 'tools/sound_balance.py' --vice $Vice --model $chip
            if ($LASTEXITCODE -ne 0) { throw "The measure of the effects against the music failed ($chip): see evidence/." }
        }
    } elseif ($Mode -eq 'Play' -or $Mode -eq 'PlayTest') {
        $engine = @{ '6581' = '256'; '8580' = '257' }[$Model]
        $disk = if ($Mode -eq 'PlayTest') { 'game/build/test/starbraze2.d64' } else { 'game/build/starbraze2.d64' }
        $warp = if ($RealLoad) { '+autostart-warp' } else { '-autostart-warp' }
        $arguments = @('-default','-pal','-sound','-sidenginemodel',$engine,'+VICIIvcache',
            '-drive8type','1541','-drive8truedrive','+busdevice8',$warp,
            '-joydev2','1','-autostart',$disk)
        Start-Process -FilePath $Vice -ArgumentList $arguments -WorkingDirectory $root
    }
} finally {
    Pop-Location
}
