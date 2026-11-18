; Written by game/assets/music.py from score.py: do not
; edit.

MUSIC_GATE_TICK = 2
MUSIC_SHORTEST_STEP = 4
MUSIC_HIGHEST = 93
MUSIC_SONGS = 7
SONG_THEME = 0
SONG_THEME_FRAMES = 2592
SONG_SPACE = 1
SONG_SPACE_FRAMES = 2464
SONG_BOSS = 2
SONG_BOSS_FRAMES = 1024
SONG_TITLE = 3
SONG_TITLE_FRAMES = 1920
SONG_CLEAR = 4
SONG_CLEAR_FRAMES = 160
SONG_OVER = 5
SONG_OVER_FRAMES = 144
SONG_WIN = 6
SONG_WIN_FRAMES = 240
SONG_END = $fd

freq_lo:
        .byte $16, $27, $39, $4b, $5f, $74, $8a, $a1
        .byte $ba, $d4, $f0, $0e, $2d, $4e, $71, $96
        .byte $be, $e7, $14, $42, $74, $a9, $e0, $1b
        .byte $5a, $9c, $e2, $2d, $7b, $cf, $27, $85
        .byte $e8, $51, $c1, $37, $b4, $38, $c4, $59
        .byte $f7, $9d, $4e, $0a, $d0, $a2, $81, $6d
        .byte $67, $70, $89, $b2, $ed, $3b, $9c, $13
        .byte $a0, $45, $02, $da, $ce, $e0, $11, $64
        .byte $da, $76, $39, $26, $40, $89, $04, $b4
        .byte $9c, $c0, $23, $c8, $b4, $eb, $72, $4c
        .byte $80, $12, $08, $68, $39, $80, $45, $90
        .byte $68, $d6, $e3, $99, $00, $24
freq_hi:
        .byte $01, $01, $01, $01, $01, $01, $01, $01
        .byte $01, $01, $01, $02, $02, $02, $02, $02
        .byte $02, $02, $03, $03, $03, $03, $03, $04
        .byte $04, $04, $04, $05, $05, $05, $06, $06
        .byte $06, $07, $07, $08, $08, $09, $09, $0a
        .byte $0a, $0b, $0c, $0d, $0d, $0e, $0f, $10
        .byte $11, $12, $13, $14, $15, $17, $18, $1a
        .byte $1b, $1d, $1f, $20, $22, $24, $27, $29
        .byte $2b, $2e, $31, $34, $37, $3a, $3e, $41
        .byte $45, $49, $4e, $52, $57, $5c, $62, $68
        .byte $6e, $75, $7c, $83, $8b, $93, $9c, $a5
        .byte $af, $b9, $c4, $d0, $dd, $ea
tempo_table:
        .byte $05, $04, $05, $04, $06, $05, $06, $05
        .byte $04, $04, $04, $04, $06, $06, $06, $06
        .byte $05, $05, $05, $05, $06, $06, $06, $06
        .byte $05, $05, $05, $05
song_lists:
        .byte $00, $03, $06, $09, $0c, $0f, $12
ins_ad:
        .byte $08, $18, $07, $07, $07, $05, $05, $05
        .byte $28, $28, $28, $48
ins_sr:
        .byte $a8, $a9, $a4, $a4, $a4, $00, $00, $00
        .byte $86, $86, $86, $a9
ins_ad_fx:
        .byte $05, $15, $05, $05, $05, $05, $05, $05
        .byte $25, $25, $25, $45
ins_sr_fx:
        .byte $58, $59, $54, $54, $54, $00, $00, $00
        .byte $36, $36, $36, $59
ins_wave:
        .byte $01, $01, $0b, $0f, $00, $02, $05, $08
        .byte $02, $05, $08, $12
ins_pw_lo:
        .byte $00, $00, $00, $00, $00, $00, $00, $00
        .byte $00, $00, $00, $00
ins_pw_hi:
        .byte $08, $08, $06, $06, $06, $04, $04, $04
        .byte $06, $06, $06, $08
ins_sweep:
        .byte $20, $00, $00, $00, $00, $10, $10, $10
        .byte $18, $18, $18, $00
