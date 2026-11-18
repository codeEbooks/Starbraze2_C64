param(
    [ValidateSet('Build','Play','PlayTest','Verify','Games','Record')][string]$Mode = 'Play', # {17}
#|    [ValidateSet('Build','Play','PlayTest')][string]$Mode = 'Play', # {1-16}
    [ValidateSet('6581','8580')][string]$Model = '6581',
    [switch]$RealLoad,
    [string]$Python = '',
    [string]$Assembler = '',
    [string]$Vice = ''
)
# Starbraze II: build the program and run it in VICE. Run it from
# this folder's parent (the project) or from anywhere:
#   Build   write the data (game/assets/build_assets.py), check that no {16}
#           line of the sources is longer than 60 characters {16}
#           (tools/check_lines.py) and assemble with 64tass into {16}
#           game/build: starbraze2.prg, .lst, .lbl and main.inc (its {16}
#           labels, for the modules); the modules by themselves, each {16}
#           its .bin, .lst and .lbl: the GRAVEYARD WARDEN {16}
#           (game/src/warden.asm, at $f000), the VARKON CORVETTE {16}
#           (corvette.asm, at the same place), the station's module {16}
#           (station.asm, at $e000), the DEFENSE TURRET ARRAY {16}
#           (defense.asm, at $f000), the SUPER-COMPUTER VARKON {16}
#           (supercomp.asm, from SC_AT, below $f000), the escape's code {16}
#           (escape.asm, at SC_AT: level 6's file packs it); the disk, {16}
#           game/build/starbraze2.d64 (tools/make_disk.py, with VICE's {16}
#           c1541, next to x64sc): the program and the game's files {16}
#           (PHASE1 (levels 1 and 2, the title's module), LEVEL3 with {16}
#           the WARDEN, LEVEL4 with the CORVETTE, LEVEL5 with the {16}
#           station's module, its theme and the DEFENSE TURRET ARRAY, {16}
#           LEVEL6 with the station's module, the SUPER-COMPUTER VARKON {16}
#           and the escape); all twice: game/build, the game on the {16}
#           disk, without the keys I and L (the author, 11 November); {16}
#           game/build/test, the test build (-D TEST_BUILD=1: the keys I {16}
#           and L in it), its own program, modules, files and disk (the {16}
#           modules read their build's labels: -I); {16}
#|#   Build   write the data (game/assets/build_assets.py), check that no {15-15}
#|#           line of the sources is longer than 60 characters {15-15}
#|#           (tools/check_lines.py) and assemble with 64tass into {15-15}
#|#           game/build: starbraze2.prg, .lst, .lbl and main.inc (its {15-15}
#|#           labels, for the modules); the modules by themselves, each {15-15}
#|#           its .bin, .lst and .lbl: the GRAVEYARD WARDEN {15-15}
#|#           (game/src/warden.asm, at $f000), the VARKON CORVETTE {15-15}
#|#           (corvette.asm, at the same place), the station's module {15-15}
#|#           (station.asm, at $e000), the DEFENSE TURRET ARRAY {15-15}
#|#           (defense.asm, at $f000), the SUPER-COMPUTER VARKON {15-15}
#|#           (supercomp.asm, from SC_AT, below $f000), the escape's code {15-15}
#|#           (escape.asm, at SC_AT: level 6's file packs it); the disk, {15-15}
#|#           game/build/starbraze2.d64 (tools/make_disk.py, with VICE's {15-15}
#|#           c1541, next to x64sc): the program and the game's files {15-15}
#|#           (PHASE1 (levels 1 and 2, the module of title.asm), LEVEL3 {15-15}
#|#           with the WARDEN, LEVEL4 with the CORVETTE, LEVEL5 with the {15-15}
#|#           station's module, its theme and the DEFENSE TURRET ARRAY, {15-15}
#|#           LEVEL6 with the station's module, the SUPER-COMPUTER VARKON {15-15}
#|#           and the escape); all twice: game/build, the game on the {15-15}
#|#           disk, without the keys I and L (the author, 11 November); {15-15}
#|#           game/build/test, the test build (-D TEST_BUILD=1: the keys I {15-15}
#|#           and L in it), its own program, modules, files and disk (the {15-15}
#|#           modules read their build's labels: -I); {15-15}
#|#   Build   write the data (game/assets/build_assets.py), check that no {14-14}
#|#           line of the sources is longer than 60 characters {14-14}
#|#           (tools/check_lines.py) and assemble with 64tass into {14-14}
#|#           game/build: starbraze2.prg, .lst, .lbl and main.inc (its {14-14}
#|#           labels, for the modules); the modules by themselves, each {14-14}
#|#           its .bin, .lst and .lbl: the GRAVEYARD WARDEN {14-14}
#|#           (game/src/warden.asm, at $f000), the VARKON CORVETTE {14-14}
#|#           (corvette.asm, at the same place), the station's module {14-14}
#|#           (station.asm, at $e000), the DEFENSE TURRET ARRAY {14-14}
#|#           (defense.asm, at $f000), the SUPER-COMPUTER VARKON {14-14}
#|#           (supercomp.asm, from SC_AT, below $f000); the disk, {14-14}
#|#           game/build/starbraze2.d64 (tools/make_disk.py, with VICE's {14-14}
#|#           c1541, next to x64sc): the program and the game's files {14-14}
#|#           (PHASE1 (levels 1 and 2, the module of title.asm), LEVEL3 {14-14}
#|#           with the WARDEN, LEVEL4 with the CORVETTE, LEVEL5 with the {14-14}
#|#           station's module, its theme and the DEFENSE TURRET ARRAY, {14-14}
#|#           LEVEL6 with the station's module and the SUPER-COMPUTER {14-14}
#|#           VARKON); all twice: game/build, the game on the disk, {14-14}
#|#           without the keys I and L (the author, 11 November); {14-14}
#|#           game/build/test, the test build (-D TEST_BUILD=1: the keys I {14-14}
#|#           and L in it), its own program, modules, files and disk (the {14-14}
#|#           modules read their build's labels: -I); {14-14}
#|#   Build   write the data (game/assets/build_assets.py), check that no {13-13}
#|#           line of the sources is longer than 60 characters {13-13}
#|#           (tools/check_lines.py) and assemble with 64tass into {13-13}
#|#           game/build: starbraze2.prg, .lst, .lbl and main.inc (its {13-13}
#|#           labels, for the modules); the modules by themselves, each {13-13}
#|#           its .bin, .lst and .lbl: the GRAVEYARD WARDEN {13-13}
#|#           (game/src/warden.asm, at $f000), the VARKON CORVETTE {13-13}
#|#           (corvette.asm, at the same place), the station's module {13-13}
#|#           (station.asm, at $e000), the DEFENSE TURRET ARRAY {13-13}
#|#           (defense.asm, at $f000); the disk, game/build/starbraze2.d64 {13-13}
#|#           (tools/make_disk.py, with VICE's c1541, next to x64sc): the {13-13}
#|#           program and the game's files (PHASE1 (levels 1 and 2, the {13-13}
#|#           module of title.asm), LEVEL3 with the WARDEN, LEVEL4 with {13-13}
#|#           the CORVETTE, LEVEL5 with the station's module, its theme {13-13}
#|#           and the DEFENSE TURRET ARRAY); all twice: game/build, the {13-13}
#|#           game on the disk, without the keys I and L (the author, 11 {13-13}
#|#           November); game/build/test, the test build (-D TEST_BUILD=1: {13-13}
#|#           the keys I and L in it), its own program, modules, files and {13-13}
#|#           disk (the modules read their build's labels: -I); {13-13}
#|#   Build   write the data (game/assets/build_assets.py), check that no {12-12}
#|#           line of the sources is longer than 60 characters {12-12}
#|#           (tools/check_lines.py) and assemble with 64tass into {12-12}
#|#           game/build: starbraze2.prg, .lst, .lbl and main.inc (its {12-12}
#|#           labels, for the modules); the modules by themselves, each {12-12}
#|#           its .bin, .lst and .lbl: the GRAVEYARD WARDEN {12-12}
#|#           (game/src/warden.asm, at $f000), the VARKON CORVETTE {12-12}
#|#           (corvette.asm, at the same place); the disk, {12-12}
#|#           game/build/starbraze2.d64 (tools/make_disk.py, with VICE's {12-12}
#|#           c1541, next to x64sc): the program and the game's files {12-12}
#|#           (PHASE1 (levels 1 and 2, the module of title.asm), LEVEL3 {12-12}
#|#           with the WARDEN, LEVEL4 with the CORVETTE); all twice: {12-12}
#|#           game/build, the game on the disk, without the keys I and L {12-12}
#|#           (the author, 11 November); game/build/test, the test build {12-12}
#|#           (-D TEST_BUILD=1: the keys I and L in it), its own program, {12-12}
#|#           modules, files and disk (the modules read their build's {12-12}
#|#           labels: -I); {12-12}
#|#   Build   write the data (game/assets/build_assets.py), check that no {11-11}
#|#           line of the sources is longer than 60 characters {11-11}
#|#           (tools/check_lines.py) and assemble with 64tass into {11-11}
#|#           game/build: starbraze2.prg, .lst, .lbl and main.inc (its {11-11}
#|#           labels, for the modules); the modules by themselves, each {11-11}
#|#           its .bin, .lst and .lbl: the GRAVEYARD WARDEN {11-11}
#|#           (game/src/warden.asm, at $f000); the disk, {11-11}
#|#           game/build/starbraze2.d64 (tools/make_disk.py, with VICE's {11-11}
#|#           c1541, next to x64sc): the program and the game's files {11-11}
#|#           (PHASE1 (levels 1 and 2, the module of title.asm), LEVEL3 {11-11}
#|#           with the WARDEN); all twice: game/build, the game on the {11-11}
#|#           disk, without the keys I and L (the author, 11 November); {11-11}
#|#           game/build/test, the test build (-D TEST_BUILD=1: the keys I {11-11}
#|#           and L in it), its own program, modules, files and disk (the {11-11}
#|#           modules read their build's labels: -I); {11-11}
#|#   Build   write the data (game/assets/build_assets.py), check that no {10-10}
#|#           line of the sources is longer than 60 characters {10-10}
#|#           (tools/check_lines.py) and assemble with 64tass into {10-10}
#|#           game/build: starbraze2.prg, .lst, .lbl and main.inc (its {10-10}
#|#           labels); the disk, game/build/starbraze2.d64 {10-10}
#|#           (tools/make_disk.py, with VICE's c1541, next to x64sc): the {10-10}
#|#           program and the game's files (PHASE1 (levels 1 and 2, the {10-10}
#|#           module of title.asm), LEVEL3); all twice: game/build, the {10-10}
#|#           game on the disk, without the keys I and L (the author, 11 {10-10}
#|#           November); game/build/test, the test build (-D TEST_BUILD=1: {10-10}
#|#           the keys I and L in it), its own program, files and disk; {10-10}
#|#   Build   write the data (game/assets/build_assets.py), check that no {3-9}
#|#           line of the sources is longer than 60 characters {3-9}
#|#           (tools/check_lines.py) and assemble with 64tass into {3-9}
#|#           game/build: starbraze2.prg, .lst, .lbl and main.inc (its {3-9}
#|#           labels); all twice: game/build, the game, without the keys I {3-9}
#|#           and L (the author, 11 November); game/build/test, the test {3-9}
#|#           build (-D TEST_BUILD=1: the keys I and L in it), its own {3-9}
#|#           program; {3-9}
#|#   Build   write the data (game/assets/build_assets.py), check that no {1-2}
#|#           line of the sources is longer than 60 characters {1-2}
#|#           (tools/check_lines.py) and assemble with 64tass into {1-2}
#|#           game/build: starbraze2.prg, .lst, .lbl and main.inc (its {1-2}
#|#           labels); all twice: game/build, the game; game/build/test, {1-2}
#|#           the test build (-D TEST_BUILD=1, which the program does not {1-2}
#|#           read here), its own program; {1-2}
#   Play    build, then start the game from its disk in VICE (x64sc): a {10}
#           PAL C64 with the SID chosen by -Model, a 1541 emulated as {10}
#           hardware (the program loads in warp, as VICE's autostart {10}
#           does, or with -RealLoad at its real speed, about two {10}
#           minutes; the game's files load from the disk at their real {10}
#           speed), joystick 2 on the keypad; {10}
#|#   Play    build, then start the program in VICE (x64sc): a PAL C64 {1-9}
#|#           with the SID chosen by -Model, a 1541 emulated as hardware {1-9}
#|#           (the program loads in warp, as VICE's autostart does, or {1-9}
#|#           with -RealLoad at its real speed), joystick 2 on the keypad; {1-9}
#   PlayTest the same with the test build's disk: the keys I and L in {10}
#           it; {10}
#|#   PlayTest the same with the test build's program: the keys I and L in {3-9}
#|#           it; {3-9}
#|#   PlayTest the same with the test build's program; {1-2}
#   Verify  build, then run the test (tests/verify_game.py): a pilot {17}
#           flies level 1 twice with the three ships and their twelve {17}
#           weapons, taking the capsules, in the four sound modes, and {17}
#           against the boss; then levels 2 to 6, each from its file {17}
#           from level 3 on, with their bosses, the escape and the {17}
#           victory; the title, the choice of the ship, the pause, GAME {17}
#           OVER; the keys I and L; frame by frame against the models {17}
#           and the reference pictures, about forty minutes (on the test {17}
#           build); then the levels' checks (tests/levels.py), the {17}
#           keyboard's (tests/keys.py, both builds) and the game's disk {17}
#           (tests/disk.py); {17}
#   Games   build, then four whole games on the game's disk {17}
#           (tests/whole_games.py): LOAD"*",8,1 and RUN typed and {17}
#           measured, the pilot to the victory with the three ships, {17}
#           then a GAME OVER in level 5; frame by frame as Verify, about {17}
#           two hours; {17}
#   Record  build, then assemble the programs for the recordings (-D {17}
#           RECORD_THEME=1: MUSIC at the start; -D RECORD_GAME=1: MUSIC {17}
#           + FX with Fire held; -D RECORD_SFX=1: the effects one after {17}
#           the other; -D RECORD_GAME=1 with -D RECORD_MUTE=4, the music {17}
#           alone, and =3, the effects alone; -D RECORD_THEME=1 with -D {17}
#           RECORD_SONG=1, the theme of space, and =3, 2, 4, 5, 6, the {17}
#           title's theme, the bosses' and the three jingles; -D {17}
#           RECORD_THEME=1 -D RECORD_LEVEL=5, the station's theme, level {17}
#           5's file from the disk) and record them from VICE's SID, {17}
#           6581 and 8580 (tools/record_music.py), then the effects {17}
#           against the music in MUSIC + FX (tools/sound_balance.py); in {17}
#           real time, about twenty-five minutes: {17}
#           evidence/starbraze2-*.wav, sound-*.json, game/build/*.mp3. {17}
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
    # the game on the disk, then the test build (TEST_BUILD) {10}
