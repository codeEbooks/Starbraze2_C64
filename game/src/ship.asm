; The ship and its shots. {4}
;|; The ship. {3-3}
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
; No notches left: it explodes, a ship is lost, a wait; then {16}
; another ship is chosen (states.asm), the game held, and it {16}
; comes in from the left with a full shield, blinking. No {16}
; ships left: GAME OVER, then the title. At the start of a {16}
; game the ship is chosen first, then flies from its place {16}
; (START_X, ENTER_Y). {16}
;|; No notches left: it explodes, a ship is lost, a wait, then {3-15}
;|; it comes back in from the left with a full shield, {3-15}
;|; blinking. No ships left: three more, and the game goes on. {3-15}
; {4}
; Fire held: the weapon's volley (weapons.asm) every so many {4}
; frames, while its shots have free places among the four {4}
; (objects 0-3 of the multiplexer). The shots fly right {4}
; (some climb or dive) and end on the rock, past the right {4}
; edge or out of the playfield; each half of a double bolt {4}
; ends on its own. {4}
; A Gauss shot bursts. The missile and the satellite fly {6}
; with the ship (weapons.asm). {6}
; {8}
; After the boss (boss.asm, STAGE CLEAR) the ship flies off {8}
; to the right (LEAVE), then is gone (GONE); with the next {8}
; level it comes back in from the left. In the arena the {8}
; rock is read in the characters themselves: the boss's body {8}
; is made of characters that change. {8}

CONTROL = 0
EXPLODE = 1
WAIT    = 2
ENTER   = 3
LEAVE   = 4 ; {8}
GONE    = 5 ; {8}
CHOOSE  = 6                     ; held: being chosen {16}
JOY_UP    = %00000001
JOY_DOWN  = %00000010
JOY_LEFT  = %00000100
JOY_RIGHT = %00001000

; The joystick and the keys, 1 = pushed: SPACE (bit 0: the {16}
; pause, states.asm), F1, F3, F5, F7 (bits 3-6: the sound's {16}
; mode, player.asm; those just pushed: new_keys, in the main {16}
; loop after joy_ready). {16}
;|; The joystick and the keys, 1 = pushed: F1, F3, F5, F7 {7-15}
;|; (bits 3-6: the sound's mode, player.asm; those just {7-15}
;|; pushed: new_keys, in the main loop after joy_ready). {7-15}
;|; The joystick, 1 = pushed. {3-6}
; In the test build (TEST_BUILD: main.asm) also the keys I
; and L (test_keys, bits 0-1), only for the tests by hand
; (test_step). Port A of CIA 1 is an input for the joystick;
; for the keys it drives one row of the keyboard low at a
; time.
read_input:
        .if RECORD_GAME != 0 ; {17}
        lda #JOY_FIRE           ; to record: Fire held {17}
        .else ; {17}
        lda $dc00               ; joystick 2
        eor #%11111111
        and #%00011111
        .fi ; {17}
        sta joy
        lda #$ff                ; port A out: the rows
        sta $dc02
        lda #%01111111          ; row 7: SPACE on bit 4 {16}
        sta $dc00 ; {16}
        lda $dc01 ; {16}
        eor #%11111111 ; {16}
        and #%00010000 ; {16}
        lsr a ; {16}
        lsr a ; {16}
        lsr a ; {16}
        lsr a ; {16}
        sta keys ; {16}
        lda #%11111110          ; row 0: F1, F3, F5 on bits {7}
        sta $dc00               ; 4-6, F7 on bit 3 {7}
        lda $dc01 ; {7}
        eor #%11111111 ; {7}
        sta temp ; {7}
        and #%01110000          ; F1, F3, F5: keys bits 3-5 {7}
        lsr a ; {7}
        ora keys ; {16}
        sta keys ; {7}
        lda temp ; {7}
        and #%00001000          ; F7: bit 6 {7}
        asl a ; {7}
        asl a ; {7}
        asl a ; {7}
        ora keys ; {7}
        sta keys ; {7}
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

