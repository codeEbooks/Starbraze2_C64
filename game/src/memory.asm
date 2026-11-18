; STARBRAZE II - where things are in memory.

; VIC-II bank 1, $4000-$7fff
SCREEN_A  = $4000               ; two screens: one shown,
SCREEN_B  = $4400               ; one made ready
CHARSET   = $4800               ; the playfield's characters
HUDSET    = $5000               ; the HUD's characters
SPRITES   = $6000               ; the sprites, 64 bytes each
POINTERS_A = SCREEN_A + $3f8    ; the eight sprite pointers, {3}
POINTERS_B = SCREEN_B + $3f8    ; one set a screen {3}
COLOURS   = $d800               ; the colour RAM

; $d018: a screen and the characters at $0800 (the
; playfield) or $1000 (the HUD, always on screen A).
D018_A    = %00000010
D018_B    = %00010010 ; {2}
HUD_D018  = %00000100
D016_BASE = %00010000           ; multicolour, 38 columns

; Raster lines: row R of the playfield starts on line
; 51 + 8 R; the HUD's rows 22-24 on lines 227-250.
TOP_LINE  = 20                  ; in the upper border
FAR_LINE  = 132                 ; in row 10: the far layer
NEAR_LINE = 164                 ; in row 14: the near again
COLOUR_LINE = 131               ; rows 0-9 shown: colours {2}
FIELD_LINE = 70                 ; the field's interrupts
HUD_LINE  = 227                 ; the HUD's first line
HUD_ROW   = 22
HUD_CELL  = HUD_ROW * 40

; The playfield's rows: the near layer is rows 0-9 and
; 14-21 (14 always blank), the far layer rows 10-13 (10 the
; same all along). Its metatile rows, two cell rows each:
NEAR_MROWS = [0, 1, 2, 3, 4, 7, 8, 9, 10]
FAR_MROWS  = [5, 6]
READY     = 7                   ; prep_stage: back screen ok {2}
JOY_FIRE  = %00010000 ; {4}

; The title's module (title.asm), in phase 1's store, at the {16}
; end of memory: over the other files' (their levels' {16}
; bosses). {16}
;|; The module of title.asm (the start of a game), in phase {10-15}
;|; 1's store, at the end of memory. {10-15}
;|; The module of title.asm (the start of a game), in the {1-9}
;|; store, at the end of memory. {1-9}
TITLE_AT  = $f800
MUSIC_AT  = $f000               ; phase 1's songs {7}

; Zero page
src       = $fb                 ; two bytes: where to read
dst       = $fd                 ; two bytes: where to write
vector    = $f9                 ; two bytes: a routine
count     = $f8
row       = $f7                 ; a row of the playfield {2}
star      = $f6                 ; a star, 0 - STAR_COUNT-1 {2}
last      = $f5                 ; the row's last star + 1 {2}
sky       = $f4                 ; the row's blank sky {2}
ring_code = $f3                 ; the row's star character {2}

; Variables
frame_count = $02               ; +1 a frame (top interrupt)
frame_flag  = $03               ; 1: the HUD has started
joy         = $04               ; the joystick, 1 = pushed {3}
camera      = $05               ; 2 bytes: the level's x at
cam_frac    = $07               ; the left edge; 256ths
speed       = $08               ; 2 bytes, 256ths a frame {2}
next        = $0a               ; 2 bytes: the next camera {2}
next_frac   = $0c ; {2}
front       = $0d               ; 0: screen A shown, 1: B
prep_stage  = $0e               ; 0-6 to do, 7 ready {2}
swap_flag   = $0f               ; 1: show the back screen {2}
far_flag    = $10               ; 1: far layer one column on {2}
restart_flag = $11              ; 1: the level's end {3}
far_cam     = $12               ; 2 bytes: (camera + 1) / 2
far_col     = $14               ; far_cam / 8
shown_d018  = $15               ; for the interrupts:
near_d016   = $16               ; the screen, the scrolls
far_d016    = $17
column      = $18               ; 2 bytes: a level column
fine        = $1a ; {2}
fresh       = $1b               ; 1: stars in a new screen {2}
shift       = $1c               ; 6 bytes: star_planes' {2}
                                ; sc and sp {2}
