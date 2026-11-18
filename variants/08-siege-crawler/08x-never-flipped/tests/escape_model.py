"""A model of the escape: game/src/escape.asm and its start in the
station's module (station.asm, es_beams), written again from their
rules, for the test (tests/verify_game.py) to compare the program with,
frame by frame.

The escape is the seventh level (game/assets/escape.py), in level 6's
file. The station's module unpacks the escape's code a piece a frame
at its start (ES_PIECES frames: its count is the module's, 0 again
whenever a file brings the module: phase_need); then every frame the
escape's step (from the engine's beam_step, before the Varkon), and
for a falling piece (FALL) its own way (part). Its steps:
  START  TIME 60 in the HUD (where VARKONIA is), the pieces' pictures
         into the egg's blocks;
  IN     the countdown (a second every 50 frames), the scroll a pixel
         a frame while the ship flies in the right half (ES_FAST_X),
         half a pixel otherwise; the time over: the ship explodes (a
         ship less; key I: the escape again at once), the escape again
         once it has (no ships left: the engine's game over); the way
         out (the camera at ES_OUT): OUT;
  OUT    the time stops; a pixel a frame until ES_STOP, then none; a
         fireball every ES_BOOM_EVERY frames on the station's last
         plates, ES_BOOMS of them, the last with the screen white
         ES_FLASH frames (top_d021: the HUD's interrupt writes $d021
         at line 227, so from the frame after the next); then the ship
         flies off; gone, the
         camera still, the back screen made: END;
  END    the victory's screen (rows 0-21 of screen A blank, a quarter a
         turn, then its texts; screen A in the HUD's characters); then
         every ES_COUNT_EVERY frames a second left, then a notch of the
         shield, into the score (1 000 each), counted down on the
         screen; then, after
         ES_FIRE_AFTER frames Fire, after ES_END_WAIT anyway: a new
         game (three ships, the weapons new, the score from 0, level 1:
         PHASE1 from the disk).
"""

import parts                           # (D.2) the steps of the chain
import player_model                    # the songs
import ship_model

READY = 7                                # the back screen made
QUARTERS = 4                             # END: rows 0-21 blank in
                                         # four turns

ST_START, ST_IN, ST_OUT, ST_END = range(4)
NAMES = ["START", "IN", "OUT", "END"]
FREE, FLYING, BOOM = 0, 1, 2
BOSS = 3                                 # the parts' behaviour
JOY_FIRE = 16
SCREEN_A = 0x4000


