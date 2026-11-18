; STARBRAZE II 1.0 - the whole game, PAL C64 with a 1541. {17}
; Assemble this file: it includes the others. {17}
;|; STARBRAZE II, step 1 of 17: the canyons. PAL C64. Assemble {1-1}
;|; this file: it includes the others. {1-1}
;|; STARBRAZE II, step 2 of 17: scrolling. PAL C64. Assemble {2-2}
;|; this file: it includes the others. {2-2}
;|; STARBRAZE II, step 3 of 17: the ships. PAL C64. Assemble {3-3}
;|; this file: it includes the others. {3-3}
;|; STARBRAZE II, step 4 of 17: the Varkon. PAL C64. Assemble {4-4}
;|; this file: it includes the others. {4-4}
;|; STARBRAZE II, step 5 of 17: hits and score. PAL C64. {5-5}
;|; Assemble this file: it includes the others. {5-5}
;|; STARBRAZE II, step 6 of 17: weapons and capsules. PAL C64. {6-6}
;|; Assemble this file: it includes the others. {6-6}
;|; STARBRAZE II, step 7 of 17: the SID. PAL C64. Assemble {7-7}
;|; this file: it includes the others. {7-7}
;|; STARBRAZE II, step 8 of 17: the SIEGE CRAWLER. PAL C64. {8-8}
;|; Assemble this file: it includes the others. {8-8}
;|; STARBRAZE II, step 9 of 17: level 2 and the SHIELD CORE. {9-9}
;|; PAL C64. Assemble this file: it includes the others. {9-9}
;|; STARBRAZE II, step 10 of 17: the disk. PAL C64 with a {10-10}
;|; 1541. Assemble this file: it includes the others. {10-10}
;|; STARBRAZE II, step 11 of 17: the GRAVEYARD WARDEN. PAL C64 {11-11}
;|; with a 1541. Assemble this file: it includes the others. {11-11}
;|; STARBRAZE II, step 12 of 17: the VARKON CORVETTE. PAL C64 {12-12}
;|; with a 1541. Assemble this file: it includes the others. {12-12}
;|; STARBRAZE II, step 13 of 17: the DEFENSE TURRET ARRAY. PAL {13-13}
;|; C64 with a 1541. Assemble this file: it includes the {13-13}
;|; others. {13-13}
;|; STARBRAZE II, step 14 of 17: the SUPER-COMPUTER VARKON. {14-14}
;|; PAL C64 with a 1541. Assemble this file: it includes the {14-14}
;|; others. {14-14}
;|; STARBRAZE II, step 15 of 17: the escape. PAL C64 with a {15-15}
;|; 1541. Assemble this file: it includes the others. {15-15}
;|; STARBRAZE II, step 16 of 17: the states. PAL C64 with a {16-16}
;|; 1541. Assemble this file: it includes the others. {16-16}
;
; Level 1, THE CANYONS of Varkonia Prime:
;|;  - The start of the level, still: the near layer (rows {1-1}
;|;    0-9, 14-21), the far mesas (rows 10-13), the HUD (rows {1-1}
;|;    22-24). {1-1}
;  - It scrolls from right to left at the speeds of the {2}
;    level, with the far mesas at half speed and the stars {2}
;    in three planes, to the arena at its end. {2}
;  - The ship flies in it (joystick 2, Fire; SPACE the {16}
;    pause) and meets its rock. {16}
;|;  - The ship flies in it (joystick 2, Fire) and meets its {4-15}
;|;    rock. {4-15}
;|;  - The ship flies in it (joystick 2) and meets its rock. {3-3}
;  - The level's script brings its Varkon: raiders, drones, {4}
;    lancers, leapers on the rock, the flak turrets of the {4}
;    mesas, the carriers in gold; up to 24 objects on {4}
;    sprites 2-7, the multiplexer puts them down the screen. {4}
;  - The ship's shots destroy them, their plasma and their {5}
;    bodies cost the ship its shield; the score. {5}
;  - Each ship's weapon has four levels; the carriers leave {6}
;    their capsules: W the weapon, S speed, M the missile, O {6}
;    the satellite, E the shield. {6}
;  - The theme of the level plays on the SID; F1, F3, F5, F7 {7}
;    choose the sound: MUSIC, MUSIC + FX, SOUND FX, SILENT. {7}
;  - In the arena, its boss: the SIEGE CRAWLER (boss.asm); {8}
;    STAGE CLEAR, then the next level. {8}
; {9}
; Level 2, SHIELD GENERATORS, in deep space: towers with {9}
; their fields (varkon.asm), beams (beams.asm), clouds that {9}
; are not rock; its boss, the SHIELD CORE (core.asm, {9}
; sphere.asm), on the boss engine made common (boss.asm). {9}
; {10}
; Level 3, GRAVEYARD OF HELIOS: the scouts, the gunships and {11}
; their fans, the mines, the rocks and their shards {11}
; (varkon.asm, hits.asm), the alien's spines (beams.asm), {11}
; the theme of space (player.asm); its boss, the GRAVEYARD {11}
; WARDEN (warden.asm, assembled by itself, its code from the {11}
; disk). {11}
;|; Level 3, GRAVEYARD OF HELIOS: the scouts, the gunships and {10-10}
;|; their fans, the mines, the rocks and their shards {10-10}
;|; (varkon.asm, hits.asm), the alien's spines (beams.asm), {10-10}
;|; the theme of space (player.asm); its arena has no boss: {10-10}
;|; STAGE CLEAR at once. {10-10}
; {12}
; Level 4, THE BLOODY ORBIT: the heavy lancers, the gold {12}
; scouts, the station's hull and its turrets; its boss, the {12}
; VARKON CORVETTE (corvette.asm). {12}
; {13}
; Level 5, VARKON-OMEGA, the station: its crawlers, laser {13}
; mines and turrets on the ceiling, its theme (station.asm); {13}
; its boss, the DEFENSE TURRET ARRAY (defense.asm). {13}
; {14}
; Level 6, THE CORE: guardians, eggs, barriers and their {14}
; energy (station.asm); its boss, the SUPER-COMPUTER VARKON {14}
; (supercomp.asm). {14}
; {15}
; Level 7, THE ESCAPE: out of the station against the clock {16}
; (escape.asm, its code in LEVEL6's file); then the victory, {16}
; and the title. {16}
;|; Level 7, THE ESCAPE: out of the station against the clock {15-15}
;|; (escape.asm, its code in LEVEL6's file); then the victory, {15-15}
;|; and the game again from level 1. {15-15}
; {10}
; The game is on a disk: the PRG brings phase 1 (the planet: {14}
; levels 1 and 2); the file of a level from 3 on (LEVEL3 to {14}
; LEVEL6) is read with the KERNAL's routines when the level {14}
; starts (phase.asm, the loading screen phase_show.asm). {14}
;|; The game is on a disk: the PRG brings phase 1 (the planet: {13-13}
;|; levels 1 and 2); the file of a level from 3 on (LEVEL3 to {13-13}
;|; LEVEL5) is read with the KERNAL's routines when the level {13-13}
;|; starts (phase.asm, the loading screen phase_show.asm). {13-13}
;|; The game is on a disk: the PRG brings phase 1 (the planet: {12-12}
;|; levels 1 and 2); the file of a level from 3 on (LEVEL3, {12-12}
;|; LEVEL4) is read with the KERNAL's routines when the level {12-12}
;|; starts (phase.asm, the loading screen phase_show.asm). {12-12}
;|; The game is on a disk: the PRG brings phase 1 (the planet: {10-11}
;|; levels 1 and 2); the file of a level from 3 on (LEVEL3) is {10-11}
;|; read with the KERNAL's routines when the level starts {10-11}
;|; (phase.asm, the loading screen phase_show.asm). {10-11}
; {16}
; The states: the title (title.asm, phase 1's store), the {16}
; choice of the ship at the start and after each ship lost {16}
; (choice.asm), the pause, GAME OVER (states.asm). {16}
; {17}
; The songs: the title's theme, the bosses', the jingles {17}
; (player.asm). {17}
; {3}
; With -D TEST_BUILD=1 the test build: the keys I and L for {10}
; the tests by hand (ship.asm, test_step): I, the ship that {10}
; cannot be hurt; L, the next level at once. The game on the {10}
; disk is without them (the author, 11 November: «Via dal {10}
; disco, restano in una build di prova»). {10}
;|; With -D TEST_BUILD=1 the test build: the keys I and L for {3-9}
;|; the tests by hand (ship.asm, test_step): I, the ship that {3-9}
;|; cannot be hurt; L, the next level at once. The game is {3-9}
;|; without them (the author, 11 November: «Via dal disco, {3-9}
;|; restano in una build di prova»). {3-9}
; {17}
; The recordings (any RECORD_ below) start the game at once: {17}
; no title, no choice of the ship; in those of the sound {17}
; (THEME, GAME, SFX) the ship cannot be hurt: a ship lost {17}
; would hold the game, silent. With -D RECORD_THEME=1 the {17}
; program starts in MUSIC (the theme on three voices); with {17}
; -D RECORD_GAME=1 Fire is held; with -D RECORD_SFX=1 it {17}
; plays the sound effects one after the other {17}
; (tools/record_music.py records them). With -D {17}
; RECORD_MUTE=n (only to measure) voices are silent in the {17}
; SID: bit 0 voice 1, bit 1 voice 2, bit 2 voice 3 {17}
; (tools/sound_balance.py). With -D RECORD_SONG=n every {17}
; level plays song n (1: the theme of space; 2 the bosses', {17}
; 3 the title's, 4-6 the jingles). With -D RECORD_LEVEL=n {17}
; (only to record the station's theme) the program starts in {17}
; level n, its file from the disk, the ship that cannot be {17}
; hurt. The recordings are made without the test build's {17}
; keys, as the game. {17}
        .cpu "6502"
        .weak ; {3}
TEST_BUILD = 0                  ; 0: the game on the disk {10}
;|TEST_BUILD = 0                  ; 0: the game {3-9}
RECORD_THEME = 0                ; 0: the game as it is {17}
RECORD_GAME = 0 ; {17}
RECORD_SFX  = 0 ; {17}
RECORD_MUTE = 0 ; {17}
RECORD_SONG = 0 ; {17}
RECORD_LEVEL = 0 ; {17}
REC_SOUND = RECORD_THEME | RECORD_GAME | RECORD_SFX ; {17}
REC_MORE = RECORD_MUTE | RECORD_SONG | RECORD_LEVEL ; {17}
RECORDING = (REC_SOUND | REC_MORE) != 0 ; {17}
        .endweak ; {3}
        .include "memory.asm"
        .include "../assets/generated/assets.inc"

        * = $0801
        .word basic_end         ; BASIC line: 10 SYS 2061
        .word 10
        .byte $9e
        .text "2061"
        .byte 0
basic_end:
        .word 0

entry:
        sei                     ; no interrupts here
        cld
        ldx #$ff                ; fresh stack
        txs
        lda $ba                 ; the drive it came {10}
        cmp #8                  ; from: the phases' too (8 {10}
        bcs +                   ; when not from a drive) {10}
        lda #8 ; {10}
+       sta disk_dev ; {10}
        lda #1                  ; file 1's store (phase 1): {10}
        sta file_now            ; the PRG brings it {10}
        jsr kernal_out          ; BASIC and KERNAL out
        jsr move_store          ; the packed levels,
                                ; title.asm's module
        jsr sound_init          ; the SID's copy, silent {7}
        jsr score_init          ; 0, the best 0 {5}
        .if RECORDING ; {17}
        jmp game_start          ; no title {17}
        .else ; {17}
        jmp title               ; title.asm {16}
        .fi ; {17}
;|        jmp game_start ; {1-15}

; The main loop: one turn a frame, when the HUD starts. {5}
; First what has a deadline at the top of the screen: the {5}
; camera, the ship and the sprites; then the screens' work, {5}
; the camera of the next turn, the Varkon of the next frame {5}
; (with the hits); then, in the frame's lower half, rows 0-9 {5}
; of the next frame (ahead). {5}
;|; The main loop: one turn a frame, when the HUD starts. {4-4}
;|; First what has a deadline at the top of the screen: the {4-4}
;|; camera, the ship and the sprites; then the screens' work, {4-4}
;|; the camera of the next turn, the Varkon of the next frame; {4-4}
;|; then, in the frame's lower half, rows 0-9 of the next {4-4}
;|; frame (ahead). {4-4}
;|; The main loop: one turn a frame, when the HUD starts. {3-3}
;|; First what has a deadline at the top of the screen: the {3-3}
;|; camera, the ship and its sprites; then the screens' work, {3-3}
;|; the camera of the next turn; then, in the frame's lower {3-3}
;|; half, rows 0-9 of the next frame (ahead). {3-3}
;|; The main loop: one turn a frame, when the HUD starts. {2-2}
;|; First what has a deadline at the top of the screen: the {2-2}
;|; camera; then the screens' work, the camera of the next {2-2}
;|; turn; then, in the frame's lower half, rows 0-9 of the {2-2}
;|; next frame (ahead). {2-2}
;|; The main loop: one turn a frame, when the HUD starts {1-1}
;|; (frame_flag); the picture is still: the turn has no work. {1-1}
frame_loop:
        lda frame_flag
        beq frame_loop
        lda #0
        sta frame_flag
        lda frame_count         ; the frame of the turn {2}
        sta turn_count ; {2}
        jsr read_input          ; joystick 2, the keys {3}
joy_ready:                      ; the tests stop here
        lda prev_keys           ; keys pushed since the {7}
        eor #%11111111          ; last frame {7}
        and keys ; {7}
        sta new_keys ; {7}
        lda keys ; {7}
        sta prev_keys ; {7}
        lda held                ; the game held: the {16}
        beq +                   ; choice, the pause, GAME {16}
        jmp held_turn           ; OVER (states.asm) {16}
+       lda new_keys            ; SPACE: the pause, at this {16}
        and #KEY_SPACE          ; turn's end {16}
        beq + ; {16}
        lda #HELD_PAUSE ; {16}
        sta held ; {16}
+ ; {16}
        .if TEST_BUILD != 0      ; the test build only {3}
        lda test_keys           ; keys I and L: {3}
        ora test_prev           ; none now or before: no {3}
        beq +                   ; work (a few cycles) {3}
        jsr test_step ; {3}
+ ; {3}
        .fi ; {3}
        jsr move_camera ; {2}
        lda restart_flag ; {3}
        beq + ; {3}
        jsr next_level          ; the next level, from its {3}
        jsr restart_level       ; start, the ship in; {16}
;|        jsr restart_level       ; start, the ship in {3-15}
        lda ship_mode           ; a ship lost (the escape's {16}
        cmp #WAIT               ; time over): the next one {16}
        bne _again              ; chosen {16}
        jsr choose_lost ; {16}
        jmp _planned ; {16}
_again: ; {16}
        jsr ship_again ; {3}
_planned: ; {16}
        jsr camera_plan ; {3}
        inc turn_wait ; {3}
        jmp frame_ready ; {3}
+       lda swap_flag ; {3}
;|        lda swap_flag ; {2-2}
        beq + ; {2}
        jsr flip_front          ; the back screen in front {2}
+ ; {2}
        jsr update_ship         ; the ship, on its rock {3}
;|        jsr ship_sprites ; {3-3}
;|        lda enable              ; the ship's sprites on {3-3}
;|        sta $d015 ; {3-3}
;|        lda ship_bits           ; their ninth bits {3-3}
;|        sta $d010 ; {3-3}
        jsr plan_sprites        ; sprites before line 50 {4}
        jsr shots_rock          ; its shots and the rock {4}
        jsr sound_keys          ; F1-F7: the sound's mode {7}
        lda arena               ; the arena: no work of {2}
        beq +                   ; the screens {2}
        jsr boss_draw           ; the boss's body {8}
        jmp _plan ; {2}
+       lda swap_flag ; {2}
        beq _steps ; {2}
        jsr colour_bottom       ; the swap: rows 15-21 {2}
        jsr swap_back           ; the new column {2}
        jmp _far ; {2}
_steps: ; {2}
        lda speed + 1           ; under a pixel a frame, and {2}
        bne +                   ; the camera on to its next {2}
        lda cam_frac            ; pixel next frame (when the {2}
        clc                     ; stars move, in ahead): no {2}
        adc speed               ; step of the back screen {2}
        bcs _far                ; (there is time: 16 frames {2}
+       jsr prepare_back        ; a column, 8 of them still) {2}
_far: ; {2}
        lda far_flag            ; the far layer: a column on {2}
        beq + ; {2}
        jsr far_step ; {2}
+ ; {2}
_plan: ; {2}
        jsr camera_plan         ; the next turn's camera {2}
        jsr update_varkon       ; the Varkon for the next {4}
        jsr mux_ahead           ; frame; the objects' order {4}
        jsr update_hud ; {3}
frame_ready:                    ; the tests look here
        jsr music_play          ; the sound of the next {7}
        jsr sfx_play            ; frame, into the SID's copy {7}
sound_done:                     ; the tests look here {7}
        lda held                ; the game held from {16}
        bne +                   ; this turn: no rows 0-9 for {16}
        jsr ahead               ; the next frame (held_off) {16}
;|        jsr ahead               ; rows 0-9 of the next frame {2-15}
+ ; {16}
        lda turn_wait           ; after the level's start (a {3}
        beq +                   ; turn longer than a frame): {3}
        lda #0                  ; the next turn from a new {3}
        sta turn_wait           ; frame {3}
        sta frame_flag ; {3}
+ ; {3}
        jmp frame_loop

        .include "irq.asm"
        .include "vic.asm"
        .include "level.asm"
        .include "scroll.asm" ; {2}
        .include "stars.asm" ; {2}
        .include "ship.asm" ; {3}
        .include "mux.asm" ; {4}
        .include "hits.asm"     ; the hits {5}
        .include "phase.asm"    ; from the disk {10}
        .include "states.asm"   ; the game held {16}
        .include "data.asm"     ; (with core.asm in the {9}
                                ; HUD's hole) {9}
;|        .include "data.asm" ; {1-8}

        * = AUDIO               ; the sound, from $8000 {7}
;|        * = AUDIO               ; from $8000 {1-6}
        .include "player.asm" ; {7}
        .include "effects.asm" ; {7}
        .if RECORD_SFX != 0 ; {17}
        .include "reel.asm" ; {17}
        .fi ; {17}
        .include "../assets/generated/music.asm" ; {7}
        .include "../assets/generated/sfx.asm" ; {7}
audio_end: ; {7}
        .include "varkon.asm"   ; after the sound {7}
;|        .include "varkon.asm" ; {4-6}
        .include "weapons.asm" ; {4}
        .include "score.asm" ; {5}
        .include "fast.asm" ; {2}
        .include "boss.asm"     ; the boss {8}
        .include "beams.asm"    ; level 2's beams {9}
        .include "sphere.asm"   ; the SHIELD CORE's sphere {9}
                                ; (its cosines in the {9}
                                ; store's tail: levels.inc) {9}
        .include "choice.asm"   ; the ship's choice {16}
        .include "../assets/generated/varkon.inc" ; {4}
        .include "../assets/generated/boss.inc" ; {8}
;{17}
        .if RECORD_LEVEL != 0
; Only to record the station's theme: the rest of game_start
; (title.asm) here, the level's file first: it writes over
; the title's module, where game_start is; last before the
; alignment, so that nothing the files write to moves.
rec_level:
        jsr file_need           ; its file from the disk
        jsr init_level          ; with no Varkon, no objects
        lda #START_X            ; then the ship (init_ship's
        ldx #0                  ; come_in), as game_start
        ldy #CONTROL            ; has it
        jsr come_in
        jsr plan_sprites
        jsr update_hud
        jsr camera_plan         ; the first turn's camera
        lda sound_mode          ; the music from its start
        jsr sound_set
        lda #0
        sta frame_count
        sta frame_flag
        sta turn_wait
        jsr init_irq            ; the interrupts on
        jsr screen_on
        jmp frame_loop
        .fi
;{}
        .align 256              ; rock_at's table, made {3}
;|        .align 256 ; {1-2}
rock_lines:                     ; at each level start {3}
;|rock_lines: ; {1-2}
stage_1:                        ; the store's 2nd piece
        .binary "../assets/generated/store1.bin"
        .fill 8 * 256 - STAGE_LEN_1
LEVEL_W2:                       ; the level's maps
stage_2:                        ; and the store's 3rd piece
        .binary "../assets/generated/store2.bin"
music_from:                     ; the songs of {7}
        .logical MUSIC_AT       ; phase 1's store (music.py: {7}
        .include "../assets/generated/music_store.asm" ; {7}
        .here                   ; STORE_SONGS), to MUSIC_AT {7}
MUSIC_LEN = * - music_from ; {7}
        .cerror MUSIC_AT < STORE + STORE_SIZE, "MUSIC_AT" ; {7}
        .cerror MUSIC_AT + MUSIC_LEN > TITLE_AT, "MUSIC_AT" ; {7}
high_end:
        .cerror LEVEL_W2 + LEVEL_W2_SIZE > $d000, "LEVEL_W2"
        .cerror * > $d000, "the code reaches the I/O"
        .cerror STORE + STORE_SIZE > $fffa, "the store"
