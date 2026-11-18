; ---------------------------------------------------------
; The files from the disk: phase 1's, then a file a level
; ---------------------------------------------------------

; The game is three phases of two levels: the planet, deep
; space, the station. The PRG brings phase 1's store (its
; packed levels, the SHIELD CORE's tail); the disk holds the
; game's files (phases.py): PHASE1 (levels 1 and 2), then
; LEVEL3 to LEVEL5 (a level and its boss each). A file is
; read with the KERNAL's own routines at the start of a
; level whose file is not in the store, over the one before:
; from level 2 to level 3 LEVEL3, then LEVEL4, LEVEL5; back
; to level 1 (after level 5, the key L) PHASE1 again. The
; loading screen is in the HUD's hole (phase_show.asm).
; A file: its mark "SB", its number, the bytes of a cell of
; the bar; records (an address, a count, the bytes) until a
; count 0; a sum: all its bytes add up to 0 (mod 256).

; The KERNAL's routines, and the few variables of its own
; they need: the game has all the rest of pages 0, 2 and 3.
K_SETLFS  = $ffba
K_SETNAM  = $ffbd
K_OPEN    = $ffc0
K_CLOSE   = $ffc3
K_CHKIN   = $ffc6
K_CLRCHN  = $ffcc
K_CHRIN   = $ffcf
K_READST  = $ffb7
K_RESTOR  = $ff8a
K_STATUS  = $90                 ; the bus's last status
K_C3PO    = $94                 ; a byte kept for the bus
K_LDTND   = $98                 ; the files open
K_DFLTN   = $99                 ; input from (0: keys)
K_DFLTO   = $9a                 ; output to (3: screen)
K_MSGFLG  = $9d                 ; its messages
K_ENABL   = $02a1               ; RS-232 at work
K_NMI     = $0318               ; RESTORE's vector
PH_FILE   = 2                   ; the file: its number and
                                ; its channel on the drive
PH_SAVE   = rock_lines          ; pages 0, 2, 3 meanwhile
                                ; (made again: load_level)
PH_PTR    = src                 ; where the next byte goes
PH_COUNT  = dst                 ; (the KERNAL: not $fb-$fe)

; The level's file in the store: when it is not there, from
; the disk (restart_level: the screen off, the level drawn
; after).
file_need:
        ldx level
        lda level_file,x
        cmp file_now
        beq +
        jsr load_file
+       rts

                                ; the files' names
                                ; (level_file: hole.asm)
        .include "../assets/generated/phase_names.inc"

; File A from the disk: the interrupts stopped, the SID
; silent, the loading screen; the file read until it comes
; whole and right, INSERT THE DISK a while in between; then
; the screen off and the interrupts from the top again.
load_file:
        sta ph_want
        sei
        lda #0
        sta $d01a               ; no raster interrupt
        sta $d418               ; the SID silent
        lda #%00001111          ; none pending
        sta $d019
        jsr phase_screen
_try:
        jsr file_read           ; C = 1: not read
        bcc _read
        ldy #<ph_insert         ; INSERT THE DISK, a while
        lda #>ph_insert
        jsr ph_words
        jsr ph_pause
        jsr ph_reset            ; then LOADING again
        jmp _try
_read:
        lda ph_want
        sta file_now
        jsr screen_off
        lda #<irq_top           ; the interrupts from the
        sta $fffe               ; top, as at the start
        lda #>irq_top
        sta $ffff
        jmp init_irq

; File ph_want read and its records put where they go, the
; game's pages 0, 2 and 3 aside meanwhile (the KERNAL works
; there): C = 0; C = 1 when the disk did not give it whole
; and right.
file_read:
        ldx #0                  ; the game's pages aside
-       lda $00,x
        sta PH_SAVE,x
        lda $0200,x
        sta PH_SAVE + $100,x
        lda $0300,x
        sta PH_SAVE + $200,x
        inx
        bne -
        lda #0                  ; the KERNAL's own: no file
        sta K_STATUS            ; open, no byte kept, input
        sta K_C3PO              ; from the keys, none of its
        sta K_LDTND             ; messages, no RS-232
        sta K_DFLTN
        sta K_MSGFLG
        sta K_ENABL
        lda #3                  ; output to the screen
        sta K_DFLTO
        lda #$36                ; the KERNAL in, the I/O in,
        sta $01                 ; BASIC out
        jsr K_RESTOR            ; its vectors in page 3
        lda #<nmi               ; RESTORE: nothing
        sta K_NMI
        lda #>nmi
        sta K_NMI + 1
        jsr ph_read_file        ; C = 1: not read
        php
        jsr K_CLRCHN            ; the drive stops talking
        lda #PH_FILE
        jsr K_CLOSE
        sei
        ldx #0                  ; the game's pages back
