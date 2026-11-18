; The boss engine, common to the levels' bosses (level_boss:
; 1 the SIEGE CRAWLER, the boss of level 1,
; game/assets/crawler.py; 2 the SHIELD CORE, core.asm; 3 the
; GRAVEYARD WARDEN, warden.asm, assembled by itself and
; brought by level 3's file, LEVEL3; 4 the VARKON CORVETTE,
; corvette.asm, brought by LEVEL4: from 3 on, their body,
; their steps and their colours through the jumps W_DRAW,
; W_STEP, W_PAINT, at the start of the code the level's file
; has brought at WARDEN_AT): WAIT, the chain, the wreck,
; STAGE CLEAR and the bar are the engine's; a boss has its
; start, its steps 1-4 (b_steps, nine a boss), its parts'
; places, pictures and colours. Below, the SIEGE CRAWLER's.
;
; At the level's end the camera stops (camera_plan): the
; arena. The screen does not scroll any more, and the frame
; has time for the boss. Its body is characters on rows
; 15-18, on the floor: rock that moves, so that it pushes
; the ship and stops its shots by the rock's own rules
; (rock_at reads the characters themselves in the arena).
; It moves by multicolour pixels: its columns come shifted
; by 0-3 pixels (body_data, by phase) into one of two sets
; of characters, the one the screen does not show, in two
; turns (columns 0-7, then 8-14); then the screen's cells
; take that set (the flip). Its parts are Varkon of the
; multiplexer (behaviour BOSS): the two cannons on its back,
; then the core; the program puts them on the body each
; frame, they are hit as the Varkon are.
;
; Its steps (boss_state), one after the other:
;  - WAIT: no Varkon flying or exploding for ARENA_WAIT
;    frames; then the cannons take two free Varkon, the bar
;    comes into the HUD;
;  - ENTER: the body comes in from the right to its station;
;  - FIGHT: it patrols, the cannons fire their fans (three
;    shots by their aim), the mouth launches drones; both
;    cannons destroyed, the hatch opens;
;  - OPEN: the core rises from the hatch (it can be hit);
;  - CORE: it patrols faster, more drones, the core fires;
;    the core destroyed, everything else explodes;
;  - CHAIN: CHAIN_COUNT explosions on the body, the hull
;    white at each;
;  - WRECK: the hull goes dark;
;  - CLEAR: STAGE CLEAR; the ship flies off to the right,
;    the shield's notches go into the score; then the next
;    level (restart_flag), with the score, the ships and
;    the weapons.

ST_WAIT  = 0
ST_ENTER = 1
ST_FIGHT = 2
ST_OPEN  = 3
ST_CORE  = 4
ST_CHAIN = 5
ST_WRECK = 6
ST_CLEAR = 7
ST_DONE  = 8
ST_RAGE  = 3                    ; the SHIELD CORE's
BOSS    = 3                     ; the parts' behaviour

        .cerror (CAMERA_END / 8) % 2 != 0, "arena: screen A"

