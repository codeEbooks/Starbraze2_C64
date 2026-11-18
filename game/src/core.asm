; The SHIELD CORE, the boss of level 2
; (game/assets/shieldcore.py). The level plan (§2): the main
; generator, a sphere in the middle of the arena with four
; segments of shield that turn around it; the segments open
; in turn, the core fires, it is hit through the gap. The
; author's decisions (18 October): «Nucleo e due cannoni»
; and the segments «Fermano i colpi, toccarli costa 1»; (19
; October) «bisogna rendere mortali gli scudi»: the segments
; «Distruggibili a colpi», «12 colpi ciascuno», «Resta
; distrutto».
;
; The engine is boss.asm's (common to the levels: level_boss
; 1 the SIEGE CRAWLER, 2 this one): WAIT, the chain, the
; wreck, STAGE CLEAR are its. Here the SHIELD CORE's own:
; its start (core_begin), its steps ENTER (it comes on),
; FIGHT and RAGE (under half the core's life), its parts'
; places and pictures, its colours.
;  - the sphere: 6 x 6 characters, still (codes from
;    SPHERE_FIRST, which the arena does not show), its cells
;    on screen A; not rock: the arena's rock is the rock's
;    table here (arena_chars 0), its codes emptied in it.
;    Its characters have the horizon's pixels around it (the
;    far layer's, build_assets.py), its last rows the
;    horizon's colours. Its cells' writes are made early
;    in a turn, in boss_draw (sphere_draw: before the beam
;    draws rows 8-13), asked for by boss_update (cb_paint):
;    the cells on, its colours, white, the arena's cells
;    again;
;    in ENTER it grows from its equator, two lines a frame;
;  - the core: in the sphere's middle, the shots' target;
;  - the segments: four Varkon around the core, at the
;    angle of the turn (cb_angle, 64 steps) + 16 k, at a
;    radius that closes the core (R_IN); in turn one goes
;    out to R_OUT and back (cb_open_k, cb_open_r, by the
;    frames of its cycle cb_open_t). A shot ends on one,
;    a laser too (hits.asm), and takes its
;    damage: one destroyed is not placed again (seg_put),
;    its gap stays open;
;  - the cannons: two pods, the top one (part_a) fires its
;    fans downwards, the low one (part_b) upwards; the boss
;    engine's parts bits 0-1, the core bit 2.

SPHERE_AT = SCREEN_A + SPHERE_ROW * 40 + SPHERE_COL
SPHERE_COLOURS = COLOURS + SPHERE_ROW * 40 + SPHERE_COL

; WAIT is over: seven free Varkon (a capsule may keep one:
; else later), the four segments, the core, the two pods
; (the core and the pods where they stay); the arena's 36
; cells kept (codes, colours: cb_save); the bar; ENTER.
core_begin:
        ldx #ENEMIES - 1
        ldy #0
-       lda en_on,x
        bne +
        iny
+       dex
        bpl -
        cpy #7
        bcs +
        rts
+       ldy #0                  ; the segments
-       sty b_tmp + 1
        jsr free_varkon
        txa
        ldy b_tmp + 1
        sta cb_seg,y
        ldy #KIND_SEGMENT
        jsr new_part
        ldy b_tmp + 1
        iny
        cpy #4
        bne -
        jsr free_varkon         ; the core: its first shot
        stx part_core           ; after ENTER
        ldy #KIND_SHCORE
        jsr new_part
        lda #CB_CORE_FIRST
        sta en_fire,x
        jsr free_varkon         ; the pods, their first fans
        stx part_a
        lda #CB_FAN_PERIOD / 2
        jsr new_pod
        jsr free_varkon
        stx part_b
        lda #CB_FAN_PERIOD
        jsr new_pod
        lda #%00000111
        sta parts
        ldx part_core           ; the core, the pods: still
        lda #CB_CORE_XR
        ldy #CB_CORE_Y
        jsr place_fixed
        ldx part_a
        lda #CB_POD_XR
        ldy #CB_POD_TOP_Y
        jsr place_fixed
        ldx part_b
        lda #CB_POD_XR
        ldy #CB_POD_LOW_Y
        jsr place_fixed
        ldx #SPHERE_CELLS - 1   ; the arena's cells kept
-       ldy cb_cell,x
        lda SPHERE_AT,y
        sta cb_save,x
        lda SPHERE_COLOURS,y
        and #%00001111
        sta cb_save + SPHERE_CELLS,x
        dex
        bpl -
        stx cb_last             ; (core_place: all to do)
        jsr bar_on
        lda #0
        sta boss_timer
        sta cb_angle
        sta cb_angle + 1
        sta cb_open_t
        sta cb_shots
        lda #3                  ; the first gap: segment 3
        sta cb_open_k
        lda #R_ENTER
        sta cb_rad
        sta cb_open_r
        lda #ST_ENTER
        sta boss_state
        jmp core_place

; Cell X of the sphere: the character the arena's cell
; showed into its code (CHARSET + 8 code to CHARSET + 8
; (SPHERE_FIRST + X)). X kept.
cell_behind:
        lda cb_save,x
        sta src
        sta src
        lda #0
        .rept 3
        asl src
        rol a
        .endrept
        adc #>CHARSET           ; (C = 0)
        sta src + 1
        txa                     ; to CHARSET + 8
        clc                     ; (SPHERE_FIRST + k)
        adc #SPHERE_FIRST
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
        rts

; Varkon X a pod, its first fan in A frames, its aim left.
new_pod:
        sta en_fire,x
        ldy #KIND_POD
        jsr new_part
        lda #0
        sta en_aim,x
        rts

; --- ENTER: it comes on -----------------------------------
; Frames 1 to CB_PREP - 1: in the sphere's codes the
; characters its cells show, a row a frame (so that nothing
; changes when they take them); frame CB_PREP: its codes out
; of the rock's table, its cells on in the next turn; then
; it grows (sphere_draw). The segments close in from
; R_ENTER, a pixel every two frames, to R_IN, turning;
; ENTER_FRAMES, then FIGHT.
core_enter:
        inc boss_timer
        lda boss_timer
        cmp #CB_PREP
        bcc _row
        bne _close
        lda #0                  ; not rock
        ldx #SPHERE_CELLS - 1
-       .for r_k in range(8)
        sta rock_lines + r_k * 256 + SPHERE_FIRST,x
        .endfor
        dex
        bpl -
        lda #1                  ; its cells, next turn
        sta cb_paint
        bne _close
_row:
        asl a                   ; row frame - 1: cells 6 f -
        sta b_tmp               ; 6 to 6 f - 1 (f the frame)
        asl a
        adc b_tmp               ; (C = 0)
        tax
        lda #SPHERE_COLS
        sta b_tmp
-       dex
        jsr cell_behind
        dec b_tmp
        bne -
_close:
        lda boss_timer
        lsr a
        sta b_tmp
        lda #R_ENTER
        sec
        sbc b_tmp
        cmp #R_IN
        bcs +
        lda #R_IN
+       sta cb_rad
        sta cb_open_r
        lda #CB_SPIN_A
        jsr spin
        lda boss_timer
        cmp #CB_ENTER_FRAMES
        bcc +
        lda #ST_FIGHT
        sta boss_state
+       rts

; --- FIGHT, RAGE ------------------------------------------
; The core destroyed: the end (boss_dies). In FIGHT, the
; core down to RAGE_LIFE: RAGE (its shots BURST_GAP frames
; apart, bursts of BURST, then BURST_PAUSE). The turn, the
; gap, the pods' aim and fans, the bar (the core's life).
core_fight:
core_rage:
        jsr check_parts
        lda parts
        and #%00000100
        bne +
        jmp boss_dies
