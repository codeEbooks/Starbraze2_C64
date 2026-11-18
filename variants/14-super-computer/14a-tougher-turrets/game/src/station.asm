; The station's module: the code phase 3 adds to the
; program, level 5's (VARKON-OMEGA) Varkon of their own;
; level 6's (THE CORE).
;
; Assembled by itself at P3_AT ($e000, RAM under the KERNAL,
; after a phase-3 level's store), after the program, whose
; labels it reads (game/build/main.inc); level 5's file
; (LEVEL5) brings it, a record after the store's
; (tools/make_disk.py), as the bosses' files bring theirs at
; WARDEN_AT; level 6's file (LEVEL6) brings it too. The
; program comes here through the jump at its start:
; move_varkon's, for a Varkon whose behaviour is phase 3's
; (P3_BEH and after: such kinds are only in the station's
; files, with this module).
;
; From P3_MUSIC the station's theme, which takes the theme
; of space's place (song 1) in phase 3 (music.py).
;
; Phase 3's kinds take phase 2's slots in the program's
; tables (the station's file writes its own there, phase 2's
; files write theirs back: build_assets.py, overlays; level
; 6's file its own set, table set 4). Here six behaviours
; (GUARD, EGG and BAR further on), for a Varkon on the
; screen (X, its object Y; both kept): its picture into the
; object; then the program's colour and, for a kind with a
; period, its shot (move_varkon, _colour):
;  - CRAWL, a crawler on the floor or under the ceiling: it
;    runs along it to the left, CRAWL_VX against the rock
;    (the program moves it with the rock); its pictures by
;    the frame (its tracks); it fires at its kind's period,
;    its kind's shot (up on the floor, down on the ceiling);
;  - LMINE, the laser mine, anchored: its pictures by the
;    frame (its lens); rested (LMINE_REST frames after a
;    ray), the ship flying, the ship's line within
;    LMINE_BAND of its own and the ship ahead of it (its x
;    register to the left of the mine's): its ray, three
;    bolts (its kind's fan: fire_plasma);
;  - HANG, a turret on the ceiling: it aims as a turret
;    (aim: down-left, down, down-right), its picture by its
;    aim; every HANG_PERIOD frames (the first HANG_FIRST
;    after it comes) a shot that way (its kind's fan's
;    entries are its aims': kind_fan + en_aim).

        .include "main.inc"     ; (-I its build)

        * = P3_AT
        jmp st_part             ; P3_PART
        .cerror * != P3_BEAMS, "P3_BEAMS"
        jmp st_beams            ; P3_BEAMS
        .fill P3_MUSIC - *, 0   ; (room for jumps to come)

; Phase 3's song 1, the station's theme (station_theme.py,
; music.py): its patterns and its order lists, where its
; files make the program's tables point (overlays).
        .include "../assets/generated/station_music.asm"

; A Varkon of phase 3 on the screen (X, its object Y).
st_part:
        lda en_beh,x
        cmp #CRAWL
        beq st_crawl
        cmp #LMINE
        beq st_lmine
        cmp #GUARD              ; level 6's: the
        bcs st_six              ; guardian, the egg, the bar
        jmp st_hang             ; HANG
st_six:
        bne +
        jmp st_guard            ; GUARD
+       cmp #EGG
        bne +
        jmp st_egg              ; EGG
+       jmp st_bar              ; BAR

; The crawler: CRAWL_VX against the rock (24 bits, signed),
; its picture by the frame.
st_crawl:
        clc
        lda en_xf,x
        adc #<CRAWL_VX
        sta en_xf,x
        lda en_x,x
        adc #>CRAWL_VX
        sta en_x,x
        lda en_xh,x
        adc #$ff                ; (CRAWL_VX < 0)
        sta en_xh,x
        .cerror CRAWL_VX < $8000, "CRAWL_VX: to the left"
st_frame:
        lda anim3               ; its picture by the frame
        and en_pmask,x
        clc
        adc en_block,x
        sta obj_block,y
        rts

; The laser mine: its picture by the frame; rested, the ship
; on its line ahead of it: its ray.
st_lmine:
        jsr st_frame
        lda en_fire,x           ; resting after a ray
        beq +
        dec en_fire,x
        rts
+       lda ship_mode           ; the ship flies?
        bne _no
        lda ship_y              ; |its line - the mine's|
        sec
        sbc en_y,x
        bcs +
        eor #$ff
        adc #1                  ; (C = 0)
+       cmp #LMINE_BAND + 1
        bcs _no
        lda ship_x              ; its x register (+ 24)
        clc                     ; to the left of the mine's
        adc #24
        sta v_tmp
        lda ship_xh
        adc #0
        sta v_tmp + 1
        lda v_tmp
        cmp en_x,x
        lda v_tmp + 1
        sbc en_xh,x
        bvc +
        eor #$80
+       bpl _no                 ; (signed: not less)
        lda #LMINE_REST
        sta en_fire,x
        stx v_i
        sty v_j
        jsr fire_plasma         ; its fan: the ray
        ldx v_i
        ldy v_j
_no:
        rts

; The turret on the ceiling: its aim, its picture; its own
; period.
st_hang:
        jsr aim                 ; en_aim: 0, 1, 2 (X kept)
        lda en_aim,x
        clc
        adc en_block,x
        sta obj_block,y
        lda en_fire,x           ; its first frame: the first
        bne +                   ; shot HANG_FIRST later
        lda #HANG_FIRST
        sta en_fire,x
+       dec en_fire,x
        bne _no
        lda #HANG_PERIOD
        sta en_fire,x
        stx v_i
        sty v_j
        ldy en_kind,x           ; its aim's entry: its
        lda kind_fan,y          ; kind's fan's first + aim
        clc
        adc en_aim,x
        sta f_entry
        jsr fire_entry
        ldx v_i
        ldy v_j
_no:
        rts

;  - GUARD, the core's guardian: it comes in
;    (GUARD_IN_VX on the screen), stops at GUARD_STOP_X and
;    follows the ship's line; shut GUARD_SHUT frames (its
;    shell: its life aside, GUARD_SHELL meanwhile), open
;    GUARD_OPEN (its life back, its kind's fan at once);
;    GUARD_TIMES times, then it leaves (GUARD_OUT_VX). Its
;    state in en_vyl (0 new, 1 coming in, 2 shut, 3 open,
;    4 leaving: a Varkon on the rock does not use its y
;    velocity), its frames in en_vyh, its life aside in
;    en_aim, its openings left in en_seg; its x velocity
;    against the rock (en_vx*, added by move_varkon) the
;    camera's speed less its own on the screen;
;  - EGG, a drone's egg: its glow by the frame; the ship
;    flying, its x register less than EGG_NEAR pixels to
;    the left of the egg's (or to its right): it hatches, a
;    drone (new_part) on its path out of it, up from the
;    floor, down from the ceiling;
;  - BAR, a barrier's middle piece (rows 10-14 are never
;    rock), with the barriers' cycle (by anim: the gap
;    above, in the middle, below, in the middle, 64 frames
;    each; a piece about to come on dimmed 16 frames):
;    on, its sparks, never destroyed (its life back every
;    frame, no flash), it pushes the ship back as a field
;    (field_touch); dimmed, its threads at its line, its
;    own line away (BAR_AWAY: never met); off, not shown.
;    The energy above and below with the same cycle:
;    st_beams (P3_BEAMS), from the engine's beam_step.

st_guard:
        lda en_vyl,x            ; new: its life aside
        bne +
        lda en_life,x
        sta en_aim,x
        lda #GUARD_TIMES
        sta en_seg,x
        lda #1
        sta en_vyl,x
+       cmp #3
        beq _open
        lda #GUARD_SHELL        ; shut: its shell, no flash
        sta en_life,x
        lda #0
        sta en_flash,x
        lda en_vyl,x
        cmp #2
        beq _shut
        bcc _coming
        lda #<GUARD_OUT_VX      ; leaving
        sta v_tmp
        lda #>GUARD_OUT_VX
        sta v_tmp + 1
        jsr st_drift
        jmp _shut_pic
_coming:
        lda #<GUARD_IN_VX
        sta v_tmp
        lda #>GUARD_IN_VX
        sta v_tmp + 1
        jsr st_drift
        lda en_xh,x             ; at its place?
        bne _shut_pic
        lda en_x,x
        cmp #GUARD_STOP_X + 1
        bcs _shut_pic
        lda #2                  ; it stops, shut
        sta en_vyl,x
        lda #GUARD_SHUT
        sta en_vyh,x
        bne _shut_pic
_shut:
        jsr st_stand
        dec en_vyh,x
        bne _shut_pic
        lda #3                  ; it opens: its life back,
        sta en_vyl,x            ; its fan
        lda #GUARD_OPEN
        sta en_vyh,x
        lda en_aim,x
        sta en_life,x
        stx v_i
        sty v_j
        jsr fire_plasma         ; (its kind's fan: three)
        ldx v_i
        ldy v_j
        jmp _open_pic
_open:
        jsr st_stand
        dec en_vyh,x
        bne _open_pic
        lda en_life,x           ; it shuts: its life aside
        sta en_aim,x
        lda #GUARD_SHELL
        sta en_life,x
        lda #GUARD_SHUT
        sta en_vyh,x
        lda #2
        dec en_seg,x            ; openings left: none, it
        bne +                   ; leaves
        lda #4
+       sta en_vyl,x
_shut_pic:
        lda en_block,x
        sta obj_block,y
        rts
_open_pic:
        lda en_block,x
        clc
        adc #1
        sta obj_block,y
        rts

; Varkon X still on the screen (its x velocity the camera's
; speed); its line a line nearer the ship's every other
; frame, within GUARD_TOP-GUARD_LOW.
st_stand:
        lda #0
        sta v_tmp
        sta v_tmp + 1
        jsr st_drift
        lda anim
        and #%00000001
        bne _done
        lda en_y,x
        cmp ship_y
        beq _done
        bcs _up
        cmp #GUARD_LOW
        bcs _done
        inc en_y,x
        rts
_up:
        cmp #GUARD_TOP + 1
        bcc _done
        dec en_y,x
_done:
        rts

; Varkon X's x velocity against the rock: the camera's speed
; less v_tmp (256ths a frame to the left on the screen).
st_drift:
        sec
        lda speed
        sbc v_tmp
        sta en_vxl,x
        lda speed + 1
        sbc v_tmp + 1
        sta en_vxh,x
        lda #0                  ; its sign
        bcs +
        lda #$ff
+       sta en_vxs,x
        rts

; The egg: its glow; the ship near, a drone out of it.
st_egg:
        jsr st_frame
        lda ship_mode           ; the ship flies?
        bne _no
        lda ship_x              ; its x register + EGG_NEAR
        clc
        adc #24 + EGG_NEAR
        sta v_tmp
        lda ship_xh
        adc #0
        sta v_tmp + 1
        lda v_tmp               ; still to the left of the
        cmp en_x,x              ; egg's? far yet
        lda v_tmp + 1
        sbc en_xh,x
        bvc +
        eor #$80
+       bmi _no                 ; (signed: less)
        stx v_i
        sty v_j
        lda en_y,x              ; on the floor up, under the
        cmp #88                 ; ceiling down
        lda #PATH_EMERGE_UP
        bcs +
        lda #PATH_EMERGE_DOWN
+       pha
        ldy #KIND_DRONE
        jsr new_part            ; a drone (X kept)
        pla
        sta en_seg,x
        jsr load_stretch
        lda en_period,x         ; its first shot
        lsr a
        ora #1
        sta en_fire,x
        ldx v_i
        ldy v_j
_no:
        rts

; The barrier's piece (X, its object Y): its look by the
; cycle's sixteenth.
st_bar:
        lda en_vyl,x            ; new: its line in en_aim
        bne +
        lda en_y,x
        sta en_aim,x
        lda #1
        sta en_vyl,x
+       sty v_j
        lda anim                ; the cycle's sixteenth
        lsr a
        lsr a
        lsr a
        lsr a
        tay
        lda cycle_mid,y
        ldy v_j
        cmp #2
        beq _on
        pha
        lda #BAR_AWAY           ; dimmed or off: not met
        sta en_y,x
        pla
        bne _dim
        lda #NONE               ; off: not shown
        sta obj_y,y
        bne _kept               ; (NONE: not 0)
_dim:
        lda anim3               ; its threads at its line
        and #%00000001
        ora #%00000010
        clc
        adc en_block,x
        sta obj_block,y
        lda en_aim,x
        clc
        adc #50
        sta obj_y,y
_kept:
        lda #BARRIER_LIFE       ; never destroyed, no flash
        sta en_life,x
        lda #0
        sta en_flash,x
        rts
_on:
        lda en_aim,x            ; on: its line, its sparks
        sta en_y,x
        clc
        adc #50
        sta obj_y,y
        lda anim3
        and #%00000001
        clc
        adc en_block,x
        sta obj_block,y
        lda #BARRIER_LIFE
        sta en_life,x
        lda #0
        sta en_flash,x
        jmp field_touch

; Level 6's beams (beam_step, for a level whose
; beam_module is not 0): the energy above and below the
; corridor (the level's codes BAR_TOP and BAR_LOW) with the
; barriers' cycle, written when it changes (beam_timer
; keeps what was written: 127 at the level's start). None
; in the arena (STAGE CLEAR's letters may take the codes).
st_beams:
        lda arena
        bne _done
        lda anim                ; the cycle's sixteenth
        lsr a
        lsr a
        lsr a
        lsr a
        tay
        lda cycle_low,y         ; the looks: below x 4 +
        asl a                   ; above
        asl a
        ora cycle_top,y
        cmp beam_timer          ; as written?
        beq _done
        sta beam_timer
        lda cycle_low,y
        pha
        lda cycle_top,y
        tay
        ldx #BAR_TOP
        jsr set_beam            ; (beams.asm)
        pla
        tay
        ldx #BAR_LOW
        jmp set_beam
_done:
        rts

; The barriers' cycle (varkon.py, BAR_*_LOOKS).
        .include "../assets/generated/bar_looks.inc"

        .cerror EGG_NEAR + 24 > 255 || GUARD_STOP_X > 255
        .cerror GUARD_TIMES == 0 || GUARD_SHELL < 128
        .cerror NONE == 0 || BAR_AWAY + 50 < 230

P3_END:
        .cerror P3_END > WARDEN_AT, "the boss's place"
        .cerror P3_END > SC_AT, "the SUPER-COMPUTER"
