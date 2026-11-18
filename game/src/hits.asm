; The hits: the ship's shots against the Varkon, the Varkon {6}
; and their plasma against the ship; the missile and the {6}
; blasts against the Varkon, the ship against the capsules. {6}
;|; The hits: the ship's shots against the Varkon, the Varkon {5-5}
;|; and their plasma against the ship. {5-5}
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
;    A laser flies on (it hurts each Varkon once: shot_pl, {6}
;    shot_ph), a Gauss shot bursts (start_blast). The {6}
;    missile is a point too (m_hx, m_hy: its nose). A blast {6}
;    is a box, tried once, in the frame after it is armed {6}
;    (bl_*, copied to bn_*): each Varkon in it but the one {6}
;    its shot met loses its damage. {6}
;  - The ship is a box (its ship's: ship_box_*). A Varkon's {8}
;    box on it: the ship loses a notch (hurt) and the Varkon {8}
;    explodes (a boss's part does not). A plasma shot's {8}
;    middle in it (ship_pbox_*: the box grown by half the {8}
;    shot): a notch, and the shot ends. The ship can be hit {8}
;    only when it flies and does not blink; after a hit it {8}
;    blinks. {8}
;|;  - The ship is a box (its ship's: ship_box_*). A Varkon's {5-7}
;|;    box on it: the ship loses a notch (hurt) and the Varkon {5-7}
;|;    explodes. A plasma shot's middle in it (ship_pbox_*: {5-7}
;|;    the box grown by half the shot): a notch, and the shot {5-7}
;|;    ends. The ship can be hit only when it flies and does {5-7}
;|;    not blink; after a hit it blinks. {5-7}
;    It takes a capsule (its box on the ship's) when it {6}
;    flies, blinking too. {6}
; To try few: the targets are made once a frame
; (hit_prepare), with the lines a Varkon must be on to meet
; one of them (near_top, near_span); most Varkon are not.

; The targets of this frame: the lines of the shots' points {6}
; (hit_x, hit_y: the shots keep them as they fly, ship.asm; {6}
; $ff: none), of the missile's (m_hy), of the blast's box if {6}
; one is tried (blast_now): hs_top and hs_bottom; the ship's {6}
; boxes if it flies (it takes capsules; sb_on: and does not {6}
; blink, it can be hit); the lines to try. {6}
;|; The targets of this frame: the lines of the shots' points {5-5}
;|; (hit_x, hit_y: the shots keep them as they fly, ship.asm; {5-5}
;|; $ff: none): hs_top and hs_bottom; the ship's boxes if it {5-5}
;|; flies (sb_on: and does not blink, it can be hit); the {5-5}
;|; lines to try. {5-5}
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
        lda m_hy                ; the missile's point {6}
        cmp #$ff ; {6}
        beq + ; {6}
        jsr hs_line ; {6}
+       lda blast_now           ; the blast's box {6}
        beq + ; {6}
        lda bn_top ; {6}
        jsr hs_line ; {6}
        ldx bn_bottom ; {6}
        dex ; {6}
        txa ; {6}
        jsr hs_line ; {6}
+       lda #0                  ; the ship: flying? not {6}
;|        lda #0                  ; the ship: flying? not {5-5}
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

; Line A among the targets' (hs_top, hs_bottom). {6}
hs_line: ; {6}
        cmp hs_top ; {6}
        bcs + ; {6}
        sta hs_top ; {6}
+       cmp hs_bottom ; {6}
        bcc + ; {6}
        sta hs_bottom ; {6}
+       rts ; {6}

; Varkon X (object Y, on the screen, flying, A: its y {6}
; register - near_top): its box against the shots' points, {6}
; the missile's, the blast's box, then against the ship. A {6}
; shot in it: shot_hit; the missile: missile_hit; in the {6}
; blast: its damage; on the ship: contact. Y kept. {6}
;|; Varkon X (object Y, on the screen, flying, A: its y {5-5}
;|; register - near_top): its box against the shots' points, {5-5}
;|; then against the ship. A shot in it: shot_hit; on the {5-5}
;|; ship: contact. Y kept. {5-5}
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
        lda m_on                ; the missile's point? {6}
        beq + ; {6}
        lda m_hy ; {6}
        sec ; {6}
        sbc e_top ; {6}
        cmp e_h ; {6}
        bcs + ; {6}
        lda m_hx ; {6}
        sec ; {6}
        sbc e_left ; {6}
        cmp e_w ; {6}
        bcs + ; {6}
        jsr missile_hit ; {6}
        lda en_on,x ; {6}
        cmp #BOOM ; {6}
        beq _done ; {6}
+       lda blast_now           ; in the blast? {6}
        beq _ship ; {6}
        cpx bn_skip             ; (not the one it burst on) {6}
        beq _ship ; {6}
        lda e_top               ; the boxes overlap? {6}
        cmp bn_bottom ; {6}
        bcs _ship ; {6}
        adc e_h                 ; (C = 0) {6}
        cmp bn_top ; {6}
        beq _ship ; {6}
        bcc _ship ; {6}
        lda e_left ; {6}
        cmp bn_right ; {6}
        bcs _ship ; {6}
        adc e_w                 ; (C = 0) {6}
        cmp bn_left ; {6}
        beq _ship ; {6}
        bcc _ship ; {6}
        lda bn_dmg ; {6}
        jsr damage ; {6}
        lda en_on,x ; {6}
        cmp #BOOM ; {6}
        beq _done ; {6}
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

; Shot Y has hit Varkon X: a laser flies on (a Varkon it has {6}
; hurt already: nothing), a Gauss shot bursts, the others {6}
; end (and hit nothing else); the Varkon loses the kind's {6}
; damage. X kept. {6}
;|; Shot Y has hit Varkon X: it ends (and hits nothing else); {5-5}
;|; the Varkon loses the kind's damage. X kept. {5-5}
shot_hit:
        sty fv_shot
        lda shot_kind,y ; {6}
        tay ; {6}
        lda en_kind,x           ; a shield's segment {9}
        cmp #KIND_SEGMENT       ; stops even a laser (and {9}
        beq _stop               ; is hurt by it) {9}
        lda shot_pierce,y ; {6}
        beq _stop ; {6}
        ldy fv_shot             ; a laser: once a Varkon {6}
        lda varkon_bit,x        ; (its bit: shot_pl for {6}
        cpx #8                  ; 0-7, shot_ph for 8-11) {6}
        bcs _high ; {6}
        and shot_pl,y ; {6}
        bne _same               ; hurt already {6}
        lda varkon_bit,x ; {6}
        ora shot_pl,y ; {6}
        sta shot_pl,y ; {6}
        jmp _damage ; {6}
_high: ; {6}
        and shot_ph,y ; {6}
        bne _same ; {6}
        lda varkon_bit,x ; {6}
        ora shot_ph,y ; {6}
        sta shot_ph,y ; {6}
        jmp _damage ; {6}
_same: ; {6}
        rts ; {6}
_stop: ; {6}
        lda shot_blast,y ; {6}
        bne _burst ; {6}
        ldy fv_shot             ; it ends {6}
        lda #0
        sta shot_mask,y
        lda #$ff
        sta hit_y,y
        bne _damage ; {6}
_burst: ; {6}
        stx bl_skip             ; it bursts: a blast {6}
        stx v_i ; {6}
        ldx fv_shot ; {6}
        jsr start_blast ; {6}
        ldx v_i ; {6}
_damage:
        ldy fv_shot
        lda shot_kind,y
        tay
        lda shot_damage,y
; Varkon X loses A hits: none left, it explodes (a rock {10}
; splits: its shards), else it flashes white. X kept. {10}
;|; Varkon X loses A hits: none left, it explodes, else it {5-9}
;|; flashes white. X kept. {5-9}
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
        jsr destroy ; {10}
        lda en_kind,x           ; a rock: its two {10}
        cmp #KIND_ROCK          ; shards {10}
        bne + ; {10}
        jmp split ; {10}
+       rts ; {10}
;|        jmp destroy ; {5-9}

; The missile has hit Varkon X: it ends, its damage. {6}
missile_hit: ; {6}
        lda #0 ; {6}
        sta m_on ; {6}
        lda #$ff ; {6}
        sta m_hy ; {6}
        lda #MISSILE_DAMAGE ; {6}
        bne damage ; {6}

varkon_bit:                     ; Varkon X's bit (0-7, 8-11) {6}
        .for vb_i in range(ENEMIES) ; {6}
        .byte 1 << (vb_i % 8) ; {6}
        .endfor ; {6}

; Varkon X explodes: its explosion from its first frame, its {9}
; points to the score, its sound; a tower's core takes its {9}
; field with it. X kept. {9}
;|; Varkon X explodes: its explosion from its first frame, its {7-8}
;|; points to the score, its sound. X kept. {7-8}
;|; Varkon X explodes: its explosion from its first frame, its {5-6}
;|; points to the score. X kept. {5-6}
destroy:
        lda #BOOM
        sta en_on,x
        lda #0
        sta en_left,x
        sta en_flash,x
        ldy en_kind,x
        jsr score_add
        lda en_beh,x ; {9}
        cmp #STAND ; {9}
        bne + ; {9}
        jsr fields_down ; {9}
+       lda #FX_BOOM ; {9}
;|        lda #FX_BOOM ; {7-8}
        jmp sfx_start ; {7}
;|        rts ; {5-6}

; Varkon X on the ship: it explodes (not a boss's part: it {9}
; stays; nor a tower's core), the ship loses a notch (and is {9}
; not tried again this frame). X kept. {9}
;|; Varkon X on the ship: it explodes (not a boss's part: it {8-8}
;|; stays), the ship loses a notch (and is not tried again {8-8}
;|; this frame). X kept. {8-8}
;|; Varkon X on the ship: it explodes, the ship loses a notch {5-7}
;|; (and is not tried again this frame). X kept. {5-7}
contact:
        lda #0
        sta sb_on
        lda en_beh,x ; {8}
        cmp #BOSS ; {8}
        bcs + ; {8}
        jsr destroy
+       lda #1 ; {8}
;|        lda #1 ; {5-7}
        jmp hurt

; Capsule X (object Y, on the screen; the ship flies): its {6}
; box on the ship's (sb_*)? Then the ship takes it (C = 1). {6}
; X and Y kept. {6}
pickup: ; {6}
        lda obj_y,y ; {6}
        clc ; {6}
        adc #CAP_BOX_Y ; {6}
        cmp sb_bottom ; {6}
        bcs _no ; {6}
        adc #CAP_BOX_H          ; (C = 0) {6}
        cmp sb_top ; {6}
        beq _no ; {6}
        bcc _no ; {6}
        lda obj_xh,y            ; x register / 2 {6}
        lsr a ; {6}
        lda obj_x,y ; {6}
        ror a ; {6}
        clc ; {6}
        adc #CAP_BOX_X ; {6}
        cmp sb_right ; {6}
        bcs _no ; {6}
        adc #CAP_BOX_W          ; (C = 0) {6}
        cmp sb_left ; {6}
        beq _no ; {6}
        bcc _no ; {6}
        lda en_cap,x ; {6}
        sec ; {6}
        sbc #1 ; {6}
        jsr take_capsule ; {6}
        sec ; {6}
        rts ; {6}
_no: ; {6}
        clc ; {6}
        rts ; {6}

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

; Rock X destroyed (it explodes): two shards from its {10}
; place, one on its path up, one down (SHARD_DY lines {10}
; lower), in the first free Varkon (none free: no shard). {10}
; X kept. {10}
split: ; {10}
        lda #PATH_SHARD_UP ; {10}
        sta sp_path ; {10}
        lda #SHARD_DY_UP ; {10}
        jsr shard ; {10}
        lda #PATH_SHARD_DOWN ; {10}
        sta sp_path ; {10}
        lda #SHARD_DY_DOWN ; {10}
shard: ; {10}
        sta sp_dy ; {10}
        ldy #0                  ; the first free Varkon {10}
-       lda en_on,y ; {10}
        beq _free ; {10}
        iny ; {10}
        cpy #ENEMIES ; {10}
        bne - ; {10}
        rts ; {10}
_free: ; {10}
        lda #FLYING ; {10}
        sta en_on,y ; {10}
        lda #KIND_SHARD ; {10}
        sta en_kind,y ; {10}
        lda #PATH ; {10}
        sta en_beh,y ; {10}
        lda kind_life + KIND_SHARD ; {10}
        sta en_life,y ; {10}
        lda kind_block + KIND_SHARD ; {10}
        sta en_block,y ; {10}
        lda kind_pmask + KIND_SHARD ; {10}
        sta en_pmask,y ; {10}
        lda kind_colour + KIND_SHARD ; {10}
        sta en_colour,y ; {10}
        lda #0 ; {10}
        sta en_period,y ; {10}
        sta en_fire,y ; {10}
        sta en_cap,y ; {10}
        sta en_delay,y ; {10}
        sta en_flash,y ; {10}
        sta en_xf,y ; {10}
        sta en_yf,y ; {10}
        lda en_x,x              ; the rock's place {10}
        sta en_x,y ; {10}
        lda en_xh,x ; {10}
        sta en_xh,y ; {10}
        lda en_y,x ; {10}
        clc ; {10}
        adc sp_dy ; {10}
        sta en_y,y ; {10}
        lda sp_path ; {10}
        sta en_seg,y ; {10}
        stx sp_rock ; {10}
        tya ; {10}
        tax ; {10}
        jsr load_stretch        ; its first stretch {10}
        jsr wave_pri            ; its priority {10}
        ldx sp_rock ; {10}
        rts ; {10}
