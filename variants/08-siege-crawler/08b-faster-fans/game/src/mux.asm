; The multiplexer: more objects than sprites.
;
; Sprites 0 and 1 are the ship's. Sprites 2-7 show the
; objects: the ship's four shots (0-3), the twelve Varkon
; (4-15), their six shots (16-21), the satellite (22) and
; the missile (23), all multicolour. An object has a y
; register (255: not shown), an x register (and its ninth
; bit, $ff), a block, a colour, in two banks of OBJ_BANK
; places: obj_base is this frame's; the Varkon are moved
; into the other one for the next frame while the interrupts
; still read this one.
;
; Each frame, before line 50, plan_sprites makes the plan:
;  - the objects in order of y, in two orders kept from
;    frame to frame, by insertion: the Varkon's and their
;    shots' (order_v, 4-21), sorted at the end of the turn
;    before, when they have moved for this frame
;    (mux_ahead); the ship's (order_s: 0-3, 22, 23), sorted
;    now, when they have been written. The plan takes the
;    two orders together, the lower first (equal: the
;    Varkon's).
;  - in that order each object becomes the plan's next
;    entry I, on sprite 2 + I mod 6. The first six are
;    written now; from the seventh on the interrupts write
;    entry I once the entry before it on that sprite has
;    been drawn, from line acc_trig = its y + MUX_FREE, the
;    writes MUX_COST lines apart, each done within MUX_DONE
;    lines, before the entry's own line;
;  - an object that could not be written in time gets no
;    entry: of it and the last six entries, the one with
;    the lowest priority (obj_pri) is left out (the Varkon's
;    shots 3, the Varkon 2, the ship's shots 1, + STARVE if
;    the plan before left it out: they take turns; equal:
;    the later one). If that is an entry, the object takes
;    its place: the same sprite and the same write, for a
;    later line.

MUX_FREE = 22                   ; the line after a sprite
MUX_COST = 4                    ; a write can take 4 lines
MUX_DONE = 5                    ; in a crowded band
STARVE   = 4
HARDWARE = 6
NONE     = 255                  ; y of an object not shown

; The plan of this frame and the sprites before line 50.
plan_sprites:
        lda obj_base            ; this frame's bank
        eor #OBJ_BANK
        sta obj_base
        lda #0                  ; none left out yet
        sta left_n
        jsr ship_sprites        ; sprites 0, 1
        jsr export_shots        ; objects 0-3, 22, 23
        lda obj_base
        bne +
        jsr sort_sa             ; the ship's order of y
        jsr plan_a              ; the entries, their lines
        jmp ++
+       jsr sort_sb
        jsr plan_b
+       jsr first_sprites
        lda #HARDWARE
        sta mux_next
        lda #1                  ; the interrupts may use it
        sta mux_ready
sprites_placed:                 ; the tests look here
        rts

; At the end of the turn, once the Varkon of the next frame
; are in its bank: the priorities for the next plan; the
; Varkon's order sorted for that bank.
mux_ahead:
        jsr priorities
        lda obj_base            ; the next frame's bank
        bne +
        jmp sort_vb
+       jmp sort_va

; Insertion: an object moves up its order while the one
; before it has a greater y. Most frames none moves: one
; comparison each, unrolled. \ys: the bank's y registers;
; \ord, \n: the order and its length.
sort_order .macro ys, ord, n
        .for s_i in range(1, \n)
        ldy \ord + s_i
        lda \ys,y
        ldy \ord + s_i - 1
        cmp \ys,y
        bcs +
        ldx #s_i                ; it moves up
        jsr _move
+
        .endfor
        rts
_move:                          ; X: its place, A: its y,
        sta b_key               ; Y: the one before it
        lda \ord,x
        sta b_o
_down:
        tya
        sta \ord,x
        dex
        beq _place
        ldy \ord - 1,x
        lda \ys,y
        cmp b_key
        beq _place
        bcs _down
_place:
        lda b_o
        sta \ord,x
        rts
        .endmacro

V_COUNT = ENEMIES + ESHOTS      ; the Varkon's order: 4-21
S_COUNT = OBJECTS - V_COUNT     ; the ship's: 0-3, 22, 23
order_v = order
order_s = order + V_COUNT
sort_va #sort_order obj_y, order_v, V_COUNT
sort_vb #sort_order obj_y + OBJ_BANK, order_v, V_COUNT
sort_sa #sort_order obj_y, order_s, S_COUNT
sort_sb #sort_order obj_y + OBJ_BANK, order_s, S_COUNT

; The entries, in the two orders together: mux_count of
; them, each with plan_ix (its object's place in the bank),
; plan_y, acc_trig (from the seventh on). \base: the
; bank's first place. X: the place in order_v; s_pos the
; place in order_s, s_key and s_obj its object's y and
; number.
plan_objects .macro base
        lda #FIELD_LINE - MUX_COST
        sta b_done              ; the writes: none yet
        ldx #0                  ; X: in order_v
        stx mux_count
        stx b_valid
        stx s_pos
        jsr _s_head
_next:
        lda #NONE               ; the Varkon's next ...
        cpx #V_COUNT
        bcs +
        ldy order_v,x
        lda obj_y + \base,y
+       cmp s_key               ; ... or the ship's, lower
        bcc _v                  ; (equal: the Varkon's)
        beq _v
        lda s_obj               ; the ship's
        sta b_o
        lda s_key
        sta b_key
        inc s_pos
        jsr _s_head
        lda b_key
        jmp _entry
_v:
        cmp #NONE
        beq _end                ; the rest are not shown
        sty b_o
        inx
_entry:
        ldy mux_count
        cpy #HARDWARE
        bcs _timed
_take:
        sta plan_y,y            ; entry Y: A its y
        lda b_o
        .if \base != 0
        clc
        adc #\base
        .endif
        sta plan_ix,y
        inc mux_count
_skip:
        jmp _next
_end:
        rts
_s_head:                        ; order_s's next object
        ldy s_pos
        cpy #S_COUNT
        bcs +
        lda order_s,y
        sta s_obj
        tay
        lda obj_y + \base,y
        sta s_key
        rts
+       lda #NONE
        sta s_key
        rts
_timed:
        sta b_key
        lda plan_y - HARDWARE,y ; its sprite's last: free
        adc #MUX_FREE - 1       ; from this line (C = 1)
        sta b_free
        lda b_done              ; after the writes before
        adc #MUX_COST
        cmp b_free
        bcs +
        lda b_free
+       sta b_start             ; the write's first line
        clc
        adc #MUX_DONE           ; done before its own line?
        cmp b_key
        beq +
        bcs _crowded
+       lda b_free
        sta acc_trig,y
        lda b_start
        sta b_done
        lda #0                  ; the last six change
        sta b_valid
        lda b_key
        jmp _take
_crowded:
        jsr crowded
        jmp _skip
        .endmacro

plan_a  #plan_objects 0
plan_b  #plan_objects OBJ_BANK

        .cerror 204 + MUX_FREE + MUX_COST + MUX_DONE > 255
        .cerror OBJ_BANK + OBJECTS > 255

; Object b_o (y b_key) could not be written in time: of it
; and the last six entries, the one with the lowest
; priority (equal: the later) is left out; if it is an
; entry, b_o takes its place. The last six's lowest is
; kept (b_valid) until an entry is added or replaced: in a
; crowded band most objects only meet it.
crowded:
        stx b_i
        ldy b_o                 ; priority 1, the
        lda obj_pri,y           ; lowest there is: it
        cmp #2                  ; leaves, without looking
        bcs +                   ; (equal: the later one)
        jmp _self
+       lda b_valid
        bne _known
        lda #$ff                ; the lowest of entries
        sta b_low               ; n - 1 to n - 6 (b_pos: k)
        ldy mux_count
        .for c_k in range(1, HARDWARE + 1)
        ldx plan_ix - c_k,y
        lda obj_pri,x           ; (by the place in the bank,
        cmp b_low               ; in both)
        bcs +
        sta b_low
        lda #c_k
        sta b_pos
+
        .endfor
        tya                     ; its entry: n - k
        sec
        sbc b_pos
        sta b_pos
        inc b_valid
        ldy b_o
_known:
        lda obj_pri,y           ; (Y: b_o)
        cmp b_low
        beq _self               ; not higher: b_o leaves
        bcc _self
        ldy b_pos               ; entry b_pos leaves, b_o in
        lda plan_ix,y           ; its place
        sec
        sbc obj_base
        ldx left_n
        sta left_list,x
        inc left_n
        lda b_o
        clc
        adc obj_base
        sta plan_ix,y
        lda b_key
        sta plan_y,y
        lda #0                  ; the six have changed
        sta b_valid
        ldx b_i
        rts
_self:
        lda b_o
        ldx left_n
        sta left_list,x
        inc left_n
        ldx b_i
        rts

; After the plan: the objects the plan before left out
; have their class again, those this one left out their
; class + STARVE, for the next plan; this list becomes the
; one before. obj_pri is kept for both banks' places.
priorities:
        ldx prev_n
        beq +
-       ldy prev_list - 1,x
        lda obj_class,y
        sta obj_pri,y
        sta obj_pri + OBJ_BANK,y
        dex
        bne -
+       ldx left_n
        stx prev_n
        beq +
-       ldy left_list - 1,x
        tya
        sta prev_list - 1,x
        lda obj_class,y
        ora #STARVE
        sta obj_pri,y
        sta obj_pri + OBJ_BANK,y
        dex
        bne -
+       rts

        .cerror STARVE != 4, "priorities: ORA"

; Before line 50: the plan's first six entries on sprites
; 2-7, unrolled (the others off); $d010 from the ship's
; bits and theirs, $d01c (all multicolour but the ship's
; accent), $d015.
first_sprites:
        lda ship_bits
        sta d010_now
        lda #%11111110
        sta $d01c
        ldx mux_count
        .for f_i in range(HARDWARE)
        cpx #f_i + 1
        bcs +
        jmp _offs               ; fewer: the rest off
+       ldy plan_ix + f_i       ; entry f_i: sprite 2 + f_i
        lda obj_y,y
        sta $d001 + 2 * (2 + f_i)
        lda obj_x,y
        sta $d000 + 2 * (2 + f_i)
        lda obj_block,y
        sta POINTERS_A + 2 + f_i
        sta POINTERS_B + 2 + f_i
        lda obj_colour,y
        sta $d027 + 2 + f_i
        lda obj_xh,y
        and #1 << (2 + f_i)
        ora d010_now
        sta d010_now
        .endfor
        ldx #HARDWARE
        bne _on
_offs:
        stx b_i                 ; X: the first one off
-       lda entry_sprite,x
        tax
        jsr sprite_off
        inc b_i
        ldx b_i
        cpx #HARDWARE
        bne -
        ldx mux_count
_on:
        lda enable              ; on: the first X
        ora first_on,x
        sta enable
        sta $d015
        lda d010_now
        sta $d010
        rts

first_on:                       ; sprites 2 to 2 + X - 1
        .for f_n in range(HARDWARE + 1)
        .byte ((1 << f_n) - 1) << 2
        .endfor

; At the start of the level: no objects in either bank,
; the orders 4-21 and 0-3, 22, 23, no one left out before,
; no plan.
init_objects:
        lda #0
        sta obj_base
        sta mux_ready
        sta mux_count
        ldx #2 * OBJ_BANK - 1
-       lda #NONE
        sta obj_y,x
        lda #0
        sta obj_x,x
        sta obj_xh,x
        sta obj_block,x
        sta obj_colour,x
        dex
        bpl -
        sta prev_n              ; none left out before
        lda #PLASMA_COLOUR      ; the plasma's places: their
        ldx #ESHOTS - 1         ; its colour
-       sta PLASMA_A,x
        sta PLASMA_B,x
        dex
        bpl -
        ldx #OBJECTS - 1
-       lda init_order,x
        sta order,x
        lda obj_class,x         ; priorities: the class
        sta obj_pri,x
        sta obj_pri + OBJ_BANK,x
        dex
        bpl -
        rts

init_order:                     ; order_v, then order_s
        .for i_o in range(FIRST_ENEMY, FIRST_SAT)
        .byte i_o
        .endfor
        .byte 0, 1, 2, 3, FIRST_SAT, FIRST_MISSILE
        .cerror FIRST_SAT != FIRST_ESHOT + ESHOTS, "order_s"
        .cerror FIRST_MISSILE != OBJECTS - 1, "order_s"

PLASMA_A = obj_colour + FIRST_ESHOT
PLASMA_B = PLASMA_A + OBJ_BANK

; All sprites off (the end of the level).
sprites_all_off:
        lda #0
        sta $d015
        sta mux_ready
        rts

; Entry I: its sprite (2 + I mod 6), 2 x that, its bit.
entry_sprite:
        .for e_i in range(OBJECTS)
        .byte 2 + e_i % HARDWARE
        .endfor
entry_reg:
        .for e_i in range(OBJECTS)
        .byte 2 * (2 + e_i % HARDWARE)
        .endfor
entry_bit:
        .for e_i in range(OBJECTS)
        .byte 1 << (2 + e_i % HARDWARE)
        .endfor
