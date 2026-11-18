; The level on the screens: its columns, from the maps of
; metatiles, and the HUD. The levels are packed (lz.py,
; their numbers in bits): each start of a level unpacks its
; own (load_level).
;
; The near map is 9 rows of NEAR_MCOLS metatiles, one row
; after the other: the metatile rows of NEAR_MROWS (cells of
; rows 0-9 and 14-21); the far map 2 rows of FAR_MCOLS (rows
; 10-13). A column of characters is half a metatile: its
; left (TL, BL) or right corners (TR, BR). The colour RAM
; comes from the level's boundaries (start_paint;
; scroll.asm: a colour from its column on); in rows 10-13 it
; keeps the row's colour.

NEAR_ROWS = range(10) .. range(14, 22)

; The level from its start: its data, camera 0, both screens
; drawn (screen A in front), the colour RAM, the scrolls,
; the stars; no Varkon, no objects; no boss (its characters
; the level's again). The caller turns the screen off and
; on.
init_level:
        jsr load_level          ; the level's data
        jsr boss_reset
        lda #0
        sta camera
        sta camera + 1
        sta cam_frac
        sta front
        sta prep_stage
        sta swap_flag
        sta far_flag
        sta restart_flag
        sta speed_ix
        sta column + 1
        sta column              ; the near layer: columns
_near:                          ; 0-39 into both screens
        jsr near_column
        ldy column
        jsr put_near_a
        ldy column
        jsr put_near_b
        inc column
        lda column
        cmp #40
        bne _near
        jsr set_scrolls         ; the far layer: its columns
        sta far_col             ; far_col to far_col + 39
                                ; (screen B's: its row 10;
                                ; 11-13 are never shown)
        lda #0
        sta count
_far:
        clc
        adc far_col
        jsr far_column
        ldy count
        jsr put_far_a
        ldy count
        jsr put_far_b
        inc count
        lda count
        cmp #40
        bne _far
        ldx #39                 ; rows 10-13: the colour of
_paint:                         ; their row
        lda level_far_10
        sta COLOURS + 10 * 40,x
        lda level_far_11
        sta COLOURS + 11 * 40,x
        lda level_far_12
        sta COLOURS + 12 * 40,x
        lda level_far_13
        sta COLOURS + 13 * 40,x
        dex
        bpl _paint
        jsr start_paint         ; rows 0-9, 14-21
        lda #0                  ; the colour boundaries:
        ldx #COLOUR_SLOTS - 1   ; each row from its first
-       sta cb_first,x
        dex
        bpl -
        lda #D018_A
        sta shown_d018
        jsr init_objects        ; no objects, no Varkon
        jsr init_varkon
        jsr start_stars
        jmp swap_back           ; for the first swap

; Rows 0-9 and 14-21 of the colour RAM at the level's start,
; columns 0-39: each row from its first colour
; (start_first), then its boundaries (bound_*, scroll.asm: a
; colour from its column on). Row 14 has none: BOUND_END, an
; end in every level.
start_paint:
        ldx #NEAR_SLOTS - 1     ; X: the row (its slot)
_row:
        lda paint_lo,x
        sta dst
        lda paint_hi,x
        sta dst + 1
        lda start_first,x
        sta pc_colour
        lda paint_at,x          ; its first boundary
        sta pc_bound
        stx pc_slot
        ldy #0                  ; Y: the column
_col:
        ldx pc_bound            ; its next boundary there?
        lda bound_hi,x          ; (256 or more: not yet)
        bne _put
        tya
        cmp bound_lo,x
        bcc _put
        lda bound_colour,x      ; yes: its colour from here
        sta pc_colour
        inc pc_bound
_put:
        lda pc_colour
        sta (dst),y
        iny
        cpy #40
        bne _col
        ldx pc_slot
        dex
        bpl _row
        rts

NEAR_SLOTS = 18
paint_lo:
        .byte <(COLOURS + range(10) * 40)
        .byte <(COLOURS + range(14, 22) * 40)
paint_hi:
        .byte >(COLOURS + range(10) * 40)
        .byte >(COLOURS + range(14, 22) * 40)
paint_at:                       ; (row 14: BOUND_END)
        .byte BOUND_AT_0, BOUND_AT_1, BOUND_AT_2, BOUND_AT_3
        .byte BOUND_AT_4, BOUND_AT_5, BOUND_AT_6, BOUND_AT_7
        .byte BOUND_AT_8, BOUND_AT_9, BOUND_END
        .byte BOUND_AT_15, BOUND_AT_16, BOUND_AT_17
        .byte BOUND_AT_18, BOUND_AT_19, BOUND_AT_20
        .byte BOUND_AT_21
        .cerror BOUND_TOTAL > 256, "start_paint: X"

; A level from its start (the main loop: restart_flag): the
; screen off; the level's file (from the disk if it is not
; in memory: load_file silences the SID); the sound off and
; the music from its start, after the file, which may bring
; its song (it plays from the next frame of the main loop);
; the level from its start, the screen on again. The main
; loop waits for a new frame.
restart_level:
        jsr screen_off
        jsr sprites_all_off
        jsr file_need           ; from the disk
        lda sound_mode          ; the music from its start
        jsr sound_set
        jsr init_level
        jsr screen_on
        lda #0
        sta frame_flag
        rts