class Escape:
    def __init__(self, files):
        self.files = files
        self.c = files["constants"]
        self.es = files["escape"]["numbers"]   # escape.json: its
        self.stats = {}
        self.pieces = 0                    # the module's count
        self.reset()

    def count(self, what):
        self.stats[what] = self.stats.get(what, 0) + 1

    def reset(self):
        """At each level's start (boss_reset: its variables 0)."""
        self.state = ST_START
        self.frames = self.secs = self.dead = 0
        self.timer = self.k = self.left = self.shown = 0
        self.top = None                    # top_d021: the white
        self.d021 = None                   # flash; $d021 shown (the
                                           # HUD's interrupt's, line
                                           # 227: the turn before's)
        self.hud_view = False              # END: screen A, HUD's set
        self.wrote = False                 # this turn: screen A's rows
                                           # 0-21 written (the beam on
                                           # them: not a picture)

    def variables(self):
        """Its eight bytes (cb_save)."""
        return bytes([self.state, self.frames, self.secs, self.dead,
                      self.timer & 255, self.k & 255, self.left,
                      self.shown])

    def file_loaded(self, number):
        """A file brings the station's module (phases: 4 and 5): its
        count from 0."""
        if number in (4, 5):
            self.pieces = 0

    # --- every frame (the module's es_beams) --------------------------

    def step(self, state):
        self.d021 = self.top               # (from line 227 before)
        self.wrote = False
        if self.pieces < self.es["ES_PIECES"]:
            self.pieces += 1
            self.count("the escape's code: a piece unpacked")
            return
        getattr(self, "step_" + NAMES[self.state].lower())(state)

    def set_speed(self, state, value):
        t = state.t                        # (new lists: the level's own
        t["speed_lo"] = [value & 255] + list(t["speed_lo"][1:])  # stay
        t["speed_hi"] = [value >> 8] + list(t["speed_hi"][1:])   # as
                                                                 # read)

    def hud_time(self, state):
        c = self.c
        cell = 880 + c["HUD_BAR"] + self.es["ES_TIME_DIGITS"]
        screen = state.screens[0]
        screen[cell] = c["DIGIT_CODE"] + self.secs // 10
        screen[cell + 1] = c["DIGIT_CODE"] + self.secs % 10

    def step_start(self, state):
        c, es, t = self.c, self.es, state.t
        cell = 880 + c["HUD_BAR"]
        for k, code in enumerate(t["es_time_text"]):
            state.screens[0][cell + k] = code
            state.colour[cell + k] = es["ES_TIME_COLOUR"]
        at = es["ES_RUBBLE_AT"] - c["SPRITES2"]
        state.sprites2[at:at + len(t["es_rubble"])] = bytes(
            t["es_rubble"])
        self.secs, self.frames = es["ES_SECONDS"], 0
        self.hud_time(state)
        self.state = ST_IN
        self.count("the escape: TIME 60")
        self.set_speed(state, es["ES_SLOW"])

    def again(self, state, why):
        state.level = self.es["ES_LEVEL"] - 1
        state.boss.restart = True
        self.count("the escape again from its start")
        self.count(f"the escape again: {why}")

    def step_in(self, state):
        es, ship = self.es, state.ship
        if self.dead:
            if ship.mode == ship_model.WAIT:
                if not ship.lives and not parts.has("states"):
                    ship.lives = state.c["LIVES"]   # (D.2) step 15:
                    self.count("the escape: no ships left, three "
                               "more")              # three more
                if ship.lives:
                    self.again(state, "the ship exploded, a ship less")
                else:
                    self.count("the escape: no ships left (the game "
                               "over)")
            return
        if state.camera >= es["ES_OUT"]:
            self.left = self.secs
            self.timer = self.k = 0
            self.state = ST_OUT
            self.count("the escape: out of the station")
            self.set_speed(state, es["ES_FAST"])
            return
        self.frames += 1
        if self.frames >= 50:
            self.frames = 0
            self.secs -= 1
            self.hud_time(state)
            if self.secs == 0:
                self.count("the escape: the time over")
                if ship.invuln:
                    self.again(state, "the time over, unhurtable")
                    return
                if ship.mode in (ship_model.EXPLODE, ship_model.WAIT):
                    self.count("the escape: the time over, the ship "
                               "down already")
                    self.dead = 1
                    return
                if ship.mode != ship_model.CONTROL:
                    self.again(state, "the time over, the ship coming "
                               "in")
                    return
                if ship.blink:          # blinking: no longer, or
                    self.count("the escape: the time over, the ship "
                               "blinking")      # hurt does nothing
                ship.blink = 0
                ship.hurt(es["ES_ALL_NOTCHES"], "the time over")
                self.count("the escape: the time over, the ship "
                           "explodes")
                self.dead = 1
                return
        if ship.mode == ship_model.CONTROL and \
                ship.x >= es["ES_FAST_X"]:
            self.set_speed(state, es["ES_FAST"])
            self.count("the escape: a pixel a frame")
        else:
            self.set_speed(state, es["ES_SLOW"])
            self.count("the escape: half a pixel a frame")

    def step_out(self, state):
        es, v, ship = self.es, state.varkon, state.ship
        if state.camera >= es["ES_STOP"]:
            self.set_speed(state, 0)
        if self.k < es["ES_BOOMS"]:
            self.timer += 1
            if self.timer < es["ES_BOOM_EVERY"]:
                return
            self.timer = 0
            i = next((n for n, on in enumerate(v.on) if on == FREE),
                     None)                 # (free_varkon)
            if i is not None:
                state.mux.set_pri(4 + i, 2)
                v.on[i] = BOOM
                v.kind[i] = self.c["KIND_CORE"]
                v.left[i] = v.flash[i] = v.cap[i] = 0
                k = self.k & 7
                v.y[i] = state.t["es_boom_y"][k] << 8 | (v.y[i] & 255)
                x = es["ES_HULL"] + 24 - state.camera - \
                    state.t["es_boom_dx"][k]
                if x < 0:
                    x = 24
                v.x[i] = (x & 0xFFFF) << 8
                self.count("the escape: the station blows up")
            else:
                self.count("the escape: a fireball, no free Varkon")
            v.sound("explode")
            self.k += 1
            if self.k == es["ES_BOOMS"]:
                self.top = es["ES_WHITE"]
                self.timer = es["ES_FLASH"]
                self.count("the escape: the screen white")
            return
        if self.timer:
            self.timer -= 1
            if not self.timer:
                self.top = None
        if ship.mode in (ship_model.CONTROL, ship_model.ENTER):
            ship.mode = ship_model.LEAVE
            ship.blink = 0
            ship.count("the ship flies off")
            return
        if ship.mode == ship_model.GONE and \
                (state.t["speed_lo"][0] | state.t["speed_hi"][0]) == 0 \
                and state.prep == READY:
            self.timer = self.k = self.shown = 0
            if parts.has("songs"):              # (D.2: step 17)
                state.player.song_start(player_model.SONG["WIN"])
            self.state = ST_END
            self.count("the escape: the victory")

    def step_end(self, state):
        es, ship, v = self.es, state.ship, state.varkon
        if self.shown <= QUARTERS:         # the screen: rows 0-21
            k = self.shown                 # blank, a quarter a turn,
            self.shown += 1                # then its texts
            if k < QUARTERS:
                self.blank(state, k)
            else:
                self.victory(state)
            return
        self.k += 1
        if self.k >= es["ES_COUNT_EVERY"]:
            self.k = 0
            if self.left:
                self.left -= 1
                self.bonus(state)
                self.count("the escape: a second into the score")
                return
            if ship.shield:
                ship.shield -= 1
                self.bonus(state)
                self.count("the escape: a notch into the score")
                return
        if self.left or ship.shield:
            return
        self.timer = (self.timer + 1) & 255
        if self.timer < es["ES_FIRE_AFTER"]:
            return
        if state.joy & JOY_FIRE or self.timer >= es["ES_END_WAIT"]:
            self.new_game(state)

    def bonus(self, state):
        boss = state.boss
        state.varkon.score.add(boss.notch_points(), state.ship)
        state.varkon.sound("capsule")
        self.counts(state)

    def counts(self, state):
        c, es = self.c, self.es
        self.wrote = True
        screen = state.screens[0]
        screen[es["ES_TIME_CELL"]] = c["DIGIT_CODE"] + self.left // 10
        screen[es["ES_TIME_CELL"] + 1] = c["DIGIT_CODE"] + self.left % 10
        screen[es["ES_SHIELD_CELL"]] = c["DIGIT_CODE"] + \
            state.ship.shield

    def blank(self, state, k):
        """A quarter of rows 0-21 of screen A blank: code 0, colour
        0."""
        size = 880 // QUARTERS
        for cell in range(k * size, (k + 1) * size):
            state.screens[0][cell] = 0
            state.colour[cell] = 0
        self.wrote = True
        self.count("the escape: the victory's screen blank, a quarter")

    def victory(self, state):
        screen, t = state.screens[0], state.t
        data, k = t["es_texts"], 0
        while data[k + 1]:
            at = (data[k] | data[k + 1] << 8) - SCREEN_A
            colour, n = data[k + 2], data[k + 3]
            for j in range(n):
                screen[at + j] = data[k + 4 + j]
                state.colour[at + j] = colour
            k += 4 + n
        self.counts(state)
        self.hud_view = True
        self.count("the escape: the victory's screen")

    def new_game(self, state):
        """«Fine partita, poi partita nuova»: the title first
        (title_return: the turn ends there; State.step), then the new
        game (State.new_game)."""
        if not parts.has("states"):     # (D.2) step 15: the game
            state.level = -1            # again from level 1, the
            state.boss.restart = True   # score, the ships, the weapons
            self.count("the escape: the game again from level 1")
            return
        state.title_now = True
        self.count("the escape: the title")
