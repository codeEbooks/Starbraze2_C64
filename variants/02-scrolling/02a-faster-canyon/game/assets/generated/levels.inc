; Written by game/assets/build_assets.py: do not edit.

LEVEL_W1_SIZE = 1568
bound_lo = LEVEL_W1 + 0
bound_hi = LEVEL_W1 + 238
bound_colour = LEVEL_W1 + 476
bound_step = LEVEL_W1 + 714
speed_at_lo = LEVEL_W1 + 952
speed_at_hi = LEVEL_W1 + 961
speed_lo = LEVEL_W1 + 970
speed_hi = LEVEL_W1 + 978
wave_col_lo = LEVEL_W1 + 986
wave_col_hi = LEVEL_W1 + 1034
wave_path = LEVEL_W1 + 1082
wave_kind = LEVEL_W1 + 1130
wave_count = LEVEL_W1 + 1178
wave_spacing = LEVEL_W1 + 1226
wave_x_lo = LEVEL_W1 + 1274
wave_x_hi = LEVEL_W1 + 1322
wave_y = LEVEL_W1 + 1370
wave_dy = LEVEL_W1 + 1418
wave_cap = LEVEL_W1 + 1466
level_d021 = LEVEL_W1 + 1514
level_d022 = LEVEL_W1 + 1515
level_d023 = LEVEL_W1 + 1516
level_far_10 = LEVEL_W1 + 1517
level_far_11 = LEVEL_W1 + 1518
level_far_12 = LEVEL_W1 + 1519
level_far_13 = LEVEL_W1 + 1520
level_decor = LEVEL_W1 + 1521
level_boss = LEVEL_W1 + 1522
beam_down = LEVEL_W1 + 1523
beam_up = LEVEL_W1 + 1524
beam_module = LEVEL_W1 + 1525
beam_bytes = LEVEL_W1 + 1526
start_first = LEVEL_W1 + 1550
LEVEL_W2_SIZE = 3290
near_map = LEVEL_W2 + 0
far_map = LEVEL_W2 + 1800
metatiles = LEVEL_W2 + 2022
floor_lo = LEVEL_W2 + 2890
floor_hi = LEVEL_W2 + 3146

STORE = $d000
STORE_SIZE = 6474
STORE_ROOM = 12282
LEVEL_COUNT = 7
METATILE_COUNT = 217
BEAM_CYCLE = 128
BEAM_DOWN_DIM = 0
BEAM_DOWN_ON = 16
BEAM_UP_DIM = 64
BEAM_UP_ON = 80
BOUND_AT_0 = 0
BOUND_AT_1 = 23
BOUND_AT_2 = 38
BOUND_AT_3 = 61
BOUND_AT_4 = 86
BOUND_AT_5 = 113
BOUND_AT_6 = 140
BOUND_AT_7 = 157
BOUND_AT_8 = 172
BOUND_AT_9 = 181
BOUND_AT_15 = 194
BOUND_AT_16 = 202
BOUND_AT_17 = 211
BOUND_AT_18 = 218
BOUND_AT_19 = 227
BOUND_AT_20 = 231
BOUND_AT_21 = 234
BOUND_TOTAL = 238
BOUND_END = 237
BAR_TOP = 30
BAR_LOW = 45
LEVEL_SONGS = [0, 0, 1, 1, 1, 1, 1]
sphere_data = $e7ea
cosine = $e90a
STAGE_LEN_0 = 4096
STAGE_AT_0 = STORE + 0
STAGE_LEN_1 = 2048
STAGE_AT_1 = STORE + 4096
STAGE_LEN_2 = 330
STAGE_AT_2 = STORE + 6144
STAGE_LEN_3 = 0
STAGE_AT_3 = STORE + 6474
STAGE_LEN_4 = 0
STAGE_AT_4 = STORE + 6474
STAGE_OFFS = [0, 4096, 6144, 6474, 6474]
STAGE_LENS = [4096, 2048, 330, 0, 0]

; the packed streams: by level, its characters, LEVEL_W2, LEVEL_W1, its pictures; where they are in the store, where they go, where they end
lz_src_lo:
        .byte <(STORE + 0), <(STORE + 1069), <(STORE + 2157), <(STORE + 2911), <(STORE + 2911), <(STORE + 3926), <(STORE + 5122), <(STORE + 5788), <(STORE + 0), <(STORE + 1082), <(STORE + 2434), <(STORE + 3292), <(STORE + 0), <(STORE + 1028), <(STORE + 2060), <(STORE + 2693), <(STORE + 0), <(STORE + 380), <(STORE + 1116), <(STORE + 1520), <(STORE + 0), <(STORE + 465), <(STORE + 1061), <(STORE + 1466), <(STORE + 1780), <(STORE + 2051), <(STORE + 2645), <(STORE + 1466)
lz_src_hi:
        .byte >(STORE + 0), >(STORE + 1069), >(STORE + 2157), >(STORE + 2911), >(STORE + 2911), >(STORE + 3926), >(STORE + 5122), >(STORE + 5788), >(STORE + 0), >(STORE + 1082), >(STORE + 2434), >(STORE + 3292), >(STORE + 0), >(STORE + 1028), >(STORE + 2060), >(STORE + 2693), >(STORE + 0), >(STORE + 380), >(STORE + 1116), >(STORE + 1520), >(STORE + 0), >(STORE + 465), >(STORE + 1061), >(STORE + 1466), >(STORE + 1780), >(STORE + 2051), >(STORE + 2645), >(STORE + 1466)
lz_end_lo:
        .byte <(CHARSET + 2048), <(LEVEL_W2 + 3290), <(LEVEL_W1 + 1568), <(SPRITES2 + 0), <(CHARSET + 2048), <(LEVEL_W2 + 3290), <(LEVEL_W1 + 1568), <(SPRITES2 + 1024), <(CHARSET + 2048), <(LEVEL_W2 + 3290), <(LEVEL_W1 + 1568), <(SPRITES2 + 1024), <(CHARSET + 2048), <(LEVEL_W2 + 3290), <(LEVEL_W1 + 1568), <(SPRITES2 + 1024), <(CHARSET + 2048), <(LEVEL_W2 + 3290), <(LEVEL_W1 + 1568), <(SPRITES2 + 832), <(CHARSET + 2048), <(LEVEL_W2 + 3290), <(LEVEL_W1 + 1568), <(SPRITES2 + 1024), <(CHARSET + 2048), <(LEVEL_W2 + 3290), <(LEVEL_W1 + 1568), <(SPRITES2 + 1024)
lz_end_hi:
        .byte >(CHARSET + 2048), >(LEVEL_W2 + 3290), >(LEVEL_W1 + 1568), >(SPRITES2 + 0), >(CHARSET + 2048), >(LEVEL_W2 + 3290), >(LEVEL_W1 + 1568), >(SPRITES2 + 1024), >(CHARSET + 2048), >(LEVEL_W2 + 3290), >(LEVEL_W1 + 1568), >(SPRITES2 + 1024), >(CHARSET + 2048), >(LEVEL_W2 + 3290), >(LEVEL_W1 + 1568), >(SPRITES2 + 1024), >(CHARSET + 2048), >(LEVEL_W2 + 3290), >(LEVEL_W1 + 1568), >(SPRITES2 + 832), >(CHARSET + 2048), >(LEVEL_W2 + 3290), >(LEVEL_W1 + 1568), >(SPRITES2 + 1024), >(CHARSET + 2048), >(LEVEL_W2 + 3290), >(LEVEL_W1 + 1568), >(SPRITES2 + 1024)
