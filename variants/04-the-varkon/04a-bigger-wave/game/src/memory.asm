; STARBRAZE II - where things are in memory.

; VIC-II bank 1, $4000-$7fff
SCREEN_A  = $4000               ; two screens: one shown,
SCREEN_B  = $4400               ; one made ready
CHARSET   = $4800               ; the playfield's characters
HUDSET    = $5000               ; the HUD's characters
SPRITES   = $6000               ; the sprites, 64 bytes each
POINTERS_A = SCREEN_A + $3f8    ; the eight sprite pointers,
POINTERS_B = SCREEN_B + $3f8    ; one set a screen
COLOURS   = $d800               ; the colour RAM

; $d018: a screen and the characters at $0800 (the
; playfield) or $1000 (the HUD, always on screen A).
D018_A    = %00000010
D018_B    = %00010010
HUD_D018  = %00000100
D016_BASE = %00010000           ; multicolour, 38 columns

; Raster lines: row R of the playfield starts on line
; 51 + 8 R; the HUD's rows 22-24 on lines 227-250.
TOP_LINE  = 20                  ; in the upper border
FAR_LINE  = 132                 ; in row 10: the far layer
NEAR_LINE = 164                 ; in row 14: the near again
COLOUR_LINE = 131               ; rows 0-9 shown: colours
FIELD_LINE = 70                 ; the field's interrupts
HUD_LINE  = 227                 ; the HUD's first line
HUD_ROW   = 22
HUD_CELL  = HUD_ROW * 40

; The playfield's rows: the near layer is rows 0-9 and
; 14-21 (14 always blank), the far layer rows 10-13 (10 the
; same all along). Its metatile rows, two cell rows each:
NEAR_MROWS = [0, 1, 2, 3, 4, 7, 8, 9, 10]
FAR_MROWS  = [5, 6]
READY     = 7                   ; prep_stage: back screen ok
JOY_FIRE  = %00010000

; The module of title.asm (the start of a game), in the
; store, at the end of memory.
TITLE_AT  = $f800

; Zero page
src       = $fb                 ; two bytes: where to read
dst       = $fd                 ; two bytes: where to write
vector    = $f9                 ; two bytes: a routine
count     = $f8
row       = $f7                 ; a row of the playfield
star      = $f6                 ; a star, 0 - STAR_COUNT-1
last      = $f5                 ; the row's last star + 1
sky       = $f4                 ; the row's blank sky
ring_code = $f3                 ; the row's star character

; Variables
frame_count = $02               ; +1 a frame (top interrupt)
frame_flag  = $03               ; 1: the HUD has started
joy         = $04               ; the joystick, 1 = pushed
camera      = $05               ; 2 bytes: the level's x at
cam_frac    = $07               ; the left edge; 256ths
speed       = $08               ; 2 bytes, 256ths a frame
next        = $0a               ; 2 bytes: the next camera
next_frac   = $0c
front       = $0d               ; 0: screen A shown, 1: B
prep_stage  = $0e               ; 0-6 to do, 7 ready
swap_flag   = $0f               ; 1: show the back screen
far_flag    = $10               ; 1: far layer one column on
restart_flag = $11              ; 1: the level's end
far_cam     = $12               ; 2 bytes: (camera + 1) / 2
far_col     = $14               ; far_cam / 8
shown_d018  = $15               ; for the interrupts:
near_d016   = $16               ; the screen, the scrolls
far_d016    = $17
column      = $18               ; 2 bytes: a level column
fine        = $1a
fresh       = $1b               ; 1: stars in a new screen
shift       = $1c               ; 6 bytes: star_planes'
                                ; sc and sp
temp        = $22
cb_col      = $23               ; 2 bytes: the colour RAM's
                                ; column (colour_row)
star_rec    = $0300             ; a star's cell, $ff none
                                ; (screen B's: star + 32)
star_col    = $0340             ; a row's first cell (B's:
                                ; row + 16)
edge_chars  = $0360             ; a column: 22 characters
edge_far    = $03a0             ; a far column: rows 10-13
plane_cell  = $03b0             ; the planes' U / 8,
plane_pix   = $03b3             ; U AND 7

