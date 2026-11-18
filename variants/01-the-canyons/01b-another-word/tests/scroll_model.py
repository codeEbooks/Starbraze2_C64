"""The model of the game: what the program does, frame by frame.

State holds what the test reads from the C64: the camera, the two
screens, the colour RAM, the stars, the fine scrolls, the ship and its
shots (ship_model.py), the Varkon and the multiplexer's plan
(mux_model.py), the sprites. step() is one turn of the main loop,
after the HUD's interrupt, with what the program does for that frame
before it (the stars and rows 0-9 of the colour RAM, behind the beam):
the keys and the joystick, the camera, the swap of the screens or a
step of the back screen, the far layer, the stars, the ship, the plan
of the sprites, the Varkon for the next frame, the end of the level.
The order inside a turn changes nothing the test reads. It follows
the rules of the program, written again in Python from the comments
of the sources, without the program: if the two disagree, the test
says where.

The levels: State.level (0-6) is the program's `level`; each start of a
level takes its files (reference.set_level), as load_level unpacks them:
its characters, the rock's table (rock_lines, make_rock), its colours;
after STAGE CLEAR the next level, after the game's end the first. The
beams (beam_step). The arena reads its rock from the characters only
when the level's boss is the SIEGE CRAWLER (arena_chars); the bosses
(boss_model.py). The escape, level 7 (escape_model.py): its step in
beam_step (beam_module 2), its speed rewritten, its screen white ($d021:
State.d021), the victory's screen (State.hud_view, shown_d018 HUD_D018).
The game held (states.asm): the choice of the ship at the start and
after each ship lost, the pause (SPACE), GAME OVER, then the title
(State.held, its turns held_step: nothing moves, row 1 of the HUD its
message); a new game after the title (State.new_game, the program's
game_start).
"""

from pathlib import Path
import sys

import boss_model
import escape_model
import mux_model
import parts
import player_model
import reference
import ship_model
import varkon_model

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "game/assets"))
import phases  # noqa: E402  the files of the disk
import font    # noqa: E402  the HUD's letters
import title   # noqa: E402  the messages

SCREEN_A, SCREEN_B = 0, 1
D018 = [0x02, 0x12]            # screen $4000 or $4400, characters $4800
HUD_D018 = 0x04                # screen A, the HUD's characters
NEAR_ROWS = list(range(10)) + list(range(14, 22))
COPY_TOP = list(range(10))     # rows 0-9 and 15-21: copied, coloured
COPY_BOTTOM = list(range(15, 22))
# The back screen's stages, one a frame: the rows each copies (and
# whether it takes their stars out of the copy), then the stars of
# rows 0-4, of rows 5-9; the new column in the turn of the swap.
STAGES = [[(range(0, 3), True)], [(range(3, 6), True)],
          [(range(6, 9), True)], [(range(15, 19), False),
                                  (range(9, 10), True)],
          range(5), range(5, 10),       # the stars
          [(range(19, 22), False)]]
FAR_ROWS = [11, 12, 13]        # row 10 is the same all along
READY = len(STAGES)
FIRE = 0x10
# Only for the tests by hand (to be taken out): the keys I and L
# (test_keys: the route gives them as bits 8 and 9 of its keys)
TEST_I, TEST_L = 1, 2
BORDER_RED = 2
# The game held (states.asm): held's values; SPACE (keys bit 0);
# GAME OVER's frames; row 1 of the HUD.
HELD_CHOOSE, HELD_SHIP, HELD_PAUSE, HELD_PAUSED = 1, 2, 3, 4
HELD_OVER, HELD_END = 5, 6
KEY_SPACE = 1
OVER_FRAMES = 150
ROW1 = 880 + 40
JOY_LEFT, JOY_RIGHT, JOY_FIRE = 4, 8, 16
HUD_CODES = {letter: k for k, letter in enumerate(
    [g for g in font.GLYPHS if g != " "], 1)}
HUD_CODES[" "] = 0


def messages():
    """The messages (title.py): (column, colour, codes): ship
    k's name 2 k, its pilot 2 k + 1, PAUSED, GAME OVER."""
    return [(col, colour, [HUD_CODES[ch] for ch in text])
            for col, colour, text in title.messages()]


MESSAGES = messages()
MSG_PAUSE, MSG_OVER = len(MESSAGES) - 2, len(MESSAGES) - 1


