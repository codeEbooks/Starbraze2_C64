; The music player: Dreadcastle's (volume 3), adapted to a
; busier frame. Three voices of the SID, one frame of music
; a frame; the sound modes.
;
; The SID's registers can only be written: the player keeps
; a copy of all 25 (sid_shadow), works on the copy, and the
; top interrupt copies it into the SID, always at the same
; moment of the frame (sid_copy, line 20). The work on the
; copy is done by the main loop after its turn
; (sound_frame: music_play, then sfx_play in effects.asm):
; there the frame has room, and the sprites, due before
; line 50, never wait for it. The tests read the copy.
;
; Time goes by steps (a semiquaver), each of 5, 4, 5 and 4
; frames in turn (tempo_table). A voice reads its pattern
; ahead: in each step, one frame each (voice 1 in the
; step's second frame, voice 2 in the third, voice 3 in
; the fourth), the voice whose note has just begun reads
; its next one (read_ahead): a note, or a rest, and before
; them a duration or an instrument; at the end of a
; pattern, the voice's order list gives the next pattern
; and how many semitones to move it; at the end of the
; list, $fe and the entry to start again from. When its
; note is over, at the step, the note read ahead begins
; (next_note). So the steps where all three voices change
; note, and patterns, cost no more than the other frames:
; this is the change from Dreadcastle, whose voices read
; at the step. In every frame each voice reads a row of its
; instrument's wavetable: a waveform, and a pitch above its
; note or a fixed note (arpeggios, drums); long notes waver
; (vibrato); the pulse width sweeps up and down between
; PW_LOW and PW_HIGH. A voice's attack, decay, sustain and
; release go into the copy when its note starts (they do
; not change during a note).
;
; The modes (F1, F3, F5, F7): MUSIC, the music on the three
; voices; MUSIC + FX, the music on voices 1 and 2 and the
; effects on voice 3 (the music's third voice reads its
; pattern on, silent, so that it stays in step); SOUND FX,
; the effects on the three voices; SILENT. A new mode, and
; each start of the level, begin in silence: then the music
; from its start, if the mode has it.

SID           = $d400
PW_LOW        = $0200           ; the pulse width sweeps
PW_HIGH       = $0e00           ; between these two
REST          = $60             ; a pattern byte: a rest
MODE_MUSIC    = 0
MODE_MUSIC_FX = 1
MODE_FX       = 2
MODE_SILENT   = 3
        .if RECORD_THEME != 0
START_MODE    = MODE_MUSIC      ; to record the theme
        .else
START_MODE    = MODE_MUSIC_FX   ; «MUSIC + FX», 15 October
        .fi
F_KEYS        = %01111000       ; keys: F1, F3, F5, F7
        .cerror MUSIC_SONGS != 7, "seven songs"

; The copy into the SID, at the top interrupt (it keeps
; only A): from the top, so that each voice's attack, decay,
; sustain and release are written before its control. (A
; voice in RECORD_MUTE gets 0 there: no envelope, silent.)
m_bit   .function c_reg         ; (RECORD_MUTE: its voice)
        .endf ((RECORD_MUTE >> (c_reg / 7)) & 1) != 0
sid_copy .macro
        .for c_reg in range(24, -1, -1)
        .if c_reg < 21 && c_reg % 7 >= 4 && m_bit(c_reg)
        lda #0
        .else
        lda sid_shadow + c_reg
        .fi
        sta SID + c_reg
        .endfor
        .endmacro

