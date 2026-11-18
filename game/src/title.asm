; ---------------------------------------------------------
; The title, and the start of a game {16}
;|; The start of a game {1-15}
; ---------------------------------------------------------

;{16}
; The title's module: assembled with the program, carried by
; the PRG in LEVEL_W1 (data.asm) and moved to TITLE_AT by
; move_store; phase 1's file brings it again (make_disk.py)
; after levels 3-6, whose files write over it. The program
; comes here at its start (entry) and after GAME OVER and
; the victory (title_return), always with phase 1 in the
; store; it runs here, under the KERNAL (out).
;
; The author, 4 November: «Logo con una piccola scena»: {17}
; STARBRAZE II big in characters, the story's sentence (in {17}
; English in the game), the record, the sound's menu, the {17}
; stars scrolling and the three ships across the screen in {17}
; sprites. How (title.py, build_assets.py: title.inc): {17}
; screen A with its own characters at CHARSET (the HUD's {17}
; letters copied, the same codes: the HUD's texts; then the {17}
; stars, `.`, `+` and the logo's pieces); the logo's letters {17}
; are the HUD's, a pixel 2 x 3 multicolour pixels, yellow, {17}
; orange, red from the top (II white, orange, red); the {17}
; three ships in a V on sprites 0-5, a pixel a frame; SOUND: {17}
; Up and Down, the mode at once (the title's theme from its {17}
; start); Fire: the game (the choice of the ship, {17}
; states.asm). The game's interrupts run (irq.asm: the SID's {17}
; copy, frame_flag): the screen and the scrolls the same at {17}
; their writes, no plan of sprites; the HUD's rows (22-24) {17}
; from the HUD's own characters, the same letters (no stars {17}
; there). {17}
;|; The author, 4 November: «Logo con una piccola scena»: {16-16}
;|; STARBRAZE II big in characters, the story's sentence (in {16-16}
;|; English in the game), the record, the sound's menu, the {16-16}
;|; stars scrolling and the three ships across the screen in {16-16}
;|; sprites. How (title.py, build_assets.py: title.inc): {16-16}
;|; screen A with its own characters at CHARSET (the HUD's {16-16}
;|; letters copied, the same codes: the HUD's texts; then the {16-16}
;|; stars, `.`, `+` and the logo's pieces); the logo's letters {16-16}
;|; are the HUD's, a pixel 2 x 3 multicolour pixels, yellow, {16-16}
;|; orange, red from the top (II white, orange, red); the {16-16}
;|; three ships in a V on sprites 0-5, a pixel a frame; SOUND: {16-16}
;|; Up and Down, the mode at once (the canyons' theme from its {16-16}
;|; start); Fire: the game (the choice of the ship, {16-16}
;|; states.asm). The game's interrupts run (irq.asm: the SID's {16-16}
;|; copy, frame_flag): the screen and the scrolls the same at {16-16}
;|; their writes, no plan of sprites; the HUD's rows (22-24) {16-16}
;|; from the HUD's own characters, the same letters (no stars {16-16}
;|; there). {16-16}

T_D016    = %00011000           ; multicolour, 40 columns
; Its variables in LEVEL_W1, which no level fills yet (the
; module never changes: phase 1's file and the tests find it
; as the PRG brings it): the stars' x, the V's.
t_sx      = LEVEL_W1            ; T_STAR_COUNT bytes
t_sxh     = t_sx + T_STAR_COUNT
t_v       = t_sxh + T_STAR_COUNT ; 2 bytes
SHIP_GAP  = 32                  ; the wingmen behind, pixels
SHIP_WRAP = 512                 ; the V's x: 0-511, a pass
SHIP_SHOW = 360                 ; seen from 0 to 359

title:
        sei
        ldx #$ff                ; fresh stack: from the
        txs                     ; game, the main loop's
        lda #0
        sta level               ; (sound_set: level 1's
        sta held                ; song)
        sta mux_ready           ; no plan of sprites
        sta top_d021            ; black
        jsr init_vic            ; screens 0, the screen off
        jsr init_sprites
        lda #D018_A             ; for the interrupts: screen
        sta shown_d018          ; A, the title's characters,
        lda #T_D016             ; its colours
        sta near_d016
        sta far_d016
        lda #T_D022
        sta top_d022
        lda #T_D023
        sta top_d023
        lda #<HUDSET            ; the HUD's characters
        sta src
        lda #>HUDSET
        sta src + 1
        lda #<CHARSET
        sta dst
        lda #>CHARSET
        sta dst + 1
        lda #<(HUD_CHARS * 8)
        sta lz_end
        lda #>(HUD_CHARS * 8)
        sta lz_end + 1
        jsr copy_bytes
        ldx #8 * 8 - 1          ; the stars: a pixel in row
