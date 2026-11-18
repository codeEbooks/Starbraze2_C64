; The VARKON CORVETTE, the boss of level 4
; (game/assets/corvette.py). The level plan (§2): a great
; ship that comes in from the right and stops in the middle
; of the screen; turrets on its flanks to destroy, then the
; bridge; it launches scouts from its hangar. The author's
; decisions (23 October): «Torrette, poi il ponte», «Avanti
; e indietro, lenta», «Un po' più del WARDEN», «Roccia come
; il WARDEN».
;
; Assembled by itself at WARDEN_AT (from $f000, RAM under
; the KERNAL), after the program, whose labels it reads
; (game/build/main.inc); level 4's file (LEVEL4) brings
; it, a record after the store's (tools/make_disk.py), as
; level 3's brings the WARDEN. The program comes here
; through the jumps at its start: boss_draw's (the body),
; boss_update's (its steps), paint's (its colours).
;
; The engine is boss.asm's: the bar, the white flash, the
; wreck, STAGE CLEAR. Here the CORVETTE's own:
;  - the body: 12 columns x 40 lines of characters on rows
;    8-12, its left edge at cv_x (multicolour pixels from
;    the screen's left: column x / 4, phase x AND 3). Its
;    drawing comes in four phases, shifted right by 0-3
;    pixels, 13 columns of 40 lines each: phase 0 in the
;    file (cv_comp), phases 1-3 made from it in the arena's
;    WAIT (cv_make, a column a turn, at CV_PHASES);
;  - a new body: a phase's columns, one a turn (two while
;    it comes in: no Varkon then, the frame has time),
;    into the set of characters the screen does not show
;    (its codes cell by cell: cv_code, a row after the
;    other; where each goes in the characters: cv_dlo,
;    cv_dhi) and into the rock's table (it is rock); over
;    the far layer
;    (rows 10-12) the cells with empty pixels where the far
;    layer has pixels (cv_mask) take them there; then the
;    flip: screen A's cells take that set, the columns it
;    leaves get the arena's cells back (kept at the start:
;    cv_save_code, cv_save_col);
;  - rows 10-14 are rock while it is there (as for the
;    WARDEN: rock_row, air_rock; the far layer's codes out
;    of the rock's table): boss_reset puts them back;
;  - it moves a step at a new body (cv_toward): in from the
;    right, then back and forth in the arena's right half;
;  - at its station the two turrets of its deck come on
;    (Varkon of kind CTURRET: parts bit 0), both destroyed
;    the two under its keel (two at a time: four made turns
;    of 20 000 cycles), and fire their fans; its hangar
;    launches scouts; all four destroyed, the bridge's dome
;    (part_core, parts bit 2) comes on the
;    tower and fires at the ship, under half its life
;    faster; destroyed, the engine's end (boss_dies), its
;    chain on the body (cv_chain).

        .include "main.inc"     ; (-I its build)
        .include "../assets/generated/corvette.inc"

; Its variables, where the SHIELD CORE's are (page 2, 0 at
; the level's start: boss_reset), and the engine's own ones
; with its meaning.
cv_x     = body_x               ; its left edge
cv_gone  = cb_angle             ; the turrets destroyed
cv_part  = cv_gone + 1          ; 4: the turrets' Varkon
cv_live  = cv_part + 4          ; those on and not destroyed
cv_pair  = cv_live + 1          ; 0 the deck's, 1 the wait,
cv_c0    = cv_pair + 1          ; 2 the keel's; the columns
                                ; shown: c0 to
cv_c1    = cv_c0 + 1            ; c1 - 1
cv_mode  = cv_c1 + 1            ; its colours: 0 own, 1
cv_made  = cv_mode + 1          ; white, 2 the wreck's; the
cv_mp    = cv_made + 1          ; phases' columns made, the
cv_mc    = cv_mp + 1            ; phase (- 1), the column
cv_pp    = cv_mc + 1            ; the body being made: its
cv_pc0   = cv_pp + 1            ; phase, first column, its
cv_pm    = cv_pc0 + 1           ; masks (13 phase), its
cv_base  = cv_pm + 1            ; drawing (2 bytes)
cv_ci    = cv_base + 2          ; scratch: a code's place,
cv_c     = cv_ci + 1            ; a column, a row,
cv_r     = cv_c + 1
cv_s     = cv_r + 1             ; a row's place in the save
cv_k     = cv_s + 1             ; and four more
cv_t     = cv_k + 1
cv_b     = cv_t + 1
cv_m     = cv_b + 1
cv_mk    = cv_m + 1             ; a column's masks
cv_n0    = cv_mk + 1            ; the flip: the columns of
cv_n1    = cv_n0 + 1            ; the new body (n0 to n1 -
cv_ra0   = cv_n1 + 1            ; 1); the old ones left (ra0
cv_ra1   = cv_ra0 + 1           ; to ra1 - 1, rb0 to rb1 -
cv_rb0   = cv_ra1 + 1           ; 1); the new ones (na0 to
cv_rb1   = cv_rb0 + 1           ; na1 - 1, nb0 to nb1 - 1)
cv_na0   = cv_rb1 + 1
cv_na1   = cv_na0 + 1
cv_nb0   = cv_na1 + 1
cv_nb1   = cv_nb0 + 1
CV_VARS_END = cv_nb1 + 1
        .cerror CV_VARS_END > CB_SAVE_END, "its variables"
        .cerror cv_gone != arena_chars + 1

        * = WARDEN_AT
        jmp cv_draw             ; W_DRAW
        jmp cv_step             ; W_STEP
        jmp cv_paint            ; W_PAINT
        .cerror cv_draw - WARDEN_AT != 9

CV_ALL   = 3 * CV_COLS          ; the phases' columns
CV_LAST  = 40                   ; the screen's columns
        .cerror CV_SAVE_C0 + CV_SAVE_COLS != CV_LAST

; ---------------------------------------------------------
; The body on the screen (boss_draw, a turn): nothing to
; do, or column 0 of the other set; 1; ... 12 (prep_step:
; the columns made); the flip. While it comes in (ENTER,
; no Varkon), two columns a turn: 0-1, 2-3, ... 12. (The
; fight's turns have no time for two: a first try,
; two a turn all along, made turns of 20 900 cycles.)
; ---------------------------------------------------------

cv_draw:
        lda boss_state          ; WAIT: no body yet
        beq _done
        ldx prep_step
        beq _start
        cpx #CV_COLS
        bcc _more
        jmp cv_show
_start:
        lda cv_x                ; where it is shown: nothing
        cmp shown_x             ; to do
        beq _done
        sta prep_x
        jsr cv_prep
        ldx #0
_more:
        jsr cv_column           ; column X
        inc prep_step
        lda boss_state          ; ENTER: the next one too
        cmp #ST_ENTER
        bne _done
        inx
        jsr cv_column
        inc prep_step
_done:
        rts

; The body being made (prep_x): its phase, its drawing,
; its first column, its masks' place.
cv_prep:
        lda prep_x
        and #%00000011
        sta cv_pp
        tay
        lda cv_phase_lo,y
        sta cv_base
        lda cv_phase_hi,y
        sta cv_base + 1
        lda prep_x
        lsr a
        lsr a
        sta cv_pc0
        lda cv_pp               ; 13 x the phase
        asl a
        asl a
        sta cv_t
        asl a
        adc cv_t                ; (C = 0)
        adc cv_pp
        sta cv_pm
        rts

; Column X (0-12) of the other set, if on the screen: its
; five characters from its phase (40 lines), their lines
; in the rock's table, a row after the other (unrolled:
; the frame's time); over the far layer, in the cells
; cv_mask names, the far layer's pixels where it has none
; (cv_merge). X kept.
cv_column:
        stx cv_c
        cpx #CV_COLS
        bcs _off
        txa
        clc
        adc cv_pc0
        cmp #CV_LAST
        bcc +
_off:
        rts
+       sta cv_k                ; its column on the screen
        lda cv_base             ; src: its lines
        clc
        adc cv_col_lo,x
        sta src
        lda cv_base + 1
        adc cv_col_hi,x
        sta src + 1
        txa                     ; its masks
        clc
        adc cv_pm
        tay
        lda cv_mask,y
        sta cv_mk
        lda shown_set           ; its first code's place:
        eor #1                  ; the other set's
        beq +
        lda #CV_CELLS
+       clc
        adc cv_c
        sta cv_ci
        ldy #0
        .for cv_q in range(CV_ROWS)
        ldx cv_ci               ; row cv_q: dst (CHARSET + 8
        lda cv_dlo + cv_q * CV_COLS,x   ; code - 8 row: the
        sta dst                 ; same Y for both), X its
        lda cv_dhi + cv_q * CV_COLS,x   ; code
        sta dst + 1
        lda cv_code + cv_q * CV_COLS,x
        tax
        .for cv_l in range(8)
        lda (src),y
        sta (dst),y
        sta rock_lines + cv_l * 256,x
        iny
        .endfor
        .if cv_q >= CV_BAND_ROW
        lda cv_mk               ; over the far layer?
        and #1 << (cv_q - CV_BAND_ROW)
        beq +
        ldy #8 * cv_q
        ldx #cv_q
        jsr cv_merge
+
        .fi
        .endfor
        ldx cv_c
        rts

        .cerror (CHARSET & $ff) != 0, "cv_merge: CHARSET"
        .cerror CV_ROWS * 8 > 256 || 2 * CV_CELLS > 256

; The cell just made (row X, column cv_k of the screen; Y 8
; X): where it has no pixel, the far layer's (the cell kept
; there: its code's lines; cv_inv, the body's byte's empty
; pixels). Y 8 X + 8 at the end.
cv_merge:
        sty cv_t                ; 8 row
        lda cv_k
        clc
        adc cv_srow,x
        tax
        lda cv_save_code,x
        ldx #0                  ; vector: CHARSET + 8 its
        stx vector + 1          ; code - 8 row
        .rept 3
        asl a
        rol vector + 1
        .endrept
        sec
        sbc cv_t
        sta vector
        lda vector + 1
        sbc #0
        clc
        adc #>CHARSET
        sta vector + 1