; Only in the test build (TEST_BUILD), for the tests by {8}
; hand: the keys I and L just pushed. I: the ship cannot be {8}
; hurt (hurt does nothing: the rock still pushes it), or can {8}
; again; the border red while it cannot. L: the next level {8}
; at once, as after STAGE CLEAR (restart_flag: the main {8}
; loop), only while the ship flies (CONTROL). Called after {8}
; joy_ready, where the tests write test_keys, if a key is {8}
; down or was before. {8}
;|; Only in the test build (TEST_BUILD), for the tests by {3-7}
;|; hand: the keys I and L just pushed. I: the ship cannot be {3-7}
;|; hurt (hurt does nothing: the rock still pushes it), or can {3-7}
;|; again; the border red while it cannot. L: the next level {3-7}
;|; at once (restart_flag: the main loop), only while the ship {3-7}
;|; flies (CONTROL). Called after joy_ready, where the tests {3-7}
;|; write test_keys, if a key is down or was before. {3-7}
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
        sta cooldown ; {4}
        ldx ship_type
        lda ship_shield,x
        sta shield
        lda #ENTER_BLINK
        sta ship_blink
        lda #1
        sta hud_dirty
        rts

;{8}
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
;{}

; The next level after STAGE CLEAR (main loop): the ship {8}
; comes in from the left with a full shield, its satellite {8}
; with it. {8}
;|; A ship lost (update_ship), the level again (main loop): {6-7}
;|; the ship comes in from the left with a full shield, its {6-7}
;|; satellite with it. {6-7}
;|; A ship lost (update_ship), the level again (main loop): {3-5}
;|; the ship comes in from the left with a full shield. {3-5}
ship_again:
        lda #ENTER_X
        ldx #$ff
        ldy #ENTER
        jsr come_in
        lda ship_x ; {6}
        sta sat_x ; {6}
        lda ship_xh ; {6}
        sta sat_xh ; {6}
        lda ship_y ; {6}
        sta sat_y ; {6}
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
        bne _other ; {8}
;|        bne _enter ; {3-7}
        inc ship_timer          ; the wait
        lda ship_timer
        cmp #WAIT_FRAMES
        bne _shots
        lda ship_lives          ; no ships left: GAME {16}
        bne +                   ; OVER (states.asm) {16}
        lda #HELD_OVER ; {16}
        sta held ; {16}
        bne _shots              ; (always) {16}
+       jsr choose_lost         ; another ship chosen {16}
;|        lda ship_lives          ; no ships left: three {3-15}
;|        bne +                   ; more {3-15}
;|        lda #LIVES ; {3-15}
;|        sta ship_lives ; {3-15}
;|+       jsr ship_again          ; in again, from the left {3-15}
        jmp _shots
_other: ; {8}
        cmp #LEAVE              ; off to the right; {8}
        bcc _enter              ; gone: nothing {8}
        bne _shots ; {8}
        jsr ship_leave ; {8}
        jmp _shots ; {8}
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
        jmp fly_shots ; {4}
;|        rts ; {3-3}

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
        bne _fire ; {4}
;|        bne _done ; {3-3}
        jsr collide
_fire: ; {4}
        jsr move_satellite      ; after the ship {6}
        lda cooldown ; {4}
        beq + ; {4}
        dec cooldown ; {4}
+       lda ship_mode ; {4}
        bne _done               ; it has just exploded {4}
        lda joy ; {4}
        and #JOY_FIRE ; {4}
        beq _done ; {4}
        lda cooldown ; {4}
        bne _done ; {4}
        jsr fire ; {4}
_done:
        jmp fly_shots ; {4}
;|        rts ; {3-3}

