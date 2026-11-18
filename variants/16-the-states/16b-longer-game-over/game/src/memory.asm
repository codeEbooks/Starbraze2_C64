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

; The title's module (title.asm), in phase 1's store, at the
; end of memory: over the other files' (their levels'
; bosses).
TITLE_AT  = $f800
MUSIC_AT  = $f000               ; phase 1's songs

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
keys        = $30               ; SPACE bit 0, F1-F7
prev_keys   = $31
new_keys    = $32
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
high        = $4f
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
shown_score = $0796             ; the score's bytes in the
shown_hi    = $0799             ; HUD (score.asm)
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

; The hits (hits.asm): the targets of a frame, made once
; (hit_prepare), and the box of the Varkon being tried; the
; score (score.asm); others.
cam_step    = $25               ; 3 bytes: the camera's move
                                ; to the next frame, 256ths
e_top       = $28               ; a Varkon's box: top (y
e_left      = $29               ; register), left (x reg.
e_h         = $2a               ; / 2), height, width
e_w         = $2b
near_top    = $2c               ; the Varkon to try: y
near_span   = $2d               ; register near_top + 0-span
hs_top      = $2e               ; the shots' points: top,
hs_bottom   = $2f               ; bottom
sb_on       = $7e               ; 1: the ship can be hit
hurt_n      = $7f               ; hurt: notches
sb_left     = $cd               ; the ship's box against the
sb_right    = $ce               ; Varkon: x register / 2,
sb_top      = $cf               ; y register
sb_bottom   = $d0
pb_left     = $d1               ; against the plasma (its
pb_top      = $d2               ; middle): left, top, width,
pb_w        = $d3               ; height
pb_h        = $d4
hit_x       = $d5               ; 4 bytes: the ship's shots'
hit_y       = $d9               ; points ($ff: none)
f_x         = $dd               ; fire_plasma: the shot's x,
f_xh        = $de               ; its high byte, y, its
f_y         = $df               ; entry in the fire tables,
f_entry     = $e0               ; its place
f_slot      = $eb
score       = $e1               ; 3 bytes, BCD: 6 digits
hi_score    = $e4               ; 3 bytes: the best so far
next_life   = $e7               ; BCD: the next ship at
                                ; score + 2 = this (10 000s)
score_dirty = $e8               ; 1: the HUD's digits to do
leap_col    = $e9               ; 2 bytes: takeoff's column

; The weapons (weapons.asm): the level, the speed, the
; missile, the satellite, the blasts. Page 2 is free: the
; KERNAL is out.
cur_speed_lo = $ec              ; the ship's speed: its own
cur_speed_hi = $ed              ; + the S capsules', 256ths
w_index     = $ee               ; the weapon: ship * 4 +
weapon      = $ef               ; level; its level, 0-3
blast_armed = $f0               ; 1: a blast to try (next)
m_on        = $f1               ; the missile: 0 none, 1
sat_on      = $f2               ; falling, 2 running; 1: the
                                ; satellite flies
shot_dy     = $0200             ; 4 each: y velocity (lines
shot_pl     = $0204             ; a frame), the Varkon 0-7
shot_bl     = $0208             ; pierced, blast frames
s_caps      = $020c             ; S capsules taken, 0-3
missiles    = $020d             ; 1: the M capsule taken
sat_x       = $020e             ; the satellite: x, its high
sat_xh      = $020f             ; byte, y
sat_y       = $0210
m_x         = $0211             ; the missile: x, high byte,
m_xh        = $0212             ; y; its point for the hits
m_y         = $0213             ; (x register / 2, y
m_hx        = $0214             ; register; $ff none)
m_hy        = $0215
bl_left     = $0216             ; the blast armed: its box
bl_top      = $0217             ; (x register / 2, y
bl_right    = $0218             ; register; right, bottom
bl_bottom   = $0219             ; excluded), its damage, the
bl_dmg      = $021a             ; Varkon it hit (not again,
bl_skip     = $021b             ; $ff none)
blast_now   = $021c             ; 1: one tried this frame
fv_left     = $021d             ; fire: shots to place, the
fv_entry    = $021e             ; entry; hits: the shot
fv_shot     = $021f
m_col       = $0221             ; 2 bytes: a level column
cap_keep    = $0223             ; take_capsule: Y kept
shot_ph     = $0224             ; 4: pierced, Varkon 8-11
bn_left     = $0228             ; the blast tried this frame
bn_top      = $0229             ; (bl_* when it was armed)
bn_right    = $022a
bn_bottom   = $022b
bn_dmg      = $022c
bn_skip     = $022d
s_pos       = $022e             ; the plan (mux.asm): the
s_key       = $022f             ; place in order_s, its
s_obj       = $0230             ; object's y and number
turn_wait   = $0231             ; 1: after a restart (main)
WEAPONS_END = $0232