_line:
        lda (dst),y             ; the body's byte
        tax
        lda (vector),y          ; the far layer's pixels
        and cv_inv,x            ; where it has none
        sta cv_t
        txa
        ora cv_t
        sta (dst),y
        iny
        tya
        and #%00000111
        bne _line
        rts

; The flip: the other set is made, the screen shows it
; from the next frame. Its columns on the screen (n0 to
; n1 - 1) take its codes (unrolled when all 13 are on the
; screen), the new ones its colours; the columns it showed
; and does not now get the arena's cells back.
cv_show:
        lda shown_set
        eor #1
        sta shown_set
        lda prep_x
        sta shown_x
        lda cv_pc0              ; n0, n1
        sta cv_n0
        clc
        adc #CV_COLS
        cmp #CV_LAST
        bcc +
        lda #CV_LAST
+       sta cv_n1
        lda cv_c0               ; the cells left: c0 to
        sta cv_ra0              ; min(c1, n0) - 1, max(c0,
        lda cv_c1               ; n1) to c1 - 1
        sta cv_rb1
        cmp cv_n0
        bcc +
        lda cv_n0
+       sta cv_ra1
        lda cv_c0
        cmp cv_n1
        bcs +
        lda cv_n1
+       sta cv_rb0
        lda cv_n0               ; the new ones: n0 to
        sta cv_na0              ; min(n1, c0) - 1, max(n0,
        lda cv_n1               ; c1) to n1 - 1
        sta cv_nb1
        cmp cv_c0
        bcc +
        lda cv_c0