+       ldx part_core
        lda boss_state
        cmp #ST_RAGE
        beq _rage
        lda en_life,x
        cmp #CB_RAGE_LIFE + 1
        bcs _turn
        lda #ST_RAGE            ; half its life: RAGE
        sta boss_state
        lda #CB_BURST_GAP
        sta en_period,x
        bne _turn
_rage:
        lda cb_shots            ; a burst ended: the pause
        cmp #CB_BURST
        bne +
        lda #CB_BURST_PAUSE
        sta en_fire,x
        lda #0
        sta cb_shots
+       lda en_fire,x           ; it fires in this frame
        cmp #1
        bne _turn
        inc cb_shots
_turn:
        lda boss_state          ; the phase: 0 FIGHT, 1 RAGE
        sec
        sbc #ST_FIGHT
        tay
        lda cb_spin,y
        jsr spin
        inc cb_open_t           ; the gap's cycle
        lda cb_open_t
        cmp cb_open_every,y
        bcc +
        lda #0
        sta cb_open_t
        lda cb_open_k           ; the next segment
        clc
        adc #1
        and #%00000011
        sta cb_open_k
+       lda cb_open_t           ; out, held, in, closed
        cmp #CB_OPEN_STEPS
        bcs +
        asl a
        adc #R_IN               ; (C = 0)
        bne _r
+       sbc #CB_OPEN_STEPS      ; (C = 1)
        cmp cb_open_hold,y
        bcs +
        lda #R_OUT
        bne _r
+       sbc cb_open_hold,y      ; (C = 1)
        cmp #CB_OPEN_STEPS
        bcs _closed
        asl a
        sta b_tmp
        lda #R_OUT
        sec
        sbc b_tmp
        bne _r