ins_vibrato:
        .byte $14, $10, $00, $00, $00, $00, $00, $00
        .byte $00, $00, $00, $18
wave_ctrl:
        .byte $40, $20, $40, $40, $40, $40, $40, $40
        .byte $40, $40, $40, $40, $10, $10, $40, $80
        .byte $80, $40, $10
wave_pitch:
        .byte $00, $00, $00, $03, $07, $00, $04, $07
        .byte $00, $04, $0a, $b0, $a6, $9e, $00, $d6
        .byte $cf, $00, $00
wave_next:
        .byte $00, $01, $03, $04, $02, $06, $07, $05
        .byte $09, $0a, $08, $0c, $0d, $0e, $0e, $10
        .byte $11, $11, $12
pattern_lo:
        .byte <pat_0
        .byte <pat_1
        .byte <pat_2
        .byte <pat_3
        .byte <pat_4
        .byte <pat_5
        .byte <pat_6
        .byte <pat_7
        .byte <pat_8
        .byte <pat_9
        .byte <pat_10
        .byte <pat_11
        .byte <pat_12
        .byte <pat_13
        .byte <pat_14
        .byte <pat_15
        .byte <pat_16
        .byte <pat_17
        .byte <pat_18
        .byte <pat_19
        .byte <pat_20
        .byte <pat_21
        .byte <pat_22
        .byte <pat_23
        .byte <pat_24
        .byte <pat_25
        .byte <pat_26
        .byte <pat_27
        .byte <pat_28
        .byte <pat_29
        .byte <pat_30
        .byte <pat_31
        .byte <pat_32
        .byte <pat_33
        .byte <pat_34
        .byte <pat_35
        .byte <pat_36
        .byte <pat_37
        .byte <pat_38
        .byte <pat_39
        .byte <pat_40
        .byte <pat_41
        .byte <pat_42
        .byte <pat_43
        .byte <pat_44
        .byte <pat_45
        .byte <pat_46
        .byte <pat_47
        .byte <pat_48
        .byte <pat_49
        .byte <pat_50
        .byte <pat_51
pattern_hi:
        .byte >pat_0
        .byte >pat_1
        .byte >pat_2
        .byte >pat_3
        .byte >pat_4
        .byte >pat_5
        .byte >pat_6
        .byte >pat_7
        .byte >pat_8
        .byte >pat_9
        .byte >pat_10
        .byte >pat_11
        .byte >pat_12
        .byte >pat_13
        .byte >pat_14
        .byte >pat_15
        .byte >pat_16
        .byte >pat_17
        .byte >pat_18
        .byte >pat_19
        .byte >pat_20
        .byte >pat_21
        .byte >pat_22
        .byte >pat_23
        .byte >pat_24
        .byte >pat_25
        .byte >pat_26
        .byte >pat_27
        .byte >pat_28
        .byte >pat_29
        .byte >pat_30
        .byte >pat_31
        .byte >pat_32
        .byte >pat_33
        .byte >pat_34
        .byte >pat_35
        .byte >pat_36
        .byte >pat_37
        .byte >pat_38
        .byte >pat_39
        .byte >pat_40
        .byte >pat_41
        .byte >pat_42
        .byte >pat_43
        .byte >pat_44
        .byte >pat_45
        .byte >pat_46
        .byte >pat_47
        .byte >pat_48
        .byte >pat_49
        .byte >pat_50
        .byte >pat_51
order_lo:
        .byte <order_0
        .byte <order_1
        .byte <order_2
        .byte <order_3
        .byte <order_4
        .byte <order_5
        .byte <order_6
        .byte <order_7
        .byte <order_8
        .byte <order_9
        .byte <order_10
        .byte <order_11
        .byte <order_12
        .byte <order_13
        .byte <order_14
        .byte <order_15
        .byte <order_16
        .byte <order_17
        .byte <order_18
        .byte <order_19
        .byte <order_20
order_hi:
        .byte >order_0
        .byte >order_1
        .byte >order_2
        .byte >order_3
        .byte >order_4
        .byte >order_5
        .byte >order_6
        .byte >order_7
        .byte >order_8
        .byte >order_9
        .byte >order_10
        .byte >order_11
        .byte >order_12
        .byte >order_13
        .byte >order_14
        .byte >order_15
        .byte >order_16
        .byte >order_17
        .byte >order_18
        .byte >order_19
        .byte >order_20
