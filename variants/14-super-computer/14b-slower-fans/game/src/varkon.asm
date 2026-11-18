; The Varkon: the waves of the level's script; the ship's
; shots and the ship against them (hits.asm); their
; explosions.
;
; A wave comes in when the camera reaches its column
; (wave_col): its members take free Varkon. A Varkon has a
; kind (kind_*) and so a behaviour:
;  - PATH, a flyer: it follows its path on the screen (the
;    members of a wave one after the other, wave_spacing
;    frames apart, each wave_dy lines below the one before).
;    A path is a list of stretches: so many frames (0: the
;    end) at a velocity in 256ths of a pixel a frame;
;  - HOP, a leaper, and TURRET, a flak gun: they stand on
;    the rock and move with it (each frame their x goes
;    back by the camera's move, cam_step). The leaper walks
;    to the left in hops (leap), the turret turns its barrel
;    to the ship (aim).
; A Varkon on the screen fires (its kind's period) a plasma
; shot (fire_plasma). Hit by the ship's shots it loses their
; damage; none left, it explodes (EXPLOSION_FRAMES frames,
; the fireball of the ship's explosion) and its points go to
; the score. It leaves at its path's end or past the left
; edge; a shot past either edge or out of the playfield.
;
; A carrier leaves its capsule where it exploded (en_cap: 1
; + its letter, the wave's): the capsule stays on its place
; of the rock, its pod's colour turning, until the ship
; takes it (hits.asm, weapons.asm) or it goes past the left
; edge.
;
; All this at the end of the turn, for the next frame: the
; objects go into the other bank as they move. An object is
; shown if its x register is 1-343 (the screen and a little
; border); one not shown gets y 255 (its other fields are
; never read). Only a Varkon shown fires and can be hit.

PATH    = 0                     ; behaviours (kind_beh)
HOP     = 1
TURRET  = 2
STAND   = 4                     ; a tower's core,
FIELD   = 5                     ; its field (BOSS = 3: boss)
MINE    = 6                     ; level 3's mine
FLYING  = 1                     ; en_on: 0 free, 1 flying,
BOOM    = 2                     ; 2 exploding, 3 a capsule
CAPSULE = 3

; At the start of the level: none.
init_varkon:
        lda #0
        sta wave_ptr
        sta anim
        tax                     ; all their bytes 0: the
-       sta en_on,x             ; first page, then the rest
        inx
        bne -
        ldx #VARKON_END - en_on - 256
-       sta en_on + 255,x
        dex
        bne -
        ldx #MORE_END - en_life - 1
-       sta en_life,x           ; then en_life to MORE_END
        dex
        bpl -
        ldx #ENEMIES - 1        ; and the capsules
-       sta en_cap,x
        dex
        bpl -
        rts

        .cerror (en_on & $ff) != 0, "init_varkon: a page"
        .cerror VARKON_END - en_on > 512, "init_varkon"

; One frame: the camera's move, the blast to try (armed in
; the frame before), the targets, the shots, the boss, level
; 2's beams, the Varkon, the waves; the objects 4-21 for the
; next frame.
update_varkon:
        inc anim
        lda anim                ; the Varkon's picture:
        lsr a                   ; anim / 8 AND 3
        lsr a
        lsr a
        and #%00000011
        sta anim3
        lda obj_base            ; the next frame's bank
        eor #OBJ_BANK
        sta v_base
        sec                     ; the camera's move to the
        lda next_frac           ; next frame (camera_plan
        sbc cam_frac            ; made it): a pixel at most,
        sta cam_step            ; or back to the column's
        lda next                ; last pixel (it waits)
        sbc camera
        sta cam_step + 1
        lda next + 1
        sbc camera + 1
        sta cam_step + 2
        lda blast_armed         ; a blast armed: tried now
        sta blast_now
        beq +
        ldx #5                  ; its box, its damage, the
-       lda bl_left,x           ; Varkon to skip
        sta bn_left,x
        dex
        bpl -
        lda #0
        sta blast_armed
+       jsr hit_prepare         ; the ship's shots, the ship
        jsr move_plasma
        jsr boss_update         ; the boss, its parts
        jsr beam_step           ; level 2's beams
        jsr move_varkon
        jmp start_waves

; The shots on: by their x velocity (whole pixels, signed),
; their y velocity (256ths); gone past either edge (the x
; register 0 or less, 344 or more) or out of the playfield.
; One shown may hit the ship. Their objects (16-21; their
; colour is always the plasma's: init_objects), placed as
; plasma_object does.
move_plasma:
        lda anim                ; their picture: anim / 4
        lsr a                   ; AND 3
        lsr a
        and #%00000011
        clc
        adc #PLASMA_BLOCK
        sta v_tmp + 1
        lda v_base
        clc
        adc #FIRST_ESHOT
        tay                     ; Y: the object
        ldx #0
_shot:
        lda sh_on,x
        bne +
        jmp _none
+       lda sh_vx,x             ; x: 16 bits, + vx signed
        bmi _left
        clc
        adc sh_x,x
        sta sh_x,x
        bcc _y
        inc sh_xh,x
        bcs _y
_left:
        clc
        adc sh_x,x
        sta sh_x,x
        bcs _y
        dec sh_xh,x
_y:
        lda sh_vyl,x            ; y, if it moves
        ora sh_vyh,x
        beq _place
        clc
        lda sh_yf,x
        adc sh_vyl,x
        sta sh_yf,x
        lda sh_y,x
        adc sh_vyh,x
        sta sh_y,x
        cmp #VARKON_Y_MAX + 1
        bcs _out
_place:
        lda sh_xh,x             ; the x register 1-343?
        bmi _out
        bne _high
        lda sh_x,x
        beq _out
        sta obj_x,y
        lda #0
        beq _shown
_high:
        cmp #1
        bne _out
        lda sh_x,x
        cmp #344 - 256
        bcs _out
        sta obj_x,y
        lda #$ff
_shown:
        sta obj_xh,y
        lda sh_y,x
        clc
        adc #50
        sta obj_y,y
        lda v_tmp + 1
        sta obj_block,y
        lda sb_on               ; the ship can be hit?
        beq _next
        jsr plasma_hit
        jmp _next
_out:
        lda #0                  ; gone
        sta sh_on,x
_none:
        lda #NONE
        sta obj_y,y
_next:
        iny
        inx
        cpx #ESHOTS
        beq +
        jmp _shot
+       rts

; Shot X's object Y, if its x register is 1-343; C = 1 if it
; is gone (past an edge).
plasma_object:
        lda sh_xh,x
        bmi _gone
        bne _high
        lda sh_x,x
        beq _gone
        sta obj_x,y
        lda #0
        beq _shown
_high:
        cmp #1
        bne _gone
        lda sh_x,x
        cmp #344 - 256
        bcs _gone
        sta obj_x,y
        lda #$ff
_shown:
        sta obj_xh,y
        lda sh_y,x
        clc
        adc #50
        sta obj_y,y
        lda v_tmp + 1
        sta obj_block,y
        clc
        rts
_gone:
        sec
        rts

; The Varkon: waiting, or moving by their behaviour, or
; exploding, or a capsule; on the screen they can be hit,
; and fire; their objects (4-15). X: the Varkon, Y: its
; object. The flyers, the most, have a way of their own
; (_path), with their place and picture in it; the leapers
; and the turrets share the rest (_ground).
move_varkon:
        lda v_base
        clc
        adc #FIRST_ENEMY
        tay
        ldx #0                  ; in order: the first free
_one:                           ; shot goes to the first
        lda en_on,x
        beq _none
        cmp #BOOM
        bcc +
        jmp _boom               ; exploding, or a capsule
+       lda en_delay,x
        beq _move
        dec en_delay,x          ; still waiting its turn
_none:
        lda #NONE
        sta obj_y,y
        jmp _next
_move:
        clc                     ; x: 24 bits
        lda en_xf,x
        adc en_vxl,x
        sta en_xf,x
        lda en_x,x
        adc en_vxh,x
        sta en_x,x
        lda en_xh,x
        adc en_vxs,x
        sta en_xh,x
        lda en_beh,x
        beq _path
        jmp _ground
_path:
        lda en_vyl,x            ; y: 16 bits, if it moves
        ora en_vyh,x
        beq +
        clc
        lda en_yf,x
        adc en_vyl,x
        sta en_yf,x
        lda en_y,x
        adc en_vyh,x
        sta en_y,x
+       dec en_left,x           ; the stretch's frames
        bne _place
        inc en_seg,x            ; the next stretch
        sty v_j
        jsr load_stretch
        ldy v_j
        lda en_left,x
        bne _place
        jmp _off                ; the path's end
_place:
        lda en_xh,x             ; the x register: 0 or less,
        bmi _gone               ; gone; 1-343 shown
        bne _high
        lda en_x,x
        beq _gone
        sta obj_x,y
        lda #0
        beq _shown
_high:
        cmp #1
        bne _hidden
        lda en_x,x
        cmp #344 - 256
        bcs _hidden
        sta obj_x,y
        lda #$ff
_shown:
        sta obj_xh,y
        lda en_y,x
        clc
        adc #50
        sta obj_y,y
        sec                     ; near the targets?
        sbc near_top
        cmp near_span
        bcs _picture
        jsr hit_enemy           ; hit, or on the ship
        lda en_on,x
        cmp #BOOM
        bne _picture
        jmp _boomed             ; it explodes from now
_picture:
        lda anim3               ; its picture by the frame,
        and en_pmask,x          ; of four or of two
        clc
        adc en_block,x
        sta obj_block,y
_colour:
        lda en_flash,x          ; just hit: white
        bne _white
        lda en_colour,x
        sta obj_colour,y
_fire:
        lda en_period,x         ; fire?
        beq _later
        dec en_fire,x
        bne _later
        sta en_fire,x
        stx v_i
        sty v_j
        jsr fire_plasma
        ldx v_i
        ldy v_j
        jmp _next
_white:
        dec en_flash,x
        lda #1
        sta obj_colour,y
        bne _fire
_later:
        jmp _next
_gone:
        jmp _off
_hidden:
        lda #NONE               ; past the right edge
        sta obj_y,y
        jmp _next
_ground:
        lda en_beh,x            ; a boss's part: the
        cmp #BOSS               ; camera is still (arena)
        beq +
        jsr with_rock           ; on the rock: the camera
        lda en_beh,x
+       cmp #HOP
        bne +                   ; a turret: no more
        sty v_j                 ; a leaper: its hop
        jsr leap
        ldy v_j
+       jsr varkon_object       ; on the screen?
        bcs _gone               ; past the left edge
        cmp #NONE
        beq _hidden
        sec                     ; near the targets?
        sbc near_top
        cmp near_span
        bcs +
        lda en_beh,x            ; not a field: the
        cmp #FIELD              ; shots go through it
        beq +
        jsr hit_enemy
        lda en_on,x
        cmp #BOOM
        beq _boomed
+       lda en_beh,x            ; its picture:
        cmp #TURRET             ; the turret's by its aim
        beq _turret
        cmp #BOSS               ; a boss's part's by the
        beq _part               ; boss
        cmp #FIELD              ; a field's: of two
        beq _field
        cmp #P3_BEH             ; the station's: its
        bcs _p3                 ; module (P3_AT)
        cmp #MINE               ; a mine: the ship
        bne +                   ; near, it bursts
        jsr mine_near
        bcc +
        jmp _boomed
+       jmp _picture            ; the others' by the frame
_part:
        jsr part_picture
        jmp _colour
_p3:
        jsr P3_PART             ; its picture, its own way
        jmp _colour
_field:
        lda anim3               ; a field: it pushes the
        and #%00000001          ; ship (it is not hit)
        clc
        adc en_block,x
        sta obj_block,y
        jsr field_touch
        jmp _colour
_turret:
        jsr aim
        lda en_aim,x
        clc
        adc en_block,x
        sta obj_block,y
        jmp _colour
_boom:
        bne _capsule            ; (en_on: not BOOM)
        lda en_beh,x            ; exploding: on the rock it
        beq +                   ; goes with the camera
        jsr with_rock
+       inc en_left,x           ; the explosion's next frame
        lda en_left,x
        cmp #EXPLOSION_FRAMES
        beq _over               ; it is over
        jsr varkon_object
        bcs _off
        cmp #NONE
        bne _boomed
        jmp _hidden
_boomed:
        sty v_j                 ; its picture, its colour
        ldy en_left,x
        lda explosion_block,y   ; (the fireball: the block
        clc                     ; after the sparks')
        adc #1
        sta v_tmp
        lda explosion_own,y
        ldy v_j
        sta obj_colour,y
        lda v_tmp
        sta obj_block,y
        jmp _next
_over:
        lda en_cap,x            ; a carrier: its capsule
        beq _off
        lda #CAPSULE
        sta en_on,x
_capsule:
        jsr with_rock           ; on its place of the rock
        jsr varkon_object
        bcs _off                ; past the left edge
        cmp #NONE
        bne +
        jmp _hidden
+       lda ship_mode           ; the ship takes it, if it
        bne +                   ; flies (its box made by
        jsr pickup              ; hit_prepare)
        bcs _off
+       lda en_cap,x            ; its picture: its letter
        clc
        adc #CAPSULE_BLOCK - 1
        sta obj_block,y
        sty v_j                 ; the pod's colour turns
        lda anim
        lsr a
        lsr a
        and #%00000011
        tay
        lda capsule_colour,y
        ldy v_j
        sta obj_colour,y
        jmp _next
_off:
        lda #0
        sta en_on,x
        lda #NONE
        sta obj_y,y
_next:
        iny
        inx
        cpx #ENEMIES
        beq +
        jmp _one
+       rts

; Varkon X's object Y: its place, if its x register is
; 1-343 (A: its y register); C = 1 if it is gone (0 or less:
; past the left edge); A = NONE if it is past the right one.
varkon_object:
        lda en_xh,x
        bmi _gone
        bne _high
        lda en_x,x
        beq _gone
        sta obj_x,y
        lda #0
        beq _shown
_high:
        cmp #1
        bne _right
        lda en_x,x
        cmp #344 - 256
        bcs _right
        sta obj_x,y
        lda #$ff
_shown:
        sta obj_xh,y
        lda en_y,x
        clc
        adc #50
        sta obj_y,y
        clc
        rts
_right:
        lda #NONE
        clc
        rts
_gone:
        sec
        rts

; Varkon X on the rock: back by the camera's move (24 bits).
with_rock:
        sec
        lda en_xf,x
        sbc cam_step
        sta en_xf,x
        lda en_x,x
        sbc cam_step + 1
        sta en_x,x
        lda en_xh,x
        sbc cam_step + 2
        sta en_xh,x
        rts

; Varkon X takes the stretch en_seg: frames, velocity.
load_stretch:
        ldy en_seg,x
        lda seg_frames,y
        sta en_left,x
        lda seg_vxl,y
        sta en_vxl,x
        lda seg_vxh,y
        sta en_vxh,x
        and #%10000000          ; its sign, for 24 bits
        beq +
        lda #$ff
+       sta en_vxs,x
        lda seg_vyl,y
        sta en_vyl,x
        lda seg_vyh,y
        sta en_vyh,x
        rts

; A leaper's hop (X): y by vy, vy by gravity; when a hop is
; over, the next one: its landing column, HOP_FRAMES later,
; is (the level's x of its foot) / 8; the floor there is
; floor_line (255: none, it lands where it is); a hop that
; lands d lines lower starts with vy = 8 d - HOP_UP, so that
; it lands there exactly.
leap:
        lda en_left,x           ; a hop to start?
        bne _fly
        lda en_x,x              ; the level's x of the foot
        clc                     ; at the landing: x register
        adc next                ; - 24 + the next camera +
        sta leap_col            ; LEAP_FOOT + HOP_FRAMES *
        lda en_xh,x             ; LEAP_VX
        adc next + 1
        sta leap_col + 1
        lda leap_col
        sec
        sbc #LEAP_BACK
        sta leap_col
        bcs +
        dec leap_col + 1
+       .rept 3                 ; / 8: its column
        lsr leap_col + 1
        ror leap_col
        .endrept
        ldy leap_col
        lda leap_col + 1        ; the floor there
        bne +
        lda floor_lo,y
        jmp ++
+       lda floor_hi,y
+       cmp #255
        beq _level              ; none: d = 0
        sec                     ; d = floor - 21 - y
        sbc #LEAP_FEET + 1
        sec
        sbc en_y,x
        jmp _vy
_level:
        lda #0
_vy:
        sta en_vyl,x            ; 8 d, 16 bits, signed
        ldy #0
        cmp #$80
        bcc +
        dey
+       tya
        sta en_vyh,x
        .rept 3
        asl en_vyl,x
        rol en_vyh,x
        .endrept
        sec                     ; - HOP_UP
        lda en_vyl,x
        sbc #<HOP_UP
        sta en_vyl,x
        lda en_vyh,x
        sbc #>HOP_UP
        sta en_vyh,x
        lda #HOP_FRAMES
        sta en_left,x
_fly:
        dec en_left,x
        clc                     ; y += vy
        lda en_yf,x
        adc en_vyl,x
        sta en_yf,x
        lda en_y,x
        adc en_vyh,x
        sta en_y,x
        clc                     ; vy += HOP_G
        lda en_vyl,x
        adc #HOP_G
        sta en_vyl,x
        bcc +
        inc en_vyh,x
+       rts

LEAP_BACK = 24 - LEAP_FOOT + HOP_FRAMES / 2
        .cerror LEAP_VX != -128, "leap: half a pixel back"
        .cerror HOP_G > 255, "leap: HOP_G"

; Turret X: its barrel to the ship (en_aim): left (0) if the
; ship is more than AIM_SIDE pixels to its left, right (2)
; if more to its right, else up (1). Both sprites are 24
; pixels wide: their x registers tell.
aim:
        lda ship_x              ; the ship's x register -
        clc                     ; the turret's
        adc #24
        sta v_tmp
        lda ship_xh
        adc #0
        sta v_tmp + 1
        sec
        lda v_tmp
        sbc en_x,x
        sta v_tmp
        lda v_tmp + 1
        sbc en_xh,x
        bmi _left               ; negative
        bne _right              ; 256 or more
        lda v_tmp
        cmp #AIM_SIDE + 1
        bcs _right
_up:
        lda #1
        bne _set
_left:
        cmp #$ff
        bne _far
        lda v_tmp
        cmp #256 - AIM_SIDE
        bcs _up
_far:
        lda #0
        beq _set
_right:
        lda #2
_set:
        sta en_aim,x
        rts

; Varkon X fires: a plasma shot in the first free place (or
; none), from its fire entry (fire_*: its kind's; a turret's
; by its aim; a gunship's fan of three, fire_fan; a boss's
; cannon's, given in f_entry, at fire_entry): where it
; starts from the Varkon's sprite, its x velocity (whole
; pixels), its y velocity; a drone's drifts towards the
; ship, unless the ship is within AIM_DEAD lines. Its object
; at once (the shots have moved already).
fire_plasma:
        ldy en_kind,x           ; its entry
        lda kind_fan,y          ; a gunship's: its
        beq +                   ; fan, three entries
        ldy #3
        jmp fire_fan
+       lda en_beh,x
        cmp #TURRET
        bne +
        ldy en_aim,x
        lda aim_entry,y
        tay
+       sty f_entry
fire_entry:
        ldy #0
-       lda sh_on,y
        beq _free
        iny
        cpy #ESHOTS
        bne -
        rts
_free:
        sty f_slot
        lda #FX_PLASMA          ; its sound (X, Y kept)
        jsr sfx_start
        ldy f_entry
        clc                     ; where it starts
        lda en_x,x
        adc fire_dx,y
        sta f_x
        lda fire_dx,y           ; dx's sign
        and #%10000000
        beq +
        lda #$ff
+       adc en_xh,x
        sta f_xh
        lda en_y,x
        clc
        adc fire_dy,y
        sta f_y
        lda en_yf,x
        ldx f_slot              ; X: the shot from here
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
        lda fire_aim,y          ; a drone's: to the ship
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

; The waves whose column the camera has reached.
start_waves:
        lda camera + 1          ; the column: camera / 8
        sta v_tmp + 1
        lda camera
        .rept 3
        lsr v_tmp + 1
        ror a
        .endrept
        sta v_tmp
_wave:
        ldx wave_ptr
        lda v_tmp               ; column >= the wave's?
        cmp wave_col_lo,x
        lda v_tmp + 1
        sbc wave_col_hi,x
        bcc _done
        jsr start_wave
        inc wave_ptr
        jmp _wave
_done:
        rts

; Wave X: its members into free Varkon (if there are).
; Member k waits k times the spacing, starts k steps lower,
; fires first after half its period + 7 k frames (w_delay,
; w_y, w_fire go on by those, for each member). A Varkon on
; the rock (one a wave) has the level's x: its x register is
; x + 24 - the next frame's camera, its fraction 255 - the
; camera's (so that it stays on its pixel of the rock).
start_wave:
        lda #0
        sta v_k
        sta w_delay
        sta w_fire
        lda wave_y,x
        sta w_y
_member:
        ldy #0                  ; the first free Varkon
-       lda en_on,y
        beq _free
        iny
        cpy #ENEMIES
        bne -
        jmp _skip               ; none
_free:
        lda #FLYING
        sta en_on,y
        lda wave_kind,x
        sta en_kind,y
        lda wave_cap,x          ; its capsule
        sta en_cap,y
        lda wave_path,x
        sta en_seg,y
        lda wave_x_lo,x         ; the x register: x + 24
        clc
        adc #24
        sta en_x,y
        lda wave_x_hi,x
        adc #0
        sta en_xh,y
        lda #0
        sta en_xf,y
        sta en_yf,y
        sta en_flash,y
        sta en_left,y
        lda w_delay
        sta en_delay,y
        lda w_y
        sta en_y,y
        stx v_j                 ; its kind: behaviour, life,
        lda en_kind,y           ; picture, colour, period
        tax
        lda kind_beh,x
        sta en_beh,y
        lda kind_life,x
        sta en_life,y
        lda kind_block,x
        sta en_block,y
        lda kind_pmask,x        ; four pictures or two
        sta en_pmask,y
        lda kind_colour,x
        sta en_colour,y
        lda kind_period,x
        sta en_period,y
        beq +
        lsr a
        clc
        adc w_fire
+       sta en_fire,y
        tya                     ; its first stretch
        tax
        jsr load_stretch
        jsr wave_pri            ; its priority
        lda en_beh,x
        beq _flyer
        lda #255                ; on the rock: the camera's
        sec                     ; fraction, the camera off
        sbc next_frac
        sta en_xf,x
        sec
        lda en_x,x
        sbc next
        sta en_x,x
        lda en_xh,x
        sbc next + 1
        sta en_xh,x
        lda #0                  ; a leaper: its first hop at
        sta en_left,x           ; once; its walk
        lda #<LEAP_VX
        sta en_vxl,x
        lda #>LEAP_VX
        sta en_vxh,x
        sta en_vxs,x
        lda en_beh,x
        cmp #HOP
        beq _flyer
        lda #0                  ; a turret: still
        sta en_vxl,x
        sta en_vxh,x
        sta en_vxs,x
_flyer:
        ldx v_j
_skip:
        lda w_delay             ; the next member
        clc
        adc wave_spacing,x
        sta w_delay
        lda w_y
        clc
        adc wave_dy,x
        sta w_y
        lda w_fire
        clc
        adc #7
        sta w_fire
        inc v_k
        lda v_k
        cmp wave_count,x
        beq +
        jmp _member
+       rts

; ---------------------------------------------------------
; Level 2's towers
; ---------------------------------------------------------

; Varkon X's priority in the multiplexer as it comes in: a
; tower's core and field above all (BOSS_PRI, never left
; out: the field is a wall); another Varkon its class (2)
; if its place had a boss's or a tower's (else as it is).
wave_pri:
        lda en_beh,x
        cmp #STAND
        bcc +
        lda #BOSS_PRI
        jmp set_pri
+       tya
        pha
        txa
        clc
        adc #FIRST_ENEMY
        tay
        lda obj_pri,y
        cmp #BOSS_PRI
        bne +
        lda #2
        sta obj_pri,y
        sta obj_pri + OBJ_BANK,y
+       pla
        tay
        rts

; A field (Varkon X, its object Y) and the ship: the ship
; flies and its box meets the field's: it is pushed back, to
; the left, as by a wall of rock, and loses two notches
; (hurt: none if it blinks). X and Y kept.
field_touch:
        lda ship_mode
        bne _no
        sty v_j
        lda obj_y,y             ; its box: top
        ldy en_kind,x
        clc
        adc kind_box_y,y
        cmp sb_bottom
        bcs _out
        adc kind_box_h,y        ; (C = 0)
        cmp sb_top
        beq _out
        bcc _out
        lda en_xh,x             ; x register / 2
        lsr a
        lda en_x,x
        ror a
        clc
        adc kind_box_x,y
        cmp sb_right
        bcs _out
        adc kind_box_w,y        ; (C = 0)
        cmp sb_left
        beq _out
        bcc _out
        lda #256 - PUSH_SPEED   ; back, as from a wall
        sta push_dx
        lda #0
        sta push_dy
        lda #PUSH_FRAMES
        sta ship_push
        lda #2
        jsr hurt
_out:
        ldy v_j
_no:
        rts

; A tower's core (Varkon X) is destroyed: the pieces of a
; field within FIELD_REACH pixels of it explode (no points).
; X kept.
fields_down:
        stx v_i
        ldy #ENEMIES - 1
_one:
        lda en_on,y
        cmp #FLYING
        bne _next
        lda en_beh,y
        cmp #FIELD
        bne _next
        lda en_x,y              ; |its x - the core's|
        sec
        sbc en_x,x
        sta v_tmp
        lda en_xh,y
        sbc en_xh,x
        bpl +
        eor #$ff                ; negative: - it - 1
        sta v_tmp + 1
        lda v_tmp
        eor #$ff
        sta v_tmp
        lda v_tmp + 1
+       bne _next               ; 256 or more
        lda v_tmp
        cmp #FIELD_REACH
        bcs _next
        lda #BOOM
        sta en_on,y
        lda #0
        sta en_left,y
        sta en_flash,y
_next:
        dey
        bpl _one
        ldx v_i
        rts

; ---------------------------------------------------------
; Level 3's mines and fans
; ---------------------------------------------------------

; Varkon X fires a fan: A its first fire entry, Y how many
; (fire_entry for each, the entries one after the other).
; X kept.
fire_fan:
        sta f_fan
        sty f_count
        stx f_who
-       lda f_fan
        sta f_entry
        ldx f_who
        jsr fire_entry
        inc f_fan
        dec f_count
        bne -
        ldx f_who
        rts

; A mine (Varkon X, its object Y, on the screen): the ship
; flying, its x register within MINE_REACH_X pixels of the
; mine's, its line within MINE_REACH_Y: the mine bursts,
; its shrapnel (MINE_FAN_COUNT shots), no points; C = 1.
; X and Y kept.
mine_near:
        lda ship_mode           ; the ship flies?
        bne _no
        lda ship_x              ; its x register - the
        clc                     ; mine's
        adc #24
        sta v_tmp
        lda ship_xh
        adc #0
        sta v_tmp + 1
        sec
        lda v_tmp
        sbc en_x,x
        sta v_tmp
        lda v_tmp + 1
        sbc en_xh,x
        bmi _left
        bne _no                 ; 256 or more
        lda v_tmp
        cmp #MINE_REACH_X
        bcs _no
        bcc _y
_left:
        cmp #$ff                ; -256 or less
        bne _no
        lda v_tmp
        cmp #256 - MINE_REACH_X + 1
        bcc _no
_y:
        lda ship_y              ; |its line - the mine's|
        sec
        sbc en_y,x
        bcs +
        eor #$ff
        adc #1                  ; (C = 0)
+       cmp #MINE_REACH_Y
        bcs _no
        sty mn_obj              ; it bursts
        lda #MINE_FAN_FIRST
        ldy #MINE_FAN_COUNT
        jsr fire_fan
        ldy mn_obj
        lda #BOOM
        sta en_on,x
        lda #0
        sta en_left,x
        sta en_flash,x
        lda #FX_BOOM            ; (X, Y kept)
        jsr sfx_start
        sec
        rts
_no:
        clc
        rts

        .cerror MINE_REACH_X > 255 || MINE_REACH_Y > 127