; At the level's start (init_level): no arena, no boss (its
; variables 0, its parts none; rows 10-14 never rock, as the
; GRAVEYARD WARDEN may have left them); VARKONIA in the HUD.
; (The characters the boss has used come back with the
; level's: load_level unpacks them all.)
boss_reset:
        ldx #BOSS_END - arena - 1
        lda #0
-       sta arena,x
        dex
        bpl -
        ldx #CB_SAVE_END - arena_chars - 1
-       sta arena_chars,x       ; arena_chars to CB_SAVE_END
        dex
        bpl -
        sta air_rock            ; the WARDEN's: rows
        lda #$ff                ; 10-14 no rock again
        ldx #CORRIDOR_TO - CORRIDOR_FROM - 1
-       sta rock_row + CORRIDOR_FROM,x
        dex
        bpl -
        sta part_a              ; its parts none
        sta part_b
        sta part_core
        ldx #BAR_CELLS - 1      ; VARKONIA in the HUD
-       lda hud_rows + HUD_BAR,x
        sta SCREEN_A + HUD_CELL + HUD_BAR,x
        lda hud_rows + 120 + HUD_BAR,x
        sta COLOURS + HUD_CELL + HUD_BAR,x
        dex
        bpl -
        rts

; ---------------------------------------------------------
; The body on the screen: in the arena's turns, after the
; sprites (main loop). Columns 0-7 of the other set, or
; columns 8-14 and the flip.
; (The SHIELD CORE's sphere: core.asm; a boss from 3 on, its
; own: W_DRAW.)
; ---------------------------------------------------------

boss_draw:
        lda level_boss
        cmp #3                  ; from 3 on: its own
        bcc +
        jmp W_DRAW
+       cmp #2                  ; the SHIELD CORE's
        bne +                   ; sphere
        jmp sphere_draw
+       lda boss_state          ; WAIT: no body yet
        beq _done
        lda prep_step           ; half made: the rest
        bne _second
        lda body_x              ; nothing to make: the
        cmp shown_x             ; body is where it is
        bne +                   ; shown
        lda body_var
        cmp shown_var
        beq _done
+       lda body_x              ; the other set for where
        sta prep_x              ; the body is now
        lda body_var
        sta prep_var
        ldx #0
        jsr copy_run
        ldx #1
        jsr copy_run
        inc prep_step
_done:
        rts
_second:
        ldx #2
        jsr copy_run
        ldx #3
        jsr copy_run
        ldx #4
        jsr copy_run
        lda #0
        sta prep_step
        jmp flip

; Run X of the body's columns (RUNS of them: the mouth's,
; the rest of 0-7, the hatch's, 11, 12-14) for prep_x and
; prep_var into the set the screen does not show: from the
; phase's columns (run 0 the mouth's, if it is open; run 2
; the hatch's), run_bytes of them, four a loop; the loop's
; addresses are written into it.
copy_run:
        stx b_tmp + 1           ; the run
        lda prep_x              ; the phase
        and #%00000011
        sta b_tmp
        tay
        cpx #0                  ; run 0: the mouth's?
        bne +
        lda prep_var
        and #%00000001
        beq _base
        lda mouth_src_lo,y
        ldx mouth_src_hi,y
        jmp _from
+       cpx #2                  ; run 2: the hatch's?
        bne _base
        lda prep_var
        and #%00000010
        beq _base
        lda hatch_src_lo,y
        ldx hatch_src_hi,y
        jmp _from
_base:
        tya                     ; phase * RUNS + run
        asl a
        asl a
        adc b_tmp
        adc b_tmp + 1
        tay
        lda run_src_lo,y
        ldx run_src_hi,y
_from:
        sta cp_s0 + 1
        sta cp_s1 + 1
        sta cp_s2 + 1
        sta cp_s3 + 1
        stx cp_s0 + 2
        stx cp_s1 + 2
        stx cp_s2 + 2
        stx cp_s3 + 2
        lda shown_set           ; to the other set: its
        beq +                   ; runs, RUNS from set 1's
        lda #0
        beq ++
+       lda #RUNS
+       clc
        adc b_tmp + 1
        tay
        lda run_dst_lo,y
        sta cp_d0 + 1
        sta cp_d1 + 1
        sta cp_d2 + 1
        sta cp_d3 + 1
        lda run_dst_hi,y
        sta cp_d0 + 2
        sta cp_d1 + 2
        sta cp_d2 + 2
        sta cp_d3 + 2
        ldx b_tmp + 1
        lda run_bytes,x
        sta b_tmp
        ldy #0
-
cp_s0   lda $ffff,y
cp_d0   sta $ffff,y
        iny
cp_s1   lda $ffff,y
cp_d1   sta $ffff,y
        iny
cp_s2   lda $ffff,y
cp_d2   sta $ffff,y
        iny
cp_s3   lda $ffff,y
cp_d3   sta $ffff,y
        iny
        cpy b_tmp
        bne -
        rts

        .cerror RUNS != 5, "copy_run: five runs"

; The other set is made: it is shown from the next frame.
; The screen's cells (screen A: the arena is reached after
; an even number of swaps) of rows 15-18 take its codes at
; the new columns; the old columns it no longer covers are
; emptied.
flip:
        lda shown_set
        eor #1
        sta shown_set
        lda prep_x
        sta shown_x
        lda prep_var
        sta shown_var
        lda prep_x              ; the new first column
        lsr a
        lsr a
        sta b_tmp
        clc
        adc #BODY_COLS
        sta b_tmp + 1           ; and the first past it
        ldx shown_col           ; the old columns
        ldy #BODY_COLS
_old:
        cpx #40                 ; off the screen
        bcs _new
        cpx b_tmp               ; still covered?
        bcc _empty
        cpx b_tmp + 1
        bcc _next
_empty:
        lda #0
        sta SCREEN_A + BODY_ROW * 40,x
        sta SCREEN_A + BODY_ROW * 40 + 40,x
        sta SCREEN_A + BODY_ROW * 40 + 80,x
        sta SCREEN_A + BODY_ROW * 40 + 120,x