temp        = $22
cb_col      = $23               ; 2 bytes: the colour RAM's {2}
                                ; column (colour_row) {2}
star_rec    = $0300             ; a star's cell, $ff none {2}
                                ; (screen B's: star + 32) {2}
star_col    = $0340             ; a row's first cell (B's: {2}
                                ; row + 16) {2}
edge_chars  = $0360             ; a column: 22 characters
edge_far    = $03a0             ; a far column: rows 10-13
plane_cell  = $03b0             ; the planes' U / 8, {2}
plane_pix   = $03b3             ; U AND 7 {2}

; The ship (ship.asm), and others {3}
;|; Others {2-2}
keys        = $30               ; SPACE bit 0, F1-F7 {16}
;|keys        = $30               ; F1-F7 {7-15}
prev_keys   = $31 ; {7}
new_keys    = $32 ; {7}
ship_type   = $33               ; 0-2 {3}
ship_xf     = $34               ; x: 256ths, pixels, high {3}
ship_x      = $35               ; byte (signed: it comes in {3}
ship_xh     = $36               ; from x = -16) {3}
ship_yf     = $37               ; y: 256ths, lines {3}
ship_y      = $38 ; {3}
ship_mode   = $39               ; CONTROL ... ENTER {3}
ship_timer  = $3a ; {3}
ship_blink  = $3b               ; frames left: no damage {3}
ship_push   = $3c               ; frames left of a push {3}
push_dx     = $3d               ; -2, 0, 2 pixels a frame {3}
push_dy     = $3e ; {3}
shield      = $3f               ; notches {3}
ship_lives  = $40 ; {3}
cooldown    = $41               ; frames to the next shot {4}
figure      = $42               ; 0 level, 1 up, 2 down {3}
hud_dirty   = $44               ; 1: shield or ships changed {3}
touch       = $45               ; the points on the rock {3}
spot        = $46 ; {3}
px          = $47               ; 2 bytes: a pixel's x, y {3}
py          = $49 ; {3}
q           = $4a               ; x - fine scroll {3}
rock_fine   = $4b               ; the next frame's scroll {3}
slot        = $4c ; {2}
rock_page   = $4d               ; and screen: 0 A, 4 B {3}
enable      = $4e               ; $d015, $d010 being made {3}
high        = $4f ; {16}
row_end     = $50               ; star_fixups: the last + 1 {2}
swap_row    = $51               ; colour_next: the row {2}
turn_count  = $52               ; frame_count at the turn {2}
shot_mask   = $03c0             ; 4 bytes each: the halves {4}
shot_kind   = $03c4             ; alive (0: free), the kind, {4}
shot_x      = $03c8             ; x, its high byte, y {4}
shot_xh     = $03cc ; {4}
shot_y      = $03d0 ; {4}
shot_air    = $03d4             ; 1: in the corridor {4}
shot_blk    = $03d8             ; as an object: its block, {4}
shot_col    = $03dc             ; its colour, its y register {4}
shot_yr     = $03f1 ; {4}
fp_cell     = $03f5             ; the planes kept for ahead {2}
fp_pix      = $03f8             ; (stars.asm), their camera {2}
front_cam   = $03fb             ; 2 bytes {2}
bp_cell     = $0790             ; the planes of the swap's {2}
bp_pix      = $0793             ; camera (back_top) {2}
shown_score = $0796             ; the score's bytes in the {5}
shown_hi    = $0799             ; HUD (score.asm) {5}
cb_first    = $03e0             ; 17: each colour row's {2}
                                ; first boundary in view {2}
        .cerror shot_yr < cb_first + COLOUR_SLOTS ; {4}

