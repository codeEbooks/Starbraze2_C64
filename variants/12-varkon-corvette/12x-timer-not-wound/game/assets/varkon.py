"""The Varkon as data: level 1's here first, then the other levels' and the
bosses' parts.

The level plan (STARBRAZE2_LEVEL_PLAN.md, 15 October 2026): four kinds of
Varkon in phase 1 - the raider, the drone, the lancer and the leaper, a
walker of the drone factory that hops along the canyon's floor and fires
upwards - with the flak turrets on the bunkers of tract C and the carriers,
raiders in gold (they leave the capsules). The level's waves are in
level1.py.

  KINDS   each kind: how it moves (its behaviour), its pictures and
          colour, how many hits it takes, its points, how often it
          fires and how its shot flies, its box
  PATHS   where a flyer goes: a list of stretches, each so many frames
          at a velocity (pixels a frame, x to the right, y down)

Four behaviours:
  path    a flyer: it follows its path on the screen;
  hop     a leaper: it stands on the rock and moves with it (its x
          goes with the camera), walking to the left in hops of
          HOP_FRAMES frames; each hop lands where the floor is
          (floor_line, from the level's rock), under gravity;
  turret  a flak gun on a bunker: it moves with the rock, turns its
          barrel to the ship (left, up, right) and fires that way;
  boss    a part of the boss (crawler.py): the
          boss's program puts it on the boss's body each frame and
          picks its picture; it is hit like the others, but the ship
          that touches it does not destroy it.

Places are the ship's: x of the sprite's left edge on the screen, y
of its top line in the playfield (0-154). Velocities are kept in
256ths of a pixel, like the ship's; a shot's x velocity in whole
pixels.
"""

import math

import corvette
import crawler
import defense
import shieldcore
import supercomp
import warden

PATH, HOP, TURRET, BOSS = 0, 1, 2, 3
# Level 2's: STAND, a tower's core: it stands on the steel and moves with
# it, pulses (its pictures by the frame) and fires; FIELD, a piece of a
# tower's field: it stands on the steel, the ship's shots go through it,
# the ship that touches it is pushed back as by the rock (two notches); it
# goes when its tower's core is destroyed (FIELD_REACH).
STAND, FIELD = 4, 5
FIELD_REACH = 64         # pixels: the field's pieces near a core