-       lda #0                  ; 3, at 0-7
        sta CHARSET + T_STAR0 * 8,x
        dex
        bpl -
        ldx #0
        lda #%10000000
-       sta CHARSET + T_STAR0 * 8 + 3,x
        pha
        txa
        clc
        adc #8                  ; the next character's row
        tax
        pla
        lsr a
        bcc -
        ldx #0                  ; then `.`, `+`, the logo
-       lda t_chars,x
        sta CHARSET + T_CHAR_AT * 8,x
        lda t_chars + 256,x
        sta CHARSET + T_CHAR_AT * 8 + 256,x
        lda t_chars + 512,x
        sta CHARSET + T_CHAR_AT * 8 + 512,x
        inx
        bne -
        .cerror T_CHAR_BYTES > 768, "t_chars"
        ldx #T_STAR_COUNT - 1   ; the stars at their places
-       lda t_star_x,x
        sta t_sx,x
        lda t_star_xh,x
        sta t_sxh,x
        dex
        bpl -
        jsr t_print             ; the logo, the words
        jsr t_record
        jsr t_menu
        jsr t_ships_on
        lda #%00001111          ; the sound: volume 15, the
        sta sid_shadow + 24     ; mode's (sound_init): from {17}
;|        sta sid_shadow + 24     ; mode's (sound_init) {16-16}
        lda #SONG_TITLE         ; the title's theme {17}
        jsr song_start ; {17}
;|        lda sound_mode ; {16-16}
;|        jsr sound_set ; {16-16}
        lda #$ff                ; Fire held: not pushed
        sta joy_prev
        lda #0
        sta frame_flag
        jsr init_irq
        jsr screen_on

; A turn a frame, from the HUD's line (frame_flag): the
; sound, the keys and the joystick, the stars, the ships.
title_loop:
        lda frame_flag
        beq title_loop
        lda #0
        sta frame_flag
        jsr music_play
        jsr sfx_play
        jsr read_input
title_input:                    ; the tests look here
        lda joy_prev            ; just pushed: Y
        eor #%11111111
        and joy
        tay
        lda joy
        sta joy_prev
        tya
        and #JOY_FIRE
        beq +
        jmp game_start
+       tya
        and #JOY_UP | JOY_DOWN
        beq _scene
        ldx sound_mode          ; SOUND: Up, Down
        and #JOY_UP
        beq _down
        dex
        bpl _mode
        ldx #MODE_SILENT
        bne _mode
_down:
        inx
        cpx #MODE_SILENT + 1
        bcc _mode
        ldx #MODE_MUSIC