; The scroll registers of a camera: near_d016, far_cam and
; far_d016. Fine scroll: 7 minus the 3 low bits, so that the
; picture moves left as the camera goes right. Returns A =
; far_cam / 8, the far layer's column at the left edge.
set_scrolls:
        lda camera
        and #%00000111
        eor #%00000111 | D016_BASE
        sta near_d016
        clc                     ; far_cam = (camera + 1) / 2
        lda camera
        adc #1
        sta far_cam
        lda camera + 1
        adc #0
        lsr a
        sta far_cam + 1
        ror far_cam
        lda far_cam
        and #%00000111
        eor #%00000111 | D016_BASE
        sta far_d016
        lda far_cam             ; far_cam / 8: 8 bits are
        sta temp                ; enough (at most 180)
        lda far_cam + 1
        .rept 3
        lsr a
        ror temp
        .endrept
        lda temp
        rts

; Column `column` of the near layer: its characters to
; edge_chars (rows 0-9, 14-21).
near_column:
        lda column + 1
        lsr a
        lda column
        ror a                   ; A: metatile col., C: side
        tax
        bcc _left
        jmp _right
_left:
        .for k := 0, k < len(NEAR_MROWS), k += 1
        ldy near_map + k * NEAR_MCOLS,x
        lda metatile_tl,y
        sta edge_chars + NEAR_MROWS[k] * 2
        lda metatile_bl,y
        sta edge_chars + NEAR_MROWS[k] * 2 + 1
        .endfor
        rts
_right:
        .for k := 0, k < len(NEAR_MROWS), k += 1
        ldy near_map + k * NEAR_MCOLS,x
        lda metatile_tr,y
        sta edge_chars + NEAR_MROWS[k] * 2
        lda metatile_br,y
        sta edge_chars + NEAR_MROWS[k] * 2 + 1
        .endfor
        rts

; edge_chars into a screen's column Y, rows 0-9 and 14-21;
; their colours into the colour RAM's (paint_near).
put_near .macro screen
        .for r in NEAR_ROWS
        lda edge_chars + r
        sta \screen + r * 40,y
        .endfor
        rts
        .endmacro

put_near_a      #put_near SCREEN_A
put_near_b      #put_near SCREEN_B

; Column A of the far layer: its characters to edge_far
; (rows 10-13).
far_column:
        lsr a                   ; A: metatile col., C: side
        tax
        bcs _right
        ldy far_map,x
        lda metatile_tl,y
        sta edge_far
        lda metatile_bl,y
        sta edge_far + 1
        ldy far_map + FAR_MCOLS,x
        lda metatile_tl,y
        sta edge_far + 2
        lda metatile_bl,y
        sta edge_far + 3
        rts
_right:
        ldy far_map,x
        lda metatile_tr,y
        sta edge_far
        lda metatile_br,y
        sta edge_far + 1
        ldy far_map + FAR_MCOLS,x
        lda metatile_tr,y
        sta edge_far + 2
        lda metatile_br,y
        sta edge_far + 3
        rts