+       sta cv_na1
        lda cv_n0
        cmp cv_c1
        bcs +
        lda cv_c1
+       sta cv_nb0
        lda #0
        sta cv_r
_row:
        ldx cv_r
        jsr cv_ptrs
        ldy cv_ra0              ; the arena's cells again
-       cpy cv_ra1
        bcs +
        jsr cv_back
        iny
        bne -
+       ldy cv_rb0
-       cpy cv_rb1
        bcs +
        jsr cv_back
        iny
        bne -
+       ldx cv_r                ; its codes: X their first
        lda shown_set           ; (cv_back took X)
        beq +
        lda #CV_CELLS
+       clc
        adc cv_row13,x
        tax
        ldy cv_n0
        lda cv_n1
        sec
        sbc cv_n0
        cmp #CV_COLS
        bne _few
        .for cv_q in range(CV_COLS)
        lda cv_code + cv_q,x
        sta (src),y
        iny
        .endfor
        jmp _colours
_few:
-       cpy cv_n1
        bcs _colours
        lda cv_code,x
        sta (src),y
        inx
        iny
        bne -
_colours:
        jsr cv_colour           ; the new columns' colour
        lda cv_t
        ldy cv_na0
-       cpy cv_na1
        bcs +
        sta (dst),y
        iny
        bne -