; The ship (ship.asm), and others
ship_type   = $33               ; 0-2
ship_xf     = $34               ; x: 256ths, pixels, high
ship_x      = $35               ; byte (signed: it comes in
ship_xh     = $36               ; from x = -16)
ship_yf     = $37               ; y: 256ths, lines
ship_y      = $38
ship_mode   = $39               ; CONTROL ... ENTER
ship_timer  = $3a
ship_blink  = $3b               ; frames left: no damage
ship_push   = $3c               ; frames left of a push
push_dx     = $3d               ; -2, 0, 2 pixels a frame
push_dy     = $3e
shield      = $3f               ; notches
ship_lives  = $40
cooldown    = $41               ; frames to the next shot
figure      = $42               ; 0 level, 1 up, 2 down
hud_dirty   = $44               ; 1: shield or ships changed
touch       = $45               ; the points on the rock
spot        = $46
px          = $47               ; 2 bytes: a pixel's x, y
py          = $49
q           = $4a               ; x - fine scroll
rock_fine   = $4b               ; the next frame's scroll
slot        = $4c
rock_page   = $4d               ; and screen: 0 A, 4 B
enable      = $4e               ; $d015, $d010 being made
row_end     = $50               ; star_fixups: the last + 1
swap_row    = $51               ; colour_next: the row
turn_count  = $52               ; frame_count at the turn
shot_mask   = $03c0             ; 4 bytes each: the halves
shot_kind   = $03c4             ; alive (0: free), the kind,
shot_x      = $03c8             ; x, its high byte, y
shot_xh     = $03cc
shot_y      = $03d0
shot_air    = $03d4             ; 1: in the corridor
shot_blk    = $03d8             ; as an object: its block,
shot_col    = $03dc             ; its colour, its y register
shot_yr     = $03f1
fp_cell     = $03f5             ; the planes kept for ahead
fp_pix      = $03f8             ; (stars.asm), their camera
front_cam   = $03fb             ; 2 bytes
bp_cell     = $0790             ; the planes of the swap's
bp_pix      = $0793             ; camera (back_top)
cb_first    = $03e0             ; 17: each colour row's
                                ; first boundary in view
        .cerror shot_yr < cb_first + COLOUR_SLOTS

; The multiplexer (mux.asm): objects on sprites 2-7,
; and the interrupts (irq.asm)
obj_base    = $53               ; this frame's bank: 0, 24
mux_count   = $54               ; the plan's entries
mux_next    = $55               ; the next for the interrupt
mux_end     = $56               ; how many it writes
mux_ready   = $57               ; 1: the plan is made
fixed_line  = $58               ; the next fixed write
b_i         = $59               ; making the plan
b_o         = $5a
b_key       = $5b
b_low       = $5c
b_pos       = $5d
b_valid     = $5e               ; crowded: b_low, b_pos kept
b_done      = $5f
b_free      = $60
b_start     = $61
b_end       = $62
d010_now    = $63               ; $d010 as last written
ship_bits   = $64               ; the ship's $d010 bits
left_n      = $65               ; left out: by this plan,
prev_n      = $66               ; by the plan before
irq_a       = $67               ; the field's interrupts:
irq_x       = $68               ; the registers kept
irq_y       = $69

; The Varkon (varkon.asm)
wave_ptr    = $6a               ; the next wave
anim        = $6b               ; +1 a frame: the pictures
anim3       = $6c               ; the Varkon's picture
v_base      = $6d               ; the next frame's bank
v_i         = $6e               ; a Varkon
v_j         = $6f               ; a shot
v_k         = $70               ; a wave's member
v_tmp       = $71               ; 2 bytes
w_delay     = $73               ; start_wave: the member's
w_y         = $74               ; delay, y, first shot
w_fire      = $75
FIRST_ENEMY = 4                 ; objects: the Varkon,
FIRST_ESHOT = 4 + ENEMIES       ; their shots

; The stars (stars.asm): which camera, which screen
star_cam    = $76               ; 2 bytes
star_page   = $78               ; 0: screen A, 4: screen B
rec_off     = $79               ; its records: star + 0 or
col_off     = $7a               ; 32, row + 0 or 16
back_page   = $7b               ; star_fixups: 0 or 4
swap_next   = $7c               ; ahead: 1 if a swap comes

; The scrolling (scroll.asm)
speed_ix    = $7d               ; the camera's speed entry

; More variables
cam_step    = $25               ; 3 bytes: the camera's move
                                ; to the next frame, 256ths
hurt_n      = $7f               ; hurt: notches
f_x         = $dd               ; fire_plasma: the shot's x,
f_xh        = $de               ; its high byte, y, its
f_y         = $df               ; entry in the fire tables,
f_entry     = $e0               ; its place
f_slot      = $eb
leap_col    = $e9               ; 2 bytes: takeoff's column

