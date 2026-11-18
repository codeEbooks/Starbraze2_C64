; ---------------------------------------------------------
; The game held (the choice of the ship, the pause, GAME
; OVER) and the way to the title
; ---------------------------------------------------------

; The author, 4 November: the ship chosen «All'inizio e a
; ogni vita (Consigliato)»: at the start of a game and
; after each ship lost (the escape's time over too); no
; change in flight (the keys 1-3 are gone). How:
; the game held, the ship at its place blinking, its name
; and its pilot in row 1 of the HUD (its SCORE, HI and the
; level's name kept meanwhile), row 2 with its full shield
; and the weapon's level; Left and Right another ship,
; Fire: at the start of a game it flies from its place
; (START_X, ENTER_Y), after a ship lost it comes in from the
; left to its place (ENTER_TO), blinking.
; SPACE: the pause, PAUSED in row 1, SPACE again. No ships
; left: GAME OVER in row 1 for OVER_FRAMES frames, then the
; title (the record stays).
;
; The game is held from the end of a turn (the main loop:
; its rows 0-9 for the next frame not made, ahead), so that
; the frame shown stays as it is; the turns held
; (held_turn, from the main loop's joy_ready): the frame's
; picture again (the ship, the plan of the sprites made
; last: first_sprites, the interrupts write the rest),
; nothing else moves; the SID's volume 0 (kept in held_vol,
; given back). The game on again (held_off): first the rows
; of the turn held from (ahead). So the camera, the Varkon,
; the shots, the screens and the sound go on afterwards as
; if the turns held were not there.

HELD_CHOOSE = 1                 ; held: the choice, to begin
HELD_SHIP   = 2                 ; the choice
HELD_PAUSE  = 3                 ; the pause, to begin
HELD_PAUSED = 4                 ; the pause
HELD_OVER   = 5                 ; GAME OVER, to begin
HELD_END    = 6                 ; GAME OVER, its wait
OVER_FRAMES = 150               ; three seconds
KEY_SPACE   = %00000001         ; keys: bit 0 (read_input)
HUD_ROW1    = HUD_CELL + 40     ; row 1 of the HUD

held_turn:
        jsr held_picture
        lda joy_prev            ; Y: the joystick just
        eor #%11111111          ; pushed
        and joy
        tay
        lda joy
        sta joy_prev
        lda held
        cmp #HELD_OVER
        bcs _over
        cmp #HELD_PAUSE
        bcs _pause
        cmp #HELD_SHIP
        beq _choose
        jsr held_begin          ; the choice begins
        inc held
        bne _shown              ; (always)
_choose:
        tya
        and #JOY_FIRE
        bne _go
        tya
        and #JOY_LEFT | JOY_RIGHT
        beq _blink
        ldx ship_type           ; another ship
        and #JOY_RIGHT
        beq _left
        inx
        cpx #SHIP_COUNT
        bcc _type
        ldx #0
        beq _type
_left:
        dex
        bpl _type
        ldx #SHIP_COUNT - 1
_type:
        stx ship_type
_shown:
        jsr ship_shown
_blink:
        lda frame_count         ; blinking: 8 frames on, 8
        lsr a                   ; off (ship_sprites: bit 2)
        sta ship_blink
        jmp frame_loop
_go:
        lda held_time           ; a ship lost: it comes in
        beq _here               ; from the left, blinking
        lda #ENTER_X
        ldx #$ff
        ldy #ENTER
        jsr come_in
        jmp held_off
_here:
        lda #CONTROL            ; the start: it flies from
        sta ship_mode           ; its place
        lda #ENTER_BLINK
        sta ship_blink
        bne held_off            ; (always)
_pause:
        bne _paused
        jsr held_begin          ; the pause begins
        ldx #MSG_PAUSE
        jsr hud_say
        inc held
        bne _wait               ; (always)
_paused:
        lda new_keys            ; SPACE again: on
        and #KEY_SPACE
        bne held_off
        jmp frame_loop
_over:
        cmp #HELD_END
        beq _end
        jsr held_begin          ; GAME OVER begins
        lda held_vol            ; its jingle: the {17}
        sta sid_shadow + 24     ; volume again, the song {17}
        lda #SONG_OVER ; {17}
        jsr song_start ; {17}
        ldx #MSG_OVER
        jsr hud_say
        lda #OVER_FRAMES
        sta held_time
        inc held
        bne _wait               ; (always)
_end:
        jsr music_play          ; the jingle plays {17}
        dec held_time
        bne _wait
        jmp title_return
_wait:
        jmp frame_loop

; The game on again: row 1 of the HUD as it was, the sound;
; the rows of the turn held from (ahead: behind the beam of
; the next frame, as at a turn's end).
held_off:
        ldx #39
-       lda hud_keep,x
        sta SCREEN_A + HUD_ROW1,x
        lda hud_keep_c,x
        sta COLOURS + HUD_ROW1,x
        dex
        bpl -
        lda held_vol
        sta sid_shadow + 24
        lda #0
        sta held
held_on:                        ; the tests look here
        jsr ahead
        jmp frame_loop

; The frame's picture again: the ship's sprites (in the
; choice, the ship chosen), the plan's first six, the plan
; for the interrupts (mux_ready, as plan_sprites).
held_picture:
        jsr ship_sprites
        jsr first_sprites
        lda #HARDWARE
        sta mux_next
        lda #1
        sta mux_ready
held_shown:                     ; the tests look here
        rts

; The game held from now: the sound's volume kept, then 0;
; row 1 of the HUD kept, then blank.
held_begin:
        lda sid_shadow + 24
        sta held_vol
        and #%11110000
        sta sid_shadow + 24
        lda joy                 ; what is pushed now is not
        sta joy_prev            ; pushed again
        ldx #39
-       lda SCREEN_A + HUD_ROW1,x
        sta hud_keep,x
        lda COLOURS + HUD_ROW1,x
        sta hud_keep_c,x
        dex
        bpl -
        rts

; GAME OVER, the victory: the title, with phase 1's file in
; the store (from the disk if it is not there). The record
; stays (score.asm).
title_return:
        lda #0
        sta held
        sta level
        jsr screen_off
        jsr sprites_all_off
        jsr file_need
        jmp title

; (The choice's routines, the messages: choice.asm, in the
; program's high part.)
