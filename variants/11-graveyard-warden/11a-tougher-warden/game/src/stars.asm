; The stars of the black sky, rows 0-9, in three planes.
;
; Each row has its plane, the line of the row its stars are
; on, and its own star character (STAR_CODE + row): its one
; pixel is the stars' pixel in their cells, the same for all
; the row's stars, which are on a ring of 40 cells: cell
; (first + star_cells) mod 40. A plane moves at a fraction
; of the camera (shift: camera / 8, / 4, * 3 / 8): where the
; row's ring starts, in pixels from the left of column 0,
;   T = (pixel - 7 + (camera AND 7) - shift) mod 320,
; first = T / 8 and the character's pixel T AND 7.
;
; A star goes in its cell only if the cell is the blank sky
; of its plane; rock hides it. The cells change only when
; `first` changes; the character's pixel is written every
; frame. All this for the camera star_cam, in the screen of
; star_page: in the frame before (ahead, scroll.asm), for
; the next frame's camera, each row once the beam has drawn
; it. The back screen gets its stars in stages 4 and 5, for
; the camera of the swap.
;
; Each screen keeps its own records: the cell of each star
; ($ff: none; screen B's at star + STAR_STRIDE) and the
; first cell of each row's ring (screen B's at row + 16).
; Nothing is exchanged at a swap: the screen in front
; brings its records with it.

; At the start of the level: no stars anywhere; put them
; for the camera in the front screen, and their pixels.
start_stars:
        ldx #2 * STAR_STRIDE - 1
        lda #$ff
-       sta star_rec,x
        dex
        bpl -
        ldx #10 * 8 - 1         ; the ten characters blank
        lda #0
-       sta STAR_FONT,x
        dex
        bpl -
        lda camera
        sta star_cam
        lda camera + 1
        sta star_cam + 1
        lda front
        asl a
        asl a
        sta star_page
        jsr star_setup
        jsr keep_planes         ; ahead goes on from these
        jsr star_pixels
        lda #1                  ; none to take away
        sta fresh
        jsr star_ring
        lda #0
        sta fresh
        rts

; The planes for star_cam; the records of star_page's
; screen.
star_setup:
        jsr star_offsets
        jmp star_planes

star_offsets:
        lda star_page           ; 0 or 4: the records at
        asl a                   ; row + 0 or 16,
        asl a
        sta col_off
        asl a                   ; star + 0 or 32
        sta rec_off
        rts

; The planes of the next frame's camera, for ahead. They are
; kept for the camera of the frame in front (front_cam,
; fp_cell, fp_pix: star_planes works for the back screen
; too). The same pixel: C = 0, nothing to do; a pixel on (at
; most a pixel a frame): moved (planes_on); else made again
; (star_planes). Then into plane_cell, plane_pix; C = 1.
front_planes:
        lda next                ; next - front_cam
        sec
        sbc front_cam
        tax
        lda next + 1
        sbc front_cam + 1
        bne _anew
        txa
        beq _same
        cmp #1
        bne _anew
        jsr planes_on
        jmp _use
_same:
        clc
        rts
_anew:
        lda next
        sta star_cam
        lda next + 1
        sta star_cam + 1
        jsr star_planes
        jsr keep_planes
_use:
        lda next
        sta front_cam
        lda next + 1
        sta front_cam + 1
        ldx #2
-       lda fp_cell,x
        sta plane_cell,x
        lda fp_pix,x
        sta plane_pix,x
        dex
        bpl -
        sec
        rts

; The planes kept for ahead, from star_planes' (star_cam).
keep_planes:
        lda star_cam
        sta front_cam
        lda star_cam + 1
        sta front_cam + 1
        ldx #2
-       lda plane_cell,x
        sta fp_cell,x
        lda plane_pix,x
        sta fp_pix,x
        dex
        bpl -
        rts

; The kept planes a pixel on: U = (1273 + (camera AND 7) -
; shift) mod 320 goes on by 1 - the change of the shift
; (camera / 8, camera / 4, their sum). With n = the new
; camera AND 7: n = 0, the three a cell back (- 8; plane 2
; a pixel more, - 9); n = 4, plane 0 + 1 (planes 1 and 2:
; their shift + 1 too); else the three + 1.
planes_on:
        lda front_cam
        clc
        adc #1
        and #%00000111
        beq _cell
        cmp #4
        beq _four
        ldx #2                  ; the three + 1
