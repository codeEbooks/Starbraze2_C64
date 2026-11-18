; STARBRAZE II, step 14 of 17: the SUPER-COMPUTER VARKON.
; PAL C64 with a 1541. Assemble this file: it includes the
; others.
;
; Level 1, THE CANYONS of Varkonia Prime:
;  - It scrolls from right to left at the speeds of the
;    level, with the far mesas at half speed and the stars
;    in three planes, to the arena at its end.
;  - The ship flies in it (joystick 2, Fire) and meets its
;    rock.
;  - The level's script brings its Varkon: raiders, drones,
;    lancers, leapers on the rock, the flak turrets of the
;    mesas, the carriers in gold; up to 24 objects on
;    sprites 2-7, the multiplexer puts them down the screen.
;  - The ship's shots destroy them, their plasma and their
;    bodies cost the ship its shield; the score.
;  - Each ship's weapon has four levels; the carriers leave
;    their capsules: W the weapon, S speed, M the missile, O
;    the satellite, E the shield.
;  - The theme of the level plays on the SID; F1, F3, F5, F7
;    choose the sound: MUSIC, MUSIC + FX, SOUND FX, SILENT.
;  - In the arena, its boss: the SIEGE CRAWLER (boss.asm);
;    STAGE CLEAR, then the next level.
;
; Level 2, SHIELD GENERATORS, in deep space: towers with
; their fields (varkon.asm), beams (beams.asm), clouds that
; are not rock; its boss, the SHIELD CORE (core.asm,
; sphere.asm), on the boss engine made common (boss.asm).
;
; Level 3, GRAVEYARD OF HELIOS: the scouts, the gunships and
; their fans, the mines, the rocks and their shards
; (varkon.asm, hits.asm), the alien's spines (beams.asm),
; the theme of space (player.asm); its boss, the GRAVEYARD
; WARDEN (warden.asm, assembled by itself, its code from the
; disk).
;
; Level 4, THE BLOODY ORBIT: the heavy lancers, the gold
; scouts, the station's hull and its turrets; its boss, the
; VARKON CORVETTE (corvette.asm).
;
; Level 5, VARKON-OMEGA, the station: its crawlers, laser
; mines and turrets on the ceiling, its theme (station.asm);
; its boss, the DEFENSE TURRET ARRAY (defense.asm).
;
; Level 6, THE CORE: guardians, eggs, barriers and their
; energy (station.asm); its boss, the SUPER-COMPUTER VARKON
; (supercomp.asm).
;
; The game is on a disk: the PRG brings phase 1 (the planet:
; levels 1 and 2); the file of a level from 3 on (LEVEL3 to
; LEVEL6) is read with the KERNAL's routines when the level
; starts (phase.asm, the loading screen phase_show.asm).
;
; With -D TEST_BUILD=1 the test build: the keys I and L for
; the tests by hand (ship.asm, test_step): I, the ship that
; cannot be hurt; L, the next level at once. The game on the
; disk is without them (the author, 11 November: «Via dal
; disco, restano in una build di prova»).
        .cpu "6502"
        .weak
TEST_BUILD = 0                  ; 0: the game on the disk
        .endweak
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
        lda $ba                 ; the drive it came
        cmp #8                  ; from: the phases' too (8
        bcs +                   ; when not from a drive)
        lda #8
+       sta disk_dev
        lda #1                  ; file 1's store (phase 1):
        sta file_now            ; the PRG brings it
        jsr kernal_out          ; BASIC and KERNAL out
        jsr move_store          ; the packed levels,
                                ; title.asm's module
        jsr sound_init          ; the SID's copy, silent
        jsr score_init          ; 0, the best 0
        jmp game_start

; The main loop: one turn a frame, when the HUD starts.
; First what has a deadline at the top of the screen: the
; camera, the ship and the sprites; then the screens' work,
; the camera of the next turn, the Varkon of the next frame
; (with the hits); then, in the frame's lower half, rows 0-9
; of the next frame (ahead).
frame_loop:
        lda frame_flag
        beq frame_loop
        lda #0
        sta frame_flag
        lda frame_count         ; the frame of the turn
        sta turn_count
        jsr read_input          ; joystick 2, the keys
