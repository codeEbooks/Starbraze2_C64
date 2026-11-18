; Written by game/assets/build_assets.py: do not edit.
; the escape's tables (escape.py, sprites.py)
; TIME in the HUD (its digits after it)
es_time_text:
        .byte 30, 19, 23, 15, 0, 0, 0, 0
; the falling pieces' pictures
es_rubble:
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 85, 0
        .byte 5, 170, 80, 26, 186, 164, 26, 250, 169, 107, 170, 105
        .byte 106, 166, 164, 105, 170, 169, 26, 170, 148, 22, 166, 164
        .byte 5, 170, 80, 0, 84, 0, 0, 0, 0, 0, 0, 0
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        .byte 0, 0, 21, 0, 1, 106, 84, 6, 170, 185, 26, 106
        .byte 249, 26, 170, 233, 106, 154, 168, 106, 170, 100, 107, 170
        .byte 164, 27, 234, 80, 5, 170, 80, 0, 85, 0, 0, 0
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        .byte 0, 0, 0, 0, 0, 0, 0, 0
; the victory's texts: place, colour, count, codes; 0, 0 the end
es_texts:
        .byte 168, 64, 1, 24, 30, 18, 15, 0, 29, 30, 11, 30
        .byte 19, 25, 24, 0, 19, 29, 0, 14, 15, 29, 30, 28
        .byte 25, 35, 15, 14, 252, 64, 7, 16, 23, 19, 29, 29
        .byte 19, 25, 24, 0, 13, 25, 23, 26, 22, 15, 30, 15
        .byte 97, 66, 3, 22, 30, 19, 23, 15, 0, 12, 25, 24
        .byte 31, 29, 0, 0, 0, 1, 1, 0, 34, 0, 2, 1
        .byte 1, 1, 177, 66, 3, 22, 29, 18, 19, 15, 22, 14
        .byte 0, 12, 25, 24, 31, 29, 0, 0, 1, 0, 34, 0
        .byte 2, 1, 1, 1, 0, 0
; the fireballs' lines (x register's)
es_boom_y:
        .byte 30, 100, 60, 140, 20, 120, 80, 150
; the fireballs' steps back from the hull's end
es_boom_dx:
        .byte 0, 20, 40, 8, 56, 30, 12, 48