+       ldy cv_nb0
-       cpy cv_nb1
        bcs +
        sta (dst),y
        iny
        bne -
+       inc cv_r
        lda cv_r
        cmp #CV_ROWS
        beq +
        jmp _row
+       lda cv_n0
        sta cv_c0
        lda cv_n1
        sta cv_c1
        lda #0
        sta prep_step
        rts

; Cell Y of the row cv_ptrs set: the arena's again. Y kept.
cv_back:
        tya
        clc
        adc cv_s
        tax
        lda cv_save_code,x
        sta (src),y
        lda cv_save_col,x
        sta (dst),y
        rts

; Row X of the body (screen row CV_ROW0 + X): src its
; cells, dst their colours, cv_s its place in the save
; (- CV_SAVE_C0). X kept.
cv_ptrs:
        lda row_lo + CV_ROW0,x
        sta src
        sta dst
        lda row_hi + CV_ROW0,x
        sta src + 1
        clc
        adc #>(COLOURS - SCREEN_A)
        sta dst + 1
        lda cv_srow,x
        sta cv_s
        rts

        .cerror (COLOURS - SCREEN_A) & $ff != 0

; The colour of row cv_r: cv_t (cv_mode's). X kept.
cv_colour:
        lda cv_mode
        asl a
        asl a
        adc cv_mode             ; (C = 0)
        adc cv_r
        tay
        lda cv_paints,y
        sta cv_t
        rts

; Its colours (paint, boss.asm): X 0 its own, 1 white, 2
; the wreck's, in the cells it shows now (and in those the
; flips show from now).
cv_paint:
        stx cv_mode
        lda #0
        sta cv_r
_row:
        ldx cv_r
        jsr cv_ptrs
        jsr cv_colour
        lda cv_t
        ldy cv_c0
-       cpy cv_c1
        bcs +
        sta (dst),y
        iny
        bne -
+       inc cv_r
        lda cv_r
        cmp #CV_ROWS
        bne _row
        rts

; ---------------------------------------------------------
; Its turn (boss_update, after the bar's step): its parts
; for the frame after the next, its step.
; ---------------------------------------------------------

cv_step:
        jsr cv_partx
        jsr cv_place
        ldx boss_state
        lda cv_steps_lo,x
        sta vector
        lda cv_steps_hi,x
        sta vector + 1
        jmp (vector)

cv_steps_lo:
        .byte <cv_wait, <cv_enter, <cv_fight, <cv_open
        .byte <cv_core, <cv_chain, <step_wreck, <step_clear
        .byte <step_done
cv_steps_hi:
        .byte >cv_wait, >cv_enter, >cv_fight, >cv_open
        .byte >cv_core, >cv_chain, >step_wreck, >step_clear
        .byte >step_done

        .cerror ST_OPEN != 3 || ST_DONE != 8

; part_x: the x register of the body's left edge (2 x +
; 24) the screen will show in the frame after the next
; (the one being made if it flips in the next turn: its
; columns made, else the one shown).
cv_partx:
        lda shown_x
        ldx prep_step
        cpx #CV_COLS
        bcc +
        lda prep_x
