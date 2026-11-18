; ---------------------------------------------------------
; The start of a game
; ---------------------------------------------------------

; The module of the start of a game: assembled with the
; program, carried by the PRG in LEVEL_W1 (data.asm) and
; moved to TITLE_AT by move_store. The program comes here at
; its start (entry); it runs here, under the KERNAL (out).

; The game's start: the VIC-II, the HUD, level 1; the
; interrupts on, the main loop.
game_start:
        lda #0
        sta level
        jsr init_vic            ; the screen off meanwhile
        jsr draw_hud
        jsr init_level
        jsr camera_plan         ; the first turn's camera
        lda #0
        sta frame_count
        sta frame_flag
        jsr init_irq            ; the interrupts on
        jsr screen_on
        jmp frame_loop

; The VIC-II: bank 1, multicolour characters, 38 columns,
; black until the level's colours (load_level). Both screens
; are cleared first: the store's first piece was there
; (data.asm), and what no row shows (screen B's rows 22-24,
; the bytes before the pointers) stays 0.
init_vic:
        lda #0
        tax
-       .for clr_k in range(8)
        sta SCREEN_A + clr_k * 256,x
        .endfor
        inx
        bne -
        lda $dd02               ; CIA 2 port A, bits 0-1 out
        ora #%00000011
        sta $dd02
        lda $dd00               ; bank 1: bits 0-1 = %10
        and #%11111100
        ora #%00000010
        sta $dd00
        lda #D018_A
        sta $d018
        lda #D016_BASE          ; multicolour, 38 columns
        sta $d016
        lda #%00001011          ; 25 rows, screen off
        sta $d011
        lda #0
        sta $d020               ; black border
        lda #0                  ; black until the level's
        sta $d021               ; colours (load_level)
        sta $d022
        sta $d023
        rts

; The HUD: three rows of codes on screen A, their colours.
draw_hud:
        ldx #0
_cell:
        lda hud_rows,x
        sta SCREEN_A + HUD_CELL,x
        lda hud_rows + 120,x
        sta COLOURS + HUD_CELL,x
        inx
        cpx #120
        bne _cell
        rts

TITLE_ALL = TITLE_LEN
