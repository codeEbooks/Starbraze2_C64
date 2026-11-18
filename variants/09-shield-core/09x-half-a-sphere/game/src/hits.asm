; The hits: the ship's shots against the Varkon, the Varkon
; and their plasma against the ship; the missile and the
; blasts against the Varkon, the ship against the capsules.
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
;    A laser flies on (it hurts each Varkon once: shot_pl,
;    shot_ph), a Gauss shot bursts (start_blast). The
;    missile is a point too (m_hx, m_hy: its nose). A blast
;    is a box, tried once, in the frame after it is armed
;    (bl_*, copied to bn_*): each Varkon in it but the one
;    its shot met loses its damage.
;  - The ship is a box (its ship's: ship_box_*). A Varkon's
;    box on it: the ship loses a notch (hurt) and the Varkon
;    explodes (a boss's part does not). A plasma shot's
;    middle in it (ship_pbox_*: the box grown by half the
;    shot): a notch, and the shot ends. The ship can be hit
;    only when it flies and does not blink; after a hit it
;    blinks.
;    It takes a capsule (its box on the ship's) when it
;    flies, blinking too.
; To try few: the targets are made once a frame
; (hit_prepare), with the lines a Varkon must be on to meet
; one of them (near_top, near_span); most Varkon are not.

; The targets of this frame: the lines of the shots' points
; (hit_x, hit_y: the shots keep them as they fly, ship.asm;
; $ff: none), of the missile's (m_hy), of the blast's box if
; one is tried (blast_now): hs_top and hs_bottom; the ship's
; boxes if it flies (it takes capsules; sb_on: and does not
; blink, it can be hit); the lines to try.
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
        lda m_hy                ; the missile's point
        cmp #$ff
        beq +
        jsr hs_line
+       lda blast_now           ; the blast's box
        beq +
        lda bn_top
        jsr hs_line
        ldx bn_bottom
        dex
        txa
        jsr hs_line
+       lda #0                  ; the ship: flying? not
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

; Line A among the targets' (hs_top, hs_bottom).
hs_line:
        cmp hs_top
        bcs +
        sta hs_top
+       cmp hs_bottom
        bcc +
        sta hs_bottom
+       rts

; Varkon X (object Y, on the screen, flying, A: its y
; register - near_top): its box against the shots' points,
; the missile's, the blast's box, then against the ship. A
; shot in it: shot_hit; the missile: missile_hit; in the
; blast: its damage; on the ship: contact. Y kept.
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
        lda m_on                ; the missile's point?
        beq +
        lda m_hy
        sec
        sbc e_top
        cmp e_h
        bcs +
        lda m_hx
        sec
        sbc e_left
        cmp e_w
        bcs +
        jsr missile_hit
        lda en_on,x
        cmp #BOOM
        beq _done
+       lda blast_now           ; in the blast?
        beq _ship
        cpx bn_skip             ; (not the one it burst on)
        beq _ship
        lda e_top               ; the boxes overlap?
        cmp bn_bottom
        bcs _ship
        adc e_h                 ; (C = 0)
        cmp bn_top
        beq _ship
        bcc _ship
        lda e_left
        cmp bn_right
        bcs _ship
        adc e_w                 ; (C = 0)
        cmp bn_left
        beq _ship
        bcc _ship
        lda bn_dmg
        jsr damage
        lda en_on,x
        cmp #BOOM
        beq _done
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

; Shot Y has hit Varkon X: a laser flies on (a Varkon it has
; hurt already: nothing), a Gauss shot bursts, the others
; end (and hit nothing else); the Varkon loses the kind's
; damage. X kept.
shot_hit:
        sty fv_shot
        lda shot_kind,y
        tay
        lda en_kind,x           ; a shield's segment
        cmp #KIND_SEGMENT       ; stops even a laser (and
        beq _stop               ; is hurt by it)
        lda shot_pierce,y
        beq _stop
        ldy fv_shot             ; a laser: once a Varkon
        lda varkon_bit,x        ; (its bit: shot_pl for
        cpx #8                  ; 0-7, shot_ph for 8-11)
        bcs _high
        and shot_pl,y
        bne _same               ; hurt already
        lda varkon_bit,x
        ora shot_pl,y
        sta shot_pl,y
        jmp _damage
_high:
        and shot_ph,y
        bne _same
        lda varkon_bit,x
        ora shot_ph,y
        sta shot_ph,y
        jmp _damage
_same:
        rts
_stop:
        lda shot_blast,y
        bne _burst
        ldy fv_shot             ; it ends
        lda #0
        sta shot_mask,y
        lda #$ff
        sta hit_y,y
        bne _damage
_burst:
        stx bl_skip             ; it bursts: a blast
        stx v_i
        ldx fv_shot
        jsr start_blast
        ldx v_i
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

; The missile has hit Varkon X: it ends, its damage.
missile_hit:
        lda #0
        sta m_on
        lda #$ff
        sta m_hy
        lda #MISSILE_DAMAGE
        bne damage

varkon_bit:                     ; Varkon X's bit (0-7, 8-11)
        .for vb_i in range(ENEMIES)
        .byte 1 << (vb_i % 8)
        .endfor

; Varkon X explodes: its explosion from its first frame, its
; points to the score, its sound; a tower's core takes its
; field with it. X kept.
destroy:
        lda #BOOM
        sta en_on,x
        lda #0
        sta en_left,x
        sta en_flash,x
        ldy en_kind,x
        jsr score_add
        lda en_beh,x
        cmp #STAND
        bne +
        jsr fields_down
+       lda #FX_BOOM
        jmp sfx_start

; Varkon X on the ship: it explodes (not a boss's part: it
; stays; nor a tower's core), the ship loses a notch (and is
; not tried again this frame). X kept.
contact:
        lda #0
        sta sb_on
        lda en_beh,x
        cmp #BOSS
        bcs +
        jsr destroy
+       lda #1
        jmp hurt

; Capsule X (object Y, on the screen; the ship flies): its
; box on the ship's (sb_*)? Then the ship takes it (C = 1).
; X and Y kept.
pickup:
        lda obj_y,y
        clc
        adc #CAP_BOX_Y
        cmp sb_bottom
        bcs _no
        adc #CAP_BOX_H          ; (C = 0)
        cmp sb_top
        beq _no
        bcc _no
        lda obj_xh,y            ; x register / 2
        lsr a
        lda obj_x,y
        ror a
        clc
        adc #CAP_BOX_X
        cmp sb_right
        bcs _no
        adc #CAP_BOX_W          ; (C = 0)
        cmp sb_left
        beq _no
        bcc _no
        lda en_cap,x
        sec
        sbc #1
        jsr take_capsule
        sec
        rts
_no:
        clc
        rts

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
