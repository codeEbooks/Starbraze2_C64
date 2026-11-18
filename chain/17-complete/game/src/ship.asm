; The ship and its shots.
;
; The ship flies in eight directions at its speed (ship
; tables in tables.inc), 256ths of a pixel a frame. Five
; points of it meet the rock: the nose, the top and the
; bottom edge near the front and near the tail. The rock is
; read in the screen the next frame shows, at its fine
; scroll, pixel by pixel: a pair of a multicolour cell that
; is not background. On the rock the ship is pushed away for
; PUSH_FRAMES frames (down from the overhang, up from the
; floor, else back) and, if it is not blinking, loses two
; notches and blinks for HIT_BLINK frames.
; No notches left: it explodes, a ship is lost, a wait; then
; another ship is chosen (states.asm), the game held, and it
; comes in from the left with a full shield, blinking. No
; ships left: GAME OVER, then the title. At the start of a
; game the ship is chosen first, then flies from its place
; (START_X, ENTER_Y).
;
; Fire held: the weapon's volley (weapons.asm) every so many
; frames, while its shots have free places among the four
; (objects 0-3 of the multiplexer). The shots fly right
; (some climb or dive) and end on the rock, past the right
; edge or out of the playfield; each half of a double bolt
; ends on its own.
; A Gauss shot bursts. The missile and the satellite fly
; with the ship (weapons.asm).
;
; After the boss (boss.asm, STAGE CLEAR) the ship flies off
; to the right (LEAVE), then is gone (GONE); with the next
; level it comes back in from the left. In the arena the
; rock is read in the characters themselves: the boss's body
; is made of characters that change.

CONTROL = 0
EXPLODE = 1
WAIT    = 2
ENTER   = 3
LEAVE   = 4
GONE    = 5
CHOOSE  = 6                     ; held: being chosen
JOY_UP    = %00000001
JOY_DOWN  = %00000010
JOY_LEFT  = %00000100
JOY_RIGHT = %00001000

; The joystick and the keys, 1 = pushed: SPACE (bit 0: the
; pause, states.asm), F1, F3, F5, F7 (bits 3-6: the sound's
; mode, player.asm; those just pushed: new_keys, in the main
; loop after joy_ready).
; In the test build (TEST_BUILD: main.asm) also the keys I
; and L (test_keys, bits 0-1), only for the tests by hand
; (test_step). Port A of CIA 1 is an input for the joystick;
; for the keys it drives one row of the keyboard low at a
; time.
read_input:
        .if RECORD_GAME != 0
        lda #JOY_FIRE           ; to record: Fire held
        .else
        lda $dc00               ; joystick 2
        eor #%11111111
        and #%00011111
        .fi
        sta joy
        lda #$ff                ; port A out: the rows
        sta $dc02
        lda #%01111111          ; row 7: SPACE on bit 4
        sta $dc00
        lda $dc01
        eor #%11111111
        and #%00010000
        lsr a
        lsr a
        lsr a
        lsr a
        sta keys
        lda #%11111110          ; row 0: F1, F3, F5 on bits
        sta $dc00               ; 4-6, F7 on bit 3
        lda $dc01
        eor #%11111111
        sta temp
        and #%01110000          ; F1, F3, F5: keys bits 3-5
        lsr a
        ora keys
        sta keys
        lda temp
        and #%00001000          ; F7: bit 6
        asl a
        asl a
        asl a
        ora keys
        sta keys
        .if TEST_BUILD != 0      ; the test build only
        lda #%11101111          ; row 4: I on
        sta $dc00               ; bit 1
        lda $dc01
        eor #%11111111
        and #%00000010
        lsr a
        sta test_keys
        lda #%11011111          ; row 5: L on bit 2
        sta $dc00
        lda $dc01
        eor #%11111111
        and #%00000100
        lsr a
        ora test_keys
        sta test_keys
        .fi
        lda #$ff
        sta $dc00
        lda #0                  ; port A in again
        sta $dc02
        rts

; Only in the test build (TEST_BUILD), for the tests by
; hand: the keys I and L just pushed. I: the ship cannot be
; hurt (hurt does nothing: the rock still pushes it), or can
; again; the border red while it cannot. L: the next level
; at once, as after STAGE CLEAR (restart_flag: the main
; loop), only while the ship flies (CONTROL). Called after
; joy_ready, where the tests write test_keys, if a key is
; down or was before.
        .if TEST_BUILD != 0