; edge_far into a screen's column Y, rows 10-13.
put_far .macro screen
        .for r in range(10, 14)
        lda edge_far + r - 10
        sta \screen + r * 40,y
        .endfor
        rts
        .endmacro

put_far_a       #put_far SCREEN_A
put_far_b       #put_far SCREEN_B

; (draw_hud, the start of a game, is in title.asm.)

; ---------------------------------------------------------
; The levels, packed
; ---------------------------------------------------------

STEP_LEVELS = 5

; The next level after STAGE CLEAR (after the last, the
; first again).
next_level:
        inc level
        lda level
        cmp #STEP_LEVELS
        bcc +
        lda #0
        sta level
+       rts

; The store of the packed levels into place, once, with the
; module of title.asm: the PRG carries them in pieces
; (data.asm, main.asm). STORE is under the KERNAL and the
; I/O: the RAM there is seen only with $01 = $34 (no
; interrupts meanwhile: here, at the entry, there are none).
move_store:
        lda store_moved
        bne _done
        lda #$34                ; all RAM
        sta $01
        ldx #STAGES - 1
-       lda stage_from_lo,x
        sta src
        lda stage_from_hi,x
        sta src + 1
        lda stage_to_lo,x
        sta dst
        lda stage_to_hi,x
        sta dst + 1
        lda stage_len_lo,x
        sta lz_end
        lda stage_len_hi,x
        sta lz_end + 1
        jsr copy_bytes
        dex
        bpl -
        lda #$35                ; the I/O again
        sta $01
        inc store_moved
_done:
        rts

; The sixth piece: the module of title.asm (the start of a
; game), carried in LEVEL_W1 (data.asm), to TITLE_AT. The
; seventh: phase 1's songs, carried after stage_2
; (main.asm), to MUSIC_AT.
STAGES = 7
STORE_FROM = [stage_0, stage_1, stage_2, stage_3, stage_4]
MOD_FROM = [title_from, music_from]
STAGE_FROM = STORE_FROM .. MOD_FROM
MOD_TO = [TITLE_AT, MUSIC_AT]
STAGE_TO = (STORE + STAGE_OFFS) .. MOD_TO
MOD_LENS = [TITLE_LEN, MUSIC_LEN]
STAGE_LEN = STAGE_LENS .. MOD_LENS
stage_from_lo:
        .byte <STAGE_FROM
stage_from_hi:
        .byte >STAGE_FROM
stage_to_lo:
        .byte <STAGE_TO
stage_to_hi:
        .byte >STAGE_TO
stage_len_lo:
        .byte <STAGE_LEN
stage_len_hi:
        .byte >STAGE_LEN

; lz_end bytes from src to dst (a page at a time, then the
; rest). X kept.
copy_bytes:
        ldy #0
_page:
        lda lz_end + 1
        beq _rest
-       lda (src),y
        sta (dst),y
        iny
        bne -
        inc src + 1
        inc dst + 1
        dec lz_end + 1
        jmp _page
_rest:
        cpy lz_end
        beq _done
        lda (src),y
        sta (dst),y
        iny
        jmp _rest
_done:
        rts

; The level `level`: its packed streams (its characters,
; LEVEL_W2, LEVEL_W1, its pictures: levels.inc) unpacked;
; the rock's table of its characters (make_rock); its
; colours into the interrupt at the top and the VIC-II.
load_level:
        lda level               ; four streams a level
        asl a
        asl a
        tax
        ldy #4
-       lda lz_src_lo,x
        sta src
        lda lz_src_hi,x
        sta src + 1
        lda lz_dst_lo - 1,y     ; the same four in
        sta dst                 ; every level, by Y
        lda lz_dst_hi - 1,y
        sta dst + 1
        lda lz_end_lo,x
        sta lz_end
        lda lz_end_hi,x
        sta lz_end + 1
        txa
        pha
        tya
        pha
        jsr lz_unpack
        pla
        tay
        pla
        tax
        inx
        dey
        bne -
        jsr make_rock
        lda level_d021          ; the level's colours ($d021
        sta top_d021            ; at line 227: irq.asm)
        lda level_d022
        sta $d022
        sta top_d022
        lda level_d023
        sta $d023
        sta top_d023
        jmp beam_reset          ; (beams.asm)

