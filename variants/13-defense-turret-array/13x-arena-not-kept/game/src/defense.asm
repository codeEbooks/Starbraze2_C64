; The DEFENSE TURRET ARRAY, the boss of level 5
; (game/assets/defense.py). The level plan (§2): a wall of
; turrets that closes the hall, in three rows; the rows open
; and fire in turn; the turrets destroyed, the wall's core.
; The author's decisions (26 October): «Una fila alla
; volta», «Ferma», «Un po' più della CORVETTE», «Un raggio
; laser».
;
; Assembled by itself at WARDEN_AT (from $f000, RAM under
; the KERNAL), after the program, whose labels it reads
; (game/build/main.inc); level 5's file (LEVEL5) brings
; it, a record after the store's and the station's module
; (tools/make_disk.py), as level 4's brings the CORVETTE.
; The program comes here through the jumps at its start:
; boss_draw's (the wall), boss_update's (its steps),
; paint's (its colours).
;
; The engine is boss.asm's: the bar, the white flash, the
; wreck, STAGE CLEAR. Here the ARRAY's own:
;  - the wall: 9 columns x 17 rows of characters, columns
;    31-39, rows 2-18 (from the ceiling to the floor). It
;    does not move: in WAIT its characters go into codes
;    the arena does not show (dt_make: their lines into
;    the rock's table too: it is rock), and, no Varkon of
;    the level flying any more, its parts' pictures over
;    the level's first ones; in ENTER it closes in, a row
;    of its cells a turn, from the ceiling and the floor;
;  - rows 10-14 are rock while it is there (as for the
;    WARDEN: rock_row, air_rock; the far layer's codes out
;    of the rock's table): boss_reset puts them back;
;  - its patches: its three bays' cells and the core's
;    (shut, half open, open: dt_want, the step's; drawn a
;    patch a turn, dt_have);
;  - the rows in turn: shut, opening (its two turrets, two
;    free Varkon of kind ATURRET, with the lives they had),
;    open (their fans), shutting again (back in) after
;    DT_OPEN_FRAMES; a row whose turrets are destroyed
;    stays open, the next comes;
;  - the six destroyed: the core's hatch opens, its lens
;    (part_core, ATURRET's partner ACORE) fires aimed
;    shots; every DT_CALM frames (fewer under half its
;    life) it warns (its colours in turn) and fires its
;    ray along rows 10-11, from it to the screen's left
;    edge: the arena's cells under it kept (DT_SAVE) and
;    given back; the ship on its lines loses DT_RAY_HURT
;    notches, as on the rock;
;  - destroyed, the engine's end (boss_dies), its chain on
;    the wall (dt_chain).

        .include "main.inc"     ; (-I its build)
        .include "../assets/generated/defense.inc"

; Its variables, where the SHIELD CORE's are (page 2, 0 at
; the level's start: boss_reset).
dt_gone  = cb_angle             ; the turrets destroyed
dt_part  = dt_gone + 1          ; 6: their Varkon
dt_life  = dt_part + 6          ; 6: their lives kept
dt_live  = dt_life + 6          ; those on, not destroyed
dt_turn  = dt_live + 1          ; the row's place in turn
dt_row   = dt_turn + 1          ; the row (0-2) of the turn
dt_cycle = dt_row + 1           ; 0 shut, 1 opening, 2 open,
                                ; 3 shutting
dt_want  = dt_cycle + 1         ; 4: the patches' states
dt_have  = dt_want + 4          ; 4: drawn
dt_wrows  = dt_have + 4          ; ENTER: its rows wanted,
dt_drawn = dt_wrows + 1          ; drawn
dt_made  = dt_drawn + 1         ; WAIT: its codes, pictures
dt_ray   = dt_made + 1          ; 0 calm, 1 warns, 2 ray
dt_rt    = dt_ray + 1           ; frames left of that
dt_rwant = dt_rt + 1            ; the ray wanted (1), drawn
dt_rhave = dt_rwant + 1
dt_shim  = dt_rhave + 1         ; the ray's picture (0, 1)
dt_mode  = dt_shim + 1          ; its colours: 0 own, 1
                                ; white, 2 the wreck's
dt_k     = dt_mode + 1          ; scratch
dt_t     = dt_k + 1
dt_r     = dt_t + 1
DT_VARS_END = dt_r + 1
        .cerror DT_VARS_END > CB_SAVE_END, "its variables"
        .cerror dt_gone != arena_chars + 1

        * = WARDEN_AT
        jmp dt_draw             ; W_DRAW
        jmp dt_step             ; W_STEP
        jmp dt_paint            ; W_PAINT
        .cerror dt_draw - WARDEN_AT != 9

DT_GROUPS = (DT_CODES + 3) / 4  ; its codes, four a turn
DT_MADE_ALL = DT_GROUPS + DT_PICTURE_BYTES / 64
        .cerror DT_PICTURE_BYTES % 64 != 0
        .cerror (CHARSET | SCREEN_A) & $ff != 0

; ---------------------------------------------------------
; The wall on the screen (boss_draw, a turn): in ENTER a
; row of its cells; else a patch whose state changed; else
; the ray on or off; else, the ray on, its shimmer.
; ---------------------------------------------------------

dt_draw:
        lda boss_state          ; WAIT: nothing yet
        beq _done
        lda dt_drawn            ; a row of the wall
        cmp dt_wrows
        bcs +
        jmp dt_wall_row
+       ldx #DT_PATCHES - 1     ; a patch
-       lda dt_want,x
        cmp dt_have,x
        beq +
        jmp dt_patch
+       dex
        bpl -
        lda dt_rwant            ; the ray
        cmp dt_rhave
        beq +
        jmp dt_ray_draw
+       lda dt_rhave            ; on: every 4 frames the
        beq _done               ; other picture
        lda anim
        and #%00000011
        bne _done
        lda dt_shim
        eor #1
        sta dt_shim
        asl a
        asl a
        asl a
        asl a
        tax
        ldy #0
-       lda dt_rays,x
        sta CHARSET + 8 * DT_RAY_CODE,y
        lda dt_rays + 8,x
        sta CHARSET + 8 * DT_RAY_CODE2,y
        inx
        iny
        cpy #8
        bne -
_done:
        rts

; Row dt_enter[dt_drawn] of the wall: its cells, colours.
dt_wall_row:
        ldx dt_drawn
        inc dt_drawn
        ldy dt_closing,x
        jsr dt_ptrs
        lda dt_row9,y           ; its first cell
        tax
        ldy #0
-       lda dt_wall,x
        sta (src),y
        lda dt_colour,x
        sta (dst),y
        inx
        iny
        cpy #DT_COLS
        bne -
        rts

; Row Y of the wall: src its first cell on screen A, dst
; its colours. Y kept.
dt_ptrs:
        lda row_lo + DT_ROW0,y
        clc
        adc #DT_COL0
        sta src
        sta dst
        lda row_hi + DT_ROW0,y
        adc #0
        sta src + 1
        clc
        adc #>(COLOURS - SCREEN_A)
        sta dst + 1
        rts

        .cerror (COLOURS - SCREEN_A) & $ff != 0

; Patch X in its state wanted: its cells' codes.
dt_patch:
        lda dt_want,x
        sta dt_have,x
        tay
        lda dt_pc_lo,y          ; src: the codes of that
        sta src                 ; state
        lda dt_pc_hi,y
        sta src + 1
        lda dt_p_first + 1,x
        sta dt_t
        ldy dt_p_first,x
-       lda dt_p_lo,y
        sta dst
        lda dt_p_hi,y
        clc
        adc #>SCREEN_A
        sta dst + 1
        lda (src),y
        sty dt_k
        ldy #0
        sta (dst),y
        ldy dt_k
        iny
        cpy dt_t
        bne -
        rts

; The ray on (dt_rwant 1): the cells under it kept, its
; codes and its colour there; off: the cells again.
dt_ray_draw:
        lda dt_rwant
        sta dt_rhave
        beq _off
        ldy #DT_RAY_COLS - 1
-       lda #DT_RAY_CODE
        sta SCREEN_A + RAY_A,y
        lda #DT_RAY_CODE2
        sta SCREEN_A + RAY_B,y
        lda #DT_RAY_OWN
        sta COLOURS + RAY_A,y
        sta COLOURS + RAY_B,y
        dey
        bpl -
        rts
_off:
        ldy #DT_RAY_COLS - 1
-       lda DT_SAVE,y
        sta SCREEN_A + RAY_A,y
        lda DT_SAVE + DT_RAY_COLS,y
        sta SCREEN_A + RAY_B,y
        lda DT_SAVE + 2 * DT_RAY_COLS,y
        sta COLOURS + RAY_A,y
        lda DT_SAVE + 3 * DT_RAY_COLS,y
        sta COLOURS + RAY_B,y
        dey
        bpl -
        rts

RAY_A = 40 * DT_RAY_ROW         ; its rows' first cells
RAY_B = RAY_A + 40

; Its colours (paint, boss.asm): X 0 its own, 1 white, 2
; the wreck's, in all its cells (a row unrolled: the
; chain's turns have little time), from its top row
; down: the beam comes there first (bottom up, a chain's
; turn once wrote row 1 while the beam fetched it).
dt_paint:
        stx dt_mode
        lda #0
        sta dt_r
_row:
        ldy dt_r
        jsr dt_ptrs
        ldx dt_mode
        bne _fixed
        lda dt_row9,y
        tax
        .for dt_l in range(DT_COLS)
        lda dt_colour + dt_l,x
        ldy #dt_l
        sta (dst),y
        .endfor
        jmp _next
_fixed:
        lda dt_paints - 1,x
        ldy #DT_COLS - 1
-       sta (dst),y
        dey
        bpl -
_next:
        inc dt_r
        lda dt_r
        cmp #DT_ROWS
        bcc _row
        rts

dt_paints:
        .byte DT_FLASH_OWN, DT_WRECK_OWN

; ---------------------------------------------------------
; Its turn (boss_update, after the bar's step): its step.
; ---------------------------------------------------------

dt_step:
        lda #<DT_PART_X         ; its parts' places are from
        sta part_x              ; here (and the chain's)
        lda #>DT_PART_X
        sta part_x + 1
        ldx boss_state
        lda dt_steps_lo,x
        sta vector
        lda dt_steps_hi,x
        sta vector + 1
        jmp (vector)

dt_steps_lo:
        .byte <dt_wait, <dt_enter, <dt_fight, <dt_open
        .byte <dt_core, <dt_chain, <step_wreck, <step_clear
        .byte <step_done
dt_steps_hi:
        .byte >dt_wait, >dt_enter, >dt_fight, >dt_open
        .byte >dt_core, >dt_chain, >step_wreck, >step_clear
        .byte >step_done

        .cerror ST_OPEN != 3 || ST_DONE != 8

; Varkon X at part_x + A (its x register): its line set.
place_one_x:
        clc
        adc part_x
        sta en_x,x
        lda part_x + 1
        adc #0
        sta en_xh,x
        lda #0
        sta en_xf,x
        rts

; --- WAIT -------------------------------------------------
; Its codes are made meanwhile, four a turn; when no
; Varkon flies or explodes, its pictures, one a turn; WAIT
; ends when they are made and no Varkon has flown or
; exploded for ARENA_WAIT frames.
dt_wait:
        jsr dt_make_codes
        ldx #ENEMIES - 1        ; a Varkon flying or
-       lda en_on,x             ; exploding: wait for it
        cmp #FLYING
        beq _busy
        cmp #BOOM
        beq _busy
        dex
        bpl -
        jsr dt_picture
        inc boss_timer
        lda boss_timer
        cmp #ARENA_WAIT
        bcc _done
        lda dt_made
        cmp #DT_MADE_ALL
        bcc _done
        jmp dt_begin
_done:
        rts
_busy:
        lda #0
        sta boss_timer
        rts

; Four of its codes (dt_made's group): their lines from
; dt_chars into the characters; into the rock's table the
; wall's (its ray's: none, it is not rock).
dt_make_codes:
        lda dt_made
        cmp #DT_GROUPS
        bcs _done
        asl a
        asl a
        sta dt_k                ; its first code's place
        inc dt_made
        lda #4
        sta dt_t
-       ldx dt_k
        cpx #DT_CODES
        bcs _done
        jsr dt_one_code
        inc dt_k
        dec dt_t
        bne -
_done:
        rts

; Code X of its codes (dt_code, its lines dt_chars + 8 X).
dt_one_code:
        lda #0                  ; src: dt_chars + 8 k
        sta src + 1
        txa
        .rept 3
        asl a
        rol src + 1
        .endrept
        clc
        adc #<dt_chars
        sta src
        lda src + 1
        adc #>dt_chars
        sta src + 1
        lda dt_code,x           ; dst: CHARSET + 8 code
        ldy #0
        sty dst + 1
        .rept 3
        asl a
        rol dst + 1
        .endrept
        sta dst
        lda dst + 1
        clc
        adc #>CHARSET
        sta dst + 1
        cpx #DT_WALL_CODES
        lda dt_code,x
        tax
        bcs _ray
        .for dt_l in range(8)
        lda (src),y
        sta (dst),y
        sta rock_lines + dt_l * 256,x
        iny
        .endfor
        rts
_ray:
        .for dt_l in range(8)
        lda (src),y
        sta (dst),y
        lda #0
        sta rock_lines + dt_l * 256,x
        iny
        .endfor
        rts

; A picture of its parts (dt_made - DT_GROUPS): 64 bytes
; over the level's (its first: no Varkon of the level
; flies in the arena any more).
dt_picture:
        lda dt_made
        cmp #DT_GROUPS
        bcc _done
        cmp #DT_MADE_ALL
        bcs _done
        sec
        sbc #DT_GROUPS
        inc dt_made
        tax
        lda dt_pic_lo,x
        sta src
        lda dt_pic_hi,x
        sta src + 1
        lda dt_spr_lo,x
        sta dst
        lda dt_spr_hi,x
        sta dst + 1
        ldy #63
-       lda (src),y
        sta (dst),y
        dey
        bpl -
_done:
        rts

; WAIT is over: rows 10-14 rock, the far layer's codes not;
; the turrets' lives; the bar; ENTER.
dt_begin:
        ldx #CORRIDOR_TO - CORRIDOR_FROM - 1
-       txa                     ; rows 10-14: their rows
        clc
        adc #CORRIDOR_FROM
        lsr a
        lsr a
        lsr a
        sta rock_row + CORRIDOR_FROM,x
        dex
        bpl -
        lda #1
        sta air_rock
        ldx #DT_FAR_COUNT - 1   ; the far layer's codes: not
        lda #0                  ; rock
-       ldy dt_far,x
        .for dt_l in range(8)
        sta rock_lines + dt_l * 256,y
        .endfor
        dex
        bpl -
        ldx #2 * DT_TIERS - 1   ; the turrets' lives
        lda #DT_TURRET_LIFE
-       sta dt_life,x
        dex
        bpl -
        lda #0
        sta boss_timer
        sta parts
        sta dt_mode
        lda #$ff
        sta part_core
        jsr bar_on
        lda #ST_ENTER
        sta boss_state
        rts

        .cerror CORRIDOR_FROM & 7 != 0, "its lines"
        .cerror CORRIDOR_TO - CORRIDOR_FROM > 128

; --- ENTER: it closes in ---------------------------------
; A row more every DT_ENTER_EVERY frames (drawn in the next
; turn); all drawn, its sound, the fight: the first row
; opens after DT_SHUT_WAIT frames.
dt_enter:
        lda dt_wrows
        cmp #DT_ROWS
        bcs _all
        inc boss_timer
        lda boss_timer
        cmp #DT_ENTER_EVERY
        bcc _done
        lda #0
        sta boss_timer
        inc dt_wrows
_done:
        rts
_all:
        lda dt_drawn
        cmp #DT_ROWS
        bcc _done
        lda #FX_BOOM
        jsr sfx_start
        lda #0
        sta dt_turn
        sta dt_cycle
        lda dt_tier
        sta dt_row
        lda #DT_SHUT_WAIT
        sta boss_timer
        lda #ST_FIGHT
        sta boss_state
        jmp dt_bar

; --- FIGHT: the rows in turn -----------------------------
; Shut: DT_SHUT_WAIT frames, then its shutters half open,
; DT_ANIM frames, then open: its turrets left in free
; Varkon (not enough: a frame later), their lives as they
; were. Open: their fans; destroyed, out of the turn; both
; destroyed, the row stays open and the next comes; after
; DT_OPEN_FRAMES, back in, the shutters half shut, shut.
; All six destroyed: the core's step (OPEN).
dt_fight:
        lda dt_cycle
        cmp #2
        beq _open
        dec boss_timer
        bne _bar
        lda dt_cycle
        bne +
        lda #1                  ; shut: half open
        ldx dt_row
        sta dt_want,x
        sta dt_cycle
        lda #DT_ANIM
        sta boss_timer
_bar:
        jmp dt_bar
+       cmp #1
        bne _shut
        jsr dt_row_on           ; opening: its turrets
        bcc +
        inc boss_timer          ; (not enough: a frame
        bne _bar                ; later)
+       lda #2
        ldx dt_row
        sta dt_want,x
        sta dt_cycle
        lda #DT_OPEN_FRAMES
        sta boss_timer
        lda parts
        ora #%00000001
        sta parts
        jmp dt_bar
_shut:
        lda #0                  ; shutting: shut
        ldx dt_row
        sta dt_want,x
        jsr dt_next
        jmp dt_bar
_open:
        jsr dt_turrets
        lda dt_gone
        cmp #%00111111
        bne +
        lda #ST_OPEN            ; all six: the core
        sta boss_state
        lda #DT_CORE_WAIT
        sta boss_timer
        lda #0
        sta dt_cycle
        sta parts
        jmp dt_bar
+       ldx dt_row              ; this row's both: the next
        lda dt_gone
        and dt_row_bits,x
        cmp dt_row_bits,x
        bne +
        lda parts
        and #%11111110
        sta parts
        jsr dt_next
        jmp dt_bar
+       jsr dt_fans
        dec boss_timer
        bne _bar
        ldy #2 * DT_TIERS - 1   ; its time: back in
-       lda dt_live
        and dt_bit,y
        beq +
        ldx dt_part,y
        lda #0
        sta en_on,x
+       dey
        bpl -
        lda #0
        sta dt_live
        lda parts
        and #%11111110
        sta parts
        lda #1                  ; half shut
        ldx dt_row
        sta dt_want,x
        lda #3
        sta dt_cycle
        lda #DT_ANIM
        sta boss_timer
        jmp dt_bar

; The next row with turrets left (this one again, if it
; is the last): shut, DT_SHUT_WAIT frames.
dt_next:
        ldy dt_turn
-       iny
        cpy #DT_TIERS
        bcc +
        ldy #0
+       ldx dt_tier,y
        lda dt_gone
        and dt_row_bits,x
        cmp dt_row_bits,x
        beq -
        sty dt_turn
        stx dt_row
        lda #0
        sta dt_cycle
        lda #DT_SHUT_WAIT
        sta boss_timer
        rts

; The row's turrets not destroyed in free Varkon (C = 0),
; their lives as they were, their first fans; not enough
; free Varkon: none, C = 1.
dt_row_on:
        lda dt_row              ; its first turret
        asl a
        sta dt_r
        ldy #0                  ; how many wanted
        ldx dt_r
        lda dt_gone
        and dt_bit,x
        bne +
        iny
+       lda dt_gone
        and dt_bit + 1,x
        bne +
        iny
+       sty dt_t
        ldy #0                  ; how many free
        ldx #ENEMIES - 1
-       lda en_on,x
        bne +
        iny
+       dex
        bpl -
        cpy dt_t
        bcc _none
        ldy dt_r
        jsr _one
        ldy dt_r
        iny
        jsr _one
        clc
        rts
_none:
        sec
        rts
_one:
        lda dt_gone             ; turret Y, if not destroyed
        and dt_bit,y
        bne _done
        sty dt_k
        jsr free_varkon
        txa
        ldy dt_k
        sta dt_part,y
        lda dt_live
        ora dt_bit,y
        sta dt_live
        ldy #KIND_ATURRET
        jsr new_part
        ldy dt_k
        lda dt_life,y
        sta en_life,x
        lda #0
        sta en_aim,x
        lda dt_fan_first,y
        sta en_fire,x
        lda dt_turret_y,y
        sta en_y,x
        lda dt_turret_dx,y
        jmp place_one_x
_done:
        rts

        .cerror ENEMIES < 2, "two turrets"

; The turrets destroyed this frame (their Varkon not
; flying: exploding) into dt_gone, out of dt_live, their
; life 0; the others' lives kept.
dt_turrets:
        ldy #2 * DT_TIERS - 1
_one:
        lda dt_live
        and dt_bit,y
        beq _next
        ldx dt_part,y
        lda en_on,x
        cmp #FLYING
        beq _alive
        lda dt_gone
        ora dt_bit,y
        sta dt_gone
        lda dt_live
        eor dt_bit,y
        sta dt_live
        lda #0
        sta dt_life,y
        beq _next
_alive:
        lda en_life,x
        sta dt_life,y
_next:
        dey
        bpl _one
        rts

; Each turret on: its fan when its time comes.
dt_fans:
        ldy #2 * DT_TIERS - 1
_one:
        lda dt_live
        and dt_bit,y
        beq _next
        sty dt_k
        ldx dt_part,y
        dec en_fire,x
        bne +
        jsr dt_fan
+       ldy dt_k
_next:
        dey
        bpl _one
        rts

; Turret X's fan: aimed up at the ship above it (the SHIELD
; CORE's low pod's fans), else down or left (the top
; pod's); DT_FAN_PERIOD frames to the next. X kept.
dt_fan:
        jsr aim_one
        ldy #POD_FAN_FIRST
        lda en_aim,x
        bne +
        jsr aim_top
        ldy #POD_FAN_FIRST + 9
+       jsr fan_pod
        lda #DT_FAN_PERIOD
        sta en_fire,x
        rts

; --- OPEN: the turrets gone, the core's hatch ------------
; DT_CORE_WAIT frames, the hatch half open; DT_ANIM, open;
; DT_ANIM, the lens in a free Varkon (none: a frame later):
; its first shot, the calm; the core's fight.
dt_open:
        dec boss_timer
        bne _bar
        lda dt_cycle
        cmp #2
        beq _lens
        inc dt_cycle            ; the hatch: half, open
        lda dt_cycle
        sta dt_want + 3
        lda #DT_ANIM
        sta boss_timer
_bar:
        jmp dt_bar
_lens:
        jsr free_varkon
        bcc +
        inc boss_timer
        bne _bar
+       stx part_core
        ldy #KIND_ACORE
        jsr new_part
        lda #DT_CORE_FIRST
        sta en_fire,x
        lda #DT_LENS_Y
        sta en_y,x
        lda #DT_LENS_DX
        jsr place_one_x
        lda parts
        ora #%00000100
        sta parts
        lda #0
        sta dt_ray
        lda #DT_CALM
        sta dt_rt
        lda #ST_CORE
        sta boss_state
        jmp dt_bar

        .cerror DT_PATCHES != 4, "the core's patch: 3"

; --- CORE: the lens's fight ------------------------------
; Calm (its aimed shots: the kind's period) DT_CALM frames
; (under DT_RAGE_LIFE, DT_CALM_RAGE); it warns DT_WARN
; frames (its colours in turn, no shot); its ray
; DT_RAY_FRAMES frames (no shot; the ship on its lines:
; hurt); the calm again. Destroyed: the ray off, the end
; (the engine's boss_dies, then dt_chain).
dt_core:
        ldx part_core
        lda en_on,x
        cmp #FLYING
        beq +
        lda #0
        sta dt_rwant
        sta dt_ray
        jmp boss_dies
+       lda dt_ray
        bne _warns
        dec dt_rt               ; calm
        bne _bar
        lda #1                  ; it warns
        sta dt_ray
        lda #DT_WARN
        sta dt_rt
        lda #FX_PLASMA
        jsr sfx_start
        ldx part_core
_warns:
        lda #2                  ; no shot meanwhile
        sta en_fire,x
        lda dt_ray
        cmp #2
        beq _ray
        lda dt_rt               ; its colours in turn
        lsr a
        lsr a
        and #%00000001
        tay
        lda dt_warn_own,y
        sta en_colour,x
        dec dt_rt
        bne _bar
        lda #2                  ; its ray
        sta dt_ray
        lda #1
        sta dt_rwant
        sta en_colour,x         ; (white)
        lda #DT_RAY_FRAMES
        sta dt_rt
        lda #FX_LASER
        jsr sfx_start
_bar:
        jmp dt_bar
_ray:
        jsr dt_burn
        ldx part_core
        dec dt_rt
        bne _bar
        lda #0                  ; the calm again
        sta dt_rwant
        sta dt_ray
        lda #DT_LENS_OWN
        sta en_colour,x
        lda #DT_CORE_FIRST
        sta en_fire,x
        lda #DT_CALM
        ldy en_life,x
        cpy #DT_RAGE_LIFE + 1
        bcs +
        lda #DT_CALM_RAGE
+       sta dt_rt
        jmp dt_bar

; The ray drawn, the ship flying (not blinking: sb_on) and
; its box (against the Varkon: sb_top, sb_bottom, y
; registers) on the ray's lines: DT_RAY_HURT notches.
dt_burn:
        lda dt_rhave
        beq _no
        lda sb_on
        beq _no
        lda sb_top
        cmp #DT_RAY_BOTTOM
        bcs _no
        lda sb_bottom
        cmp #DT_RAY_TOP + 1
        bcc _no
        lda #DT_RAY_HURT
        jmp hurt
_no:
        rts

; The bar's steps by the life left: the turrets' (0 the
; ones destroyed, the kept life of the others), the lens's
; (all of it before it comes).
dt_bar:
        lda #0
        sta dt_t
        ldy #2 * DT_TIERS - 1
_one:
        lda dt_gone
        and dt_bit,y
        bne _next
        lda dt_live
        and dt_bit,y
        bne _on
        lda dt_life,y
        bpl _add
_on:
        ldx dt_part,y
        lda en_life,x
_add:
        clc
        adc dt_t
        sta dt_t
_next:
        dey
        bpl _one
        lda #DT_CORE_LIFE
        ldx part_core
        cpx #$ff
        beq +
        lda en_life,x
+       clc
        adc dt_t
        tax
        lda dt_bar_of,x
        sta bar_want
        rts

        .cerror 6 * DT_TURRET_LIFE + DT_CORE_LIFE > 255
        .cerror DT_TURRET_LIFE > 127

; --- CHAIN: as the engine's step_chain, on the wall -------
; Every CHAIN_EVERY frames a fireball (a free Varkon
; exploding; none free: none) at dt_chain_dx from part_x,
; on line dt_chain_y; its sound, the wall white for a
; moment.
dt_chain:
        inc boss_timer
        lda boss_timer
        cmp #CHAIN_EVERY
        bcc _done
        lda #0
        sta boss_timer
        jsr free_varkon
        bcs _next
        lda #2
        jsr set_pri
        lda #BOOM
        sta en_on,x
        lda #KIND_ACORE
        sta en_kind,x
        lda #BOSS
        sta en_beh,x
        lda #0
        sta en_left,x
        sta en_flash,x
        sta en_cap,x
        ldy chain_k
        lda dt_chain_y,y
        sta en_y,x
        lda dt_chain_dx,y
        jsr place_one_x
_next:
        lda #FX_EXPLODE
        jsr sfx_start
        lda #3
        sta flash_left
        ldx #1
        jsr paint
        inc chain_k
        lda chain_k
        cmp #CHAIN_COUNT
        bcc _done
        lda #ST_WRECK
        sta boss_state
_done:
        rts

; ---------------------------------------------------------
; Its tables, its data (game/assets/build_assets.py).
; ---------------------------------------------------------

dt_row9:                        ; a row's first cell
        .for dt_l in range(DT_ROWS)
        .byte dt_l * DT_COLS
        .endfor
dt_pc_lo:                       ; the patches' codes by
        .byte <dt_p_code0, <dt_p_code1, <dt_p_code2
dt_pc_hi:                       ; state
        .byte >dt_p_code0, >dt_p_code1, >dt_p_code2
dt_pic_lo:                      ; its pictures: from, to
        .for dt_l in range(DT_PICTURE_BYTES / 64)
        .byte <(dt_pictures + 64 * dt_l)
        .endfor
dt_pic_hi:
        .for dt_l in range(DT_PICTURE_BYTES / 64)
        .byte >(dt_pictures + 64 * dt_l)
        .endfor
dt_spr_lo:
        .for dt_l in range(DT_PICTURE_BYTES / 64)
        .byte <(DT_SPRITES + 64 * dt_l)
        .endfor
dt_spr_hi:
        .for dt_l in range(DT_PICTURE_BYTES / 64)
        .byte >(DT_SPRITES + 64 * dt_l)
        .endfor
        .cerror DT_ROWS * DT_COLS > 256 || DT_PCELLS > 256
        .cerror DT_CODES * 8 > 1024

        .include "../assets/generated/defense_data.inc"
DT_END:                         ; the file's end
        .cerror DT_END > $fffa, "the ARRAY past $fffa"
        .cerror DT_SAVE + 4 * DT_RAY_COLS > WARDEN_AT