-       jsr _plus
        dex
        bpl -
        rts
_four:
        ldx #0
        jmp _plus
_cell:
        ldx #2                  ; the three a cell back
-       jsr _back
        dex
        bpl -
        dec fp_pix + 2          ; plane 2 a pixel more
        bpl +
        lda #7
        sta fp_pix + 2
        ldx #2
        jmp _back
+       rts
_plus:
        inc fp_pix,x            ; + 1: a pixel, or a cell
        lda fp_pix,x
        cmp #8
        bne +
        lda #0
        sta fp_pix,x
        inc fp_cell,x
        lda fp_cell,x
        cmp #40
        bne +
        lda #0
        sta fp_cell,x
+       rts
_back:
        dec fp_cell,x           ; a cell back, mod 40
        bpl +
        lda #39
        sta fp_cell,x
+       rts

        .cerror STAR_STRIDE != 32, "star_setup: 32"
        .cerror STAR_COUNT > STAR_STRIDE, "star_setup"

; The turn of the swap: the new column into the back screen
; (scroll.asm) and the planes of its stars, for the camera
; of the next swap (the next column's first pixel: speeds
; are at most 1 pixel a frame), kept for stages 4 and 5.
; Also at the level's start (init_level), for the first
; swap.
swap_back:
        jsr new_column
        jsr back_setup
        jsr star_planes         ; (kept for back_top and
        ldx #2                  ; back_bottom)
-       lda plane_cell,x
        sta bp_cell,x
        lda plane_pix,x
        sta bp_pix,x
        dex
        bpl -
        jmp back_done

; Stages 4 (rows 0-4) and 5 (rows 5-9): the stars of the
; back screen, by the planes of swap_back; cells only: a
; fresh screen, none to take away.
back_top:
        jsr back_planes
        jsr star_ring_0
        jmp back_done

back_bottom:
        jsr back_planes
        jsr star_ring_5
back_done:
        lda #0
        sta fresh
        rts

back_planes:
        jsr back_setup          ; the planes of swap_back
        ldx #2
-       lda bp_cell,x
        sta plane_cell,x
        lda bp_pix,x
        sta plane_pix,x
        dex
        bpl -
        rts

; The camera of the swap, the back screen's records (its
; planes: back_top makes them, back_bottom uses them again).
back_setup:
        lda camera + 1          ; (camera / 8 + 1) * 8
        sta star_cam + 1
        lda camera
        and #%11111000
        clc
        adc #8
        sta star_cam
        bcc +
        inc star_cam + 1
+       lda front
        eor #1
        asl a
        asl a
        sta star_page
        lda #1
        sta fresh
        jmp star_offsets

; For each plane U = (1280 - 7 + (camera AND 7) - shift)
; mod 320, so that a row's T is U + its pixel (less 320 if
; over); kept as U / 8 (plane_cell, 0-39) and U AND 7
; (plane_pix). With shift = 8 sc + sp and 1273 = 8 * 159
; + 1: U = 8 (159 - sc) + (1 + (camera AND 7) - sp), the
; second part -6 to 8 (a cell less or more). The camera:
; star_cam; sc and sp from camera / 4 (plane 1), camera / 8
; (plane 0) and their sum (plane 2).
star_planes:
        lda star_cam + 1        ; camera / 4: 11 bits
        sta temp
        lda star_cam
        lsr temp
        ror a
        lsr temp
        ror a
        tax
        and #%00000111
        sta shift + 1           ; sp of plane 1
        txa
        lsr temp                ; camera / 32: sc of plane 1
        ror a
        lsr temp
        ror a
        lsr temp
        ror a
        sta shift
        lsr a                   ; camera / 64: sc of plane 0
        sta shift + 2
        txa                     ; camera / 8 AND 7: sp of
        lsr a                   ; plane 0
        and #%00000111
        sta shift + 3
        lda star_cam
        and #%00000111
        clc
        adc #1
        sta shift + 4           ; 1 + (camera AND 7)
        ldy #1                  ; plane 1
        lda shift
        ldx shift + 1
        jsr _plane
        ldy #0                  ; plane 0
        lda shift + 2
        ldx shift + 3
        jsr _plane
        lda shift + 1           ; plane 2: the sum
        clc
        adc shift + 3
        tax
        and #%00000111
        sta shift + 5
        txa
        cmp #8                  ; C: a carry into sc
        lda shift
        adc shift + 2
        ldx shift + 5
        ldy #2
        .cerror CAMERA_END * 3 / 64 + 1 > 159, "star_planes"
