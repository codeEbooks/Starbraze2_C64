"""The model of the bosses: the SIEGE CRAWLER in the arena, written
again from game/src/boss.asm's rules and comments, without the program:
the test compares the two frame by frame.

The arena: the camera stopped at CAMERA_END (State.plan_next sets
`arena`). From the next turn the screens do no work; the boss:
  - draw() (the main loop, after the sprites): the body's characters
    into the set the screen does not show, columns 0-7 in a turn,
    8-14 in the next one, then the flip: rows 15-18 of screen A take
    that set's codes where the body is (the columns it leaves
    emptied);
  - update() (update_varkon, after the plasma, before the Varkon
    move): the step's work (WAIT, ENTER, FIGHT, OPEN, CORE, CHAIN,
    WRECK, CLEAR, DONE), the parts put on the body for the frame after
    the next, the bar, the hull's colours, STAGE CLEAR, the shield into
    the score, the level again (restart);
  - hud(): the bar's cells in the HUD.
The parts are Varkon of varkon_model.py (kind cannon, core: behaviour
BOSS); the drones of the mouth are drones on the paths launch_up and
launch_low. A level may have no boss (LEVEL_BOSS 0, the escape): when
WAIT ends, STAGE CLEAR at once.

The engine is common (LEVEL_BOSS 1 the SIEGE CRAWLER, 2 the SHIELD CORE
of level 2, game/src/core.asm, 3-6 the bosses below): WAIT, CHAIN,
WRECK, CLEAR, DONE are the same; the SHIELD CORE has its own start
(core_begin: seven free Varkon; the arena's cells under the sphere kept,
in its codes the characters they show, not rock), its steps ENTER, FIGHT
and RAGE (core_enter, core_fight), its parts' places (core_place: the
four segments turning around the core, one open in turn; the core; the
two pods), its pictures (two each). Its sphere is drawn by draw()
(sphere_draw, early in the next turn): what update() asked for
(cb_paint: its cells on, its colours, white, the arena's cells again)
and, in ENTER, two lines of its characters a frame from its equator. The
segments can be destroyed (varkon_model.py): one destroyed is not placed
again (core_place), its gap stays open.

Level 3's boss, the GRAVEYARD WARDEN (LEVEL_BOSS 3,
game/src/warden.asm): its own WAIT's end (w_begin: the arena's cells
under its columns kept, rows 10-14 rock - air_rock - the far layer's
codes out of the rock's table, its patches to make), ENTER (it comes
down from above the screen), FIGHT (its four ports open in turn, a gun
in each, its fans; a gun destroyed breaks its port off, two shards of
level 3's), BARE (no port left: the core's pit opens), CORE (the core's
fight, faster under half its life, shards from it), CHAIN (on its
body); its body drawn by draw() (w_draw: the patches into its drawing
and two columns of the other set a turn, their lines into the rock's
table, the nebula's pixels where it has none over rows 11-13; then the
flip: its rows on screen A, the rows it leaves the arena's cells
again); its colours (w_paint).

Level 4's boss, the VARKON CORVETTE (LEVEL_BOSS 4,
game/src/corvette.asm): in WAIT the three other phases of its drawing
made from phase 0, a column a turn (c_make); its WAIT's end (c_begin:
four free Varkon, its turrets; the arena's cells under its way kept,
rows 10-14 rock, the far layer's codes out of the rock's table; the
body at the right, off the screen), ENTER (in from the right, a step
at a new body), FIGHT (back and forth; the turrets' fans; the hangar's
scouts), OPEN (all four turrets destroyed: the bridge's wait), CORE
(the dome on the bridge, faster under half its life), CHAIN (on its
body); its body drawn by draw() (c_draw: two columns of the other set
a turn, cell by cell, their lines into the rock's table, the far
layer's pixels where it has none in the cells cv_mask names; then the
flip: its columns on screen A's rows 8-12, the columns it leaves the
arena's cells again); its colours by row (c_paint).

Level 5's boss, the DEFENSE TURRET ARRAY (LEVEL_BOSS 5,
game/src/defense.asm): in WAIT its characters made, four codes a turn
(their lines into the rock's table, its ray's not), then, no Varkon
flying or exploding, its parts' pictures over the level's first ones
(d_codes, d_picture: state.sprites2); its WAIT's end (d_begin: rows
10-14 rock, the far layer's codes out of the rock's table, the
turrets' lives), ENTER (a row of its cells more every
DT_ENTER_EVERY frames, drawn in the next turn), FIGHT (its rows in
turn: shut, half open, open with their two turrets, back in after
DT_OPEN_FRAMES; a row whose turrets are destroyed stays open), OPEN
(the core's hatch, then its lens), CORE (calm, its aimed shots; it
warns, its colours in turn; its ray along rows 10-11, the ship on its
lines hurt), CHAIN (on the wall); its wall drawn by draw() (d_draw: a
row of it, a patch, the ray on or off, the ray's shimmer, one a turn);
its colours (d_paint).

Level 6's boss, the SUPER-COMPUTER VARKON (LEVEL_BOSS 6,
game/src/supercomp.asm): its model in supercomp_model.py, a part of
this one (Boss takes its routines: s_draw, s_step, s_paint).
"""

import parts                          # (D.2) the steps of the chain
import player_model                   # the songs
from supercomp_model import SuperComputer

ST_WAIT, ST_ENTER, ST_FIGHT, ST_OPEN, ST_CORE = range(5)
ST_CHAIN, ST_WRECK, ST_CLEAR, ST_DONE = range(5, 9)
ST_RAGE = 3                    # the SHIELD CORE's 3
NAMES = ("WAIT", "ENTER", "FIGHT", "OPEN", "CORE", "CHAIN", "WRECK",
         "CLEAR", "DONE")
# The SHIELD CORE's steps, by its state
CORE_STEPS = ("step_wait", "core_enter", "core_fight", "core_fight",
              "step_done", "step_chain", "step_wreck", "step_clear",
              "step_done")
FREE, FLYING, BOOM, CAPSULE = 0, 1, 2, 3
BOSS = 3
BOSS_PRI = 8
COLUMNS = 15
ROW = 15                       # the body's first row
LEAVE = 4                      # ship modes (ship_model)
GONE = 5
ENTER = 3
CONTROL = 0
HUD_CELL = 880


