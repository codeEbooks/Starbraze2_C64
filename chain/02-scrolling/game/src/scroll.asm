; Horizontal scrolling in one direction, with two screens.
;
; camera is the level's x (screen pixels) at the left edge
; of the playfield, with cam_frac, 256ths of a pixel. Each
; frame it goes on by the speed of the level at that place.
; Its low 3 bits make the near
; layer's fine scroll; camera / 8 is the level's column in
; screen column 0: when it changes, everything moves by a
; column.
;
; The characters for that are ready in the back screen: it
; is made in seven steps, one a frame, never in a frame
; that swaps: stage 0, rows 0-2 copied from the front
; screen one column to the left (without the stars); stage
; 1, rows 3-5 the same; stage 2, rows 6-8; stage 3, rows
; 15-18 and 9; stage 4, the stars of rows 0-4 where they
; will be at the swap; stage 5, those of rows 5-9; stage
; 6, rows 19-21.
; The column that comes in at the right, from the level,
; with its colours, and the stars' planes are made in the
; turn of the swap itself (swap_back), after the colour
; RAM's rows 15-21. At a pixel a frame there are seven
; frames between two swaps, each with a stage; the far layer
; moves with stage 6, and the frame before the swap moves
; the colour RAM. Then it is ready (READY). If it is not
; ready the camera waits at the last pixel of its column.
;
; Rows 0-9 of the next frame are made in the frame before,
; each once the beam has drawn it (ahead, after the turn):
; the stars for the next camera and, if the screens will
; swap, the colour RAM (it is one for both screens: it
; changes in place, only where a row's colour changes
; along the level). Rows 15-21 of the colour RAM change in
; the turn of the swap, before the beam reaches them. Rows
; 10-14 keep their colours all along.
;
; The far layer, rows 11-13 (10 is the same all along),
; moves at half the camera's speed: far_cam = (camera + 1)
; / 2, its own fine scroll. It is shown from screen A
; whichever screen is in front (irq.asm): when far_cam / 8
; changes, rows 11-13 of screen A move by a column in place
; and the new far column comes in at the right. The + 1
; keeps this away from the frames that swap the screens and
; puts it, at a pixel a frame, in the frame before a swap,
; with the back screen's lightest stage (6).

; The camera's next place and what it brings: next,
; next_frac; swap_flag (a new column, the back screen
; ready), or the wait at the last pixel of the column.
; The camera stops at CAMERA_END: there it is the arena.
; Asked a turn early (and at the start): the next turn uses
; it.
camera_plan:
        lda #0
        sta swap_flag
        jsr camera_next
        bcc +
        lda #<CAMERA_END        ; past the end: at the end
        sta next
        lda #>CAMERA_END
        sta next + 1
        lda #0
        sta next_frac
        lda camera              ; there already: the arena
        cmp #<CAMERA_END
        bne +
        lda camera + 1
        cmp #>CAMERA_END
        bne +
        lda #1
        sta arena
        rts
+       lda camera              ; a new column if the fine
        and #%00000111          ; part goes down: 7 -> 0, 1
        sta fine
        lda next
        and #%00000111
        cmp fine
        bcs _done               ; same column
        lda prep_stage          ; back screen ready?
        cmp #READY
        bne _hold
        inc swap_flag           ; yes: show it
_done:
        rts
_hold:
        lda camera              ; no: wait at the last pixel
        ora #%00000111          ; of this column
        sta next
        lda camera + 1
        sta next + 1
        lda #0
        sta next_frac
        rts

; The camera's move for this frame (camera_plan made it in
; the frame before), the scrolls, the far layer's column.
move_camera:
        lda #0
        sta far_flag
        lda next
        sta camera
        lda next + 1
        sta camera + 1
        lda next_frac
        sta cam_frac
        jsr set_scrolls         ; the fine scrolls; A: the
        cmp far_col             ; far layer's column
        beq +
        sta far_col
        inc far_flag
+       rts

; The camera's next place: next, next_frac = camera +
; the speed of the level where the camera is (the last
; entry whose place is reached; speed_ix keeps it). C = 1
; if it is the end of the level.
camera_next:
        ldx speed_ix            ; from the entry found the