+       asl a
        sta part_x
        lda #0
        rol a
        sta part_x + 1
        lda part_x
        clc
        adc #24
        sta part_x
        bcc +
        inc part_x + 1
+       rts

; Its parts alive on it: the turrets on their mounts, the
; dome on the tower.
cv_place:
        lda boss_state
        beq _done               ; (WAIT: none yet)
        cmp #ST_CHAIN
        bcs _done
        lda parts               ; the turrets on?
        lsr a
        bcc _dome
        ldy #3
_one:
        lda cv_live
        and cv_bit,y
        beq _next
        sty cv_k
        ldx cv_part,y
        lda cv_turret_y,y
        pha
        lda cv_turret_dx,y
        tay
        pla
        jsr cv_set
        ldy cv_k
_next:
        dey
        bpl _one
_dome:
        lda parts
        and #%00000100
        beq _done
        ldx part_core
        ldy #CV_BRIDGE_DX
        lda #CV_BRIDGE_Y
        jmp cv_set
_done:
        rts

; Varkon X at part_x + Y (its x register), line A.
cv_set:
        sta en_y,x
        tya
        jmp place_one_x

; As place_one (boss.asm), the line already set.
place_one_x:
        clc
        adc part_x
        sta en_x,x
        lda part_x + 1
        adc #0
        sta en_xh,x
        lda #0
        sta en_xf,x
        rts

; --- WAIT (as the engine's step_wait) --------------------
; Its phases are made meanwhile, a column a turn: WAIT ends
; when they are made and no Varkon flies or explodes for
; ARENA_WAIT frames.
cv_wait:
        jsr cv_make
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
        bcc _done
        lda cv_made
        cmp #CV_ALL
        bcs cv_begin
_done:
        rts
_busy:
        lda #0
        sta boss_timer
        rts

; A column of phases 1-3 (cv_mp + 1, cv_mc): phase 0's,
; shifted right by 2 (cv_mp + 1) bits, the column before
; it bringing its pixels in.
cv_make:
        lda cv_made
        cmp #CV_ALL
        bcs _done
        ldx cv_mc
        lda #<cv_comp           ; src: its column in phase 0
        clc
        adc cv_col_lo,x
        sta src
        lda #>cv_comp
        adc cv_col_hi,x
        sta src + 1
        lda src                 ; vector: the one before
        sec
        sbc #CV_LINES
        sta vector
        lda src + 1
        sbc #0
        sta vector + 1
        ldy cv_mp               ; dst: in its phase
        lda cv_phase_lo + 1,y
        clc
        adc cv_col_lo,x
        sta dst
        lda cv_phase_hi + 1,y
        adc cv_col_hi,x
        sta dst + 1
        tya
        asl a
        adc #2                  ; (C = 0) the bits
        sta cv_b
        ldy #0
_line:
        lda cv_mc               ; the column before (none
        beq +                   ; for the first)
        lda (vector),y
+       sta cv_t
        lda (src),y
        ldx cv_b
-       lsr cv_t
        ror a
        dex
        bne -
        sta (dst),y
        iny
        cpy #CV_LINES
        bne _line
        inc cv_made
        inc cv_mc
        lda cv_mc
        cmp #CV_COLS
        bcc _done
        lda #0
        sta cv_mc
        inc cv_mp
_done:
        rts

; WAIT is over: the arena's cells under its way kept; rows
; 10-14 rock, the far layer's codes not; the body at the
; right, off the screen, nothing of it shown; the bar;
; ENTER.
cv_begin:
        lda #0                  ; the cells kept
        sta cv_r
_row:
        ldx cv_r
        jsr cv_ptrs
        ldy #CV_SAVE_C0
-       tya
        clc
        adc cv_s
        tax
        lda (src),y
        sta cv_save_code,x
        lda (dst),y
        and #%00001111
        sta cv_save_col,x
        iny
        cpy #CV_LAST
        bne -
        inc cv_r
        lda cv_r
        cmp #CV_ROWS
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
        ldx #CV_FAR_COUNT - 1   ; the far layer's codes: not
        lda #0                  ; rock
-       ldy cv_far,x
        .for cv_l in range(8)
        sta rock_lines + cv_l * 256,y
        .endfor
        dex
        bpl -
        lda #CV_X_START         ; at the right, as shown
        sta cv_x
        sta shown_x
        sta prep_x
        lda #0
        sta body_xf
        sta shown_set
        sta prep_step
        sta cv_mode
        sta cv_gone
        sta patrol
        sta patrol_left
        sta parts
        sta drone_turn
        lda #CV_LAST
        sta cv_c0
        sta cv_c1
        lda #$ff
        sta part_core
        jsr bar_on
        lda #ST_ENTER
        sta boss_state
        jsr cv_partx
        jmp cv_place

        .cerror CORRIDOR_FROM & 7 != 0, "its lines"
        .cerror CORRIDOR_TO - CORRIDOR_FROM > 128

; --- ENTER: in from the right to its station -------------
; There, the turrets in four free Varkon (else a frame
; later), their first fans; the hangar's first scout; the
; fight.
cv_enter:
        lda #CV_X_STATION
        ldy #CV_ENTER_STEP
        jsr cv_toward
        bcc _done
        ldy #0                  ; the deck's pair (else a
        jsr cv_pair_on          ; frame later)
        bcs _done
        lda #%00000001
        sta parts
        lda #CV_LAUNCH_FIRST
        sta mouth_timer
        lda #0
        sta patrol
        sta patrol_left
        lda #ST_FIGHT
        sta boss_state
        jsr cv_place
        jmp cv_bar