_mode:
        txa
        jsr mode_set            ; from silence (the {17}
                                ; title's theme) {17}
;|        jsr sound_set           ; from silence {16-16}
        lda #FX_CAPSULE         ; a click, if the mode has
        jsr sfx_start           ; effects
        jsr t_menu
_scene:
        jsr t_stars
        jsr t_ships
        jmp title_loop

; The records of title.inc: a cell of the screen (0-999,
; low and high byte), a colour, a count (0: the end), the
; codes; into screen A and the colour RAM.
t_print:
        lda #<t_records
        sta src
        lda #>t_records
        sta src + 1
_record:
        ldy #3
        lda (src),y             ; the count
        beq _done
        sta count
        dey
        lda (src),y             ; the colour
        sta temp
        dey
        lda (src),y
        tax
        clc
        adc #>SCREEN_A
        sta dst + 1
        txa
        adc #>COLOURS
        sta vector + 1
        dey
        lda (src),y
        sta dst
        sta vector
        clc                     ; the codes
        lda src
        adc #4
        sta src
        bcc +
        inc src + 1
+       ldy #0
-       lda (src),y
        sta (dst),y
        lda temp
        sta (vector),y
        iny
        cpy count
        bne -
        tya                     ; the next record
        clc
        adc src
        sta src
        bcc _record
        inc src + 1
        bne _record             ; (always)
_done:
        rts

; The record of the session (score.asm: hi_score): six
; digits, from the high byte.
t_record:
        ldx #2
        ldy #0
-       lda hi_score,x
        lsr a
        lsr a
        lsr a
        lsr a
        clc
        adc #DIGIT_CODE
        sta SCREEN_A + T_HI_CELL,y
        lda hi_score,x
        and #%00001111
        clc
        adc #DIGIT_CODE
        sta SCREEN_A + T_HI_CELL + 1,y
        iny
        iny
        dex
        bpl -
        rts

; The sound's menu: the mode's row in its colour, the other
; three in theirs.
t_menu:
        ldx #0
_row:
        lda #T_MENU_OFF
        cpx sound_mode
        bne +
        lda #T_MENU_ON
+       ldy t_menu_at,x
        sty dst
        ldy t_menu_hi,x
        sty dst + 1
        ldy #T_MENU_LEN - 1
-       sta (dst),y
        dey
        bpl -
        inx
        cpx #4
        bne _row
        rts

t_menu_at:
        .byte <(COLOURS + T_MENU_CELL + range(4) * 40)
t_menu_hi:
        .byte >(COLOURS + T_MENU_CELL + range(4) * 40)

; The stars: each in its row, x in half pixels (0-639),
; left by its speed a frame; a character of the eight, its
; pixel.
t_stars:
        ldx #T_STAR_COUNT - 1
_star:
        lda t_star_row,x        ; its row: screen, colours
        sta dst
        sta vector
        lda t_star_hi,x
        sta dst + 1
        clc
        adc #>(COLOURS - SCREEN_A)
        sta vector + 1
        jsr _cell
        lda #0                  ; off where it was
        sta (dst),y
        sec
        lda t_sx,x
        sbc t_star_v,x
        sta t_sx,x
        lda t_sxh,x
        sbc #0
        bcs +                   ; (C = 0: under 0)
        lda t_sx,x              ; past the left: from the
        adc #<640               ; right, + 640
        sta t_sx,x
        lda #$ff
        adc #>640
+       sta t_sxh,x
        jsr _cell
        lda t_sx,x              ; its pixel: (x / 2) AND 7
        lsr a
        and #%00000111
        clc
        adc #T_STAR0
        sta (dst),y
        lda t_star_c,x
        sta (vector),y
        dex
        bpl _star
        rts
_cell:                          ; Y: x / 16, its cell
        lda t_sxh,x
        sta temp
        lda t_sx,x
        .for c_k in range(4)
        lsr temp
        ror a
        .endfor
        tay
        rts

; The ships: sprites 0-5 (the accent, then the colour
; layer, as the game's ship), their pictures, colours and
; lines; on as they come.
t_ships_on:
        lda #%00101010          ; the colour layers
        sta $d01c
        ldx #SHIP_COUNT - 1     ; X: the ship, its type
-       txa
        asl a
        tay                     ; Y: 2 X, its first sprite
        lda t_ship_block,x
        sta POINTERS_A,y
        ora #1                  ; the colour layer next
        sta POINTERS_A + 1,y
        lda ship_accent,x
        sta $d027,y
        lda ship_own,x
        sta $d028,y
        tya
        asl a
        tay                     ; Y: 4 X, its registers
        lda t_ship_y,x
        sta $d001,y
        sta $d003,y
        dex
        bpl -
        lda #0
        sta t_v
        sta t_v + 1
        rts

; A frame of the V: its x + 1 (0-511); each ship's x, the
; leader's that, the wingmen's SHIP_GAP less; seen from 0
; to SHIP_SHOW - 1, else off.
t_ships:
        inc t_v
        bne +
        lda t_v + 1
        eor #1
        sta t_v + 1
+       lda #0
        sta enable
        sta high
        ldx #SHIP_COUNT - 1
        ldy #4 * (SHIP_COUNT - 1)
_ship:
        sec
        lda t_v
        sbc t_ship_gap,x
        sta temp
        lda t_v + 1
        sbc #0
        bcc _off                ; under 0
        cmp #>SHIP_SHOW
        bcc _on
        bne _off
        lda temp
        cmp #<SHIP_SHOW
        bcs _off
        lda #1
_on:
        lsr a                   ; its ninth bit
        bcc +
        lda t_bits,x
        ora high
        sta high
+       lda temp
        sta $d000,y
        sta $d002,y
        lda t_bits,x
        ora enable
        sta enable
_off:
        dey
        dey
        dey
        dey
        dex
        bpl _ship
        lda high
        sta $d010
        lda enable
        sta $d015
        rts

; The V: the leader the Redux (ship 0), the Phantom above
; and the Titan below behind it, in rows 9-13.
T_V_TOP = 50 + 9 * 8
t_bits:                         ; a ship's two sprites
        .byte %00000011, %00001100, %00110000
t_ship_block:                   ; its first picture (level)
        .byte SPRITE_BLOCK + range(3) * 6
t_ship_gap:
        .byte 0, SHIP_GAP, SHIP_GAP
t_ship_y:
        .byte T_V_TOP + 9, T_V_TOP, T_V_TOP + 19
        .cerror SHIP_COUNT != 3, "the V"
;{}
;|; The module of the start of a game: assembled with the {10-15}
;|; program, carried by the PRG in LEVEL_W1 (data.asm) and {10-15}
;|; moved to TITLE_AT by move_store; phase 1's file brings it {10-15}
;|; again (make_disk.py) after the levels whose files write {10-15}
;|; over it. The program comes here at its start (entry); it {10-15}
;|; runs here, under the KERNAL (out). {10-15}
;|; The module of the start of a game: assembled with the {1-9}
;|; program, carried by the PRG in LEVEL_W1 (data.asm) and {1-9}
;|; moved to TITLE_AT by move_store. The program comes here at {1-9}
;|; its start (entry); it runs here, under the KERNAL (out). {1-9}
;{16}
;{}

; Fire: a game. The VIC-II, the HUD, the sprites, level 1, {16}
; the ship to choose (states.asm), the score from 0 (the {16}
; record stays); the interrupts on, the main loop. {16}
;|; The game's start: the VIC-II, the HUD, the sprites, level {5-15}
;|; 1, the first ship, the score from 0; the interrupts on, {5-15}
;|; the main loop. {5-15}
;|; The game's start: the VIC-II, the HUD, the sprites, level {3-4}
;|; 1, the first ship; the interrupts on, the main loop. {3-4}
;|; The game's start: the VIC-II, the HUD, level 1; the {1-2}
;|; interrupts on, the main loop. {1-2}
game_start:
        lda #0
        sta level
        sta invuln              ; the ship can be {3}
        .if TEST_BUILD != 0      ; hurt; (the test build) no {3}
        sta test_prev           ; keys I, L before {3}
        .fi ; {3}
        sta held ; {16}
        .if RECORD_LEVEL != 0 ; {17}
        lda #RECORD_LEVEL - 1   ; only to record {17}
        sta level ; {17}
        lda #1 ; {17}
        sta invuln ; {17}
        .fi ; {17}
        .if REC_SOUND != 0      ; the recordings: a {17}
        lda #1                  ; ship lost would hold the {17}
        sta invuln              ; game, silent (the choice) {17}
        .fi ; {17}
        jsr init_vic            ; the screen off meanwhile
        jsr draw_hud
        jsr init_sprites ; {3}
        .if RECORD_LEVEL != 0 ; {17}
        jsr init_ship           ; this module's own {17}
        jsr score_shown         ; first: level n's file {17}
        jmp rec_level           ; writes over it (main.asm) {17}
        .fi ; {17}
        jsr init_level          ; with no Varkon, no objects {4}
;|        jsr init_level ; {1-3}
        jsr init_ship ; {3}
        jsr score_shown         ; 0, the best kept {5}
        jsr plan_sprites ; {4}
        jsr update_hud ; {3}
        jsr camera_plan         ; the first turn's camera {2}
        lda sound_mode          ; the music from its start {7}
        jsr sound_set ; {7}
        lda #0
        sta frame_count
        sta frame_flag
        sta turn_wait ; {3}
        jsr init_irq            ; the interrupts on
        jsr screen_on
        .if RECORD_SFX != 0 ; {17}
        jmp sfx_reel ; {17}
        .else ; {17}
        jmp frame_loop
        .fi ; {17}

;{3}
; At the start of a game: the first ship, three of them, in {17}
; the middle of the corridor, held there, to be chosen {17}
; (states.asm; the recordings: flying, blinking). {17}
;|; At the start of a game: the first ship, three of them, in {16-16}
;|; the middle of the corridor, held there, to be chosen {16-16}
;|; (states.asm). {16-16}
;|; At the start of a game: the first ship, three of them, in {3-15}
;|; the middle of the corridor, flying in (come_in). {3-15}
init_ship:
        lda #0
        sta ship_type
        sta prev_keys ; {7}
        ldx #3 ; {4}
-       lda #0 ; {4}
        sta shot_mask,x ; {4}
        lda #$ff                ; no points for the hits {5}
        sta hit_y,x ; {5}
        dex ; {4}
        bpl - ; {4}
        lda #LIVES
        sta ship_lives
        jsr init_weapons        ; the first level, no {6}
                                ; capsules {6}
;|        jsr init_weapons        ; the first level {4-5}
;|        lda ship_speed_lo       ; the first ship's speed {3-3}
;|        sta cur_speed_lo ; {3-3}
;|        lda ship_speed_hi ; {3-3}
;|        sta cur_speed_hi ; {3-3}
        .if RECORDING ; {17}
        lda #START_X ; {17}
        ldx #0 ; {17}
        ldy #CONTROL ; {17}
        jmp come_in ; {17}
        .else ; {17}
        lda #START_X            ; held there, to be {16}
        jmp choose_next         ; chosen {16}
;|        lda #START_X ; {3-15}
;|        ldx #0 ; {3-15}
;|        ldy #CONTROL ; {3-15}
;|        jmp come_in ; {3-15}
        .fi ; {17}
;{}

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


;{3}
; The sprites: the shared colours; no stretching; in front {4}
; of the characters; sprite 1 multicolour (the ship's colour {4}
; layer) until plan_sprites writes $d01c, where they are and {4}
; what they show, every frame. {4}
;|; The sprites: the shared colours; no stretching; in front {3-3}
;|; of the characters; sprite 1 multicolour (the ship's colour {3-3}
;|; layer); all off: the main loop turns the ship's on, where {3-3}
;|; it is, every frame (ship_sprites). {3-3}
init_sprites:
        lda #%00000010
        sta $d01c
        lda #SPRITE_SHARED_1
        sta $d025
        lda #SPRITE_SHARED_2
        sta $d026
        lda #0
        sta $d017               ; no stretching
        sta $d01d
        sta $d01b               ; in front of the characters
        sta $d015               ; all off for now
        ldx #7                  ; all eight: block 0,
-       sta POINTERS_A,x        ; colour 0, place 0
        sta POINTERS_B,x
        sta $d027,x
        dex
        bpl -
        ldx #15
-       sta $d000,x
        dex
        bpl -
        sta $d010
        rts
;{}

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

;{4}
; At the start of a game: the first level, no capsules, no {6}
; missile, no blast; the shots' other bytes (shot_dy, {6}
; shot_bl, shot_pl, shot_ph) 0. {6}
;|; At the start of a game: the first level. {4-5}
init_weapons:
        lda #0 ; {6}
        sta blast_armed ; {6}
        ldx #3 ; {6}
-       sta shot_dy,x ; {6}
        sta shot_bl,x ; {6}
        sta shot_pl,x ; {6}
        sta shot_ph,x ; {6}
        dex ; {6}
        bpl - ; {6}
        lda #0
        sta weapon
        sta s_caps
        sta missiles ; {6}
        sta sat_on ; {6}
        sta m_on ; {6}
        lda #$ff ; {6}
        sta m_hy ; {6}
        jmp set_weapon
;{}

;{7}
; At the program's start: all the sound's variables 0 (the
; copy too, but the volume: 15, no filter; the song 0, the
; theme); the first mode, still silent (the level starts
; it: sound_set).
sound_init:
        lda #0
        ldx #SOUND_ZP_END - mus_frame - 1
-       sta mus_frame,x
        dex
        bpl -
        ldx #SOUND_END - v_list_lo - 1
-       sta v_list_lo,x
        dex
        bpl -
        lda #%00001111          ; volume 15, no filter
        sta sid_shadow + 24
        lda #START_MODE
        sta sound_mode
        rts

        .cerror SOUND_ZP_END - mus_frame > 128
        .cerror SOUND_END - v_list_lo > 128
;{}

;{5}
; A new game: the score from 0, the first ship more at
; EXTRA_EVERY. (At the start the best is 0 too: score_init.)
score_reset:
        lda #0
        sta score
        sta score + 1
        sta score + 2
        lda #EXTRA_EVERY
        sta next_life
        lda #1
        sta score_dirty
        rts

score_init:
        lda #0
        ldx #2
-       sta hi_score,x
        dex
        bpl -
; A game from the title: the HUD drawn again, none of its {16}
; digits shown yet; the score from 0, the best kept (the {16}
; record of the session: the author, 4 November). {16}
;|; A new game: none of the HUD's digits shown yet (update_hud {5-15}
;|; writes them all); the score from 0. {5-15}
score_shown:
        lda #$ff                ; none shown yet
        ldx #2
-       sta shown_score,x
        sta shown_hi,x
        dex
        bpl -
        jmp score_reset
;{}

; (Its data, title.inc, after it: data.asm, SPRITES2.) {16}
TITLE_ALL = TITLE_LEN + TITLE_DATA_LEN ; {16}
;|TITLE_ALL = TITLE_LEN ; {1-15}
