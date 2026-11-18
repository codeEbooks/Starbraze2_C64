; The GRAVEYARD WARDEN, the boss of level 3
; (game/assets/warden.py). The level plan (§2): a mass of
; wrecks welded together by the Varkon; it fires from its
; openings, which open one at a time; it crumbles in pieces.
; The author's decisions (21 October): «Aperture, poi il
; nucleo», «Su e giù, lento», «A ogni apertura distrutta»,
; «Come lo SHIELD CORE».
;
; Assembled by itself at WARDEN_AT (from $f000, RAM under
; the KERNAL), after the program, whose labels it reads
; (game/build/main.inc); level 3's file (LEVEL3) brings it,
; a record after the store's (tools/make_disk.py). The
; program comes here through the jumps at its start:
; boss_draw's (the body), boss_update's (its steps), paint's
; (its colours).
;
; The engine is boss.asm's: the bar, the white flash, the
; wreck, STAGE CLEAR. Here the WARDEN's own:
;  - the body: 7 columns x 72 lines of characters at the
;    arena's right edge (columns 32-38: 39 is under the
;    border), its top line wd_y (signed: it comes down from
;    above the screen). Its drawing (wd_comp: each column 8
;    empty lines, 72, 8 empty) is copied, shifted down by
;    wd_y AND 7, into ten characters a column of the set the
;    screen does not show (wd_code), a column a turn, and
;    into the rock's table (rock_lines: it is rock); over
;    the nebula (rows 11-13) its empty pixels take the
;    nebula's; then the flip: screen A's cells take that
;    set, the rows it leaves get the arena's cells back
;    (kept at the start: wd_save_code, wd_save_col, eight
;    places a row);
;  - rows 10-14 are rock while it is there (rock_row, and
;    air_rock: the ship's and the shots' shortcut of the
;    corridor off; the far layer's codes out of the rock's
;    table): boss_reset puts them back at the level's start;
;  - its drawing changes by patches (wd_want: the four ports
;    shut, open, destroyed; the core's pit shut, open),
;    copied into wd_comp when a new body is made;
;  - the ports open in turn (wd_order): a gun of the Varkon
;    in it (part_a) fires its fans, then goes back in (its
;    life kept); destroyed, the port breaks off (two shards,
;    hits.asm's split) and the next one opens;
;  - all four destroyed: the core's pit opens, the core
;    (part_core) fires, under half its life faster; two
;    shards from it now and then; destroyed, the engine's
;    end (boss_dies), its chain on the body (wd_chain).

        .include "main.inc"     ; (-I its build)
        .include "../assets/generated/warden.inc"

; Its variables, where the SHIELD CORE's are (page 2, 0 at
; the level's start: boss_reset), and the engine's own ones
; with its meaning.
wd_y     = body_x               ; its top line (signed)
wd_yf    = body_xf              ; 256ths
shown_y  = shown_x              ; the body the screen shows,
prep_y   = prep_x               ; the one being made
wd_cycle = shown_var            ; the port: 0 shut, 1 open
wd_turn  = prep_var             ; its place in wd_order
wd_timer = mouth_timer          ; frames left of its step
wd_shed  = drone_turn           ; frames to the shards
wd_gone  = cb_angle             ; the ports destroyed (bits)
wd_life  = wd_gone + 1          ; 4: the guns' lives
wd_want  = wd_life + 4          ; 5: the patches wanted:
wd_have  = wd_want + 5          ; ports 0-3, the core; made
wd_r0    = wd_have + 5          ; the rows of it shown: r0
wd_r1    = wd_r0 + 1            ; to r1 - 1
wd_colour = wd_r1 + 1           ; its cells' colour
wd_port  = wd_colour + 1        ; the port open (or last)
wd_s     = wd_port + 1          ; the body being made: its
wd_off   = wd_s + 1             ; line AND 7, 8 - that,
wd_row0  = wd_off + 1           ; its first row (signed),
wd_kb0   = wd_row0 + 1          ; its codes over the
wd_kb1   = wd_kb0 + 1           ; nebula: from, to
wd_c     = wd_kb1 + 1           ; scratch: a column,
wd_k     = wd_c + 1             ; a code or a row,
wd_t     = wd_k + 1             ; and three more
wd_b     = wd_t + 1
wd_m     = wd_b + 1
W_VARS_END = wd_m + 1
        .cerror W_VARS_END > CB_SAVE_END, "its variables"
        .cerror wd_gone != arena_chars + 1

        * = WARDEN_AT
        jmp wd_step             ; W_DRAW
        jmp wd_draw             ; W_STEP
        jmp wd_paint            ; W_PAINT
        .cerror wd_draw - WARDEN_AT != 9

; ---------------------------------------------------------
; The body on the screen (boss_draw, a turn): nothing to
; do, or the patches and column 0 of the other set; column
; 1; ... column 6; the flip (a turn each: the frame has
; time for one).
; ---------------------------------------------------------

wd_draw:
        lda boss_state          ; WAIT: no body yet
        beq _done
        ldx prep_step
        beq _start
        cpx #W_FLIP
        bne +
        jmp wd_flip
+       jsr wd_column           ; column `step`
        inc prep_step
_done:
        rts
_start:
        lda wd_y                ; where it is shown, as it
        cmp shown_y             ; is shown: nothing to do
        bne _go
        ldx #4
-       lda wd_want,x
        cmp wd_have,x
        bne _go
        dex
        bpl -
        rts
_go:
        jsr wd_patches
        lda wd_y
        sta prep_y
        jsr wd_prep
        ldx #0
        jsr wd_column
        inc prep_step
        rts

        .cerror W_FLIP != W_COLS, "a column a step"

; The patches wanted and not made yet into wd_comp: patch
; 3 k + state for port k, 12 + state for the core.
wd_patches:
        ldx #4
_one:
        lda wd_want,x
        cmp wd_have,x
        beq _next
        sta wd_have,x
        sta wd_t
        stx wd_k
        txa
        asl a
        adc wd_k                ; (C = 0)
        adc wd_t
        tay
        jsr wd_patch
        ldx wd_k
_next:
        dex
        bpl _one
        rts

; Patch Y into wd_comp: its columns one after the other.
wd_patch:
        lda wd_p_src_lo,y
        sta src
        lda wd_p_src_hi,y
        sta src + 1
        lda wd_p_dst_lo,y
        sta dst
        lda wd_p_dst_hi,y
        sta dst + 1
        lda wd_p_cols,y
        sta wd_m
        lda wd_p_lines,y
        sta wd_b
_col:
        ldy #0
-       lda (src),y
        sta (dst),y
        iny
        cpy wd_b
        bne -
        clc                     ; the next column
        lda src
        adc wd_b
        sta src
        bcc +
        inc src + 1
+       clc
        lda dst
        adc #W_STRIDE
        sta dst
        bcc +
        inc dst + 1
+       dec wd_m
        bne _col
        rts

; The body being made (prep_y): its line AND 7, 8 - that,
; its first row (the line / 8, signed), its codes over the
; nebula's rows (k from W_BAND_FROM - row0 to W_BAND_TO -
; row0, at most W_CODES).
wd_prep:
        lda prep_y
        and #%00000111
        sta wd_s
        eor #%11111111
        sec
        adc #8                  ; 8 - s
        sta wd_off
        lda prep_y
        .rept 3
        cmp #$80
        ror a
        .endrept
        sta wd_row0
        lda #W_BAND_FROM
        sec
        sbc wd_row0
        cmp #W_CODES
        bcc +
        lda #W_CODES
+       sta wd_kb0
        lda #W_BAND_TO
        sec
        sbc wd_row0
        cmp #W_CODES
        bcc +
        lda #W_CODES
+       sta wd_kb1
        rts

        .cerror W_Y_START < -128 || W_Y_START + W_LINES < 0
        .cerror W_BAND_FROM - (W_Y_START >> 3) > 127

; Column X (0-6) of the other set: its ten characters from
; wd_comp (from line 8 - s of its column, 80 lines), its
; codes' lines in the rock's table; over the nebula the
; nebula's pixels where it has none. X kept.
wd_column:
        stx wd_c
        lda wd_col_lo,x         ; src: its column + 8 - s
        clc
        adc wd_off
        sta src
        lda wd_col_hi,x
        adc #0
        sta src + 1
        lda shown_set           ; the other set's code
        eor #1
        asl a
        asl a
        asl a
        adc wd_c                ; (C = 0)
        tay
        lda wd_code,y
        tax                     ; X: the code
        lda #0                  ; dst: CHARSET + 8 code
        sta dst + 1
        txa
        .rept 3
        asl a
        rol dst + 1
        .endrept
        sta dst
        lda dst + 1
        adc #>CHARSET           ; (C = 0)
        sta dst + 1
        ldy #0
_code:
        .for wd_l in range(8)
        lda (src),y
        sta (dst),y
        sta rock_lines + wd_l * 256,x
        iny
        .endfor
        inx
        cpy #W_CODES * 8
        bne _code
        lda wd_kb0              ; over the nebula
        sta wd_k
_band:
        lda wd_k
        cmp wd_kb1
        bcs _done
        clc                     ; its row's cell kept: the
        adc wd_row0             ; code under it
        asl a
        asl a
        asl a
        ora wd_c
        tay
        lda wd_save_code,y
        ldx #0                  ; vector: CHARSET + 8 its
        stx vector + 1          ; code - 8 k (the same Y
        .rept 3                 ; for both: 8 k + line)
        asl a
        rol vector + 1
        .endrept
        sta vector
        lda wd_k
        asl a
        asl a
        asl a
        sta wd_t                ; 8 k
        lda vector
        sec
        sbc wd_t
        sta vector
        lda vector + 1
        sbc #0
        clc
        adc #>CHARSET
        sta vector + 1
        ldy wd_t
_line:
        lda (dst),y             ; the body's byte
        sta wd_b
        lsr a                   ; its pixels: 11 where it
        ora wd_b                ; has one
        and #%01010101
        sta wd_m
        asl a
        ora wd_m
        eor #%11111111          ; where it has none: the
        and (vector),y          ; nebula's
        ora wd_b
        sta (dst),y
        iny
        tya
        and #%00000111
        bne _line
        inc wd_k
        jmp _band
_done:
        ldx wd_c
        rts

        .cerror (CHARSET & $ff) != 0, "wd_column: CHARSET"
        .cerror W_ROWS * 8 > 256, "wd_save: a byte"

; The flip: the other set is made, the screen shows it
; from the next frame. Its rows (row0 to row0 + W_CODES - 1,
; on the screen: from 0, under W_ROWS) take its codes and
; its colour; the rows it showed and does not now get the
; arena's cells back.
wd_flip:
        lda shown_set
        eor #1
        sta shown_set
        lda prep_y
        sta shown_y
        lda wd_row0             ; the new rows: n0 = wd_b,
        bpl +                   ; n1 = wd_m
        lda #0
+       sta wd_b
        lda wd_row0
        clc
        adc #W_CODES
        bmi _none               ; (all above the screen)
        cmp #W_ROWS
        bcc +
        lda #W_ROWS
+       cmp wd_b
        bcs +
_none:
        lda wd_b
+       sta wd_m
        lda wd_r0               ; the old rows not covered
        sta wd_k
_old:
        lda wd_k
        cmp wd_r1
        bcs _new
        cmp wd_b
        bcc +
        cmp wd_m
        bcc _kept
+       jsr wd_restore
_kept:
        inc wd_k
        bne _old
_new:
        lda wd_b
        sta wd_r0
        sta wd_k
        lda wd_m
        sta wd_r1
_row:
        lda wd_k
        cmp wd_r1
        bcs _end
        tay
        jsr wd_ptrs
        lda wd_k                ; the code's place in the
        sec                     ; column: the row - row0
        sbc wd_row0
        sta wd_t
        lda shown_set
        asl a
        asl a
        asl a
        tax
        ldy #0
-       lda wd_code,x
        clc
        adc wd_t
        sta (src),y
        lda wd_colour
        sta (dst),y
        inx
        iny
        cpy #W_COLS
        bne -
        inc wd_k
        bne _row
_end:
        lda #0
        sta prep_step
        rts

; Row wd_k of the body's columns: the arena's cells again.
wd_restore:
        ldy wd_k
        jsr wd_ptrs
        lda wd_k
        asl a
        asl a
        asl a
        tax
        ldy #0
-       lda wd_save_code,x
        sta (src),y
        lda wd_save_col,x
        sta (dst),y
        inx
        iny
        cpy #W_COLS
        bne -
        rts

; Row Y of screen A from the body's column: src its cells,
; dst their colours.
wd_ptrs:
        lda row_lo,y
        clc
        adc #W_COL
        sta src
        sta dst
        lda row_hi,y
        adc #0
        sta src + 1
        clc
        adc #>(COLOURS - SCREEN_A)
        sta dst + 1
        rts

        .cerror (COLOURS - SCREEN_A) & $ff != 0

; Its colours (paint, boss.asm): X 0 its own, 1 white, 2
; the wreck's, in the cells it shows now (and in those the
; flips show from now).
wd_paint:
        lda wd_paints,x
        sta wd_colour
        lda wd_r0
        sta wd_k