_closed:
        lda #R_IN
_r:
        sta cb_open_r
        lda parts               ; the pods
        lsr a
        bcc +
        ldx part_a              ; its fan in this frame: its
        dec en_fire,x           ; aim, the fan
        bne +
        jsr aim_top
        ldy #POD_FAN_FIRST + 9
        jsr fan_pod
+       lda parts
        and #%00000010
        beq +
        ldx part_b
        dec en_fire,x
        bne +
        jsr aim_one
        ldy #POD_FAN_FIRST
        jsr fan_pod
+       ldx part_core           ; the bar: the core's life
        lda en_life,x
        sta bar_want
        rts

cb_spin:
        .byte CB_SPIN_A, CB_SPIN_B
cb_open_every:
        .byte CB_OPEN_EVERY_A, CB_OPEN_EVERY_B
cb_open_hold:
        .byte CB_OPEN_HOLD_A, CB_OPEN_HOLD_B

; The turn on by A (256ths of a step).
spin:
        clc
        adc cb_angle
        sta cb_angle
        bcc +
        inc cb_angle + 1
+       rts

; Pod X's fan (its en_fire, counting the frames, has come
; to 0): CB_FAN_PERIOD frames to the next; three shots,
; entries Y + 3 aim + 0-2.
fan_pod:
        lda #CB_FAN_PERIOD
        sta en_fire,x
        sty b_tmp
        stx b_tmp + 1
        lda en_aim,x
        asl a
        adc en_aim,x            ; (C = 0)
        adc b_tmp
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
        rts

; The top pod (X) turns to the ship below it, as aim_one
; (boss.asm) does to the ship above: dx = its x register -
; the ship's; the ship to its right (dx < 4): down (2); dy =
; the ship's line - its line - 2: not below it, left (0);
; else q = dx / 4: 2 if dy >= 3 q, 1 if dy >= q, else 0.
aim_top:
        jsr aim_dx
        bcs _down
        lda ship_y
        sec
        sbc en_y,x
        sec
        sbc #2
        bcc _left
        beq _left
        jmp aim_dy
_left:
        lda #0
        sta en_aim,x
        rts
_down:
        lda #2
        sta en_aim,x
        rts

; --- the parts' places, each frame (boss_update) ----------
; The segments (ENTER, FIGHT, RAGE): segment k at the angle
; cb_angle + 16 k, at cb_rad (the open one at cb_open_r):
; its middle (CX + dx, CY + dy), dx = r cos, dy = r sin
; (seg_xy). The cosines' table turns over by a half turn
; (cos(a + 32) = -cos a, checked: build_assets.py), so a
; quarter turn on is (-dy, dx): the closed ones from one
; pair of products, the open one from its own. (The core
; and the pods stay where core_begin put them.)
core_place:
        lda boss_state
        beq +
        cmp #ST_CHAIN
        bcc ++
+       rts
+       ldx #3                  ; the turn's step, the open
-       lda cb_angle + 1,x      ; one, its radius, the
        cmp cb_last,x           ; closed radius as when it
        bne _new                ; placed them: nothing to do
        dex
        bpl -
        rts
_new:
        ldx #3
-       lda cb_angle + 1,x
        sta cb_last,x
        dex
        bpl -
        lda cb_angle + 1        ; segment 0 at the closed
        ldx cb_rad              ; radius
        jsr seg_xy
        ldx #$ff                ; the open one by itself, if
        lda cb_open_r           ; not at the closed radius
        cmp cb_rad              ; (m_b: the one left out)
        beq +
        ldx cb_open_k
+       stx m_b
        lda #0                  ; k (m_a: seg_off's, free
        sta m_a                 ; here)
_seg:
        lda m_a
        cmp m_b
        beq +
        tay
        ldx cb_seg,y
        jsr seg_put