; One packed stream (lz.py) from src to dst, until dst is
; lz_end. Its numbers in bits: a token's first
; bit, 0 literals, 1 a match (none after literals: a match
; always comes); literals: gamma(k), k bytes; a match:
; gamma(h + 1), a byte l, gamma(L - 1): L bytes copied from
; 128 h + l + 1 back, a byte at a time (they may overlap).
; The store's bytes through get_src (under the I/O).
lz_unpack:
        lda #$80                ; no bits yet
        sta lz_bits
        ldy #0
        sty lz_after
_token:
        lda dst                 ; the end?
        cmp lz_end
        lda dst + 1
        sbc lz_end + 1
        bcs _done
        lda lz_after            ; after literals: a match
        bne _after
        jsr get_bit
        bcs _match
        jsr get_gamma           ; literals
        tax
-       jsr get_src
        sta (dst),y
        inc dst
        bne +
        inc dst + 1
+       dex
        bne -
        inc lz_after
        jmp _token
_after:
        dec lz_after
_match:
        jsr get_gamma           ; h + 1
        sec
        sbc #1
        lsr a                   ; (offset - 1) / 256, C: the
        sta vector + 1          ; low byte's top bit
        jsr get_src             ; (C kept)
        bcc +
        ora #%10000000
+       sta vector
        clc                     ; from: dst - (offset - 1)
        lda dst                 ; - 1
        sbc vector
        sta vector
        lda dst + 1
        sbc vector + 1
        sta vector + 1
        jsr get_gamma           ; L - 1
        tax
        inx
-       lda (vector),y          ; a byte at a time
        sta (dst),y
        inc vector
        bne +
        inc vector + 1
+       inc dst
        bne +
        inc dst + 1
+       dex
        bne -
        jmp _token
_done:
        rts

; The stream's next bit into C: from lz_bits, a bit byte
; from the stream when none is left (its first bit at once,
; a 1 after its last: when only that is left, it is empty).
; X, Y kept.
get_bit:
        asl lz_bits
        bne +
        jsr get_src
        sec
        rol a
        sta lz_bits
+       rts

; A number in gamma into A (1-255): its 0 bits, then its own
; after the first 1. Y kept.
get_gamma:
        ldx #0
-       jsr get_bit
        bcs +
        inx
        bne -
+       lda #1
        sta lz_g
        txa
        beq _done
-       jsr get_bit
        rol lz_g
        dex
        bne -
_done:
        lda lz_g
        rts

; The store's next byte (src, then src + 1): the RAM
; under the I/O is seen with $01 = $34, no interrupt
; meanwhile (the I flag as it was after). X, Y kept.
get_src:
        php
        sei
        lda #$34
        sta $01
        lda (src),y
        sta lz_byte
        lda #$35
        sta $01
        plp
src_got:                        ; the tests look here:
        inc src                 ; an interrupt kept waiting
        bne +
        inc src + 1
+       lda lz_byte
        rts

; The rock's table (rock_lines, ship.asm): line L of each
; character's bitmap at L * 256 + its code; 0 for the kept
; codes (the blank, the skies, the stars) and the scenery
; (codes from level_decor; 0: none).
make_rock:
        lda #<CHARSET
        sta src
        lda #>CHARSET
        sta src + 1
        ldx #0                  ; the code
_code:
        ldy #7
        cpx #FIRST_SOLID        ; kept: nothing
        bcc _empty
        lda level_decor         ; scenery: nothing
        beq _solid
        sta temp
        cpx temp
        bcs _empty
_solid:
        .for r_k in range(7, -1, -1)
        ldy #r_k
        lda (src),y
        sta rock_lines + r_k * 256,x
        .endfor
        jmp _next
_empty:
        lda #0
        .for r_k in range(8)
        sta rock_lines + r_k * 256,x
        .endfor
_next:
        lda src                 ; the next code's bitmap
        clc
        adc #8
        sta src
        bcc +
        inc src + 1
+       inx
        bne _code
        rts