; The boss (boss.asm), in page 2 after the weapons: the
; arena, the boss's step, its body (where it goes; on the
; screen: x, variant, set, column; the set in the making),
; its parts (their Varkon), its mouth, its end, its bar in
; the HUD.
arena       = $0232             ; 1: the camera has stopped
boss_state  = $0233             ; B_*
boss_timer  = $0234
body_x      = $0235             ; multicolour pixels from
body_xf     = $0236             ; the left edge; 256ths
body_var    = $0237             ; bit 0 mouth, bit 1 hatch
shown_x     = $0238             ; the body on the screen
shown_var   = $0239
shown_set   = $023a             ; its characters' set, 0/1
shown_col   = $023b             ; its first column (40 none)
prep_x      = $023c             ; the other set, being made:
prep_var    = $023d             ; x, variant; 0 nothing, 1
prep_step   = $023e             ; columns 0-7 made
patrol      = $023f             ; the patrol's entry, 0-3
patrol_left = $0240             ; frames to wait there
part_a      = $0241             ; the Varkon of the cannons
part_b      = $0242             ; and of the core ($ff:
part_core   = $0243             ; none yet)
parts       = $0244             ; alive: bits 0, 1 cannons,
                                ; 2 the core
mouth_timer = $0245             ; frames to the next drone
drone_turn  = $0246             ; 0 the drone up, 1 low
chain_k     = $0247             ; the chain's next blast
bar_want    = $0248             ; the bar's steps: to show,
bar_shown   = $0249             ; shown
bar_dirty   = $024a             ; 1: the HUD's cells to do
flash_left  = $024b             ; frames of the white hull
part_x      = $024c             ; 2 bytes: 2 x the body's x
b_tmp       = $024e             ; 2 bytes
BOSS_END    = $0250
; The level (0: level 1), unpacked at its start (level.asm);
; its beams (beams.asm): the frame of their cycle;
; lz_unpack's end (2 bytes).
level       = $0251
beam_timer  = $0252
lz_end      = $0253
; Only for the tests by hand (the test build, TEST_BUILD:
; main.asm; ship.asm, test_step): the keys I and L (bits 0,
; 1), the frame before's; 1: the ship cannot be hurt (key I;
; in the game on the disk always 0).
test_keys   = $0255
test_prev   = $0256
invuln      = $0257
TEST_I      = %00000001
TEST_L      = %00000010
; The boss engine's (boss.asm): 1: the arena's rock from the
; characters (the SIEGE CRAWLER's body); the SHIELD CORE's
; (core.asm): its segments' turn (2 bytes: 256ths of a step,
; the step 0-63), the gap's segment, its radius, the closed
; radius (these three after the turn's step: core_place
; compares the four with cb_last, the ones it placed the
; segments by), the frames of the gap's cycle, the core's
; shots in its burst, the segments' Varkon (4), the sphere's
; cells to do in the next turn (cb_paint: 0 nothing, 1 on, 2
; its colours, 3 white, 4 gone); seg_off's scratch; cb_last;
; the arena's 36 cells under the sphere (codes, then
; colours: cb_save).
arena_chars = $0258
cb_angle    = $0259
cb_open_k   = $025b
cb_open_r   = $025c
cb_rad      = $025d
cb_open_t   = $025e
cb_shots    = $025f
cb_seg      = $0260
cb_paint    = $0264
CB_END      = $0265
m_sign      = $0265
m_a         = $0266
m_b         = $0267
m_r         = $0268
m_lo        = $0269
cb_last     = $026a             ; 4 bytes
cb_save     = $026e             ; 72 bytes
CB_SAVE_END = $02b6
; lz_unpack (level.asm): the store's byte get_src read; the
; packed stream's bits (a 1 after the last); 1 after
; literals; a number in gamma.
lz_byte     = $02b6
lz_bits     = $02b7
lz_after    = $02b8
lz_g        = $02b9
; 1 while the GRAVEYARD WARDEN's body is in the arena
; (warden.asm): rows 10-14 can be rock, the ship's and the
; shots' shortcut of the corridor is off (0 at the level's
; start: boss_reset).
air_rock    = $02ba
; The states (states.asm): the game held (HELD_*: the
; choice, the pause, GAME OVER), GAME OVER's frames left,
; the joystick of the frame before (the choice, the title),
; the SID's volume kept, hud_say's colour and end.
held        = $02bb
held_time   = $02bc
joy_prev    = $02bd
held_vol    = $02be
say_colour  = $02bf
say_end     = $02c0
PAGE2_END   = $02c1
        .cerror PAGE2_END > star_rec, "page 2's variables"
        .cerror bl_skip - bl_left != 5, "bl_*: in order"
        .cerror bn_skip - bn_left != 5, "bn_*: in order"