_next:
        inx
        dey
        bne _old
_new:
        lda b_tmp
        sta shown_col
        tax                     ; X: the screen's column,
        ldy #0                  ; Y: the set's column
        lda shown_set
        beq _cell
        ldy #BODY_COLS
_cell:
        cpx #40                 ; the rest off the screen
        bcs _done
        lda set_code,y          ; its four codes, down
        sta SCREEN_A + BODY_ROW * 40,x
        adc #1                  ; (C = 0)
        sta SCREEN_A + BODY_ROW * 40 + 40,x
        adc #1
        sta SCREEN_A + BODY_ROW * 40 + 80,x
        adc #1
        sta SCREEN_A + BODY_ROW * 40 + 120,x
        inx
        iny
        cpx b_tmp + 1
        bne _cell
_done:
        rts

; ---------------------------------------------------------
; The boss's turn (update_varkon, after the plasma, before
; the Varkon move): for the frame after the next, as the
; Varkon.
; ---------------------------------------------------------

boss_update:
        lda arena
        bne +
        rts
+       lda level_boss          ; the SHIELD CORE:
        cmp #2                  ; part_x the sphere's, for
        bne +                   ; the chain
        lda #CB_PART_X
        sta part_x
        lda #0
        sta part_x + 1
        beq ++
+       jsr body_next           ; the parts' place
+       lda flash_left          ; the hull white: its end
        beq +
        dec flash_left
        bne +
        ldx #0                  ; its colour again
        jsr paint
+       lda bar_shown           ; the bar: a step a frame
        cmp bar_want            ; to what it must show
        beq _state
        bcc +
        dec bar_shown
        bcs ++
+       inc bar_shown
+       lda #1
        sta bar_dirty
_state:
        lda level_boss
        cmp #3                  ; from 3 on: its own parts
        bcc +                   ; and steps
        jmp W_STEP
+       cmp #2                  ; the SHIELD CORE's parts,
        bne +                   ; its steps
        jsr core_place
        lda boss_state
        clc
        adc #9
        tax
        bne ++
+       jsr place_parts
        ldx boss_state          ; the step's routine
+       lda b_steps_lo,x
        sta vector
        lda b_steps_hi,x
        sta vector + 1
        jmp (vector)

b_steps_lo:
        .byte <step_wait, <step_enter, <step_fight
        .byte <step_open, <step_core, <step_chain
        .byte <step_wreck, <step_clear, <step_done
        .byte <step_wait, <core_enter, <core_fight
        .byte <core_rage, <step_done, <step_chain
        .byte <step_wreck, <step_clear, <step_done
b_steps_hi:
        .byte >step_wait, >step_enter, >step_fight
        .byte >step_open, >step_core, >step_chain
        .byte >step_wreck, >step_clear, >step_done
        .byte >step_wait, >core_enter, >core_fight
        .byte >core_rage, >step_done, >step_chain
        .byte >step_wreck, >step_clear, >step_done