_speed:                         ; frame before: the camera
        lda camera              ; only goes on
        cmp speed_at_lo + 1,x
        lda camera + 1
        sbc speed_at_hi + 1,x
        bcc _found              ; camera < next place
        inx
        bne _speed
_found:
        stx speed_ix
        lda speed_lo,x
        sta speed
        lda speed_hi,x
        sta speed + 1
        clc
        lda cam_frac
        adc speed
        sta next_frac
        lda camera
        adc speed + 1
        sta next
        lda camera + 1
        adc #0
        sta next + 1
        lda next                ; C = 1: next >= CAMERA_END
        cmp #<CAMERA_END
        lda next + 1
        sbc #>CAMERA_END
        rts

; The back screen goes in front, from the next frame: the
; top interrupt shows it. Its stars are there (stage 5),
; with their records; rows 0-9 of the colour RAM have
; moved (ahead). A new back screen from the start.
flip_front:
        lda front
        eor #1
        sta front
        tax
        lda d018_values,x
        sta shown_d018
        lda #0
        sta prep_stage
        rts

; The turn of the swap, after the sprites: rows 15-21 of
; the colour RAM, row by row, before the beam reaches them.
colour_bottom:
        #colour_column camera   ; the new column
        lda #15
        sta swap_row
-       jsr colour_next
        lda swap_row
        cmp #22
        bne -
        rts

; After the turn, for the next frame (its camera planned
; in the turn, camera_plan): nothing if its pixel is the
; same as this one's and no swap comes (the stars are
; there already); if the screens will
; swap, the
; colours of rows 0-9, each once the beam has drawn the row
; in this frame (row_after; at once if the HUD has started);
; once it has drawn row 9, the stars for the next camera, in
; the screen the next frame shows (the back one if they will
; swap: its stars are there since stage 5). Nothing before
; the end of the level. The tests look at row_coloured,
; row_done, ahead_done.
ahead:
        lda swap_flag
        sta swap_next
        jsr front_planes        ; the stars' planes for next
        bcs +                   ; (C = 0: the same pixel as
        lda swap_next           ; now: with no swap, the
        beq ahead_done          ; stars are already there)
+       lda front               ; the next frame's screen
        eor swap_next
        asl a
        asl a
        sta star_page
        jsr star_offsets        ; its records
        lda #0
        sta swap_row
        lda swap_next
        beq +
        #colour_column next     ; a swap: the new column
        jmp _row
+       lda #9                  ; no swap: the stars
        sta swap_row
_row:
        ldx swap_row
-       lda frame_flag          ; the HUD has started
        bne _now
        lda frame_count         ; still the frame in which
        cmp turn_count          ; the turn began?
        beq -
        lda $d012               ; the beam past row R?
        cmp row_after,x
        bcc -
_now:
        lda swap_next
        beq ahead_stars
        lda frame_flag          ; the beam past row 9
        bne colour_fast         ; already: the rest at once
        lda $d012
        cmp #COLOUR_LINE
        bcs colour_fast
        jsr colour_next         ; row R's colours
        lda swap_row
        cmp #10
        bne _row
ahead_stars:
        jsr star_pixels         ; the stars, rows 0-9
        jsr star_ring
ahead_done:                     ; the tests look here
        rts

; The colours of rows swap_row-9 one after the
; other, when the beam is past row 9 already (a turn that
; ended late): no waiting, no dispatch.
colour_fast:
        ldx swap_row
        lda fast_lo,x
        sta vector
        lda fast_hi,x
        sta vector + 1
fast_rows:                      ; the tests look here
        jmp (vector)
fast_0:
        jsr colour_r0
        jsr colour_r1
        jsr colour_r2
        jsr colour_r3
        jsr colour_r4
        jsr colour_r5
        jsr colour_r6
        jsr colour_r7
        jsr colour_r8
        jsr colour_r9
        lda #10
        sta swap_row
        jmp ahead_stars
fast_lo:
        .for f_row in range(10)
        .byte <(fast_0 + 3 * f_row)
        .endfor