; The multiplexer (mux.asm): objects on sprites 2-7, {4}
; and the interrupts (irq.asm) {4}
;|; The interrupts (irq.asm) {1-3}
obj_base    = $53               ; this frame's bank: 0, 24 {4}
mux_count   = $54               ; the plan's entries {4}
mux_next    = $55               ; the next for the interrupt {4}
mux_end     = $56               ; how many it writes {4}
mux_ready   = $57               ; 1: the plan is made {4}
fixed_line  = $58               ; the next fixed write
b_i         = $59               ; making the plan {4}
b_o         = $5a ; {4}
b_key       = $5b ; {4}
b_low       = $5c ; {4}
b_pos       = $5d ; {4}
b_valid     = $5e               ; crowded: b_low, b_pos kept {4}
b_done      = $5f ; {4}
b_free      = $60 ; {4}
b_start     = $61 ; {4}
b_end       = $62 ; {4}
d010_now    = $63               ; $d010 as last written {4}
ship_bits   = $64               ; the ship's $d010 bits {3}
left_n      = $65               ; left out: by this plan, {4}
prev_n      = $66               ; by the plan before {4}
irq_a       = $67               ; the field's interrupts:
irq_x       = $68               ; the registers kept
irq_y       = $69

; The Varkon (varkon.asm) {4}
wave_ptr    = $6a               ; the next wave {4}
anim        = $6b               ; +1 a frame: the pictures {4}
anim3       = $6c               ; the Varkon's picture {4}
v_base      = $6d               ; the next frame's bank {4}
v_i         = $6e               ; a Varkon {4}
v_j         = $6f               ; a shot {4}
v_k         = $70               ; a wave's member {4}
v_tmp       = $71               ; 2 bytes {4}
w_delay     = $73               ; start_wave: the member's {4}
w_y         = $74               ; delay, y, first shot {4}
w_fire      = $75 ; {4}
FIRST_ENEMY = 4                 ; objects: the Varkon, {4}
FIRST_ESHOT = 4 + ENEMIES       ; their shots {4}

; The stars (stars.asm): which camera, which screen {2}
star_cam    = $76               ; 2 bytes {2}
star_page   = $78               ; 0: screen A, 4: screen B {2}
rec_off     = $79               ; its records: star + 0 or {2}
col_off     = $7a               ; 32, row + 0 or 16 {2}
back_page   = $7b               ; star_fixups: 0 or 4 {2}
swap_next   = $7c               ; ahead: 1 if a swap comes {2}

; The scrolling (scroll.asm) {2}
speed_ix    = $7d               ; the camera's speed entry {2}

; The hits (hits.asm): the targets of a frame, made once {5}
; (hit_prepare), and the box of the Varkon being tried; the {5}
; score (score.asm); others. {5}
;|; More variables {3-4}
cam_step    = $25               ; 3 bytes: the camera's move {4}
                                ; to the next frame, 256ths {4}
e_top       = $28               ; a Varkon's box: top (y {5}
e_left      = $29               ; register), left (x reg. {5}
e_h         = $2a               ; / 2), height, width {5}
e_w         = $2b ; {5}
near_top    = $2c               ; the Varkon to try: y {5}
near_span   = $2d               ; register near_top + 0-span {5}
hs_top      = $2e               ; the shots' points: top, {5}
hs_bottom   = $2f               ; bottom {5}
sb_on       = $7e               ; 1: the ship can be hit {5}
hurt_n      = $7f               ; hurt: notches {3}
sb_left     = $cd               ; the ship's box against the {5}
sb_right    = $ce               ; Varkon: x register / 2, {5}
sb_top      = $cf               ; y register {5}
sb_bottom   = $d0 ; {5}
pb_left     = $d1               ; against the plasma (its {5}
pb_top      = $d2               ; middle): left, top, width, {5}
pb_w        = $d3               ; height {5}
pb_h        = $d4 ; {5}
hit_x       = $d5               ; 4 bytes: the ship's shots' {5}
hit_y       = $d9               ; points ($ff: none) {5}
f_x         = $dd               ; fire_plasma: the shot's x, {4}
f_xh        = $de               ; its high byte, y, its {4}
f_y         = $df               ; entry in the fire tables, {4}
f_entry     = $e0               ; its place {4}
f_slot      = $eb ; {4}
score       = $e1               ; 3 bytes, BCD: 6 digits {5}
hi_score    = $e4               ; 3 bytes: the best so far {5}
next_life   = $e7               ; BCD: the next ship at {5}
                                ; score + 2 = this (10 000s) {5}
