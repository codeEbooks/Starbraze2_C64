; Code in the HUD's character set after the HUD's own
; characters (hudset.bin: the codes the HUD shows), up to
; $5800: the VIC-II never shows the rest, the CPU runs it as
; any memory.

        .include "phase_show.asm"  ; the loading
                                ; screen
; Each level's file (phase.asm, file_need) and where its
; streams go (level.asm, load_level): here, the low part
; being full.
level_file:
        .byte LEVEL_FILES
        .include "../assets/generated/levels_hole.inc"
        .include "core.asm"     ; the SHIELD CORE
