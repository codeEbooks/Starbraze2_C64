; The raster interrupts of a frame.
;  - irq_top, line 20, in the upper border: the screen to
;    show, the near layer's fine scroll, the level's shared
;    colours; it counts the frame.
;  - irq_start, line 70 (FIELD_LINE), then irq_field as {4}
;    often as needed down the playfield: the multiplexer {4}
;    puts the plan's entries from the seventh on onto {4}
;    sprites 2-7, each when its sprite's entry before it has {4}
;    been drawn (acc_trig); in between, the two fixed {4}
;    writes: in row 10 (line 132) the far layer's fine {4}
;    scroll, for rows 10-13, and screen A, whose rows 11-13 {4}
;    are the far layer's in both screens; in row 14 (line {4}
;    164) the near layer's scroll and the screen shown {4}
;    again. Rows 10 and 14 are the same from one end to the {4}
;    other, in both screens: in them the moment of the {4}
;    change does not show. {4}
;|;  - irq_start, line 70 (FIELD_LINE), then irq_field down {1-3}
;|;    the playfield: the two fixed writes. In row 10 (line {1-3}
;|;    132) the far layer's fine scroll, for rows 10-13, and {1-3}
;|;    screen A, whose rows 11-13 are the far layer's in both {1-3}
;|;    screens; in row 14 (line 164) the near layer's scroll {1-3}
;|;    and the screen shown again. Rows 10 and 14 are the same {1-3}
;|;    from one end to the other, in both screens: in them the {1-3}
;|;    moment of the change does not show. {1-3}
;  - irq_hud, line 225: it waits for line 226, the
;    playfield's last, lets the VIC-II finish it and sets
;    the HUD's screen and characters and no fine scroll,
;    in the border, before the VIC-II reads the HUD's first
;    row on line 227; then the HUD's grey. Then it tells
;    the main loop to start.

; The CIA's interrupts off; the KERNAL out (its ROM and its
; interrupts are not used), the vectors in RAM; the
; joystick's port as inputs.
kernal_out:
        lda #%01111111          ; CIA interrupts off
        sta $dc0d               ; CIA 1: IRQ
        sta $dd0d               ; CIA 2: NMI
        lda $dc0d               ; clear what is pending
        lda $dd0d
        lda #$35                ; I/O in; BASIC, KERNAL out
        sta $01
        lda #<irq_top           ; the vectors, now in RAM
        sta $fffe
        lda #>irq_top
        sta $ffff
        lda #<nmi
        sta $fffa
        lda #>nmi
        sta $fffb
        lda #0                  ; CIA 1 port A: all inputs, {3}
        sta $dc02               ; joystick 2 {3}
        rts

; The raster interrupts on.
init_irq:
        lda #TOP_LINE           ; first interrupt: line 20
        sta $d012
        lda $d011
        and #%01111111          ; line bit 8: 0
        sta $d011
        lda #%00000001          ; raster interrupt on
        sta $d01a
        sta $d019               ; clear one pending
        cli
        rts

; RESTORE: nothing happens.
nmi:
        rti

irq_top:
        pha
        lda shown_d018          ; the screen shown
        sta $d018
        lda near_d016           ; the near layer's scroll
        sta $d016
        lda #0                  ; and the level's shared
top_d022 = * - 1                ; colours (load_level
        sta $d022               ; writes them here)
        lda #0
top_d023 = * - 1
        sta $d023
top_set:                        ; the tests look here
        inc frame_count
        #sid_copy                ; the sound of this frame {7}
sound_copied:                   ; the tests look here {7}
        lda #FAR_LINE           ; the field: far first
        sta fixed_line
        #next_irq FIELD_LINE, irq_start

; The field's first interrupt: is the plan of this frame {4}
; made? (The main loop makes it before line 50.) If not, {4}
; none of it is written this frame. The field's next ones {4}
; come to irq_field. {4}
;|; The field's first interrupt; the field's next ones come to {1-3}
;|; irq_field. {1-3}
irq_start:
        sta irq_a
        stx irq_x
        sty irq_y
        cld                     ; (score.asm: SED) {5}
        lda #%00000001          ; done with this one, at
        sta $d019               ; once (field_set)
        lda mux_ready ; {4}
        beq + ; {4}
        lda mux_count ; {4}
+       sta mux_end ; {4}
        lda #<irq_field
        sta $fffe
        lda #>irq_field
        sta $ffff
        jmp field_loop