#|    # the game, then the test build (TEST_BUILD) {1-9}
    foreach ($b in @(@{ Dir = 'game/build'; Define = @() },
                     @{ Dir = 'game/build/test'; Define = @('-D', 'TEST_BUILD=1') })) {
        $d = $b.Dir
        $define = $b.Define
        New-Item -ItemType Directory -Force -Path $d | Out-Null
        & $Assembler --cbm-prg -Wall -Werror @define --vice-labels-numeric -l "$d/starbraze2.lbl" --normal-labels -l "$d/main.inc" -L "$d/starbraze2.lst" -o "$d/starbraze2.prg" game/src/main.asm
        if ($LASTEXITCODE -ne 0) { throw "64tass stopped ($d): its message names the file and the line." }
        $modules = [ordered]@{ 'warden' = 'the GRAVEYARD WARDEN'; 'corvette' = 'the VARKON CORVETTE'; # {15}
            'station' = 'the station''s module'; 'defense' = 'the DEFENSE TURRET ARRAY'; # {15}
            'supercomp' = 'the SUPER-COMPUTER VARKON'; 'escape' = 'the escape' } # {15}
#|        $modules = [ordered]@{ 'warden' = 'the GRAVEYARD WARDEN' } # {11-11}
#|        $modules = [ordered]@{ 'warden' = 'the GRAVEYARD WARDEN'; 'corvette' = 'the VARKON CORVETTE' } # {12-12}
#|        $modules = [ordered]@{ 'warden' = 'the GRAVEYARD WARDEN'; 'corvette' = 'the VARKON CORVETTE'; # {13-14}
#|            'station' = 'the station''s module'; 'defense' = 'the DEFENSE TURRET ARRAY' } # {13-13}
#|            'station' = 'the station''s module'; 'defense' = 'the DEFENSE TURRET ARRAY'; # {14-14}
#|            'supercomp' = 'the SUPER-COMPUTER VARKON' } # {14-14}
        foreach ($m in $modules.Keys) { # {11}
            & $Assembler --nostart -Wall -Werror -I $d --vice-labels-numeric -l "$d/$m.lbl" -L "$d/$m.lst" -o "$d/$m.bin" "game/src/$m.asm" # {11}
            if ($LASTEXITCODE -ne 0) { throw "64tass stopped on $($modules[$m]) (game/src/$m.asm, $d): its message names the file and the line." } # {11}
        } # {11}
        if ($Vice) { & $Python 'tools/make_disk.py' --build $d --vice $Vice } else { & $Python 'tools/make_disk.py' --build $d } # {10}
        if ($LASTEXITCODE -ne 0) { throw "The disk could not be made ($d): see the message above (c1541 is next to x64sc)." } # {10}
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
    if ($Mode -eq 'Verify') { # {17}
        & $Python 'tests/verify_game.py' --vice $Vice # {17}
        if ($LASTEXITCODE -ne 0) { throw 'The test failed: see evidence/game-test.json.' } # {17}
        & $Python 'tests/levels.py' # {17}
        if ($LASTEXITCODE -ne 0) { throw 'The checks of the levels failed: see evidence/levels.json.' } # {17}
        & $Python 'tests/keys.py' # {17}
        if ($LASTEXITCODE -ne 0) { throw 'The check of the keyboard failed: see evidence/keys.json.' } # {17}
        & $Python 'tests/disk.py' # {17}
        if ($LASTEXITCODE -ne 0) { throw 'The check of the game''s disk failed: see evidence/disk.json.' } # {17}
    } elseif ($Mode -eq 'Games') { # {17}
        & $Python 'tests/whole_games.py' --vice $Vice # {17}
        if ($LASTEXITCODE -ne 0) { throw 'The whole games failed: see evidence/whole-games.json.' } # {17}
    } elseif ($Mode -eq 'Record') { # {17}
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_THEME=1 -o game/build/starbraze2-theme.prg game/src/main.asm # {17}
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of the theme.' } # {17}
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_THEME=1 -D RECORD_SONG=1 -o game/build/starbraze2-space.prg game/src/main.asm # {17}
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of the theme of space.' } # {17}
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_THEME=1 -D RECORD_LEVEL=5 -o game/build/starbraze2-station.prg game/src/main.asm # {17}
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of the station''s theme.' } # {17}
        $songs = @{ 'boss' = 2; 'title' = 3; 'clear' = 4; 'over' = 5; 'win' = 6 } # {17}
        foreach ($what in 'title', 'boss', 'clear', 'over', 'win') { # {17}
            & $Assembler --cbm-prg -Wall -Werror -D RECORD_THEME=1 -D "RECORD_SONG=$($songs[$what])" -o "game/build/starbraze2-$what.prg" game/src/main.asm # {17}
            if ($LASTEXITCODE -ne 0) { throw "64tass stopped on the program for the recording of the song $what." } # {17}
        } # {17}
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_GAME=1 -o game/build/starbraze2-game.prg game/src/main.asm # {17}
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of the game.' } # {17}
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_SFX=1 -o game/build/starbraze2-sfx.prg game/src/main.asm # {17}
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the recording of the effects.' } # {17}
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_GAME=1 -D RECORD_MUTE=4 -o game/build/starbraze2-game-music.prg game/src/main.asm # {17}
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the music alone.' } # {17}
        & $Assembler --cbm-prg -Wall -Werror -D RECORD_GAME=1 -D RECORD_MUTE=3 -o game/build/starbraze2-game-fx.prg game/src/main.asm # {17}
        if ($LASTEXITCODE -ne 0) { throw '64tass stopped on the program for the effects alone.' } # {17}
        foreach ($what in 'theme', 'space', 'station', 'title', 'boss', 'clear', 'over', 'win', 'game', 'sfx') { # {17}
            foreach ($chip in '6581', '8580') { # {17}
                & $Python 'tools/record_music.py' --vice $Vice --model $chip --what $what # {17}
                if ($LASTEXITCODE -ne 0) { throw "The recording failed ($what, $chip): see evidence/." } # {17}
            } # {17}
        } # {17}
        foreach ($chip in '6581', '8580') { # {17}
            & $Python 'tools/sound_balance.py' --vice $Vice --model $chip # {17}
            if ($LASTEXITCODE -ne 0) { throw "The measure of the effects against the music failed ($chip): see evidence/." } # {17}
        } # {17}
    } elseif ($Mode -eq 'Play' -or $Mode -eq 'PlayTest') { # {17}
#|    if ($Mode -eq 'Play' -or $Mode -eq 'PlayTest') { # {1-16}
        $engine = @{ '6581' = '256'; '8580' = '257' }[$Model]
        $disk = if ($Mode -eq 'PlayTest') { 'game/build/test/starbraze2.d64' } else { 'game/build/starbraze2.d64' } # {10}
#|        $disk = if ($Mode -eq 'PlayTest') { 'game/build/test/starbraze2.prg' } else { 'game/build/starbraze2.prg' } # {1-9}
        $warp = if ($RealLoad) { '+autostart-warp' } else { '-autostart-warp' }
        $arguments = @('-default','-pal','-sound','-sidenginemodel',$engine,'+VICIIvcache',
            '-drive8type','1541','-drive8truedrive','+busdevice8',$warp,
            '-joydev2','1','-autostart',$disk)
        Start-Process -FilePath $Vice -ArgumentList $arguments -WorkingDirectory $root
    }
} finally {
    Pop-Location
}