score_dirty = $e8               ; 1: the HUD's digits to do {5}
leap_col    = $e9               ; 2 bytes: takeoff's column {4}

; The weapons (weapons.asm): the level, the speed, the {6}
; missile, the satellite, the blasts. Page 2 is free: the {6}
; KERNAL is out. {6}
;|; The weapon (weapons.asm): the ship's speed, the weapon and {4-5}
;|; its level. Page 2 is free: the KERNAL is out. {4-5}
;|; The ship's speed. Page 2 is free: the KERNAL is out. {3-3}
cur_speed_lo = $ec              ; the ship's speed: its own {3}
cur_speed_hi = $ed              ; + the S capsules', 256ths {4}
;|cur_speed_hi = $ed              ; (256ths) {3-3}
w_index     = $ee               ; the weapon: ship * 4 + {4}
weapon      = $ef               ; level; its level, 0-3 {4}
blast_armed = $f0               ; 1: a blast to try (next) {6}
m_on        = $f1               ; the missile: 0 none, 1 {6}
sat_on      = $f2               ; falling, 2 running; 1: the {6}
                                ; satellite flies {6}
shot_dy     = $0200             ; 4 each: y velocity (lines {4}
shot_pl     = $0204             ; a frame), the Varkon 0-7 {6}
shot_bl     = $0208             ; pierced, blast frames {6}
;|shot_bl     = $0208             ; a frame) {4-5}
s_caps      = $020c             ; S capsules taken, 0-3 {4}
missiles    = $020d             ; 1: the M capsule taken {6}
sat_x       = $020e             ; the satellite: x, its high {6}
sat_xh      = $020f             ; byte, y {6}
sat_y       = $0210 ; {6}
m_x         = $0211             ; the missile: x, high byte, {6}
m_xh        = $0212             ; y; its point for the hits {6}
m_y         = $0213             ; (x register / 2, y {6}
m_hx        = $0214             ; register; $ff none) {6}
m_hy        = $0215 ; {6}
bl_left     = $0216             ; the blast armed: its box {6}
bl_top      = $0217             ; (x register / 2, y {6}
bl_right    = $0218             ; register; right, bottom {6}
bl_bottom   = $0219             ; excluded), its damage, the {6}
bl_dmg      = $021a             ; Varkon it hit (not again, {6}
bl_skip     = $021b             ; $ff none) {6}
blast_now   = $021c             ; 1: one tried this frame {6}
fv_left     = $021d             ; fire: shots to place, the {4}
fv_entry    = $021e             ; entry; hits: the shot {5}
;|fv_entry    = $021e             ; entry {4-4}
fv_shot     = $021f ; {5}
m_col       = $0221             ; 2 bytes: a level column {6}
cap_keep    = $0223             ; take_capsule: Y kept {6}
shot_ph     = $0224             ; 4: pierced, Varkon 8-11 {6}
bn_left     = $0228             ; the blast tried this frame {6}
bn_top      = $0229             ; (bl_* when it was armed) {6}
bn_right    = $022a ; {6}
bn_bottom   = $022b ; {6}
bn_dmg      = $022c ; {6}
bn_skip     = $022d ; {6}
s_pos       = $022e             ; the plan (mux.asm): the {4}
s_key       = $022f             ; place in order_s, its {4}
s_obj       = $0230             ; object's y and number {4}
turn_wait   = $0231             ; 1: after a restart (main) {3}
WEAPONS_END = $0232 ; {3}