_plane:                         ; A: sc, X: sp, Y: the plane
        sta fine
        lda #159
        sec
        sbc fine
        sta fine                ; 159 - sc
        stx temp
        lda shift + 4
        sec
        sbc temp                ; 1 + (camera AND 7) - sp
        bpl +
        clc                     ; below 0: a cell less
        adc #8
        dec fine
        jmp ++
+       cmp #8
        bcc +
        sbc #8                  ; 8: a cell more
        inc fine
+       sta plane_pix,y
        lda fine
-       cmp #40                 ; mod 40
        bcc +
        sbc #40
        bcs -
+       sta plane_cell,y
        rts

STAR_FONT = CHARSET + STAR_CODE * 8

; The row's pixel in each star character: (U AND 7 + the
; row's pixel) AND 7, U of its plane. Unrolled: the rows'
; planes, pixels and lines are constants (assets.inc).
star_pixels:
        .for p_row in range(10)
        lda plane_pix + ROW_PLANES[p_row]
        clc
        adc #ROW_PIXELS[p_row]
        and #%00000111
        tax
        lda star_bit,x
        sta STAR_FONT + 8 * p_row + ROW_LINES[p_row]
        .endfor
        rts

; Each row's first cell: U / 8 + (U AND 7 + the row's
; pixel) / 8, mod 40; the row's stars put again if it has
; changed (or all, if `fresh`). Unrolled; rows 0-4 and
; 5-9 can be done apart (stages 4 and 5).
ring_rows .macro rows
        .for r_ring in \rows
        lda plane_pix + ROW_PLANES[r_ring]
        clc
        adc #ROW_PIXELS[r_ring]
        cmp #8                  ; C: the next cell
        lda plane_cell + ROW_PLANES[r_ring]
        adc #0
        cmp #40
        bcc +
        sbc #40
+       ldx col_off             ; the screen's record of it
        ldy fresh
        bne +                   ; a fresh screen: put them
        cmp star_col + r_ring,x
        beq ++                  ; the same cells
+       sta star_col + r_ring,x
        sta fine
        lda #r_ring
        sta row
        jsr star_row
+
        .endfor
        .endmacro

star_ring:
        #ring_rows range(5)
star_ring_5:
        #ring_rows range(5, 10)
        rts
star_ring_0:
        #ring_rows range(5)
        rts

; The stars of row `row` into the screen of star_page, from
; cell `fine`: the old ones taken away (not if fresh).
; Their records: star + rec_off.
star_row:
        ldx row
        lda star_sky,x
        sta sky
        txa
        clc
        adc #STAR_CODE
        sta ring_code
        lda star_first + 1,x
        clc
        adc rec_off
        sta last
        lda row_lo,x            ; the row in its screen
        sta dst
        lda row_hi,x
        clc
        adc star_page
        sta dst + 1
        lda star_first,x
        clc
        adc rec_off
        sta star
        tax
        lda fresh
        bne _put
_off:
        ldy star_rec,x          ; take the old ones away
        cpy #$ff
        beq +
        lda sky
        sta (dst),y
+       inx
        cpx last
        bne _off
_put:
        ldx star
_one:
        lda #$ff
        sta star_rec,x
        lda fine                ; its cell: first + its own,
        clc                     ; on the ring of 40
        adc star_cells,x
        cmp #40
        bcc +
        sbc #40
+       cmp #39                 ; column 39: never seen
        bcs _skip
        tay
        lda (dst),y
        cmp sky                 ; only on the blank sky
        bne _skip
        lda ring_code
        sta (dst),y
        tya
        sta star_rec,x
_skip:
        inx
        cpx last
        bne _one
row_done:                       ; the tests look here
        rts

star_bit:
        .byte $80, $40, $20, $10, $08, $04, $02, $01
row_lo:                         ; rows 0-21 of screen A
        .for s_row in range(22)
        .byte <(SCREEN_A + s_row * 40)
        .endfor
row_hi:
        .for s_row in range(22)
        .byte >(SCREEN_A + s_row * 40)
        .endfor