; pattern 15: s_lead_intro
pat_15:
        .byte $bf, $60, $ff
; pattern 16: s_lead_a
pat_16:
        .byte $cb, $85, $40, $81, $45, $83, $47, $48
        .byte $87, $45, $83, $43, $41, $85, $40, $81
        .byte $43, $83, $48, $47, $87, $4a, $83, $47
        .byte $43, $85, $45, $81, $48, $83, $4c, $4a
        .byte $87, $48, $83, $45, $41, $85, $44, $81
        .byte $47, $83, $4c, $4a, $8b, $47, $83, $60
        .byte $ff
; pattern 17: s_lead_b
pat_17:
        .byte $c1, $83, $45, $48, $4d, $4c, $87, $4a
        .byte $83, $47, $43, $4c, $81, $4a, $47, $83
        .byte $43, $47, $8b, $45, $83, $40, $81, $41
        .byte $45, $83, $48, $4d, $4c, $4a, $4f, $81
        .byte $4d, $4c, $83, $4a, $85, $49, $81, $4c
        .byte $87, $51, $83, $51, $81, $4f, $4c, $83
        .byte $49, $47, $ff
; pattern 18: s_lead_c
pat_18:
        .byte $cb, $87, $41, $83, $40, $3e, $87, $3c
        .byte $83, $39, $3c, $87, $40, $83, $3e, $3c
        .byte $87, $3b, $83, $3e, $43, $85, $45, $81
        .byte $41, $83, $3e, $41, $85, $48, $81, $45
        .byte $83, $41, $45, $85, $47, $81, $44, $83
        .byte $40, $44, $87, $47, $83, $4a, $4c, $ff
; pattern 19: s_pulse
pat_19:
        .byte $c2, $81, $21, $c4, $2d, $21, $2d, $c3
        .byte $21, $c4, $2d, $21, $2d, $ff
; pattern 20: s_turn
pat_20:
        .byte $c2, $81, $21, $c4, $2d, $21, $2d, $c3
        .byte $21, $c4, $2d, $c3, $21, $21, $ff
; pattern 21: s_half
pat_21:
        .byte $c2, $83, $21, $c4, $2d, $c3, $21, $c4
        .byte $2d, $ff
; pattern 22: s_minor
pat_22:
        .byte $c8, $8f, $2d, $ff
; pattern 23: s_major
pat_23:
        .byte $c9, $8f, $2d, $ff
; pattern 24: s_dom7
pat_24:
        .byte $ca, $8f, $2d, $ff
order_3:
        .byte $0f, $00, $10, $00, $11, $00, $12, $00
        .byte $fe, $01
order_4:
        .byte $13, $00, $13, $fc, $13, $00, $14, $fb
        .byte $13, $00, $13, $fc, $13, $03, $13, $fe
        .byte $13, $00, $13, $fc, $13, $fb, $14, $fb
        .byte $13, $fc, $13, $fe, $13, $fb, $13, $00
        .byte $13, $fc, $13, $fe, $13, $00, $14, $00
        .byte $15, $05, $15, $fc, $15, $00, $15, $fe
        .byte $13, $05, $13, $fc, $13, $fb, $14, $fb
        .byte $fe, $04
order_5:
        .byte $16, $00, $17, $fc, $16, $00, $17, $fb
        .byte $16, $00, $17, $fc, $17, $03, $17, $fe
        .byte $16, $00, $17, $fc, $17, $fb, $18, $fb
        .byte $17, $fc, $17, $fe, $16, $fb, $16, $00
        .byte $17, $fc, $17, $fe, $17, $00, $17, $00
        .byte $16, $05, $17, $fc, $16, $00, $17, $fe
        .byte $16, $05, $17, $fc, $17, $fb, $18, $fb
        .byte $fe, $04
; pattern 25: b_riff
pat_25:
        .byte $c0, $81, $3c, $3c, $3f, $3c, $43, $3c
        .byte $42, $43, $ff
; pattern 26: b_neap
pat_26:
        .byte $c0, $81, $3d, $41, $44, $41, $83, $49
        .byte $48, $ff