; The weapon (weapons.asm): the ship's speed, the weapon and
; its level. Page 2 is free: the KERNAL is out.
cur_speed_lo = $ec              ; the ship's speed: its own
cur_speed_hi = $ed              ; + the S capsules', 256ths
w_index     = $ee               ; the weapon: ship * 4 +
weapon      = $ef               ; level; its level, 0-3
shot_dy     = $0200             ; 4 each: y velocity (lines
shot_bl     = $0208             ; a frame)
s_caps      = $020c             ; S capsules taken, 0-3
fv_left     = $021d             ; fire: shots to place, the
fv_entry    = $021e             ; entry
s_pos       = $022e             ; the plan (mux.asm): the
s_key       = $022f             ; place in order_s, its
s_obj       = $0230             ; object's y and number
turn_wait   = $0231             ; 1: after a restart (main)
WEAPONS_END = $0232

; In page 2 after the others: the arena (scroll.asm).
arena       = $0232             ; 1: the camera has stopped
; The level (0: level 1), unpacked at its start (level.asm);
; lz_unpack's end (2 bytes).
level       = $0251
lz_end      = $0253
; Only for the tests by hand (the test build, TEST_BUILD:
; main.asm; ship.asm, test_step): the keys I and L (bits 0,
; 1), the frame before's; 1: the ship cannot be hurt (key I;
; in the game always 0).
test_keys   = $0255
test_prev   = $0256
invuln      = $0257
TEST_I      = %00000001
TEST_L      = %00000010
; lz_unpack (level.asm): the store's byte get_src read; the
; packed stream's bits (a 1 after the last); 1 after
; literals; a number in gamma.
lz_byte     = $02b6
lz_bits     = $02b7
lz_after    = $02b8
lz_g        = $02b9
PAGE2_END   = $02c1
        .cerror PAGE2_END > star_rec, "page 2's variables"

; From AUDIO the rest of the code (main.asm).
AUDIO       = $8000

; Objects: two banks of 24 (OBJ_BANK): the ship's shots 0-3,
; the Varkon 4-15, their shots 16-21, 22 and 23 unused.
obj_y       = $0400             ; y register, 255: none
obj_x       = $0430             ; x register, low 8 bits
obj_xh      = $0460             ; $ff: x register over 255
obj_block   = $0490
obj_colour  = $04c0
obj_pri     = $04f0             ; priority, both banks (48)
order       = $0538             ; the objects in order of y
                                ; (the Varkon's, the ship's)
plan_ix     = $0550             ; the plan: its object's
                                ; place in this bank,
plan_y      = $0568             ; its y register,
acc_trig    = $0580             ; the line to write it,
left_list   = $0598             ; left out by this plan
prev_list   = $05b0             ; and by the plan before

; The Varkon: 12 each. Places: x is the sprite's x
; register (x + 24), 256ths, pixels, high byte (signed);
; y the playfield's line (the register is y + 50).
en_on       = $0600
en_kind     = $060c
en_delay    = $0618
en_seg      = $0624             ; the stretch of its path
en_left     = $0630             ; frames left in it
en_vxl      = $063c             ; velocity, 256ths of a
en_vxh      = $0648             ; pixel a frame
en_vyl      = $0654
en_vyh      = $0660
en_xf       = $066c
en_x        = $0678
en_xh       = $0684
en_yf       = $0690
en_y        = $069c
en_fire     = $06a8             ; frames to its next shot
en_vxs      = $06b4             ; vx's sign: 0 or $ff
en_block    = $06c0             ; its kind's: first picture,
en_colour   = $06cc             ; colour, frames between
en_period   = $06d8             ; shots

; Their shots: 6 each. x: the x register, pixels and high
; byte (signed); they fly by sh_vx whole pixels a frame
; (signed: the turrets' go up and right too); y in 256ths,
; with vy.
sh_on       = $06e4
sh_x        = $06ea
sh_xh       = $06f0
sh_yf       = $06f6
sh_y        = $06fc
sh_vx       = $0702
sh_vyl      = $0708
sh_vyh      = $070e
VARKON_END  = $0714

; 12 each: hits left, the behaviour (PATH, HOP, TURRET), the
; turret's aim (0 left, 1 up, 2 right).
en_life     = $0760
en_beh      = $0778
en_aim      = $0784
MORE_END    = $0790
; 12: the pictures' mask (3: four, 1: two).
en_pmask    = $07a8
pc_colour   = $07bb             ; start_paint's colour,
pc_bound    = $07bc             ; boundary, row
pc_slot     = $07bd
PAGE7_END   = $07c9
        .cerror PAGE7_END > $0800, "page 7's variables"
        .cerror MORE_END > bp_cell, "en_*: on bp_cell"