fast_hi:
        .for f_row in range(10)
        .byte >(fast_0 + 3 * f_row)
        .endfor

row_after:                      ; the line after row R
        .for r_row in range(10)
        .byte 59 + 8 * r_row
        .endfor
        .cerror 59 + 8 * 9 != COLOUR_LINE, "row_after"

; The colours of row swap_row, then swap_row + 1.
colour_next:
        lda swap_row
        jsr colour_row
row_coloured:                   ; the tests look here
        inc swap_row
        rts

d018_values:
        .byte D018_A, D018_B

; One step of the back screen a frame: stages 0-6, then
; READY. The routine: by the front screen and the stage.
prepare_back:
        lda prep_stage
        cmp #READY
        bcs _done
        asl a                   ; 2 bytes an address
        ldx front
        beq +
        adc #2 * READY          ; front B: the second half
+       tax
        lda prep_routines,x
        sta vector
        lda prep_routines + 1,x
        sta vector + 1
        jsr _call
        inc prep_stage
_done:
        rts
_call:
        jmp (vector)

prep_routines:                  ; front A (back B), front B
        .word a_top0, a_top1, a_top2, a_bottom9, back_top
        .word back_bottom, a_bottom1
        .word b_top0, b_top1, b_top2, b_bottom9, back_top
        .word back_bottom, b_bottom1

        .cerror READY != 7, "prep_routines: seven stages"

; The column of the level that comes in, column camera / 8
; + 39, into column 38 of the back screen (swap_back).
new_column:
        lda camera + 1
        sta column + 1
        lda camera
        .rept 3
        lsr column + 1
        ror a
        .endrept
        clc
        adc #39
        sta column
        bcc +
        inc column + 1
+       jsr near_column
        ldy #38
        lda front
        bne +
        jmp put_near_b          ; front A: back B
+       jmp put_near_a

; Stages 0-2 copied the stars of the front screen too:
; where a star was, in column C of row R, the back screen
; gets the row's blank sky in column C - 1. Rows A to X - 1,
; the front's records.
star_fixups:
        sta row
        stx row_end
        lda front               ; its records: star + 0 / 32
        lsr a
        ror a
        lsr a
        lsr a
        sta rec_off
        lda front               ; the back screen: + 4 pages
        eor #1                  ; if B
        asl a
        asl a
        sta back_page
_row:
        ldx row
        lda row_lo,x
        sta dst
        lda row_hi,x
        clc
        adc back_page
        sta dst + 1
        lda star_sky,x
        sta sky
        lda star_first + 1,x
        clc
        adc rec_off
        sta last
        lda star_first,x
        clc
        adc rec_off
        tax
        cpx last
        beq _next
_star:
        ldy star_rec,x          ; its cell, $ff: none
        beq _skip               ; column 0: not copied
        cpy #$ff
        beq _skip
        dey                     ; one column to the left
        lda sky
        sta (dst),y
_skip:
        inx
        cpx last
        bne _star
_next:
        inc row
        lda row
        cmp row_end
        bne _row
        rts

back_hi:
        .byte >SCREEN_B, >SCREEN_A

; The far layer one column on: rows 11-13 of screen A, in
; place, and the new far column at column 38. The far rows
; are always shown from screen A (the interrupt of row 10
; points the VIC-II at it, that of row 14 back at the
; screen in front): screen B's rows 11-13 are never shown,
; and nothing moves there.
far_step:
        lda far_col
        clc
        adc #38
        jsr far_column          ; the new column: edge_far
        jsr far_moves_a
        ldy #38
        jsr put_far_a
far_done:                       ; the tests look here
        rts

; The routines that move rows of characters by a column
; to the left: cell X takes cell X + 1, X from 0 to 37.
; Each is unrolled on its rows: 9 or 10 cycles a cell. The
; three of rows 0-9 then take the stars out of the copy,
; from row \fix to row \upto - 1.
move_left .macro from, to, rows, fix=-1, upto=0
        ldx #0
-
        .for r in \rows
        lda \from + r * 40 + 1,x
        sta \to + r * 40,x
        .endfor
        inx
        cpx #38
        bne -
        .if \fix >= 0
        lda #\fix
        ldx #\upto
        jmp star_fixups
        .else
        rts
        .endif
        .endmacro

