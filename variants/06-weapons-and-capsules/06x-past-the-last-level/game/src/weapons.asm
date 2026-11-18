; The weapons: four levels a ship, the volleys, the Gauss
; blasts, the missile, the satellite, the capsules' gifts.
;
; The weapon is the ship's and its level (weapon, 0-3): the
; W capsules raise it, a ship lost lowers it by one.
; w_index = ship * 4 + level picks its row of the tables
; (tables.inc, from ships.py): frames between two volleys
; (w_period), the volley's shots (w_count from entry w_first
; of v_kind, v_dx, v_dy: each from the ship's nose,
; SHOT_START).
; A volley leaves only when all its shots have a free place
; among the four (objects 0-3).
; With it the satellite's bolt (if a place is still free)
; and the missile (if the M capsule was taken and none
; flies).
;
; A shot of a kind (shot_*): its halves (a double bolt has
; two, each ends on the rock alone), its x speed, its y
; speed (the spread's shots climb or dive a line a frame;
; past the playfield they end).
; Whether it pierces (the laser: it flies on through the
; Varkon, hurting each once: shot_pl, shot_ph), whether it
; bursts (the Gauss shot: on a Varkon or the rock it becomes
; a blast: the fireball for BLAST_FRAMES frames in its
; place, and its box hurts the Varkon around in the next
; update_varkon).
;
; The S capsules make the ship faster (cur_speed: its own +
; SPEED_STEP 256ths a capsule, three at most). The satellite
; (O) follows the ship and fires with it; the missile (M)
; falls to the floor and runs along it.

; (init_weapons, the start of a game, is in title.asm.)

; The weapon's row (w_index) and the ship's speed from its
; ship, its level, its S capsules; the HUD's pips again. X
; kept.
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

; A ship lost: the weapon a level down, the satellite gone
; (the speed and the missile stay). X kept.
weapon_down:
        lda weapon
        beq +
        dec weapon
+       lda #0
        sta sat_on
        jmp set_weapon

; Fire: the weapon's volley, if all its shots have a free
; place (else nothing: the next frame again); with it the
; satellite's bolt and the missile. Then the wait to the
; next volley.
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
        lda sat_on              ; the satellite's bolt
        beq _missile
        ldx #0
-       lda shot_mask,x
        beq +
        inx
        cpx #4
        bne -
        beq _missile            ; no place left
+       clc
        lda sat_x
        adc #SAT_SHOT
        sta px
        lda sat_xh
        adc #0
        sta px + 1
        lda sat_y
        sta py
        lda #SATBOLT
        jsr shot_begin
_missile:
        lda missiles            ; the missile: one at a time
        beq _done
        lda m_on
        bne _done
        lda #1                  ; it falls
        sta m_on
        clc
        lda ship_x
        adc #MISSILE_DX
        sta m_x
        lda ship_xh
        adc #0
        sta m_xh
        lda ship_y
        clc
        adc #MISSILE_DY
        sta m_y
        rts
_done:
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
        lda #0
        sta shot_bl,x
        sta shot_pl,x
        sta shot_ph,x
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

