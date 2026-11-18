; Written by game/assets/build_assets.py: do not edit.

; the plane of the stars of rows 0-9
star_plane:
        .byte 2, 2, 2, 2, 2, 2, 2, 2, 2, 2
; the line of the row they are on, 0-7
star_line:
        .byte 2, 5, 1, 6, 3, 6, 1, 4, 2, 5
; their pixel in the cell at camera 0, 0-7
star_pixel:
        .byte 5, 1, 3, 6, 2, 0, 4, 7, 1, 3
; the blank sky of their plane
star_sky:
        .byte 3, 3, 3, 3, 3, 3, 3, 3, 3, 3
; where the row's stars start in star_cells
star_first:
        .byte 0, 3, 5, 8, 11, 13, 16, 19, 21, 24, 27
; the stars' cells on the ring of 40, twice: star + 32 for screen B's records
star_cells:
        .byte 4, 19, 33, 11, 26, 1, 15, 30, 8, 22, 37, 17
        .byte 34, 5, 20, 28, 12, 25, 39, 2, 31, 9, 23, 36
        .byte 6, 18, 29, 0, 0, 0, 0, 0, 4, 19, 33, 11
        .byte 26, 1, 15, 30, 8, 22, 37, 17, 34, 5, 20, 28
        .byte 12, 25, 39, 2, 31, 9, 23, 36, 6, 18, 29
; the ships: speed, 256ths of a pixel a frame
ship_speed_lo:
        .byte 128, 0, 0
ship_speed_hi:
        .byte 1, 2, 1
; notches of the shield
ship_shield:
        .byte 4, 3, 6
; colour of the colour layer, of the accent
ship_own:
        .byte 15, 0, 12
ship_accent:
        .byte 14, 3, 7
; the ship's y with its five points in the corridor (rows 10-14): from, to (excluded)
ship_air_from:
        .byte 76, 75, 78
ship_air_to:
        .byte 103, 105, 105
; five points meeting the rock, x in the sprite, a ship after the other
ship_spot_x:
        .byte 23, 17, 6, 17, 6, 23, 17, 6, 17, 6, 23, 17
        .byte 6, 17, 6
ship_spot_y:
        .byte 11, 8, 4, 13, 17, 10, 8, 5, 12, 15, 9, 4
        .byte 2, 13, 15
; the ship's box against the Varkon: left (x register / 2 + this), its right, top (y register + this), its height
ship_box_x:
        .byte 1, 1, 1
ship_box_w:
        .byte 9, 9, 9
ship_box_y:
        .byte 7, 6, 5
ship_box_h:
        .byte 8, 9, 8
; against a plasma shot's middle: the box less the middle's place in the shot's sprite
ship_pbox_x:
        .byte 250, 250, 250
ship_pbox_w:
        .byte 11, 11, 11
ship_pbox_y:
        .byte 251, 250, 249
ship_pbox_h:
        .byte 12, 13, 12
; the shots: pixels a frame, colour
shot_speed:
        .byte 6, 8, 4, 6, 6, 6, 6, 6, 8, 4, 8, 8
        .byte 4, 4, 6
shot_colour:
        .byte 14, 3, 7, 14, 14, 14, 14, 14, 3, 7, 3, 3
        .byte 13, 13, 13
; the sprite block of each kind (both halves; the upper, the lower next)
shot_block:
        .byte 158, 161, 162, 187, 188, 189, 190, 193, 196, 199, 200, 201
        .byte 202, 203, 204
; its halves when it leaves (%11 a double bolt), y velocity (lines a frame), 1 if it pierces, its blast (0 none, 1, 2)
shot_halves:
        .byte 3, 1, 1, 1, 1, 1, 3, 3, 3, 1, 1, 1
        .byte 1, 1, 1
shot_vy:
        .byte 0, 0, 0, 0, 255, 1, 255, 1, 0, 0, 0, 0
        .byte 0, 0, 0
shot_pierce:
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1
        .byte 0, 0, 0
shot_blast:
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        .byte 1, 2, 0
; the blasts: half width (x register / 2), half height (lines), hits off
blast_rx:
        .byte 8, 14
blast_ry:
        .byte 14, 24
blast_dmg:
        .byte 1, 2
; a shot that bursts: the fireball's sprite from the shot's, x, y (its middle on the point)
shot_bdx:
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        .byte 252, 254, 0
shot_bdy:
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        .byte 255, 255, 0
; a blast by its frames left (1-BLAST_FRAMES): the fireball's block, its colour
blast_block:
        .byte 147, 157, 157, 155, 155, 153, 153, 153, 151, 151, 149, 147
        .byte 147