_row:
        lda wd_k
        cmp wd_r1
        bcs _done
        tay
        jsr wd_ptrs
        lda wd_colour
        ldy #W_COLS - 1
-       sta (dst),y
        dey
        bpl -
        inc wd_k
        bne _row
_done:
        rts

; ---------------------------------------------------------
; Its turn (boss_update, after the bar's step): its parts
; for the frame after the next, its step.
; ---------------------------------------------------------

wd_step:
        lda #<W_PART_X          ; the parts' x registers:
        sta part_x              ; from the gun's (the body's
        lda #>W_PART_X          ; left edge + GUN_DX)
        sta part_x + 1
        jsr wd_place
        ldx boss_state
        lda wd_steps_lo,x
        sta vector
        lda wd_steps_hi,x
        sta vector + 1
        jmp (vector)

wd_steps_lo:
        .byte <wd_wait, <wd_enter, <wd_fight, <wd_bare
        .byte <wd_core, <wd_chain, <step_wreck, <step_clear
        .byte <step_done
wd_steps_hi:
        .byte >wd_wait, >wd_enter, >wd_fight, >wd_bare
        .byte >wd_core, >wd_chain, >step_wreck, >step_clear
        .byte >step_done

        .cerror ST_OPEN != 3 || ST_DONE != 8

; The parts alive on the body the screen will show in the
; frame after the next (the one being made if it flips in
; the next turn, else the one shown): the gun in its port,
; the core in its pit.
wd_place:
        lda shown_y
        ldx prep_step
        cpx #W_FLIP
        bne +
        lda prep_y
+       sta wd_t
        lda parts
        lsr a
        bcc +
        ldy wd_port
        lda wd_gun_dy,y
        clc
        adc wd_t
        tay
        ldx part_a
        lda #0
        jsr place_one
+       lda parts
        and #%00000100
        beq +
        lda wd_t
        clc
        adc #W_CORE_DY
        tay
        ldx part_core
        lda #W_CORE_DX
        jmp place_one
+       rts

; --- WAIT (as the engine's step_wait) --------------------
wd_wait:
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
        bcs wd_begin
        rts
_busy:
        lda #0
        sta boss_timer
        rts

; WAIT is over: the arena's cells under the body kept; rows
; 10-14 rock, the far layer's codes not; the patches all to
; make (wd_have $ff: the drawing as built); the guns' lives;
; the body above the screen, nothing of it shown; the bar;
; ENTER.
wd_begin:
        lda #0
        sta wd_k                ; the row
_row:
        ldy wd_k
        jsr wd_ptrs
        lda wd_k                ; its first cell kept: eight
        asl a                   ; places a row
        asl a
        asl a
        tax
        ldy #0
-       lda (src),y
        sta wd_save_code,x
        lda (dst),y
        and #%00001111
        sta wd_save_col,x
        inx
        iny
        cpy #W_COLS
        bne -
        inc wd_k
        lda wd_k
        cmp #W_ROWS
        bne _row
        ldx #CORRIDOR_TO - CORRIDOR_FROM - 1
-       txa                     ; rows 10-14: their rows
        clc
        adc #CORRIDOR_FROM
        lsr a
        lsr a
        lsr a
        sta rock_row + CORRIDOR_FROM,x
        dex
        bpl -
        lda #1
        sta air_rock
        ldx #W_FAR_COUNT - 1    ; the far layer's codes: not
        lda #0                  ; rock
-       ldy wd_far,x
        .for wd_l in range(8)
        sta rock_lines + wd_l * 256,y
        .endfor
        dex
        bpl -
        ldx #4                  ; the patches: all shut, to
-       lda #0                  ; make
        sta wd_want,x
        lda #$ff
        sta wd_have,x
        dex
        bpl -
        lda #W_GUN_LIFE
        ldx #3
-       sta wd_life,x
        dex
        bpl -
        lda #<W_Y_START         ; above the screen, as shown
        sta wd_y
        sta shown_y
        lda #0
        sta wd_yf
        sta shown_set
        sta prep_step
        sta wd_r0
        sta wd_r1
        sta wd_gone
        sta wd_turn
        sta wd_cycle
        sta wd_port
        sta patrol
        sta patrol_left
        sta parts
        lda #$ff
        sta part_a
        sta part_core
        lda #W_SHUT_WAIT
        sta wd_timer
        lda wd_paints
        sta wd_colour
        jsr bar_on
        lda #ST_ENTER
        sta boss_state
        rts

        .cerror CORRIDOR_FROM & 7 != 0, "its lines"
        .cerror CORRIDOR_TO - CORRIDOR_FROM > 128

; --- ENTER: it comes down to its station -----------------
wd_enter:
        clc
        lda wd_yf
        adc #W_ENTER_SPEED
        sta wd_yf
        lda wd_y
        adc #0
        sta wd_y
        bmi _on                 ; still above (signed)
        cmp #W_Y_STATION
        bcc _on
        lda #W_Y_STATION        ; there: the fight
        sta wd_y
        lda #0
        sta wd_yf
        lda #ST_FIGHT
        sta boss_state
_on:
        rts

; --- FIGHT: the ports in turn ----------------------------
; Shut: W_SHUT_WAIT frames, then the next port opens (its
; gun a free Varkon; none: a frame later), its gun's life
; as it was. Open: its gun fires its fans; destroyed, the
; port is broken off (two shards from it) and the next one
; waits; W_OPEN_FRAMES frames, the gun goes back in, the
; port shuts. All four destroyed: the core's step.
wd_fight:
        jsr wd_patrol
        lda wd_cycle
        bne _open
        dec wd_timer
        beq +
_bar:
        jmp wd_bar
+       jsr free_varkon
        bcc +
        inc wd_timer            ; none: next frame
        bne _bar
+       stx part_a
        ldy #KIND_WGUN
        jsr new_part
        ldy wd_turn
        lda wd_order,y
        sta wd_port
        tay
        lda wd_life,y
        sta en_life,x
        lda #W_FAN_FIRST
        sta en_fire,x
        lda #0
        sta en_aim,x
        lda #1                  ; its port open
        sta wd_want,y
        sta wd_cycle
        lda parts
        ora #%00000001
        sta parts
        lda #W_OPEN_FRAMES
        sta wd_timer
        jsr wd_place
        jmp _bar
_open:
        ldx part_a
        lda en_on,x
        cmp #FLYING
        beq _alive
        jsr split               ; destroyed: two shards,
        ldy wd_port             ; the port broken off
        lda #2
        sta wd_want,y
        lda #0
        sta wd_life,y
        lda wd_gone
        ora wd_bit,y
        sta wd_gone
        lda #FX_EXPLODE
        jsr sfx_start
        jmp _next
_alive:
        ldy wd_port             ; its life, for the bar and
        lda en_life,x           ; for later
        sta wd_life,y
        dec en_fire,x           ; its fan
        bne +
        jsr wd_fan
+       dec wd_timer
        beq +
        jmp wd_bar
+       lda #0                  ; its time: back in, the
        sta en_on,x             ; port shut
        ldy wd_port
        sta wd_want,y
_next:
        lda #$ff
        sta part_a
        lda parts
        and #%11111110
        sta parts
        lda #0
        sta wd_cycle
        lda #W_SHUT_WAIT
        sta wd_timer
        lda wd_gone
        cmp #%00001111
        beq _bare
        ldy wd_turn             ; the next port left
-       iny
        tya
        and #%00000011
        tay
        ldx wd_order,y
        lda wd_gone
        and wd_bit,x
        bne -
        sty wd_turn
        jmp wd_bar
_bare:
        lda #ST_OPEN            ; all four: the core's pit
        sta boss_state          ; opens after a while
        lda #W_CORE_WAIT
        sta wd_timer
        jmp wd_bar

; Gun X's fan: aimed up at the ship above it (the SHIELD
; CORE's low pod's fans), else down or left (the top
; pod's); W_FAN_PERIOD frames to the next. X kept.
wd_fan:
        jsr aim_one
        ldy #POD_FAN_FIRST
        lda en_aim,x
        bne +
        jsr aim_top
        ldy #POD_FAN_FIRST + 9
+       jsr fan_pod
        lda #W_FAN_PERIOD
        sta en_fire,x
        rts

; --- BARE (ST_OPEN): no port left -----------------------
; W_CORE_WAIT frames, then the core in a free Varkon (none:
; a frame later): its pit open, its first shot, the core's
; patrol, its shards' time; the core's fight.
wd_bare:
        jsr wd_patrol
        dec wd_timer
        bne _bar
        jsr free_varkon
        bcc +
        inc wd_timer
_bar:
        jmp wd_bar
+       stx part_core
        ldy #KIND_WCORE
        jsr new_part
        lda #W_CORE_FIRST
        sta en_fire,x
        lda #1
        sta wd_want + 4
        lda parts
        ora #%00000100
        sta parts
        lda #2
        sta patrol
        lda #0
        sta patrol_left
        lda #W_SHED_EVERY
        sta wd_shed
        lda #ST_CORE
        sta boss_state
        jsr wd_place
        jmp wd_bar

; --- CORE: the core's fight ------------------------------
; Destroyed: the end (the engine's boss_dies, then
; wd_chain). Under RAGE_LIFE: its shots RAGE_PERIOD apart.
; Every W_SHED_EVERY frames two shards from it.
wd_core:
        ldx part_core
        lda en_on,x
        cmp #FLYING
        beq +
        jmp boss_dies
+       lda en_life,x
        cmp #W_RAGE_LIFE + 1
        bcs +
        lda #W_RAGE_PERIOD
        sta en_period,x
+       dec wd_shed
        bne +
        lda #W_SHED_EVERY
        sta wd_shed
        jsr split
+       jsr wd_patrol
        jmp wd_bar

; The bar's steps by the life left: the guns' (0 the ports
; destroyed), the core's (all of it before it comes).
wd_bar:
        lda wd_life
        clc
        adc wd_life + 1
        adc wd_life + 2
        adc wd_life + 3
        sta wd_t
        lda #W_CORE_LIFE
        ldx part_core
        cpx #$ff
        beq +
        lda en_life,x
+       clc
        adc wd_t
        tax
        lda wd_bar_of,x
        sta bar_want
        rts

        .cerror 4 * W_GUN_LIFE + W_CORE_LIFE > 255

; The patrol (its entry: patrol, 0-1 the ports' fight, 2-3
; the core's): wait at a line, then to the other of its two
; at its speed; there, its wait. (As patrol_step, up and
; down: lines W_Y_TOP-W_Y_LOW, under 128.)
wd_patrol:
        lda patrol_left
        beq +
        dec patrol_left
        rts
+       ldx patrol
        lda wd_y
        cmp wd_patrol_to,x
        bcc _down
        bne _up
        lda wd_yf
        beq _there
_up:
        sec
        lda wd_yf
        sbc wd_patrol_speed,x
        sta wd_yf
        lda wd_y
        sbc #0
        sta wd_y
        cmp wd_patrol_to,x
        bcs _done
        bcc _there
_down:
        clc
        lda wd_yf
        adc wd_patrol_speed,x
        sta wd_yf
        lda wd_y
        adc #0
        sta wd_y
        cmp wd_patrol_to,x
        bcc _done
_there:
        lda wd_patrol_to,x
        sta wd_y
        lda #0
        sta wd_yf
        lda wd_patrol_wait,x
        sta patrol_left
        txa
        eor #1
        sta patrol
_done:
        rts

; --- CHAIN: as the engine's step_chain, on the body -------
; Every CHAIN_EVERY frames a fireball (a free Varkon
; exploding; none free: none) at wd_chain_dx from part_x,
; wd_chain_y from the body's top line; its sound, the body
; white for a moment.
wd_chain:
        inc boss_timer
        lda boss_timer
        cmp #CHAIN_EVERY
        bcc _done
        lda #0
        sta boss_timer
        jsr free_varkon
        bcs _next
        lda #2
        jsr set_pri
        lda #BOOM
        sta en_on,x
        lda #KIND_WCORE
        sta en_kind,x
        lda #BOSS
        sta en_beh,x
        lda #0
        sta en_left,x
        sta en_flash,x
        sta en_cap,x
        sta en_xf,x
        ldy chain_k
        lda wd_chain_y,y
        clc
        adc shown_y
        sta en_y,x
        lda wd_chain_dx,y
        clc
        adc part_x
        sta en_x,x
        lda part_x + 1
        adc #0
        sta en_xh,x
_next:
        lda #FX_EXPLODE
        jsr sfx_start
        lda #3
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

; ---------------------------------------------------------
; Its data (game/assets/build_assets.py), then its space.
; ---------------------------------------------------------

        .include "../assets/generated/warden_data.inc"
wd_data_end:                     ; the file's end; after it
wd_save_code = wd_data_end      ; the arena's cells under
wd_save_col = wd_save_code + W_ROWS * 8 ; the body: codes,
W_END    = wd_save_col + W_ROWS * 8 ; colours (8 a row)
        .cerror W_END > $fffa, "the WARDEN past $fffa"
