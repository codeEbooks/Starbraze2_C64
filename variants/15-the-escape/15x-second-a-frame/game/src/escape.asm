; The escape: the seventh level's own
; code (escape.py), after the SUPER-COMPUTER VARKON, in
; level 6's file (the author, 31 October: «Nel file del
; livello 6 (Consigliato)»).
;
; Assembled by itself at ES_AT (the SUPER-COMPUTER's data's
; place, SC_AT: after him nothing there is needed), with the
; program's labels (game/build/main.inc). Level 6's file
; brings it packed in the store (ES_PACK; make_disk.py:
; ES_PIECES pieces of ES_PIECE bytes); the station's module
; unpacks it a piece a frame at the escape's start
; (station.asm, es_beams), then comes here every frame
; through ES_STEP (the engine's beam_step: beam_module 2),
; and through ES_PART for a Varkon of the behaviour FALL.
;
; «Crolli e pochi Varkon (Consigliato)»: the time is the
; real enemy. A scroll that never stops would never run out
; of time: here it goes a pixel a frame while the ship flies
; in the screen's right half (ES_FAST_X), half a pixel
; otherwise (the escape's single speed, rewritten every
; frame; the two the engine scrolls well). Its
; steps (es_state):
;  - START (the level's first frame here): TIME 60 in the
;    HUD where VARKONIA is, the falling pieces' pictures
;    into the egg's blocks (the escape has none);
;  - IN: the countdown, a second every 50 frames; the time
;    over with the ship flying: it explodes (a ship less;
;    key I: none), and when it has, the escape again from
;    its start (no ships left: three more); the way out (the
;    camera at ES_OUT): OUT;
;  - OUT: the time stops; a pixel a frame; behind the ship
;    the station blows up (ES_BOOMS fireballs on its last
;    plates, the screen white at the end); the camera stops
;    at ES_STOP, the ship flies off: END;
;  - END: the victory: rows 0-21 of screen A in the HUD's
;    characters (its texts: escape.py, VICTORY), the time
;    left and the shield into the score (TIME BONUS, SHIELD
;    BONUS: 1 000 a second, 1 000 a notch, counted down on
;    the screen); then, ES_END_WAIT frames later or with
;    Fire, the game again from level 1, the score, the ships
;    and the weapons kept.
; Its variables in page 2, in the SHIELD CORE's place for
; the arena's cells (cb_save): 0 at each level's start
; (boss_reset).

        .include "main.inc"     ; (-I its build)
        .include "../assets/generated/escape.inc"

TIME_AT  = SCREEN_A + HUD_CELL + HUD_BAR + ES_TIME_DIGITS
ST_START = 0
ST_IN    = 1
ST_OUT   = 2
ST_END   = 3
ES_QUARTERS = 4                 ; END: rows 0-21 blank in
                                ; four turns

es_state = cb_save              ; ST_*
es_frames = cb_save + 1         ; frames of the second
es_secs  = cb_save + 2          ; seconds left
es_dead  = cb_save + 3          ; 1: the time over
es_timer = cb_save + 4          ; frames (OUT, END)
es_k     = cb_save + 5          ; fireballs made; END's
                                ; count's step
es_left  = cb_save + 6          ; seconds still to count
es_shown = cb_save + 7          ; END: the screen's turns
                                ; done (blank 1-4, texts 5)
        .cerror es_shown >= CB_SAVE_END, "cb_save"

        * = ES_AT
        jmp escape_step             ; ES_STEP
        .cerror * != ES_PART, "ES_PART"
        jmp escape_part             ; ES_PART

; Every frame of the escape (the station's module, from
; the engine's beam_step, after the engine's beams: the
; stretches that close): the step's routine.
escape_step:
        ldx es_state
        lda steps_lo,x
        sta vector
        lda steps_hi,x
        sta vector + 1
        jmp (vector)

steps_lo:
        .byte <step_start, <step_in, <step_out, <step_end
steps_hi:
        .byte >step_start, >step_in, >step_out, >step_end

; --- START ------------------------------------------------
step_start:
        ldx #ES_TIME_CELLS - 1  ; TIME and its colour where
-       lda es_time_text,x      ; VARKONIA is
        sta SCREEN_A + HUD_CELL + HUD_BAR,x
        lda #ES_TIME_COLOUR
        sta COLOURS + HUD_CELL + HUD_BAR,x
        dex
        bpl -
        ldx #ES_RUBBLE_BYTES - 1 ; the pieces' pictures
-       lda es_rubble,x
        sta ES_RUBBLE_AT,x
        dex
        bpl -
        lda #ES_SECONDS
        sta es_secs
        lda #0
        sta es_frames
        jsr time_digits
        lda #ST_IN
        sta es_state
        jmp slow

; --- IN ---------------------------------------------------
step_in:
        lda es_dead             ; the time over: once the
        beq _flying             ; ship has exploded
        lda ship_mode
        cmp #WAIT
        bne _done
        lda ship_lives          ; no ships left: three
        bne _again              ; more
        lda #LIVES
        sta ship_lives
        sta hud_dirty           ; the HUD's ships
_again:
        lda #ES_LEVEL - 1       ; the escape from its start
        sta level               ; (next_level: + 1)
        lda #1
        sta restart_flag
_done:
        rts
_flying:
        lda camera              ; the way out?
        cmp #<ES_OUT
        lda camera + 1
        sbc #>ES_OUT
        bcc +
        lda es_secs             ; OUT: the time stops
        sta es_left
        lda #0
        sta es_timer
        sta es_k
        lda #ST_OUT
        sta es_state
        jmp fast
+       inc es_frames           ; the countdown
        lda es_frames
        cmp #1
        bcc _speed
        lda #0
        sta es_frames
        dec es_secs
        jsr time_digits
        lda es_secs
        bne _speed
        lda invuln              ; the time over: key I, the
        bne _again              ; escape again at once
        lda ship_mode
        cmp #EXPLODE            ; down already: when it has
        beq _down               ; exploded
        cmp #WAIT
        beq _down
        cmp #CONTROL            ; coming in: again at once
        bne _again
        sta ship_blink          ; flying: it explodes (a
        lda #ES_ALL_NOTCHES     ; ship less)
        jsr hurt
_down:
        lda #1
        sta es_dead
        rts
_speed:
        lda ship_mode           ; the ship flying in the
        bne slow                ; right half: a pixel a
        lda ship_xh             ; frame
        bne fast
        lda ship_x
        cmp #ES_FAST_X
        bcs fast
slow:
        lda #<ES_SLOW
        ldx #>ES_SLOW
        jmp +
fast:
        lda #<ES_FAST
        ldx #>ES_FAST
+       sta speed_lo            ; the escape's only speed
        stx speed_hi
        rts

; The seconds left (two digits) into the HUD.
time_digits:
        lda es_secs
        ldx #0
-       cmp #10
        bcc +
        sbc #10
        inx
        bne -
+       clc
        adc #DIGIT_CODE
        sta TIME_AT + 1
        txa
        clc
        adc #DIGIT_CODE
        sta TIME_AT
        rts

; --- OUT --------------------------------------------------
step_out:
        lda camera              ; the camera stops there
        cmp #<ES_STOP
        lda camera + 1
        sbc #>ES_STOP
        bcc +
        lda #0
        sta speed_lo
        sta speed_hi
+       lda es_k                ; the fireballs, then the
        cmp #ES_BOOMS           ; ship flies off
        bcc +
        jmp _leave
+
        inc es_timer
        lda es_timer
        cmp #ES_BOOM_EVERY
        bcc _done
        lda #0
        sta es_timer
        jsr free_varkon         ; a fireball on the
        bcs _sound              ; station's last plates
        lda #2                  ; (none free: none)
        jsr set_pri
        lda #BOOM
        sta en_on,x
        lda #KIND_CORE
        sta en_kind,x
        lda #BOSS               ; (still on the screen)
        sta en_beh,x
        lda #0
        sta en_left,x
        sta en_flash,x
        sta en_cap,x
        sta en_xf,x
        lda es_k
        and #%00000111
        tay
        lda es_boom_y,y
        sta en_y,x
        lda #<(ES_HULL + 24)    ; x register: the hull's end
        sec                     ; on the screen, less a bit
        sbc camera
        sta v_tmp
        lda #>(ES_HULL + 24)
        sbc camera + 1
        sta v_tmp + 1
        lda v_tmp
        sec
        sbc es_boom_dx,y
        sta en_x,x
        lda v_tmp + 1
        sbc #0
        sta en_xh,x
        bpl +                   ; off the left edge: at it
        lda #24
        sta en_x,x
        lda #0
        sta en_xh,x
+
_sound:
        lda #FX_EXPLODE
        jsr sfx_start
        inc es_k
        lda es_k
        cmp #ES_BOOMS
        bne _done
        lda #ES_WHITE           ; the last: the screen white
        sta top_d021            ; (the HUD's interrupt
                                ; writes it at line 227:
                                ; from the frame after next)
        lda #ES_FLASH
        sta es_timer
_done:
        rts
_leave:
        lda es_timer            ; the white, a few frames
        beq +
        dec es_timer
        bne +
        lda level_d021
        sta top_d021
+       lda ship_mode           ; the ship flies off
        beq +
        cmp #ENTER
        bne ++
+       lda #LEAVE
        sta ship_mode
        lda #0
        sta ship_blink
+       cmp #GONE               ; gone, the camera still,
        bne _done               ; the back screen made: END
        lda speed_lo
        ora speed_hi
        bne _done
        lda prep_stage
        cmp #READY
        bne _done
        lda #0
        sta es_timer
        sta es_k
        sta es_shown
        lda #ST_END
        sta es_state
        rts

; --- END --------------------------------------------------
step_end:
        lda es_shown            ; first the screen: rows
        cmp #ES_QUARTERS + 1    ; 0-21 blank, a quarter a
        bcs _count              ; turn (a turn each: the
        inc es_shown            ; frame's time), then its
        cmp #ES_QUARTERS        ; texts
        bcs +
        jmp blank
+       jmp victory
_count:
        inc es_k                ; a step of the count every
        lda es_k                ; ES_COUNT_EVERY frames
        cmp #ES_COUNT_EVERY
        bcc _wait
        lda #0
        sta es_k
        lda es_left             ; the time left: a second
        beq _shield             ; into the score
        dec es_left
        jsr bonus
        jmp counts
_shield:
        lda shield              ; then the shield: a notch
        beq _wait
        dec shield
        lda #1
        sta hud_dirty
        jsr bonus
        jmp counts
_wait:
        lda es_left             ; counted: the end's wait,
        ora shield              ; or Fire
        bne _done
        inc es_timer
        lda es_timer
        cmp #ES_FIRE_AFTER
        bcc _done
        lda joy
        and #JOY_FIRE
        bne new_game
        lda es_timer
        cmp #ES_END_WAIT
        bcs new_game
_done:
        rts

; After the victory, Fire: the game again from level 1,
; the score, the ships and the weapons kept.
new_game:
        lda #$ff                ; (next_level: + 1, level 1)
        sta level
        lda #1
        sta restart_flag
        rts

bonus:
        ldy #KIND_NOTCH         ; 1 000 points
        jsr score_add
        lda #FX_CAPSULE
        jmp sfx_start

; The two counts on the screen: the seconds left, the
; notches.
counts:
        lda es_left
        ldx #0
-       cmp #10
        bcc +
        sbc #10
        inx
        bne -
+       clc
        adc #DIGIT_CODE
        sta SCREEN_A + ES_TIME_CELL + 1
        txa
        clc
        adc #DIGIT_CODE
        sta SCREEN_A + ES_TIME_CELL
        lda shield
        clc
        adc #DIGIT_CODE
        sta SCREEN_A + ES_SHIELD_CELL
        rts

; A quarter of rows 0-21 of screen A blank (A: 0-3): code 0
; (blank in both character sets), colour 0.
ES_QUARTER = 22 * 40 / ES_QUARTERS
blank:
        tax
        lda quarters_lo,x
        sta dst
        sta src
        lda quarters_hi,x
        sta dst + 1
        clc
        adc #>(COLOURS - SCREEN_A)
        sta src + 1
        ldy #ES_QUARTER - 1
        lda #0
-       sta (dst),y
        sta (src),y
        dey
        cpy #$ff
        bne -
        rts

quarters_lo:
        .byte <(SCREEN_A + range(ES_QUARTERS) * ES_QUARTER)
quarters_hi:
        .byte >(SCREEN_A + range(ES_QUARTERS) * ES_QUARTER)
        .cerror ES_QUARTER * ES_QUARTERS != 22 * 40
        .cerror ES_QUARTER > 256

; The victory's screen, rows 0-21 blank: its texts and their
; colours; then screen A in the HUD's characters (rows 10-13
; keep the far layer's: blank).
victory:
        ldy #0                  ; the texts: place (2),
_text:                          ; colour, count, codes; 0
                                ; the end
        lda es_texts,y
        sta dst
        iny
        lda es_texts,y
        beq _shown
        sta dst + 1
        iny
        lda es_texts,y
        sta v_tmp               ; its colour
        iny
        lda es_texts,y
        sta v_tmp + 1           ; its count
        iny
        sty count
        lda dst + 1             ; the colour's place
        clc
        adc #>(COLOURS - SCREEN_A)
        sta src + 1
        lda dst
        sta src
        ldy #0
-       sty temp
        ldy count
        lda es_texts,y
        inc count
        ldy temp
        sta (dst),y
        lda v_tmp
        sta (src),y
        iny
        cpy v_tmp + 1
        bne -
        ldy count
        jmp _text
_shown:
        jsr counts
        lda #HUD_D018           ; screen A, the HUD's set
        sta shown_d018
        rts

; --- FALL -------------------------------------------------
; A falling piece (X, its object Y): down FALL_VY a frame
; (with the rock: the program moves it); at FALL_END it
; breaks, a fireball, no points; its picture by the frame.
escape_part:
        clc
        lda en_yf,x
        adc #<FALL_VY
        sta en_yf,x
        lda en_y,x
        adc #>FALL_VY
        sta en_y,x
        cmp #FALL_END
        bcc +
        lda #BOOM
        sta en_on,x
        lda #0
        sta en_left,x
        sta en_flash,x
        sta en_cap,x
+       lda anim3               ; its picture by the frame
        and en_pmask,x
        clc
        adc en_block,x
        sta obj_block,y
        rts

        .include "../assets/generated/escape_data.inc"

ESCAPE_END:
        .cerror ESCAPE_END > ES_AT + ES_PIECES * ES_PIECE
        .cerror ESCAPE_END > WARDEN_AT, "the escape: long"