test_step:
        lda test_prev           ; pushed since last frame
        eor #%11111111
        and test_keys
        tax
        lda test_keys
        sta test_prev
        txa
        and #TEST_I
        beq +
        lda invuln
        eor #1
        sta invuln
        tay
        lda test_border,y
        sta $d020
+       txa
        and #TEST_L
        beq +
        lda ship_mode
        cmp #CONTROL
        bne +
        lda #1
        sta restart_flag
+       rts

test_border:
        .byte 0, 2              ; black; red: unhurtable
        .fi

; (init_ship, the start of a game, is in title.asm.)

; The ship comes in at x = A (high byte X), mode Y: full
; shield, blinking.
come_in:
        sta ship_x
        stx ship_xh
        sty ship_mode
        lda #ENTER_Y
        sta ship_y
        lda #0
        sta ship_xf
        sta ship_yf
        sta ship_timer
        sta ship_push
        sta figure
        sta cooldown
        ldx ship_type
        lda ship_shield,x
        sta shield
        lda #ENTER_BLINK
        sta ship_blink
        lda #1
        sta hud_dirty
        rts

; STAGE CLEAR: the ship off to the right, its satellite
; after it; past LEAVE_END it is gone.
ship_leave:
        clc
        lda ship_x
        adc #LEAVE_SPEED
        sta ship_x
        lda ship_xh
        adc #0
        sta ship_xh
        jsr move_satellite
        lda ship_xh
        beq +
        lda ship_x
        cmp #<LEAVE_END
        bcc +
        lda #GONE
        sta ship_mode
+       rts

        .cerror LEAVE_END < 256 || LEAVE_END > 511

; The next level after STAGE CLEAR (main loop): the ship
; comes in from the left with a full shield, its satellite
; with it.
ship_again:
        lda #ENTER_X
        ldx #$ff
        ldy #ENTER
        jsr come_in
        lda ship_x
        sta sat_x
        lda ship_xh
        sta sat_xh
        lda ship_y
        sta sat_y
        rts

; One frame of the ship, then of its shots.
update_ship:
        lda near_d016           ; the rock: the fine scroll
        and #%00000111          ; and the screen of the
        sta rock_fine           ; next frame
        lda front               ; (swapped already, if the
        asl a                   ; screens swap): 0 or 4,
        asl a                   ; screen A or B
        sta rock_page
        lda ship_mode
        cmp #CONTROL
        beq steer_ship
        cmp #EXPLODE
        bne +
        inc ship_timer          ; the explosion's pictures
        lda ship_timer
        cmp #EXPLOSION_FRAMES
        bne _shots
        lda #WAIT
        sta ship_mode
        lda #0
        sta ship_timer
        beq _shots
+       cmp #WAIT
        bne _other
        inc ship_timer          ; the wait
        lda ship_timer
        cmp #WAIT_FRAMES
        bne _shots
        lda ship_lives          ; no ships left: GAME
        bne +                   ; OVER (states.asm)
        lda #HELD_OVER
        sta held
        bne _shots              ; (always)
+       jsr choose_lost         ; another ship chosen
        jmp _shots
_other:
        cmp #LEAVE              ; off to the right;
        bcc _enter              ; gone: nothing
        bne _shots
        jsr ship_leave
        jmp _shots
_enter:
        lda ship_blink          ; coming in from the left
        beq +
        dec ship_blink
+       clc
        lda ship_x
        adc #2
        sta ship_x
        lda ship_xh
        adc #0
        sta ship_xh
        bne _shots              ; still left of 0
        lda ship_x
        cmp #ENTER_TO
        bcc _shots
        lda #CONTROL
        sta ship_mode
_shots:
        jmp fly_shots

steer_ship:
        lda ship_blink
        beq +
        dec ship_blink
+       lda ship_push
        beq _steer
        dec ship_push           ; pushed away from the rock
        clc
        lda ship_x
        adc push_dx
        sta ship_x
        lda push_dx             ; -2, 0 or 2: its high byte
        and #%10000000
        beq +
        lda #$ff
+       adc ship_xh
        sta ship_xh
        clc
        lda ship_y
        adc push_dy
        sta ship_y
        lda #0
        sta figure
        jmp _clamp
_steer:
        lda #0
        sta figure
        lda joy
        and #JOY_RIGHT
        beq +
        clc
        lda ship_xf
        adc cur_speed_lo
        sta ship_xf
        lda ship_x
        adc cur_speed_hi
        sta ship_x
        lda ship_xh
        adc #0
        sta ship_xh
        jmp _vertical