; The body the screen will show in the frame after the next
; (the Varkon's frame): the other set if it is half made
; (the next turn ends it), else the one shown. part_x = 2 x
; its x: the parts' x registers are counted from it.
body_next:
        lda prep_step
        beq +
        lda prep_x
        jmp ++
+       lda shown_x
+       asl a
        sta part_x
        lda #0
        rol a
        sta part_x + 1
        rts

; The parts alive on the body: their x register (part_x +
; their place), their line; xf 0.
place_parts:
        lda parts
        lsr a
        bcc +
        ldx part_a
        lda #CANNON_A_DX
        ldy #CANNON_Y
        jsr place_one
+       lda parts
        and #%00000010
        beq +
        ldx part_b
        lda #CANNON_B_DX
        ldy #CANNON_Y
        jsr place_one
+       lda parts
        and #%00000100
        beq +
        ldx part_core
        lda #CORE_DX
        ldy #CORE_Y
        jmp place_one
+       rts

; Varkon X at part_x + A (its x register), line Y.
place_one:
        clc
        adc part_x
        sta en_x,x
        lda part_x + 1
        adc #0
        sta en_xh,x
        lda #0
        sta en_xf,x
        tya
        sta en_y,x
        rts

; The parts that were alive and are not (destroyed: their
; Varkon explodes): out of parts.
check_parts:
        lda parts
        lsr a
        bcc +
        ldx part_a
        lda en_on,x
        cmp #FLYING
        beq +
        lda parts
        and #%11111110
        sta parts
+       lda parts
        and #%00000010
        beq +
        ldx part_b
        lda en_on,x
        cmp #FLYING
        beq +
        lda parts
        and #%11111101
        sta parts
+       lda parts
        and #%00000100
        beq +
        ldx part_core
        lda en_on,x
        cmp #FLYING
        beq +
        lda parts
        and #%11111011
        sta parts
+       rts

; --- WAIT -------------------------------------------------
; No Varkon flying or exploding for ARENA_WAIT frames: the
; boss's start (none: STAGE CLEAR at once, clear_now).
step_wait:
        ldx #ENEMIES - 1        ; a Varkon flying or
-       lda en_on,x             ; exploding: wait for it
        cmp #FLYING
        beq _busy
        cmp #BOOM
        beq _busy
        dex
        bpl -
        inc boss_timer
        lda boss_timer
        cmp #ARENA_WAIT
        bcs +
        rts
_busy:
        lda #0
        sta boss_timer
        rts
+       lda level_boss          ; the level's boss
        bne +                   ; none: STAGE CLEAR at
        jmp clear_now           ; once
+       cmp #2                  ; the SHIELD CORE: its
        bne +                   ; own start
        jmp core_begin
+       jsr free_varkon         ; the cannons: two free
        bcc +                   ; Varkon (else later)
        rts
+       stx part_a
        lda #FLYING             ; (taken, for the next
        sta en_on,x             ; search)
        jsr free_varkon
        bcc +
        lda #0                  ; one only: later
        ldx part_a
        sta en_on,x
        rts
+       stx part_b
        ldx part_a
        lda #FAN_PERIOD / 2     ; the first fans
        jsr new_cannon
        ldx part_b
        lda #FAN_PERIOD
        jsr new_cannon
        lda #%00000011
        sta parts
        lda #X_START            ; the body: at the right
        sta body_x
        lda #0
        sta body_xf
        sta body_var
        sta patrol
        sta patrol_left
        sta drone_turn
        lda #X_START            ; nothing shown, nothing
        sta shown_x             ; made yet
        lda #0
        sta shown_var
        sta shown_set
        lda #40
        sta shown_col
        lda #DRONE_EVERY_A
        sta mouth_timer
        jsr bar_on
        ldx #0                  ; rows 15-18: the hull's
        jsr paint_hull          ; colours
        lda #ST_ENTER
        sta boss_state
        jsr body_next
        jmp place_parts

; The bar fills, in red where VARKONIA was.
bar_on:
        lda #BAR_STEPS
        sta bar_want
        lda #1
        sta bar_dirty
        ldx #BAR_CELLS - 1
        lda #BAR_COLOUR
-       sta COLOURS + HUD_CELL + HUD_BAR,x
        dex
        bpl -
        rts

; The first free Varkon: X, C = 0; none: C = 1.
free_varkon:
        ldx #0
-       lda en_on,x
        beq +
        inx
        cpx #ENEMIES
        bne -
        sec
        rts
+       clc
        rts

; Varkon X a cannon, its first fan in A frames.
new_cannon:
        sta en_fire,x
        ldy #KIND_CANNON
        jsr new_part
        lda #0                  ; its aim: left
        sta en_aim,x
        rts

; Varkon X a part of kind Y, flying, still, not waiting:
; its behaviour, life, picture, colour, period from the
; kind; its object's priority in the multiplexer: a boss's
; part BOSS_PRI, over all the others (never left out), a
; drone the Varkon's.
new_part:
        lda kind_beh,y
        cmp #BOSS
        lda #BOSS_PRI
        bcs +
        lda #2
+       jsr set_pri
        lda #FLYING
        sta en_on,x
        tya
        sta en_kind,x
        lda #0
        sta en_delay,x
        sta en_flash,x
        sta en_cap,x
        sta en_left,x
        sta en_vxl,x
        sta en_vxh,x
        sta en_vxs,x
        sta en_vyl,x
        sta en_vyh,x
        sta en_yf,x
        lda kind_beh,y
        sta en_beh,x
        lda kind_life,y
        sta en_life,x
        lda kind_block,y
        sta en_block,x
        lda kind_pmask,y        ; four pictures or two
        sta en_pmask,x
        lda kind_colour,y
        sta en_colour,x
        lda kind_period,y
        sta en_period,x
        rts