; The boss (boss.asm), in page 2 after the weapons: the {8}
; arena, the boss's step, its body (where it goes; on the {8}
; screen: x, variant, set, column; the set in the making), {8}
; its parts (their Varkon), its mouth, its end, its bar in {8}
; the HUD. {8}
;|; In page 2 after the others: the arena (scroll.asm). {2-7}
arena       = $0232             ; 1: the camera has stopped {2}
boss_state  = $0233             ; B_* {8}
boss_timer  = $0234 ; {8}
body_x      = $0235             ; multicolour pixels from {8}
body_xf     = $0236             ; the left edge; 256ths {8}
body_var    = $0237             ; bit 0 mouth, bit 1 hatch {8}
shown_x     = $0238             ; the body on the screen {8}
shown_var   = $0239 ; {8}
shown_set   = $023a             ; its characters' set, 0/1 {8}
shown_col   = $023b             ; its first column (40 none) {8}
prep_x      = $023c             ; the other set, being made: {8}
prep_var    = $023d             ; x, variant; 0 nothing, 1 {8}
prep_step   = $023e             ; columns 0-7 made {8}
patrol      = $023f             ; the patrol's entry, 0-3 {8}
patrol_left = $0240             ; frames to wait there {8}
part_a      = $0241             ; the Varkon of the cannons {8}
part_b      = $0242             ; and of the core ($ff: {8}
part_core   = $0243             ; none yet) {8}
parts       = $0244             ; alive: bits 0, 1 cannons, {8}
                                ; 2 the core {8}
