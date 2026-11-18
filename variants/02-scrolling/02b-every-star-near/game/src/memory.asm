; STARBRAZE II - where things are in memory.

; VIC-II bank 1, $4000-$7fff
SCREEN_A  = $4000               ; two screens: one shown,
SCREEN_B  = $4400               ; one made ready
CHARSET   = $4800               ; the playfield's characters
HUDSET    = $5000               ; the HUD's characters
SPRITES   = $6000               ; the sprites, 64 bytes each
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
camera      = $05               ; 2 bytes: the level's x at
cam_frac    = $07               ; the left edge; 256ths
speed       = $08               ; 2 bytes, 256ths a frame
next        = $0a               ; 2 bytes: the next camera
next_frac   = $0c
front       = $0d               ; 0: screen A shown, 1: B
prep_stage  = $0e               ; 0-6 to do, 7 ready
swap_flag   = $0f               ; 1: show the back screen
far_flag    = $10               ; 1: far layer one column on
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

; Others
slot        = $4c
row_end     = $50               ; star_fixups: the last + 1
swap_row    = $51               ; colour_next: the row
turn_count  = $52               ; frame_count at the turn
fp_cell     = $03f5             ; the planes kept for ahead
fp_pix      = $03f8             ; (stars.asm), their camera
front_cam   = $03fb             ; 2 bytes
bp_cell     = $0790             ; the planes of the swap's
bp_pix      = $0793             ; camera (back_top)
cb_first    = $03e0             ; 17: each colour row's
                                ; first boundary in view

; The interrupts (irq.asm)
fixed_line  = $58               ; the next fixed write
irq_a       = $67               ; the field's interrupts:
irq_x       = $68               ; the registers kept
irq_y       = $69

; The stars (stars.asm): which camera, which screen
star_cam    = $76               ; 2 bytes
star_page   = $78               ; 0: screen A, 4: screen B
rec_off     = $79               ; its records: star + 0 or
col_off     = $7a               ; 32, row + 0 or 16
back_page   = $7b               ; star_fixups: 0 or 4
swap_next   = $7c               ; ahead: 1 if a swap comes

; The scrolling (scroll.asm)
speed_ix    = $7d               ; the camera's speed entry

; In page 2 after the others: the arena (scroll.asm).
arena       = $0232             ; 1: the camera has stopped
; The level (0: level 1), unpacked at its start (level.asm);
; lz_unpack's end (2 bytes).
level       = $0251
lz_end      = $0253
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

pc_colour   = $07bb             ; start_paint's colour,
pc_bound    = $07bc             ; boundary, row
pc_slot     = $07bd
PAGE7_END   = $07c9
        .cerror PAGE7_END > $0800, "page 7's variables"
