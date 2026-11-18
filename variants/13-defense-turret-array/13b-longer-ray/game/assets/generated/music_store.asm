; Written by game/assets/music.py: do not edit. The songs
; in phase 1's store, at MUSIC_AT: THEME, TITLE.

; pattern 0: lead_intro
pat_0:
        .byte $bf, $60, $ff
; pattern 1: lead_a
pat_1:
        .byte $c0, $81, $39, $3e, $41, $85, $45, $81
        .byte $43, $41, $83, $43, $81, $41, $3e, $83
        .byte $3a, $3e, $81, $3c, $40, $43, $85, $48
        .byte $81, $46, $45, $83, $45, $81, $43, $41
        .byte $83, $40, $3d, $81, $3e, $41, $45, $85
        .byte $4a, $81, $48, $45, $83, $46, $81, $45
        .byte $43, $83, $41, $3e, $81, $43, $46, $83
        .byte $4a, $81, $48, $46, $83, $45, $81, $40
        .byte $41, $43, $40, $83, $3d, $39, $ff
; pattern 2: lead_b
pat_2:
        .byte $c1, $87, $48, $83, $45, $41, $85, $43
        .byte $81, $45, $83, $43, $40, $85, $41, $81
        .byte $43, $83, $45, $3e, $41, $81, $43, $41
        .byte $83, $3e, $41, $81, $45, $48, $87, $4d
        .byte $81, $4c, $48, $83, $4a, $81, $48, $46
        .byte $83, $43, $40, $46, $81, $45, $43, $83
        .byte $4a, $46, $87, $45, $83, $40, $3d, $ff
; pattern 3: lead_a2
pat_3:
        .byte $c0, $81, $39, $3e, $41, $85, $45, $81
        .byte $43, $41, $83, $43, $81, $41, $3e, $83
        .byte $3a, $3e, $81, $3c, $40, $43, $85, $48
        .byte $81, $46, $45, $83, $45, $81, $43, $41
        .byte $83, $40, $3d, $81, $3e, $41, $45, $85
        .byte $4a, $81, $48, $45, $83, $46, $81, $45
        .byte $43, $83, $41, $3e, $81, $40, $41, $43
        .byte $45, $83, $49, $4c, $8b, $4a, $83, $60
        .byte $ff
; pattern 4: lead_c
pat_4:
        .byte $c0, $83, $3e, $43, $85, $46, $81, $45
        .byte $83, $45, $41, $87, $3e, $83, $3e, $41
        .byte $85, $46, $81, $48, $83, $48, $45, $87
        .byte $41, $81, $43, $45, $83, $46, $4a, $4f
        .byte $4d, $81, $4c, $4a, $87, $45, $83, $43
        .byte $46, $85, $4b, $81, $4a, $83, $49, $4c
        .byte $45, $81, $43, $40, $ff
; pattern 5: drive
pat_5:
        .byte $c2, $81, $1a, $c4, $26, $c3, $1a, $c4
        .byte $26, $c2, $1a, $c4, $26, $c3, $1a, $c4
        .byte $26, $ff
; pattern 6: fill
pat_6:
        .byte $c2, $81, $1a, $c4, $26, $c3, $1a, $c4
        .byte $26, $c3, $80, $1a, $1a, $c4, $81, $26
        .byte $c3, $80, $1a, $1a, $1a, $1a, $ff
; pattern 7: half
pat_7:
        .byte $c2, $83, $1a, $c4, $26, $c3, $1a, $c4
        .byte $26, $ff
; pattern 8: rest_bar
pat_8:
        .byte $8f, $60, $ff
; pattern 9: minor
pat_9:
        .byte $c5, $81, $32, $32, $32, $32, $32, $32
        .byte $32, $32, $ff
; pattern 10: major
pat_10:
        .byte $c6, $81, $32, $32, $32, $32, $32, $32
        .byte $32, $32, $ff
; pattern 11: dom7
pat_11:
        .byte $c7, $81, $32, $32, $32, $32, $32, $32
        .byte $32, $32, $ff
; pattern 12: pad_minor
pat_12:
        .byte $c8, $8f, $32, $ff
; pattern 13: pad_major
pat_13:
        .byte $c9, $8f, $32, $ff
; pattern 14: pad_dom7
pat_14:
        .byte $ca, $8f, $32, $ff
