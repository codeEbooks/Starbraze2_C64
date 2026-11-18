; The data written by game/assets/build_assets.py.
;
; The levels are packed: each level start unpacks its own
; (level.asm, load_level) into its places, LEVEL_W1 here and
; LEVEL_W2 (after rock_lines), its characters into CHARSET,
; its pictures into SPRITES2. The packed levels live in
; STORE ($d000, under the I/O and the KERNAL); the PRG
; cannot load there, so it carries them in pieces where the
; program later makes other things (STAGE_*: here at
; SCREEN_A, LEVEL_W1 and SPRITES2, at rock_lines and at
; LEVEL_W2: main.asm), and moves them once (move_store).

        .include "../assets/generated/tables.inc"
        .include "../assets/generated/levels.inc"
metatile_tl = metatiles
metatile_tr = metatiles + METATILE_COUNT
metatile_bl = metatiles + 2 * METATILE_COUNT
metatile_br = metatiles + 3 * METATILE_COUNT
hud_rows:
        .binary "../assets/generated/hud.bin"
store_moved:                    ; 1: the store is in place
        .byte 0
LEVEL_W1:                       ; the store's 4th
stage_3:                        ; piece, until it is moved
        .binary "../assets/generated/store3.bin"
        .cerror STAGE_LEN_3 != 0, "LEVEL_W1: the title's"
title_from:                     ; title.asm's module,
        .logical TITLE_AT       ; until move_store moves it
        .include "title.asm"    ; to TITLE_AT, in the store
        .here
TITLE_LEN = * - title_from
        .cerror TITLE_LEN > LEVEL_W1_SIZE, "the title"
        .cerror TITLE_AT < STORE + STORE_SIZE, "the title"
        .cerror TITLE_AT + TITLE_ALL > $fffa, "the title"
        .fill LEVEL_W1_SIZE - TITLE_LEN
code_end:
        .cerror * > SCREEN_A, "code and data reach screen A"

        * = SCREEN_A            ; (screens, characters)
stage_0:
        .binary "../assets/generated/store0.bin"
        .cerror * > HUDSET, "the store's first piece"
        * = HUDSET
        .binary "../assets/generated/hudset.bin"
hud_hole:                       ; the codes the HUD
        .include "hole.asm"     ; never shows: the program's
        .cerror * > HUDSET + $800, "the HUD's hole"
        * = HUDSET + $800       ; (the crawler's body) {8}
        .include "../assets/generated/boss_body.inc" ; {8}
        .include "../assets/generated/states_text.inc" ; {16}
        .cerror * > SPRITES, "the boss's body: too long" ; {8}
                                ; (and the messages' {16}
                                ; codes, states.asm) {16}
        * = SPRITES ; {3}
        .binary "../assets/generated/sprites.bin" ; {3}
        .include "../assets/generated/boss_more.inc" ; {8}
        .cerror * > SPRITES2, "the mouth and the hatch" ; {8}
        * = SPRITES2            ; the level's pictures, at
stage_4:                        ; first the store's 5th
        .binary "../assets/generated/store4.bin" ; piece
        .cerror STAGE_LEN_4 != 0, "SPRITES2: the title's"
title_data_from:                ; the title's data, {16}
        .logical TITLE_AT + TITLE_LEN ; after its code {16}
        .include "../assets/generated/title.inc" ; {16}
        .here ; {16}
TITLE_DATA_LEN = * - title_data_from ; {16}
        .fill $400 - TITLE_DATA_LEN ; {16}
;|        .fill $400 ; {1-15}
        .cerror * > AUDIO, "the sprites past $8000"