; The five points against the rock; a push, the damage. All {11}
; five in the corridor (rows 10-14, ship_y from {11}
; ship_air_from to ship_air_to - 1): no rock there (unless a {11}
; boss's body is there: air_rock). {11}
;|; The five points against the rock; a push, the damage. All {3-10}
;|; five in the corridor (rows 10-14, ship_y from {3-10}
;|; ship_air_from to ship_air_to - 1): no rock there. {3-10}
collide:
        ldx ship_type
        lda air_rock            ; a body in the corridor? {11}
        bne + ; {11}
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

; The ship hit: A notches off its shield, unless it blinks {17}
; or the key I of the test build (or a recording) has made {17}
; it unhurtable (invuln); it blinks for HIT_BLINK frames; no {17}
; notches left, it explodes and a ship is lost. X and Y {17}
; kept. {17}
;|; The ship hit: A notches off its shield, unless it blinks {3-16}
;|; or the key I of the test build has made it unhurtable {3-16}
;|; (invuln); it blinks for HIT_BLINK frames; no notches left, {3-16}
;|; it explodes and a ship is lost. X and Y kept. {3-16}
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
        bne _hurt ; {7}
;|        bne _done ; {3-6}
        lda #EXPLODE            ; no notches left
        sta ship_mode
        lda #0
        sta ship_timer
        dec ship_lives
        tya                     ; the weapon a level down, {6}
        pha                     ; the satellite lost {6}
        jsr weapon_down ; {6}
        pla ; {6}
        tay ; {6}
        lda #FX_EXPLODE ; {7}
        jmp sfx_start ; {7}
;|        rts ; {3-6}
_hurt: ; {7}
        lda #FX_HURT ; {7}
        jmp sfx_start ; {7}
_done:
        rts

spot_first:
        .byte 0, 5, 10

;{4}
; Shot X: the line of its point for the hits, the middle of {5}
; its halves left (hit_y, $ff if none); its picture (a {5}
; double bolt's by its halves: both, the upper, the lower). {5}
;|; Shot X: its picture (a double bolt's by its halves: both, {4-4}
;|; the upper, the lower). {4-4}
shot_line:
        lda shot_mask,x
        beq _none
        lda shot_kind,x         ; kind * 4 + its halves {5}
        asl a ; {5}
        asl a ; {5}
        ora shot_mask,x ; {5}
        tay ; {5}
        lda shot_y,x ; {5}
        clc ; {5}
        adc shot_mid,y ; {5}
        sta hit_y,x ; {5}
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
        lda #$ff ; {5}
        sta hit_y,x ; {5}
        rts
;{}

;{4}
; The shots fly on: past the right edge they end; one that
; climbs or dives moves its y too, and ends out of the
; playfield.
; Their points for the hits go with them (hit_x by half the {5}
; speed; hit_y when the y moves). {5}
; A blast counts its frames down (its pictures), then ends. {6}
; Then the missile (weapons.asm). {6}
; The rock: shots_rock, after the sprites are written.
fly_shots:
        ldx #3
_shot:
        lda shot_mask,x
        bne +
        jmp _next
+       lda shot_bl,x ; {6}
        beq + ; {6}
        jmp _blast ; {6}
+       ldy shot_kind,x
        lda hit_x,x             ; its point: half the speed {5}
        clc                     ; (an even number) {5}
        adc shot_half,y ; {5}
        sta hit_x,x ; {5}
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
        lda shot_dy,x ; {5}
        clc ; {5}
        adc hit_y,x ; {5}
        sta hit_y,x ; {5}
        jmp _next
_end:
        lda #0
        sta shot_mask,x
        lda #$ff ; {5}
        sta hit_y,x ; {5}
        bne _next ; {6}
_blast: ; {6}
        dec shot_bl,x           ; a blast: its frames {6}
        beq _end ; {6}
        ldy shot_bl,x           ; its picture {6}
        lda blast_block,y ; {6}
        sta shot_blk,x ; {6}
        lda blast_own,y ; {6}
        sta shot_col,x ; {6}
_next:
        dex
        bmi +
        jmp _shot
+       jmp fly_missile ; {6}
;|+       rts ; {4-5}
;{}

;{4}
; The shots against the rock, after the sprites are written
; (a shot that meets it shows there a frame, then ends): a
; half on the rock ends (a double bolt has two, the others
; one: the upper).
; A Gauss shot bursts (its blast from the next frame). {6}
; A shot in the corridor (shot_air) never meets the rock {11}
; (unless a boss's body is there: air_rock); nor does a {11}
; blast. {11}
;|; A shot in the corridor (shot_air) never meets the rock; {6-10}
;|; nor does a blast. {6-10}
;|; A shot in the corridor (shot_air) never meets the rock. {4-5}
shots_rock:
        ldx #3
_shot:
        lda shot_mask,x
        beq _next
        lda shot_bl,x ; {6}
        bne _next               ; a blast: no rock {6}
        lda air_rock            ; a body in the corridor? {11}
        bne + ; {11}
        lda shot_air,x          ; in the corridor: no rock
        bne _next
+ ; {11}
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
        ldy shot_kind,x         ; on the rock: a Gauss shot {6}
        lda shot_blast,y        ; bursts {6}
        beq + ; {6}
        lda #$ff                ; (no Varkon met) {6}
        sta bl_skip ; {6}
        jsr start_blast ; {6}
        jmp _next ; {6}
+       lda shot_mask,x         ; the others end {6}
;|        lda shot_mask,x         ; it ends {4-5}
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
;{}

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
        ldx arena_chars         ; the crawler's arena: {8}
        bne _chars              ; from the characters {8}
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
;{8}
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
;{}

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

; Sprites 0 and 1, the ship, for this frame: sprite 0 its {4}
; accent, 1 its colour layer (multicolour); or the {4}
; explosion's sparks and fireball; or off (waiting, or {4}
; hidden while it blinks). Registers and pointers in both {4}
; screens; their bits of $d015 in `enable`, of $d010 in {4}
; ship_bits (plan_sprites writes those registers). {4}
;|; Sprites 0 and 1, the ship, for this frame: sprite 0 its {3-3}
;|; accent, 1 its colour layer (multicolour); or the {3-3}
;|; explosion's sparks and fireball; or off (waiting, or {3-3}
;|; hidden while it blinks). Registers and pointers in both {3-3}
;|; screens; their bits of $d015 in `enable`, of $d010 in {3-3}
;|; ship_bits (the main loop writes those registers). {3-3}
ship_sprites:
        lda #0
        sta enable
        sta ship_bits
        lda ship_mode
        cmp #EXPLODE
        beq _boom
        cmp #WAIT
        beq _none
        cmp #GONE ; {8}
        beq _none ; {8}
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

;{4}
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
        jmp export_more         ; the satellite, the missile {6}
;|        rts ; {4-5}

half_image:
        .byte 0, 1, 2, 0
;{}

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

; The shield's notches (full, empty, none past the ship's {8}
; own), the ships left (LIVES_MAX places) and the weapon's {8}
; pips, in the HUD, when they change; then the score; first {8}
; the boss's bar. {8}
;|; The shield's notches (full, empty, none past the ship's {6-7}
;|; own), the ships left (LIVES_MAX places) and the weapon's {6-7}
;|; pips, in the HUD, when they change; then the score. {6-7}
;|; The shield's notches (full, empty, none past the ship's {5-5}
;|; own) and the ships left (LIVES_MAX places), in the HUD, {5-5}
;|; when they change; then the score. {5-5}
;|; The shield's notches (full, empty, none past the ship's {3-4}
;|; own) and the ships left (LIVES_MAX places), in the HUD, {3-4}
;|; when they change. {3-4}
update_hud:
        jsr boss_hud ; {8}
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
        jsr weapon_pips         ; the weapon's level {6}
_done:
        jmp score_digits        ; and the score, if changed {5}
;|        rts ; {3-4}