class State:
    def __init__(self, files):
        self.files = files
        self.c = files["constants"]
        self.t = files["tables"]
        self.level = 0                        # level 1 first
        self.file = 1                         # the PRG's (file
                                              # 1, phase 1's: phases.py)
        self.stats = {}                       # the levels' counts
        self.charset = bytearray(files["charset"])
        self.rock_lines = bytearray(2048)
        self.frame = 0
        self.restarts = 0
        self.test_prev = 0                    # keys I, L
        self.screens = [bytearray(1024), bytearray(1024)]
        self.colour = bytearray(1000)
        hud = files["hud"]
        self.screens[0][880:1000] = hud[:120]
        self.colour[880:1000] = hud[120:240]
        self.varkon = varkon_model.Varkon(files)
        self.mux = mux_model.Mux(files)
        self.boss = boss_model.Boss(files)
        self.varkon.boss = self.boss
        self.player = player_model.Player()   # sound_init
        self.escape = escape_model.Escape(files)
        self.joy = 0
        self.prev_keys = 0                    # the keys
        self.held, self.held_time = 0, 0      # the game held
        self.joy_prev, self.held_vol = 0, 0
        self.kept = None                      # row 1 of the HUD kept
        self.frame_count = 0                  # the program's
                                              # (the test writes it)
        self.title_now = False                # the escape's end
        self.fresh = False                    # a new game's first
        self.start_level()
        self.new_ship()
        self.plan_sprites()
        self.hud()
        if parts.has("sound"):              # (D.2: the steps, parts.py)
            self.player.set_mode(player_model.START_MODE, self.song())

    def new_ship(self):
        """init_ship: the first ship, to choose (held); its
        counts go on from the ship before (the test's)."""
        stats = self.ship.stats if hasattr(self, "ship") else {}
        self.ship = ship_model.Ship(self.files)
        self.ship.stats = stats
        self.ship.sound = self.varkon.sound = self.player.sfx_start
        self.ship.anim = lambda: self.varkon.anim
        self.ship.chosen = False
        if not parts.has("states"):     # steps 3-15: it flies in
            self.ship.come_in(self.c["START_X"], ship_model.CONTROL)
            return
        self.held = HELD_CHOOSE

    def new_game(self):
        """Fire on the title (game_start): the screens blank
        (init_vic), the HUD drawn (draw_hud), level 1 (its file in
        the store: title_return), the first ship to choose, the score
        from 0 (the record kept), the plan of the sprites, the HUD,
        the music from its start in the mode the title left."""
        self.level = 0
        self.test_prev = 0
        self.held = 0
        self.screens = [bytearray(1024), bytearray(1024)]
        hud = self.files["hud"]
        self.screens[0][880:1000] = hud[:120]
        self.colour[880:1000] = hud[120:240]
        self.start_level()
        self.new_ship()
        self.varkon.score.reset()
        self.prev_keys = 0
        self.plan_sprites()
        self.hud()
        self.player.set_mode(self.player.mode, self.song())
        self.fresh = True                      # (the first turn's
        self.count("a new game")               # compare: a start)

    def title_begin(self):
        """The title (title.asm, from entry or title_return): level 1,
        the SID's volume 15, the title's theme from its start in the
        mode there is (song_start); Fire not taken until it is let go."""
        self.level = 0
        self.held = 0
        self.player.shadow[24] = 0x0F
        if parts.has("songs"):
            self.player.song_start(player_model.SONG["TITLE"])
        else:                   # (D.2) step 16: sound_set, the song
            self.player.set_mode(self.player.mode, self.song())
        self.joy_prev = 0xFF
        self.count("the title")

    def title_frame(self, joy):
        """A frame of the title at title_input: its sound
        (music_play, sfx_play), then the joystick just pushed: Fire
        (True: the game, game_start), Up and Down the mode (sound_set,
        and the capsule's sound as a click)."""
        self.player.frame()
        return self.title_input(joy)

    def title_input(self, joy):
        """title_frame's second half (the test compares the
        sound between): the joystick at title_input."""
        new = joy & ~self.joy_prev & 0xFF
        self.joy_prev = joy
        if new & JOY_FIRE:
            return True
        if new & 3:
            step = -1 if new & 1 else 1
            mode = (self.player.mode + step) % 4
            self.player.set_mode(mode, None if parts.has("songs")
                                 else self.song())  # mode_set: the
                                    # title's theme (D.2: step 16,
                                    # sound_set: level 1's song)
            self.player.sfx_start("capsule")
            self.count("the title: the mode, " + ("Up" if new & 1
                                                  else "Down"))
        return False

    def song(self):
        """The song of the level `level` (sound_set)."""
        return self.files["levels"][self.level]["info"]["constants"][
            "LEVEL_SONG"]

    def count(self, what):
        self.stats[what] = self.stats.get(what, 0) + 1

    def clear_objects(self):
        """Both banks of objects empty; this frame's bank 0."""
        none = (0, 0, 0, 0, 0)
        self.banks = [[none] * mux_model.OBJECTS for _ in range(2)]
        self.bank = 0

    def plan_sprites(self):
        """The ship's sprites (0 and 1) and the multiplexer's plan for
        the frame: the objects of this frame's bank (the ship's shots
        just written), in order, chosen, timed. What the program
        writes before line 50: the ship and the plan's first six, the
        pointers in both screens; the HUD."""
        if not parts.has("varkon"):            # steps 1-3
            self.ship_sprites()
            return
        self.bank ^= 1
        objects = self.banks[self.bank]
        objects[0:4] = self.ship.shot_objects()
        objects[mux_model.FIRST_SAT:] = self.ship.more_objects()
        plan = self.mux.make_plan(objects)
        ship = self.ship.sprites()
        first = []
        for i in range(mux_model.HARDWARE):
            if i < len(plan):
                o, y, x, block, colour, mc = plan[i]
                first.append((True, x, y, block, colour, mc))
            else:
                first.append((False, 0, 0, 0, 0, 0))
        self.first = [s + (n == 1,) if len(s) == 5 else s
                      for n, s in enumerate(ship)] + first
        for screen in self.screens:
            for n, sprite in enumerate(self.first):
                screen[1016 + n] = sprite[3]
        self.hud()
        # what the VIC-II draws this frame: (sprite, x, y, block,
        # colour, multicolour)
        self.drawn = [(n, s[1], s[2], s[3], s[4], s[5])
                      for n, s in enumerate(self.first[:2]) if s[0]]
        self.drawn += [(2 + i % mux_model.HARDWARE, x, y, block, colour,
                        mc) for i, (o, y, x, block, colour, mc)
                       in enumerate(plan)]

    def ship_sprites(self):
        """Steps 1-3, no multiplexer: in step 3 the ship's two sprites
        (ship_sprites; the main loop writes $d015 and $d010 after it),
        their pointers in both screens; the others off. None in steps
        1-2."""
        off = (False, 0, 0, 0, 0, 0)
        if not parts.has("ship"):
            self.first, self.drawn = [off] * 8, []
            return
        ship = self.ship.sprites()
        self.first = [s + (n == 1,) for n, s in enumerate(ship)] + \
            [off] * 6
        for screen in self.screens:
            for n in range(2):
                if self.first[n][0]:
                    screen[1016 + n] = self.first[n][3]
        self.hud()
        self.drawn = [(n, s[1], s[2], s[3], s[4], s[5])
                      for n, s in enumerate(self.first[:2]) if s[0]]

    def hud(self):
        """The HUD's notches, ships, score and best, the boss's bar,
        when it changes."""
        if parts.has("boss"):
            self.boss.hud(self.screens[0])
        if parts.has("ship"):
            self.ship.hud(self.screens[0])
        if parts.has("hits"):
            self.varkon.score.hud(self.screens[0])

    def vic(self):
        """The sprite registers as the program leaves them before line
        50: $d000-$d010, $d015, $d01c (all multicolour but sprite 0),
        $d027-$d02e."""
        positions = bytearray(17)
        enable = 0
        for n, (on, x, y, block, colour, mc) in enumerate(self.first):
            positions[2 * n] = x & 255
            positions[2 * n + 1] = y
            positions[16] |= (x >> 8) << n
            enable |= on << n
        colours = bytes(s[4] for s in self.first)
        multi = 0xFE if parts.has("varkon") else 0x02   # (D.2: step
        return bytes(positions), enable, multi, colours  # 3's)

    # --- the level from its start ----------------------------------

    def start_level(self):
        """Both screens drawn at camera 0, the colour RAM, the stars:
        what init_level does; no Varkon, no objects; no boss (its
        characters the level's again, VARKONIA). First the level's data
        (load_level): its files, its characters, the rock's table, the
        beams off."""
        reference.set_level(self.files, self.level + 1)
        if parts.STEP == 10 and self.c["LEVEL_BOSS"] >= 3:
            self.c["LEVEL_BOSS"] = 0    # (D.2) step 10: level 3's
        self.charset[:] = self.files["charset"]     # arena empty
        # The level's pictures (SPRITES2): the DEFENSE TURRET ARRAY puts
        # its own over level 5's in the arena
        self.sprites2 = bytearray(self.files["sprites2"])
        if parts.has("ship"):
            self.make_rock()
        self.beam_timer = self.c["BEAM_CYCLE"] - 1
        if parts.has("boss"):
            self.boss.reset(self)
        else:                                   # (D.2) steps 1-7:
            self.boss.arena = 0                 # init_level's
        self.escape.reset()                     # (cb_save)
        self.varkon.reset()
        self.mux.reset()
        self.clear_objects()
        self.camera, self.frac = 0, 0
        self.front = SCREEN_A
        self.prep = 0
        self.edge = [0] * 22
        self.far_col = self.far_camera() >> 3
        for screen in self.screens:
            for row in NEAR_ROWS:
                for col in range(40):
                    screen[row * 40 + col] = self.near(col, row)
            for row in range(10, 14):
                for col in range(40):
                    screen[row * 40 + col] = self.far(self.far_col + col,
                                                      row)
        for k, row in enumerate(NEAR_ROWS):    # start_colours
            self.colour[row * 40:row * 40 + 40] = bytes(
                self.t["start_colours"][k * 40:k * 40 + 40])
        for row in range(10, 14):
            colour = self.c[f"FAR_COLOUR_{row}"]
            for col in range(40):
                self.colour[row * 40 + col] = colour
        self.records = [[] for _ in range(10)]   # (column) a row
        self.star_column = [None] * 10
        self.back_records, self.back_column = None, None
        self.plan_speed = self.speed(0)  # camera_plan's
        if not parts.has("scroll"):      # step 1: still
            return
        for row in range(10):
            self.charset[(self.c["STAR_CODE"] + row) * 8:
                         (self.c["STAR_CODE"] + row) * 8 + 8] = bytes(8)
        self.stars(fresh=True)
        self.new_column()                # for the first swap

    def near(self, column, row):
        return reference.near_cell(self.files, column, row)

    def far(self, column, row):
        return reference.far_cell(self.files, column, row)

    def far_camera(self):
        return (self.camera + 1) >> 1

    @property
    def near_xs(self):
        return 7 - (self.camera & 7)

    @property
    def far_xs(self):
        return 7 - (self.far_camera() & 7)

    @property
    def d018(self):
        if self.escape.hud_view:               # the victory
            return HUD_D018
        return D018[self.front]

    @property
    def d021(self):
        """$d021 if the escape has made it white, else None
        (the level's)."""
        return self.escape.d021

    @property
    def hud_view(self):
        return self.escape.hud_view

    # --- one frame -------------------------------------------------

    def speed(self, joy):
        value = 0
        for i in range(self.c["SPEED_COUNT"]):
            start = self.t["speed_at_lo"][i] | self.t["speed_at_hi"][i] << 8
            if self.camera >= start:
                value = self.t["speed_lo"][i] | self.t["speed_hi"][i] << 8
        return value

    @property
    def border(self):
        """$d020, red while the ship cannot be hurt."""
        return BORDER_RED if self.ship.invuln else 0

    def test_keys(self, test):
        """Only for the tests by hand (test_step): the
        keys I and L just pushed. I: the ship unhurtable, or not; L:
        the next level at once if the ship flies. True for L."""
        new = test & ~self.test_prev
        self.test_prev = test
        if new & TEST_I:
            self.ship.invuln = not self.ship.invuln
            self.count("key I: unhurtable" if self.ship.invuln else
                       "key I: hurtable again")
        if new & TEST_L:
            if self.ship.mode == ship_model.CONTROL:
                if self.boss.arena:
                    self.count("key L in the arena")
                return True
            self.count("key L while the ship does not fly: nothing")
        return False

    def phase_need(self, info):
        """The level's file in the store (phase 1's, then a level's own:
        phases.FILES): when it is not there, the program reads it from
        the disk (phase.asm: file_need) in this turn, before the level's
        start."""
        number = phases.file_of(self.level + 1)
        if number != self.file:
            self.file = number
            info["file"] = number
            self.count(f"file {number} from the disk")
            self.escape.file_loaded(number)     # the module's
            phase = phases.file_phase(number)   # its song's
            if phase >= 2:                      # tables (music.py)
                self.player.tables(phase)

    def step(self, joy=0, keys=0):
        """One turn of the main loop; joy: the joystick bits (1 =
        pushed), keys: 1, 2, 3 (bits 0-2), as the program keeps
        them; bits 8-9 the keys I and L (test_keys)."""
        self.frame += 1
        self.joy = joy                          # the escape's
        info = {"swap": False, "hold": False, "far": False,
                "stage": None, "restart": False, "gameover": False,
                "arena": None, "file": None, "held": False,
                "title": False}
        if not parts.has("scroll"):             # step 1: still
            return info
        new_keys = keys & ~self.prev_keys & 0xFF   # (at joy_ready)
        self.prev_keys = keys & 0xFF
        if self.held:                           # the game held
            info["held"] = True
            self.held_step(joy, new_keys, info)
            return info
        if new_keys & KEY_SPACE:                # the pause,
            self.held = HELD_PAUSE              # from the turn's end
            self.count("SPACE: the pause")
        if self.fresh:                          # the first turn
            self.fresh = False                  # of a new game
            info["new_game"] = True
        skip = self.test_keys(keys >> 8)
        keys &= 0xFF
        if self.boss.restart or skip:  # after STAGE CLEAR
            self.boss.restart = False
            self.restarts += 1
            info["restart"] = True
            self.level = (self.level + 1) % parts.levels(
                self.c["LEVEL_COUNT"])          # (D.2: a step's)
            self.count(f"level {self.level + 1} after the key L" if skip
                       else f"level {self.level + 1} after STAGE CLEAR")
            self.phase_need(info)               # the file,
            if parts.has("sound"):
                self.player.set_mode(self.player.mode, self.song())
            self.start_level()
            if self.ship.mode == ship_model.WAIT and \
                    parts.has("states"):        # a ship lost
                self.ship.choose_next(lost=True)  # (the escape's time
                self.ship.chosen = False         # over): to choose
                self.held = HELD_CHOOSE
                self.count("the escape again: another ship to choose")
            else:
                self.ship.again(skip)
            if parts.has("varkon"):             # (D.2: step 3 leaves
                self.no_sprites()               # the ship's sprites)
            if parts.has("sound"):
                self.player.frame()
            return info
        arena = self.boss.arena        # as at the turn's start
        if arena:
            camera, frac = self.camera, self.frac
        else:
            # the speed camera_plan used in the turn before (the escape
            # rewrites the level's speed after it)
            speed = self.plan_speed
            position = (self.camera << 8 | self.frac) + speed
            camera, frac = position >> 8, position & 255
            if camera >= self.c["CAMERA_END"]:
                camera, frac = self.c["CAMERA_END"], 0
            if camera >> 3 != self.camera >> 3:
                if self.prep == READY:
                    info["swap"] = True
                else:
                    info["hold"] = True
                    camera, frac = self.camera | 7, 0
        self.camera, self.frac = camera, frac
        if info["swap"]:
            self.swap()
            self.new_column()            # after the colours
        far_col = self.far_camera() >> 3
        if far_col != self.far_col:
            info["far"] = True
            self.far_col = far_col
            self.far_rows(self.screens[SCREEN_A])
        if not info["swap"] and not arena:
            info["stage"] = self.prep
            # under a pixel a frame (the speed that brought the camera
            # here), the camera on to its next pixel next frame: no step
            if speed < 256 and frac + speed >= 256:
                info["stage"] = "waits"
            else:
                self.prepare()
        self.stars()
        if parts.has("ship"):                   # (D.2: from step 3)
            self.ship.step(self, joy, keys)
        if self.ship.chosen:                    # another ship
            self.ship.chosen = False            # to choose: held from
            self.held = HELD_CHOOSE             # the next turn
        self.plan_sprites()
        if parts.has("varkon"):                 # (D.2: the shots)
            self.ship.shots_rock(self)
        if self.ship.gameover:                  # GAME OVER from
            info["gameover"] = True             # the next turn
            self.held = HELD_OVER
        if parts.has("sound"):                  # (D.2: steps 7-16,
            self.player.keys(new_keys, None if parts.has("songs")
                             else self.song())  # the level's song)
        if arena and parts.has("boss"):
            info["arena"] = self.boss.draw(self)
        self.next_camera = self.plan_next()
        if parts.has("varkon"):
            self.varkon.update(self)
        if self.title_now:              # the victory's end: the
            self.title_now = False      # title (title_return), the
            self.level = 0              # turn ends there
            self.phase_need(info)
            info["title"] = True
            return info
        if parts.has("varkon"):
            self.banks[self.bank ^ 1][mux_model.FIRST_ENEMY:
                                      mux_model.FIRST_SAT] = \
                self.varkon.objs
            self.mux.update_priorities()
            self.mux.sort(self.banks[self.bank ^ 1])
        self.hud()
        if parts.has("sound"):
            self.player.frame()
        return info

    # --- the game held -----------------------------------------------

    def held_step(self, joy, new_keys, info):
        """A turn held (held_turn): the frame's picture again; the
        joystick just pushed; the choice (its start: row 1 kept, the
        ship's name; Left, Right another ship; Fire: it flies), the
        pause (SPACE: on again), GAME OVER (its start, its wait, then
        the title: info["title"], phase 1's file)."""
        self.held_picture()
        new = joy & ~self.joy_prev & 0xFF
        self.joy_prev = joy
        ship = self.ship
        if self.held == HELD_PAUSE:
            self.held_begin(joy)
            self.say(MSG_PAUSE)
            self.held = HELD_PAUSED
            return
        if self.held == HELD_PAUSED:
            if new_keys & KEY_SPACE:
                self.held_off(info)
                self.count("SPACE again: the game on")
            return
        if self.held == HELD_OVER:
            self.held_begin(joy)
            if parts.has("songs"):                      # (D.2)
                self.player.shadow[24] = self.held_vol      # its
                self.player.song_start(player_model.SONG["OVER"])
            self.say(MSG_OVER)
            self.held_time = OVER_FRAMES
            self.held = HELD_END
            self.count("GAME OVER")
            return
        if self.held == HELD_END:
            if parts.has("songs"):                      # (D.2)
                self.player.music_play()
            self.held_time -= 1
            if self.held_time == 0:             # title_return
                self.held = 0
                self.level = 0
                self.phase_need(info)
                info["title"] = True
                self.count("GAME OVER: the title")
            return
        if self.held == HELD_CHOOSE:
            self.held_begin(joy)
            self.held = HELD_SHIP
            self.shown()
            self.count("the choice of the ship")
        elif new & JOY_FIRE:
            ship.go()
            self.held_off(info)
            self.count(f"ship {ship.type + 1} chosen: it flies")
            return
        elif new & (JOY_LEFT | JOY_RIGHT):
            k = ship.type + (1 if new & JOY_RIGHT else -1)
            ship.type = k % self.c["SHIP_COUNT"]
            self.shown()
            self.count("the choice: " + ("Right" if new & JOY_RIGHT
                                         else "Left"))
        ship.blink = self.frame_count >> 1 & 255

    def held_picture(self):
        """held_picture: the ship's sprites again (as ship_sprites),
        the plan the same."""
        ship = self.ship.sprites()
        self.first[:2] = [s + (n == 1,) for n, s in enumerate(ship)]
        for screen in self.screens:
            for n in range(2):
                screen[1016 + n] = self.first[n][3]
        self.drawn = [d for d in self.drawn if d[0] >= 2]
        self.drawn[:0] = [(n, s[1], s[2], s[3], s[4], s[5])
                          for n, s in enumerate(self.first[:2]) if s[0]]

    def held_begin(self, joy):
        """The sound's volume kept, then 0; the joystick now; row 1
        of the HUD kept."""
        self.held_vol = self.player.shadow[24]
        self.player.shadow[24] &= 0xF0
        self.joy_prev = joy
        self.kept = (bytes(self.screens[0][ROW1:ROW1 + 40]),
                     bytes(self.colour[ROW1:ROW1 + 40]))

    def held_off(self, info):
        """The game on again: row 1 as it was, the volume; the rows
        0-9 of the turn held from (ahead: info["resumed"])."""
        info["resumed"] = True
        codes, colours = self.kept
        self.screens[0][ROW1:ROW1 + 40] = codes
        self.colour[ROW1:ROW1 + 40] = colours
        self.player.shadow[24] = self.held_vol
        self.held = 0

    def shown(self):
        """ship_shown: the ship chosen, its weapon at the level it
        had, its full shield; row 1 blank, its name and its pilot;
        the HUD (update_hud)."""
        ship = self.ship
        ship.choose(ship.type)
        self.screens[0][ROW1:ROW1 + 40] = bytes(40)
        self.say(2 * ship.type)
        self.say(2 * ship.type + 1)
        ship.hud(self.screens[0])   # (update_hud: the score, the bar
                                    # unchanged, not written again)

    def say(self, k):
        """hud_say: message k into row 1."""
        col, colour, codes = MESSAGES[k]
        for j, code in enumerate(codes):
            self.screens[0][ROW1 + col + j] = code
            self.colour[ROW1 + col + j] = colour

    def plan_next(self):
        """The camera of the next turn, as camera_plan makes it in
        this turn (after the back screen's step): on by the speed of
        the level; at a new column, the last pixel of this one if the
        back screen is not ready. It stops at CAMERA_END:
        there already, the arena (the boss's turns from now)."""
        end = self.c["CAMERA_END"]
        self.plan_speed = self.speed(0)        # (kept)
        position = (self.camera << 8 | self.frac) + self.plan_speed
        camera, frac = position >> 8, position & 255
        if camera >= end:
            camera, frac = end, 0
            if self.camera == end:
                if not self.boss.arena:
                    self.boss.count("the arena")
                self.boss.arena = 1
                if self.c["LEVEL_BOSS"] == 1:      # the crawler's
                    self.boss.arena_chars = 1      # body: the rock from
                return camera, frac                # the characters
        if camera >> 3 != self.camera >> 3 and self.prep != READY:
            camera, frac = self.camera | 7, 0
        return camera, frac

    def no_sprites(self):
        """The end of the level: all sprites off."""
        self.first = [(False, 0, 0, 0, 0, 0)] * 8
        self.drawn = []

    def swap(self):
        """The back screen in front; its stars, put there in stage 5,
        are now the front's. The colour RAM: rows 0-9 move in the
        frame before (after the test has read it), rows 15-21 in the
        turn: at frame_ready all of them have."""
        self.front ^= 1
        self.records, self.star_column = \
            self.back_records, self.back_column
        for row in COPY_TOP + COPY_BOTTOM:
            base = row * 40
            self.colour[base:base + 38] = self.colour[base + 1:base + 39]
            self.colour[base + 38] = self.edge[row]
        self.prep = 0

    def far_rows(self, screen):
        """The far layer one column on in a screen: screen A's, which
        shows rows 11-13 whichever screen is in front (screen B's are
        never shown)."""
        for row in FAR_ROWS:
            base = row * 40
            screen[base:base + 38] = screen[base + 1:base + 39]
            screen[base + 38] = self.far(self.far_col + 38, row)

    def new_column(self):
        """The level's column camera / 8 + 39 into column 38 of the back
        screen, its colours for the next swap (swap_back: in the turn of
        the swap, after its colours, and at the level's start); the back
        screen's star records anew."""
        back = self.screens[self.front ^ 1]
        column = (self.camera >> 3) + 39
        for row in COPY_TOP + COPY_BOTTOM:
            code = self.near(column, row)
            back[row * 40 + 38] = code
            self.edge[row] = reference.cell_colour(self.files, column,
                                                   row)
        self.back_records, self.back_column = [], []

    def prepare(self):
        """One stage of the back screen (STAGES), if it is not
        ready."""
        if self.prep >= READY:
            return
        front = self.screens[self.front]
        back = self.screens[self.front ^ 1]
        stage = STAGES[self.prep]
        if isinstance(stage, range):           # the stars
            self.back_stars(back, stage)
        else:
            for rows, stars in stage:
                for row in rows:
                    base = row * 40
                    back[base:base + 38] = front[base + 1:base + 39]
                    if stars:                  # no stars in the copy
                        sky = self.t["star_sky"][row]
                        for col in self.records[row]:
                            if col >= 1:
                                back[base + col - 1] = sky
        self.prep += 1

    # --- the stars -------------------------------------------------

    def star_place(self, row, camera=None):
        """The first cell of the row's ring and the pixel of its star,
        at the camera: (column 0-39, pixel 0-7)."""
        if camera is None:
            camera = self.camera
        plane = self.t["star_plane"][row]
        shift = (camera >> 3, camera >> 2,
                 (camera >> 2) + (camera >> 3))[plane]
        value = (self.t["star_pixel"][row] - 7 + (camera & 7)
                 - shift) % 320
        return value >> 3, value & 7

    def put_stars(self, screen, row, column):
        """The row's stars into a screen from the ring's first cell,
        where the cell is the row's blank sky: their columns."""
        code = self.c["STAR_CODE"] + row
        sky = self.t["star_sky"][row]
        first = self.t["star_first"][row]
        last = self.t["star_first"][row + 1]
        put = []
        for k in self.t["star_cells"][first:last]:
            col = (column + k) % 40
            if col <= 38 and screen[row * 40 + col] == sky:
                screen[row * 40 + col] = code
                put.append(col)
        return put

    def back_stars(self, back, rows):
        """Stages 4 (rows 0-4) and 5 (rows 5-9): the stars of the back
        screen, where they will be when the screens swap (the camera at
        the next column's first pixel: speeds are at most 1 pixel a
        frame)."""
        camera = ((self.camera >> 3) + 1) << 3
        for row in rows:
            column, _ = self.star_place(row, camera)
            self.back_column.append(column)
            self.back_records.append(self.put_stars(back, row, column))

    def stars(self, fresh=False):
        """The stars of rows 0-9 in the front screen: the row's star
        character gets its pixel; where the ring has moved, the old
        cells get the blank sky back and the new ones the star. After
        a swap the cells are already there (stage 5). fresh: none yet
        (the start of the level)."""
        front = self.screens[self.front]
        for row in range(10):
            column, pixel = self.star_place(row)
            code = self.c["STAR_CODE"] + row
            line = self.t["star_line"][row]
            self.charset[code * 8 + line] = 0x80 >> pixel
            if not fresh and column == self.star_column[row]:
                continue
            sky = self.t["star_sky"][row]
            if not fresh:
                for col in self.records[row]:
                    front[row * 40 + col] = sky
            self.star_column[row] = column
            self.records[row] = self.put_stars(front, row, column)

    # --- the rock and the beams --------------------------------------

    def make_rock(self):
        """rock_lines: line L of each character at L * 256 + its code;
        nothing for the kept codes (under FIRST_SOLID) and the scenery
        (from DECOR_FIRST)."""
        first, decor = self.c["FIRST_SOLID"], self.c["DECOR_FIRST"]
        for code in range(256):
            solid = first <= code < decor
            for line in range(8):
                self.rock_lines[line * 256 + code] = \
                    self.charset[code * 8 + line] if solid else 0

    def beam_step(self):
        """One frame of the beams' cycle (update_varkon, after the
        boss): the beams down dimmed at BEAM_DOWN_DIM (those up off),
        on at BEAM_DOWN_ON; off at BEAM_UP_DIM (those up dimmed); those
        up on at BEAM_UP_ON. Not in the arena, where their codes may
        be STAGE CLEAR's letters."""
        c = self.c
        if not parts.has("level2"):     # (D.2: from step 9)
            return
        if c.get("BEAM_MODULE") == 2:   # the engine's beams,
            self.plain_beams()          # then the escape's code
            self.escape.step(self)      # (unpacked by the module)
            return
        if c.get("BEAM_MODULE"):        # level 6's: the
            self.varkon.module_beams(self)   # station's module's
            return
        self.plain_beams()

    def plain_beams(self):
        """The engine's cycle (beam_plain)."""
        c = self.c
        if not c["BEAM_DOWN"] or self.boss.arena:   # (none in the
            return                                  # arena)
        self.beam_timer = (self.beam_timer + 1) & (c["BEAM_CYCLE"] - 1)
        t = self.beam_timer
        down, up = c["BEAM_DOWN"], c["BEAM_UP"]
        if t == c["BEAM_DOWN_DIM"]:
            self.set_beam(up, 0)
            self.set_beam(down, 1)
            self.count("the beams up off, down dimmed")
        elif t == c["BEAM_DOWN_ON"]:
            self.set_beam(down, 2)
            self.count("the beams down on")
        elif t == c["BEAM_UP_DIM"]:
            self.set_beam(down, 0)
            self.set_beam(up, 1)
            self.count("the beams down off, up dimmed")
        elif t == c["BEAM_UP_ON"]:
            self.set_beam(up, 2)
            self.count("the beams up on")

    def set_beam(self, code, look):
        """The beam's character: off (0), dimmed (1), on (2, rock)."""
        data = self.t["beam_bytes"][look * 8:look * 8 + 8]
        self.charset[code * 8:code * 8 + 8] = bytes(data)
        for line in range(8):
            self.rock_lines[line * 256 + code] = \
                data[line] if look == 2 else 0
