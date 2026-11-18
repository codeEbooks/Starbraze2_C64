; The hits: the ship's shots against the Varkon, the Varkon
; and their plasma against the ship.
;
; Boxes, in software: the VIC-II's collision register cannot
; say which object of the multiplexer met which. They are
; tried at the end of the turn, while the Varkon move for
; the next frame (update_varkon): each Varkon on the screen,
; at its new place, against the ship's shots and the ship as
; this frame shows them. Places are in the sprites' units: y
; the y register; x the x register / 2 (half the screen's
; pixels: a byte, a multicolour pixel).
;  - A shot is a point: the tip of its bolt, the middle of
;    what is left of it (shot_tip, shot_mid). In a Varkon's
;    box (its kind's: kind_box_*) it ends and does its
;    damage (shot_damage); no hits left, the Varkon
;    explodes.
;  - The ship is a box (its ship's: ship_box_*). A Varkon's
;    box on it: the ship loses a notch (hurt) and the Varkon
;    explodes. A plasma shot's middle in it (ship_pbox_*:
;    the box grown by half the shot): a notch, and the shot
;    ends. The ship can be hit only when it flies and does
;    not blink; after a hit it blinks.
; To try few: the targets are made once a frame
; (hit_prepare), with the lines a Varkon must be on to meet
; one of them (near_top, near_span); most Varkon are not.

; The targets of this frame: the lines of the shots' points
; (hit_x, hit_y: the shots keep them as they fly, ship.asm;
; $ff: none): hs_top and hs_bottom; the ship's boxes if it
; flies (sb_on: and does not blink, it can be hit); the
; lines to try.
hit_prepare:
        lda #$ff                ; no shots yet: top > bottom
        sta hs_top
        lda #0
        sta hs_bottom
        ldx #3
_shot:
        lda hit_y,x
        cmp #$ff
        beq _next
        cmp hs_top
        bcs +
        sta hs_top
+       cmp hs_bottom
        bcc _next
        sta hs_bottom
_next:
        dex
        bpl _shot
        lda #0                  ; the ship: flying? not
        sta sb_on               ; blinking?
        lda ship_mode
        bne _near
        lda ship_blink
        bne +
        inc sb_on
+       ldy ship_type
        lda ship_x              ; x register / 2
        clc
        adc #24
        sta v_tmp
        lda ship_xh
        adc #0
        lsr a
        lda v_tmp
        ror a
        sta v_tmp
        clc
        adc ship_box_x,y
        sta sb_left
        clc
        adc ship_box_w,y
        sta sb_right
        lda v_tmp
        clc
        adc ship_pbox_x,y
        sta pb_left
        lda ship_pbox_w,y
        sta pb_w
        lda ship_y              ; y register
        clc
        adc #50
        sta v_tmp
        clc
        adc ship_box_y,y
        sta sb_top
        clc
        adc ship_box_h,y
        sta sb_bottom
        lda v_tmp
        clc
        adc ship_pbox_y,y
        sta pb_top
        lda ship_pbox_h,y
        sta pb_h
_near:
        lda hs_top              ; the lines: from the top
        ldx hs_bottom           ; target - 20 to the lowest
        ldy sb_on
        beq +
        cmp sb_top              ; the ship's top higher?
        bcc +
        lda sb_top
+       sta near_top
        cpy #0
        beq +
        cpx sb_bottom           ; its bottom line lower?
        bcs +
        ldx sb_bottom
        dex
+       stx v_tmp
        lda near_top
        cmp #$ff
        beq _none               ; no targets
        sec
        sbc #20
        sta near_top
        lda v_tmp               ; span: lowest - near_top
        sec                     ; + 1
        sbc near_top
        clc
        adc #1
        sta near_span
        rts
_none:
        lda #0                  ; none: no Varkon is near
        sta near_span
        rts

; Varkon X (object Y, on the screen, flying, A: its y
; register - near_top): its box against the shots' points,
; then against the ship. A shot in it: shot_hit; on the
; ship: contact. Y kept.
hit_enemy:
        sty v_j
        lda obj_y,y             ; its box: top
        ldy en_kind,x
        clc
        adc kind_box_y,y
        sta e_top
        lda kind_box_h,y
        sta e_h
        lda kind_box_w,y
        sta e_w
        lda en_xh,x             ; x register / 2 (shown:
        lsr a                   ; en_xh is 0 or 1)
        lda en_x,x
        ror a
        clc
        adc kind_box_x,y
        sta e_left
        lda hs_bottom           ; the shots: below its top?
        cmp e_top
        bcc _no_shot
        lda e_top               ; its bottom over their top?
        clc
        adc e_h
        cmp hs_top
        beq _no_shot
        bcs _shots
_no_shot:
        jmp _ship
_shots:
        .for h_k in range(4)
        lda hit_y + h_k         ; shot k's point in the box?
        sec
        sbc e_top
        cmp e_h
        bcs +
        lda hit_x + h_k
        sec
        sbc e_left
        cmp e_w
        bcs +
        ldy #h_k
        jsr shot_hit
        lda en_on,x             ; exploding: no more
        cmp #BOOM
        bne +
        jmp _done
+
        .endfor
_ship:
        lda sb_on               ; the ship can be hit?
        beq _done
        lda e_top               ; the boxes overlap?
        cmp sb_bottom
        bcs _done
        adc e_h                 ; (C = 0)
        cmp sb_top
        beq _done
        bcc _done
        lda e_left
        cmp sb_right
        bcs _done
        adc e_w                 ; (C = 0)
        cmp sb_left
        beq _done
        bcc _done
        jsr contact
_done:
        ldy v_j
        rts

; Shot Y has hit Varkon X: it ends (and hits nothing else);
; the Varkon loses the kind's damage. X kept.
shot_hit:
        sty fv_shot
        lda #0
        sta shot_mask,y
        lda #$ff
        sta hit_y,y
_damage:
        ldy fv_shot
        lda shot_kind,y
        tay
        lda shot_damage,y
; Varkon X loses A hits: none left, it explodes, else it
; flashes white. X kept.
damage:
        sta v_tmp
        lda en_life,x
        sec
        sbc v_tmp
        sta en_life,x
        beq _down
        bcc _down
        lda #FLASH_FRAMES
        sta en_flash,x
        rts
_down:
        jmp destroy

; Varkon X explodes: its explosion from its first frame, its
; points to the score. X kept.
destroy:
        lda #BOOM
        sta en_on,x
        lda #0
        sta en_left,x
        sta en_flash,x
        ldy en_kind,x
        jsr score_add
        rts

; Varkon X on the ship: it explodes, the ship loses a notch
; (and is not tried again this frame). X kept.
contact:
        lda #0
        sta sb_on
        jsr destroy
        lda #1
        jmp hurt

; Plasma shot X (object Y, on the screen): its middle in the
; ship's box? Then the shot ends and the ship loses a notch.
; X and Y kept.
plasma_hit:
        lda obj_y,y
        sec
        sbc pb_top
        cmp pb_h
        bcs _miss
        lda obj_xh,y            ; x register / 2 ($ff or 0)
        lsr a
        lda obj_x,y
        ror a
        sec
        sbc pb_left
        cmp pb_w
        bcs _miss
        lda #0                  ; the shot ends
        sta sh_on,x
        sta sb_on               ; not tried again
        lda #NONE
        sta obj_y,y
        lda #1
        jmp hurt
_miss:
        rts
