; Written by game/assets/music.py from station_theme.py:
; do not edit. Phase 3's song 1 (the station's theme), in
; the station's module from P3_MUSIC.

        .cerror * != P3_MUSIC, "P3_MUSIC"
; pattern 15: o_lead_intro
p3_pat_15:
        .byte $bf, $60, $ff
        .cerror p3_pat_15 != $e010
; pattern 16: o_lead_a
p3_pat_16:
        .byte $c0, $82, $40, $43, $81, $47, $82, $45
        .byte $43, $81, $42, $82, $43, $40, $81, $3c
        .byte $87, $40, $82, $42, $45, $81, $4a, $82
        .byte $48, $47, $81, $45, $85, $47, $81, $45
        .byte $83, $42, $3f, $82, $40, $43, $81, $47
        .byte $82, $4c, $4a, $81, $47, $82, $48, $47
        .byte $81, $43, $87, $40, $82, $45, $48, $81
        .byte $4c, $82, $4a, $48, $81, $45, $8b, $47
        .byte $83, $60, $ff
        .cerror p3_pat_16 != $e013
; pattern 17: o_lead_b
p3_pat_17:
        .byte $c1, $87, $4c, $83, $4f, $4c, $85, $4e
        .byte $81, $4c, $83, $4a, $45, $85, $47, $81
        .byte $48, $83, $47, $43, $8b, $40, $83, $60
        .byte $48, $4c, $4f, $4c, $4e, $51, $81, $4e
        .byte $4c, $83, $4a, $85, $4b, $81, $4e, $87
        .byte $53, $83, $51, $81, $4e, $4b, $83, $47
        .byte $45, $ff
        .cerror p3_pat_17 != $e056
; pattern 18: o_lead_c
p3_pat_18:
        .byte $cb, $87, $39, $83, $3c, $40, $87, $43
        .byte $83, $40, $3c, $87, $3b, $83, $40, $43
        .byte $87, $42, $83, $3e, $39, $85, $3c, $81
        .byte $40, $83, $45, $48, $85, $4c, $81, $48
        .byte $83, $43, $40, $85, $3f, $81, $42, $83
        .byte $47, $4b, $87, $4e, $83, $4b, $47, $ff
        .cerror p3_pat_18 != $e088
; pattern 19: o_drive
p3_pat_19:
        .byte $c2, $81, $1c, $c4, $80, $28, $1c, $81
        .byte $23, $28, $c3, $1c, $c4, $80, $28, $1c
        .byte $81, $23, $23, $ff
        .cerror p3_pat_19 != $e0b8
; pattern 20: o_turn
p3_pat_20:
        .byte $c2, $81, $1c, $c4, $80, $28, $1c, $81
        .byte $23, $28, $c3, $1c, $1c, $1c, $1c, $ff
        .cerror p3_pat_20 != $e0cc
; pattern 21: o_half
p3_pat_21:
        .byte $c2, $83, $1c, $c4, $23, $c3, $1c, $c4
        .byte $23, $ff
        .cerror p3_pat_21 != $e0dc
; pattern 22: o_minor
p3_pat_22:
        .byte $c5, $81, $34, $80, $60, $81, $34, $80
        .byte $60, $81, $34, $60, $34, $60, $34, $ff
        .cerror p3_pat_22 != $e0e6
; pattern 23: o_major
p3_pat_23:
        .byte $c6, $81, $34, $80, $60, $81, $34, $80
        .byte $60, $81, $34, $60, $34, $60, $34, $ff
        .cerror p3_pat_23 != $e0f6
; pattern 24: o_dom7
p3_pat_24:
        .byte $c7, $81, $34, $80, $60, $81, $34, $80
        .byte $60, $81, $34, $60, $34, $60, $34, $ff
        .cerror p3_pat_24 != $e106
p3_order_3:
        .byte $0f, $00, $10, $00, $11, $00, $12, $00
        .byte $fe, $01
        .cerror p3_order_3 != $e116
p3_order_4:
        .byte $13, $00, $13, $00, $13, $fc, $14, $fb
        .byte $13, $00, $13, $fc, $13, $fe, $13, $fb
        .byte $13, $00, $13, $fc, $13, $05, $14, $fb
        .byte $13, $fc, $13, $fe, $13, $00, $13, $00
        .byte $13, $fc, $13, $fe, $13, $fb, $14, $fb
        .byte $15, $05, $15, $fc, $15, $00, $15, $fe
        .byte $13, $05, $13, $fc, $13, $fb, $14, $fb
        .byte $fe, $04
        .cerror p3_order_4 != $e120
p3_order_5:
        .byte $16, $00, $16, $00, $17, $fc, $18, $fb
        .byte $16, $00, $17, $fc, $17, $fe, $18, $fb
        .byte $16, $00, $17, $fc, $16, $05, $18, $fb
        .byte $17, $fc, $17, $fe, $16, $00, $16, $00
        .byte $17, $fc, $17, $fe, $17, $fb, $18, $fb
        .byte $16, $05, $17, $fc, $16, $00, $17, $fe
        .byte $16, $05, $17, $fc, $17, $fb, $18, $fb
        .byte $fe, $04
        .cerror p3_order_5 != $e15a
P3_MUSIC_END:
