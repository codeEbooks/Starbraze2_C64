; Written by game/assets/build_assets.py: do not edit.

; the copy's runs: by phase, from (the base's; the mouth's, the hatch's)
run_src_lo:
        .byte <(body_data + 0), <(body_data + 160), <(body_data + 256), <(body_data + 352), <(body_data + 384)
        .byte <(body_data + 480), <(body_data + 640), <(body_data + 736), <(body_data + 832), <(body_data + 864)
        .byte <(body_data + 960), <(body_data + 1120), <(body_data + 1216), <(body_data + 1312), <(body_data + 1344)
        .byte <(body_data + 1440), <(body_data + 1600), <(body_data + 1696), <(body_data + 1792), <(body_data + 1824)
run_src_hi:
        .byte >(body_data + 0), >(body_data + 160), >(body_data + 256), >(body_data + 352), >(body_data + 384)
        .byte >(body_data + 480), >(body_data + 640), >(body_data + 736), >(body_data + 832), >(body_data + 864)
        .byte >(body_data + 960), >(body_data + 1120), >(body_data + 1216), >(body_data + 1312), >(body_data + 1344)
        .byte >(body_data + 1440), >(body_data + 1600), >(body_data + 1696), >(body_data + 1792), >(body_data + 1824)
mouth_src_lo:
        .byte <(mouth_data + 0), <(mouth_data + 160), <(mouth_data + 320), <(mouth_data + 480)
mouth_src_hi:
        .byte >(mouth_data + 0), >(mouth_data + 160), >(mouth_data + 320), >(mouth_data + 480)
hatch_src_lo:
        .byte <(hatch_data + 0), <(hatch_data + 96), <(hatch_data + 192), <(hatch_data + 288)
hatch_src_hi:
        .byte >(hatch_data + 0), >(hatch_data + 96), >(hatch_data + 192), >(hatch_data + 288)
; by set: where each run goes (the charset), its bytes
run_dst_lo:
        .byte <(CHARSET + 192), <(CHARSET + 352), <(CHARSET + 1744), <(CHARSET + 1840), <(CHARSET + 1872)
        .byte <(CHARSET + 872), <(CHARSET + 1032), <(CHARSET + 1176), <(CHARSET + 1272), <(CHARSET + 576)
run_dst_hi:
        .byte >(CHARSET + 192), >(CHARSET + 352), >(CHARSET + 1744), >(CHARSET + 1840), >(CHARSET + 1872)
        .byte >(CHARSET + 872), >(CHARSET + 1032), >(CHARSET + 1176), >(CHARSET + 1272), >(CHARSET + 576)
run_bytes:
        .byte 160, 96, 96, 32, 96
; each set's columns: the first of their four codes
set_code:
        .byte 24, 28, 32, 36, 40, 44, 48, 52, 218, 222, 226, 230
        .byte 234, 238, 242, 109, 113, 117, 121, 125, 129, 133, 137, 147
        .byte 151, 155, 159, 72, 76, 80
; the letters' glyphs in the HUD's set, their codes
letter_glyph:
        .byte 29, 30, 11, 17, 15, 13, 22, 28, 18, 19, 14, 12
        .byte 25, 24, 31
letter_code:
        .byte 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102
        .byte 103, 104, 84
; STAGE CLEAR's cells (screen offset), codes, line (0 the first)
text_lo:
        .byte 213, 214, 215, 216, 217, 219, 220, 221, 222, 223, 77, 78
        .byte 79, 80, 81, 82, 84, 85, 86, 87, 88
text_hi:
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1
        .byte 1, 1, 1, 1, 1, 1, 1, 1, 1
text_code:
        .byte 91, 92, 93, 94, 95, 96, 97, 95, 93, 98, 91, 99
        .byte 100, 95, 97, 101, 102, 103, 104, 84, 91
text_line:
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1
        .byte 1, 1, 1, 1, 1, 1, 1, 1, 1
; the first line's colour, by anim / 4 AND 3
text_cycle:
        .byte 1, 7, 1, 3
; the bar's steps (0-64) by the life left
bar_of_life:
        .byte 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3
        .byte 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7
        .byte 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10
        .byte 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 14, 14
        .byte 14, 15, 15, 15, 15, 16, 16, 16, 17, 17, 17, 17
        .byte 18, 18, 18, 19, 19, 19, 20, 20, 20, 20, 21, 21
        .byte 21, 22, 22, 22, 23, 23, 23, 23, 24, 24, 24, 25
        .byte 25, 25, 25, 26, 26, 26, 27, 27, 27, 28, 28, 28
        .byte 28, 29, 29, 29, 30, 30, 30, 31, 31, 31, 31, 32
        .byte 32, 32, 33, 33, 33, 33, 34, 34, 34, 35, 35, 35
        .byte 36, 36, 36, 36, 37, 37, 37, 38, 38, 38, 39, 39
        .byte 39, 39, 40, 40, 40, 41, 41, 41, 41, 42, 42, 42
        .byte 43, 43, 43, 44, 44, 44, 44, 45, 45, 45, 46, 46
        .byte 46, 47, 47, 47, 47, 48, 48, 48, 49, 49, 49, 49
        .byte 50, 50, 50, 51, 51, 51, 52, 52, 52, 52, 53, 53
        .byte 53, 54, 54, 54, 55, 55, 55, 55, 56, 56, 56, 57
        .byte 57, 57, 57, 58, 58, 58, 59, 59, 59, 60, 60, 60
        .byte 60, 61, 61, 61, 62, 62, 62, 63, 63, 63, 63, 64
        .byte 64
; the patrols, the cannons' then the core's: where to, speed (256ths), frames to wait there
patrol_to:
        .byte 56, 92, 32, 92
patrol_speed:
        .byte 64, 64, 128, 128
patrol_wait:
        .byte 60, 90, 30, 50
; the chain: the fireball's x register - 2 x the body's x, its line; then the SHIELD CORE's: - CB_PART_X
chain_dx:
        .byte 75, 35, 107, 55, 91, 27, 119, 67, 99, 47, 24, 8
        .byte 40, 16, 34, 4, 44, 22, 30, 12
chain_y:
        .byte 114, 122, 120, 130, 132, 116, 126, 122, 114, 136, 78, 68
        .byte 84, 90, 64, 80, 74, 94, 60, 84
; rows 15-18's colours (multicolour): the hull, white, the wreck
hull_colour:
        .byte 10, 10, 10, 9, 9, 9, 9, 9, 8, 8, 8, 8
