; Written by game/assets/build_assets.py: do not edit.
; the files' names, by phase.asm (the low part)
ph_name_1: .text "PHASE1,S,R"
ph_name_2: .text "LEVEL3,S,R"
ph_name_3: .text "LEVEL4,S,R"
ph_name_4: .text "LEVEL5,S,R"
ph_name_5: .text "LEVEL6,S,R"
ph_name_lo:
        .byte <ph_name_1, <ph_name_2, <ph_name_3, <ph_name_4, <ph_name_5
ph_name_hi:
        .byte >ph_name_1, >ph_name_2, >ph_name_3, >ph_name_4, >ph_name_5
