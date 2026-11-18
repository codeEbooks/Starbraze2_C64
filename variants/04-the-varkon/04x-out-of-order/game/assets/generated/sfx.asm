; Written by game/assets/sfx.py: do not edit.

FX_SHOT_DOUBLE = 0
FX_SHOT_NEEDLE = 1
FX_SHOT_SLUG = 2
FX_PLASMA = 3
FX_HURT = 4
FX_EXPLODE = 5
FX_BOOM = 6
FX_LASER = 7
FX_MISSILE = 8
FX_CAPSULE = 9
FX_COUNT = 10
FX_HEADER = 4
FX_REEL_FRAMES = 40

sfx_first:
        .byte $00, $11, $1c, $2f, $42, $55, $6c, $81
        .byte $8e, $9b
sfx_voice:
        .byte $00, $00, $00, $01, $02, $02, $01, $00
        .byte $00, $02
sfx_pri:
        .byte $01, $01, $01, $02, $04, $05, $03, $01
        .byte $01, $04
; 0: shot_double
sfx_data:
        .byte $01, $00, $f4, $06, $41, $54, $41, $4f, $41
        .byte $4a, $41, $45, $41, $40, $41, $3b, $00
; 1: shot_needle
        .byte $01, $00, $c2, $05, $41, $58, $41, $53, $41
        .byte $4e, $00
; 2: shot_slug
        .byte $01, $00, $f5, $08, $81, $48, $21, $30, $21
        .byte $2d, $21, $29, $21, $26, $21, $23, $21, $1f
        .byte $00
; 3: plasma
        .byte $02, $00, $f4, $08, $11, $30, $11, $37, $11
        .byte $32, $11, $39, $11, $34, $11, $3b, $11, $42
        .byte $00
; 4: hurt
        .byte $02, $00, $f6, $08, $81, $51, $21, $40, $21
        .byte $3c, $21, $39, $21, $35, $21, $32, $21, $2f
        .byte $00
; 5: explode
        .byte $03, $0a, $8a, $08, $81, $4c, $81, $48, $81
        .byte $45, $81, $41, $81, $3e, $81, $3b, $81, $37
        .byte $81, $34, $81, $30, $00
; 6: boom
        .byte $02, $00, $f6, $08, $81, $51, $81, $4d, $81
        .byte $4a, $81, $45, $81, $41, $81, $3e, $81, $39
        .byte $81, $35, $00
; 7: laser
        .byte $01, $00, $c3, $04, $41, $54, $41, $4f, $41
        .byte $48, $41, $43, $00
; 8: missile
        .byte $02, $00, $c4, $08, $81, $30, $81, $34, $81
        .byte $37, $81, $3c, $00
; 9: capsule
        .byte $02, $00, $f6, $08, $41, $3c, $41, $40, $41
        .byte $43, $41, $48, $41, $4c, $41, $4f, $41, $54
        .byte $00