; (sound_init, the program's start, is in title.asm.)

; The keys F1, F3, F5, F7 just pushed (new_keys, bits 3-6):
; the mode of the first one, from silence.
sound_keys:
        lda new_keys
        and #F_KEYS
        beq _none
        lsr a                   ; F1 in bit 0, F7 in bit 3
        lsr a
        lsr a
        ldx #MODE_MUSIC
-       lsr a                   ; the first one pushed
        bcs _mode
        inx
        bne -                   ; (one is)
_mode:
        txa
        jmp sound_set           ; the song it plays
_none:
        rts

; Song A (the title's, the bosses', a jingle) from its
; start, in the mode there is (none in SOUND FX and SILENT:
; then it is the song a new mode starts).
song_start:
        sta mus_song
        lda sound_mode
        jmp mode_set

; Mode A, from silence: every gate off in the copy, no
; effects, no music; then the music from its start if the
; mode has it, on 3 voices (MUSIC) or 2 (MUSIC + FX). At
; each start of the level, in the mode it has, the level's
; song; a new mode (mode_set) the song it played.
sound_set:
        ldx level               ; the level's song:
        ldy level_song,x        ; the theme of the canyons,
        sty mus_song            ; of space
mode_set:
        sta sound_mode
        lda #0
        sta mus_on
        ldx #2
-       sta fx_pos,x
        sta fx_pri,x
        sta fx_next,x
        dex
        bpl -
        jsr gates_off
        lda sound_mode
        cmp #MODE_FX
        bcs +                   ; SOUND FX, SILENT
        lda #3                  ; the music's voices
        sec
        sbc sound_mode
        sta mus_voices
        jmp start_song
+       rts

level_song:                     ; by level
        .if RECORD_SONG != 0
        .fill LEVEL_COUNT, RECORD_SONG
        .else
        .byte LEVEL_SONGS
        .fi

gates_off:
        ldx #2
-       ldy voice_regs,x        ; the control register of
        lda sid_shadow + 4,y    ; each voice: the gate off
        and #%11111110
        sta sid_shadow + 4,y
        dex
        bpl -
        rts

; Every voice at the start of its order list of mus_song;
; playing. Its first step in the fifth frame: in the frames
; before, the voices read their first notes ahead, and the
; copy keeps the gates off, so that the SID lets the notes
; before go.
start_song:
        lda #4                  ; the fifth frame starts a
        sta mus_tick            ; step
        lda #1
        sta mus_on
        sta mus_first
        lda #0
        sta mus_tempo
        ldx #2                  ; voices 2, 1, 0
_voice:
        txa                     ; the voice's order list
        ldy mus_song
        clc
        adc song_lists,y
        tay
        lda order_lo,y
        sta v_list_lo,x
        lda order_hi,y
        sta v_list_hi,x
        lda #0
        sta v_order,x
        sta v_pins,x
        sta v_ins,x
        sta v_note,x
        sta v_gate,x
        sta v_wave,x
        sta v_ctrl,x
        sta v_pw_lo,x
        sta v_pw_hi,x
        sta v_sweep,x
        sta v_vib,x
        sta v_fresh,x
        sta p_ready,x           ; its first note: to read
        lda #1                  ; a step to wait: the notes
        sta v_dur,x             ; start in the first step
        sta v_left,x
        jsr load_order
        dex
        bpl _voice
        rts

; One frame of the music (the main loop, sound_frame);
; stopped, nothing. At a step, the notes over give way to
; those read ahead; in the step's frames with mus_tick 3,
; 2, 1, voice 1, 2, 3 reads its next note if it has begun
; one; then each voice the music sounds, its frame.
music_play:
        lda mus_on
        bne +
        rts
+       inc mus_frame
        bne +
        inc mus_frame + 1
+       dec mus_tick
        bne _ahead
        lda mus_song            ; a new step: the song's
        asl a                   ; tempo, four steps a song
        asl a
        ora mus_tempo
        tax
        lda tempo_table,x
        sta mus_tick
        inc mus_tempo
        lda mus_tempo
        and #%00000011
        sta mus_tempo
        ldx #2                  ; all three voices go on
-       dec v_left,x            ; a note over: the next
        bne +
        jsr next_note
+       dex
        bpl -
        lda #0                  ; the notes have begun
        sta mus_first
        beq _frame
_ahead:
        lda mus_tick            ; 3, 2, 1: voice 0, 1, 2
        cmp #4
        bcs _frame
        eor #%00000011
        tax
        lda p_ready,x           ; its next note read?
        bne _frame
        jsr read_ahead
_frame:
        lda mus_first           ; before the first step:
        bne _done               ; the gates stay off
        ldx mus_voices          ; the voices it sounds
        dex
-       jsr voice_frame
        dex
        bpl -
_done:
        rts

        .cerror MUSIC_SHORTEST_STEP < 4, "4 frames a step"

; Voice X: the pattern and the transposition of entry
; v_order of its order list; $fe: start again from the
; entry that follows it; SONG_END: the song is over (carry
; set).
load_order:
        lda v_list_lo,x
        sta mus_ptr
        lda v_list_hi,x
        sta mus_ptr + 1
        lda v_order,x
        asl a                   ; two bytes an entry
        tay
        lda (mus_ptr),y
        cmp #$fe
        bne +
        iny                     ; the end: back to the entry
        lda (mus_ptr),y
        sta v_order,x
        asl a
        tay
        lda (mus_ptr),y
+       cmp #SONG_END
        bne +
        sec                     ; the song's end
        rts
+       sta mus_work            ; the pattern
        iny
        lda (mus_ptr),y
        sta v_trans,x           ; its transposition
        ldy mus_work
        lda pattern_lo,y
        sta v_ptr_lo,x
        lda pattern_hi,y
        sta v_ptr_hi,x
        clc
        rts

; Voice X reads its next note ahead: its pattern up to a
; note or a rest (instruments and durations on the way are
; for the notes that follow), or the song's end. p_note
; (the note, transposed; REST; SONG_END), p_ins, p_left.
read_ahead:
        lda v_ptr_lo,x
        sta mus_ptr
        lda v_ptr_hi,x
        sta mus_ptr + 1
        ldy #0
_next:
        lda (mus_ptr),y
        iny
        cmp #$ff
        bne _event
        inc v_order,x           ; end of the pattern: the
        jsr load_order          ; next entry of the list
        bcc +
        lda #SONG_END           ; the song is over
        bne _store
+       lda v_ptr_lo,x
        sta mus_ptr
        lda v_ptr_hi,x
        sta mus_ptr + 1
        ldy #0
        beq _next
_event:
        cmp #$c0
        bcc +
        and #%00011111          ; an instrument
        sta v_pins,x
        jmp _next
+       cmp #$80
        bcc +
        and #%00111111          ; a duration
        clc
        adc #1
        sta v_dur,x
        jmp _next
+       cmp #REST
        beq +
        clc                     ; a note: transposed
        adc v_trans,x
+       sta mus_note
        tya                     ; the pattern goes on here
        clc
        adc mus_ptr
        sta v_ptr_lo,x
        lda mus_ptr + 1
        adc #0
        sta v_ptr_hi,x
        lda mus_note
_store:
        sta p_note,x
        lda v_pins,x
        sta p_ins,x
        lda v_dur,x
        sta p_left,x
        lda #1
        sta p_ready,x
        rts

; Voice X, at the step that ends its note: the note read
; ahead begins (its instrument from the start: wavetable,
; pulse width and sweep, vibrato's delay; its envelope
; into the copy in voice_frame), or a rest (the gate off),
; or the song's end (the player stops).
next_note:
        lda #0                  ; the next: to read ahead
        sta p_ready,x
        lda p_left,x
        sta v_left,x
        lda p_note,x
        cmp #REST
        beq _rest
        cmp #SONG_END
        beq _end
        sta v_note,x
        lda #1                  ; the gate on, a new note
        sta v_gate,x
        sta v_fresh,x
        lda p_ins,x
        sta v_ins,x
        tay
        lda ins_wave,y
        sta v_wave,x
        lda ins_pw_lo,y
        sta v_pw_lo,x
        lda ins_pw_hi,y
        sta v_pw_hi,x
        lda ins_sweep,y
        sta v_sweep,x
        lda ins_vibrato,y
        sta v_vib,x
        rts
_end:
        lda #0
        sta mus_on
_rest:
        lda #0                  ; the gate off
        sta v_gate,x
        rts

; Voice X, one frame: gate, wavetable, frequency, vibrato,
; pulse width; then its registers in the copy (the
; envelope only when a note has started).
voice_frame:
        lda v_left,x            ; in the last frames of the
        cmp #1                  ; note the gate is off, so
        bne +                   ; that the next one starts
        lda mus_tick
        cmp #MUSIC_GATE_TICK + 1
        bcs +
        lda #0
        sta v_gate,x
+       ldy v_wave,x            ; the wavetable row
        lda wave_ctrl,y
        sta v_ctrl,x
        lda wave_next,y         ; next frame: the next row
        sta v_wave,x
        lda wave_pitch,y
        bmi _fixed
        clc                     ; semitones above the note
        adc v_note,x
        tay
        jmp _pitch
_fixed:
        and #%01111111          ; a fixed note
        tay
_pitch:
        lda freq_lo,y
        sta mus_freq
        lda freq_hi,y
        sta mus_freq + 1
        ldy v_ins,x             ; vibrato, after a delay
        lda ins_vibrato,y
        beq _pulse
        lda v_vib,x
        beq _wobble
        dec v_vib,x
        jmp _pulse
_wobble:
        lda mus_freq + 1        ; a step: frequency / 256
        sta mus_work
        lda mus_frame
        and #%00000111
        tay
        lda vibrato_table,y     ; -2 to 2 steps
        beq _pulse
        bmi _down
        tay
-       clc
        lda mus_freq
        adc mus_work
        sta mus_freq
        bcc +
        inc mus_freq + 1
+       dey
        bne -
        beq _pulse
_down:
        eor #$ff                ; how many: -A
        clc
        adc #1
        tay
-       sec
        lda mus_freq
        sbc mus_work
        sta mus_freq
        bcs +
        dec mus_freq + 1
+       dey
        bne -
_pulse:
        lda v_sweep,x           ; the pulse width sweeps
        beq _copy
        bmi _narrower
        clc                     ; wider
        adc v_pw_lo,x
        sta v_pw_lo,x
        lda v_pw_hi,x
        adc #0
        sta v_pw_hi,x
        cmp #>PW_HIGH
        bcc _copy
        lda #<PW_HIGH           ; at the top: turn back
        sta v_pw_lo,x
        lda #>PW_HIGH
        sta v_pw_hi,x
        jmp _turn
_narrower:
        clc                     ; narrower: sweep < 0
        adc v_pw_lo,x
        sta v_pw_lo,x
        lda v_pw_hi,x
        adc #$ff
        sta v_pw_hi,x
        cmp #>PW_LOW
        bcs _copy
        lda #<PW_LOW            ; at the bottom: turn back
        sta v_pw_lo,x
        lda #>PW_LOW
        sta v_pw_hi,x
_turn:
        lda v_sweep,x
        eor #$ff
        clc
        adc #1
        sta v_sweep,x
_copy:
        ldy voice_regs,x        ; the voice's registers
        lda v_fresh,x           ; a new note: its envelope
        beq +
        lda #0
        sta v_fresh,x
        stx mus_work
        lda v_ins,x
        tax
        lda sound_mode          ; MUSIC + FX: the
        bne _soft               ; music softer
        lda ins_ad,x            ; attack and decay
        sta sid_shadow + 5,y
        lda ins_sr,x            ; sustain and release
        jmp _sr
_soft:
        lda ins_ad_fx,x
        sta sid_shadow + 5,y
        lda ins_sr_fx,x
_sr:
        sta sid_shadow + 6,y
        ldx mus_work
+       lda mus_freq
        sta sid_shadow,y
        lda mus_freq + 1
        sta sid_shadow + 1,y
        lda v_pw_lo,x
        sta sid_shadow + 2,y
        lda v_pw_hi,x
        sta sid_shadow + 3,y
        lda v_ctrl,x
        ora v_gate,x            ; gate: bit 0
        sta sid_shadow + 4,y
        rts

voice_regs:
        .byte 0, 7, 14
vibrato_table:
        .byte 0, 1, 2, 1, 0, $ff, $fe, $ff