+       lda joy
        and #JOY_LEFT
        beq _vertical
        sec
        lda ship_xf
        sbc cur_speed_lo
        sta ship_xf
        lda ship_x
        sbc cur_speed_hi
        sta ship_x
        lda ship_xh
        sbc #0
        sta ship_xh
_vertical:
        lda joy
        and #JOY_UP
        beq +
        sec
        lda ship_yf
        sbc cur_speed_lo
        sta ship_yf
        lda ship_y
        sbc cur_speed_hi
        sta ship_y
        lda #1                  ; climbing
        sta figure
        jmp _clamp
+       lda joy
        and #JOY_DOWN
        beq _clamp
        clc
        lda ship_yf
        adc cur_speed_lo
        sta ship_yf
        lda ship_y
        adc cur_speed_hi
        sta ship_y
        lda #2                  ; diving
        sta figure
_clamp:
        lda ship_xh             ; x: X_MIN-X_MAX
        bmi _left
        bne _right_edge
        lda ship_x
        cmp #X_MIN
        bcs +
_left:
        lda #X_MIN
        sta ship_x
        lda #0
        sta ship_xh
        sta ship_xf
        beq _y
+       lda ship_xh
        beq _y                  ; under 256: within X_MAX
_right_edge:
        lda ship_x              ; 256 or more
        cmp #<(X_MAX + 1)
        bcc _y
        lda #<X_MAX
        sta ship_x
        lda #>X_MAX
        sta ship_xh
        lda #0
        sta ship_xf
_y:
        lda ship_y              ; y: 0-Y_MAX; above 0 it
        cmp #Y_MAX + 1          ; wraps to 255 and down
        bcc _rock
        cmp #$c0
        bcs _top
        lda #Y_MAX
        bne +
_top:
        lda #Y_MIN
+       sta ship_y
        lda #0
        sta ship_yf
_rock:
        lda ship_push
        bne _fire
        jsr collide
_fire:
        jsr move_satellite      ; after the ship
        lda cooldown
        beq +
        dec cooldown
+       lda ship_mode
        bne _done               ; it has just exploded
        lda joy
        and #JOY_FIRE
        beq _done
        lda cooldown
        bne _done
        jsr fire
_done:
        jmp fly_shots