order_0:
        .byte $00, $00, $01, $00, $02, $00, $03, $00
        .byte $04, $00, $fe, $01
order_1:
        .byte $05, $00, $05, $00, $05, $fc, $06, $fb
        .byte $05, $00, $05, $fc, $05, $fe, $05, $fb
        .byte $05, $00, $05, $fc, $05, $f9, $06, $fb
        .byte $05, $03, $05, $fe, $05, $00, $05, $fc
        .byte $05, $03, $05, $fe, $05, $f9, $06, $fb
        .byte $05, $00, $05, $fc, $05, $fe, $05, $fb
        .byte $05, $00, $05, $fc, $05, $fb, $06, $00
        .byte $07, $f9, $07, $00, $07, $fc, $07, $03
        .byte $05, $f9, $05, $00, $05, $01, $06, $fb
        .byte $fe, $04
order_2:
        .byte $08, $00, $08, $00, $0a, $fc, $0a, $fb
        .byte $09, $00, $0a, $fc, $0a, $fe, $0b, $fb
        .byte $09, $00, $0a, $fc, $09, $f9, $0b, $fb
        .byte $0d, $03, $0d, $fe, $0c, $00, $0d, $fc
        .byte $0d, $03, $0d, $fe, $0c, $f9, $0d, $fb
        .byte $09, $00, $0a, $fc, $0a, $fe, $0b, $fb
        .byte $09, $00, $0a, $fc, $0b, $fb, $09, $00
        .byte $09, $f9, $09, $00, $0a, $fc, $0a, $03
        .byte $09, $f9, $09, $00, $0a, $01, $0b, $fb
        .byte $fe, $04
; pattern 33: t_lead_intro
pat_33:
        .byte $bf, $60, $ff
; pattern 34: t_lead_a
pat_34:
        .byte $c1, $85, $37, $81, $3a, $87, $3e, $85
        .byte $3f, $81, $3e, $83, $3c, $3a, $85, $3e
        .byte $81, $41, $87, $46, $83, $45, $43, $41
        .byte $3c, $85, $43, $81, $41, $83, $3e, $37
        .byte $3a, $3c, $3f, $43, $87, $42, $83, $45
        .byte $3e, $8b, $3e, $83, $60, $ff
; pattern 35: t_lead_b
pat_35:
        .byte $c0, $85, $48, $81, $46, $83, $43, $3f
        .byte $85, $3e, $81, $43, $87, $46, $83, $46
        .byte $48, $4b, $4a, $85, $4a, $81, $48, $87
        .byte $46, $85, $4b, $81, $4a, $83, $48, $43
        .byte $85, $46, $81, $48, $83, $4b, $4f, $85
        .byte $4e, $81, $4c, $83, $4a, $45, $42, $45
        .byte $48, $4a, $ff
; pattern 36: t_pulse
pat_36:
        .byte $c2, $81, $1f, $c4, $2b, $1f, $2b, $c3
        .byte $1f, $c4, $2b, $1f, $2b, $ff
; pattern 37: t_turn
pat_37:
        .byte $c2, $81, $1f, $c4, $2b, $1f, $2b, $c3
        .byte $1f, $1f, $1f, $1f, $ff
; pattern 38: t_minor
pat_38:
        .byte $c8, $8f, $2b, $ff
; pattern 39: t_major
pat_39:
        .byte $c9, $8f, $2b, $ff
; pattern 40: t_dom7
pat_40:
        .byte $ca, $8f, $2b, $ff
order_9:
        .byte $21, $00, $22, $00, $23, $00, $fe, $01
order_10:
        .byte $24, $00, $24, $fc, $24, $05, $25, $fb
        .byte $24, $00, $24, $fc, $24, $03, $24, $fe
        .byte $24, $00, $24, $fc, $24, $fb, $25, $fb
        .byte $24, $05, $24, $00, $24, $fc, $24, $03
        .byte $24, $05, $24, $fc, $24, $fb, $25, $fb
        .byte $fe, $04
order_11:
        .byte $26, $00, $27, $fc, $26, $05, $28, $fb
        .byte $26, $00, $27, $fc, $27, $03, $27, $fe
        .byte $26, $00, $27, $fc, $27, $fb, $28, $fb
        .byte $26, $05, $26, $00, $27, $fc, $27, $03
        .byte $26, $05, $27, $fc, $27, $fb, $28, $fb
        .byte $fe, $04