_done:
        rts

; A pair of turrets on (Y 0: the deck's, 2: the keel's) in
; two free Varkon, their first fans: C = 0; not two free:
; none, C = 1.
cv_pair_on:
        sty cv_k
        ldy #0                  ; two free Varkon?
        ldx #ENEMIES - 1
-       lda en_on,x
        bne +
        iny
+       dex
        bpl -
        cpy #2
        bcc _none
        ldy cv_k
        jsr _one
        ldy cv_k
        iny
_one:
        sty cv_k
        jsr free_varkon
        txa
        ldy cv_k
        sta cv_part,y
        lda cv_live
        ora cv_bit,y
        sta cv_live
        ldy #KIND_CTURRET
        jsr new_part
        lda #0
        sta en_aim,x
        ldy cv_k
        lda cv_fan_first,y
        sta en_fire,x
        clc
        rts
_none:
        sec
        rts

        .cerror ENEMIES < 2, "two turrets"

; --- FIGHT: the turrets ----------------------------------
; Its patrol, the turrets' fans, the hangar's scouts; the
; deck's two destroyed: CV_PAIR_WAIT frames, then the
; keel's two (two free Varkon: else a frame later); the
; four destroyed: the bridge's wait (ST_OPEN).
cv_fight:
        jsr cv_turrets
        lda cv_gone
        cmp #%00001111
        bne +
        lda parts               ; (the turrets off)
        and #%11111110
        sta parts
        lda #CV_BRIDGE_WAIT
        sta boss_timer
        lda #ST_OPEN
        sta boss_state
        jmp cv_bar
+       lda cv_pair             ; the pairs
        bne _wait
        lda cv_gone             ; the deck's both gone: the
        and #%00000011          ; wait
        cmp #%00000011
        bne _fight
        inc cv_pair
        lda #CV_PAIR_WAIT
        sta boss_timer
        bne _fight
_wait:
        cmp #1
        bne _fight
        dec boss_timer
        bne _fight
        ldy #2                  ; the keel's
        jsr cv_pair_on
        bcc +
        inc boss_timer          ; (none: a frame later)
        bne _fight
+       inc cv_pair
        jsr cv_place
_fight:
        jsr cv_patrol
        jsr cv_fans
        jsr cv_hangar
        jmp cv_bar

; The turrets destroyed this frame (their Varkon not
; flying: exploding) into cv_gone, out of cv_live.
cv_turrets:
        ldy #3
