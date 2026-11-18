"""The model of the ship and its shots: what the program does with them,
frame by frame (hurt by the Varkon too, varkon_model.py; its weapons,
the missile, the satellite).

Ship.step() is the turn's ship: the joystick (eight directions at the
ship's speed and its S capsules'), the push away from the rock and the
blinking, the shield, the explosion (a weapon level lost, the satellite
lost), the wait; then another ship to choose, held at its place (CHOOSE:
scroll_model.State, the game held), or no ships left (GAME OVER); the
satellite after the ship, Fire (the weapon's volley, when all its shots
have free places; the satellite's bolt, the missile); then the shots fly
on (some climb or dive) or count a blast's frames, and the missile falls
or runs along the floor. shots_rock(), after the sprites are written:
the shots meet the rock (a Gauss shot bursts: a blast). sprites() gives
the ship's two sprites (0 and 1) as the program writes them to the
VIC-II for the next frame, shot_objects() the four shots as objects of
the multiplexer, more_objects() the satellite and the missile (objects
22 and 23).
The rock is read from the screen the next frame shows, pixel by pixel: a
pair of a multicolour cell that is not background is rock (through the
rock's table; in the SIEGE CRAWLER's arena, from the characters
themselves: arena_chars). The missile ends on a boss's body only in the
crawler's arena. Rows 10-14 (the corridor) are never rock, but while the
GRAVEYARD WARDEN is in level 3's arena (air_rock): its body is rock
there too; the same for the VARKON CORVETTE in level 4's, the DEFENSE
TURRET ARRAY's wall in level 5's, the SUPER-COMPUTER VARKON's rings,
shell and housing in level 6's.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       "game/assets"))
import sfx           # noqa: E402

import parts         # noqa: E402  (D.2) the steps of the chain

CONTROL, EXPLODE, WAIT, ENTER, LEAVE, GONE, CHOOSE = range(7)
UP, DOWN, LEFT, RIGHT, FIRE = 1, 2, 4, 8, 16
SHOTS = 4                      # objects 0-3 of the multiplexer
EFFECTS = [e[0] for e in sfx.compile_effects()[0]]
FALL, RUN = 1, 2               # the missile


def signed8(v):
    return v - 256 if v & 0x80 else v


class Shot:
    """A shot of the ship: x (pixels, the sprite's left edge), y (its
    top line, a byte), kind, halves (mask), y velocity, the Varkon it
    has pierced (a set), blast frames left (0: a shot)."""

    def __init__(self, t, x, y, kind):
        self.x, self.y, self.kind = x, y, kind
        self.mask = t["shot_halves"][kind]
        self.dy = signed8(t["shot_vy"][kind])
        self.pierced = set()
        self.bl = 0


class Missile:
    def __init__(self, x, y):
        self.on, self.x, self.y = FALL, x, y


class Blast:
    """A blast's box (hits' units: x register / 2, y register; right
    and bottom excluded), its damage, the Varkon not to try (None)."""

    def __init__(self, left, top, right, bottom, damage, skip):
        self.left, self.top = left, top
        self.right, self.bottom = right, bottom
        self.damage, self.skip = damage, skip


class Ship:
    def __init__(self, files):
        self.c = files["constants"]
        self.t = files["tables"]
        self.type = 0
        self.lives = self.c["LIVES"]
        self.shots = [None] * SHOTS      # Shot or None
        self.gameover = False
        self.stats = {}                  # what happened, for the test
        self.sound = lambda effect: None   # sfx_start (player_model)
        self.anim = lambda: 0            # varkon_model's anim
        self.blast = None                # the blast armed
        self.invuln = False              # the key I
        self.chosen = False              # a ship to choose
        self.reset_weapons()
        self.choose_next()               # init_ship

    # --- the weapons ------------------------------------------------

    def reset_weapons(self):
        self.weapon, self.s_caps, self.missiles = 0, 0, 0
        self.sat = None                  # [x, y]
        self.missile = None

    def windex(self):
        return self.type * 4 + self.weapon

    def speed(self):
        t = self.t
        return (t["ship_speed_lo"][self.type] |
                t["ship_speed_hi"][self.type] << 8) + \
            self.s_caps * self.c["SPEED_STEP"]

    def again(self, skip=False):
        """The level again after STAGE CLEAR (ship_again): the ship
        comes in from the left, its satellite with it. Also after the
        key L (skip)."""
        self.come_in(self.c["ENTER_X"] - 256, ENTER)
        if self.sat:
            self.sat = [self.x, self.y]
        self.count("the ship in again after the key L" if skip else
                   "the ship in again after STAGE CLEAR")

    def choose_next(self, lost=False):
        """choose_next: the next ship to choose, at its place (at a
        game's start START_X; after a ship lost, choose_lost, ENTER_TO;
        ENTER_Y), held (the State sees `chosen`)."""
        self.come_in(self.c["ENTER_TO" if lost else "START_X"], CHOOSE)
        self.chosen = True
        self.lost = lost                 # after the choice: in from
                                         # the left (held_time 1)

    def go(self):
        """Fire on the choice: at a game's start it flies from its
        place, blinking; after a ship lost it comes in from the left."""
        if self.lost:
            self.come_in(self.c["ENTER_X"] - 256, ENTER)
            self.count("back in from the left")
        else:
            self.mode = CONTROL
            self.blink = self.c["ENTER_BLINK"]

    def choose(self, k):
        """ship_shown: ship k chosen, its weapon (the level it
        had), its full shield."""
        self.type = k
        self.shield = self.t["ship_shield"][k]

    def come_in(self, x, mode):
        c = self.c
        self.mode, self.timer = mode, 0
        self.x, self.xf = x, 0
        self.y, self.yf = c["ENTER_Y"], 0
        self.shield = self.t["ship_shield"][self.type]
        self.blink = c["ENTER_BLINK"]
        self.push, self.push_dx, self.push_dy = 0, 0, 0
        self.figure, self.cooldown = 0, 0

    # --- the rock ----------------------------------------------------

    @staticmethod
    def solid(state, px, py):
        """Is the pixel (px, py) of the playfield rock, in the screen
        the next frame shows (state.front), at its fine scroll?"""
        if py < 0 or py >= 176:
            return False
        row = py >> 3
        if 10 <= row <= 14 and not state.boss.air_rock:   # (but a
            return False                  # boss's body there)
        q = px - state.near_xs
        if q < 0 or q >= 320:
            return False
        code = state.screens[state.front][row * 40 + (q >> 3)]
        if code < state.c["FIRST_SOLID"]:
            return False
        # in the crawler's arena the characters themselves; else the rock's
        # table (without the scenery, the beams only when on; also in the
        # other arenas)
        if state.boss.arena_chars:
            byte = state.charset[code * 8 + (py & 7)]
        else:
            byte = state.rock_lines[(py & 7) * 256 + code]
        return byte & (0xC0 >> ((q & 7) >> 1) * 2) != 0

    @staticmethod
    def point_cell(state, px, py):
        """For the counts: the code under the pixel (px,
        py) as solid() finds it, and whether the character draws the
        pixel; None where solid() looks at no cell."""
        if py < 0 or py >= 176 or (10 <= py >> 3 <= 14 and
                                   not state.boss.air_rock):
            return None
        q = px - state.near_xs
        if q < 0 or q >= 320:
            return None
        code = state.screens[state.front][(py >> 3) * 40 + (q >> 3)]
        byte = state.charset[code * 8 + (py & 7)]
        return code, byte & (0xC0 >> ((q & 7) >> 1) * 2) != 0

    def passing(self, state):
        """For the counts: a point of the ship on a pixel
        that is drawn but not rock (level 2's clouds, a dimmed
        beam)."""
        c = self.c
        first = self.type * 5
        for dx, dy in zip(self.t["ship_spot_x"][first:first + 5],
                          self.t["ship_spot_y"][first:first + 5]):
            found = self.point_cell(state, self.x + dx, self.y + dy)
            if not found or not found[1] or \
                    self.solid(state, self.x + dx, self.y + dy):
                continue
            if found[0] >= c["DECOR_FIRST"]:
                self.count("through the scenery: not rock")
            elif c["BEAM_DOWN"] and found[0] in (c["BEAM_DOWN"],
                                                 c["BEAM_UP"]):
                self.count("through a dimmed beam: not rock")

    def touching(self, state):
        """Which of the five points are in the rock."""
        first = self.type * 5
        xs = self.t["ship_spot_x"][first:first + 5]
        ys = self.t["ship_spot_y"][first:first + 5]
        return [self.solid(state, self.x + dx, self.y + dy)
                for dx, dy in zip(xs, ys)]

    # --- one frame ---------------------------------------------------

    def count(self, what):
        self.stats[what] = self.stats.get(what, 0) + 1

    def step(self, state, joy, keys):
        c, t = self.c, self.t
        self.gameover = False
        if self.mode == CONTROL:
            if self.blink:
                self.blink -= 1
            if self.push:
                self.x += self.push_dx
                self.y += self.push_dy
                self.push -= 1
                self.figure = 0
            else:
                speed = self.speed()
                x = (self.x << 8 | self.xf)
                y = (self.y << 8 | self.yf)
                if joy & RIGHT:
                    x += speed
                elif joy & LEFT:
                    x -= speed
                if joy & UP:
                    y -= speed
                elif joy & DOWN:
                    y += speed
                self.x, self.xf = x >> 8, x & 255
                self.y, self.yf = y >> 8, y & 255
                self.figure = 1 if joy & UP else 2 if joy & DOWN else 0
            if self.x < c["X_MIN"]:
                self.x, self.xf = c["X_MIN"], 0
            elif self.x > c["X_MAX"]:
                self.x, self.xf = c["X_MAX"], 0
            if self.y < c["Y_MIN"]:
                self.y, self.yf = c["Y_MIN"], 0
            elif self.y > c["Y_MAX"]:
                self.y, self.yf = c["Y_MAX"], 0
            if not self.push:
                self.collide(state)
            self.passing(state)                # the counts
            self.move_satellite()
            if self.cooldown:
                self.cooldown -= 1
            if self.mode == CONTROL and joy & FIRE and \
                    not self.cooldown and parts.has("varkon"):
                self.fire()                 # (D.2: from step 4)
        elif self.mode == EXPLODE:
            self.timer += 1
            if self.timer == c["EXPLOSION_FRAMES"]:
                self.mode, self.timer = WAIT, 0
        elif self.mode == WAIT:
            self.timer += 1
            if self.timer == c["WAIT_FRAMES"]:
                if not parts.has("states"):     # (D.2) steps 3-15:
                    if self.lives == 0:         # three more; in again
                        self.lives = c["LIVES"]
                        self.count("no ships left: three more")
                    self.come_in(c["ENTER_X"] - 256, ENTER)
                    self.count("a ship lost: in again from the left")
                elif self.lives == 0:           # GAME OVER
                    self.gameover = True
                    self.count("no ships left: GAME OVER")
                else:                           # the next one
                    self.count("a ship lost: another to choose")
                    if state.boss.arena:
                        self.count("a ship lost: another to choose, "
                                   "in the arena")
                    self.choose_next(lost=True)
        elif self.mode == ENTER:
            if self.blink:
                self.blink -= 1
            self.x += 2
            if self.x >= c["ENTER_TO"]:
                self.mode = CONTROL
        elif self.mode == LEAVE:                # STAGE CLEAR
            self.x += c["LEAVE_SPEED"]
            self.move_satellite()
            if self.x >= c["LEAVE_END"]:
                self.mode = GONE
                self.count("the ship gone, right")
        self.fly_shots(state)
        self.fly_missile(state)

    def body_name(self):
        """Whose body is rock in rows 10-14: the WARDEN's (level
        3), the CORVETTE's (level 4), the ARRAY's (level 5), the
        SUPER-COMPUTER's (level 6)."""
        return {4: "the CORVETTE's", 5: "the ARRAY's",
                6: "the SUPER-COMPUTER's"}.get(
            self.c["LEVEL_BOSS"], "the WARDEN's")

    def collide(self, state):
        points = self.touching(state)
        nose, top_f, top_r, bottom_f, bottom_r = points
        top, bottom = top_f or top_r, bottom_f or bottom_r
        if not (nose or top or bottom):
            return
        first = self.type * 5
        if any(points[k] and 10 <= (self.y + self.t["ship_spot_y"][
                first + k]) >> 3 <= 14 for k in range(5)):
            self.count(f"on {self.body_name()} body in the corridor "
                       "(rows 10-14)")
        c, first = self.c, self.type * 5         # on a beam
        for k in range(5):
            found = points[k] and self.point_cell(
                state, self.x + self.t["ship_spot_x"][first + k],
                self.y + self.t["ship_spot_y"][first + k])
            if found and c["BEAM_DOWN"] and found[0] in (c["BEAM_DOWN"],
                                                         c["BEAM_UP"]):
                self.count("on a beam: pushed")
                break
        speed = self.c["PUSH_SPEED"]
        if top and not bottom:
            self.push_dx, self.push_dy = 0, speed
            self.count("pushed down from the overhang")
        elif bottom and not top:
            self.push_dx, self.push_dy = 0, -speed
            self.count("pushed up from the floor")
        else:
            self.push_dx, self.push_dy = -speed, 0
            self.count("pushed back from a wall")
            if state.boss.arena:
                self.count("pushed back from a wall, in the arena")
        self.push = self.c["PUSH_FRAMES"]
        if self.blink:
            self.count("on the rock while blinking: no damage")
        elif not self.invuln:
            self.count("two notches lost")
        self.hurt(2, "the rock")

    def hurt(self, notches, what=""):
        """The ship hit (the rock, a Varkon or its plasma): notches off
        its shield unless it blinks or the key I has made it unhurtable;
        it blinks; none left, it explodes."""
        if self.blink:
            return
        if self.invuln:
            self.count(f"unhurtable (key I): {what}, no notch lost")
            return
        self.shield = max(0, self.shield - notches)
        self.blink = self.c["HIT_BLINK"]
        if self.shield == 0:
            self.mode, self.timer = EXPLODE, 0
            self.lives -= 1
            self.count("exploded")
            if self.weapon:
                self.weapon -= 1
                self.count("a weapon level lost")
            if self.sat:
                self.count("the satellite lost")
            self.sat = None
            self.sound("explode")
        else:
            self.sound("hurt")

    def fire(self):
        """The weapon's volley, if all its shots have free places;
        the wait, its sound; the satellite's bolt; the missile."""
        c, t = self.c, self.t
        w = self.windex()
        count, first = t["w_count"][w], t["w_first"][w]
        free = [i for i in range(SHOTS) if self.shots[i] is None]
        if len(free) < count:
            self.count("Fire: no room for the volley")
            if not free:
                self.count("Fire with four shots flying")
            return
        for e, i in zip(range(first, first + count), free):
            kind = t["v_kind"][e]
            x = self.x + c["SHOT_START"] + t["v_dx"][e]
            y = (self.y + signed8(t["v_dy"][e])) & 255
            self.shots[i] = Shot(t, x, y, kind)
            self.count(f"shot {kind} fired")
        self.count(f"weapon {self.type + 1}.{self.weapon + 1} fires")
        self.cooldown = t["w_period"][w]
        self.sound(EFFECTS[t["w_fx"][w]])
        if self.sat:
            for i in range(SHOTS):
                if self.shots[i] is None:
                    self.shots[i] = Shot(t, self.sat[0] + c["SAT_SHOT"],
                                         self.sat[1], c["SATBOLT"])
                    self.count("the satellite fires")
                    break
            else:
                self.count("the satellite: no place left")
        if self.missiles and self.missile is None:
            self.missile = Missile(self.x + c["MISSILE_DX"],
                                   (self.y + c["MISSILE_DY"]) & 255)
            self.count("missile away")
            self.sound("missile")

    def start_blast(self, shot, skip):
        """The shot bursts at its point: its blast armed (tried in the
        next update of the Varkon), its fireball from now."""
        t, c = self.t, self.c
        k = shot.kind
        hx = ((shot.x + t["shot_tip"][k]) >> 1) & 255
        hy = (shot.y + t["shot_mid"][k * 4 + shot.mask]) & 255
        b = t["shot_blast"][k] - 1
        rx, ry = t["blast_rx"][b], t["blast_ry"][b]
        self.blast = Blast((hx - rx) & 255, (hy - ry) & 255,
                           (hx + rx) & 255, (hy + ry) & 255,
                           t["blast_dmg"][b], skip)
        shot.bl = c["BLAST_FRAMES"] + 1
        shot.x += signed8(t["shot_bdx"][k])
        shot.y = (shot.y + signed8(t["shot_bdy"][k])) & 255
        self.count(f"blast {b + 1}")

    def fly_shots(self, state):
        """The shots fly on (past the edge, out of the playfield they
        end), a blast counts its frames; the rock: shots_rock."""
        t, c = self.t, self.c
        for i, shot in enumerate(self.shots):
            if shot is None:
                continue
            k = shot.kind
            if shot.bl:
                shot.bl -= 1
                if not shot.bl:
                    self.shots[i] = None
                    self.count("blast over")
                continue
            shot.x += t["shot_speed"][k]
            if shot.x > 320:
                self.shots[i] = None
                self.count(f"shot {k} past the edge")
                continue
            if shot.dy:
                shot.y = (shot.y + shot.dy) & 255
                if shot.y > c["VARKON_Y_MAX"]:
                    self.shots[i] = None
                    self.count(f"shot {k} out of the playfield")
                    self.count("a shot out of the playfield")

    def shots_rock(self, state):
        """After the sprites are written: a half on the rock ends, a
        Gauss shot bursts (its blast from the next frame)."""
        t = self.t
        for i, shot in enumerate(self.shots):
            if shot is None or shot.bl:
                continue
            k = shot.kind
            for half in (0, 1):
                if shot.mask >> half & 1:
                    at = k * 2 + half
                    if self.solid(state, shot.x + t["shot_point_x"][at],
                                  shot.y + t["shot_point_y"][at]):
                        if 10 <= (shot.y + t["shot_point_y"][at]) >> 3 \
                                <= 14:
                            self.count(f"a shot on {self.body_name()} "
                                       "body in the corridor (rows "
                                       "10-14)")
                        if half == 0 and t["shot_blast"][k]:
                            self.start_blast(shot, None)
                            self.count(f"shot {k} bursts on the rock")
                            break
                        shot.mask &= ~(1 << half)
                        self.count(f"shot {k} half {half} on "
                                   "the rock")
            if not shot.mask:
                self.shots[i] = None

    def move_satellite(self):
        """After the ship: SAT_BACK behind, SAT_ABOVE above (below
        when the ship is above SAT_LOW), SAT_STEP a frame at most;
        also from x < 0, after STAGE CLEAR."""
        if not self.sat:
            return
        c = self.c
        step = c["SAT_STEP"]
        tx = self.x - c["SAT_BACK"]
        ty = self.y - c["SAT_ABOVE"] if self.y >= c["SAT_LOW"] else \
            self.y + c["SAT_ABOVE"]
        x, y = self.sat
        for name, far in (("right", tx - x), ("left", x - tx),
                          ("down", ty - y), ("up", y - ty)):
            if far > step:
                self.count(f"the satellite catches up, {name}")
        x = tx if abs(tx - x) <= step else x + (step if tx > x
                                                 else -step)
        y = ty if abs(ty - y) <= step else y + (step if ty > y
                                                 else -step)
        self.sat = [x, y]

    def floor(self, state, x):
        """The floor's first line under the missile's toe (255: none):
        the level's column (camera + x + MISSILE_REACH) / 8."""
        t = self.t
        col = (state.camera + x + self.c["MISSILE_REACH"]) >> 3
        return t["floor_lo"][col] if col < 256 else \
            t["floor_hi"][col - 256]

    def on_body(self, state, x):
        """Is the missile's toe (x + MISSILE_REACH) in the boss's body
        shown (from its front, BODY_WIDTH pixels)? (Only in the SIEGE
        CRAWLER's arena.)"""
        c, boss = self.c, state.boss
        if not boss.state or c["LEVEL_BOSS"] != 1:
            return False
        d = (x + c["MISSILE_REACH"] - 2 * boss.shown_x) & 0xFFFF
        if d > 255:
            return False
        return c["BODY_WALL"] <= d < c["BODY_WALL"] + c["BODY_WIDTH"]

    def fly_missile(self, state):
        m, c = self.missile, self.c
        if m is None:
            return
        foot, step = c["MISSILE_FOOT"], c["MISSILE_STEP"]
        if m.on == FALL:
            m.x += 1
            m.y = (m.y + 2) & 255
            if m.y > c["VARKON_Y_MAX"]:
                self.missile = None
                self.count("missile under the playfield")
                return
            if m.x > c["MISSILE_X_END"]:
                self.missile = None
                self.count("missile past the edge")
                return
            if self.on_body(state, m.x):
                self.missile = None
                self.count("missile on the boss's body")
                return
            floor = self.floor(state, m.x)
            if floor != 255:
                land = floor - foot
                if land <= m.y:
                    if m.y - land > step:
                        self.missile = None
                        self.count("missile on a wall, falling")
                        return
                    m.y, m.on = land, RUN
                    self.count("missile lands")
        else:
            m.x += 3
            if m.x > c["MISSILE_X_END"]:
                self.missile = None
                self.count("missile past the edge")
                return
            if self.on_body(state, m.x):
                self.missile = None
                self.count("missile on the boss's body")
                return
            floor = self.floor(state, m.x)
            if floor == 255:
                m.on = FALL
                self.count("missile into a river")
            else:
                new = floor - foot
                if new + step < m.y:
                    self.missile = None
                    self.count("missile on a wall")
                    return
                if m.y + step < new:
                    m.on = FALL
                    self.count("missile off a drop")
                else:
                    if new != m.y:
                        self.count("missile follows the floor")
                    m.y = new

    def missile_point(self):
        """Its nose for the hits (x register / 2, y register), or
        None."""
        m, t = self.missile, self.t
        if m is None:
            return None
        return (((m.x + t["m_nose_x"][m.on - 1]) >> 1) & 255,
                (m.y + t["m_nose_y"][m.on - 1]) & 255)

    def take_capsule(self, letter):
        """A capsule: W a level, S speed, M the missile, O the
        satellite, E the shield; past its most, the bonus (True)."""
        c, t = self.c, self.t
        self.sound("capsule")
        self.count(f"capsule {letter} taken")
        if letter == "W" and self.weapon < c["LEVELS"] - 1:
            self.weapon += 1
        elif letter == "S" and self.s_caps < c["SPEED_STEPS"]:
            self.s_caps += 1
        elif letter == "M" and not self.missiles:
            self.missiles = 1
        elif letter == "O" and not self.sat:
            self.sat = [self.x, self.y]
        elif letter == "E" and \
                self.shield < t["ship_shield"][self.type]:
            self.shield = t["ship_shield"][self.type]
            self.count("the shield full again")
        else:
            self.count(f"capsule {letter} past its most: the bonus")
            return True
        return False

    # --- what the VIC-II shows next ----------------------------------

    def sprites(self):
        """Sprites 0 and 1: (on, x register, y register, block,
        colour); the ship's accent and its colour layer, or the
        explosion's sparks and fireball."""
        c, t = self.c, self.t
        out = [(False, 0, 0, 0, 0)] * 2
        x, y = (self.x + 24) & 0x1FF, self.y + 50
        base = c["SPRITE_BLOCK"] + self.type * 6 + self.figure * 2
        shown = not (self.blink & 4)
        if self.mode in (CONTROL, ENTER, LEAVE, CHOOSE) and shown:
            out[0] = (True, x, y, base, t["ship_accent"][self.type])
            out[1] = (True, x, y, base + 1, t["ship_own"][self.type])
        elif self.mode == EXPLODE:              # sparks, fireball
            block = t["explosion_block"][self.timer]
            out[0] = (True, x, y, block,
                      t["explosion_spark"][self.timer])
            out[1] = (True, x, y, block + 1,
                      t["explosion_own"][self.timer])
        return out

    def shot_objects(self):
        """The four shots as objects of the multiplexer: (y register
        or 0, x register, block, colour, multicolour 1); a blast's
        fireball."""
        t = self.t
        out = []
        for shot in self.shots:
            if shot is None:
                out.append((0, 0, 0, 0, 0))
                continue
            k = shot.kind
            if shot.bl:
                block = t["blast_block"][shot.bl]
                colour = t["blast_own"][shot.bl]
            else:
                block = t["shot_block"][k]
                if t["shot_halves"][k] == 3:
                    block += {3: 0, 1: 1, 2: 2}[shot.mask]
                colour = t["shot_colour"][k]
            out.append(((shot.y + 50) & 255, (shot.x + 24) & 0x1FF,
                        block, colour, 1))
        return out

    def more_objects(self):
        """Objects 22 and 23: the satellite (its two pictures by
        anim), the missile (running, falling)."""
        c = self.c
        out = [(0, 0, 0, 0, 0)] * 2
        if self.sat:
            out[0] = (self.sat[1] + 50, (self.sat[0] + 24) & 0x1FF,
                      c["SATELLITE_BLOCK"] + (self.anim() >> 3 & 1),
                      c["SATELLITE_OWN"], 1)
        m = self.missile
        if m:
            out[1] = ((m.y + 50) & 255, (m.x + 24) & 0x1FF,
                      c["MISSILE_BLOCK"] + 2 - m.on,
                      c["MISSILE_OWN"], 1)
        return out

    def hud(self, screen):
        """The shield's notches, the ships left and the weapon's pips,
        in the HUD."""
        c = self.c
        top = self.t["ship_shield"][self.type]
        for i in range(6):
            code = (c["SHIELD_FULL_CODE"] if i < self.shield else
                    c["SHIELD_EMPTY_CODE"] if i < top else 0)
            screen[880 + c["HUD_SHIELD"] + i] = code
        for i in range(c["LIVES_MAX"]):
            screen[880 + c["HUD_SHIPS"] + i] = \
                c["SHIP_ICON_CODE"] if i < self.lives else 0
        for i in range(c["LEVELS"]):
            screen[880 + c["HUD_WEAPON"] + i] = \
                c["PIP_FULL_CODE"] if i <= self.weapon else \
                c["PIP_EMPTY_CODE"]