blast_own:
        .byte 7, 9, 9, 9, 9, 8, 8, 8, 8, 8, 7, 7
        .byte 7
; the missile's point for the hits, falling, running: x + 24, y + 50 in its sprite
m_nose_x:
        .byte 39, 43
m_nose_y:
        .byte 63, 61
; a capsule's colour, by anim / 4 AND 3
capsule_colour:
        .byte 2, 10, 8, 10
; the weapons, ship * 4 + level: frames between volleys, shots in a volley, its first entry, its sound
w_period:
        .byte 8, 6, 12, 12, 4, 4, 6, 6, 14, 14, 16, 16
w_count:
        .byte 1, 1, 3, 3, 1, 1, 1, 2, 1, 1, 1, 1
w_first:
        .byte 0, 1, 2, 5, 8, 9, 10, 11, 13, 14, 15, 16
w_fx:
        .byte 0, 0, 0, 0, 1, 1, 7, 7, 2, 2, 2, 2
; a volley's shots: kind, from the nose dx, dy
v_kind:
        .byte 0, 0, 3, 4, 5, 0, 6, 7, 1, 8, 10, 11
        .byte 11, 2, 9, 12, 13
v_dx:
        .byte 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        .byte 24, 0, 0, 0, 0
v_dy:
        .byte 0, 0, 0, 254, 2, 0, 254, 2, 0, 0, 0, 0
        .byte 0, 0, 0, 0, 0
; the explosion, frame by frame: the sparks' block (the fireball's is the next), their colours
explosion_block:
        .byte 146, 146, 146, 148, 148, 148, 148, 150, 150, 150, 150, 150
        .byte 152, 152, 152, 152, 152, 152, 154, 154, 154, 154, 154, 154
        .byte 156, 156, 156, 156, 156, 156
explosion_spark:
        .byte 1, 1, 1, 7, 7, 7, 7, 7, 7, 7, 7, 7
        .byte 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8
        .byte 9, 9, 9, 9, 9, 9
explosion_own:
        .byte 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8
        .byte 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9
        .byte 9, 9, 9, 9, 9, 9
; hits off a Varkon
shot_damage:
        .byte 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1, 2
        .byte 3, 4, 1
; half the speed: the point's x register / 2
shot_half:
        .byte 3, 4, 2, 3, 3, 3, 3, 3, 4, 2, 4, 4
        .byte 2, 2, 3
; the shot's y with its points in the corridor: from, to (excluded)
air_from:
        .byte 73, 70, 71, 70, 72, 68, 75, 72, 72, 71, 70, 70
        .byte 71, 71, 70
air_to:
        .byte 106, 110, 111, 110, 112, 108, 108, 105, 108, 111, 110, 110
        .byte 111, 111, 110
; the point against the Varkon: x of its tip + 24; its line + 50, by kind * 4 + its halves
shot_tip:
        .byte 33, 39, 32, 33, 33, 33, 33, 33, 39, 33, 47, 47
        .byte 32, 34, 33
shot_mid:
        .byte 0, 57, 64, 60, 0, 60, 60, 60, 0, 59, 59, 59
        .byte 0, 60, 60, 60, 0, 58, 58, 58, 0, 62, 62, 62
        .byte 0, 55, 62, 58, 0, 58, 65, 61, 0, 58, 62, 60
        .byte 0, 59, 59, 59, 0, 60, 60, 60, 0, 60, 60, 60
        .byte 0, 59, 59, 59, 0, 59, 59, 59, 0, 60, 60, 60
; a shot that leaves, all its halves: its point's line + 50
shot_mid0:
        .byte 60, 60, 59, 60, 58, 62, 58, 61, 60, 59, 60, 60
        .byte 59, 59, 60
; two points each: the tips of the bolts
shot_point_x:
        .byte 9, 9, 15, 15, 8, 8, 9, 9, 9, 9, 9, 9
        .byte 9, 9, 9, 9, 15, 15, 9, 9, 23, 23, 23, 23
        .byte 8, 8, 10, 10, 9, 9
shot_point_y:
        .byte 7, 14, 10, 10, 9, 9, 10, 10, 8, 8, 12, 12
        .byte 5, 12, 8, 15, 8, 12, 9, 9, 10, 10, 10, 10
        .byte 9, 9, 9, 9, 10, 10
