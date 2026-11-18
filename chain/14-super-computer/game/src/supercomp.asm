; The SUPER-COMPUTER VARKON, the boss of level 6
; (game/assets/supercomp.py). The level plan (§2): the
; fleet's brain, kept by three rings that turn, each with a
; gap; three phases: the rings, the core's defences, the
; core uncovered. The author's decisions (29 October): «Uno
; alla volta, da fuori», «Torrette che escono a turno»,
; «Ventaglio che ruota», «Il più difficile del gioco».
;
; Assembled by itself (game/build/supercomp.bin) after
; the program, whose labels it reads (game/build/main.inc):
; its data from SC_AT (after the station's module, under
; the KERNAL), its code from WARDEN_AT with the jumps there
; (W_DRAW, W_STEP, W_PAINT), then the rest of its data;
; level 6's file (LEVEL6) brings it, a record after the
; store's and the station's module (tools/make_disk.py).
;
; The engine is boss.asm's: the bar, the white flash, the
; wreck, STAGE CLEAR. Here the SUPER-COMPUTER's own:
;  - the housing: its computer banks, 5 columns x 17 rows
;    of characters (columns 35-39, rows 2-18), rock; in
;    ENTER it closes in, a row a turn, from the ceiling and
;    the floor; its lights in turn (sc_light, a step every
;    SC_LIGHT_EVERY frames);
;  - the area: the cells (columns 25-32, rows 6-14) of the
;    rings waiting in characters, of the core's shell and
;    of the back plate behind them: 17 elements (the middle
;    ring's 8 segments, the inner one's 8, the shell), each
;    shown or not (sc_shown; wanted: less the gaps, sc_want;
;    drawn: sc_have, an element a turn); a cell's code by
;    the state of the elements it touches (sc_d_*): only the
;    rings' and the shell's pixels are rock (a code's rock:
;    its pixels AND its mask, sc_mask);
;  - rows 10-14 rock while it is there (rock_row, air_rock;
;    the far layer's codes out of the rock's table);
;  - FIGHT: the ring whose turn it is turns (sc_ang, 256 a
;    turn), its plates (free Varkon of its kind: the outer
;    one's KIND_SEGMENT, which stops even a laser) placed
;    each frame around the core; the rings waiting leave out
;    the segment where its gap is: the gaps in a line; while
;    they face the ship (left), the core's shot through them
;    every sc_every frames (sc_shoot). The last plate gone,
;    the next ring's segments go, its plates come there,
;    turning the other way, faster; the inner ring's gone:
;  - OPEN, the defences: two pairs of turrets in turn out of
;    the core (sc_slide), their fans aimed at the ship
;    (sc_aim: 16 ways), back in (their lives kept); all four
;    destroyed, the shell opens, the core (part_core) comes:
;  - CORE: its fan of three turns, a way back every
;    SC_TURN_EVERY frames, fired every SC_FAN_EVERY frames
;    while it is towards the left (fewer under half its
;    life, and its colour); destroyed, the engine's end
;    (boss_dies), its chain on it (sc_chain).

        .include "main.inc"     ; (-I its build)
        .include "../assets/generated/supercomp.inc"

; Its variables, where the SHIELD CORE's are (page 2, 0 at
; the level's start: boss_reset).
sc_ring  = cb_angle             ; the ring whose turn it is
                                ; (3: none, the defences)
sc_ang   = sc_ring + 1          ; 2: its angle (256ths, the
                                ; angle: 256 a turn)
sc_pv    = sc_ang + 2           ; its plates' Varkon, by
                                ; place ($ff: none)
sc_shown = sc_pv + SC_MOST    ; 3: the elements shown,
sc_want  = sc_shown + 3         ; 3: wanted (less the gaps),
sc_have  = sc_want + 3          ; 3: drawn
sc_hrows = sc_have + 3          ; ENTER: the housing's rows
sc_hdrawn = sc_hrows + 1        ; wanted, drawn
sc_arows = sc_hdrawn + 1        ; the area's rows wanted,
sc_adrawn = sc_arows + 1        ; drawn
sc_made  = sc_adrawn + 1        ; WAIT: its codes, pictures
sc_estep = sc_made + 1          ; ENTER's step
sc_count = sc_estep + 1         ; ENTER: elements, plates
sc_cyc   = sc_count + 1         ; FIGHT: 1 the next ring
                                ; coming; OPEN: the cycle
sc_fire  = sc_cyc + 1           ; frames to the core's shot
sc_light = sc_fire + 1          ; the lights' step,
sc_lshown = sc_light + 1        ; drawn
sc_mode  = sc_lshown + 1        ; its colours: 0 own, 1
                                ; white, 2 the wreck's
sc_pair  = sc_mode + 1          ; the pair of turrets
sc_slide = sc_pair + 1          ; their way out
sc_tv    = sc_slide + 1         ; 4: the turrets' Varkon
sc_tlife = sc_tv + 4            ; 4: their lives
sc_tlive = sc_tlife + 4         ; on the screen (bits)
sc_tgone = sc_tlive + 1         ; destroyed (bits)
sc_way   = sc_tgone + 1         ; the core's fan's way
sc_wt    = sc_way + 1           ; frames to its next way
sc_ft    = sc_wt + 1            ; frames to its next fan
sc_di    = sc_ft + 1            ; the area's cells to draw:
sc_dn    = sc_di + 1            ; the next (sc_lists), end
sc_sum   = sc_dn + 1            ; scratch: 2, the life left
sc_gcol  = sc_sum + 2           ; 6, the housing's colours:
sc_i     = sc_gcol + 6          ; the groups', sc_fixed
sc_n     = sc_i + 1
sc_k     = sc_n + 1
sc_t     = sc_k + 1
sc_r     = sc_t + 1
sc_e     = sc_r + 1
sc_a     = sc_e + 1
sc_b     = sc_a + 1
sc_c     = sc_b + 1
SC_VARS_END = sc_c + 1
        .cerror SC_VARS_END > CB_SAVE_END, "its variables"
        .cerror sc_ring != arena_chars + 1

        * = SC_AT
        .include "../assets/generated/supercomp_low.inc"
        .cerror * != WARDEN_AT, "its data before its code"

        * = WARDEN_AT
        jmp sc_draw             ; W_DRAW
        jmp sc_step             ; W_STEP
        jmp sc_paint            ; W_PAINT
        .cerror sc_draw - WARDEN_AT != 9

SC_GROUPS = (SC_CODES + 3) / 4  ; its codes, four a turn
SC_MADE_ALL = SC_GROUPS + SC_PICTURE_BYTES / 64
SC_SHOT = POD_FAN_FIRST + 16    ; the core's shot (its
                                ; fire entry), after the 16
                                ; ways (POD_FAN_FIRST)
        .cerror SC_PICTURE_BYTES % 64 != 0
        .cerror (CHARSET | SCREEN_A) & $ff != 0
        .cerror (COLOURS - SCREEN_A) & $ff != 0
        .cerror SC_LIGHT_EVERY & (SC_LIGHT_EVERY - 1) != 0
        .cerror SC_DCELLS * 4 > 256 || SC_ELEMENTS != 17
        .cerror KIND_PLATE != KIND_SEGMENT, "outer plates"