; pattern 27: b_fall
pat_27:
        .byte $c0, $83, $43, $41, $3f, $3e, $ff
; pattern 28: b_hold
pat_28:
        .byte $c1, $85, $43, $81, $44, $83, $43, $48
        .byte $ff
; pattern 29: b_cry
pat_29:
        .byte $c1, $8b, $48, $83, $47, $ff
; pattern 30: b_drive
pat_30:
        .byte $c2, $81, $18, $c4, $24, $18, $24, $c3
        .byte $18, $c4, $24, $18, $24, $ff
; pattern 31: b_minor
pat_31:
        .byte $c5, $81, $60, $83, $30, $30, $81, $30
        .byte $83, $30, $ff
; pattern 32: b_major
pat_32:
        .byte $c6, $81, $60, $83, $30, $30, $81, $30
        .byte $83, $30, $ff
order_6:
        .byte $19, $00, $19, $00, $19, $05, $1b, $00
        .byte $19, $00, $19, $00, $1a, $00, $1b, $00
        .byte $1c, $fc, $1c, $fc, $1c, $05, $1c, $05
        .byte $1c, $01, $1c, $01, $1d, $fb, $1b, $00
        .byte $fe, $00
order_7:
        .byte $1e, $00, $1e, $00, $1e, $05, $1e, $fb
        .byte $1e, $00, $1e, $00, $1e, $01, $1e, $fb
        .byte $1e, $fc, $1e, $fc, $1e, $05, $1e, $05
        .byte $1e, $01, $1e, $01, $1e, $fb, $1e, $fb
        .byte $fe, $00
order_8:
        .byte $1f, $00, $1f, $00, $1f, $05, $20, $fb
        .byte $1f, $00, $1f, $00, $20, $01, $20, $fb
        .byte $20, $fc, $20, $fc, $1f, $05, $1f, $05
        .byte $20, $01, $20, $01, $20, $fb, $20, $fb
        .byte $fe, $00
; pattern 41: jc_lead
pat_41:
        .byte $c1, $81, $37, $3c, $40, $85, $43, $81
        .byte $40, $43, $8b, $48, $83, $60, $ff
; pattern 42: jc_bass
pat_42:
        .byte $c2, $83, $24, $c4, $1f, $24, $1f, $c2
        .byte $8b, $24, $83, $60, $ff
; pattern 43: jc_pads
pat_43:
        .byte $c9, $8f, $30, $8b, $30, $83, $60, $ff
order_12:
        .byte $29, $00, $fd
order_13:
        .byte $2a, $00, $fd
order_14:
        .byte $2b, $00, $fd
; pattern 44: jo_lead
pat_44:
        .byte $cb, $83, $37, $35, $33, $32, $87, $30
        .byte $ff
; pattern 45: jo_bass
pat_45:
        .byte $c2, $87, $24, $c4, $1f, $18, $ff
; pattern 46: jo_pads
pat_46:
        .byte $c8, $87, $30, $c9, $2c, $c8, $30, $ff
order_15:
        .byte $2c, $00, $fd
order_16:
        .byte $2d, $00, $fd
order_17:
        .byte $2e, $00, $fd
; pattern 47: jw_lead
pat_47:
        .byte $c1, $81, $3e, $42, $45, $85, $4a, $81
        .byte $45, $4a, $83, $4c, $81, $4a, $4c, $83
        .byte $4e, $4c, $8b, $4a, $83, $60, $ff
; pattern 48: jw_bass
pat_48:
        .byte $c2, $83, $26, $c4, $21, $c2, $26, $c4
        .byte $21, $ff
; pattern 49: jw_end
pat_49:
        .byte $c2, $8b, $26, $83, $60, $ff
; pattern 50: jw_pads
pat_50:
        .byte $c9, $8f, $32, $ff
; pattern 51: jw_pend
pat_51:
        .byte $c9, $8b, $32, $83, $60, $ff
order_18:
        .byte $2f, $00, $fd
order_19:
        .byte $30, $00, $30, $fb, $31, $00, $fd
order_20:
        .byte $32, $00, $32, $fb, $33, $00, $fd