_one:
        lda cv_live
        and cv_bit,y
        beq _next
        ldx cv_part,y
        lda en_on,x
        cmp #FLYING
        beq _next
        lda cv_gone
        ora cv_bit,y
        sta cv_gone
        lda cv_live
        eor cv_bit,y
        sta cv_live
_next:
        dey
        bpl _one
        rts

; Each turret left: its fan when its time comes.
cv_fans:
        ldy #3
_one:
        lda cv_live
        and cv_bit,y
        beq _next
        sty cv_k
        ldx cv_part,y
        dec en_fire,x
        bne +
        jsr cv_fan
+       ldy cv_k
_next:
        dey
        bpl _one
        rts

; Turret X's fan: aimed up at the ship above it (the SHIELD
; CORE's low pod's fans), else down or left (the top
; pod's); CV_FAN_PERIOD frames to the next. X kept.
cv_fan:
        jsr aim_one
        ldy #POD_FAN_FIRST
        lda en_aim,x
        bne +
        jsr aim_top
        ldy #POD_FAN_FIRST + 9
+       jsr fan_pod
        lda #CV_FAN_PERIOD
        sta en_fire,x
        rts

; The hangar: every CV_LAUNCH_EVERY frames a scout (a free
; Varkon; none, or CV_SCOUTS_MAX scouts flying: none), its
; path up or low in turn, its sound.
cv_hangar:
        dec mouth_timer
        bne _none
        lda #CV_LAUNCH_EVERY
        sta mouth_timer
        ldy #0                  ; the scouts flying
        ldx #ENEMIES - 1
-       lda en_on,x
        cmp #FLYING
        bne +
        lda en_kind,x
        cmp #KIND_SCOUT
        bne +
        iny
+       dex
        bpl -
        cpy #CV_SCOUTS_MAX
        bcs _none
        jsr free_varkon
        bcs _none
        ldy #KIND_SCOUT
        jsr new_part
        lda #CV_HANGAR_Y
        sta en_y,x
        lda #CV_HANGAR_DX
        jsr place_one_x
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

; --- OPEN: the turrets gone, the bridge's wait -----------
; CV_BRIDGE_WAIT frames, then the dome in a free Varkon
; (none: a frame later): its first shot, the bridge's
; patrol (faster); the bridge's fight.
cv_open:
        jsr cv_patrol
        jsr cv_hangar
        dec boss_timer
        bne _bar
        jsr free_varkon
        bcc +
        inc boss_timer
_bar:
        jmp cv_bar
+       stx part_core
        ldy #KIND_CBRIDGE
        jsr new_part
        lda #CV_BRIDGE_FIRST
        sta en_fire,x
        lda parts
        ora #%00000100
        sta parts
        lda #2
        sta patrol
        lda #0
        sta patrol_left
        lda #ST_CORE
        sta boss_state
        jsr cv_place
        jmp cv_bar

; --- CORE: the bridge's fight ----------------------------
; The dome destroyed: the end (the engine's boss_dies, then
; cv_chain). Under CV_RAGE_LIFE: its shots CV_RAGE_PERIOD
; apart.
cv_core:
        ldx part_core
        lda en_on,x
        cmp #FLYING
        beq +
        jmp boss_dies
+       lda en_life,x
        cmp #CV_RAGE_LIFE + 1
        bcs +
        lda #CV_RAGE_PERIOD
        sta en_period,x
+       jsr cv_patrol
        jsr cv_hangar
        jmp cv_bar

; The bar's steps by the life left: the turrets' (0 the
; ones destroyed, all of it the keel's before they come),
; the dome's (all of it before it comes).
cv_bar:
        lda #0
        sta cv_t
        ldy #3
_one:
        lda cv_gone
        and cv_bit,y
        bne _next
        lda cv_live
        and cv_bit,y
        bne _on
        lda #CV_TURRET_LIFE     ; not on yet: all its life
        bne _add
_on:
        ldx cv_part,y
        lda en_life,x
_add:
        clc
        adc cv_t
        sta cv_t
_next:
        dey
        bpl _one
        lda #CV_BRIDGE_LIFE
        ldx part_core
        cpx #$ff
        beq +
        lda en_life,x
+       clc
        adc cv_t
        tax
        lda cv_bar_of,x
        sta bar_want
        rts

        .cerror 4 * CV_TURRET_LIFE + CV_BRIDGE_LIFE > 255
        .cerror CV_TURRET_LIFE == 0 || CV_PAIR_WAIT == 0

; The patrol (its entry: patrol, 0-1 the turrets' fight,
; 2-3 the bridge's): wait at a place, then to the other of
; its two, a step at a new body; there, its wait.
cv_patrol:
        lda patrol_left
        beq +
        dec patrol_left
        rts
+       ldx patrol
        lda cv_patrol_to,x
        ldy cv_patrol_step,x
        jsr cv_toward
        bcc _done
        ldx patrol
        lda cv_patrol_wait,x
        sta patrol_left
        txa
        eor #1
        sta patrol
_done:
        rts

; A step to x = A, Y pixels at most, when the body is
; shown where it is (none being made): C = 1 if it is
; there already (shown there), else C = 0. X kept.
cv_toward:
        sta cv_t
        sty cv_b
        lda prep_step
        bne _busy
        lda cv_x
        cmp shown_x
        bne _busy
        cmp cv_t
        beq _there
        bcc _right
        sbc cv_t                ; (C = 1) to the left
        cmp cv_b
        bcc _to
        beq _to
        lda cv_x
        sbc cv_b                ; (C = 1)
        sta cv_x
_busy:
        clc
        rts
_right:
        lda cv_t
        sec
        sbc cv_x
        cmp cv_b
        bcc _to
        beq _to
        lda cv_x
        clc
        adc cv_b
        sta cv_x
        clc
        rts
_to:
        lda cv_t
        sta cv_x
        clc
        rts
_there:
        sec
        rts

; --- CHAIN: as the engine's step_chain, on the body -------
; Every CHAIN_EVERY frames a fireball (a free Varkon
; exploding; none free: none) at cv_chain_dx from part_x,
; on line cv_chain_y; its sound, the body white for a
; moment.
cv_chain:
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
        lda #KIND_CBRIDGE
        sta en_kind,x
        lda #BOSS
        sta en_beh,x
        lda #0
        sta en_left,x
        sta en_flash,x
        sta en_cap,x
        ldy chain_k
        lda cv_chain_y,y
        sta en_y,x
        lda cv_chain_dx,y
        jsr place_one_x
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
; Its tables, its data (game/assets/build_assets.py), then
; its space.
; ---------------------------------------------------------

cv_col_lo:                      ; a column's place in a
        .for cv_l in range(CV_COLS)     ; phase
        .byte <(cv_l * CV_LINES)
        .endfor
cv_col_hi:
        .for cv_l in range(CV_COLS)
        .byte >(cv_l * CV_LINES)
        .endfor
cv_srow:                        ; a row's place in the save
        .for cv_l in range(CV_ROWS)     ; (- CV_SAVE_C0)
        .byte (cv_l * CV_SAVE_COLS - CV_SAVE_C0) & $ff
        .endfor
cv_row13:                       ; a row's first code's
        .for cv_l in range(CV_ROWS)     ; place in a set
        .byte cv_l * CV_COLS
        .endfor
        .cerror CV_BAND_ROW + 3 != CV_ROWS
        .cerror CV_BAND_ROWS != 3
        .cerror CV_LINES != 8 * CV_ROWS

        .include "../assets/generated/corvette_data.inc"
CV_END:                         ; the file's end
        .cerror CV_END > $fffa, "the CORVETTE past $fffa"

; The arena's cells under its way (codes, colours), after
; its phases (RAM under the KERNAL, free in level 4: its
; store ends before CV_PHASES, build_assets.py's check).
cv_save_code = CV_PHASES + 3 * CV_PHASE_BYTES
cv_save_col = cv_save_code + CV_ROWS * CV_SAVE_COLS
CV_SAVE_END = cv_save_col + CV_ROWS * CV_SAVE_COLS
        .cerror CV_SAVE_END > WARDEN_AT, "its save"
        .cerror CV_ROWS * CV_SAVE_COLS > 256
