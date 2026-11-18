; The VIC-II: bank 1, multicolour characters, 38 columns, {3}
; and the eight sprites. (init_vic and init_sprites, the {3}
; start of a game, are in title.asm.) {3}
;|; The VIC-II: bank 1, multicolour characters, 38 columns. {1-2}
;|; (init_vic, the start of a game, is in title.asm.) {1-2}

; The screen on, from the next frame; or off. Bit 7 of
; $d011 read is the beam's line bit 8; written, it is the
; interrupt line's: always 0 here, or the interrupts on
; lines 20-225 would wait for lines 276-481.
screen_on:
        lda $d011
        and #%01111111
        ora #%00010000
        sta $d011
        rts

screen_off:
        lda $d011
        and #%01101111
        sta $d011
        rts