; Shot X bursts at its point: a blast. It shows from the
; next fly_shots on (shot_bl: BLAST_FRAMES + 1, counted
; down there), its fireball's middle on the point; its box
; (the point's place in the hits' units, by the kind's
; blast) is tried in the next update_varkon (blast_armed;
; bl_skip, the Varkon not to try again, is the caller's).
; X kept.
start_blast:
        ldy shot_kind,x
        lda shot_blast,y        ; 1 or 2
        tay
        lda hit_x,x
        sec
        sbc blast_rx - 1,y
        sta bl_left
        clc
        adc blast_rx - 1,y
        adc blast_rx - 1,y
        sta bl_right
        lda hit_y,x
        sec
        sbc blast_ry - 1,y
        sta bl_top
        clc
        adc blast_ry - 1,y
        adc blast_ry - 1,y
        sta bl_bottom
        lda blast_dmg - 1,y
        sta bl_dmg
        lda #1
        sta blast_armed
        lda #$ff                ; no point any more
        sta hit_y,x
        lda #BLAST_FRAMES + 1
        sta shot_bl,x
        ldy shot_kind,x         ; the fireball's place
        clc
        lda shot_x,x
        adc shot_bdx,y
        sta shot_x,x
        lda shot_bdx,y          ; (signed)
        and #%10000000
        beq +
        lda #$ff
+       adc shot_xh,x
        sta shot_xh,x
        lda shot_y,x
        clc
        adc shot_bdy,y
        sta shot_y,x
        clc
        adc #50
        sta shot_yr,x
        rts

; The satellite after the ship: its place, SAT_BACK pixels
; behind and SAT_ABOVE lines above it (below if the ship is
; above line SAT_LOW), SAT_STEP pixels a frame at most on
; each axis. It comes in with the ship (ship_again), from x
; < 0 ($ffxx): the x's difference is signed.
move_satellite:
        lda sat_on
        bne +
        rts
+       sec                     ; x: the target
        lda ship_x
        sbc #SAT_BACK
        sta px
        lda ship_xh
        sbc #0
        sta px + 1
        lda px                  ; the target - its x
        sec
        sbc sat_x
        sta q
        lda px + 1
        sbc sat_xh
        bmi _left               ; the target to the left
        bne _right              ; 256 or more to the right
        lda q
        cmp #SAT_STEP + 1
        bcs _right
_at:
        lda px                  ; near: on it
        sta sat_x
        lda px + 1
        sta sat_xh
        jmp _y
_right:
        clc
        lda sat_x
        adc #SAT_STEP
        sta sat_x
        bcc _y
        inc sat_xh
        bcs _y
_left:
        cmp #$ff                ; - 1 to - SAT_STEP: on it
        bne _back
        lda q
        cmp #256 - SAT_STEP
        bcs _at
_back:
        sec
        lda sat_x
        sbc #SAT_STEP
        sta sat_x
        bcs _y
        dec sat_xh
_y:
        lda ship_y              ; y: the target
        cmp #SAT_LOW
        bcc +
        sbc #SAT_ABOVE          ; (C = 1)
        jmp ++
+       adc #SAT_ABOVE          ; (C = 0)
+       sta py
        cmp sat_y
        bcc _up
        sbc sat_y               ; down by (C = 1)
        cmp #SAT_STEP + 1
        bcc _y_at
        lda sat_y
        adc #SAT_STEP - 1       ; (C = 1)
        sta sat_y
        rts
_up:
        lda sat_y               ; up by
        sec
        sbc py
        cmp #SAT_STEP + 1
        bcc _y_at
        lda sat_y
        sbc #SAT_STEP           ; (C = 1)
        sta sat_y
        rts
_y_at:
        lda py
        sta sat_y
        rts

; The missile, a frame: falling (m_on 1) a pixel right and
; two down, to the floor under its toe; running (2) three
; pixels right along the floor. It ends past MISSILE_X_END,
; under the playfield, on a wall (the floor more than
; MISSILE_STEP lines higher); from a drop of more, or a
; river (no floor), it falls again. Then its point.
fly_missile:
        lda m_on
        bne +
        rts
+       cmp #2
        beq _run
        inc m_x                 ; falling
        bne +
        inc m_xh
+       lda m_y
        clc
        adc #2
        sta m_y
        cmp #VARKON_Y_MAX + 1
        bcs _end                ; under the playfield
        jsr missile_edge
        bcs _end
        jsr missile_floor
        cmp #255
        beq missile_point       ; no floor: on it falls
        sec
        sbc #MISSILE_FOOT       ; A: its y on the floor
        cmp m_y
        beq _land
        bcs missile_point       ; still above it
        sta v_tmp               ; below it: by a step at
        lda m_y                 ; most it lands, more is a
                                ; wall
        sec
        sbc v_tmp
        cmp #MISSILE_STEP + 1
        bcs _end
        lda v_tmp
_land:
        sta m_y
        lda #2
        sta m_on
        bne missile_point
_run:
        lda m_x                 ; running
        clc
        adc #3
        sta m_x
        bcc +
        inc m_xh
+       jsr missile_edge
        bcs _end
        jsr missile_floor
        cmp #255
        beq _fall               ; a river
        sec
        sbc #MISSILE_FOOT       ; A: its y on the floor here
        sta v_tmp
        clc
        adc #MISSILE_STEP
        cmp m_y
        bcc _end                ; higher by more: a wall
        lda m_y
        clc
        adc #MISSILE_STEP
        cmp v_tmp
        bcc _fall               ; lower by more: it falls
        lda v_tmp
        sta m_y
        jmp missile_point
_fall:
        lda #1
        sta m_on
        bne missile_point
_end:
        lda #0
        sta m_on
        lda #$ff
        sta m_hy
        rts

; The missile's point for the hits (hits.asm): its nose,
; falling or running: x register / 2, y register.
missile_point:
        ldy m_on
        clc
        lda m_x
        adc m_nose_x - 1,y
        sta v_tmp
        lda m_xh
        adc #0
        lsr a
        lda v_tmp
        ror a
        sta m_hx
        lda m_y
        clc
        adc m_nose_y - 1,y
        sta m_hy
        rts

; C = 1 if the missile is past MISSILE_X_END.
missile_edge:
        lda m_xh
        beq +
        lda m_x
        cmp #<(MISSILE_X_END + 1)
        rts
+       clc
        rts

        .cerror MISSILE_X_END < 256, "missile_edge"

; The floor's first line under the missile's toe (A; 255:
; none): the level's column (camera + m_x + MISSILE_REACH)
; / 8, the pixel the next frame shows there (camera +
; screen x - 7, at the fine scroll).
missile_floor:
        clc
        lda m_x
        adc #MISSILE_REACH
        sta m_col
        lda m_xh
        adc #0
        sta m_col + 1
        clc
        lda m_col
        adc camera
        sta m_col
        lda m_col + 1
        adc camera + 1
        .rept 3
        lsr a
        ror m_col
        .endrept
        ldy m_col
        cmp #0
        bne +
        lda floor_lo,y
        rts
+       lda floor_hi,y
        rts

; The ship takes a capsule (A: its letter, 0-4: W S M O E;
; hits.asm): W a weapon level, S speed, M the missile, O
; the satellite (from the ship's place), E the shield full;
; one past its most, CAPSULE_BONUS points instead. X and Y
; kept.
take_capsule:
        sty cap_keep
        beq _w
        cmp #2
        bcc _s
        beq _m
        cmp #3
        beq _o
        lda shield              ; E: the shield full
        ldy ship_type
        cmp ship_shield,y
        bcs _bonus
        lda ship_shield,y
        sta shield
        lda #1
        sta hud_dirty
        bne _done
_w:
        inc weapon
        bne _set
_s:
        lda s_caps
        cmp #SPEED_STEPS
        bcs _bonus
        inc s_caps
_set:
        jsr set_weapon
        jmp _done
_m:
        lda missiles
        bne _bonus
        inc missiles
        bne _done
_o:
        lda sat_on
        bne _bonus
        inc sat_on
        lda ship_x
        sta sat_x
        lda ship_xh
        sta sat_xh
        lda ship_y
        sta sat_y
        jmp _done
_bonus:
        ldy #KIND_BONUS
        jsr score_add
_done:
        ldy cap_keep
        rts

        .cerror CAPSULE_COUNT != 5, "take_capsule: WSMOE"

; Objects 22 and 23 of this frame's bank (Y: its first
; place): the satellite (two pictures by anim), the missile
; (its picture falling or running), or none.
export_more:
        lda sat_on
        beq _no_sat
        lda sat_y
        clc
        adc #50
        sta obj_y + FIRST_SAT,y
        clc
        lda sat_x
        adc #24
        sta obj_x + FIRST_SAT,y
        lda sat_xh
        adc #0
        beq +
        lda #$ff
+       sta obj_xh + FIRST_SAT,y
        lda anim
        lsr a
        lsr a
        lsr a
        and #%00000001
        clc
        adc #SATELLITE_BLOCK
        sta obj_block + FIRST_SAT,y
        lda #SATELLITE_OWN
        sta obj_colour + FIRST_SAT,y
        jmp _missile
_no_sat:
        lda #NONE
        sta obj_y + FIRST_SAT,y
_missile:
        lda m_on
        beq _no_missile
        lda m_y
        clc
        adc #50
        sta obj_y + FIRST_MISSILE,y
        clc
        lda m_x
        adc #24
        sta obj_x + FIRST_MISSILE,y
        lda m_xh
        adc #0
        beq +
        lda #$ff
+       sta obj_xh + FIRST_MISSILE,y
        lda #MISSILE_BLOCK + 2  ; running (2): its first
        sec                     ; picture, falling the next
        sbc m_on
        sta obj_block + FIRST_MISSILE,y
        lda #MISSILE_OWN
        sta obj_colour + FIRST_MISSILE,y
        rts
_no_missile:
        lda #NONE
        sta obj_y + FIRST_MISSILE,y
        rts

; The HUD's pips: the weapon's level (LEVELS of them).
weapon_pips:
        ldy weapon
        iny
        sty temp
        ldx #0
-       lda #PIP_FULL_CODE
        cpx temp
        bcc +
        lda #PIP_EMPTY_CODE
+       sta SCREEN_A + HUD_CELL + HUD_WEAPON,x
        inx
        cpx #LEVELS
        bne -
        rts