; The five points against the rock; a push, the damage. All
; five in the corridor (rows 10-14, ship_y from
; ship_air_from to ship_air_to - 1): no rock there (unless a
; boss's body is there: air_rock).
collide:
        ldx ship_type
        lda air_rock            ; a body in the corridor?
        bne +
        lda ship_y
        cmp ship_air_from,x
        bcc +
        cmp ship_air_to,x
        bcs +
        rts
+       lda #0
        sta touch
        lda spot_first,x        ; the ship's five points,
        clc                     ; from the last to the first
        adc #4                  ; (unrolled)
        sta spot
        .for c_k in range(5)
        ldy spot
        clc
        lda ship_x
        adc ship_spot_x - c_k,y
        sta px
        lda ship_xh
        adc #0
        sta px + 1
        clc
        lda ship_y
        adc ship_spot_y - c_k,y
        sta py
        jsr rock_at
        rol touch               ; the last ends in bit 4
        .endfor
        lda touch               ; bit 0 nose, 1-2 top front
        beq _none               ; and rear, 3-4 bottom
        and #%00000110
        beq _below              ; no top
        lda touch
        and #%00011000
        bne _back               ; top and bottom
        lda #0                  ; the overhang: down
        ldx #PUSH_SPEED
        bne _push
_below:
        lda touch
        and #%00011000
        beq _back               ; the nose only
        lda #0                  ; the floor: up
        ldx #256 - PUSH_SPEED
        bne _push
_back:
        lda #256 - PUSH_SPEED   ; a wall: back
        ldx #0
_push:
        sta push_dx
        stx push_dy
        lda #PUSH_FRAMES
        sta ship_push
        lda #2                  ; the rock: two notches
        jmp hurt
_none:
        rts

; The ship hit: A notches off its shield, unless it blinks
; or the key I of the test build (or a recording) has made
; it unhurtable (invuln); it blinks for HIT_BLINK frames; no
; notches left, it explodes and a ship is lost. X and Y
; kept.
hurt:
        sta hurt_n
        lda ship_blink
        ora invuln              ; key I
        bne _done               ; blinking: no damage
        lda #1
        sta hud_dirty
        lda #HIT_BLINK
        sta ship_blink
        lda shield
        sec
        sbc hurt_n
        bcs +
        lda #0
+       sta shield
        bne _hurt
        lda #EXPLODE            ; no notches left
        sta ship_mode
        lda #0
        sta ship_timer
        dec ship_lives
        tya                     ; the weapon a level down,
        pha                     ; the satellite lost
        jsr weapon_down
        pla
        tay
        lda #FX_EXPLODE
        jmp sfx_start
_hurt:
        lda #FX_HURT
        jmp sfx_start
_done:
        rts

spot_first:
        .byte 0, 5, 10

; Shot X: the line of its point for the hits, the middle of
; its halves left (hit_y, $ff if none); its picture (a
; double bolt's by its halves: both, the upper, the lower).
shot_line:
        lda shot_mask,x
        beq _none
        lda shot_kind,x         ; kind * 4 + its halves
        asl a
        asl a
        ora shot_mask,x
        tay
        lda shot_y,x
        clc
        adc shot_mid,y
        sta hit_y,x
        ldy shot_kind,x         ; its picture
        lda shot_halves,y
        cmp #%11                ; (C = 1: two halves)
        lda shot_block,y
        bcc +
        ldy shot_mask,x
        clc
        adc half_image,y
+       sta shot_blk,x
        rts
_none:
        lda #$ff
        sta hit_y,x
        rts

; The shots fly on: past the right edge they end; one that
; climbs or dives moves its y too, and ends out of the
; playfield.
; Their points for the hits go with them (hit_x by half the
; speed; hit_y when the y moves).
; A blast counts its frames down (its pictures), then ends.
; Then the missile (weapons.asm).
; The rock: shots_rock, after the sprites are written.
fly_shots:
        ldx #3
_shot:
        lda shot_mask,x
        bne +
        jmp _next
+       lda shot_bl,x
        beq +
        jmp _blast
+       ldy shot_kind,x
        lda hit_x,x             ; its point: half the speed
        clc                     ; (an even number)
        adc shot_half,y
        sta hit_x,x
        clc
        lda shot_x,x
        adc shot_speed,y
        sta shot_x,x
        lda shot_xh,x
        adc #0
        sta shot_xh,x
        beq _dy                 ; under 256
        lda shot_x,x
        cmp #<(320 + 1)
        bcc _dy
        jmp _end                ; past the edge
_dy:
        lda shot_dy,x           ; climbing or diving
        beq _next
        clc
        adc shot_y,x
        sta shot_y,x
        cmp #VARKON_Y_MAX + 1
        bcc +
        jmp _end                ; out of the playfield
+       cmp air_from,y          ; in the corridor?
        bcc +
        cmp air_to,y
        lda #1
        bcc ++
+       lda #0
+       sta shot_air,x
        lda shot_dy,x           ; its y register and its
        clc                     ; point's line: the same
        adc shot_yr,x           ; step
        sta shot_yr,x
        lda shot_dy,x
        clc
        adc hit_y,x
        sta hit_y,x
        jmp _next
_end:
        lda #0
        sta shot_mask,x
        lda #$ff
        sta hit_y,x
        bne _next
_blast:
        dec shot_bl,x           ; a blast: its frames
        beq _end
        ldy shot_bl,x           ; its picture
        lda blast_block,y
        sta shot_blk,x
        lda blast_own,y
        sta shot_col,x
_next:
        dex
        bmi +
        jmp _shot
+       jmp fly_missile

; The shots against the rock, after the sprites are written
; (a shot that meets it shows there a frame, then ends): a
; half on the rock ends (a double bolt has two, the others
; one: the upper).
; A Gauss shot bursts (its blast from the next frame).
; A shot in the corridor (shot_air) never meets the rock
; (unless a boss's body is there: air_rock); nor does a
; blast.
shots_rock:
        ldx #3
_shot:
        lda shot_mask,x
        beq _next
        lda shot_bl,x
        bne _next               ; a blast: no rock
        lda air_rock            ; a body in the corridor?
        bne +
        lda shot_air,x          ; in the corridor: no rock
        bne _next
+
        ldy shot_kind,x
        stx slot
        tya                     ; its points: kind * 2, the
        asl a                   ; upper; + 1, the lower
        sta spot
        lda shot_mask,x
        and #%01
        beq _lower
        jsr shot_rock
        ldx slot
        bcc _lower
        ldy shot_kind,x         ; on the rock: a Gauss shot
        lda shot_blast,y        ; bursts
        beq +
        lda #$ff                ; (no Varkon met)
        sta bl_skip
        jsr start_blast
        jmp _next
+       lda shot_mask,x         ; the others end
        and #%10
        sta shot_mask,x
        jsr shot_line
_lower:
        lda shot_mask,x
        and #%10
        beq _next
        inc spot
        jsr shot_rock
        ldx slot
        bcc _next
        lda shot_mask,x
        and #%01
        sta shot_mask,x
        jsr shot_line
_next:
        dex
        bpl _shot
        rts

; Point `spot` of shot X: on the rock? C = 1 if it is.
shot_rock:
        ldy spot
        clc
        lda shot_x,x
        adc shot_point_x,y
        sta px
        lda shot_xh,x
        adc #0
        sta px + 1
        clc
        lda shot_y,x
        adc shot_point_y,y
        sta py
        jmp rock_at

; Is the pixel (px, py) rock? C = 1 if it is. The screen
; the next frame shows, at its fine scroll: rock_page and
; rock_fine, set by update_ship. The column is
; (px - fine scroll) / 8, the pair in it
; ((px - fine scroll) AND 7) / 2. For its time:
; the row by a table (rows 10-14 and under the playfield:
; none), the character's line from rock_lines (its lines
; page by page: the line's page is written into _line).
rock_at:
        ldx py
        lda rock_row,x
        bmi _air                ; no rock on this line
        tax                     ; X: the row
        sec                     ; q = px - fine scroll
        lda px
        sbc rock_fine
        sta q
        lda px + 1
        sbc #0
        bmi _air                ; left of column 0
        lsr a                   ; q's bit 8 into C
        lda q
        bcc +
        cmp #64                 ; 256-319: columns 32-39
        bcs _air
        sec                     ; bit 8 again
+       ror a                   ; the column: q / 8
        lsr a
        lsr a
        tay
        lda row_lo,x            ; the row in the screen of
        sta dst                 ; the next frame
        lda row_hi,x
        ora rock_page
        sta dst + 1
        lda (dst),y             ; its character
        cmp #FIRST_SOLID
        bcc _air                ; blank, sky, stars
        ldx arena_chars         ; the crawler's arena:
        bne _chars              ; from the characters
        tax
        lda py                  ; its line's page
        and #%00000111
        clc
        adc #>rock_lines
        sta _line + 2
        lda q                   ; the pair's bits
        and #%00000111
        tay
_line:
        lda rock_lines,x
        and pair_bits,y
        beq _air
        sec
        rts
_air:
        clc
        rts
_chars:
        ldx #0                  ; CHARSET + 8 code + line
        stx dst + 1
        .rept 3
        asl a
        rol dst + 1
        .endrept
        sta dst
        lda py
        and #%00000111
        ora dst
        sta dst
        lda dst + 1
        adc #>CHARSET           ; (C = 0)
        sta dst + 1
        lda q                   ; the pair's bits
        and #%00000111
        tay
        lda pair_bits,y
        ldy #0
        and (dst),y
        beq _air
        sec
        rts

        .cerror (CHARSET & $ff) != 0, "rock_at: CHARSET"

pair_bits:                      ; by (q AND 7)
        .byte %11000000, %11000000, %00110000, %00110000
        .byte %00001100, %00001100, %00000011, %00000011
rock_row:                       ; by the line: its row, or
        .for r_line in range(256) ; $ff (rows 10-14, under
        .if r_line < 80 || (r_line >= 120 && r_line < 176)
        .byte r_line / 8        ; the playfield)
        .else
        .byte $ff
        .endif
        .endfor
        .cerror SCREEN_B - SCREEN_A != $0400, "rock_page"
        .cerror (>SCREEN_A) & 4 != 0, "rock_page: ORA"

; Sprites 0 and 1, the ship, for this frame: sprite 0 its
; accent, 1 its colour layer (multicolour); or the
; explosion's sparks and fireball; or off (waiting, or
; hidden while it blinks). Registers and pointers in both
; screens; their bits of $d015 in `enable`, of $d010 in
; ship_bits (plan_sprites writes those registers).
ship_sprites:
        lda #0
        sta enable
        sta ship_bits
        lda ship_mode
        cmp #EXPLODE
        beq _boom
        cmp #WAIT
        beq _none
        cmp #GONE
        beq _none
        lda ship_blink          ; blinking: hidden 4 frames
        and #%00000100          ; in 8
        bne _none
        lda ship_type           ; block: 128 + type * 6
        asl a                   ; + figure * 2
        adc ship_type
        adc figure
        asl a
        adc #SPRITE_BLOCK
        sta POINTERS_A
        sta POINTERS_B
        adc #1                  ; its colour layer next
        sta POINTERS_A + 1
        sta POINTERS_B + 1
        ldx ship_type
        lda ship_accent,x
        sta $d027
        lda ship_own,x
        sta $d028
_both:
        jsr ship_xy
        lda px
        sta $d000
        sta $d002
        lda py
        sta $d001
        sta $d003
        lda #%00000011
        sta enable
        ldx px + 1              ; the ninth bits
        beq +
        sta ship_bits
+       rts
_boom:
        ldx ship_timer          ; the explosion: sparks in
        lda explosion_block,x   ; sprite 0, the fireball in
        sta POINTERS_A          ; sprite 1
        sta POINTERS_B
        clc
        adc #1
        sta POINTERS_A + 1
        sta POINTERS_B + 1
        lda explosion_spark,x
        sta $d027
        lda explosion_own,x
        sta $d028
        jmp _both
_none:
        ldx #0                  ; no ship
        jsr sprite_off
        ldx #1
        jmp sprite_off

; The four shots as objects 0-3 of this frame's bank (the
; multiplexer shows them): y register (255: none), x
; register (and its ninth bit), block, colour. The y
; register, the block and the colour are kept from when
; they change; unrolled. Then objects 22 and 23.
export_shots:
        ldy obj_base            ; Y: object 0 of the bank
        .for e_k in range(4)
        .block
        lda shot_mask + e_k
        bne _on
        lda #NONE               ; none
        sta obj_y + e_k,y
        jmp _done
_on:
        lda shot_yr + e_k
        sta obj_y + e_k,y
        lda shot_blk + e_k
        sta obj_block + e_k,y
        lda shot_col + e_k
        sta obj_colour + e_k,y
        clc
        lda shot_x + e_k
        adc #24
        sta obj_x + e_k,y
        lda shot_xh + e_k
        adc #0
        beq _low                ; the ninth bit: $ff
        lda #$ff
_low:
        sta obj_xh + e_k,y
_done:
        .bend
        .endfor
        jmp export_more         ; the satellite, the missile

half_image:
        .byte 0, 1, 2, 0

; The ship's sprite place: px = x + 24, px + 1 its ninth
; bit; py = y + 50.
ship_xy:
        clc
        lda ship_x
        adc #24
        sta px
        lda ship_xh
        adc #0
        and #1
        sta px + 1
        clc
        lda ship_y
        adc #50
        sta py
        rts

; Sprite X off: block 0 in both screens, colour 0, place 0.
sprite_off:
        lda #0
        sta POINTERS_A,x
        sta POINTERS_B,x
        sta $d027,x
        txa
        asl a
        tay
        lda #0
        sta $d000,y
        sta $d001,y
        rts

; The sprites' bits: no routine reads them (a table left
; behind by an earlier version of the program).
sprite_bit:
        .byte 1, 2, 4, 8, 16, 32, 64, 128

; The shield's notches (full, empty, none past the ship's
; own), the ships left (LIVES_MAX places) and the weapon's
; pips, in the HUD, when they change; then the score; first
; the boss's bar.
update_hud:
        jsr boss_hud
        lda hud_dirty
        beq _done
        lda #0
        sta hud_dirty
        ldx ship_type
        lda ship_shield,x
        sta temp
        ldx #0
_notch:
        lda #SHIELD_FULL_CODE
        cpx shield
        bcc +
        lda #SHIELD_EMPTY_CODE
        cpx temp
        bcc +
        lda #0
+       sta SCREEN_A + HUD_CELL + HUD_SHIELD,x
        inx
        cpx #6
        bne _notch
        ldx #0
_life:
        lda #SHIP_ICON_CODE
        cpx ship_lives
        bcc +
        lda #0
+       sta SCREEN_A + HUD_CELL + HUD_SHIPS,x
        inx
        cpx #LIVES_MAX
        bne _life
        jsr weapon_pips         ; the weapon's level
_done:
        jmp score_digits        ; and the score, if changed
