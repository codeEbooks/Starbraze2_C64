; For the frame's time: routines written out in full (no
; loop), from AUDIO, where there is room.

; Rows \rows of screen \from one column to the left into
; screen \to: columns 1-38 into 0-37, unrolled.
move_left_u .macro from, to, rows
        .for u_col in range(38)
        .for u_row in \rows
        lda \from + u_row * 40 + u_col + 1
        sta \to + u_row * 40 + u_col
        .endfor
        .endfor
        rts
        .endmacro

; The far layer's rows 11-13, in screen A (far_step).
far_moves_a #move_left_u SCREEN_A, SCREEN_A, range(11, 14)
; Stages 3 and 6 of the back screen, rows 15-18 and 19-21
; (prepare_back): front A, back B; front B, back A.
a_bottom0 #move_left_u SCREEN_A, SCREEN_B, range(15, 19)
b_bottom0 #move_left_u SCREEN_B, SCREEN_A, range(15, 19)
; Stage 6, rows 19-21.
a_bottom1 #move_left_u SCREEN_A, SCREEN_B, range(19, 22)
b_bottom1 #move_left_u SCREEN_B, SCREEN_A, range(19, 22)
; Stage 3 is rows 15-18 and row 9 (with its stars taken out
; of the copy: scroll.asm, move_left).
a_bottom9:
        jsr a_bottom0
a_row9    #move_left SCREEN_A, SCREEN_B, range(9, 10), 9, 10
b_bottom9:
        jsr b_bottom0
b_row9    #move_left SCREEN_B, SCREEN_A, range(9, 10), 9, 10