; front A, back B; then front B, back A. (Rows 15-21,
; stages 3 and 6, and stage 3's row 9: fast.asm, unrolled.)
a_top0    #move_left SCREEN_A, SCREEN_B, range(3), 0, 3
a_top1    #move_left SCREEN_A, SCREEN_B, range(3, 6), 3, 6
a_top2    #move_left SCREEN_A, SCREEN_B, range(6, 9), 6, 9
b_top0    #move_left SCREEN_B, SCREEN_A, range(3), 0, 3
b_top1    #move_left SCREEN_B, SCREEN_A, range(3, 6), 3, 6
b_top2    #move_left SCREEN_B, SCREEN_A, range(6, 9), 6, 9

; The colour RAM moves with the screens only where a row's
; colour changes along the level. At a swap, column X of
; row R takes the colour of the level's column cb_col + X:
; it is new only where a colour starts in those columns
; (bound_*, from build_assets.py: each row's columns where a
; colour starts, and the colour). Row R's routine writes
; those in cb_col to cb_col + 38; the first one still in
; view is kept (cb_first + the row's slot): at a swap at
; most one leaves, at cb_col - 1.
colour_bounds .macro row, slot
        ldy cb_first + \slot    ; has the first one left?
        lda bound_lo + BOUND_AT_\row,y
        cmp cb_col
        lda bound_hi + BOUND_AT_\row,y
        sbc cb_col + 1
        bcs _each
        iny                     ; yes: the next one
        sty cb_first + \slot
_each:
        lda bound_lo + BOUND_AT_\row,y
        sec                     ; X: its column on the
        sbc cb_col              ; screen
        tax
        lda bound_hi + BOUND_AT_\row,y
        sbc cb_col + 1
        bne _done               ; past column 38, or the
        cpx #VIEW               ; row's end ($ffff)
        bcs _done
_next:
        lda bound_colour + BOUND_AT_\row,y
        sta COLOURS + \row * 40,x
        txa                     ; the next: by its step
        clc
        adc bound_step + BOUND_AT_\row,y
        bcs _done
        tax
        iny
        cpx #VIEW
        bcc _next
_done:
        rts
        .endmacro

VIEW = 39                       ; colour RAM columns 0-38

; cb_col: the column of a camera (\from, two bytes) / 8.
colour_column .macro from
        lda \from + 1
        sta cb_col + 1
        lda \from
        .rept 3
        lsr cb_col + 1
        ror a
        .endrept
        sta cb_col
        .endmacro

; Row A of the colour RAM for the column cb_col.
colour_row:
        asl a
        tax
        lda colour_rows,x
        sta vector
        lda colour_rows + 1,x
        sta vector + 1
        jmp (vector)

colour_rows:                    ; rows 0-9, 15-21
        .word colour_r0, colour_r1, colour_r2, colour_r3
        .word colour_r4, colour_r5, colour_r6, colour_r7
        .word colour_r8, colour_r9, 0, 0, 0, 0, 0
        .word colour_r15, colour_r16, colour_r17
        .word colour_r18, colour_r19, colour_r20
        .word colour_r21

colour_r0       #colour_bounds 0, 0
colour_r1       #colour_bounds 1, 1
colour_r2       #colour_bounds 2, 2
colour_r3       #colour_bounds 3, 3
colour_r4       #colour_bounds 4, 4
colour_r5       #colour_bounds 5, 5
colour_r6       #colour_bounds 6, 6
colour_r7       #colour_bounds 7, 7
colour_r8       #colour_bounds 8, 8
colour_r9       #colour_bounds 9, 9
colour_r15      #colour_bounds 15, 10
colour_r16      #colour_bounds 16, 11
colour_r17      #colour_bounds 17, 12
colour_r18      #colour_bounds 18, 13
colour_r19      #colour_bounds 19, 14
colour_r20      #colour_bounds 20, 15
colour_r21      #colour_bounds 21, 16
COLOUR_SLOTS = 17

; The far layer's rows 11-13, in screen A: fast.asm.