mouth_timer = $0245             ; frames to the next drone {8}
drone_turn  = $0246             ; 0 the drone up, 1 low {8}
chain_k     = $0247             ; the chain's next blast {8}
bar_want    = $0248             ; the bar's steps: to show, {8}
bar_shown   = $0249             ; shown {8}
bar_dirty   = $024a             ; 1: the HUD's cells to do {8}
flash_left  = $024b             ; frames of the white hull {8}
part_x      = $024c             ; 2 bytes: 2 x the body's x {8}
b_tmp       = $024e             ; 2 bytes {8}
BOSS_END    = $0250 ; {8}
; The level (0: level 1), unpacked at its start (level.asm); {9}
; its beams (beams.asm): the frame of their cycle; {9}
; lz_unpack's end (2 bytes). {9}
;|; The level (0: level 1), unpacked at its start (level.asm); {1-8}
;|; lz_unpack's end (2 bytes). {1-8}
level       = $0251
beam_timer  = $0252 ; {9}
lz_end      = $0253
; Only for the tests by hand (the test build, TEST_BUILD: {17}
; main.asm; ship.asm, test_step): the keys I and L (bits 0, {17}
; 1), the frame before's; 1: the ship cannot be hurt (key I; {17}
; the recordings; in the game on the disk always 0). {17}
;|; Only for the tests by hand (the test build, TEST_BUILD: {10-16}
;|; main.asm; ship.asm, test_step): the keys I and L (bits 0, {10-16}
;|; 1), the frame before's; 1: the ship cannot be hurt (key I; {10-16}
;|; in the game on the disk always 0). {10-16}
;|; Only for the tests by hand (the test build, TEST_BUILD: {3-9}
;|; main.asm; ship.asm, test_step): the keys I and L (bits 0, {3-9}
;|; 1), the frame before's; 1: the ship cannot be hurt (key I; {3-9}
;|; in the game always 0). {3-9}
test_keys   = $0255 ; {3}
test_prev   = $0256 ; {3}
invuln      = $0257 ; {3}
TEST_I      = %00000001 ; {3}
TEST_L      = %00000010 ; {3}
; The boss engine's (boss.asm): 1: the arena's rock from the {9}
; characters (the SIEGE CRAWLER's body); the SHIELD CORE's {9}
; (core.asm): its segments' turn (2 bytes: 256ths of a step, {9}
; the step 0-63), the gap's segment, its radius, the closed {9}
; radius (these three after the turn's step: core_place {9}
; compares the four with cb_last, the ones it placed the {9}
; segments by), the frames of the gap's cycle, the core's {9}
; shots in its burst, the segments' Varkon (4), the sphere's {9}
; cells to do in the next turn (cb_paint: 0 nothing, 1 on, 2 {9}
; its colours, 3 white, 4 gone); seg_off's scratch; cb_last; {9}
; the arena's 36 cells under the sphere (codes, then {9}
; colours: cb_save). {9}
;|; The boss engine's (boss.asm): 1: the arena's rock from the {8-8}
;|; characters (the SIEGE CRAWLER's body); then the bytes to {8-8}
;|; CB_SAVE_END, 0 at the level's start (boss_reset). {8-8}
arena_chars = $0258 ; {8}
cb_angle    = $0259 ; {9}
cb_open_k   = $025b ; {9}
cb_open_r   = $025c ; {9}
cb_rad      = $025d ; {9}
cb_open_t   = $025e ; {9}
cb_shots    = $025f ; {9}
cb_seg      = $0260 ; {9}
cb_paint    = $0264 ; {9}
CB_END      = $0265 ; {9}
m_sign      = $0265 ; {9}
m_a         = $0266 ; {9}
m_b         = $0267 ; {9}
m_r         = $0268 ; {9}
m_lo        = $0269 ; {9}
cb_last     = $026a             ; 4 bytes {9}
cb_save     = $026e             ; 72 bytes {9}
CB_SAVE_END = $02b6 ; {8}
; lz_unpack (level.asm): the store's byte get_src read; the
; packed stream's bits (a 1 after the last); 1 after
; literals; a number in gamma.
lz_byte     = $02b6
lz_bits     = $02b7
lz_after    = $02b8
lz_g        = $02b9
; 1 while the GRAVEYARD WARDEN's body is in the arena {11}
; (warden.asm): rows 10-14 can be rock, the ship's and the {11}
; shots' shortcut of the corridor is off (0 at the level's {11}
; start: boss_reset). {11}
air_rock    = $02ba ; {11}
; The states (states.asm): the game held (HELD_*: the {16}
; choice, the pause, GAME OVER), GAME OVER's frames left, {16}
; the joystick of the frame before (the choice, the title), {16}
; the SID's volume kept, hud_say's colour and end. {16}
held        = $02bb ; {16}
held_time   = $02bc ; {16}
joy_prev    = $02bd ; {16}
held_vol    = $02be ; {16}
say_colour  = $02bf ; {16}
say_end     = $02c0 ; {16}
PAGE2_END   = $02c1
        .cerror PAGE2_END > star_rec, "page 2's variables" ; {2}
        .cerror bl_skip - bl_left != 5, "bl_*: in order" ; {6}
        .cerror bn_skip - bn_left != 5, "bn_*: in order" ; {6}

