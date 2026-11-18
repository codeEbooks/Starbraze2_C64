; ---------------------------------------------------------
; The choice of the ship (states.asm),
; in the program's high part
; ---------------------------------------------------------

; The ship chosen: its weapon (the level it had), its full
; shield, its name and its pilot in row 1, row 2 again.
ship_shown:
        jsr set_weapon          ; (and the HUD's row 2)
        ldx ship_type
        lda ship_shield,x
        sta shield
        lda #0
        ldx #39                 ; row 1 blank
-       sta SCREEN_A + HUD_ROW1,x
        dex
        bpl -
        lda ship_type           ; messages 2 k, 2 k + 1
        asl a
        pha
        tax
        jsr hud_say
        pla
        tax
        inx
        jsr hud_say
        jmp update_hud

; Message X into row 1 of the HUD: its codes (the HUD's
; letters) from its column, in its colour.
hud_say:
        lda msg_colour,x
        sta say_colour
        lda msg_end,x
        sta say_end
        ldy msg_col,x
        lda msg_from,x
        tax
-       lda msg_text,x
        sta SCREEN_A + HUD_ROW1,y
        lda say_colour
        sta COLOURS + HUD_ROW1,y
        iny
        inx
        cpx say_end
        bne -
        rts

; The next ship to choose, held at its place: after a ship
; lost where it comes in to (ENTER_TO, by the left edge:
; after the choice it comes in from the left; held_time 1);
; at the start of a game at A (title.asm: START_X; after the
; choice it flies from it).
choose_lost:
        lda #1
        sta held_time
        lda #ENTER_TO
        bne choose_at           ; (always)
choose_next:
        ldx #0
        stx held_time
choose_at:
        ldx #0
        ldy #CHOOSE
        jsr come_in
        lda #HELD_CHOOSE
        sta held
        rts

; The messages (build_assets.py): the ships' names and
; their pilots, PAUSED, GAME OVER: where they begin and end,
; their columns and colours (states.inc); their codes after
; the boss's body (data.asm: msg_text, states_text.inc).
        .include "../assets/generated/states.inc"