; Varkon X's object: priority A, in both banks. X and Y
; kept.
set_pri:
        sta temp
        tya
        pha
        txa
        clc
        adc #FIRST_ENEMY
        tay
        lda temp
        sta obj_pri,y
        sta obj_pri + OBJ_BANK,y
        pla
        tay
        rts

BOSS_PRI = 8                    ; over 3 + STARVE
        .cerror BOSS_PRI <= 3 + STARVE, "BOSS_PRI"

; --- ENTER ------------------------------------------------
step_enter:
        sec                     ; to the left, to its
        lda body_xf             ; station
        sbc #ENTER_SPEED
        sta body_xf
        lda body_x
        sbc #0
        sta body_x
        cmp #X_STATION
        bcs +
        lda #X_STATION          ; there: the fight
        sta body_x
        lda #0
        sta body_xf
        lda #ST_FIGHT
        sta boss_state
+       jmp aim_cannons

; --- FIGHT ------------------------------------------------
step_fight:
        jsr check_parts
        lda parts
        and #%00000011
        bne +
        lda #ST_OPEN             ; both cannons destroyed:
        sta boss_state          ; the hatch opens, the
        lda #0                  ; mouth shuts
        sta boss_timer
        lda #%00000010
        sta body_var
        rts
+       jsr patrol_step         ; the cannons' patrol
        ldx #0
        jsr mouth
        jsr aim_cannons
        jsr fire_cannons
        jmp bar_life

; --- OPEN -------------------------------------------------
step_open:
        lda boss_timer          ; first: the core takes a
        bne +                   ; free Varkon
        jsr free_varkon
        bcs _later
        stx part_core
        ldy #KIND_CORE
        jsr new_part
        lda #CORE_PERIOD        ; its first shot
        sta en_fire,x
        lda parts
        ora #%00000100
        sta parts
        jsr place_parts
+       inc boss_timer
        lda boss_timer
        cmp #CORE_RISE_FRAMES
        bcc +
        lda #ST_CORE             ; risen: the core's fight
        sta boss_state
        lda #2
        sta patrol
        lda #0
        sta patrol_left
        lda #DRONE_EVERY_B
        sta mouth_timer
+       jmp bar_life
_later:
        rts

; --- CORE -------------------------------------------------
step_core:
        jsr check_parts
        lda parts
        and #%00000100
        bne +
        jmp boss_dies
+       jsr patrol_step         ; the core's patrol
        ldx #1
        jsr mouth
        jmp bar_life

; --- the end --------------------------------------------
; The core destroyed: every Varkon flying explodes (no
; points), the plasma is gone, the mouth shuts, the bar
; empties; the chain from the next frame.
boss_dies:
        ldx #ENEMIES - 1
-       lda en_on,x
        cmp #FLYING
        bne +
        lda #BOOM
        sta en_on,x
        lda #0
        sta en_left,x
        sta en_flash,x
+       dex
        bpl -
        lda #0
        ldx #ESHOTS - 1
-       sta sh_on,x
        dex
        bpl -
        sta chain_k
        sta bar_want
        sta boss_timer
        sta parts               ; none
        lda body_var            ; (the hatch stays open)
        and #%00000010
        sta body_var
        lda #ST_CHAIN
        sta boss_state
        rts