; The sound (player.asm, effects.asm): the code and its data {7}
; from AUDIO; its variables in zero page and after the {7}
; Varkon's. {7}
;|; From AUDIO the rest of the code (main.asm). {1-6}
AUDIO       = $8000
mus_frame   = $80               ; 2 bytes: +1 a frame {7}
mus_tick    = $82               ; frames left of the step {7}
mus_tempo   = $83               ; the step: 0-3 {7}
mus_song    = $84 ; {7}
mus_on      = $85               ; 1: the music plays {7}
mus_first   = $86               ; 1: before its first step {7}
mus_ptr     = $87               ; 2 bytes: a pattern, a list {7}
mus_work    = $89 ; {7}
mus_note    = $8a ; {7}
mus_freq    = $8b               ; 2 bytes {7}
mus_voices  = $8d               ; the voices it sounds: 3, 2 {7}
sound_mode  = $8e               ; MODE_* {7}
sfx_new     = $8f               ; sfx_start: the effect {7}
sfx_keep    = $90               ; 2 bytes: X and Y kept {7}
fx_voice    = $92               ; sfx_play: the voice {7}
sid_shadow  = $93               ; 25 bytes: the SID's copy {7}
; a voice of the music: 3 bytes each, voices 0-2; in zero {7}
; page what voice_frame reads every frame {7}
v_left      = $ac               ; steps left of the note {7}
v_note      = $af ; {7}
v_wave      = $b2               ; its wavetable row {7}
v_gate      = $b5 ; {7}
v_pw_lo     = $b8               ; its pulse width {7}
v_pw_hi     = $bb ; {7}
v_sweep     = $be ; {7}
v_vib       = $c1               ; frames before the vibrato {7}
v_ctrl      = $c4 ; {7}
v_fresh     = $c7               ; 1: a note has started {7}
v_ins       = $ca               ; the note's instrument {7}
SOUND_ZP_END = $cd ; {7}
v_list_lo   = $0720             ; its order list {7}
v_list_hi   = $0723 ; {7}
v_order     = $0726             ; its place in the list {7}
v_ptr_lo    = $0729             ; where its pattern goes on {7}
v_ptr_hi    = $072c ; {7}
v_trans     = $072f             ; the pattern's semitones {7}
v_dur       = $0732             ; steps a note {7}
v_pins      = $0735             ; the pattern's instrument {7}
p_ready     = $0738             ; 1: the next note is read: {7}
p_note      = $073b             ; the note (REST, SONG_END), {7}
p_ins       = $073e             ; its instrument, its steps {7}
p_left      = $0741 ; {7}
; an effect on a voice: 3 bytes each {7}
fx_pos      = $0744             ; its next row (0: none) {7}
fx_tick     = $0747             ; frames left of the row {7}
fx_speed    = $074a             ; frames a row {7}
fx_pri      = $074d             ; its priority (0: none) {7}
fx_next     = $0750             ; one waiting: number + 1 {7}
SOUND_END   = $0753 ; {7}

; Objects: two banks of 24 (OBJ_BANK): the ship's shots 0-3, {6}
; the Varkon 4-15, their shots 16-21, the satellite 22, the {6}
; missile 23. {6}
;|; Objects: two banks of 24 (OBJ_BANK): the ship's shots 0-3, {4-5}
;|; the Varkon 4-15, their shots 16-21, 22 and 23 unused. {4-5}
obj_y       = $0400             ; y register, 255: none {4}
obj_x       = $0430             ; x register, low 8 bits {4}
obj_xh      = $0460             ; $ff: x register over 255 {4}
obj_block   = $0490 ; {4}
obj_colour  = $04c0 ; {4}
obj_pri     = $04f0             ; priority, both banks (48) {4}
order       = $0538             ; the objects in order of y {4}
                                ; (the Varkon's, the ship's) {4}
plan_ix     = $0550             ; the plan: its object's {4}
                                ; place in this bank, {4}
plan_y      = $0568             ; its y register, {4}
acc_trig    = $0580             ; the line to write it, {4}
left_list   = $0598             ; left out by this plan {4}
prev_list   = $05b0             ; and by the plan before {4}

; The Varkon: 12 each. Places: x is the sprite's x {4}
; register (x + 24), 256ths, pixels, high byte (signed); {4}
; y the playfield's line (the register is y + 50). {4}
en_on       = $0600 ; {4}
en_kind     = $060c ; {4}
en_delay    = $0618 ; {4}
en_seg      = $0624             ; the stretch of its path {4}
en_left     = $0630             ; frames left in it {4}
en_vxl      = $063c             ; velocity, 256ths of a {4}
en_vxh      = $0648             ; pixel a frame {4}
en_vyl      = $0654 ; {4}
en_vyh      = $0660 ; {4}
en_xf       = $066c ; {4}
en_x        = $0678 ; {4}
en_xh       = $0684 ; {4}
en_yf       = $0690 ; {4}
en_y        = $069c ; {4}
en_fire     = $06a8             ; frames to its next shot {4}
en_vxs      = $06b4             ; vx's sign: 0 or $ff {4}
en_block    = $06c0             ; its kind's: first picture, {4}
en_colour   = $06cc             ; colour, frames between {4}
en_period   = $06d8             ; shots {4}

