; Written by game/assets/build_assets.py: do not edit.
; where the streams go (level.asm, load_level)
lz_dst_lo:
        .byte <(SPRITES2), <(LEVEL_W1), <(LEVEL_W2), <(CHARSET)
lz_dst_hi:
        .byte >(SPRITES2), >(LEVEL_W1), >(LEVEL_W2), >(CHARSET)