class Boss(SuperComputer):
    def __init__(self, files):
        self.files = files
        self.c = files["constants"]
        self.t = files["tables"]
        self.stats = {}
        self.restart = False
        self.reset_values()
        # The WARDEN's drawing (w_comp) and the arena's cells under it
        # (w_save_code, w_save_col): its own memory, not cleared at a
        # level's start
        self.wd_comp = bytearray(self.t["wd_comp"])
        self.wd_save_code = [0] * (self.c["W_ROWS"] * 8)  # (8 a row)
        self.wd_save_col = [0] * (self.c["W_ROWS"] * 8)
        # The CORVETTE's: its phases 1-3 (at CV_PHASES), the arena's cells
        # under its way (cv_save_code, cv_save_col)
        c = self.c
        self.cv_phases = [bytearray(c["CV_PHASE_BYTES"])
                          for _ in range(3)]
        n = c["CV_ROWS"] * c["CV_SAVE_COLS"]
        self.cv_save_code = [0] * n
        self.cv_save_col = [0] * n
        # The ARRAY's: the arena's cells under its ray (DT_SAVE: codes,
        # colours of rows 10-11)
        self.dt_save = [0] * (4 * c["DT_RAY_COLS"])

    def count(self, what):
        self.stats[what] = self.stats.get(what, 0) + 1

    def reset_values(self):
        self.arena = 0
        self.state = ST_WAIT
        self.timer = 0
        self.parts = 0
        self.prep_step = 0
        self.flash = 0
        self.bar_want = self.bar_shown = 0
        self.bar_dirty = 0
        self.part = [0xFF, 0xFF, 0xFF]       # cannon A, B, the core
        # the rest as the program leaves them until WAIT ends
        self.body_x = self.body_xf = self.body_var = 0
        self.shown_x = self.shown_var = self.shown_set = 0
        self.shown_col = 0
        self.prep_x = self.prep_var = 0
        self.patrol = self.patrol_left = 0
        self.mouth_timer = self.drone_turn = 0
        self.chain_k = 0
        self.part_x = 0
        # The rock from the characters (the crawler's arena); the SHIELD
        # CORE's: the turn (256ths of a step), the open segment, its
        # radius, its cycle's frames, the others' radius, the shots of the
        # burst, the segments' Varkon
        self.arena_chars = 0
        self.cb_angle = 0
        self.cb_open_k = self.cb_open_r = self.cb_open_t = 0
        self.cb_rad = self.cb_shots = 0
        self.cb_seg = [0, 0, 0, 0]
        self.cb_paint = 0
        self.cb_last = [0, 0, 0, 0]          # core_place's (cleared,
        self.cb_save = [0] * 72              # with seg_off's scratch)
        # The GRAVEYARD WARDEN's (over the SHIELD CORE's): its ports
        # destroyed, the guns' lives, the patches wanted and made, the rows
        # it shows, its colour, the port, the body being made (its line AND
        # 7, 8 - that, its first row, its codes over the nebula); rows
        # 10-14 rock (air_rock)
        self.wd_gone = 0
        self.wd_life = [0] * 4
        self.wd_want = [0] * 5
        self.wd_have = [0] * 5
        self.wd_r0 = self.wd_r1 = self.wd_colour = self.wd_port = 0
        self.wd_s = self.wd_off = self.wd_row0 = 0
        self.wd_kb0 = self.wd_kb1 = 0
        self.air_rock = 0
        # The VARKON CORVETTE's (over the WARDEN's): its turrets
        # destroyed, their Varkon, the columns shown, its colours, the
        # phases' columns made, the body being made (its phase, its
        # first column, its masks' place)
        self.cv_gone = 0
        self.cv_part = [0] * 4
        self.cv_live = self.cv_pair = 0     # the turrets on; the pair
        self.cv_c0 = self.cv_c1 = self.cv_mode = 0
        self.cv_made = self.cv_mp = self.cv_mc = 0
        self.cv_pp = self.cv_pc0 = self.cv_pm = 0
        # The DEFENSE TURRET ARRAY's (over the CORVETTE's): its turrets
        # destroyed, their Varkon, their lives, those on; the row's place
        # in turn, the row, its cycle; the patches wanted, drawn; ENTER's
        # rows wanted, drawn; WAIT's codes and pictures made; the ray's
        # step, its frames, wanted, drawn, its picture; its colours
        self.dt_gone = 0
        self.dt_part = [0] * 6
        self.dt_life = [0] * 6
        self.dt_live = self.dt_turn = self.dt_row = self.dt_cycle = 0
        self.dt_want = [0] * 4
        self.dt_have = [0] * 4
        self.dt_wrows = self.dt_drawn = self.dt_made = 0
        self.dt_ray = self.dt_rt = self.dt_rwant = self.dt_rhave = 0
        self.dt_shim = self.dt_mode = 0
        # The SUPER-COMPUTER VARKON's (supercomp_model.py)
        self.s_reset_values()

    # --- the level's start (boss_reset) ------------------------------

    def reset(self, state):
        """No arena, no boss (its variables 0, its parts none); the
        characters the boss uses are the level's again; VARKONIA in
        the HUD."""
        self.reset_values()
        pristine = self.files["charset"]
        for code in self.used_codes():
            state.charset[code * 8:code * 8 + 8] = \
                pristine[code * 8:code * 8 + 8]
        hud = self.files["hud"]
        at = self.c["HUD_BAR"]
        for k in range(self.c["BAR_CELLS"]):
            state.screens[0][HUD_CELL + at + k] = hud[at + k]
            state.colour[HUD_CELL + at + k] = hud[120 + at + k] & 15

    def used_codes(self):
        codes = set()
        for first in self.t["set_code"]:
            codes.update(range(first, first + 4))
        codes.update(self.t["letter_code"])
        return sorted(codes)

    # --- the body (boss_draw) ----------------------------------------

    def columns(self, x, var, first, last):
        """The body's columns first..last-1 for x and variant var: their
        32 bytes each (the phase x AND 3; the mouth's for columns 0-4
        if it is open, the hatch's for 8-10)."""
        t, p = self.t, x & 3
        out = []
        for c in range(first, last):
            if c < 5 and var & 1:
                at = (p * 5 + c) * 32
                out.append(t["mouth_data"][at:at + 32])
            elif 8 <= c < 11 and var & 2:
                at = (p * 3 + c - 8) * 32
                out.append(t["hatch_data"][at:at + 32])
            else:
                at = (p * COLUMNS + c) * 32
                out.append(t["body_data"][at:at + 32])
        return out

    def copy(self, state, first, last):
        """Columns first..last-1 for prep_x, prep_var into the set the
        screen does not show."""
        other = self.shown_set ^ 1
        for c, data in zip(range(first, last),
                           self.columns(self.prep_x, self.prep_var,
                                        first, last)):
            code = self.t["set_code"][other * COLUMNS + c]
            state.charset[code * 8:code * 8 + 32] = bytes(data)

    def draw(self, state):
        """A turn in the arena: columns 0-7 of the other set if the body
        must change, or columns 8-14 and the flip (the crawler's body
        only)."""
        if self.c["LEVEL_BOSS"] == 6:
            return self.s_draw(state)
        if self.c["LEVEL_BOSS"] == 5:
            return self.d_draw(state)
        if self.c["LEVEL_BOSS"] == 4:
            return self.c_draw(state)
        if self.c["LEVEL_BOSS"] == 3:
            return self.w_draw(state)
        if self.c["LEVEL_BOSS"] == 2:
            return self.sphere_draw(state)
        if self.state == ST_WAIT:
            return "none"
        if self.prep_step:
            self.copy(state, 8, COLUMNS)
            self.prep_step = 0
            self.flip(state)
            return "body 8-14, flip"
        if self.body_x == self.shown_x and self.body_var == self.shown_var:
            return "none"
        self.prep_x, self.prep_var = self.body_x, self.body_var
        self.copy(state, 0, 8)
        self.prep_step = 1
        return "body 0-7"

    def flip(self, state):
        self.shown_set ^= 1
        self.shown_x, self.shown_var = self.prep_x, self.prep_var
        new = self.prep_x >> 2
        screen = state.screens[0]
        for col in range(self.shown_col, self.shown_col + COLUMNS):
            if col >= 40:
                break
            if not new <= col < new + COLUMNS:
                for r in range(4):
                    screen[(ROW + r) * 40 + col] = 0
        self.shown_col = new
        for c in range(COLUMNS):
            col = new + c
            if col >= 40:
                break
            code = self.t["set_code"][self.shown_set * COLUMNS + c]
            for r in range(4):
                screen[(ROW + r) * 40 + col] = code + r
        self.count("the body flips")

    # --- a turn's update (boss_update) -------------------------------

    def body_next(self):
        x = self.prep_x if self.prep_step else self.shown_x
        self.part_x = 2 * x

    def update(self, v, state):
        """v: varkon_model.Varkon (the parts are its Varkon)."""
        if not self.arena:
            return
        self.v, self.state_ = v, state
        core = self.c["LEVEL_BOSS"] == 2
        if core:                           # the sphere's, for
            self.part_x = self.c["CB_PART_X"]   # the chain
        else:
            self.body_next()
        if self.flash:
            self.flash -= 1
            if not self.flash:
                self.paint(state, 0)
        if self.bar_shown != self.bar_want:
            self.bar_shown += 1 if self.bar_shown < self.bar_want else -1
            self.bar_dirty = 1
        if self.c["LEVEL_BOSS"] == 6:
            self.s_step()
            return
        if self.c["LEVEL_BOSS"] == 5:
            self.d_step()
            return
        if self.c["LEVEL_BOSS"] == 4:
            self.c_step()
            return
        if self.c["LEVEL_BOSS"] == 3:
            self.w_step()
            return
        if core:
            self.core_place()
            getattr(self, CORE_STEPS[self.state])()
            return
        self.place_parts()
        getattr(self, "step_" + NAMES[self.state].lower())()

    def place_one(self, i, dx, y):
        v = self.v
        xr = (self.part_x + dx) & 0xFFFF
        v.x[i] = xr << 8                     # xf 0
        v.y[i] = y << 8 | (v.y[i] & 255)

    def place_parts(self):
        c = self.c
        if self.parts & 1:
            self.place_one(self.part[0], c["CANNON_A_DX"], c["CANNON_Y"])
        if self.parts & 2:
            self.place_one(self.part[1], c["CANNON_B_DX"], c["CANNON_Y"])
        if self.parts & 4:
            self.place_one(self.part[2], c["CORE_DX"], c["CORE_Y"])

    def check_parts(self):
        names = ("cannon A destroyed", "cannon B destroyed",
                 "the core destroyed")
        if self.c["LEVEL_BOSS"] == 2:
            names = ("the top pod destroyed", "the low pod destroyed",
                     "the SHIELD CORE's core destroyed")
        for k in range(3):
            if self.parts >> k & 1 and \
                    self.v.on[self.part[k]] != FLYING:
                self.parts &= ~(1 << k)
                self.count(names[k])

    def free_varkon(self):
        for i in range(len(self.v.on)):
            if self.v.on[i] == FREE:
                return i
        return None

    def set_pri(self, i, value):
        self.state_.mux.set_pri(4 + i, value)

    def new_part(self, i, kind):
        v, t = self.v, self.t
        self.set_pri(i, BOSS_PRI if t["kind_beh"][kind] >= BOSS else 2)
        v.on[i] = FLYING
        v.kind[i] = kind
        v.own[i] = None                     # its kind's colour
        v.delay[i] = v.flash[i] = v.cap[i] = v.left[i] = 0
        v.vx[i] = 0
        v.vy[i] = 0
        v.y[i] &= 0xFF00                    # yf 0
        v.life[i] = t["kind_life"][kind]
        v.period[i] = t["kind_period"][kind]    # its own

    def paint(self, state, which):
        """Rows 15-18 all along: 0 the hull's colours, 1 white, 2 the
        wreck's. The SHIELD CORE: its sphere's cells."""
        if self.c["LEVEL_BOSS"] == 6:     # the SUPER-COMPUTER's
            self.s_paint(state, which)
            return
        if self.c["LEVEL_BOSS"] == 5:     # the ARRAY's
            self.d_paint(state, which)
            return
        if self.c["LEVEL_BOSS"] == 4:     # the CORVETTE's
            self.c_paint(state, which)
            return
        if self.c["LEVEL_BOSS"] == 3:     # the WARDEN's
            self.w_paint(state, which)
            return
        if self.c["LEVEL_BOSS"] == 2:     # done by sphere_draw
            self.cb_paint = which + 2
            return
        colours = self.t["hull_colour"][which * 4:which * 4 + 4]
        for r in range(4):
            for col in range(40):
                state.colour[(ROW + r) * 40 + col] = colours[r] & 15

    # --- the steps -------------------------------------------------

    def step_wait(self):
        v, c = self.v, self.c
        if any(on in (FLYING, BOOM) for on in v.on):
            self.timer = 0
            return
        self.timer = (self.timer + 1) & 255
        if self.timer < c["ARENA_WAIT"]:
            return
        if c["LEVEL_BOSS"] == 0:           # none: STAGE CLEAR
            self.state = ST_CLEAR          # at once
            self.timer = self.chain_k = 0
            self.count("no boss: STAGE CLEAR at once")
            self.text_on()
            return
        if c["LEVEL_BOSS"] == 2:           # the SHIELD CORE
            self.core_begin()
            return
        a = self.free_varkon()
        if a is None:
            return
        v.on[a] = FLYING
        b = self.free_varkon()
        if b is None:
            v.on[a] = FREE
            return
        self.part[0], self.part[1] = a, b
        kind = self.kind("CANNON")
        for i, first in ((a, c["FAN_PERIOD"] // 2), (b, c["FAN_PERIOD"])):
            v.fire[i] = first
            self.new_part(i, kind)
            v.aim[i] = 0
        self.parts = 3
        self.body_x, self.body_xf, self.body_var = c["X_START"], 0, 0
        self.patrol = self.patrol_left = self.drone_turn = 0
        self.shown_x, self.shown_var, self.shown_set = c["X_START"], 0, 0
        self.shown_col = 40
        self.mouth_timer = c["DRONE_EVERY_A"]
        self.bar_on()
        state = self.state_
        self.paint(state, 0)
        self.state = ST_ENTER
        self.count("the boss comes")
        self.body_next()
        self.place_parts()

    def bar_on(self):
        """The bar fills, in red where VARKONIA was; the bosses' theme
        from its start (song_start)."""
        c, state = self.c, self.state_
        if parts.has("songs"):            # (D.2: step 17)
            state.player.song_start(player_model.SONG["BOSS"])
        self.bar_want = c["BAR_STEPS"]
        self.bar_dirty = 1
        for k in range(c["BAR_CELLS"]):
            state.colour[HUD_CELL + c["HUD_BAR"] + k] = c["BAR_COLOUR"]

    def kind(self, name):
        return self.c[f"KIND_{name}"]

    def step_enter(self):
        c = self.c
        pos = (self.body_x << 8 | self.body_xf) - c["ENTER_SPEED"]
        self.body_x, self.body_xf = (pos >> 8) & 255, pos & 255
        if self.body_x < c["X_STATION"]:
            self.body_x, self.body_xf = c["X_STATION"], 0
            self.state = ST_FIGHT
            self.count("the boss at its station")
        self.aim_cannons()

    def step_fight(self):
        self.check_parts()
        if not self.parts & 3:
            self.state = ST_OPEN
            self.timer = 0
            self.body_var = 2
            self.count("the hatch opens")
            return
        self.patrol_step()
        self.mouth(0)
        self.aim_cannons()
        self.fire_cannons()
        self.bar_life()

    def step_open(self):
        c, v = self.c, self.v
        if self.timer == 0:
            i = self.free_varkon()
            if i is None:
                self.count("the core waits for a free Varkon")
                return
            self.part[2] = i
            self.new_part(i, self.kind("CORE"))
            v.fire[i] = c["CORE_PERIOD"]
            self.parts |= 4
            self.place_parts()
        self.timer = (self.timer + 1) & 255
        if self.timer >= c["CORE_RISE_FRAMES"]:
            self.state = ST_CORE
            self.patrol, self.patrol_left = 2, 0
            self.mouth_timer = c["DRONE_EVERY_B"]
            self.count("the core risen")
        self.bar_life()

    def step_core(self):
        self.check_parts()
        if not self.parts & 4:
            self.dies()
            return
        self.patrol_step()
        self.mouth(1)
        self.bar_life()

    def dies(self):
        v = self.v
        for i in range(len(v.on)):
            if v.on[i] == FLYING:
                v.on[i] = BOOM
                v.left[i] = 0
                v.flash[i] = 0
                self.count("the boss's death: a Varkon explodes")
        for j in range(len(v.s_on)):
            if v.s_on[j]:
                self.count("the boss's death: a plasma shot gone")
            v.s_on[j] = 0
        self.chain_k = self.bar_want = self.timer = 0
        self.parts = 0                       # none
        self.body_var &= 2
        self.state = ST_CHAIN
        self.count("the boss destroyed")

    def step_chain(self):
        c, t, v = self.c, self.t, self.v
        self.timer = (self.timer + 1) & 255
        if self.timer < c["CHAIN_EVERY"]:
            return
        self.timer = 0
        i = self.free_varkon()
        if i is not None:
            self.set_pri(i, 2)
            v.on[i] = BOOM
            v.kind[i] = self.kind("CORE")
            v.left[i] = v.flash[i] = v.cap[i] = 0
            k = self.chain_k               # the SHIELD CORE's
            if c["LEVEL_BOSS"] == 2:       # after the crawler's
                k += c["CHAIN_COUNT"]
            v.y[i] = t["chain_y"][k] << 8 | (v.y[i] & 255)
            v.x[i] = ((t["chain_dx"][k] + self.part_x) & 0xFFFF) << 8
            self.count("a fireball of the chain")
        else:
            self.count("the chain: no free Varkon")
        v.sound("explode")
        self.flash = 3
        self.paint(self.state_, 1)
        self.chain_k += 1
        if self.chain_k >= c["CHAIN_COUNT"]:
            self.state = ST_WRECK

    def step_wreck(self):
        c = self.c
        self.timer = (self.timer + 1) & 255
        if self.timer == c["WRECK_PAINT"]:
            self.paint(self.state_, 2)
            self.count("the wreck")
        if self.timer >= c["WRECK_WAIT"]:
            self.state = ST_CLEAR
            self.timer = self.chain_k = 0
            self.text_on()

    def text_on(self):
        """STAGE CLEAR (clear_now): its jingle first."""
        state, t, c = self.state_, self.t, self.c
        if parts.has("songs"):            # (D.2: step 17)
            state.player.song_start(player_model.SONG["CLEAR"])
        hud = self.files["hudset"]
        for glyph, code in zip(t["letter_glyph"], t["letter_code"]):
            state.charset[code * 8:code * 8 + 8] = \
                hud[glyph * 8:glyph * 8 + 8]
        for lo, hi, code in zip(t["text_lo"], t["text_hi"],
                                t["text_code"]):
            cell = hi << 8 | lo
            state.screens[0][cell] = code
            state.colour[cell] = c["TEXT_COLOUR"]
        self.count("STAGE CLEAR")

    def step_clear(self):
        t, c, v = self.t, self.c, self.v
        state, ship = self.state_, self.state_.ship
        colour = t["text_cycle"][(v.anim >> 2) & 3]
        for lo, line in zip(t["text_lo"], t["text_line"]):
            if line == 0:
                state.colour[lo] = colour
        if ship.mode in (CONTROL, ENTER):
            ship.mode = LEAVE
            ship.blink = 0
            ship.count("the ship flies off")
        self.timer = (self.timer + 1) & 255
        if self.timer >= c["NOTCH_EVERY"]:
            self.timer = 0
            if ship.shield:
                ship.shield -= 1
                v.score.add(self.notch_points(), ship)
                v.sound("capsule")
                self.count("a notch into the score")
        if ship.shield == 0 and ship.mode == GONE:
            self.chain_k = (self.chain_k + 1) & 255
            if self.chain_k >= c["CLEAR_WAIT"]:
                self.state = ST_DONE
                self.restart = True
                self.count("the level again after STAGE CLEAR")

    def notch_points(self):
        t, k = self.t, self.c["KIND_NOTCH"]
        return int(f"{t['kind_pts_hi'][k]:02x}{t['kind_pts_lo'][k]:02x}")

    def step_done(self):
        pass

    # --- its ways ----------------------------------------------------

    def patrol_step(self):
        t = self.t
        if self.patrol_left:
            self.patrol_left -= 1
            return
        k = self.patrol
        to, speed = t["patrol_to"][k], t["patrol_speed"][k]
        pos = self.body_x << 8 | self.body_xf
        there = False
        if pos == to << 8:
            there = True
        elif self.body_x < to:
            pos += speed
            self.body_x, self.body_xf = pos >> 8, pos & 255
            there = self.body_x >= to
        else:
            pos -= speed
            self.body_x, self.body_xf = pos >> 8, pos & 255
            there = self.body_x < to
        if there:
            self.body_x, self.body_xf = to, 0
            self.patrol_left = t["patrol_wait"][k]
            self.patrol = k ^ 1

    def mouth(self, phase):
        c, v = self.c, self.v
        every = (c["DRONE_EVERY_A"], c["DRONE_EVERY_B"])[phase]
        most = (c["DRONES_MAX_A"], c["DRONES_MAX_B"])[phase]
        self.mouth_timer = (self.mouth_timer - 1) & 255
        if self.mouth_timer == 0:
            self.mouth_timer = every
            drone = self.kind("DRONE")
            flying = sum(1 for i in range(len(v.on))
                         if v.on[i] == FLYING and v.kind[i] == drone)
            if flying < most:
                self.launch()
            else:
                self.count("the mouth: drones enough")
        self.body_var &= ~1
        if self.mouth_timer <= c["MOUTH_OPEN"] or \
                every - self.mouth_timer < c["MOUTH_OPEN"]:
            self.body_var |= 1

    def launch(self):
        c, v, t = self.c, self.v, self.t
        i = self.free_varkon()
        if i is None:
            self.count("the mouth: no free Varkon")
            return
        kind = self.kind("DRONE")
        self.new_part(i, kind)
        xr = (c["MOUTH_DX"] + self.part_x) & 0xFFFF
        v.x[i] = xr << 8
        v.y[i] = c["MOUTH_Y"] << 8
        v.fire[i] = t["kind_period"][kind] >> 1
        v.seg[i] = (c["PATH_LAUNCH_UP"], c["PATH_LAUNCH_LOW"])[
            self.drone_turn]
        self.count(("a drone launched up", "a drone launched low")[
            self.drone_turn])
        self.drone_turn ^= 1
        v.load(i)
        v.sound("missile")

    def aim_cannons(self):
        for k in (0, 1):
            if self.parts >> k & 1:
                self.aim_one(self.part[k])

    def aim_dx(self, i):
        """q = (Varkon i's x register - the ship's) / 4; None if the
        ship is to its right or q is 0."""
        v, ship = self.v, self.state_.ship
        sx = (ship.x + 24) & 0xFFFF
        dx = ((v.x[i] >> 8) - sx) & 0xFFFF
        if dx & 0x8000 or dx >> 2 == 0:
            return None
        return (dx >> 2) & 255

    @staticmethod
    def aim_dy(q, dy):
        """dy 1-255: 2 if dy >= 3 q, 1 if dy >= q, else 0."""
        if 3 * q <= dy:
            return 2
        return 1 if dy >= q else 0

    def aim_one(self, i, what=None):
        v, ship = self.v, self.state_.ship
        q = self.aim_dx(i)
        if q is None:
            aim = 2
        else:
            dy = (v.y[i] >> 8) + 2 - (ship.y & 255)
            aim = 0 if dy <= 0 else self.aim_dy(q, dy)
        if aim != v.aim[i]:
            what = what or ("a cannon" if v.kind[i] ==
                            self.kind("CANNON") else "the low pod")
            self.count(f"{what} aims {('left', 'up', 'high')[aim]}")
        v.aim[i] = aim

    def aim_top(self, i, what="the top pod"):
        """The top pod as aim_one, the ship below it: dy = the
        ship's line - its line - 2 (8 bits: only the second
        subtraction's carry counts)."""
        v, ship = self.v, self.state_.ship
        q = self.aim_dx(i)
        if q is None:
            aim = 2
        else:
            first = ((ship.y & 255) - (v.y[i] >> 8)) & 255
            dy = first - 2
            aim = 0 if dy <= 0 else self.aim_dy(q, dy)
        if aim != v.aim[i]:
            self.count(f"{what} aims {('left', 'down', 'low')[aim]}")
        v.aim[i] = aim

    def fire_cannons(self):
        c, v = self.c, self.v
        for k in (0, 1):
            if not self.parts >> k & 1:
                continue
            i = self.part[k]
            v.fire[i] = (v.fire[i] - 1) & 255
            if v.fire[i]:
                continue
            v.fire[i] = c["FAN_PERIOD"]
            first = c["FAN_FIRST"] + 3 * v.aim[i]
            for e in range(first, first + 3):
                v.shoot_entry(i, e)
            self.count(f"a cannon fires its fan, aim {v.aim[i]}")

    def bar_life(self):
        c, v = self.c, self.v
        total = 0
        for k in (0, 1):
            if self.parts >> k & 1:
                total += v.life[self.part[k]]
        if self.parts & 4:
            total += v.life[self.part[2]]
        elif self.part[2] == 0xFF:
            total += c["CORE_LIFE"]
        self.bar_want = self.t["bar_of_life"][total & 255]

    # --- the SHIELD CORE (core.asm) ---------------------------------

    def core_begin(self):
        """WAIT is over: seven free Varkon (else later), the four
        segments, the core, the two pods (the core and the pods where
        they stay); the arena's 36 cells under the sphere kept (codes,
        colours); the bar; ENTER."""
        v, c, state = self.v, self.c, self.state_
        if sum(1 for on in v.on if on == FREE) < 7:
            self.count("the SHIELD CORE waits for seven free Varkon")
            return
        for k in range(4):
            i = self.free_varkon()
            self.cb_seg[k] = i
            self.new_part(i, self.kind("SEGMENT"))
        i = self.free_varkon()
        self.part[2] = i
        self.new_part(i, self.kind("SHCORE"))
        v.fire[i] = c["CB_CORE_FIRST"]
        for k, first in ((0, c["CB_FAN_PERIOD"] // 2),
                         (1, c["CB_FAN_PERIOD"])):
            i = self.free_varkon()
            self.part[k] = i
            v.fire[i] = first
            self.new_part(i, self.kind("POD"))
            v.aim[i] = 0
        self.parts = 7
        self.place_fixed(self.part[2], c["CB_CORE_XR"], c["CB_CORE_Y"])
        self.place_fixed(self.part[0], c["CB_POD_XR"], c["CB_POD_TOP_Y"])
        self.place_fixed(self.part[1], c["CB_POD_XR"], c["CB_POD_LOW_Y"])
        where = self.sphere_cells()
        self.cb_save = [state.screens[0][at] for at in where] + \
            [state.colour[at] & 15 for at in where]
        self.cb_last[0] = 0xFF               # (core_place: all to do)
        self.bar_on()
        self.timer = self.cb_angle = self.cb_open_t = self.cb_shots = 0
        self.cb_open_k = 3
        self.cb_rad = self.cb_open_r = c["R_ENTER"]
        self.state = ST_ENTER
        self.count("the SHIELD CORE comes")
        self.core_place()

    def sphere_cells(self):
        """The sphere's 36 cells on the screen, row after row."""
        c = self.c
        return [(c["SPHERE_ROW"] + r) * 40 + c["SPHERE_COL"] + col
                for r in range(c["SPHERE_ROWS"])
                for col in range(c["SPHERE_COLS"])]

    def core_enter(self):
        """Frames 1 to CB_PREP - 1: in the sphere's codes the characters
        its cells show, a row a frame; frame CB_PREP: its codes out of
        the rock's table, its cells on in the next turn (cb_paint 1);
        then it grows (sphere_draw). The segments close in from
        R_ENTER, a pixel every two frames, to R_IN, turning;
        ENTER_FRAMES, then FIGHT."""
        c, state = self.c, self.state_
        self.timer = (self.timer + 1) & 255
        first, cells = c["SPHERE_FIRST"], c["SPHERE_CELLS"]
        cols = c["SPHERE_COLS"]
        if self.timer < c["CB_PREP"]:
            row = self.timer - 1
            for k in range(row * cols, row * cols + cols):
                code, to = self.cb_save[k], (first + k) * 8
                state.charset[to:to + 8] = \
                    state.charset[code * 8:code * 8 + 8]
            self.count("the arena's characters into the sphere's codes")
        elif self.timer == c["CB_PREP"]:
            for line in range(8):
                for code in range(first, first + cells):
                    state.rock_lines[line * 256 + code] = 0
            self.cb_paint = 1
        self.cb_rad = self.cb_open_r = max(c["R_IN"], c["R_ENTER"] -
                                           (self.timer >> 1))
        self.spin(c["CB_SPIN_A"])
        if self.timer >= c["CB_ENTER_FRAMES"]:
            self.state = ST_FIGHT
            self.count("the SHIELD CORE fights")

    def core_fight(self):
        """FIGHT and RAGE: the core destroyed, the end; in FIGHT, the
        core down to RAGE_LIFE: RAGE (its own period BURST_GAP, bursts
        of BURST, then BURST_PAUSE). The turn, the gap, the pods, the
        bar."""
        c, v = self.c, self.v
        self.check_parts()
        if not self.parts & 4:
            self.dies()
            return
        i = self.part[2]
        if self.state != ST_RAGE:
            if v.life[i] <= c["CB_RAGE_LIFE"]:
                self.state = ST_RAGE
                v.period[i] = c["CB_BURST_GAP"]
                self.count("RAGE: half the core's life")
        else:
            if self.cb_shots == c["CB_BURST"]:
                v.fire[i] = c["CB_BURST_PAUSE"]
                self.cb_shots = 0
                self.count("RAGE: a burst's pause")
            if v.fire[i] == 1:
                self.cb_shots = (self.cb_shots + 1) & 255
        y = self.state - ST_FIGHT
        self.spin(c[("CB_SPIN_A", "CB_SPIN_B")[y]])
        self.cb_open_t = (self.cb_open_t + 1) & 255
        if self.cb_open_t >= c[("CB_OPEN_EVERY_A",
                                "CB_OPEN_EVERY_B")[y]]:
            self.cb_open_t = 0
            self.cb_open_k = (self.cb_open_k + 1) & 3
            self.count("a new gap")
        steps, hold = c["CB_OPEN_STEPS"], c[("CB_OPEN_HOLD_A",
                                              "CB_OPEN_HOLD_B")[y]]
        t = self.cb_open_t
        if t < steps:
            r = c["R_IN"] + 2 * t
        elif t - steps < hold:
            r = c["R_OUT"]
        elif t - steps - hold < steps:
            r = c["R_OUT"] - 2 * (t - steps - hold)
        else:
            r = c["R_IN"]
        if r == c["R_OUT"] and self.cb_open_r != r:
            self.count("a segment fully open")
        self.cb_open_r = r
        for k, aim, base, which in (
                (0, self.aim_top, c["POD_FAN_FIRST"] + 9, "top"),
                (1, self.aim_one, c["POD_FAN_FIRST"], "low")):
            if self.parts >> k & 1:        # its fan in this frame:
                pod = self.part[k]         # its aim, the fan
                v.fire[pod] = (v.fire[pod] - 1) & 255
                if not v.fire[pod]:
                    aim(pod)
                    self.fan_pod(pod, base, which)
        self.bar_want = v.life[i]

    def spin(self, step):
        self.cb_angle = (self.cb_angle + step) & 0xFFFF

    def fan_pod(self, i, base, which):
        """Pod i's fan (its count of frames has come to 0):
        CB_FAN_PERIOD frames to the next; entries base + 3 aim + 0-2.
        (which, a pod's place or a gun's whole name)"""
        v = self.v
        v.fire[i] = self.c["CB_FAN_PERIOD"]
        first = base + 3 * v.aim[i]
        for e in range(first, first + 3):
            v.shoot_entry(i, e)
        who = which if " " in which else f"the {which} pod"
        self.count(f"{who} fires its fan, aim {v.aim[i]}")

    def offset(self, a, r):
        """The cosine of angle a times r over 64, with its sign
        (seg_off)."""
        cos = self.files["cosine"][a & (self.c["ANGLES"] - 1)]
        p = (abs(cos) * r) >> 6
        return -p if cos < 0 else p

    def core_place(self):
        """The segments' places (ENTER, FIGHT, RAGE): segment k at the
        angle's step + 16 k, at cb_rad (the open one cb_open_r). (The
        core and the pods stay where core_begin put them.) A destroyed
        segment is not placed again (seg_put)."""
        if self.state == ST_WAIT or self.state >= ST_CHAIN:
            return
        now = [self.cb_angle >> 8, self.cb_open_k, self.cb_open_r,
               self.cb_rad]
        if now == self.cb_last:            # as when it placed them
            return
        self.cb_last = now
        c, v = self.c, self.v
        quarter = c["ANGLES"] // 4
        for k in range(4):                 # (the program: two products
            r = self.cb_open_r if k == self.cb_open_k else self.cb_rad
            a = (16 * k + (self.cb_angle >> 8)) & (c["ANGLES"] - 1)
            i = self.cb_seg[k]             # a radius, quarter turns:
            if v.on[i] != FLYING:          # destroyed: it
                self.count("a destroyed segment left in place")
                continue                   # stays where it was
            v.x[i] = ((c["CB_SEG_XR"] + self.offset(a, r)) & 0xFFFF) << 8
            y = (c["CB_SEG_Y"] + self.offset(a - quarter, r)) & 255
            v.y[i] = y << 8 | (v.y[i] & 255)   # here each by itself)

    def place_fixed(self, i, xr, y):
        v = self.v
        v.x[i] = xr << 8
        v.y[i] = y << 8 | (v.y[i] & 255)

    def sphere_draw(self, state):
        """Early in a turn (boss_draw): what update() asked for
        (cb_paint: 1 the cells on and its colours, 2 its colours, 3
        white, 4 the arena's cells again); in ENTER, frames 1 to
        CB_GROW_FRAMES, lines 23 - k and 24 + k of its characters (k
        the frame - 1)."""
        c = self.c
        asked, self.cb_paint = self.cb_paint, 0
        where = self.sphere_cells()
        cols = c["SPHERE_COLS"]
        if asked == 1:
            for k, at in enumerate(where):
                state.screens[0][at] = c["SPHERE_FIRST"] + k
            self.count("the sphere's cells on")
        if asked in (1, 2):
            own = self.files["sphere_own"]
            for k, at in enumerate(where):
                state.colour[at] = 8 | own[k // cols]
            if asked == 2:
                self.count("the sphere's colours again")
        elif asked == 3:
            for at in where:
                state.colour[at] = 8 | c["CB_FLASH_OWN"]
            self.count("the sphere white")
        elif asked == 4:
            cells = c["SPHERE_CELLS"]
            for k, at in enumerate(where):
                state.screens[0][at] = self.cb_save[k]
                state.colour[at] = self.cb_save[cells + k]
            self.count("the sphere gone: the arena's cells again")
        out = "none" if not asked else f"sphere {asked}"
        k = self.timer - c["CB_PREP"] - 1
        if self.state == ST_ENTER and 0 <= k < c["CB_GROW_FRAMES"]:
            half = 4 * c["SPHERE_ROWS"]
            self.sphere_line(state, half + k)
            self.sphere_line(state, half - 1 - k)
            self.count("the sphere grows")
            out += ", grows"
        return out

    def sphere_line(self, state, line):
        """Line `line` (0-47) of the sphere's characters into its
        codes: the line of its row's six."""
        c = self.c
        cols = c["SPHERE_COLS"]
        row, y = line >> 3, line & 7
        for col in range(cols):
            at = 8 * (row * cols + col) + y
            state.charset[8 * c["SPHERE_FIRST"] + at] = \
                self.files["sphere"][at]

    # --- the GRAVEYARD WARDEN (warden.asm) ---------------------------

    @staticmethod
    def signed(b):
        return b - 256 if b & 0x80 else b

    def w_draw(self, state):
        """A turn in the arena (boss_draw): nothing to do (the body
        where it is shown, as it is shown), or the patches and column 0
        of the other set; column 1; ... column 6; the flip."""
        if self.state == ST_WAIT:
            return "none"
        p = self.prep_step
        if p == 0:
            if self.body_x == self.shown_x and \
                    self.wd_want == self.wd_have:
                return "none"
            self.w_patches()
            self.prep_x = self.body_x
            self.w_prep()
            self.w_column(state, 0)
            self.prep_step = 1
            return "warden column 0"
        if p == self.c["W_FLIP"]:
            self.w_flip(state)
            return "warden flip"
        self.w_column(state, p)
        self.prep_step += 1
        return f"warden column {p}"

    def w_patches(self):
        """The patches wanted and not made yet into its drawing: port
        k's 3 k + its state, the core's 12 + its state."""
        t, geometry = self.t, self.files["warden"]["patches"]
        for x in range(4, -1, -1):
            if self.wd_want[x] == self.wd_have[x]:
                continue
            self.wd_have[x] = self.wd_want[x]
            k = 3 * x + self.wd_want[x]
            c0, cols, l0, lines = geometry[k]
            data = t[f"wd_patch_{k}"]
            stride = self.c["W_STRIDE"]
            for n in range(cols):
                at = (c0 + n) * stride + 8 + l0
                self.wd_comp[at:at + lines] = bytes(
                    data[n * lines:(n + 1) * lines])
            self.count("the WARDEN: a patch into its drawing")

    def w_prep(self):
        """The body being made: its line AND 7, 8 - that, its first
        row (signed), its codes over the nebula's rows."""
        c = self.c
        y = self.prep_x
        self.wd_s = y & 7
        self.wd_off = (8 - self.wd_s) & 255
        self.wd_row0 = (self.signed(y) >> 3) & 255
        self.wd_kb0 = min((c["W_BAND_FROM"] - self.wd_row0) & 255,
                          c["W_CODES"])
        self.wd_kb1 = min((c["W_BAND_TO"] - self.wd_row0) & 255,
                          c["W_CODES"])

    def w_column(self, state, x):
        """Column x of the other set: its ten characters from the
        drawing (from line 8 - s of its column), their lines in the
        rock's table; over the nebula its pixels where the body has
        none."""
        c, t = self.c, self.t
        code = t["wd_code"][(self.shown_set ^ 1) * 8 + x]
        base = x * c["W_STRIDE"] + self.wd_off
        n = 8 * c["W_CODES"]
        column = self.wd_comp[base:base + n]
        state.charset[code * 8:code * 8 + n] = column
        for i in range(n):
            state.rock_lines[(i & 7) * 256 + code + (i >> 3)] = column[i]
        for k in range(self.wd_kb0, self.wd_kb1):
            r = ((k + self.wd_row0) & 255)
            under = self.wd_save_code[((r << 3) & 255) | x]
            for line in range(8):
                at = (code + k) * 8 + line
                b = state.charset[at]
                m = (b | b >> 1) & 0x55
                m |= m << 1
                state.charset[at] = (state.charset[under * 8 + line] &
                                     ~m & 255) | b
            self.count("the WARDEN over the nebula")

    def w_rows(self, state, row):
        """Row `row` of its columns: the screen's offset of its first."""
        return row * 40 + self.c["W_COL"]

    def w_flip(self, state):
        """The other set shown from the next frame: its rows (row0 to
        row0 + W_CODES - 1, from 0, under W_ROWS) take its codes and its
        colour; the rows it showed and does not now, the arena's cells
        again."""
        c, t = self.c, self.t
        self.shown_set ^= 1
        self.shown_x = self.prep_x
        row0 = self.signed(self.wd_row0)
        n0 = max(row0, 0)
        top = (self.wd_row0 + c["W_CODES"]) & 255
        n1 = n0 if top & 0x80 else max(min(top, c["W_ROWS"]), n0)
        cols = c["W_COLS"]
        screen = state.screens[0]
        for k in range(self.wd_r0, self.wd_r1):
            if k < n0 or k >= n1:
                at = self.w_rows(state, k)
                for col in range(cols):
                    screen[at + col] = self.wd_save_code[k * 8 + col]
                    state.colour[at + col] = self.wd_save_col[k * 8 + col]
                self.count("the WARDEN leaves a row: the arena's cells")
        self.wd_r0, self.wd_r1 = n0, n1
        for k in range(n0, n1):
            at = self.w_rows(state, k)
            for col in range(cols):
                screen[at + col] = (t["wd_code"][self.shown_set * 8 + col]
                                    + k - row0) & 255
                state.colour[at + col] = self.wd_colour & 15
        self.prep_step = 0
        self.count("the WARDEN's body flips")

    def w_paint(self, state, which):
        """Its colours: 0 its own, 1 white, 2 the wreck's, in the cells
        it shows."""
        self.wd_colour = self.t["wd_paints"][which]
        for k in range(self.wd_r0, self.wd_r1):
            at = self.w_rows(state, k)
            for col in range(self.c["W_COLS"]):
                state.colour[at + col] = self.wd_colour & 15

    def w_step(self):
        """Its turn (after the bar's step): its parts for the frame after
        the next, its step."""
        c = self.c
        self.part_x = c["W_PART_X"]
        self.w_place()
        (self.w_wait, self.w_enter, self.w_fight, self.w_bare,
         self.w_core, self.w_chain, self.step_wreck, self.step_clear,
         self.step_done)[self.state]()

    def w_place(self):
        """The gun in its port, the core in its pit, on the body the
        screen will show in the frame after the next."""
        c, t = self.c, self.t
        y = self.prep_x if self.prep_step == c["W_FLIP"] else self.shown_x
        if self.parts & 1:
            self.place_one(self.part[0], 0,
                           (t["wd_gun_dy"][self.wd_port] + y) & 255)
        if self.parts & 4:
            self.place_one(self.part[2], c["W_CORE_DX"],
                           (y + c["W_CORE_DY"]) & 255)

    def w_wait(self):
        v, c = self.v, self.c
        if any(on in (FLYING, BOOM) for on in v.on):
            self.timer = 0
            return
        self.timer = (self.timer + 1) & 255
        if self.timer >= c["ARENA_WAIT"]:
            self.w_begin()

    def w_begin(self):
        """WAIT is over: the arena's cells under its columns kept; rows
        10-14 rock, the far layer's codes not; the patches all to make;
        the guns' lives; the body above the screen, none of it shown;
        the bar; ENTER."""
        c, t, state = self.c, self.t, self.state_
        cols = c["W_COLS"]
        for row in range(c["W_ROWS"]):              # (8 places a row)
            at = self.w_rows(state, row)
            for col in range(cols):
                self.wd_save_code[row * 8 + col] = \
                    state.screens[0][at + col]
                self.wd_save_col[row * 8 + col] = \
                    state.colour[at + col] & 15
        self.air_rock = 1
        for code in t["wd_far"]:
            for line in range(8):
                state.rock_lines[line * 256 + code] = 0
        self.wd_want, self.wd_have = [0] * 5, [255] * 5
        self.wd_life = [c["W_GUN_LIFE"]] * 4
        self.body_x = self.shown_x = c["W_Y_START"] & 255
        self.body_xf = self.shown_set = self.prep_step = 0
        self.wd_r0 = self.wd_r1 = self.wd_gone = 0
        self.prep_var = self.shown_var = self.wd_port = 0
        self.patrol = self.patrol_left = self.parts = 0
        self.part[0] = self.part[2] = 0xFF
        self.mouth_timer = c["W_SHUT_WAIT"]
        self.wd_colour = t["wd_paints"][0]
        self.bar_on()
        self.state = ST_ENTER
        self.count("the GRAVEYARD WARDEN comes")

    def w_enter(self):
        c = self.c
        pos = ((self.body_x << 8 | self.body_xf) + c["W_ENTER_SPEED"]) \
            & 0xFFFF
        self.body_x, self.body_xf = pos >> 8, pos & 255
        if self.body_x & 0x80 or self.body_x < c["W_Y_STATION"]:
            return
        self.body_x, self.body_xf = c["W_Y_STATION"], 0
        self.state = ST_FIGHT
        self.count("the WARDEN at its station")

    def w_fight(self):
        """The ports in turn: shut W_SHUT_WAIT frames, then the next one
        opens (its gun a free Varkon, its life as it was); open: the
        gun's fans; destroyed, the port broken off (two shards), the
        next one waits; W_OPEN_FRAMES, the gun back in, the port shut.
        All four destroyed: BARE."""
        c, t, v = self.c, self.t, self.v
        self.w_patrol()
        if not self.shown_var:                       # shut
            self.mouth_timer = (self.mouth_timer - 1) & 255
            if self.mouth_timer:
                self.w_bar()
                return
            i = self.free_varkon()
            if i is None:
                self.mouth_timer = 1
                self.count("a port waits for a free Varkon")
                self.w_bar()
                return
            self.part[0] = i
            self.new_part(i, self.kind("WGUN"))
            port = self.wd_port = t["wd_order"][self.prep_var]
            v.life[i] = self.wd_life[port]
            v.fire[i] = c["W_FAN_FIRST"]
            v.aim[i] = 0
            self.wd_want[port] = 1
            self.shown_var = 1
            self.parts |= 1
            self.mouth_timer = c["W_OPEN_FRAMES"]
            self.count(f"port {port} opens")
            self.w_place()
            self.w_bar()
            return
        i, port = self.part[0], self.wd_port
        if v.on[i] != FLYING:
            v.split(i)
            self.wd_want[port] = 2
            self.wd_life[port] = 0
            self.wd_gone |= 1 << port
            v.sound("explode")
            self.count(f"port {port} destroyed: broken off")
        else:
            self.wd_life[port] = v.life[i]
            v.fire[i] = (v.fire[i] - 1) & 255
            if not v.fire[i]:
                self.w_fan(i)
            self.mouth_timer = (self.mouth_timer - 1) & 255
            if self.mouth_timer:
                self.w_bar()
                return
            v.on[i] = FREE
            self.wd_want[port] = 0
            self.count(f"port {port} shuts, its gun back in")
        self.part[0] = 0xFF
        self.parts &= ~1
        self.shown_var = 0
        self.mouth_timer = c["W_SHUT_WAIT"]
        if self.wd_gone == 15:
            self.state = ST_OPEN
            self.mouth_timer = c["W_CORE_WAIT"]
            self.count("the WARDEN bare: no port left")
            self.w_bar()
            return
        k = self.prep_var
        while True:
            k = (k + 1) & 3
            if not self.wd_gone & 1 << t["wd_order"][k]:
                break
        self.prep_var = k
        self.w_bar()

    def w_fan(self, i):
        """Gun i's fan: up at the ship above it (the low pod's fans),
        else down or left (the top pod's); W_FAN_PERIOD to the next."""
        c, v = self.c, self.v
        self.aim_one(i, "a gun")
        base, which = c["POD_FAN_FIRST"], "a gun, up"
        if not v.aim[i]:
            self.aim_top(i, "a gun")
            base, which = c["POD_FAN_FIRST"] + 9, "a gun, down"
        self.fan_pod(i, base, which)
        v.fire[i] = c["W_FAN_PERIOD"]

    def w_bare(self):
        """No port left: W_CORE_WAIT frames, then the core in a free
        Varkon (its pit open, its first shot, the core's patrol, its
        shards' time): CORE."""
        c, v = self.c, self.v
        self.w_patrol()
        self.mouth_timer = (self.mouth_timer - 1) & 255
        if self.mouth_timer:
            self.w_bar()
            return
        i = self.free_varkon()
        if i is None:
            self.mouth_timer = 1
            self.count("the WARDEN's core waits for a free Varkon")
            self.w_bar()
            return
        self.part[2] = i
        self.new_part(i, self.kind("WCORE"))
        v.fire[i] = c["W_CORE_FIRST"]
        self.wd_want[4] = 1
        self.parts |= 4
        self.patrol, self.patrol_left = 2, 0
        self.drone_turn = c["W_SHED_EVERY"]
        self.state = ST_CORE
        self.count("the WARDEN's core shows")
        self.w_place()
        self.w_bar()

    def w_core(self):
        """The core's fight: destroyed, the end; under RAGE_LIFE its
        shots faster; every W_SHED_EVERY frames two shards from it."""
        c, v = self.c, self.v
        i = self.part[2]
        if v.on[i] != FLYING:
            self.count("the WARDEN's core destroyed")
            self.dies()
            return
        if v.life[i] < c["W_RAGE_LIFE"] + 1:
            if v.period[i] != c["W_RAGE_PERIOD"]:
                self.count("the WARDEN's core: faster")
            v.period[i] = c["W_RAGE_PERIOD"]
        self.drone_turn = (self.drone_turn - 1) & 255
        if not self.drone_turn:
            self.drone_turn = c["W_SHED_EVERY"]
            v.split(i)
            self.count("the WARDEN's core sheds two shards")
        self.w_patrol()
        self.w_bar()

    def w_bar(self):
        c, v = self.c, self.v
        total = sum(self.wd_life) & 255
        if self.part[2] == 0xFF:
            total += c["W_CORE_LIFE"]
        else:
            total += v.life[self.part[2]]
        self.bar_want = self.t["wd_bar_of"][total & 255]

    def w_patrol(self):
        """As patrol_step, up and down: its entry 0-1 the ports' fight,
        2-3 the core's."""
        t = self.t
        if self.patrol_left:
            self.patrol_left -= 1
            return
        k = self.patrol
        to, speed = t["wd_patrol_to"][k], t["wd_patrol_speed"][k]
        pos = self.body_x << 8 | self.body_xf
        if pos == to << 8:
            there = True
        elif self.body_x < to:
            pos += speed
            self.body_x, self.body_xf = pos >> 8, pos & 255
            there = self.body_x >= to
        else:
            pos -= speed
            self.body_x, self.body_xf = pos >> 8, pos & 255
            there = self.body_x < to
        if there:
            self.body_x, self.body_xf = to, 0
            self.patrol_left = t["wd_patrol_wait"][k]
            self.patrol = k ^ 1

    def w_chain(self):
        """As step_chain, on its body: the fireball at wd_chain_dx from
        part_x, wd_chain_y from the body's top line shown."""
        c, t, v = self.c, self.t, self.v
        self.timer = (self.timer + 1) & 255
        if self.timer < c["CHAIN_EVERY"]:
            return
        self.timer = 0
        i = self.free_varkon()
        if i is not None:
            self.set_pri(i, 2)
            v.on[i] = BOOM
            v.kind[i] = self.kind("WCORE")
            v.left[i] = v.flash[i] = v.cap[i] = 0
            k = self.chain_k
            y = (t["wd_chain_y"][k] + self.shown_x) & 255
            v.y[i] = y << 8 | (v.y[i] & 255)
            v.x[i] = ((t["wd_chain_dx"][k] + self.part_x) & 0xFFFF) << 8
            self.count("a fireball of the chain")
        else:
            self.count("the chain: no free Varkon")
        v.sound("explode")
        self.flash = 3
        self.paint(self.state_, 1)
        self.chain_k += 1
        if self.chain_k >= c["CHAIN_COUNT"]:
            self.state = ST_WRECK

    # --- the VARKON CORVETTE (corvette.asm) --------------------------

    def c_phase(self, p):
        """Phase p's drawing (0 the file's, cv_comp; 1-3 made in WAIT)."""
        return self.t["cv_comp"] if p == 0 else self.cv_phases[p - 1]

    def c_draw(self, state):
        """A turn in the arena (boss_draw): nothing to do (the body
        where it is shown), or column 0 of the other set; 1; ... 12
        (prep_step: the columns made); the flip. In ENTER two columns
        a turn: 0-1, 2-3, ... 12."""
        c = self.c
        if self.state == ST_WAIT:
            return "none"
        p = self.prep_step
        if p >= c["CV_COLS"]:
            self.c_show(state)
            return "corvette flip"
        if p == 0:
            if self.body_x == self.shown_x:
                return "none"
            self.prep_x = self.body_x
            self.c_prep()
        n = 2 if self.state == ST_ENTER else 1
        for x in range(p, p + n):
            self.c_column(state, x)
            self.prep_step += 1
        return f"corvette column {p}" + (f"-{p + 1}" if n == 2 else "")

    def c_prep(self):
        """The body being made (prep_x): its phase, its first column,
        its masks' place (13 x the phase)."""
        self.cv_pp = self.prep_x & 3
        self.cv_pc0 = self.prep_x >> 2
        self.cv_pm = 13 * self.cv_pp

    def c_column(self, state, x):
        """Column x of the other set, if on the screen: its five
        characters from its phase (40 lines), their lines in the
        rock's table; where cv_mask says, the far layer's pixels where
        it has none (the cell kept under it)."""
        c, t = self.c, self.t
        if x >= c["CV_COLS"] or self.cv_pc0 + x >= 40:
            return
        col = self.cv_pc0 + x
        lines = c["CV_LINES"]
        data = self.c_phase(self.cv_pp)[x * lines:(x + 1) * lines]
        first = (self.shown_set ^ 1) * c["CV_CELLS"] + x
        for r in range(c["CV_ROWS"]):
            code = t["cv_code"][first + r * c["CV_COLS"]]
            for line in range(8):
                byte = data[8 * r + line]
                state.charset[code * 8 + line] = byte
                state.rock_lines[line * 256 + code] = byte
            k = r - c["CV_BAND_ROW"]
            if k < 0 or not t["cv_mask"][self.cv_pm + x] >> k & 1:
                continue
            under = self.cv_save_code[r * c["CV_SAVE_COLS"] + col -
                                      c["CV_SAVE_C0"]]
            for line in range(8):
                at = code * 8 + line
                b = state.charset[at]
                m = (b | b >> 1) & 0x55
                m |= m << 1
                state.charset[at] = (state.charset[under * 8 + line] &
                                     ~m & 255) | b
            self.count("the CORVETTE over the far layer")

    def c_show(self, state):
        """The flip: the other set shown from the next frame; its
        columns on the screen (rows 8-12) take its codes and its
        colours by row; the columns it showed and does not now, the
        arena's cells again."""
        c, t = self.c, self.t
        self.shown_set ^= 1
        self.shown_x = self.prep_x
        n0 = self.cv_pc0
        n1 = min(n0 + c["CV_COLS"], 40)
        screen = state.screens[0]
        for r in range(c["CV_ROWS"]):
            row = (c["CV_ROW0"] + r) * 40
            for col in range(self.cv_c0, self.cv_c1):
                if n0 <= col < n1:
                    continue
                k = r * c["CV_SAVE_COLS"] + col - c["CV_SAVE_C0"]
                screen[row + col] = self.cv_save_code[k]
                state.colour[row + col] = self.cv_save_col[k]
                self.count("the CORVETTE leaves a cell: the arena's")
            colour = t["cv_paints"][self.cv_mode * 5 + r] & 15
            for col in range(n0, n1):
                screen[row + col] = t["cv_code"][
                    self.shown_set * c["CV_CELLS"] +
                    r * c["CV_COLS"] + col - n0]
                state.colour[row + col] = colour
        self.cv_c0, self.cv_c1 = n0, n1
        self.prep_step = 0
        self.count("the CORVETTE's body flips")

    def c_paint(self, state, which):
        """Its colours (by row): 0 its own, 1 white, 2 the wreck's, in
        the cells it shows."""
        c, t = self.c, self.t
        self.cv_mode = which
        for r in range(c["CV_ROWS"]):
            row = (c["CV_ROW0"] + r) * 40
            colour = t["cv_paints"][which * 5 + r] & 15
            for col in range(self.cv_c0, self.cv_c1):
                state.colour[row + col] = colour

    def c_step(self):
        """Its turn (after the bar's step): its parts for the frame after
        the next, its step."""
        self.c_partx()
        self.c_place()
        (self.c_wait, self.c_enter, self.c_fight, self.c_open,
         self.c_core, self.c_chain, self.step_wreck, self.step_clear,
         self.step_done)[self.state]()

    def c_partx(self):
        """part_x: the x register of the body's left edge the screen will
        show in the frame after the next."""
        x = self.prep_x if self.prep_step >= self.c["CV_COLS"] \
            else self.shown_x
        self.part_x = 2 * x + 24

    def c_place(self):
        """The turrets left on their mounts, the dome on the tower."""
        c, t = self.c, self.t
        if self.state == ST_WAIT or self.state >= ST_CHAIN:
            return
        for k in range(3, -1, -1):
            if self.parts & 1 and self.cv_live >> k & 1:
                self.place_one(self.cv_part[k], t["cv_turret_dx"][k],
                               t["cv_turret_y"][k])
        if self.parts & 4:
            self.place_one(self.part[2], c["CV_BRIDGE_DX"],
                           c["CV_BRIDGE_Y"])

    def c_wait(self):
        """Its phases made meanwhile, a column a turn; WAIT ends when
        they are made and no Varkon flies or explodes for ARENA_WAIT
        frames."""
        v, c = self.v, self.c
        self.c_make()
        if any(on in (FLYING, BOOM) for on in v.on):
            self.timer = 0
            return
        self.timer = (self.timer + 1) & 255
        if self.timer >= c["ARENA_WAIT"] and \
                self.cv_made >= 3 * c["CV_COLS"]:
            self.c_begin()

    def c_make(self):
        """A column of phases 1-3 (cv_mp + 1, cv_mc): phase 0's shifted
        right by 2 (cv_mp + 1) bits, the column before bringing its
        pixels in."""
        c = self.c
        if self.cv_made >= 3 * c["CV_COLS"]:
            return
        lines, x = c["CV_LINES"], self.cv_mc
        comp = self.t["cv_comp"]
        bits = 2 * (self.cv_mp + 1)
        out = self.cv_phases[self.cv_mp]
        for y in range(lines):
            a = comp[x * lines + y]
            b = comp[(x - 1) * lines + y] if x else 0
            out[x * lines + y] = ((b << 8 | a) >> bits) & 255
        self.cv_made += 1
        self.cv_mc += 1
        if self.cv_mc == c["CV_COLS"]:
            self.cv_mc = 0
            self.cv_mp += 1
        self.count("the CORVETTE: a column of a phase made")

    def c_begin(self):
        """WAIT is over: the arena's cells under its way kept; rows 10-14
        rock, the far layer's codes not; the body at the right, off the
        screen, none of it shown; the bar; ENTER."""
        c, t, state = self.c, self.t, self.state_
        cols = c["CV_SAVE_COLS"]
        for r in range(c["CV_ROWS"]):
            row = (c["CV_ROW0"] + r) * 40 + c["CV_SAVE_C0"]
            for k in range(cols):
                self.cv_save_code[r * cols + k] = state.screens[0][row + k]
                self.cv_save_col[r * cols + k] = state.colour[row + k] & 15
        self.air_rock = 1
        for code in t["cv_far"]:
            for line in range(8):
                state.rock_lines[line * 256 + code] = 0
        self.body_x = self.shown_x = self.prep_x = c["CV_X_START"]
        self.body_xf = self.shown_set = self.prep_step = 0
        self.cv_mode = self.cv_gone = 0
        self.patrol = self.patrol_left = self.parts = 0
        self.drone_turn = 0
        self.cv_c0 = self.cv_c1 = 40
        self.part[2] = 0xFF
        self.bar_on()
        self.state = ST_ENTER
        self.count("the VARKON CORVETTE comes")
        self.c_partx()
        self.c_place()

    def c_enter(self):
        """In from the right, a step at a new body; at its station the
        deck's two turrets (two free Varkon, else a frame later), their
        first fans; the hangar's first scout; the fight."""
        c = self.c
        if not self.c_toward(c["CV_X_STATION"], c["CV_ENTER_STEP"]):
            return
        if not self.c_pair_on(0):
            return
        self.parts = 1
        self.mouth_timer = c["CV_LAUNCH_FIRST"]
        self.patrol = self.patrol_left = 0
        self.state = ST_FIGHT
        self.count("the CORVETTE at its station: its deck's turrets")
        self.c_place()
        self.c_bar()

    def c_pair_on(self, first):
        """A pair of turrets on (first 0: the deck's, 2: the keel's) in
        two free Varkon, their first fans: True; else none, False."""
        t, v = self.t, self.v
        if sum(1 for on in v.on if on == FREE) < 2:
            self.count("a pair of turrets waits for two free Varkon")
            return False
        for k in (first, first + 1):
            i = self.free_varkon()
            self.cv_part[k] = i
            self.cv_live |= 1 << k
            self.new_part(i, self.kind("CTURRET"))
            v.aim[i] = 0
            v.fire[i] = t["cv_fan_first"][k]
        return True

    def c_fight(self):
        """Its patrol, the turrets' fans, the hangar's scouts; the deck's
        two destroyed: CV_PAIR_WAIT frames, then the keel's two (two
        free Varkon, else a frame later); the four destroyed: the
        bridge's wait (OPEN)."""
        c = self.c
        self.c_turrets()
        if self.cv_gone == 15:
            self.parts &= ~1
            self.timer = c["CV_BRIDGE_WAIT"]
            self.state = ST_OPEN
            self.count("the CORVETTE's turrets all destroyed")
            self.c_bar()
            return
        if self.cv_pair == 0:
            if self.cv_gone & 3 == 3:
                self.cv_pair = 1
                self.timer = c["CV_PAIR_WAIT"]
                self.count("the deck's turrets destroyed: the wait")
        elif self.cv_pair == 1:
            self.timer = (self.timer - 1) & 255
            if not self.timer:
                if self.c_pair_on(2):
                    self.cv_pair = 2
                    self.count("the keel's turrets come")
                    self.c_place()
                else:
                    self.timer = 1
        self.c_patrol()
        self.c_fans()
        self.c_hangar()
        self.c_bar()

    def c_turrets(self):
        for k in range(3, -1, -1):
            if not self.cv_live >> k & 1:
                continue
            if self.v.on[self.cv_part[k]] != FLYING:
                self.cv_gone |= 1 << k
                self.cv_live &= ~(1 << k)
                self.count(f"turret {k} destroyed")

    def c_fans(self):
        v = self.v
        for k in range(3, -1, -1):
            if not self.cv_live >> k & 1:
                continue
            i = self.cv_part[k]
            v.fire[i] = (v.fire[i] - 1) & 255
            if not v.fire[i]:
                self.c_fan(i)

    def c_fan(self, i):
        """Turret i's fan: up at the ship above it (the low pod's fans),
        else down or left (the top pod's); CV_FAN_PERIOD to the next."""
        c, v = self.c, self.v
        self.aim_one(i, "a turret")
        base, which = c["POD_FAN_FIRST"], "a turret, up"
        if not v.aim[i]:
            self.aim_top(i, "a turret")
            base, which = c["POD_FAN_FIRST"] + 9, "a turret, down"
        self.fan_pod(i, base, which)
        v.fire[i] = c["CV_FAN_PERIOD"]

    def c_hangar(self):
        """Every CV_LAUNCH_EVERY frames a scout from the hangar (a free
        Varkon; none, or CV_SCOUTS_MAX scouts flying: none), its path
        up or low in turn."""
        c, v, t = self.c, self.v, self.t
        self.mouth_timer = (self.mouth_timer - 1) & 255
        if self.mouth_timer:
            return
        self.mouth_timer = c["CV_LAUNCH_EVERY"]
        scout = self.kind("SCOUT")
        flying = sum(1 for i in range(len(v.on))
                     if v.on[i] == FLYING and v.kind[i] == scout)
        if flying >= c["CV_SCOUTS_MAX"]:
            self.count("the hangar: scouts enough")
            return
        i = self.free_varkon()
        if i is None:
            self.count("the hangar: no free Varkon")
            return
        self.new_part(i, scout)
        v.y[i] = c["CV_HANGAR_Y"] << 8 | (v.y[i] & 255)
        v.x[i] = ((c["CV_HANGAR_DX"] + self.part_x) & 0xFFFF) << 8
        v.fire[i] = t["kind_period"][scout] >> 1
        v.seg[i] = (c["PATH_LAUNCH_UP"], c["PATH_LAUNCH_LOW"])[
            self.drone_turn]
        self.count(("a scout from the hangar, up",
                    "a scout from the hangar, low")[self.drone_turn])
        self.drone_turn ^= 1
        v.load(i)
        v.sound("missile")

    def c_open(self):
        """The turrets gone: CV_BRIDGE_WAIT frames, then the dome in a
        free Varkon (its first shot, the bridge's patrol): CORE."""
        c, v = self.c, self.v
        self.c_patrol()
        self.c_hangar()
        self.timer = (self.timer - 1) & 255
        if self.timer:
            self.c_bar()
            return
        i = self.free_varkon()
        if i is None:
            self.timer = 1
            self.count("the bridge waits for a free Varkon")
            self.c_bar()
            return
        self.part[2] = i
        self.new_part(i, self.kind("CBRIDGE"))
        v.fire[i] = c["CV_BRIDGE_FIRST"]
        self.parts |= 4
        self.patrol, self.patrol_left = 2, 0
        self.state = ST_CORE
        self.count("the CORVETTE's bridge: its dome")
        self.c_place()
        self.c_bar()

    def c_core(self):
        """The dome's fight: destroyed, the end; under CV_RAGE_LIFE its
        shots faster."""
        c, v = self.c, self.v
        i = self.part[2]
        if v.on[i] != FLYING:
            self.count("the CORVETTE's bridge destroyed")
            self.dies()
            return
        if v.life[i] < c["CV_RAGE_LIFE"] + 1:
            if v.period[i] != c["CV_RAGE_PERIOD"]:
                self.count("the CORVETTE's bridge: faster")
            v.period[i] = c["CV_RAGE_PERIOD"]
        self.c_patrol()
        self.c_hangar()
        self.c_bar()

    def c_bar(self):
        c, v = self.c, self.v
        total = 0
        for k in range(3, -1, -1):
            if self.cv_gone >> k & 1:
                continue
            life = v.life[self.cv_part[k]] if self.cv_live >> k & 1 \
                else c["CV_TURRET_LIFE"]
            total = (total + life) & 255
        total += c["CV_BRIDGE_LIFE"] if self.part[2] == 0xFF \
            else v.life[self.part[2]]
        self.bar_want = self.t["cv_bar_of"][total & 255]

    def c_patrol(self):
        """Wait at a place, then to the other of its two, a step at a new
        body (its entry: 0-1 the turrets' fight, 2-3 the bridge's)."""
        t = self.t
        if self.patrol_left:
            self.patrol_left -= 1
            return
        k = self.patrol
        if self.c_toward(t["cv_patrol_to"][k], t["cv_patrol_step"][k]):
            self.patrol_left = t["cv_patrol_wait"][k]
            self.patrol = k ^ 1

    def c_toward(self, to, step):
        """A step to x = to, `step` pixels at most, when the body is
        shown where it is: True if it is there already (shown there)."""
        if self.prep_step or self.body_x != self.shown_x:
            return False
        x = self.body_x
        if x == to:
            return True
        if x > to:
            self.body_x = to if x - to <= step else x - step
        else:
            self.body_x = to if to - x <= step else x + step
        return False

    def c_chain(self):
        """As step_chain, on its body: the fireball at cv_chain_dx from
        part_x, on line cv_chain_y."""
        c, t, v = self.c, self.t, self.v
        self.timer = (self.timer + 1) & 255
        if self.timer < c["CHAIN_EVERY"]:
            return
        self.timer = 0
        i = self.free_varkon()
        if i is not None:
            self.set_pri(i, 2)
            v.on[i] = BOOM
            v.kind[i] = self.kind("CBRIDGE")
            v.left[i] = v.flash[i] = v.cap[i] = 0
            k = self.chain_k
            v.y[i] = t["cv_chain_y"][k] << 8 | (v.y[i] & 255)
            v.x[i] = ((t["cv_chain_dx"][k] + self.part_x) & 0xFFFF) << 8
            self.count("a fireball of the chain")
        else:
            self.count("the chain: no free Varkon")
        v.sound("explode")
        self.flash = 3
        self.paint(self.state_, 1)
        self.chain_k += 1
        if self.chain_k >= c["CHAIN_COUNT"]:
            self.state = ST_WRECK

    # --- the DEFENSE TURRET ARRAY (defense.asm) ----------------------

    def d_cell(self, row, col):
        """Screen A's cell of its row, column (the wall's)."""
        c = self.c
        return (c["DT_ROW0"] + row) * 40 + c["DT_COL0"] + col

    def d_draw(self, state):
        """A turn in the arena (boss_draw): in ENTER a row of its cells;
        else a patch whose state changed; else the ray on or off; else,
        the ray on, every 4 frames its other picture."""
        c, t = self.c, self.t
        if self.state == ST_WAIT:
            return "none"
        if self.dt_drawn < self.dt_wrows:
            row = t["dt_closing"][self.dt_drawn]
            self.dt_drawn += 1
            for col in range(c["DT_COLS"]):
                k = row * c["DT_COLS"] + col
                at = self.d_cell(row, col)
                state.screens[0][at] = t["dt_wall"][k]
                state.colour[at] = t["dt_colour"][k] & 15
            self.count("the ARRAY closes in: a row of its cells")
            return "array row"
        for p in range(c["DT_PATCHES"] - 1, -1, -1):
            if self.dt_want[p] != self.dt_have[p]:
                s = self.dt_have[p] = self.dt_want[p]
                codes = t[f"dt_p_code{s}"]
                for k in range(t["dt_p_first"][p], t["dt_p_first"][p + 1]):
                    at = t["dt_p_lo"][k] | t["dt_p_hi"][k] << 8
                    state.screens[0][at] = codes[k]
                self.count(f"a patch of the ARRAY: {p} to {s}")
                return "array patch"
        if self.dt_rwant != self.dt_rhave:
            self.dt_rhave = self.dt_rwant
            n, row = c["DT_RAY_COLS"], c["DT_RAY_ROW"] * 40
            screen = state.screens[0]
            if self.dt_rhave:
                for col in range(n):
                    self.dt_save[col] = screen[row + col]
                    self.dt_save[n + col] = screen[row + 40 + col]
                    self.dt_save[2 * n + col] = state.colour[row + col] & 15
                    self.dt_save[3 * n + col] = \
                        state.colour[row + 40 + col] & 15
                    screen[row + col] = c["DT_RAY_CODE"]
                    screen[row + 40 + col] = c["DT_RAY_CODE2"]
                    state.colour[row + col] = c["DT_RAY_OWN"]
                    state.colour[row + 40 + col] = c["DT_RAY_OWN"]
                self.count("the ARRAY's ray drawn")
                return "array ray on"
            for col in range(n):
                screen[row + col] = self.dt_save[col]
                screen[row + 40 + col] = self.dt_save[n + col]
                state.colour[row + col] = self.dt_save[2 * n + col]
                state.colour[row + 40 + col] = self.dt_save[3 * n + col]
            self.count("the ARRAY's ray off: the arena's cells again")
            return "array ray off"
        if self.dt_rhave and not state.varkon.anim & 3:
            self.dt_shim ^= 1
            pic = t["dt_rays"][16 * self.dt_shim:16 * self.dt_shim + 16]
            for code, half in ((c["DT_RAY_CODE"], 0),
                               (c["DT_RAY_CODE2"], 8)):
                state.charset[code * 8:code * 8 + 8] = \
                    bytes(pic[half:half + 8])
            self.count("the ARRAY's ray shimmers")
            return "array shimmer"
        return "none"

    def d_paint(self, state, which):
        """Its colours: 0 its own, 1 white, 2 the wreck's, in all its
        cells."""
        c, t = self.c, self.t
        self.dt_mode = which
        for row in range(c["DT_ROWS"]):
            for col in range(c["DT_COLS"]):
                k = row * c["DT_COLS"] + col
                colour = (t["dt_colour"][k], c["DT_FLASH_OWN"],
                          c["DT_WRECK_OWN"])[which]
                state.colour[self.d_cell(row, col)] = colour & 15

    def d_step(self):
        """Its turn (after the bar's step): part_x its own, its step."""
        self.part_x = self.c["DT_PART_X"]
        (self.d_wait, self.d_enter, self.d_fight, self.d_open,
         self.d_core, self.d_chain, self.step_wreck, self.step_clear,
         self.step_done)[self.state]()

    def d_place(self, i, dx, y):
        """Varkon i at part_x + dx (its x register), line y."""
        v = self.v
        v.y[i] = y << 8 | (v.y[i] & 255)
        v.x[i] = ((self.part_x + dx) & 0xFFFF) << 8

    def d_wait(self):
        """Its codes, four a turn; no Varkon flying or exploding, its
        pictures, one a turn; then ARENA_WAIT frames: the begin."""
        v, c = self.v, self.c
        self.d_codes()
        if any(on in (FLYING, BOOM) for on in v.on):
            self.timer = 0
            return
        self.d_picture()
        self.timer = (self.timer + 1) & 255
        groups = (c["DT_CODES"] + 3) // 4
        if self.timer >= c["ARENA_WAIT"] and \
                self.dt_made >= groups + c["DT_PICTURE_BYTES"] // 64:
            self.d_begin()

    def d_codes(self):
        c, t, state = self.c, self.t, self.state_
        groups = (c["DT_CODES"] + 3) // 4
        if self.dt_made >= groups:
            return
        first = 4 * self.dt_made
        self.dt_made += 1
        for k in range(first, min(first + 4, c["DT_CODES"])):
            code = t["dt_code"][k]
            data = t["dt_chars"][8 * k:8 * k + 8]
            state.charset[code * 8:code * 8 + 8] = bytes(data)
            for line in range(8):
                state.rock_lines[line * 256 + code] = \
                    data[line] if k < c["DT_WALL_CODES"] else 0
        self.count("the ARRAY: four of its codes made")

    def d_picture(self):
        c, state = self.c, self.state_
        groups = (c["DT_CODES"] + 3) // 4
        k = self.dt_made - groups
        if not 0 <= k < c["DT_PICTURE_BYTES"] // 64:
            return
        self.dt_made += 1
        d = self.files["defense"]
        at = d["sprite_at"] - (c["SPRITES2"]) + 64 * k
        state.sprites2[at:at + 64] = bytes(d["pictures"][64 * k:
                                                          64 * k + 64])
        self.count("the ARRAY: a picture of its parts made")

    def d_begin(self):
        """Rows 10-14 rock, the far layer's codes not; the turrets'
        lives; the bar; ENTER."""
        c, t, state = self.c, self.t, self.state_
        self.air_rock = 1
        for code in t["dt_far"]:
            for line in range(8):
                state.rock_lines[line * 256 + code] = 0
        self.dt_life = [c["DT_TURRET_LIFE"]] * 6
        self.timer = self.parts = self.dt_mode = 0
        self.part[2] = 0xFF
        self.bar_on()
        self.state = ST_ENTER
        self.count("the DEFENSE TURRET ARRAY comes")

    def d_enter(self):
        """A row more every DT_ENTER_EVERY frames; all drawn: its
        sound, the fight (the first row after DT_SHUT_WAIT)."""
        c, t = self.c, self.t
        if self.dt_wrows < c["DT_ROWS"]:
            self.timer = (self.timer + 1) & 255
            if self.timer >= c["DT_ENTER_EVERY"]:
                self.timer = 0
                self.dt_wrows += 1
            return
        if self.dt_drawn < c["DT_ROWS"]:
            return
        self.v.sound("boom")
        self.dt_turn = self.dt_cycle = 0
        self.dt_row = t["dt_tier"][0]
        self.timer = c["DT_SHUT_WAIT"]
        self.state = ST_FIGHT
        self.count("the ARRAY closed in: the fight")
        self.d_bar()

    def d_fight(self):
        """Its rows in turn (see defense.asm's dt_fight)."""
        c, t, v = self.c, self.t, self.v
        if self.dt_cycle != 2:
            self.timer = (self.timer - 1) & 255
            if self.timer:
                self.d_bar()
                return
            if self.dt_cycle == 0:
                self.dt_want[self.dt_row] = self.dt_cycle = 1
                self.timer = c["DT_ANIM"]
                self.count("a row of the ARRAY: half open")
                self.d_bar()
                return
            if self.dt_cycle == 1:
                if not self.d_row_on():
                    self.timer = 1
                    self.d_bar()
                    return
                self.dt_want[self.dt_row] = self.dt_cycle = 2
                self.timer = c["DT_OPEN_FRAMES"]
                self.parts |= 1
                self.count(f"row {self.dt_row} of the ARRAY open: its "
                           "turrets")
                self.d_bar()
                return
            self.dt_want[self.dt_row] = 0
            self.count("a row of the ARRAY shut")
            self.d_next()
            self.d_bar()
            return
        self.d_turrets()
        if self.dt_gone == 0x3F:
            self.state = ST_OPEN
            self.timer = c["DT_CORE_WAIT"]
            self.dt_cycle = self.parts = 0
            self.count("the ARRAY's turrets all destroyed")
            self.d_bar()
            return
        bits = t["dt_row_bits"][self.dt_row]
        if self.dt_gone & bits == bits:
            self.parts &= ~1
            self.count("a row's turrets destroyed: it stays open")
            self.d_next()
            self.d_bar()
            return
        self.d_fans()
        self.timer = (self.timer - 1) & 255
        if self.timer:
            self.d_bar()
            return
        for k in range(5, -1, -1):
            if self.dt_live >> k & 1:
                v.on[self.dt_part[k]] = FREE
                self.count("a turret of the ARRAY back in")
        self.dt_live = 0
        self.parts &= ~1
        self.dt_want[self.dt_row] = 1
        self.dt_cycle = 3
        self.timer = c["DT_ANIM"]
        self.count("a row of the ARRAY: half shut")
        self.d_bar()

    def d_next(self):
        """The next row with turrets left (this one again if it is the
        last): shut, DT_SHUT_WAIT frames."""
        c, t = self.c, self.t
        y = self.dt_turn
        while True:
            y = y + 1 if y + 1 < c["DT_TIERS"] else 0
            x = t["dt_tier"][y]
            bits = t["dt_row_bits"][x]
            if self.dt_gone & bits != bits:
                break
        self.dt_turn, self.dt_row = y, x
        self.dt_cycle = 0
        self.timer = c["DT_SHUT_WAIT"]

    def d_row_on(self):
        """The row's turrets not destroyed in free Varkon, their lives
        as they were, their first fans: True; not enough free: False."""
        t, v = self.t, self.v
        first = 2 * self.dt_row
        wanted = [k for k in (first, first + 1)
                  if not self.dt_gone >> k & 1]
        if sum(1 for on in v.on if on == FREE) < len(wanted):
            self.count("a row of the ARRAY waits for free Varkon")
            return False
        for k in wanted:
            i = self.free_varkon()
            self.dt_part[k] = i
            self.dt_live |= 1 << k
            self.new_part(i, self.kind("ATURRET"))
            v.life[i] = self.dt_life[k]
            v.aim[i] = 0
            v.fire[i] = t["dt_fan_first"][k]
            self.d_place(i, t["dt_turret_dx"][k], t["dt_turret_y"][k])
        return True

    def d_turrets(self):
        for k in range(5, -1, -1):
            if not self.dt_live >> k & 1:
                continue
            i = self.dt_part[k]
            if self.v.on[i] != FLYING:
                self.dt_gone |= 1 << k
                self.dt_live &= ~(1 << k)
                self.dt_life[k] = 0
                self.count(f"turret {k} of the ARRAY destroyed")
            else:
                self.dt_life[k] = self.v.life[i]

    def d_fans(self):
        c, v = self.c, self.v
        for k in range(5, -1, -1):
            if not self.dt_live >> k & 1:
                continue
            i = self.dt_part[k]
            v.fire[i] = (v.fire[i] - 1) & 255
            if v.fire[i]:
                continue
            self.aim_one(i, "a turret of the ARRAY")
            base, which = c["POD_FAN_FIRST"], "a turret of the ARRAY, up"
            if not v.aim[i]:
                self.aim_top(i, "a turret of the ARRAY")
                base = c["POD_FAN_FIRST"] + 9
                which = "a turret of the ARRAY, down"
            self.fan_pod(i, base, which)
            v.fire[i] = c["DT_FAN_PERIOD"]

    def d_open(self):
        """DT_CORE_WAIT frames, the hatch half open; DT_ANIM, open;
        DT_ANIM, the lens in a free Varkon: its first shot, the calm."""
        c, v = self.c, self.v
        self.timer = (self.timer - 1) & 255
        if self.timer:
            self.d_bar()
            return
        if self.dt_cycle != 2:
            self.dt_cycle += 1
            self.dt_want[3] = self.dt_cycle
            self.timer = c["DT_ANIM"]
            self.count(("", "the ARRAY's hatch half open",
                        "the ARRAY's hatch open")[self.dt_cycle])
            self.d_bar()
            return
        i = self.free_varkon()
        if i is None:
            self.timer = 1
            self.count("the lens waits for a free Varkon")
            self.d_bar()
            return
        self.part[2] = i
        self.new_part(i, self.kind("ACORE"))
        v.fire[i] = c["DT_CORE_FIRST"]
        self.d_place(i, c["DT_LENS_DX"], c["DT_LENS_Y"])
        self.parts |= 4
        self.dt_ray = 0
        self.dt_rt = c["DT_CALM"]
        self.state = ST_CORE
        self.count("the ARRAY's core: its lens")
        self.d_bar()

    def d_core(self):
        """Calm (its aimed shots), it warns (its colours in turn, no
        shot), its ray (no shot; the ship on its lines hurt), the calm
        again; destroyed: the ray off, the end."""
        c, t, v = self.c, self.t, self.v
        i = self.part[2]
        if v.on[i] != FLYING:
            self.dt_rwant = self.dt_ray = 0
            self.count("the ARRAY's lens destroyed")
            self.dies()
            return
        if self.dt_ray == 0:
            self.dt_rt = (self.dt_rt - 1) & 255
            if self.dt_rt:
                self.d_bar()
                return
            self.dt_ray = 1
            self.dt_rt = c["DT_WARN"]
            v.sound("plasma")
            self.count("the ARRAY's lens warns")
        v.fire[i] = 2
        if self.dt_ray == 1:
            v.own[i] = t["dt_warn_own"][(self.dt_rt >> 2) & 1]
            self.dt_rt = (self.dt_rt - 1) & 255
            if self.dt_rt:
                self.d_bar()
                return
            self.dt_ray = 2
            self.dt_rwant = 1
            v.own[i] = 1
            self.dt_rt = c["DT_RAY_FRAMES"]
            v.sound("laser")
            self.count("the ARRAY's ray")
            self.d_bar()
            return
        self.d_burn()
        self.dt_rt = (self.dt_rt - 1) & 255
        if self.dt_rt:
            self.d_bar()
            return
        self.dt_rwant = self.dt_ray = 0
        v.own[i] = c["DT_LENS_OWN"]
        v.fire[i] = c["DT_CORE_FIRST"]
        rage = v.life[i] < c["DT_RAGE_LIFE"] + 1
        self.dt_rt = c["DT_CALM_RAGE"] if rage else c["DT_CALM"]
        if rage:
            self.count("the ARRAY's lens: shorter calms")
        self.d_bar()

    def d_burn(self):
        """The ray drawn, the ship flying not blinking (sb), its box
        (against the Varkon) on the ray's lines: DT_RAY_HURT notches."""
        c, v = self.c, self.v
        if not self.dt_rhave or not v.sb:
            return
        left, right, top, bottom = v.sb
        if top < c["DT_RAY_BOTTOM"] and bottom > c["DT_RAY_TOP"]:
            self.count("the ARRAY's ray on the ship")
            self.state_.ship.hurt(c["DT_RAY_HURT"], "the ARRAY's ray")
        else:
            self.count("the ARRAY's ray: the ship off its lines")

    def d_bar(self):
        c, v = self.c, self.v
        total = 0
        for k in range(5, -1, -1):
            if self.dt_gone >> k & 1:
                continue
            life = v.life[self.dt_part[k]] if self.dt_live >> k & 1 \
                else self.dt_life[k]
            total = (total + life) & 255
        total += c["DT_CORE_LIFE"] if self.part[2] == 0xFF \
            else v.life[self.part[2]]
        self.bar_want = self.t["dt_bar_of"][total & 255]

    def d_chain(self):
        """As step_chain, on the wall: the fireball at dt_chain_dx from
        part_x, on line dt_chain_y."""
        c, t, v = self.c, self.t, self.v
        self.timer = (self.timer + 1) & 255
        if self.timer < c["CHAIN_EVERY"]:
            return
        self.timer = 0
        i = self.free_varkon()
        if i is not None:
            self.set_pri(i, 2)
            v.on[i] = BOOM
            v.kind[i] = self.kind("ACORE")
            v.left[i] = v.flash[i] = v.cap[i] = 0
            k = self.chain_k
            self.d_place(i, t["dt_chain_dx"][k], t["dt_chain_y"][k])
            self.count("a fireball of the chain")
        else:
            self.count("the chain: no free Varkon")
        v.sound("explode")
        self.flash = 3
        self.paint(self.state_, 1)
        self.chain_k += 1
        if self.chain_k >= c["CHAIN_COUNT"]:
            self.state = ST_WRECK

    # --- the HUD (update_hud) ----------------------------------------

    def hud(self, screen):
        if not self.bar_dirty:
            return
        self.bar_dirty = 0
        c = self.c
        left = self.bar_shown
        for k in range(c["BAR_CELLS"]):
            if left >= 9:
                code, left = c["BAR_CODE"] + 8, left - 8
            else:
                code, left = c["BAR_CODE"] + left, 0
            screen[HUD_CELL + c["HUD_BAR"] + k] = code

    def part_block(self, i):
        """A part's picture (part_picture)."""
        v, c = self.v, self.c
        if v.kind[i] >= self.kind("SEGMENT"):     # two each
            return v.t["kind_block"][v.kind[i]] + (v.anim3 & 1)
        if v.kind[i] == self.kind("CANNON"):
            return v.t["kind_block"][v.kind[i]] + v.aim[i]
        if self.state == ST_OPEN:
            return c["CORE_RISE_BLOCK"] + ((self.timer - 1) & 255) // 8
        return v.t["kind_block"][v.kind[i]] + v.anim3

    # --- for the test: the variables as the program keeps them -------

    def memory(self):
        """$0232-$024d: arena .. part_x (b_tmp is scratch)."""
        return bytes([
            self.arena, self.state, self.timer, self.body_x,
            self.body_xf, self.body_var, self.shown_x, self.shown_var,
            self.shown_set, self.shown_col, self.prep_x, self.prep_var,
            self.prep_step, self.patrol, self.patrol_left, self.part[0],
            self.part[1], self.part[2], self.parts, self.mouth_timer,
            self.drone_turn, self.chain_k, self.bar_want, self.bar_shown,
            self.bar_dirty, self.flash, self.part_x & 255,
            self.part_x >> 8])

    def warden_memory(self):
        """$0258-$0271: arena_chars, the WARDEN's variables
        (wd_gone ... wd_kb1; its scratch after them left out)."""
        return bytes([self.arena_chars, self.wd_gone] + self.wd_life +
                     self.wd_want + self.wd_have +
                     [self.wd_r0, self.wd_r1, self.wd_colour,
                      self.wd_port, self.wd_s, self.wd_off,
                      self.wd_row0, self.wd_kb0, self.wd_kb1])

    def corvette_memory(self):
        """$0258-$0268: arena_chars, the CORVETTE's variables
        (cv_gone ... cv_pm, with cv_live and cv_pair; cv_base, an
        address, and its scratch after them left out)."""
        return bytes([self.arena_chars, self.cv_gone] +
                     [k & 255 for k in self.cv_part] +
                     [self.cv_live, self.cv_pair,
                      self.cv_c0, self.cv_c1, self.cv_mode,
                      self.cv_made, self.cv_mp, self.cv_mc, self.cv_pp,
                      self.cv_pc0, self.cv_pm])

    def defense_memory(self):
        """$0258-$027a: arena_chars, the ARRAY's variables
        (dt_gone ... dt_mode; its scratch after them left out)."""
        return bytes([self.arena_chars, self.dt_gone] +
                     [k & 255 for k in self.dt_part] + self.dt_life +
                     [self.dt_live, self.dt_turn, self.dt_row,
                      self.dt_cycle] + self.dt_want + self.dt_have +
                     [self.dt_wrows, self.dt_drawn, self.dt_made,
                      self.dt_ray, self.dt_rt, self.dt_rwant,
                      self.dt_rhave, self.dt_shim, self.dt_mode])

    def core_memory(self):
        """$0258-$0264: arena_chars, cb_angle (2), cb_open_k,
        cb_open_r, cb_rad, cb_open_t, cb_shots, cb_seg (4), cb_paint;
        $026a-$02b5: cb_last (4), cb_save (the arena's cells under the
        sphere)."""
        return bytes([self.arena_chars, self.cb_angle & 255,
                      self.cb_angle >> 8, self.cb_open_k, self.cb_open_r,
                      self.cb_rad, self.cb_open_t, self.cb_shots] +
                     [k & 255 for k in self.cb_seg] + [self.cb_paint]), \
            bytes(self.cb_last + self.cb_save)