joy_ready:                      ; the tests stop here
        lda prev_keys           ; keys pushed since the
        eor #%11111111          ; last frame
        and keys
        sta new_keys
        lda keys
        sta prev_keys
        .if TEST_BUILD != 0      ; the test build only
        lda test_keys           ; keys I and L:
        ora test_prev           ; none now or before: no
        beq +                   ; work (a few cycles)
        jsr test_step
+
        .fi
        jsr move_camera
        lda restart_flag
        beq +
        jsr next_level          ; the next level, from its
        jsr restart_level       ; start, the ship in
        jsr ship_again
        jsr camera_plan
        inc turn_wait
        jmp frame_ready
+       lda swap_flag
        beq +
        jsr flip_front          ; the back screen in front
+
        jsr update_ship         ; the ship, on its rock
        jsr plan_sprites        ; sprites before line 50
        jsr shots_rock          ; its shots and the rock
        jsr sound_keys          ; F1-F7: the sound's mode
        lda arena               ; the arena: no work of
        beq +                   ; the screens
        jsr boss_draw           ; the boss's body
        jmp _plan
+       lda swap_flag
        beq _steps
        jsr colour_bottom       ; the swap: rows 15-21
        jsr swap_back           ; the new column
        jmp _far
_steps:
        lda speed + 1           ; under a pixel a frame, and
        bne +                   ; the camera on to its next
        lda cam_frac            ; pixel next frame (when the
        clc                     ; stars move, in ahead): no
        adc speed               ; step of the back screen
        bcs _far                ; (there is time: 16 frames
+       jsr prepare_back        ; a column, 8 of them still)
_far:
        lda far_flag            ; the far layer: a column on
        beq +
        jsr far_step
+
_plan:
        jsr camera_plan         ; the next turn's camera
        jsr update_varkon       ; the Varkon for the next
        jsr mux_ahead           ; frame; the objects' order
        jsr update_hud
frame_ready:                    ; the tests look here
        jsr music_play          ; the sound of the next
        jsr sfx_play            ; frame, into the SID's copy
sound_done:                     ; the tests look here
        jsr ahead               ; rows 0-9 of the next frame
        lda turn_wait           ; after the level's start (a
        beq +                   ; turn longer than a frame):
        lda #0                  ; the next turn from a new
        sta turn_wait           ; frame
        sta frame_flag
+
        jmp frame_loop

        .include "irq.asm"
        .include "vic.asm"
        .include "level.asm"
        .include "scroll.asm"
        .include "stars.asm"
        .include "ship.asm"
        .include "mux.asm"
        .include "hits.asm"     ; the hits
        .include "phase.asm"    ; from the disk
        .include "data.asm"     ; (with core.asm in the
                                ; HUD's hole)

        * = AUDIO               ; the sound, from $8000
        .include "player.asm"
        .include "effects.asm"
        .include "../assets/generated/music.asm"
        .include "../assets/generated/sfx.asm"
audio_end:
        .include "varkon.asm"   ; after the sound
        .include "weapons.asm"
        .include "score.asm"
        .include "fast.asm"
        .include "boss.asm"     ; the boss
        .include "beams.asm"    ; level 2's beams
        .include "sphere.asm"   ; the SHIELD CORE's sphere
                                ; (its cosines in the
                                ; store's tail: levels.inc)
        .include "../assets/generated/varkon.inc"
        .include "../assets/generated/boss.inc"
        .align 256              ; rock_at's table, made
rock_lines:                     ; at each level start
stage_1:                        ; the store's 2nd piece
        .binary "../assets/generated/store1.bin"
        .fill 8 * 256 - STAGE_LEN_1
LEVEL_W2:                       ; the level's maps
stage_2:                        ; and the store's 3rd piece
        .binary "../assets/generated/store2.bin"
music_from:                     ; the songs of
        .logical MUSIC_AT       ; phase 1's store (music.py:
        .include "../assets/generated/music_store.asm"
        .here                   ; STORE_SONGS), to MUSIC_AT
MUSIC_LEN = * - music_from
        .cerror MUSIC_AT < STORE + STORE_SIZE, "MUSIC_AT"
        .cerror MUSIC_AT + MUSIC_LEN > TITLE_AT, "MUSIC_AT"
high_end:
        .cerror LEVEL_W2 + LEVEL_W2_SIZE > $d000, "LEVEL_W2"
        .cerror * > $d000, "the code reaches the I/O"
        .cerror STORE + STORE_SIZE > $fffa, "the store"