; Their shots: 6 each. x: the x register, pixels and high {4}
; byte (signed); they fly by sh_vx whole pixels a frame {4}
; (signed: the turrets' go up and right too); y in 256ths, {4}
; with vy. {4}
sh_on       = $06e4 ; {4}
sh_x        = $06ea ; {4}
sh_xh       = $06f0 ; {4}
sh_yf       = $06f6 ; {4}
sh_y        = $06fc ; {4}
sh_vx       = $0702 ; {4}
sh_vyl      = $0708 ; {4}
sh_vyh      = $070e ; {4}
VARKON_END  = $0714 ; {4}

; 12 each: hits left, frames of the white flash after a hit, {5}
; the behaviour (PATH, HOP, TURRET), the turret's aim (0 {5}
; left, 1 up, 2 right). An exploding Varkon counts its {5}
; explosion's frames in en_left. {5}
;|; 12 each: hits left, the behaviour (PATH, HOP, TURRET), the {4-4}
;|; turret's aim (0 left, 1 up, 2 right). {4-4}
en_life     = $0760 ; {4}
en_flash    = $076c ; {5}
en_beh      = $0778 ; {4}
en_aim      = $0784 ; {4}
MORE_END    = $0790 ; {4}
en_cap      = $079c             ; 12: capsule, 1 + WSMOE {6}
CAPS_END    = $07a8 ; {6}
; 12: the pictures' mask (3: four, 1: two); fire_fan's, {10}
; mine_near's, split's. {10}
;|; 12: the pictures' mask (3: four, 1: two). {4-9}
en_pmask    = $07a8 ; {4}
f_fan       = $07b4             ; the fan's next entry, {10}
f_count     = $07b5             ; how many still, the {10}
f_who       = $07b6             ; Varkon {10}
mn_obj      = $07b7             ; the mine's object {10}
sp_path     = $07b8             ; the shard's path, its {10}
sp_dy       = $07b9             ; line under the rock's, {10}
sp_rock     = $07ba             ; the rock {10}
pc_colour   = $07bb             ; start_paint's colour,
pc_bound    = $07bc             ; boundary, row
pc_slot     = $07bd
; The files from the disk (phase.asm; phases.py: phase 1's, {10}
; then a level each) {10}
file_now    = $07be             ; the file in the store {10}
disk_dev    = $07bf             ; the drive (8, 9 ...) {10}
ph_want     = $07c0             ; the file being read {10}
ph_sum      = $07c1             ; the file's bytes added {10}
ph_last     = $07c2             ; its last byte {10}
ph_ok       = $07c3             ; the status bits allowed {10}
ph_step     = $07c4             ; two bytes: a cell's bytes {10}
ph_left     = $07c6             ; two: left to the next {10}
ph_cell     = $07c8             ; the bar's cells full {10}
PAGE7_END   = $07c9
; Row 1 of the HUD kept while the game is held (states.asm): {16}
; its codes after the plan's lists (page 5), its colours {16}
; after the phases' (page 7). {16}
hud_keep    = $05c8             ; 40 bytes {16}
hud_keep_c  = $07c9             ; 40 {16}
        .cerror hud_keep < prev_list + 24, "hud_keep" ; {16}
        .cerror hud_keep + 40 > en_on, "hud_keep" ; {16}
        .cerror hud_keep_c + 40 > $0800, "hud_keep_c" ; {16}
        .cerror PAGE7_END > $0800, "page 7's variables"
        .cerror MORE_END > bp_cell, "en_*: on bp_cell" ; {4}
        .cerror SOUND_END > en_life, "en_*: on the sound" ; {7}
