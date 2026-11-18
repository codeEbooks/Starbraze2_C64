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
HUD_D018  = %00000100
D016_BASE = %00010000           ; multicolour, 38 columns

; Raster lines: row R of the playfield starts on line
; 51 + 8 R; the HUD's rows 22-24 on lines 227-250.
TOP_LINE  = 20                  ; in the upper border
FAR_LINE  = 132                 ; in row 10: the far layer
NEAR_LINE = 164                 ; in row 14: the near again
FIELD_LINE = 70                 ; the field's interrupts
HUD_LINE  = 227                 ; the HUD's first line
HUD_ROW   = 22
HUD_CELL  = HUD_ROW * 40

; The playfield's rows: the near layer is rows 0-9 and
; 14-21 (14 always blank), the far layer rows 10-13 (10 the
; same all along). Its metatile rows, two cell rows each:
NEAR_MROWS = [0, 1, 2, 3, 4, 7, 8, 9, 10]
FAR_MROWS  = [5, 6]

; The module of title.asm (the start of a game), in the
; store, at the end of memory.
TITLE_AT  = $f800

; Zero page
src       = $fb                 ; two bytes: where to read
dst       = $fd                 ; two bytes: where to write
vector    = $f9                 ; two bytes: a routine
count     = $f8

; Variables
frame_count = $02               ; +1 a frame (top interrupt)
frame_flag  = $03               ; 1: the HUD has started
camera      = $05               ; 2 bytes: the level's x at
cam_frac    = $07               ; the left edge; 256ths
front       = $0d               ; 0: screen A shown, 1: B
far_cam     = $12               ; 2 bytes: (camera + 1) / 2
far_col     = $14               ; far_cam / 8
shown_d018  = $15               ; for the interrupts:
near_d016   = $16               ; the screen, the scrolls
far_d016    = $17
column      = $18               ; 2 bytes: a level column
temp        = $22
edge_chars  = $0360             ; a column: 22 characters
edge_far    = $03a0             ; a far column: rows 10-13

; The interrupts (irq.asm)
fixed_line  = $58               ; the next fixed write
irq_a       = $67               ; the field's interrupts:
irq_x       = $68               ; the registers kept
irq_y       = $69

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

; From AUDIO the rest of the code (main.asm).
AUDIO       = $8000

pc_colour   = $07bb             ; start_paint's colour,
pc_bound    = $07bc             ; boundary, row
pc_slot     = $07bd
PAGE7_END   = $07c9
        .cerror PAGE7_END > $0800, "page 7's variables"
