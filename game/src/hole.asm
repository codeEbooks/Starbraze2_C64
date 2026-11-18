; Code in the HUD's character set after the HUD's own
; characters (hudset.bin: the codes the HUD shows), up to
; $5800: the VIC-II never shows the rest, the CPU runs it as
; any memory.

        .include "phase_show.asm"  ; the loading {10}
                                ; screen {10}
; Each level's file (phase.asm, file_need) and where its {10}
; streams go (level.asm, load_level): here, the low part {10}
; being full. {10}
level_file: ; {10}
        .byte LEVEL_FILES ; {10}
        .include "../assets/generated/levels_hole.inc"
        .include "core.asm"     ; the SHIELD CORE {9}