-       lda PH_SAVE,x           ; ($01: $35, the KERNAL out)
        sta $00,x
        lda PH_SAVE + $100,x
        sta $0200,x
        lda PH_SAVE + $200,x
        sta $0300,x
        inx
        bne -
        lda $dc0d               ; what the bus left in the
        lda $dd0d               ; CIAs' flags: away
        plp
        rts

; The file: open, its mark, its number, its bar's step, its
; records put in place, its sum. C = 1 when not right: the
; drive or the disk not there, an error on the bus, a wrong
; mark, number or sum, the file ended early.
ph_read_file:
        ldx ph_want             ; its name: LEVEL4,S,R ...
        ldy ph_name_hi - 1,x
        lda ph_name_lo - 1,x
        tax
        lda #PH_NAME_LEN
        jsr K_SETNAM
        lda #PH_FILE            ; file 2: the drive, its
        ldx disk_dev            ; channel 2
        ldy #PH_FILE
        jsr K_SETLFS
        jsr K_OPEN
        bcs _no
        ldx #PH_FILE
        jsr K_CHKIN
        bcs _no
        jsr ph_head             ; its mark, number, step
        bcs _no
_record:
        jsr ph_byte             ; where
        bcs _no
        sta PH_PTR
        jsr ph_byte
        bcs _no
        sta PH_PTR + 1
        jsr ph_byte             ; how many: none, the end
        bcs _no
        sta PH_COUNT
        jsr ph_byte
        bcs _no
        sta PH_COUNT + 1
        ora PH_COUNT
        beq _sum
_byte:
        jsr ph_byte
        bcs _no
        jsr ph_put
        lda PH_COUNT            ; one less
        bne +
        dec PH_COUNT + 1
+       dec PH_COUNT
        lda PH_COUNT
        ora PH_COUNT + 1
        bne _byte
        beq _record
_sum:
        lda #%10111111          ; the last: the file's end
        sta ph_ok               ; allowed
        jsr ph_byte
        bcs _no
        lda ph_sum              ; all added: 0
        bne _no
        clc
        rts
_no:
        sec
        rts

; The file's head: "SB", the file wanted, the bar's step
; (into ph_step, ph_left). C = 1 when not right.
ph_head:
        lda #0
        sta ph_sum
        lda #$ff                ; no status bit allowed
        sta ph_ok
        jsr ph_byte             ; "S", "B"
        bcs _no
        cmp #PH_MARK_0
        bne _no
        jsr ph_byte
        bcs _no
        cmp #PH_MARK_1
        bne _no
        jsr ph_byte             ; the file's number
        bcs _no
        cmp ph_want
        bne _no
        jsr ph_byte             ; a cell of the bar: bytes
        bcs _no
        sta ph_step
        sta ph_left
        jsr ph_byte
        bcs _no
        sta ph_step + 1
        sta ph_left + 1
        rts                     ; (C = 0)
_no:
        sec
        rts

; The file's next byte into A, added to ph_sum; C = 1 when
; the bus reports a status bit not in ph_ok.
ph_byte:
        jsr K_CHRIN
        sta ph_last
        jsr K_READST
        and ph_ok
        bne _bad
        lda ph_last
        clc
        adc ph_sum
        sta ph_sum
        lda ph_last
        clc
        rts
_bad:
        sec
        rts

; A where PH_PTR points (under the I/O too: all RAM for the
; write), PH_PTR on; every ph_step bytes a cell of the bar.
ph_put:
        ldy #$34                ; all RAM
        sty $01
        ldy #0
        sta (PH_PTR),y
        ldy #$36                ; the KERNAL and the I/O
        sty $01
        inc PH_PTR
        bne +
        inc PH_PTR + 1
+       lda ph_left             ; the bar
        bne +
        dec ph_left + 1
+       dec ph_left
        lda ph_left
        ora ph_left + 1
        bne +
        lda ph_step
        sta ph_left
        lda ph_step + 1
        sta ph_left + 1
        ldx ph_cell
        cpx #PH_CELLS
        bcs +
        lda #PH_FULL
        sta PH_BAR,x
        inc ph_cell
+       rts