+       lda b_tmp + 1           ; a quarter turn on: (dx,
        eor #$ff                ; dy) to (-dy, dx)
        clc
        adc #1
        ldx b_tmp
        sta b_tmp
        stx b_tmp + 1
        inc m_a
        lda m_a
        cmp #4
        bne _seg
        ldx m_b                 ; the open one
        bpl +
        rts
+       txa
        asl a
        asl a
        asl a
        asl a
        adc cb_angle + 1        ; (C = 0)
        ldx cb_open_r
        jsr seg_xy
        ldy cb_open_k
        ldx cb_seg,y
seg_put:                        ; Varkon X at (dx, dy): its
        lda en_on,x             ; x register, 16 bits (not
        cmp #FLYING             ; if destroyed: it stays,
        bne _gone               ; exploding)
        ldy #0
        lda b_tmp
        bpl +
        dey
+       clc
        adc #<CB_SEG_XR
        sta en_x,x
        tya
        adc #>CB_SEG_XR
        sta en_xh,x
        lda #0
        sta en_xf,x
        lda b_tmp + 1
        clc
        adc #CB_SEG_Y
        sta en_y,x
_gone:
        rts

; Angle A (any: AND 63), radius X: b_tmp = dx = r cos a,
; b_tmp + 1 = dy = r sin a (sin a = cos(a + 48)). The radii
; of FIGHT and RAGE (R_IN, R_IN + 2 ... R_OUT) from their
; table (seg_tab: a row a radius, r |cos| / 64 for the 17
; cosines of a quarter turn); the others (ENTER) by
; products (seg_off).
seg_xy:
        stx m_r
        and #ANGLES - 1
        sta m_lo
        txa
        sec
        sbc #R_IN
        bcc _mul                ; under R_IN
        cmp #R_OUT - R_IN + 1
        bcs _mul                ; over R_OUT
        lsr a
        bcs _mul                ; R_IN + an odd number
        sta m_b                 ; t: the row 17 t
        asl a
        asl a
        asl a
        asl a
        adc m_b                 ; (C = 0)
        sta m_b
        lda m_lo
        jsr seg_look
        sta b_tmp
        lda m_lo
        clc
        adc #ANGLES * 3 / 4
        and #ANGLES - 1
        jsr seg_look
        sta b_tmp + 1
        rts
_mul:
        lda m_lo
        tay
        lda cosine,y
        jsr seg_off
        sta b_tmp
        lda m_lo
        sec
        sbc #ANGLES / 4
        and #ANGLES - 1
        tay
        lda cosine,y
        jsr seg_off
        sta b_tmp + 1
        rts

; Angle A (0-63), row m_b of seg_tab: r cos a / 64. Its
; place in the quarter turn: a AND 31, over 16 32 - it; its
; sign: minus when a + 15 has bit 5 (a 17-47; at 16 and 48
; the cosine is 0).
seg_look:
        sta m_a
        and #%00011111
        cmp #17
        bcc +
        eor #%00011111          ; 31 - it, + 1 (C = 1)
        adc #0
+       adc m_b                 ; (C = 0)
        tax
        lda m_a
        adc #15                 ; (C = 0)
        and #%00100000
        beq +
        lda #0
        sec
        sbc seg_tab,x
        rts
+       lda seg_tab,x
        rts

; Varkon X at x register A (under 256), line Y.
place_fixed:
        sta en_x,x
        tya
        sta en_y,x
        lda #0
        sta en_xh,x
        sta en_xf,x
        rts

        .cerror CB_CORE_XR > 255 || CB_POD_XR > 255

; A (a cosine, -64 to 64) times the radius m_r (under 64),
; over 64, with A's sign: A. Six steps of shift and add, one
; a bit of m_r: after them A is the product / 64 (the low
; bits are let go: rounded down, as / 64). X kept.
seg_off:
        sta m_sign
        bpl +
        eor #$ff
        clc
        adc #1
+       sta m_a
        lda m_r
        sta m_b
        lda #0
        ldy #6
-       lsr m_b
        bcc +
        clc
        adc m_a
+       ror a
        dey
        bne -
        bit m_sign
        bpl +
        eor #$ff
        clc
        adc #1
+       rts

        .cerror R_ENTER > 63 || R_OUT > 63, "seg_off: m_r"

; --- the pictures (part_picture), the colours -------------
; A part of the SHIELD CORE (X, object Y): its two pictures
; by the frame.
core_picture:
        lda anim3
        and #%00000001
        clc
        adc en_block,x
        sta obj_block,y
        rts

; The sphere's colours (boss.asm's paint): X 0 its own, 1
; white, 2 gone (the arena's cells again): asked for, done
; in the next turn's sphere_draw (cb_paint 2, 3, 4).
paint_sphere:
        inx
        inx
        stx cb_paint
        rts

seg_tab:                        ; r |cos| / 64 (seg_look)
        .binary "../assets/generated/seg_tab.bin"


SPHERE_LINES = 8 * SPHERE_ROWS
        .cerror CB_GROW_FRAMES * 2 != SPHERE_LINES
        .cerror CB_PREP - 1 != SPHERE_ROWS, "a row a frame"
        .cerror (SPHERE_ROWS - 1) * 8 * SPHERE_COLS > 248
        .cerror (CHARSET & $ff) != 0, "CHARSET: a page"
        .cerror cb_save + 2 * SPHERE_CELLS != CB_SAVE_END
        .cerror CB_SAVE_END > star_rec, "cb_save"

; (Its sphere on the screen: sphere.asm; its data,
; sphere_data and cosine: main.asm, in the high part.)