; ---------------------------------------------------------
; The screen (boss_draw, a turn): the area's cells to draw
; (SC_CELLS_TURN a turn, at most); else in ENTER a row of
; the housing, then a row of the area; else an element
; whose state changed (its cells); else the lights' step.
; ---------------------------------------------------------

sc_draw:
        lda boss_state          ; WAIT: nothing yet
        beq _done
        lda sc_di               ; cells to draw
        cmp sc_dn
        bcc sc_cells
        lda sc_hdrawn           ; a row of the housing
        cmp sc_hrows
        bcs +
        jmp sc_house_row
+       lda sc_adrawn           ; a row of the area: its
        cmp sc_arows            ; cells (the back plate
        bcs +                   ; comes)
        tax
        inc sc_adrawn
        lda sc_r_first,x
        sta sc_di
        lda sc_r_first + 1,x
        sta sc_dn
        jmp sc_cells
+       ldx #2                  ; an element
-       lda sc_want,x
        eor sc_have,x
        bne sc_element
        dex
        bpl -
        lda sc_light            ; the lights
        cmp sc_lshown
        beq _done
        lda sc_mode
        bne _done
        jmp sc_lamps
_done:
        rts

; The first element of byte X whose bits differ (A): its
; state wanted drawn, its cells to draw.
sc_element:
        sta sc_t
        txa
        asl a
        asl a
        asl a
        sta sc_e                ; 8 X: its first element
        lda sc_t
_bit:
        lsr a
        bcs _found
        inc sc_e
        bcc _bit                ; (C = 0)
_found:
        ldy sc_e
        lda sc_have,x
        eor sc_e_bit,y
        sta sc_have,x
        lda sc_e_first,y
        sta sc_di
        lda sc_e_first + 1,y
        sta sc_dn
; SC_CELLS_TURN of the cells to draw, at most.
sc_cells:
        lda #SC_CELLS_TURN
        sta sc_c
-       ldx sc_di
        cpx sc_dn
        bcs _done
        ldy sc_lists,x
        jsr sc_cell
        inc sc_di
        dec sc_c
        bne -
_done:
        rts

; Cell Y of the area: its code by the state drawn of the
; elements it touches (bit k: its element k), its colour.
sc_cell:
        sty sc_k
        tya
        asl a
        asl a
        tax                     ; its elements: 4 Y
        lda #0
        sta sc_r                ; the state
        lda #1
        sta sc_t                ; element k's bit in it
_el:
        ldy sc_d_el,x           ; its element
        bmi _code               ; (none more)
        stx sc_a
        lda sc_e_byte,y         ; drawn?
        tax
        lda sc_have,x
        ldx sc_a
        and sc_e_bit,y
        beq +
        lda sc_r
        ora sc_t
        sta sc_r
+       asl sc_t
        inx
        txa
        and #%00000011
        bne _el
_code:
        ldx sc_k
        lda sc_d_first,x
        clc
        adc sc_r
        tay
        lda sc_d_lo,x           ; its place on screen A
        sta dst
        lda sc_d_hi,x
        clc
        adc #>SCREEN_A
        sta dst + 1
        lda sc_d_codes,y
        ldy #0
        sta (dst),y
        lda dst + 1             ; its colour
        clc
        adc #>(COLOURS - SCREEN_A)
        sta dst + 1
        lda sc_d_col,x
        sta (dst),y
        rts

; Row sc_closing[sc_hdrawn] of the housing: its cells,
; their colours (a light's its group's).
sc_house_row:
        jsr sc_hues
        ldx sc_hdrawn
        inc sc_hdrawn
        ldy sc_closing,x
        jsr sc_hptrs
        jsr sc_row5
        ldy #0
-       lda sc_house,x
        sta (src),y
        stx sc_k
        lda sc_hsrc,x
        tax
        lda sc_gcol,x
        ldx sc_k
        sta (dst),y
        inx
        iny
        cpy #SC_HOUSE_COLS
        bne -
        rts

; Row Y of the housing: src its first cell on screen A,
; dst its colours. Y kept.
sc_hptrs:
        lda row_lo + SC_HOUSE_ROW0,y
        clc
        adc #SC_HOUSE_COL0
        sta src
        sta dst
        lda row_hi + SC_HOUSE_ROW0,y
        adc #0
        sta src + 1
        clc
        adc #>(COLOURS - SCREEN_A)
        sta dst + 1
        rts

; X = its first cell: Y * 5. Y kept.
sc_row5:
        tya
        asl a
        asl a
        sta sc_t
        tya
        clc
        adc sc_t
        tax
        rts

        .cerror SC_HOUSE_COLS != 5 || SC_HOUSE_ROWS > 51