# Each kind: its behaviour; its sprites (sprites.VARKON_KINDS, four
# pictures) and own colour; hits it takes (a shot of the ship does
# its kind's damage, ships.SHOT_KINDS); points; frames between two
# shots (0: it does not fire) and the shot: x velocity in whole
# pixels, y velocity in pixels, aimed (1: the drone's drifts up or
# down towards the ship) or not, where it starts from the kind's
# sprite (dx, dy).
KINDS = {
    "raider": {"behaviour": PATH, "pictures": "raider", "colour": 4,
               "life": 1, "points": 100, "period": 80,
               "shot": (-3, 0.0), "aim": 0, "from": (-8, 0)},
    "drone": {"behaviour": PATH, "pictures": "drone", "colour": 10,
              "life": 1, "points": 150, "period": 96,
              "shot": (-2, 0.0), "aim": 1, "from": (-8, 0)},
    "lancer": {"behaviour": PATH, "pictures": "lancer", "colour": 5,
               "life": 1, "points": 100, "period": 0,
               "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "leaper": {"behaviour": HOP, "pictures": "leaper", "colour": 13,
               "life": 2, "points": 200, "period": 64,
               "shot": (0, -3.0), "aim": 0, "from": (0, -6)},
    "turret": {"behaviour": TURRET, "pictures": "turret", "colour": 12,
               "life": 4, "points": 300, "period": 56,
               "shot": (0, -3.0), "aim": 0, "from": (0, 0)},
    "carrier": {"behaviour": PATH, "pictures": "raider", "colour": 7,
                "life": 2, "points": 500, "period": 80,
                "shot": (-3, 0.0), "aim": 0, "from": (-8, 0)},
    # the SIEGE CRAWLER's parts (crawler.py): the cannons fire their fans
    # from the boss's program (period 0 here), the core an aimed shot like
    # the drone's
    "cannon": {"behaviour": BOSS, "pictures": "cannon",
               "colour": crawler.CANNON_OWN, "life": crawler.CANNON_LIFE,
               "points": crawler.CANNON_POINTS, "period": 0,
               "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "core": {"behaviour": BOSS, "pictures": "core",
             "colour": crawler.CORE_OWN, "life": crawler.CORE_LIFE,
             "points": crawler.CORE_POINTS,
             "period": crawler.CORE_PERIOD,
             "shot": (crawler.CORE_SHOT[0], 0.0), "aim": 1,
             "from": crawler.CORE_SHOT[1]},
}
# level 2's: the interceptor comes from behind (from the left) and passes
# the ship, it does not fire; the carrier of level 2 is a drone in gold; a
# tower's core (it fires as the drone does) and the pieces of its field
KINDS.update({
    "interceptor": {"behaviour": PATH, "pictures": "interceptor",
                    "colour": 2, "life": 1, "points": 200, "period": 0,
                    "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "dcarrier": {"behaviour": PATH, "pictures": "drone", "colour": 7,
                 "life": 2, "points": 500, "period": 96,
                 "shot": (-2, 0.0), "aim": 1, "from": (-8, 0)},
    "gencore": {"behaviour": STAND, "pictures": "gencore", "colour": 3,
                "life": 6, "points": 400, "period": 72,
                "shot": (-2, 0.0), "aim": 1, "from": (-6, 0)},
    "field": {"behaviour": FIELD, "pictures": "field", "colour": 3,
              "life": 127, "points": 0, "period": 0,
              "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
})
# the SHIELD CORE's parts (shieldcore.py): the segments of its shield (they
# can be destroyed: a shot ends on one whole, a laser too, and takes its
# damage), its core (an aimed shot, the drone's), its two cannons (their
# fans from the boss's program)
KINDS.update({
    "segment": {"behaviour": BOSS, "pictures": "segment",
                "colour": shieldcore.SEGMENT_OWN,
                "life": shieldcore.SEGMENT_LIFE,
                "points": shieldcore.SEGMENT_POINTS, "period": 0,
                "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "shcore": {"behaviour": BOSS, "pictures": "shcore",
               "colour": shieldcore.CORE_OWN,
               "life": shieldcore.CORE_LIFE,
               "points": shieldcore.CORE_POINTS,
               "period": shieldcore.CORE_PERIOD,
               "shot": (shieldcore.CORE_SHOT[0], 0.0), "aim": 1,
               "from": shieldcore.CORE_SHOT[1]},
    "pod": {"behaviour": BOSS, "pictures": "pod",
            "colour": shieldcore.POD_OWN, "life": shieldcore.POD_LIFE,
            "points": shieldcore.POD_POINTS, "period": 0,
            "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
})
# Level 3's (the level plan, §2): the scout, small, in files that follow
# one path (the snakes), it does not fire; the gunship, slower and
# stronger, fires a fan of three shots (GUN_FAN); the carrier of level 3, a
# gunship in gold; the mine (MINE), anchored in space (it moves with the
# camera, as the turret): the ship within MINE_REACH bursts it, four shots
# of its shrapnel (MINE_FAN), no points; destroyed by the ship's shots it
# explodes as the others; the rock, an asteroid adrift (the paths
# drift_down, drift_up): destroyed by the shots, it splits into two shards
# (SHARD_PATHS: hits.asm, split), small rocks.
MINE = 6
KINDS.update({
    "scout": {"behaviour": PATH, "pictures": "scout", "colour": 14,
              "life": 1, "points": 100, "period": 0,
              "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "gunship": {"behaviour": PATH, "pictures": "gunship", "colour": 8,
                "life": 4, "points": 300, "period": 88,
                "shot": (-2, 0.0), "aim": 0, "from": (-10, 2)},
    "gcarrier": {"behaviour": PATH, "pictures": "gunship", "colour": 7,
                 "life": 2, "points": 500, "period": 88,
                 "shot": (-2, 0.0), "aim": 0, "from": (-10, 2)},
    "mine": {"behaviour": MINE, "pictures": "mine", "colour": 2,
             "life": 2, "points": 150, "period": 0,
             "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "rock": {"behaviour": PATH, "pictures": "rock", "colour": 12,
             "life": 4, "points": 200, "period": 0,
             "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "shard": {"behaviour": PATH, "pictures": "shard", "colour": 12,
              "life": 1, "points": 50, "period": 0,
              "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
})
# The GRAVEYARD WARDEN's parts (warden.py): the guns in its ports fire
# their fans from the boss's program (period 0 here), its core an aimed
# shot (the drone's), faster under half its life (warden.asm).
KINDS.update({
    "wgun": {"behaviour": BOSS, "pictures": "wgun",
             "colour": warden.GUN_OWN, "life": warden.GUN_LIFE,
             "points": warden.GUN_POINTS, "period": 0,
             "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "wcore": {"behaviour": BOSS, "pictures": "wcore",
              "colour": warden.CORE_OWN, "life": warden.CORE_LIFE,
              "points": warden.CORE_POINTS,
              "period": warden.CORE_PERIOD,
              "shot": (warden.CORE_SHOT[0], 0.0), "aim": 1,
              "from": warden.CORE_SHOT[1]},
})
# Level 4's (the level plan, §2): the heavy lancer, a big lancer that comes
# in diving (the paths dive, climb), armoured, it does not fire; the
# carrier of level 4, a scout in gold.
KINDS.update({
    "hlancer": {"behaviour": PATH, "pictures": "hlancer", "colour": 4,
                "life": 3, "points": 250, "period": 0,
                "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "scarrier": {"behaviour": PATH, "pictures": "scout", "colour": 7,
                 "life": 2, "points": 500, "period": 0,
                 "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
})
# The VARKON CORVETTE's parts (corvette.py): the turrets on its flanks fire
# their fans from the boss's program (period 0 here), the bridge's dome an
# aimed shot (the drone's), faster under half its life (corvette.asm).
KINDS.update({
    "cturret": {"behaviour": BOSS, "pictures": "cturret",
                "colour": corvette.TURRET_OWN,
                "life": corvette.TURRET_LIFE,
                "points": corvette.TURRET_POINTS, "period": 0,
                "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "cbridge": {"behaviour": BOSS, "pictures": "cbridge",
                "colour": corvette.BRIDGE_OWN,
                "life": corvette.BRIDGE_LIFE,
                "points": corvette.BRIDGE_POINTS,
                "period": corvette.BRIDGE_PERIOD,
                "shot": (corvette.BRIDGE_SHOT[0], 0.0), "aim": 1,
                "from": corvette.BRIDGE_SHOT[1]},
})
# Phase 3's (the level plan, §3; level 5, VARKON-OMEGA). Three behaviours
# of the station's module (station.asm, at P3_AT, in level 5's file):
# CRAWL, a crawler on the floor or on the ceiling, which runs along it to
# the left (CRAWL_VX against the rock) and fires straight up (on the floor)
# or down (on the ceiling); LMINE, the laser mine, anchored, which fires
# its ray (three bolts, LMINE_RAY) when the ship is ahead of it on its line
# (LMINE_BAND lines, ahead to its left) and has not fired for LMINE_REST
# frames; HANG, a turret on the ceiling: it aims as the turret (aim),
# down-left, down, down-right, and fires that way every HANG_PERIOD frames.
# The sentinel patrols to and fro (the path "patrol"), the defence fighter
# comes out of the walls (the paths "emerge_down", "emerge_up"); the
# carrier of level 5, a sentinel in gold.
CRAWL, LMINE, HANG = 7, 8, 9
P3_BEH = CRAWL           # the first behaviour of the station's module
KINDS.update({
    "sentinel": {"behaviour": PATH, "pictures": "sentinel", "colour": 3,
                 "life": 2, "points": 200, "period": 72,
                 "shot": (-2, 0.0), "aim": 1, "from": (-8, 2)},
    "tcarrier": {"behaviour": PATH, "pictures": "sentinel", "colour": 7,
                 "life": 2, "points": 500, "period": 72,
                 "shot": (-2, 0.0), "aim": 1, "from": (-8, 2)},
    "crawler": {"behaviour": CRAWL, "pictures": "crawler", "colour": 8,
                "life": 3, "points": 250, "period": 60,
                "shot": (0, -3.0), "aim": 0, "from": (0, -8)},
    "hcrawler": {"behaviour": CRAWL, "pictures": "hcrawler",
                 "colour": 8, "life": 3, "points": 250, "period": 60,
                 "shot": (0, 3.0), "aim": 0, "from": (0, 8)},
    "defender": {"behaviour": PATH, "pictures": "defender", "colour": 10,
                 "life": 2, "points": 200, "period": 64,
                 "shot": (-3, 0.0), "aim": 0, "from": (-10, 1)},
    "lmine": {"behaviour": LMINE, "pictures": "lmine", "colour": 2,
              "life": 2, "points": 200, "period": 0,
              "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "hturret": {"behaviour": HANG, "pictures": "hturret", "colour": 12,
                "life": 4, "points": 300, "period": 0,
                "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
})
# The DEFENSE TURRET ARRAY's parts (defense.py): the turrets in its bays
# fire their fans from the boss's program (period 0 here), the core's lens
# an aimed shot (the drone's) between its rays (defense.asm). Phase 3's: in
# the CORVETTE's slots.
KINDS.update({
    "aturret": {"behaviour": BOSS, "pictures": "aturret",
                "colour": defense.TURRET_OWN,
                "life": defense.TURRET_LIFE,
                "points": defense.TURRET_POINTS, "period": 0,
                "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "acore": {"behaviour": BOSS, "pictures": "acore",
              "colour": defense.LENS_OWN,
              "life": defense.CORE_LIFE,
              "points": defense.CORE_POINTS,
              "period": defense.CORE_PERIOD,
              "shot": (defense.CORE_SHOT[0], 0.0), "aim": 1,
              "from": defense.CORE_SHOT[1]},
})
# Level 6's (THE CORE; the level plan, §2, §3; the author's decisions of 26
# October: «Si apre, spara, si richiude», «Un varco che cambia posto»,
# «Quando passi vicino»). Three behaviours more of the station's module
# (station.asm): GUARD, the core's guardian, an armoured drone: it comes in
# from the right, stops in front of the ship (GUARD_STOP_X) and follows its
# line slowly; shut, it is armour (its life kept aside, the shots end on
# its shell); it opens (GUARD_SHUT frames shut, GUARD_OPEN open), fires its
# kind's fan (three shots) and only then can be hit; after GUARD_TIMES
# openings it leaves to the left. EGG, a drone's egg on the floor or on the
# ceiling: when the ship comes within EGG_NEAR pixels of it (to its left)
# it hatches: the drone out of it (the paths emerge_up, emerge_down: up
# from the floor, down from the ceiling); destroyed before, no drone. BAR,
# a timed barrier's middle piece, in the corridor (rows 10-14 are never
# rock: two sprites one over the other), on, dimmed or off with the
# barriers' cycle (below, BAR_*_LOOKS), which it also follows for the
# energy above and below (the level's two beam codes: the engine's cycle of
# the beams is not level 6's); on: it pushes the ship back as level 2's
# fields (the ship on it a notch, as on a Varkon, then the push), the shots
# end on it, it is never destroyed; dimmed, its threads, not met; off, not
# shown. The carrier of level 6, a crawler in gold.
GUARD, EGG, BAR = 10, 11, 12
KINDS.update({
    "guardian": {"behaviour": GUARD, "pictures": "guardian",
                 "colour": 13, "life": 6, "points": 400, "period": 0,
                 "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "egg": {"behaviour": EGG, "pictures": "egg", "colour": 5,
            "life": 2, "points": 150, "period": 0,
            "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "barrier": {"behaviour": BAR, "pictures": "barrier", "colour": 3,
                "life": 100, "points": 0, "period": 0,
                "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "ccarrier": {"behaviour": CRAWL, "pictures": "crawler", "colour": 7,
                 "life": 3, "points": 500, "period": 60,
                 "shot": (0, -3.0), "aim": 0, "from": (0, -8)},
})
# The escape's: FALL, a piece of the station falling from the ceiling
# through the corridor (with the rock, as the things on it), its two
# pictures by the frame; at FALL_END it breaks (its fireball, no points):
# the escape's code (escape.asm, ES_PART), where the station's module sends
# it. In level 6's table set, in the slot of phase 1's gold drone
# (PHASE_KINDS: level 6's file brings it, PHASE1 writes phase 1's back).
# Its pictures in the egg's blocks (the escape has no eggs: its code puts
# them there).
FALL = 13
FALL_VY = 1.5            # pixels a frame
FALL_END = 129           # its y where it breaks: its picture's last
                         # line (13) just over the floor in row 18
                         # (tests/levels.py, 16)
KINDS.update({
    "rubble": {"behaviour": FALL, "pictures": "rubble", "colour": 12,
               "life": 2, "points": 50, "period": 0,
               "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
})
# The SUPER-COMPUTER VARKON's parts (supercomp.py): its rings' plates (the
# outer one's in the SHIELD CORE's segment's slot: KIND_SEGMENT, which
# stops even a laser), its turrets (their fans from the boss's program,
# period 0 here), its core (its fan from the boss's program too; its shot
# through the rings' gaps, from the core's shell, a fire entry of level 6's
# table set: build_assets.py, fire_entries). Level 6's (table set 4): in
# the SHIELD CORE's slots and the CORVETTE's.
KINDS.update({
    "plate": {"behaviour": BOSS, "pictures": "plate",
              "colour": supercomp.PLATE_OWN[0],
              "life": supercomp.PLATE_LIFE[0],
              "points": supercomp.PLATE_POINTS[0], "period": 0,
              "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "plate2": {"behaviour": BOSS, "pictures": "plate2",
               "colour": supercomp.PLATE_OWN[1],
               "life": supercomp.PLATE_LIFE[1],
               "points": supercomp.PLATE_POINTS[1], "period": 0,
               "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "plate3": {"behaviour": BOSS, "pictures": "plate3",
               "colour": supercomp.PLATE_OWN[2],
               "life": supercomp.PLATE_LIFE[2],
               "points": supercomp.PLATE_POINTS[2], "period": 0,
               "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "sturret": {"behaviour": BOSS, "pictures": "sturret",
                "colour": supercomp.TURRET_OWN,
                "life": supercomp.TURRET_LIFE,
                "points": supercomp.TURRET_POINTS, "period": 0,
                "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
    "sccore": {"behaviour": BOSS, "pictures": "sccore",
               "colour": supercomp.CORE_OWN,
               "life": supercomp.CORE_LIFE,
               "points": supercomp.CORE_POINTS, "period": 0,
               "shot": (0, 0.0), "aim": 0, "from": (0, 0)},
})
GUARD_IN_VX = 1.5        # pixels a frame on the screen, coming in
GUARD_OUT_VX = 2.0       # leaving
GUARD_STOP_X = 232       # its x register where it stops (screen 208)
GUARD_SHUT = 60          # frames shut before it opens
GUARD_OPEN = 40          # frames open (its fan at the first)
GUARD_TIMES = 3          # openings, then it leaves
GUARD_SHELL = 200        # its life while shut (the real one aside)
GUARD_TOP, GUARD_LOW = 40, 120   # the lines it follows the ship within
GUARD_FAN_VX = -2
GUARD_FAN_VY = [-1.0, 0.0, 1.0]
GUARD_FAN_FROM = (-8, 2)
EGG_NEAR = 72            # pixels: the ship's x register to the egg's
BAR_LIFE = 100           # its life, given back every frame
# The barriers' cycle (station.asm, st_bar): each barrier in three pieces,
# the energy above the corridor (the level's beams down, characters), its
# middle piece in the corridor (BAR, two sprites), the energy below (the
# beams up); two on at a time, the gap moving («Un varco che cambia posto»:
# above, in the middle, below, in the middle, a quarter of 64 frames each,
# by the frame counter anim); a piece about to come on dimmed for the last
# 16 frames before (its threads: not rock, not met). Their looks by
# sixteenth of the cycle (anim / 16): 0 off, 1 dimmed, 2 on. All the
# barriers at once.
BAR_TOP_LOOKS = [0, 0, 0, 1] + [2] * 12
BAR_MID_LOOKS = [2] * 4 + [0, 0, 0, 1] + [2] * 4 + [0, 0, 0, 1]
BAR_LOW_LOOKS = [2] * 8 + [0, 0, 0, 1] + [2] * 4
BAR_AWAY = 200           # a piece's line while dimmed or off: never met
CRAWL_VX = -0.5          # pixels a frame, against the rock
LMINE_BAND = 10          # lines: the ship's line within this of its own
LMINE_REST = 64          # frames between two rays
LMINE_RAY = [(-6 - 8 * k, 1, -5, 0.0) for k in range(3)]   # dx, dy,
                         # vx (whole pixels), vy: three bolts in a row
HANG_PERIOD = 56         # frames between a hanging turret's shots
HANG_FIRST = 28          # its first, after it comes
# The hanging turret's shots, by its aim (down-left, down,
# down-right): x velocity (whole pixels), y velocity, from its sprite
# (dx, dy): the turret's turned upside down.
HANG_SHOTS = [(-2, 2.0, -12, 7), (0, 3.0, 0, 7), (2, 2.0, 11, 7)]
# Phase 3's kinds take phase 2's slots (the program's tables keep phase
# 2's: the files of levels 3 and 4 write them back, the station's file its
# own; build_assets.py, make_disk.py): never the rock's and the shard's
# (hits.asm splits KIND_ROCK into KIND_SHARD). By table set
# (phases.file_set): 3 level 5's, 4 level 6's (the same phase, the station:
# its kinds in the same slots where it can, its own in the others).
PHASE_KINDS = {3: {15: "sentinel", 16: "tcarrier", 17: "crawler",
                   18: "hcrawler", 21: "defender", 22: "lmine",
                   23: "hturret",
                   25: "aturret", 26: "acore"},
               4: {15: "sentinel", 16: "ccarrier", 17: "crawler",
                   18: "hcrawler", 21: "guardian", 22: "lmine",
                   23: "egg", 24: "barrier",
                   12: "plate", 13: "plate2", 14: "plate3",
                   25: "sturret", 26: "sccore",
                   9: "rubble"}}
KIND_ORDER = ["raider", "drone", "lancer", "leaper", "turret",
              "carrier", "cannon", "core", "interceptor", "dcarrier",
              "gencore", "field", "segment", "shcore", "pod",
              "scout", "gunship", "gcarrier", "mine", "rock", "shard",
              "wgun", "wcore", "hlancer", "scarrier",
              "cturret", "cbridge"]
# The kinds that fire a fan: the gunship's, the gold one's: GUN_FAN_VX
# whole pixels a frame, these y velocities, from the sprite at
# GUN_FAN_FROM.
FANS = ("gunship", "gcarrier")
GUN_FAN_VX = -2
GUN_FAN_VY = [-0.75, 0.0, 0.75]
GUN_FAN_FROM = (-10, 2)
# The mine's shrapnel: (x velocity, y velocity), from MINE_FAN_FROM;
# the ship's x register within MINE_REACH_X pixels of the mine's, its
# line within MINE_REACH_Y of the mine's: it bursts.
MINE_FAN = [(-2, -1.0), (-2, 1.0), (2, -1.0), (2, 1.0)]
MINE_FAN_FROM = (0, 2)
MINE_REACH_X, MINE_REACH_Y = 44, 30
# The shards of a rock: two, one up and one down, from the rock's place
# (its x register; its line + SHARD_DY), on their paths.
SHARD_PATHS = ["shard_up", "shard_down"]
SHARD_DY = [0, 6]
SHARD_RISE = 18           # the lines a shard's path takes it up or down
PICTURES = ["raider", "drone", "lancer", "leaper", "turret"]
# Level 2's pictures come after the boss's parts (build_assets.py): the
# interceptor's four, the core's four, the field's two.
LEVEL2_PICTURES = [("interceptor", 4), ("gencore", 4), ("field", 2),
                   ("segment", 2), ("shcore", 2), ("pod", 2)]
# Level 3's, in the same place (the level's own pictures: build_assets.py):
# two each, the rock's four.
LEVEL3_PICTURES = [("scout", 2), ("gunship", 2), ("mine", 2),
                   ("rock", 4), ("shard", 2),
                   ("wgun", 2), ("wcore", 2)]
# Level 4's: the names it shares with level 3 at the same blocks
# (build_assets.py checks it), the heavy lancer in the rock's.
LEVEL4_PICTURES = [("scout", 2), ("gunship", 2), ("mine", 2),
                   ("hlancer", 4), ("shard", 2),
                   ("cturret", 2), ("cbridge", 2)]
# Level 5's (the first of phase 3: its kinds in phase 2's slots; their
# pictures where level 4's were).
LEVEL5_PICTURES = [("sentinel", 2), ("crawler", 2), ("hcrawler", 2),
                   ("defender", 2), ("lmine", 2), ("hturret", 3)]
# The DEFENSE TURRET ARRAY's: no room for them among level 5's (16 blocks a
# level); in the arena, where no Varkon of the level flies any more, the
# boss's program puts them over the sentinel's and the crawler's
# (defense.asm; build_assets.py: their blocks).
ARRAY_PICTURES = [("aturret", 2), ("acore", 2)]
# Level 6's: level 5's where they are the same, the guardian's in the
# defence fighter's, the egg's in the hanging turret's, the barrier's after
# them.
LEVEL6_PICTURES = [("sentinel", 2), ("crawler", 2), ("hcrawler", 2),
                   ("guardian", 2), ("lmine", 2), ("egg", 2),
                   ("barrier", 4)]
# The SUPER-COMPUTER VARKON's: as the ARRAY's, over level 6's first ones in
# the arena (supercomp.asm; build_assets.py: their blocks).
SC_PICTURES = supercomp.PICTURES
AIM_VY = 0.5             # the drone's shot: half a pixel a frame up/down
AIM_DEAD = 4             # ... unless the ship is within 4 lines
ENEMIES = 12             # slots
SHOTS = 6
FLASH_FRAMES = 3         # white, after a hit that does not destroy

# The turret: the ship more than AIM_SIDE pixels to the left of its
# middle, or to the right, turns the barrel that way (pictures 0 and
# 2; up: 1). The shot of each way: x velocity (whole pixels), y
# velocity (pixels), from the turret's sprite (dx, dy).
AIM_SIDE = 32
TURRET_SHOTS = [(-2, -2.0, -12, -7), (0, -3.0, 0, -7),
                (2, -2.0, 11, -7)]

# The leaper: HOP_FRAMES a hop, walking at LEAP_VX (pixels a frame,
# against the rock); gravity HOP_G (256ths of a pixel a frame, each
# frame). A hop that lands d lines lower than it starts sets off at
#   vy = 8 d - HOP_UP   (256ths a frame)
# so that after 32 frames it is exactly there: 32 vy + HOP_G * 32 *
# 31 / 2 = 256 d. LEAP_FEET: the line of the sprite its feet are on;
# LEAP_FOOT: the pixel of the sprite over the floor it lands on.
HOP_FRAMES = 32
HOP_G = 32
HOP_UP = HOP_G * (HOP_FRAMES - 1) // 2
LEAP_VX = -0.5
LEAP_FEET = 20
LEAP_FOOT = 12
assert 256 * HOP_FRAMES // HOP_FRAMES == 256
assert HOP_UP * HOP_FRAMES == HOP_G * HOP_FRAMES * (HOP_FRAMES - 1) // 2

Y_MIN, Y_MAX = 0, 154


def straight(vx, frames=400):
    """Straight to the left, in stretches of at most 200 frames."""
    out = []
    while frames > 0:
        out.append((min(frames, 200), vx, 0.0))
        frames -= 200
    return out


def sine(vx, amplitude, period, frames):
    """A wave: vy follows a sine, in stretches of 8 frames."""
    out = []
    for k in range(frames // 8):
        phase = 2 * math.pi * (k * 8 + 4) / period
        vy = amplitude * 2 * math.pi / period * math.cos(phase)
        out.append((8, vx, vy))
    return out


def arc(speed, start, turn, frames, steps=12):
    """Turn at a constant speed from angle `start` by `turn` degrees
    (screen angles: 0 right, 90 down, 180 left, 270 up)."""
    out = []
    for k in range(steps):
        a = math.radians(start + turn * (k + 0.5) / steps)
        out.append((frames // steps, speed * math.cos(a),
                    speed * math.sin(a)))
    return out


PATHS = {
    "line": straight(-1.5),
    "fast": straight(-2.5, 220),
    "sine": sine(-1.25, 30, 128, 320),
    "dive": ([(36, -2.0, 1.5)] + arc(2.5, 143, 37, 24, 6) +
             straight(-2.5, 160)),
    "climb": ([(36, -2.0, -1.5)] + arc(2.5, 217, -37, 24, 6) +
              straight(-2.5, 160)),
    "loop": (straight(-2.0, 60) + arc(2.0, 180, 360, 96, 16) +
             straight(-2.0, 220)),
    # a slow line that stops, then leaves fast; a shallow wave for files of
    # drones
    "halt": ([(80, -1.5, 0.0), (60, -0.25, 0.0)] +
             straight(-2.5, 200)),
    "ripple": sine(-1.5, 12, 96, 288),
    # the leaper and the turret do not follow paths: one stretch
    # that never ends (they leave past the left edge)
    "ground": [(255, 0.0, 0.0)],
    # the drones the SIEGE CRAWLER's mouth launches: out of the maw, then
    # up in an arc and on to the left; or low, along the floor (one and the
    # other in turn)
    "launch_up": ([(14, -2.5, 0.0)] + arc(2.0, 180, 50, 36, 6) +
                  [(40, -1.5, -1.0)] + straight(-2.0, 200)),
    "launch_low": [(14, -2.5, 0.0)] + straight(-2.25, 200),
    # level 2's interceptor: from behind, at the left edge (in the border),
    # to the right, past the screen's right edge
    "intercept": [(40, 2.5, 0.0), (90, 3.25, 0.0)],
    # level 3's: the scouts' snake (a file of them on one wave), the rocks
    # adrift, a rock's shards
    "snake": sine(-1.75, 22, 112, 320),
    "drift_down": [(176, -1.0, 0.125), (176, -1.0, 0.125)],
    "drift_up": [(176, -1.0, -0.125), (176, -1.0, -0.125)],
    "shard_up": [(24, -1.5, -0.75), (200, -2.0, 0.0)],
    "shard_down": [(24, -1.5, 0.75), (200, -2.0, 0.0)],
}
# Phase 3's: the sentinel's patrol (in from the right, then once to and
# fro), the defence fighter out of the ceiling (down, then to the left) or
# the floor (up, then to the left). Their stretches take the place of phase
# 2's snake and drifts (PHASE_PATHS): the shards' paths after them keep
# their place (hits.asm).
PATHS.update({
    "patrol": ([(48, -1.5, 0.0), (16, -0.25, 0.0), (40, 0.75, 0.0),
                (16, -0.25, 0.0), (40, -1.5, 0.0), (16, -0.25, 0.0)] +
               straight(-2.0, 200)),
    "emerge_down": ([(24, 0.0, 1.25), (12, -1.0, 0.75)] +
                    straight(-2.5, 220)),
    "emerge_up": ([(24, 0.0, -1.25), (12, -1.0, -0.75)] +
                  straight(-2.5, 220)),
})
PHASE_PATHS = {3: {"snake": "patrol", "drift_down": "emerge_down",
                   "drift_up": "emerge_up"}}
PHASE_PATHS[4] = PHASE_PATHS[3]          # level 6's: the same
PATH_ORDER = ["line", "fast", "sine", "dive", "climb", "loop", "halt",
              "ripple", "ground", "launch_up", "launch_low", "intercept",
              "snake", "drift_down", "drift_up", "shard_up",
              "shard_down"]
LAUNCH_PATHS = ["launch_up", "launch_low"]


def shot_vx(kind):
    """The shot's x velocity: whole pixels a frame (0: the kind does
    not fire, or fires straight up)."""
    vx = KINDS[kind]["shot"][0]
    assert vx == int(vx), kind
    return int(vx)


def fixed(value):
    """256ths of a pixel, as a signed 16-bit number."""
    return round(value * 256) & 0xFFFF


def path_order(phase=2):
    """The paths in their order (a phase's: phase 3's in the place of phase
    2's)."""
    swap = PHASE_PATHS.get(phase, {})
    return [swap.get(name, name) for name in PATH_ORDER]


def segments(phase=2):
    """All the paths' stretches in one list, each path ending with a
    stretch of 0 frames; and where each path starts in it. The ground
    path's stretch starts again (its frames count down from 255 to 0:
    the program keeps it on stretch 255 forever). A phase's: phase 3's
    paths in the place of phase 2's, padded with empty stretches so that
    the paths after them keep their places."""
    if phase not in PHASE_PATHS:
        out, starts = [], []
        for name in PATH_ORDER:
            starts.append(len(out))
            for frames, vx, vy in PATHS[name]:
                assert 1 <= frames <= 255, (name, frames)
                out.append((frames, fixed(vx), fixed(vy)))
            out.append((0, 0, 0))
        assert len(out) <= 256
        return out, starts
    base, base_starts = segments(2)
    swap = PHASE_PATHS[phase]
    first = min(base_starts[PATH_ORDER.index(n)] for n in swap)
    last = max(base_starts[PATH_ORDER.index(n)] + len(PATHS[n]) + 1
               for n in swap)
    out, starts = list(base[:first]), list(base_starts)
    for name in PATH_ORDER:
        if name in swap:
            starts[PATH_ORDER.index(name)] = len(out)
            for frames, vx, vy in PATHS[swap[name]]:
                assert 1 <= frames <= 255, (name, frames)
                out.append((frames, fixed(vx), fixed(vy)))
            out.append((0, 0, 0))
    assert len(out) <= last, (phase, len(out), last)
    out += [(0, 0, 0)] * (last - len(out)) + base[last:]
    assert len(out) == len(base)
    return out, starts


def overlay_range(phase):
    """(first, last + 1): the stretches a phase writes over phase 2's
    (empty: none)."""
    if phase not in PHASE_PATHS:
        return (0, 0)
    base, base_starts = segments(2)
    swap = PHASE_PATHS[phase]
    first = min(base_starts[PATH_ORDER.index(n)] for n in swap)
    last = max(base_starts[PATH_ORDER.index(n)] + len(PATHS[n]) + 1
               for n in swap)
    return (first, last)


def kind_order(phase=2):
    """The kinds by number (a phase's: phase 3's in phase 2's slots)."""
    order = list(KIND_ORDER)
    for slot, name in PHASE_KINDS.get(phase, {}).items():
        order[slot] = name
    return order


def kind_number(name):
    return KIND_ORDER.index(name)


def check(waves, phase=2):
    """Every flyer's path keeps it in the playfield (y 0-154) from
    where its waves start it; the kinds and the waves are well made
    (by the level's phase: its kinds, its paths)."""
    segs, starts = segments(phase)
    order = path_order(phase)
    for column, path, kind, count, spacing, x, y0, step in waves:
        assert kind in KINDS and path in PATHS, (column, kind, path)
        assert kind in kind_order(phase) and path in order, (column, kind)
        behaviour = KINDS[kind]["behaviour"]
        assert (path == "ground") == (behaviour != PATH), (column, kind)
        assert 1 <= count <= ENEMIES and spacing * (count - 1) <= 255
        assert path not in SHARD_PATHS and kind != "shard", column
        if behaviour != PATH:
            continue
        # A rock's shards leave its place SHARD_RISE lines up or down at
        # most: the rock that far from the playfield's edges
        low, high = Y_MIN * 256, (Y_MAX + 1) * 256
        if kind == "rock":
            rise = SHARD_RISE + max(SHARD_DY)
            low, high = low + rise * 256, high - rise * 256
        for k in range(count):
            y = y0 + k * step
            yy = y * 256
            i = starts[order.index(path)]
            while segs[i][0]:
                frames, _, vy = segs[i]
                vy = vy - 65536 if vy >= 32768 else vy
                for _ in range(frames):
                    yy += vy
                    assert low <= yy < high, (column, path, y, yy / 256)
                i += 1
    columns = [w[0] for w in waves]
    assert columns == sorted(columns)
    for kind, data in KINDS.items():
        shot_vx(kind)
        assert 1 <= data["life"] <= 127 and data["points"] % 10 == 0
        assert data["behaviour"] in (PATH, HOP, TURRET, BOSS, STAND, FIELD,
                                     MINE, CRAWL, LMINE, HANG, GUARD,
                                     EGG, BAR, FALL)
        assert (data["period"] == 0) == (data["shot"] == (0, 0.0)) or \
            data["behaviour"] == TURRET, kind
        assert 0 <= data["period"] <= 255
    assert HOP_UP % 1 == 0 and fixed(LEAP_VX) & 0xFF == 0x80
    # The shards' paths: up, then level; down, then level
    for name, sign in zip(SHARD_PATHS, (-1, 1)):
        rise = sum(f * vy for f, _, vy in PATHS[name])
        assert sign * rise <= SHARD_RISE and rise * sign > 0, name
        assert PATHS[name][-1][2] == 0.0