; --- CHAIN ------------------------------------------------
; Every CHAIN_EVERY frames a fireball on the body (a free
; Varkon exploding where chain_dx, chain_y say; none free:
; none), its sound, the hull white for a moment.
step_chain:
        inc boss_timer
        lda boss_timer
        cmp #CHAIN_EVERY
        bcc _done
        lda #0
        sta boss_timer
        jsr free_varkon
        bcs _next
        lda #2                  ; the Varkon's priority
        jsr set_pri
        lda #BOOM               ; a fireball of the boss's
        sta en_on,x             ; (its kind the core's)
        lda #KIND_CORE
        sta en_kind,x
        lda #BOSS
        sta en_beh,x
        lda #0
        sta en_left,x
        sta en_flash,x
        sta en_cap,x
        sta en_xf,x
        lda chain_k             ; the explosion's place:
        ldy level_boss          ; the SHIELD CORE's after
        cpy #2                  ; the crawler's
        bne +
        clc
        adc #CHAIN_COUNT
+       tay
        lda chain_y,y
        sta en_y,x
        lda chain_dx,y
        clc
        adc part_x
        sta en_x,x
        lda part_x + 1
        adc #0
        sta en_xh,x
_next:
        lda #FX_EXPLODE
        jsr sfx_start
        lda #3                  ; the hull white
        sta flash_left
        ldx #1
        jsr paint
        inc chain_k
        lda chain_k
        cmp #CHAIN_COUNT
        bcc _done
        lda #ST_WRECK
        sta boss_state
_done:
        rts

; --- WRECK ------------------------------------------------
step_wreck:
        inc boss_timer
        lda boss_timer
        cmp #WRECK_PAINT        ; the hull dark
        bne +
        ldx #2
        jsr paint
+       lda boss_timer
        cmp #WRECK_WAIT
        bcc +
clear_now:
        lda #ST_CLEAR            ; then STAGE CLEAR
        sta boss_state
        lda #0
        sta boss_timer
        sta chain_k
        jmp text_on
+       rts

; --- CLEAR ------------------------------------------------
; STAGE CLEAR's colours turn; the ship, flying or coming
; in, flies off; a notch of the shield into the score every
; NOTCH_EVERY frames; none left and the ship gone,
; CLEAR_WAIT frames, then the level again.
step_clear:
        lda anim                ; the first line's colour
        lsr a
        lsr a
        and #%00000011
        tay
        lda text_cycle,y
        ldx #TEXT_CELLS - 1
-       ldy text_line,x
        bne +
        ldy text_lo,x
        sta COLOURS,y           ; (rows 0-6: offsets < 256)
+       dex
        bpl -
        lda ship_mode           ; the ship flies off
        beq +
        cmp #ENTER
        bne ++
+       lda #LEAVE
        sta ship_mode
        lda #0
        sta ship_blink
+       inc boss_timer
        lda boss_timer
        cmp #NOTCH_EVERY
        bcc _wait
        lda #0
        sta boss_timer
        lda shield              ; a notch into the score
        beq _wait
        dec shield
        lda #1
        sta hud_dirty
        ldy #KIND_NOTCH
        jsr score_add
        lda #FX_CAPSULE
        jsr sfx_start
_wait:
        lda shield
        bne _done
        lda ship_mode
        cmp #GONE
        bne _done
        inc chain_k
        lda chain_k
        cmp #CLEAR_WAIT
        bcc _done
        lda #ST_DONE             ; the next level
        sta boss_state
        lda #1
        sta restart_flag
_done:
        rts

step_done:
        rts

; STAGE CLEAR on the screen: the letters' glyphs from the
; HUD's set into the level's characters, the texts' cells
; and their colours (hi-res).
text_on:
        ldx #LETTERS - 1
_letter:
        lda letter_glyph,x      ; the glyph: HUDSET + 8 g
        sta src
        lda #0
        .rept 3
        asl src
        rol a
        .endrept
        adc #>HUDSET            ; (C = 0)
        sta src + 1
        lda letter_code,x       ; to CHARSET + 8 code
        sta dst
        lda #0
        .rept 3
        asl dst
        rol a
        .endrept
        adc #>CHARSET
        sta dst + 1
        ldy #7
-       lda (src),y
        sta (dst),y
        dey
        bpl -
        dex
        bpl _letter
        ldx #TEXT_CELLS - 1     ; the cells
-       lda text_lo,x
        sta dst
        lda text_hi,x
        clc
        adc #>SCREEN_A
        sta dst + 1
        lda text_code,x
        ldy #0
        sta (dst),y
        lda text_hi,x           ; its colour
        clc
        adc #>COLOURS
        sta dst + 1
        lda #TEXT_COLOUR
        sta (dst),y
        dex
        bpl -
        rts

        .cerror (SCREEN_A | COLOURS) & $ff != 0

; The boss's colours: X 0 its own, 1 white, 2 the wreck's
; (the SHIELD CORE's sphere: core.asm; a boss from 3 on, its
; own: W_PAINT).
paint:
        lda level_boss
        cmp #2
        beq +
        bcc paint_hull
        jmp W_PAINT
+       jmp paint_sphere

; The colours of rows 15-18, all along (only the body is
; there in the arena): X 0 the hull's, 1 white, 2 the
; wreck's (hull_colour, four a row).
paint_hull:
        txa
        asl a
        asl a
        tay
        ldx #39
-       lda hull_colour,y
        sta COLOURS + BODY_ROW * 40,x
        lda hull_colour + 1,y
        sta COLOURS + BODY_ROW * 40 + 40,x
        lda hull_colour + 2,y
        sta COLOURS + BODY_ROW * 40 + 80,x
        lda hull_colour + 3,y
        sta COLOURS + BODY_ROW * 40 + 120,x
        dex
        bpl -
        rts

; ---------------------------------------------------------
; Its ways: the patrol, the mouth, the cannons.
; ---------------------------------------------------------

; The patrol (its entry: patrol, 0-1 the cannons' fight,
; 2-3 the core's): wait at a place, then to the other of
; its two at its speed; there, its wait.
patrol_step:
        lda patrol_left
        beq +
        dec patrol_left
        rts
+       ldx patrol
        lda body_x              ; which way?
        cmp patrol_to,x
        bcc _right
        bne _left
        lda body_xf
        beq _there
_left:
        sec
        lda body_xf
        sbc patrol_speed,x
        sta body_xf
        lda body_x
        sbc #0
        sta body_x
        cmp patrol_to,x         ; past it?
        bcs _done
        bcc _there
_right:
        clc
        lda body_xf
        adc patrol_speed,x
        sta body_xf
        lda body_x
        adc #0
        sta body_x
        cmp patrol_to,x
        bcc _done
_there:
        lda patrol_to,x         ; there: its wait, then the
        sta body_x              ; other place
        lda #0
        sta body_xf
        lda patrol_wait,x
        sta patrol_left
        txa
        eor #1
        sta patrol
_done:
        rts

; The mouth (X: 0 the cannons' fight, 1 the core's): a
; drone every DRONE_EVERY frames, if fewer than DRONES_MAX
; fly; open MOUTH_OPEN frames before and after.
mouth:
        stx b_tmp + 1
        dec mouth_timer
        bne _open
        lda drone_every,x       ; again
        sta mouth_timer
        ldy #0                  ; the drones flying
        ldx #ENEMIES - 1
-       lda en_on,x
        cmp #FLYING
        bne +
        lda en_kind,x
        cmp #KIND_DRONE
        bne +
        iny
+       dex
        bpl -
        ldx b_tmp + 1
        tya
        cmp drones_max,x
        bcs _open
        jsr launch
        ldx b_tmp + 1
_open:
        lda body_var            ; open or shut
        and #%11111110
        sta body_var
        lda mouth_timer
        cmp #MOUTH_OPEN + 1
        bcc _opened
        lda drone_every,x
        sec
        sbc mouth_timer
        cmp #MOUTH_OPEN
        bcs _shut
_opened:
        inc body_var
_shut:
        rts

drone_every:
        .byte DRONE_EVERY_A, DRONE_EVERY_B
drones_max:
        .byte DRONES_MAX_A, DRONES_MAX_B

; A drone from the mouth (a free Varkon; none: none): its
; path up or low in turn, its sound.
launch:
        jsr free_varkon
        bcs _none
        ldy #KIND_DRONE
        jsr new_part
        lda #0
        sta en_xf,x
        lda #MOUTH_DX
        clc
        adc part_x
        sta en_x,x
        lda part_x + 1
        adc #0
        sta en_xh,x
        lda #MOUTH_Y
        sta en_y,x
        lda en_period,x         ; its first shot: half its
        lsr a                   ; period
        sta en_fire,x
        lda #PATH_LAUNCH_UP
        ldy drone_turn
        beq +
        lda #PATH_LAUNCH_LOW
+       sta en_seg,x
        tya
        eor #1
        sta drone_turn
        jsr load_stretch
        lda #FX_MISSILE
        jmp sfx_start
_none:
        rts

; Each cannon alive turns its barrel to the ship (en_aim):
; dx = its x register - the ship's, dy = its line + 2 -
; the ship's. The ship to its right (dx <= 0): up, two
; lines a pixel (2). Not above it (dy <= 0): left (0).
; Else q = dx / 4: 2 if dy >= 3 q, 1 if dy >= q, else 0.
aim_cannons:
        lda parts
        lsr a
        bcc +
        ldx part_a
        jsr aim_one
+       lda parts
        and #%00000010
        beq +
        ldx part_b
        jmp aim_one
+       rts

aim_one:
        jsr aim_dx              ; q; the ship to its right:
        bcs aim_up              ; up
        lda en_y,x              ; dy = its line + 2 - the
        clc                     ; ship's
        adc #2
        sec
        sbc ship_y
        bcc aim_left            ; the ship lower: left
        beq aim_left
aim_dy:
        sta b_tmp + 1           ; dy (1-255)
        lda b_tmp               ; 3 q (9 bits: C)
        asl a
        bcs _shallow            ; 2 q over 255
        adc b_tmp
        bcs _shallow
        cmp b_tmp + 1
        beq aim_up
        bcc aim_up              ; dy >= 3 q
_shallow:
        lda b_tmp + 1
        cmp b_tmp
        bcs aim_mid             ; dy >= q
aim_left:
        lda #0
        beq aim_set
aim_mid:
        lda #1
        bne aim_set
aim_up:
        lda #2
aim_set:
        sta en_aim,x
        rts

; dx = Varkon X's x register - the ship's: the ship to its
; right, or q = dx / 4 0: C = 1; else C = 0, b_tmp = q.
aim_dx:
        lda ship_x              ; the ship's x register
        clc
        adc #24
        sta b_tmp
        lda ship_xh
        adc #0
        sta b_tmp + 1
        sec                     ; dx
        lda en_x,x
        sbc b_tmp
        sta b_tmp
        lda en_xh,x
        sbc b_tmp + 1
        bmi _right              ; negative: to its right
        lsr a                   ; q = dx / 4
        ror b_tmp
        lsr a
        ror b_tmp
        ora b_tmp
        beq _right              ; dx 0-3: q 0... and dx 0
        clc
        rts
_right:
        sec
        rts

; Each cannon alive: its fan when its time comes (en_fire
; counts the frames), FAN_PERIOD frames to the next.
fire_cannons:
        lda parts
        lsr a
        bcc +
        ldx part_a
        jsr fire_one
+       lda parts
        and #%00000010
        beq +
        ldx part_b
        jmp fire_one
+       rts

fire_one:
        dec en_fire,x
        bne _done
        lda #FAN_PERIOD
        sta en_fire,x
        stx b_tmp + 1           ; its fan: three shots,
        lda en_aim,x            ; entries FAN_FIRST + 3
        sta b_tmp               ; aim + 0-2
        asl a
        adc b_tmp
        adc #FAN_FIRST
        sta b_tmp
        ldy #3
-       sty v_k
        lda b_tmp
        sta f_entry
        ldx b_tmp + 1
        jsr fire_entry
        inc b_tmp
        ldy v_k
        dey
        bne -
        ldx b_tmp + 1
_done:
        rts

; The bar's steps by the life left: the cannons alive, the
; core's (all of it before it comes).
bar_life:
        lda #0
        sta b_tmp
        lda parts
        lsr a
        bcc +
        ldx part_a
        lda en_life,x
        sta b_tmp
+       lda parts
        and #%00000010
        beq +
        ldx part_b
        lda en_life,x
        clc
        adc b_tmp
        sta b_tmp
+       lda parts
        and #%00000100
        beq +
        ldx part_core
        lda en_life,x
        jmp ++
+       lda #CORE_LIFE          ; to come, or gone
        ldx part_core
        cpx #$ff
        beq +
        lda #0
+       clc
        adc b_tmp
        tax
        lda bar_of_life,x
        sta bar_want
        rts

; The HUD's bar (update_hud): its cells by bar_shown, if
; it has changed: cell k shows bar_shown - 8 k columns,
; 0-8.
boss_hud:
        lda bar_dirty
        beq _done
        lda #0
        sta bar_dirty
        lda bar_shown
        ldx #0
_cell:
        cmp #9
        bcc +
        tay
        lda #BAR_CODE + 8
        sta SCREEN_A + HUD_CELL + HUD_BAR,x
        tya
        sec
        sbc #8
        jmp _next
+       tay
        clc
        adc #BAR_CODE
        sta SCREEN_A + HUD_CELL + HUD_BAR,x
        lda #0
_next:
        inx
        cpx #BAR_CELLS
        bne _cell
_done:
        rts

; The ship's part in a boss's part's picture (move_varkon):
; a cannon's by its aim, the core's rising (OPEN: by the
; frames) or glowing (by anim).
part_picture:
        lda en_kind,x
        cmp #KIND_SEGMENT       ; the SHIELD CORE's
        bcc +
        jmp core_picture
+       cmp #KIND_CANNON
        bne +
        lda en_aim,x
        clc
        adc en_block,x
        sta obj_block,y
        rts
+       lda boss_state
        cmp #ST_OPEN
        bne +
        lda boss_timer          ; (frame - 1) / 8
        sec
        sbc #1
        lsr a
        lsr a
        lsr a
        clc
        adc #CORE_RISE_BLOCK
        sta obj_block,y
        rts
+       lda anim3
        clc
        adc en_block,x
        sta obj_block,y
        rts

        .cerror CORE_RISE_EVERY != 8, "part_picture: / 8"