; The housing's colours (sc_gcol): each group of lights
; its (the step less the group), then sc_fixed's.
sc_hues:
        ldx #5
-       cpx #4
        bcc +
        lda sc_fixed - 4,x
        bcs ++
+       txa
        eor #$ff
        sec
        adc sc_light            ; the step - the group
        and #%00000011
        tay
        lda sc_cycle,y
+       sta sc_gcol,x
        dex
        bpl -
        rts

; The lights at their step (sc_light): each its group's
; colour; from the top down (the colours' pages 0, 1, 2),
; ahead of the beam.
sc_lamps:
        lda sc_light
        sta sc_lshown
        jsr sc_hues
        ldx #0                  ; page 0
-       ldy sc_lamp_g,x
        lda sc_gcol,y
        ldy sc_lamp_lo,x
        sta COLOURS,y
        inx
        cpx #SC_LAMPS1
        bne -
-       ldy sc_lamp_g,x         ; page 1
        lda sc_gcol,y
        ldy sc_lamp_lo,x
        sta COLOURS + 256,y
        inx
        cpx #SC_LAMPS2
        bne -
-       ldy sc_lamp_g,x         ; page 2
        lda sc_gcol,y
        ldy sc_lamp_lo,x
        sta COLOURS + 512,y
        inx
        cpx #SC_LIGHTS
        bne -
        rts

        .cerror SC_LAMPS1 > 128 || SC_LIGHTS > 128

; Its colours (paint, boss.asm): X 0 its own (the lights
; at their step), 1 white, 2 the wreck's, in the housing's
; cells (a row unrolled), from its top row down: ahead of
; the beam. (The area's cells keep theirs.)
sc_paint:
        stx sc_mode
        jsr sc_hues
        lda #0
        sta sc_r
_row:
        ldy sc_r
        jsr sc_hptrs
        ldx sc_mode
        bne _fixed
        jsr sc_row5
        .for sc_l in range(SC_HOUSE_COLS)
        ldy sc_hsrc + sc_l,x
        lda sc_gcol,y
        ldy #sc_l
        sta (dst),y
        .endfor
        jmp _next
_fixed:
        lda sc_paints - 1,x
        ldy #SC_HOUSE_COLS - 1
-       sta (dst),y
        dey
        bpl -
_next:
        inc sc_r
        lda sc_r
        cmp #SC_HOUSE_ROWS
        bcc _row
        rts

sc_paints:
        .byte SC_FLASH_OWN, SC_WRECK_OWN

; ---------------------------------------------------------
; Its turn (boss_update, after the bar's step): its step.
; ---------------------------------------------------------

sc_step:
        lda #<SC_PART_X         ; its parts' places from
        sta part_x              ; here (the core's, the
        lda #>SC_PART_X         ; chain's)
        sta part_x + 1
        ldx boss_state
        lda sc_steps_lo,x
        sta vector
        lda sc_steps_hi,x
        sta vector + 1
        jmp (vector)

sc_steps_lo:
        .byte <sc_wait, <sc_enter, <sc_rings, <sc_defences
        .byte <sc_core, <sc_chain, <step_wreck, <step_clear
        .byte <step_done
sc_steps_hi:
        .byte >sc_wait, >sc_enter, >sc_rings, >sc_defences
        .byte >sc_core, >sc_chain, >step_wreck, >step_clear
        .byte >step_done

        .cerror ST_OPEN != 3 || ST_DONE != 8

; Varkon X at part_x + A (its x register).
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

; Every SC_LIGHT_EVERY frames the lights' next step.
sc_step_lights:
        lda anim
        and #SC_LIGHT_EVERY - 1
        bne +
        lda sc_light
        clc
        adc #1
        and #%00000011
        sta sc_light
+       rts

; --- WAIT -------------------------------------------------
; Its codes are made meanwhile, four a turn; when no
; Varkon flies or explodes, its pictures, one a turn; WAIT
; ends when they are made and no Varkon has flown or
; exploded for ARENA_WAIT frames.
sc_wait:
        jsr sc_make_codes
        ldx #ENEMIES - 1        ; a Varkon flying or
-       lda en_on,x             ; exploding: wait for it
        cmp #FLYING
        beq _busy
        cmp #BOOM
        beq _busy
        dex
        bpl -
        jsr sc_picture
        inc boss_timer
        lda boss_timer
        cmp #ARENA_WAIT
        bcc _done
        lda sc_made
        cmp #SC_MADE_ALL
        bcc _done
        jmp sc_begin
_done:
        rts
_busy:
        lda #0
        sta boss_timer
        rts

; Four of its codes (sc_made's group): their lines from
; sc_chars into the characters; into the rock's table
; their lines AND their masks.
sc_make_codes:
        lda sc_made
        cmp #SC_GROUPS
        bcs _done
        asl a
        asl a
        sta sc_k                ; its first code's place
        inc sc_made
        lda #4
        sta sc_t
-       ldx sc_k
        cpx #SC_CODES
        bcs _done
        jsr sc_one_code
        inc sc_k
        dec sc_t
        bne -
_done:
        rts

; Code X of its codes (sc_code, its lines sc_chars + 8 X,
; its mask sc_mbytes + 8 sc_mask[X]).
sc_one_code:
        lda #0                  ; src: sc_chars + 8 X
        sta src + 1
        txa
        .rept 3
        asl a
        rol src + 1
        .endrept
        clc
        adc #<sc_chars
        sta src
        lda src + 1
        adc #>sc_chars
        sta src + 1
        lda sc_mask,x           ; vector: its mask
        ldy #0
        sty vector + 1
        .rept 3
        asl a
        rol vector + 1
        .endrept
        clc
        adc #<sc_mbytes
        sta vector
        lda vector + 1
        adc #>sc_mbytes
        sta vector + 1
        lda sc_code,x           ; dst: CHARSET + 8 code
        sty dst + 1
        .rept 3
        asl a
        rol dst + 1
        .endrept
        sta dst
        lda dst + 1
        clc
        adc #>CHARSET
        sta dst + 1
        lda sc_code,x
        tax
        .for sc_l in range(8)
        lda (src),y
        sta (dst),y
        and (vector),y
        sta rock_lines + sc_l * 256,x
        iny
        .endfor
        rts

        .cerror SC_CODES > 255 || SC_MASKS * 8 > 256 * 8

; A picture of its parts (sc_made - SC_GROUPS): 64 bytes
; over the level's (its first: no Varkon of the level
; flies in the arena any more).
sc_picture:
        lda sc_made
        cmp #SC_GROUPS
        bcc _done
        cmp #SC_MADE_ALL
        bcs _done
        sec
        sbc #SC_GROUPS
        inc sc_made
        tax
        lda sc_pic_lo,x
        sta src
        lda sc_pic_hi,x
        sta src + 1
        lda sc_spr_lo,x
        sta dst
        lda sc_spr_hi,x
        sta dst + 1
        ldy #63
-       lda (src),y
        sta (dst),y
        dey
        bpl -
_done:
        rts

; WAIT is over: rows 10-14 rock, the far layer's codes
; not; no plates yet, the turrets' lives, the outer ring's
; angle; the bar; ENTER.
sc_begin:
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
        ldx #SC_FAR_COUNT - 1   ; the far layer's codes: not
        lda #0                  ; rock
-       ldy sc_far,x
        .for sc_l in range(8)
        sta rock_lines + sc_l * 256,y
        .endfor
        dex
        bpl -
        ldx #SC_MOST - 1      ; no plates
        lda #$ff
-       sta sc_pv,x
        dex
        bpl -
        ldx #3                  ; the turrets' lives
        lda #SC_TURRET_LIFE
-       sta sc_tlife,x
        dex
        bpl -
        lda #SC_START
        sta sc_ang + 1
        lda #0
        sta sc_ang
        sta boss_timer
        sta parts
        sta sc_mode
        lda #$ff
        sta part_core
        jsr bar_on
        lda #ST_ENTER
        sta boss_state
        rts

        .cerror CORRIDOR_FROM & 7 != 0, "its lines"
        .cerror CORRIDOR_TO - CORRIDOR_FROM > 128

; --- ENTER: it comes --------------------------------------
; The housing closes in, a row every SC_HOUSE_EVERY frames
; (drawn in the next turn); the area's rows, one a frame
; (the back plate); its elements, one every
; SC_ELEMENT_EVERY frames (sc_order: the shell, the inner
; ring, the middle one); the outer ring's plates, turning,
; one every SC_PLATE_EVERY frames (none free: a frame
; later); all there, its sound, the fight.
sc_enter:
        ldx sc_estep
        beq _house
        dex
        beq _area
        dex
        beq _elements
        jmp _plates
_house:
        lda sc_hrows
        cmp #SC_HOUSE_ROWS
        bcs +
        inc boss_timer
        lda boss_timer
        cmp #SC_HOUSE_EVERY
        bcc _done
        lda #0
        sta boss_timer
        inc sc_hrows
_done:
        rts
+       lda sc_hdrawn
        cmp #SC_HOUSE_ROWS
        bcc _done
        inc sc_estep
        rts
_area:
        lda sc_arows
        cmp #SC_AREA_ROWS
        bcs +
        inc sc_arows
        rts
+       lda sc_adrawn
        cmp #SC_AREA_ROWS
        bcc _done
        lda sc_di               ; all their cells drawn?
        cmp sc_dn
        bcc _done
        inc sc_estep
        lda #0
        sta boss_timer
        sta sc_count
        rts
_elements:
        lda sc_count
        cmp #SC_ELEMENTS
        bcs _all
        inc boss_timer
        lda boss_timer
        cmp #SC_ELEMENT_EVERY
        bcc _wants
        lda #0
        sta boss_timer
        ldx sc_count
        inc sc_count
        ldy sc_order,x
        ldx sc_e_byte,y
        lda sc_shown,x
        ora sc_e_bit,y
        sta sc_shown,x
_wants:
        jmp sc_wants
_all:
        jsr sc_wants
        lda sc_di               ; all drawn?
        cmp sc_dn
        bcc _later
        ldx #2
-       lda sc_want,x
        cmp sc_have,x
        bne _later
        dex
        bpl -
        inc sc_estep
        lda #1                  ; the plates: place 1 first
        sta sc_count
        lda #0
        sta boss_timer
        rts
_plates:
        jsr sc_turn
        jsr sc_wants
        inc boss_timer
        lda boss_timer
        cmp #SC_PLATE_EVERY
        bcc _place
        jsr free_varkon
        bcs _place              ; none free: a frame later
        lda #0
        sta boss_timer
        txa
        ldy sc_count
        sta sc_pv,y
        ldy #KIND_PLATE
        jsr new_part
        inc sc_count
_place:
        jsr sc_plates           ; (the new one's place too)
        lda sc_count
        cmp sc_places
        bcs +
_later:
        rts
+       lda #FX_BOOM            ; all there: the fight
        jsr sfx_start
        lda #0
        sta sc_cyc
        lda sc_every
        sta sc_fire
        lda #ST_FIGHT
        sta boss_state
        jmp sc_bar_rings

; --- FIGHT: the rings, one at a time from outside --------
; The ring turns, its plates are placed (those destroyed
; left out), the gaps wanted; while its gap faces the ship
; (left), the core's shot every sc_every frames; its last
; plate destroyed: the next ring (its segments go, then its
; plates come where they were: sc_next_ring), the inner
; one's: the defences (OPEN).
sc_rings:
        lda sc_cyc
        beq +
        jmp sc_next_ring
+       jsr sc_turn
        jsr sc_plates
        jsr sc_wants
        lda sc_t                ; plates left?
        beq sc_ring_done
        jsr sc_gap_shot
        jsr sc_step_lights
        jmp sc_bar_rings

; The ring's plates all destroyed.
sc_ring_done:
        jsr sc_step_lights
        ldx sc_ring
        cpx #2
        bcc +
        lda #3                  ; the inner one's: no ring,
        sta sc_ring             ; the defences
        jsr sc_wants
        lda #0
        sta sc_cyc
        sta sc_pair
        lda #SC_PAIR_WAIT
        sta boss_timer
        lda #ST_OPEN
        sta boss_state
        jmp sc_bar_open
+       inx                     ; the next ring: its
        stx sc_ring             ; segments go
        lda #0
        sta sc_shown - 1,x
        lda #1
        sta sc_cyc
        jsr sc_wants
        jmp sc_bar_rings

; The next ring: its segments drawn away, its gap where
; its characters' was (the segment's middle: sc_cyc 2);
; its plates, one a frame (places 1 to its last; none
; free: a frame later), placed (not turning); all there, it
; turns, its shot.
sc_next_ring:
        jsr sc_step_lights
        jsr sc_wants
        ldx sc_ring
        lda sc_cyc
        cmp #2
        bcs _plate
        lda sc_have - 1,x       ; its segments drawn away?
        bne _bar
        lda sc_di
        cmp sc_dn
        bcc _bar
        lda sc_ang + 1          ; its gap: the segment's
        clc                     ; middle
        adc #16
        and #%11100000
        sta sc_ang + 1
        lda #0
        sta sc_ang
        lda #2
        sta sc_cyc
        lda #1
        sta sc_count
_plate:
        jsr free_varkon
        bcs _bar
        txa
        ldy sc_count
        sta sc_pv,y
        ldy sc_ring
        lda sc_plate_kind,y
        tay
        jsr new_part
        jsr sc_plates
        inc sc_count
        ldx sc_ring
        lda sc_count
        cmp sc_places,x
        bcc _bar
        lda #0                  ; all there: it turns
        sta sc_cyc
        lda sc_every,x
        sta sc_fire
_bar:
        jmp sc_bar_rings

; The ring turns.
sc_turn:
        ldx sc_ring
        lda sc_ang
        clc
        adc sc_speed_lo,x
        sta sc_ang
        lda sc_ang + 1
        adc sc_speed_hi,x
        sta sc_ang + 1
        rts

; Its plates: a destroyed one (its Varkon not flying) out
; of sc_pv; the others at their places: angle (its gap's +
; the place's) / 2 in the outer ring's table (128 + r cos,
; 128 angles), / 4 in the others' (64), its line a quarter
; turn before (r sin). sc_t: how many are left.
sc_plates:
        ldx sc_ring
        lda sc_cos_lo,x
        sta src
        lda sc_cos_hi,x
        sta src + 1
        lda sc_offs_at,x
        sta sc_r
        lda sc_places,x
        sta sc_n
        lda sc_quarter,x
        sta sc_a                ; a quarter turn there
        lda sc_amask,x
        sta sc_b                ; its angles - 1
        lda #0
        sta sc_t
        lda #1
        sta sc_i
_one:
        ldy sc_i
        cpy sc_n
        bcs _done
        ldx sc_pv,y
        bmi _next
        lda en_on,x
        cmp #FLYING
        beq _alive
        lda #$ff                ; destroyed: not placed
        sta sc_pv,y             ; again
        bne _next
_alive:
        inc sc_t
        tya
        clc
        adc sc_r
        tay
        lda sc_offs,y
        clc
        adc sc_ang + 1
        lsr a                   ; 128 angles
        ldy sc_a
        cpy #32
        beq +
        lsr a                   ; 64
+       sta sc_k
        tay
        lda (src),y             ; x register
        clc
        adc #<SC_MIDX
        sta en_x,x
        lda #>SC_MIDX
        adc #0
        sta en_xh,x
        lda #0
        sta en_xf,x
        lda sc_k                ; top line
        sec
        sbc sc_a
        and sc_b
        tay
        lda (src),y
        clc
        adc #SC_MIDY
        sta en_y,x
_next:
        inc sc_i
        bne _one
_done:
        rts

sc_cos_lo:
        .byte <sc_cos, <(sc_cos + 128), <(sc_cos + 192)
sc_cos_hi:
        .byte >sc_cos, >(sc_cos + 128), >(sc_cos + 192)
sc_quarter:
        .byte 32, 16, 16
sc_amask:
        .byte 127, 63, 63
sc_offs_at:
        .byte 0, SC_MOST, 2 * SC_MOST

; The elements wanted: those shown, less the segments of the
; gap ((angle + 16) / 32) in the rings waiting.
sc_wants:
        lda sc_ang + 1
        clc
        adc #16
        lsr a
        lsr a
        lsr a
        lsr a
        lsr a
        tax
        lda sc_bit8,x
        eor #$ff
        sta sc_b
        ldx sc_ring
        lda sc_shown            ; the middle ring's
        cpx #1
        bcs +
        and sc_b
+       sta sc_want
        lda sc_shown + 1        ; the inner ring's
        cpx #2
        bcs +
        and sc_b
+       sta sc_want + 1
        lda sc_shown + 2        ; the shell
        sta sc_want + 2
        rts

sc_bit8:
        .byte 1, 2, 4, 8, 16, 32, 64, 128

; The core's shot through the gaps while they face the
; ship (left: SC_GAP_LEFT +- SC_GAP_WINDOW), every
; sc_every frames.
sc_gap_shot:
        lda sc_ang + 1
        sec
        sbc #SC_GAP_LEFT - SC_GAP_WINDOW
        cmp #2 * SC_GAP_WINDOW + 1
        bcs _away
        dec sc_fire
        bne _done
        ldx sc_ring
        lda sc_every,x
        sta sc_fire
        jmp sc_shoot
_away:
        ldx sc_ring
        lda sc_every,x
        sta sc_fire
_done:
        rts

; The core's shot (its fire entry SC_SHOT) from the
; core's place (its shell's; fire_entry's way): in the
; first free place (none: none), aimed as a drone's.
sc_shoot:
        ldy #0
-       lda sh_on,y
        beq _free
        iny
        cpy #ESHOTS
        bne -
        rts
_free:
        sty f_slot
        lda #FX_PLASMA          ; its sound
        jsr sfx_start
        ldy #SC_SHOT
        lda fire_dx,y           ; where it starts
        clc
        adc #<(SC_MIDX + 128)
        sta f_x
        lda fire_dx,y           ; dx's sign
        and #%10000000
        beq +
        lda #$ff
+       adc #>(SC_MIDX + 128)
        sta f_xh
        lda fire_dy,y
        clc
        adc #SC_CORE_Y
        sta f_y
        ldx f_slot              ; X: the shot
        lda #0
        sta sh_yf,x
        lda #1
        sta sh_on,x
        lda f_x
        sta sh_x,x
        lda f_xh
        sta sh_xh,x
        lda f_y
        sta sh_y,x
        lda fire_vx,y
        sta sh_vx,x
        lda fire_vyl,y
        sta sh_vyl,x
        lda fire_vyh,y
        sta sh_vyh,x
        lda fire_aim,y          ; to the ship
        beq _object
        lda f_y                 ; below the ship's line
        clc                     ; by more than AIM_DEAD?
        adc #AIM_DEAD
        cmp ship_y
        bcs +
        lda #<AIM_VY            ; down
        sta sh_vyl,x
        lda #>AIM_VY
        sta sh_vyh,x
        jmp _object
+       lda ship_y              ; above it?
        clc
        adc #AIM_DEAD
        cmp f_y
        bcs _object
        lda #<(-AIM_VY)         ; up
        sta sh_vyl,x
        lda #>(-AIM_VY)
        sta sh_vyh,x
_object:
        txa                     ; its object
        clc
        adc v_base
        adc #FIRST_ESHOT
        tay
        lda anim                ; its picture: anim / 4
        lsr a                   ; AND 3
        lsr a
        and #%00000011
        clc
        adc #PLASMA_BLOCK
        sta v_tmp + 1
        jsr plasma_object       ; (C = 1: born past an edge)
        bcc +
        lda #0
        sta sh_on,x
        lda #NONE
        sta obj_y,y
+       rts

; The bar (every fourth frame): the life left (the ring's
; plates', those of the rings after it, the turrets', the
; core's) / 4 into its steps (sc_bar_of). The rings: the
; next one coming, its whole life; else its plates' left.
sc_no_bar:
        rts
sc_bar_rings:
        lda anim                ; every fourth frame
        and #%00000011
        bne sc_no_bar
        ldx sc_ring
        lda sc_cyc
        beq +
        lda sc_full_lo,x
        sta sc_sum
        lda sc_full_hi,x
        sta sc_sum + 1
        jmp sc_bar_set
+       lda sc_rest_lo,x
        sta sc_sum
        lda sc_rest_hi,x
        sta sc_sum + 1
        lda sc_places,x
        sta sc_n
        ldy #1
-       cpy sc_n
        bcs sc_bar_set
        ldx sc_pv,y
        bmi +
        lda en_life,x
        clc
        adc sc_sum
        sta sc_sum
        bcc +
        inc sc_sum + 1
+       iny
        bne -
sc_bar_set:
        lda sc_sum + 1
        lsr a
        ror sc_sum
        lsr a
        lda sc_sum
        ror a
        tax
        lda sc_bar_of,x
        sta bar_want
        rts

; The defences: the core's life, the turrets' (kept).
sc_bar_open:
        lda anim                ; every fourth frame
        and #%00000011
        bne sc_no_bar
        lda #SC_CORE_LIFE
        sta sc_sum
        lda #0
        sta sc_sum + 1
        ldy #3
-       lda sc_tlife,y
        clc
        adc sc_sum
        sta sc_sum
        bcc +
        inc sc_sum + 1
+       dey
        bpl -
        jmp sc_bar_set

; The core: its life.
sc_bar_core:
        lda anim                ; every fourth frame
        and #%00000011
        bne sc_no_bar2
        ldx part_core
        lda en_life,x
        sta sc_sum
        lda #0
        sta sc_sum + 1
        jmp sc_bar_set

sc_no_bar2:
        rts

        .cerror SC_TOTAL > 1020 || SC_CORE_LIFE > 255
        .cerror SC_TURRET_LIFE > 127

; --- OPEN: the defences ----------------------------------
; The turrets destroyed this frame; all four: the shell
; (sc_cyc 4: SC_CORE_WAIT frames, then it opens; 5: drawn
; open, SC_CORE_ANIM frames, the core). Else the pair's
; cycle: 0 SC_PAIR_WAIT frames, then its turrets left come
; out (free Varkon; not enough: a frame later), their
; lives as they were; 1 out, a step a frame, then 2 their
; fans, SC_TURRET_OUT frames; 3 back in, a step a frame,
; then freed; the next pair. A pair destroyed: the next
; at once (its wait).
sc_defences:
        jsr sc_step_lights
        jsr sc_tcheck
        lda sc_cyc
        cmp #4
        bcc +
        jmp sc_opening
+       lda sc_tgone
        cmp #%00001111
        bne +
        lda #4                  ; all four destroyed
        sta sc_cyc
        lda #SC_CORE_WAIT
        sta boss_timer
        jmp sc_bar_open
+       ldx sc_cyc
        beq _wait
        dex
        beq _out
        dex
        bne +
        jmp _fans
+       lda sc_tlive            ; 3: back in
        beq _next
        dec sc_slide
        jsr sc_tplace
        lda sc_slide
        bne _bar
        ldy #3                  ; in: freed, their lives
-       lda sc_tlive            ; kept
        and sc_tbit,y
        beq +
        ldx sc_tv,y
        lda #0
        sta en_on,x
+       dey
        bpl -
        lda #0
        sta sc_tlive
_next:
        jsr sc_next_pair
_bar:
        jmp sc_bar_open
_wait:
        dec boss_timer
        bne _bar
        jsr sc_pair_on
        bcc +
        inc boss_timer          ; (not enough: a frame
        bne _bar                ; later)
+       lda #0
        sta sc_slide
        lda #1
        sta sc_cyc
        jsr sc_tplace
        jmp _bar
_out:
        lda sc_tlive
        beq _next
        inc sc_slide
        jsr sc_tplace
        lda sc_slide
        cmp #SC_SLIDES - 1
        bcc _bar
        lda #2                  ; out: their first fans
        sta sc_cyc
        lda #SC_TURRET_OUT
        sta boss_timer
        ldy #3
-       lda sc_tlive
        and sc_tbit,y
        beq +
        ldx sc_tv,y
        tya
        and #%00000001
        sta sc_k
        tya
        pha
        ldy sc_k
        lda sc_fan_first,y
        sta en_fire,x
        pla
        tay
+       dey
        bpl -
        jmp _bar
_fans:
        lda sc_tlive
        beq _next
        jsr sc_fans
        dec boss_timer
        bne _bar
        lda #3
        sta sc_cyc
        jmp _bar

; The shell: SC_CORE_WAIT frames, it opens; drawn open,
; SC_CORE_ANIM frames, the core in a free Varkon (none: a
; frame later), its fan's way, the core's fight.
sc_opening:
        bne _open
        dec boss_timer          ; 4
        bne _bar
        lda sc_shown + 2        ; the shell opens
        and #%11111110
        sta sc_shown + 2
        jsr sc_wants
        lda #5
        sta sc_cyc
        lda #SC_CORE_ANIM
        sta boss_timer
_bar:
        jmp sc_bar_open
_open:
        lda sc_have + 2         ; drawn open?
        bne _bar
        lda sc_di
        cmp sc_dn
        bcc _bar
        dec boss_timer
        bne _bar
        jsr free_varkon
        bcc +
        inc boss_timer
        bne _bar
+       stx part_core
        ldy #KIND_SCCORE
        jsr new_part
        lda #SC_CORE_Y
        sta en_y,x
        lda #SC_CORE_DX
        jsr place_one_x
        lda parts
        ora #%00000100
        sta parts
        lda #SC_FIRST_WAY
        sta sc_way
        lda #SC_TURN_EVERY
        sta sc_wt
        lda #SC_FAN_EVERY
        sta sc_ft
        lda #ST_CORE
        sta boss_state
        jmp sc_bar_core

        .cerror SC_SHELL != 16, "the shell: byte 2, bit 0"

; The turrets destroyed this frame (their Varkon not
; flying) into sc_tgone, out of sc_tlive, their life 0;
; the others' lives kept.
sc_tcheck:
        ldy #3
_one:
        lda sc_tlive
        and sc_tbit,y
        beq _next
        ldx sc_tv,y
        lda en_on,x
        cmp #FLYING
        beq _alive
        lda sc_tgone
        ora sc_tbit,y
        sta sc_tgone
        lda sc_tlive
        eor sc_tbit,y
        sta sc_tlive
        lda #0
        sta sc_tlife,y
        beq _next
_alive:
        lda en_life,x
        sta sc_tlife,y
_next:
        dey
        bpl _one
        rts

; The other pair (this one again if the other's are
; destroyed): its wait.
sc_next_pair:
        lda sc_pair
        eor #1
        sta sc_pair
        tax
        lda sc_tgone
        and sc_pair_bits,x
        cmp sc_pair_bits,x
        bne +
        txa
        eor #1
        sta sc_pair
+       lda #0
        sta sc_cyc
        lda #SC_PAIR_WAIT
        sta boss_timer
        rts

; The pair's turrets not destroyed in free Varkon (C = 0),
; their lives as they were; not enough free Varkon: none,
; C = 1.
sc_pair_on:
        lda sc_pair             ; its first turret
        asl a
        sta sc_r
        tax
        ldy #0                  ; how many wanted
        lda sc_tgone
        and sc_tbit,x
        bne +
        iny
+       lda sc_tgone
        and sc_tbit + 1,x
        bne +
        iny
+       sty sc_t
        ldy #0                  ; how many free
        ldx #ENEMIES - 1
-       lda en_on,x
        bne +
        iny
+       dex
        bpl -
        cpy sc_t
        bcc _none
        ldy sc_r
        jsr _one
        ldy sc_r
        iny
        jsr _one
        clc
        rts
_none:
        sec
        rts
_one:
        lda sc_tgone            ; turret Y, if not destroyed
        and sc_tbit,y
        bne _done
        sty sc_k
        jsr free_varkon
        txa
        ldy sc_k
        sta sc_tv,y
        lda sc_tlive
        ora sc_tbit,y
        sta sc_tlive
        ldy #KIND_STURRET
        jsr new_part
        ldy sc_k
        lda sc_tlife,y
        sta en_life,x
_done:
        rts

; The turrets on the screen at their step of the way out
; (sc_slide): x register SC_MIDX + sc_slide_x, top line
; sc_slide_y.
sc_tplace:
        ldy #3
_one:
        lda sc_tlive
        and sc_tbit,y
        beq _next
        ldx sc_tv,y
        tya
        pha
        lda sc_tfirst,y
        clc
        adc sc_slide
        tay
        lda sc_slide_x,y
        clc
        adc #<SC_MIDX
        sta en_x,x
        lda #>SC_MIDX
        adc #0
        sta en_xh,x
        lda #0
        sta en_xf,x
        lda sc_slide_y,y
        sta en_y,x
        pla
        tay
_next:
        dey
        bpl _one
        rts

; Each turret out: its fan when its time comes, aimed at
; the ship (sc_aim: way d, the shots of ways d - 1, d,
; d + 1).
sc_fans:
        ldy #3
_one:
        lda sc_tlive
        and sc_tbit,y
        beq _next
        sty sc_i
        ldx sc_tv,y
        dec en_fire,x
        bne +
        lda #SC_FAN_PERIOD
        sta en_fire,x
        jsr sc_aim
        clc
        adc #POD_FAN_FIRST - 1
        ldy #3
        jsr fire_fan
+       ldy sc_i
_next:
        dey
        bpl _one
        rts

; Varkon X's way to the ship (A: 4-12): q = its x register
; - the ship's (8-255), p = |the ship's line - its line|;
; k = 0 if p < q/4 - q/16, 1 if p < q/2 + q/8 + q/32, 2
; if p < q + q/2, 3 if p < 5 q, else 4; the way 8 - k if
; the ship is lower, else 8 + k. X kept.
sc_aim:
        lda ship_x              ; the ship's x register
        clc
        adc #24
        sta b_tmp
        lda ship_xh
        adc #0
        sta b_tmp + 1
        sec
        lda en_x,x
        sbc b_tmp
        sta sc_k
        lda en_xh,x
        sbc b_tmp + 1
        bmi _near               ; the ship to its right
        bne _far                ; 256 or more
        lda sc_k
        cmp #8
        bcs +
_near:
        lda #8
        bne +
_far:
        lda #255
+       sta sc_k                ; q
        lda #0
        sta sc_e                ; 0: the ship lower
        lda ship_y
        sec
        sbc en_y,x
        bcs +
        eor #$ff                ; higher: |dy|
        adc #1                  ; (C = 0)
        inc sc_e
+       sta sc_t                ; p
        ldy #0
        lda sc_k                ; q/4 - q/16
        lsr a
        lsr a
        sta sc_a
        lsr a
        lsr a
        sta sc_b
        lda sc_a
        sec
        sbc sc_b
        jsr _below
        bcs _way
        iny                     ; q/2 + q/8 + q/32
        lda sc_k
        lsr a
        sta sc_a
        lsr a
        lsr a
        sta sc_b
        lsr a
        lsr a
        clc
        adc sc_b
        adc sc_a                ; (C = 0)
        jsr _below
        bcs _way
        iny                     ; q + q/2 (q < 104)
        lda sc_k
        cmp #104
        bcs _way
        lsr a
        clc
        adc sc_k
        jsr _below
        bcs _way
        iny                     ; 5 q (q < 32)
        lda sc_k
        cmp #32
        bcs _way
        asl a
        asl a
        adc sc_k                ; (C = 0)
        jsr _below
        bcs _way
        iny
_way:
        lda sc_e
        bne _up
        sty sc_a                ; lower: 8 - k
        lda #8
        sec
        sbc sc_a
        rts
_up:
        tya                     ; higher: 8 + k
        clc
        adc #8
        rts
_below:                         ; C = 1 if p < A
        cmp sc_t
        beq _no
        rts
_no:
        clc
        rts

; --- CORE: the core uncovered -----------------------------
; Destroyed: the end (boss_dies, then sc_chain). Under
; SC_RAGE_LIFE its colour, its turn and its fans faster.
; Its fan's way a step back every sc_turn_t frames;
; every sc_fan_t frames, the way from SC_FAN_LO to
; SC_FAN_HI (towards the left), three shots: ways - 1,
; it, + 1.
sc_core:
        jsr sc_step_lights
        ldx part_core
        lda en_on,x
        cmp #FLYING
        beq +
        jmp boss_dies
+       ldy #0
        lda en_life,x
        cmp #SC_RAGE_LIFE + 1
        bcs +
        lda #SC_RAGE_OWN
        sta en_colour,x
        iny
+       dec sc_wt
        bne +
        lda sc_turn_t,y
        sta sc_wt
        lda sc_way
        sec
        sbc #1
        and #%00001111
        sta sc_way
+       dec sc_ft
        bne _bar
        lda sc_fan_t,y
        sta sc_ft
        lda sc_way
        cmp #SC_FAN_LO
        bcc _bar
        cmp #SC_FAN_HI + 1
        bcs _bar
        clc
        adc #POD_FAN_FIRST - 1
        ldy #3
        jsr fire_fan
_bar:
        jmp sc_bar_core

sc_turn_t:
        .byte SC_TURN_EVERY, SC_TURN_RAGE
sc_fan_t:
        .byte SC_FAN_EVERY, SC_FAN_RAGE

        .cerror SC_FAN_LO < 1 || SC_FAN_HI > 14

; --- CHAIN: as the engine's step_chain, on it -------------
; Every CHAIN_EVERY frames a fireball (a free Varkon
; exploding; none free: none) at sc_chain_dx from part_x,
; on line sc_chain_y; its sound, the housing white for a
; moment.
sc_chain:
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
        lda #KIND_SCCORE
        sta en_kind,x
        lda #BOSS
        sta en_beh,x
        lda #0
        sta en_left,x
        sta en_flash,x
        sta en_cap,x
        ldy chain_k
        lda sc_chain_y,y
        sta en_y,x
        lda sc_chain_dx,y
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
; Its tables, the rest of its data (build_assets.py).
; ---------------------------------------------------------

sc_pic_lo:                      ; its pictures: from, to
        .for sc_l in range(SC_PICTURE_BYTES / 64)
        .byte <(sc_pictures + 64 * sc_l)
        .endfor
sc_pic_hi:
        .for sc_l in range(SC_PICTURE_BYTES / 64)
        .byte >(sc_pictures + 64 * sc_l)
        .endfor
sc_spr_lo:
        .for sc_l in range(SC_PICTURE_BYTES / 64)
        .byte <(SC_SPRITES + 64 * sc_l)
        .endfor
sc_spr_hi:
        .for sc_l in range(SC_PICTURE_BYTES / 64)
        .byte >(SC_SPRITES + 64 * sc_l)
        .endfor

        .include "../assets/generated/supercomp_data.inc"
SC_END:                         ; the file's end
        .cerror SC_END > $fffa, "past $fffa"
