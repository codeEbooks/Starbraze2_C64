; The station's module: the code phase 3 adds to the
; program, level 5's (VARKON-OMEGA) Varkon of their own.
;
; Assembled by itself at P3_AT ($e000, RAM under the KERNAL,
; after a phase-3 level's store), after the program, whose
; labels it reads (game/build/main.inc); level 5's file
; (LEVEL5) brings it, a record after the store's
; (tools/make_disk.py), as the bosses' files bring theirs at
; WARDEN_AT. The program comes here through the jump at its
; start: move_varkon's, for a Varkon whose behaviour is
; phase 3's (P3_BEH and after: such kinds are only in the
; station's files, with this module).
;
; From P3_MUSIC the station's theme, which takes the theme
; of space's place (song 1) in phase 3 (music.py).
;
; Phase 3's kinds take phase 2's slots in the program's
; tables (the station's file writes its own there, phase 2's
; files write theirs back: build_assets.py, overlays). Here
; three behaviours, for a Varkon on the screen (X, its
; object Y; both kept): its picture into the object; then
; the program's colour and, for a kind with a period, its
; shot (move_varkon, _colour):
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
        jmp st_hang             ; HANG

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

P3_END:
        .cerror P3_END > WARDEN_AT, "the boss's place"