; The sound (player.asm, effects.asm): the code and its data
; from AUDIO; its variables in zero page and after the
; Varkon's.
AUDIO       = $8000
mus_frame   = $80               ; 2 bytes: +1 a frame
mus_tick    = $82               ; frames left of the step
mus_tempo   = $83               ; the step: 0-3
mus_song    = $84
mus_on      = $85               ; 1: the music plays
mus_first   = $86               ; 1: before its first step
mus_ptr     = $87               ; 2 bytes: a pattern, a list
mus_work    = $89
mus_note    = $8a
mus_freq    = $8b               ; 2 bytes
mus_voices  = $8d               ; the voices it sounds: 3, 2
sound_mode  = $8e               ; MODE_*
sfx_new     = $8f               ; sfx_start: the effect
sfx_keep    = $90               ; 2 bytes: X and Y kept
fx_voice    = $92               ; sfx_play: the voice
sid_shadow  = $93               ; 25 bytes: the SID's copy
; a voice of the music: 3 bytes each, voices 0-2; in zero
; page what voice_frame reads every frame
v_left      = $ac               ; steps left of the note
v_note      = $af
v_wave      = $b2               ; its wavetable row
v_gate      = $b5
v_pw_lo     = $b8               ; its pulse width
v_pw_hi     = $bb
v_sweep     = $be
v_vib       = $c1               ; frames before the vibrato
v_ctrl      = $c4
v_fresh     = $c7               ; 1: a note has started
v_ins       = $ca               ; the note's instrument
SOUND_ZP_END = $cd
v_list_lo   = $0720             ; its order list
v_list_hi   = $0723
v_order     = $0726             ; its place in the list
v_ptr_lo    = $0729             ; where its pattern goes on
v_ptr_hi    = $072c
v_trans     = $072f             ; the pattern's semitones
v_dur       = $0732             ; steps a note
v_pins      = $0735             ; the pattern's instrument
p_ready     = $0738             ; 1: the next note is read:
p_note      = $073b             ; the note (REST, SONG_END),
p_ins       = $073e             ; its instrument, its steps
p_left      = $0741
; an effect on a voice: 3 bytes each
fx_pos      = $0744             ; its next row (0: none)
fx_tick     = $0747             ; frames left of the row
fx_speed    = $074a             ; frames a row
fx_pri      = $074d             ; its priority (0: none)
fx_next     = $0750             ; one waiting: number + 1
SOUND_END   = $0753

; Objects: two banks of 24 (OBJ_BANK): the ship's shots 0-3,
; the Varkon 4-15, their shots 16-21, the satellite 22, the
; missile 23.
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

; 12 each: hits left, frames of the white flash after a hit,
; the behaviour (PATH, HOP, TURRET), the turret's aim (0
; left, 1 up, 2 right). An exploding Varkon counts its
; explosion's frames in en_left.
en_life     = $0760
en_flash    = $076c
en_beh      = $0778
en_aim      = $0784
MORE_END    = $0790
en_cap      = $079c             ; 12: capsule, 1 + WSMOE
CAPS_END    = $07a8
; 12: the pictures' mask (3: four, 1: two); fire_fan's,
; mine_near's, split's.
en_pmask    = $07a8
f_fan       = $07b4             ; the fan's next entry,
f_count     = $07b5             ; how many still, the
f_who       = $07b6             ; Varkon
mn_obj      = $07b7             ; the mine's object
sp_path     = $07b8             ; the shard's path, its
sp_dy       = $07b9             ; line under the rock's,
sp_rock     = $07ba             ; the rock
pc_colour   = $07bb             ; start_paint's colour,
pc_bound    = $07bc             ; boundary, row
pc_slot     = $07bd
; The files from the disk (phase.asm; phases.py: phase 1's,
; then a level each)
file_now    = $07be             ; the file in the store
disk_dev    = $07bf             ; the drive (8, 9 ...)
ph_want     = $07c0             ; the file being read
ph_sum      = $07c1             ; the file's bytes added
ph_last     = $07c2             ; its last byte
ph_ok       = $07c3             ; the status bits allowed
ph_step     = $07c4             ; two bytes: a cell's bytes
ph_left     = $07c6             ; two: left to the next
ph_cell     = $07c8             ; the bar's cells full
PAGE7_END   = $07c9
; Row 1 of the HUD kept while the game is held (states.asm):
; its codes after the plan's lists (page 5), its colours
; after the phases' (page 7).
hud_keep    = $05c8             ; 40 bytes
hud_keep_c  = $07c9             ; 40
        .cerror hud_keep < prev_list + 24, "hud_keep"
        .cerror hud_keep + 40 > en_on, "hud_keep"
        .cerror hud_keep_c + 40 > $0800, "hud_keep_c"
        .cerror PAGE7_END > $0800, "page 7's variables"
        .cerror MORE_END > bp_cell, "en_*: on bp_cell"
        .cerror SOUND_END > en_life, "en_*: on the sound"
