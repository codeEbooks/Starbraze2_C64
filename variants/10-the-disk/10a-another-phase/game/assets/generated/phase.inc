; Written by game/assets/build_assets.py: do not edit.

FILE_COUNT = 5
LEVEL_FILES = [1, 1, 2, 3, 4, 5, 5]
FILE_PHASES = [1, 2, 2, 3, 3]
PH_MARK_0 = $53
PH_MARK_1 = $42
PH_CELLS = 20
PH_BAR = SCREEN_A + 530
PH_BAR_COLOURS = COLOURS + 530
PH_BAR_COLOUR = 5
PH_EMPTY = 40
PH_FULL = 39
PH_WAIT = 100
PH_NAME_LEN = 10
ph_words_1:
        .byte 7, 80, 1, 3, 26, 18, 11, 29, 15, 0, 2, 10
        .byte 159, 1, 7, 30, 18, 15, 0, 26, 22, 11, 24, 15
        .byte 30, 0
ph_words_2:
        .byte 7, 80, 1, 3, 26, 18, 11, 29, 15, 0, 3, 13
        .byte 157, 1, 7, 30, 18, 15, 0, 17, 28, 11, 32, 15
        .byte 35, 11, 28, 14, 0
ph_words_3:
        .byte 7, 80, 1, 3, 26, 18, 11, 29, 15, 0, 4, 17
        .byte 155, 1, 7, 30, 18, 15, 0, 29, 26, 11, 13, 15
        .byte 0, 29, 30, 11, 30, 19, 25, 24, 0
ph_loading:
        .byte 15, 140, 2, 1, 0, 0, 0, 0, 22, 25, 11, 14
        .byte 19, 24, 17, 0, 0, 0, 0, 0
ph_insert:
        .byte 15, 140, 2, 2, 19, 24, 29, 15, 28, 30, 0, 30
        .byte 18, 15, 0, 14, 19, 29, 21, 0
file_phase:
        .byte FILE_PHASES
ph_words_lo:
        .byte <ph_words_1, <ph_words_2, <ph_words_3
ph_words_hi:
        .byte >ph_words_1, >ph_words_2, >ph_words_3