; The field: the fixed writes and the plan's entries, in the {4}
; order of their lines (a fixed write first); then the next {4}
; interrupt, or the beam is waited for if it is less than {4}
; two lines away. {4}
;|; The field: the fixed writes, in the order of their lines; {1-3}
;|; then the next interrupt, or the beam is waited for if it {1-3}
;|; is less than two lines away. {1-3}
;
; The interrupt is acknowledged ($d019) when it starts, not
; at its end: if the line just written into $d012 is the
; beam's own (a badline and the sprites' fetches can delay
; the write by most of two lines), the VIC-II signals it at
; once, and that signal must not be cleared, or the next
; interrupt would come a frame late. If the beam is already
; past it, at once.
field_fixed:
        lda fixed_line
        cmp #NEAR_LINE
        beq field_near
        lda far_d016            ; row 10: the far layer's
        sta $d016               ; scroll; its rows 11-13
        lda #D018_A             ; always from screen A
        sta $d018
far_set:                        ; the tests look here
        lda #NEAR_LINE
        sta fixed_line
        jmp field_loop
field_near:
        lda near_d016           ; row 14: the near layer's
        sta $d016               ; again, and the screen
        lda shown_d018          ; shown
        sta $d018
near_set:                       ; the tests look here
        lda #$ff                ; no more
        sta fixed_line
        jmp field_loop

irq_field:
        sta irq_a
        stx irq_x
        sty irq_y
        cld ; {5}
        lda #%00000001          ; done with this one, at
        sta $d019               ; once (field_set)
field_loop:
        lda $d012               ; a fixed write due?
        cmp fixed_line
        bcs field_fixed
        ldx mux_next            ; an entry due? {4}
        cpx mux_end ; {4}
        bcs field_none ; {4}
        cmp acc_trig,x ; {4}
        bcs field_entry ; {4}
        lda acc_trig,x          ; the next line: the entry's {4}
        cmp fixed_line          ; or the fixed write's {4}
        bcc field_set ; {4}
field_none:
        lda fixed_line
        cmp #$ff
        bne field_set
        lda #<irq_hud           ; all done: the HUD's next
        sta $fffe
        lda #>irq_hud
        sta $ffff
        ldy #HUD_LINE - 2
        sty $d012
        cpy $d012               ; the beam past it? Then
        bcs field_end           ; at once
        lda irq_a
        ldx irq_x
        ldy irq_y
        jmp irq_hud
field_set:
        tay                     ; A: the line. If the beam
        sec                     ; is on it or a line before,
        sbc $d012               ; at once
        bcc field_loop
        cmp #2
        bcc field_loop
        sty $d012
        cpy $d012               ; the beam past it already
        bcc field_loop          ; (stolen cycles): at once
field_end:
        lda irq_a
        ldx irq_x
        ldy irq_y
        rti
;{4}
field_entry:
        ldy plan_ix,x           ; entry X: its object
        lda obj_xh,y            ; its ninth bit
        eor d010_now
        and entry_bit,x
        eor d010_now
        sta d010_now
        sta $d010
        lda entry_reg,x         ; its place
        tax
        lda obj_y,y
        sta $d001,x
        lda obj_x,y
        sta $d000,x
        ldx mux_next            ; its picture, its colour
        lda entry_sprite,x
        tax
        lda obj_block,y
        sta POINTERS_A,x
        sta POINTERS_B,x
        lda obj_colour,y
        sta $d027,x
mux_written:                    ; the tests look here
        inc mux_next
        jmp field_loop
;{}

        .cerror NEAR_LINE == $ff || FAR_LINE == NEAR_LINE

; The end of the short interrupt, which keeps only A:
; the next one on line \line, at \routine.
next_irq .macro line, routine
        lda #\line
        sta $d012
        lda #<\routine
        sta $fffe
        lda #>\routine
        sta $ffff
        lda #%00000001          ; done with this one
        sta $d019
        pla
        rti
        .endmacro

irq_hud:
        pha
        txa
        pha
        tya
        pha
        lda #HUD_D018
        ldx #HUD_LINE - 1
_wait:
        cpx $d012               ; wait for line 226: 7
        bne _wait               ; cycles a turn
        ldy #11                 ; 56 cycles: to the border
_delay:
        dey
        bne _delay
        sta $d018               ; on cycles 62-68 from 226's
hud_set:                        ; the tests look here
        lda #D016_BASE          ; the HUD does not scroll
        sta $d016
hud_scroll:                     ; and here
        lda #D022_HUD           ; the HUD's grey: its first
        sta $d022               ; line is black, so a late
        lda #D023_HUD           ; write shows nothing
        sta $d023
        lda #0                  ; $d021 for the next frame:
top_d021 = * - 1                ; the level's (load_level)
        sta $d021               ; (white: escape.asm) {15}
;|        sta $d021 ; {1-14}
        lda #0                  ; the plan is used: a new {4}
        sta mux_ready           ; one for the next frame {4}
        lda #1                  ; the main loop may start
        sta frame_flag
        lda #TOP_LINE           ; next: the top one
        sta $d012
        lda #<irq_top
        sta $fffe
        lda #>irq_top
        sta $ffff
        lda #%00000001
        sta $d019
        pla
        tay
        pla
        tax
        pla
        rti
