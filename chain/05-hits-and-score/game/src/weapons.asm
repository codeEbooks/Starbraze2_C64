; The weapon's volleys.
;
; The weapon is the ship's and its level (weapon, 0-3; here
; always 0: no capsules raise it).
; w_index = ship * 4 + level picks its row of the tables
; (tables.inc, from ships.py): frames between two volleys
; (w_period), the volley's shots (w_count from entry w_first
; of v_kind, v_dx, v_dy: each from the ship's nose,
; SHOT_START).
; A volley leaves only when all its shots have a free place
; among the four (objects 0-3).
;
; A shot of a kind (shot_*): its halves (a double bolt has
; two, each ends on the rock alone), its x speed, its y
; speed (the spread's shots climb or dive a line a frame;
; past the playfield they end).

; (init_weapons, the start of a game, is in title.asm.)

; The weapon's row (w_index) and the ship's speed from its
; ship, its level, its S capsules (always 0 here); the HUD
; again. X kept.
set_weapon:
        lda ship_type
        asl a
        asl a
        ora weapon
        sta w_index
        lda s_caps              ; * 64: into bits 6-7
        lsr a
        ror a
        ror a
        ldy ship_type
        clc
        adc ship_speed_lo,y
        sta cur_speed_lo
        lda ship_speed_hi,y
        adc #0
        sta cur_speed_hi
        lda #1
        sta hud_dirty
        rts

        .cerror SPEED_STEP != 64, "set_weapon: * 64"
        .cerror SPEED_STEPS > 3, "set_weapon: two bits"

; Fire: the weapon's volley, if all its shots have a free
; place (else nothing: the next frame again). Then the wait
; to the next volley.
fire:
        ldy w_index
        lda w_count,y
        sta fv_left
        lda w_first,y
        sta fv_entry
        ldx #3                  ; the free places
        lda #0
-       ldy shot_mask,x
        bne +
        clc
        adc #1
+       dex
        bpl -
        cmp fv_left
        bcs +
        rts                     ; no room for the volley
+       ldx #0                  ; X: the places, in order
_shot:
        lda shot_mask,x         ; the next free one
        beq +
        inx
        bne _shot
+       ldy fv_entry            ; from the nose + dx, dy
        clc
        lda ship_x
        adc #SHOT_START
        sta px
        lda ship_xh
        adc #0
        sta px + 1
        clc
        lda px
        adc v_dx,y
        sta px
        bcc +
        inc px + 1
+       lda ship_y
        clc
        adc v_dy,y
        sta py
        lda v_kind,y
        jsr shot_begin
        inc fv_entry
        dec fv_left
        bne _shot
        ldy w_index             ; the wait
        lda w_period,y
        sta cooldown
        rts

; Shot X of kind A leaves from (px, py): its bytes, its y
; register, its point and picture. X kept.
shot_begin:
        sta shot_kind,x
        tay
        lda shot_halves,y
        sta shot_mask,x
        lda shot_vy,y
        sta shot_dy,x
        lda shot_colour,y
        sta shot_col,x
        lda px
        sta shot_x,x
        lda px + 1
        sta shot_xh,x
        lda py
        sta shot_y,x
        clc                     ; its point (hits.asm): x
        lda px                  ; register / 2 of the tip
        adc shot_tip,y
        sta v_tmp
        lda px + 1
        adc #0
        lsr a
        lda v_tmp
        ror a
        sta hit_x,x
        lda shot_block,y        ; its picture: all halves
        sta shot_blk,x
        lda py                  ; its y register
        clc
        adc #50
        sta shot_yr,x
        lda py                  ; its point's line
        clc
        adc shot_mid0,y
        sta hit_y,x
        lda py                  ; in the corridor?
        cmp air_from,y
        bcc +
        cmp air_to,y
        lda #1
        bcc ++
+       lda #0
+       sta shot_air,x
        rts
