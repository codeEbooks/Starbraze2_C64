"""The model of the Varkon, the hits and the score.

Written again from the rules (game/src/varkon.asm, hits.asm, score.asm
and their comments), without the program: the test compares the two
frame by frame.

The Varkon move at the end of the turn, for the next frame, when the
camera of the next turn has been planned (State.plan_next):
  - cam_step: the camera's move to that frame (256ths, 24 bits);
  - the targets: the ship's shots as points (the tip of the bolt, the
    middle of what is left of it), the ship's boxes if it flies and
    does not blink, the lines a Varkon must be on to meet them;
  - the plasma shots: by their velocity; past an edge or out of the
    playfield gone; one shown whose middle is in the ship's box ends
    and the ship loses a notch;
  - the Varkon, one after the other: a wave's member waits its turn;
    a flyer follows its path; a leaper or a turret moves with the rock
    (x back by cam_step), the leaper hops (gravity, each hop landing
    where the floor is); one shown and near the targets meets the
    shots (each a point in its box: the shot ends, its damage; no
    hits left, it explodes and its points go to the score; a laser
    flies on, hurting each Varkon once, a Gauss shot bursts),
    the missile (a point: it ends, its damage), the blast armed in
    the frame before (a box: its damage, but not to the Varkon its
    shot met) and the ship (boxes overlapping: it explodes, the ship
    loses a notch); then its picture (a turret's by its aim to the
    ship), its colour (white just after a hit), and it fires at its
    period; an exploding one shows the fireball, frame by frame, then
    is gone, or (a carrier) becomes its capsule: on its place of the
    rock, until the ship (flying, blinking too) takes it or it goes
    past the left edge;
  - the waves whose column the camera (this frame's) has reached.
Objects 4-21 of the next frame's bank come out as they go.

Level 2's towers: a core (behaviour STAND) on the rock, by the frame's
picture, firing; when it explodes, the pieces of a field within
FIELD_REACH pixels of it explode too (fields_down, no points). A field's
piece (FIELD) is not hit (the shots, the missile, the blast go through
it): its two pictures by the frame; the ship, flying, its box on the
piece's, is pushed back as by a wall and loses two notches
(field_touch). The core and the field come in with the multiplexer's
highest priority (BOSS_PRI), another Varkon on a place that had it with
its class (wave_pri). A core, like a boss's part, does not explode on
the ship.

Each Varkon fires at its own period (en_period, its kind's when it
comes: the SHIELD CORE's core takes a shorter one in RAGE). A shield's
segment stops every shot that meets it, a laser too (a Gauss shot bursts
on it), takes the shot's damage and can be destroyed (the author:
«bisogna rendere mortali gli scudi»).

Level 3's: a kind's pictures by the frame are four or two (kind_pmask);
the gunship (and its gold carrier) fires a fan of three shots (kind_fan:
its first fire entry; fire_fan); the mine (behaviour MINE) stands in
space as a turret on the rock: shown, the ship flying (blinking too)
within MINE_REACH_X of its x register and MINE_REACH_Y of its line, it
bursts (mine_near): MINE_FAN_COUNT shots of its shrapnel, it explodes
without points; a rock destroyed by a shot, the missile or the blast
(not on the ship) splits: two shards in the first free Varkon, from its
place (SHARD_DY lines lower the second), on their paths up and down
(split).
"""

import parts                           # (D.2) the steps of the chain

ENEMIES, ESHOTS = 12, 6
FREE, FLYING, BOOM, CAPSULE = 0, 1, 2, 3
LETTERS = "WSMOE"
PATH, HOP, TURRET, BOSS, STAND, FIELD, MINE = 0, 1, 2, 3, 4, 5, 6
CRAWL, LMINE, HANG = 7, 8, 9           # the station's module
GUARD, EGG, BAR = 10, 11, 12           # level 6's, there too
FALL = 13                              # the escape's (its code)
LOOKS = ("off", "dimmed", "on")        # the barriers' pieces
BOSS_PRI = 8                           # (boss.asm)
FIRST_ENEMY = 4                        # the Varkon's first object
NONE = (0, 0, 0, 0, 0)


def signed8(v):
    return v - 256 if v & 0x80 else v


def signed16(v):
    return v - 65536 if v & 0x8000 else v


class Score:
    """Six digits; a ship more every 20 000 (up to LIVES_MAX); the
    best so far."""

    EVERY = 2                   # ten thousands (score.asm: EXTRA_EVERY)

    def __init__(self, c):
        self.c = c
        self.best = 0
        self.reset()

    def reset(self):
        self.value = 0
        self.next_life = self.EVERY     # ten thousands

    def add(self, points, ship):
        if self.value + points > 999990:
            ship.count("the score at its most")
        self.value = min(self.value + points, 999990)
        if self.value // 10000 >= self.next_life:
            self.next_life = self.next_life + self.EVERY if \
                self.next_life + self.EVERY <= 99 else 999
            if ship.lives < self.c["LIVES_MAX"]:
                ship.lives += 1
                ship.count("a ship more")
        self.best = max(self.best, self.value)

    def hud(self, screen):
        c = self.c
        for value, cell in ((self.value, c["SCORE_CELL"]),
                            (self.best, c["HI_CELL"])):
            for i, digit in enumerate(f"{value:06d}"):
                screen[cell + i] = c["DIGIT_CODE"] + int(digit)


class Varkon:
    def __init__(self, files):
        self.c = files["constants"]
        self.t = files["tables"]
        self.stats = {}
        self.sound = lambda effect: None   # sfx_start (player_model)
        self.score = Score(self.c)
        self.boss = None                   # boss_model.Boss
        self.reset()

    def reset(self):
        n = ENEMIES
        self.on = [FREE] * n
        self.kind = [0] * n
        self.delay = [0] * n
        self.seg = [0] * n
        self.left = [0] * n
        self.vx = [0] * n                # signed, 256ths
        self.vy = [0] * n                # 16 bits, as kept
        self.x = [0] * n                 # x register, 256ths, signed
        self.y = [0] * n                 # 16 bits: lines, 256ths
        self.fire = [0] * n
        self.period = [0] * n            # en_period
        self.life = [0] * n
        self.flash = [0] * n
        self.own = [None] * n            # a colour of its own
                                         # (the ARRAY's lens: en_colour)
        self.aim = [0] * n
        self.cap = [0] * n               # 1 + its letter, 0 none
        self.s_on = [0] * ESHOTS
        self.s_x = [0] * ESHOTS          # 256ths (whole pixels)
        self.s_y = [0] * ESHOTS
        self.s_vx = [0] * ESHOTS         # 256ths (whole pixels)
        self.s_vy = [0] * ESHOTS         # 16 bits
        self.wave = 0
        self.anim = 0
        self.objs = [NONE] * (ENEMIES + ESHOTS)

    def count(self, what):
        self.stats[what] = self.stats.get(what, 0) + 1
        if what.startswith("Varkon ") and \
                self.c.get("LEVEL_PHASE") == 3:      # the
            what += ", phase 3"                      # station's kinds,
            if self.c.get("LEVEL_TABLES") == 4:      # in phase 2's
                what = what[:-len("phase 3")] + "set 4"   # slots;
            self.stats[what] = self.stats.get(what, 0) + 1
                                                     # level 6's set

    def beh(self, i):
        return self.t["kind_beh"][self.kind[i]]

    def load(self, i):
        t, s = self.t, self.seg[i]
        self.left[i] = t["seg_frames"][s]
        self.vx[i] = signed16(t["seg_vxl"][s] | t["seg_vxh"][s] << 8)
        self.vy[i] = t["seg_vyl"][s] | t["seg_vyh"][s] << 8

    # --- a frame ----------------------------------------------------

    def update(self, state):
        """One frame, at the end of the turn: the camera's move, the
        targets, the shots, the Varkon, the waves; self.objs, the
        objects 4-21 of the next frame."""
        self.anim = (self.anim + 1) & 255
        self.anim3 = (self.anim >> 3) & 3
        nxt, nfrac = state.next_camera
        self.next = nxt
        self.next_frac = nfrac
        self.cam_step = ((nxt << 8 | nfrac) -
                         (state.camera << 8 | state.frac))
        self.ship = state.ship
        self.mux = state.mux             # wave_pri
        self.speed = state.speed(0)      # the guardian's
        self.blast = self.ship.blast     # armed: tried now
        self.ship.blast = None
        if parts.has("hits"):              # (D.2: step 4, none)
            self.prepare()
        else:
            self.hit, self.mp, self.blast = [None] * 4, None, None
            self.sb = self.box = None
            self.near = (0, 0)
        self.objs = [NONE] * (ENEMIES + ESHOTS)
        self.move_plasma()
        if self.boss and parts.has("boss"):    # the boss, its parts
            self.boss.update(self, state)
        state.beam_step()                  # level 2's beams
        for i in range(ENEMIES):
            self.move(i)
        while True:
            w = self.wave
            col = self.t["wave_col_lo"][w] | self.t["wave_col_hi"][w] << 8
            if state.camera >> 3 < col:
                break
            self.spawn(w)
            self.wave += 1

    def prepare(self):
        """The targets: the shots' points, the ship's boxes, the lines
        to try."""
        t, ship = self.t, self.ship
        self.hit = [None] * 4
        top, bottom = 255, 0
        for k, shot in enumerate(ship.shots):
            if shot is None or shot.bl:
                continue
            kind = shot.kind
            hx = ((shot.x + t["shot_tip"][kind]) >> 1) & 255
            hy = (shot.y + t["shot_mid"][kind * 4 + shot.mask]) & 255
            self.hit[k] = (hx, hy)
            top, bottom = min(top, hy), max(bottom, hy)
        self.mp = ship.missile_point()
        if self.mp:
            top, bottom = min(top, self.mp[1]), max(bottom, self.mp[1])
        if self.blast:
            low = (self.blast.bottom - 1) & 255
            top = min(top, self.blast.top, low)
            bottom = max(bottom, self.blast.top, low)
        self.hs = (top, bottom)
        self.sb = self.box = None
        if ship.mode == 0:
            s = ship.type
            xr2 = ((ship.x + 24) & 0x1FF) >> 1
            yr = ship.y + 50
            left = (xr2 + t["ship_box_x"][s]) & 255
            top_ = (yr + t["ship_box_y"][s]) & 255
            self.box = (left, (left + t["ship_box_w"][s]) & 255,
                        top_, (top_ + t["ship_box_h"][s]) & 255)
            self.pb = ((xr2 + t["ship_pbox_x"][s]) & 255,
                       (yr + t["ship_pbox_y"][s]) & 255,
                       t["ship_pbox_w"][s], t["ship_pbox_h"][s])
            if not ship.blink:
                self.sb = self.box
        if self.sb:
            top = min(top, self.sb[2])
            bottom = max(bottom, self.sb[3] - 1)
        if top == 255:
            self.near = (0, 0)
        else:
            self.near = ((top - 20) & 255,
                         (bottom - ((top - 20) & 255) + 1) & 255)

    def is_near(self, yreg):
        top, span = self.near
        return (yreg - top) & 255 < span

    # --- the plasma -------------------------------------------------

    def place_shot(self, j):
        """Shot j's object, if its x register is 1-343; False if it
        is gone."""
        x = self.s_x[j] >> 8
        if x <= 0 or x >= 344:
            return False
        self.objs[ENEMIES + j] = (
            (self.s_y[j] >> 8) + 50, x & 0x1FF,
            self.c["PLASMA_BLOCK"] + ((self.anim >> 2) & 3),
            self.c["PLASMA_COLOUR"], 1)
        return True

    def move_plasma(self):
        for j in range(ESHOTS):
            if not self.s_on[j]:
                continue
            self.s_x[j] += self.s_vx[j]
            if self.s_vy[j]:
                self.s_y[j] = (self.s_y[j] + self.s_vy[j]) & 0xFFFF
                if self.s_y[j] >> 8 > self.c["VARKON_Y_MAX"]:
                    self.s_on[j] = 0
                    self.count("plasma gone")
                    continue
            if not self.place_shot(j):
                self.s_on[j] = 0
                self.count("plasma gone")
                continue
            if self.sb:
                self.plasma_hit(j)

    def plasma_hit(self, j):
        yreg, xreg = self.objs[ENEMIES + j][0], self.objs[ENEMIES + j][1]
        left, top, w, h = self.pb
        if (yreg - top) & 255 < h and ((xreg >> 1) - left) & 255 < w:
            self.s_on[j] = 0
            self.objs[ENEMIES + j] = NONE
            self.sb = None
            self.count("plasma on the ship")
            self.ship.hurt(1, "plasma")

    # --- the Varkon -------------------------------------------------

    def place(self, i):
        """'gone' (x register 0 or less), 'hidden' (344 or more) or
        its y register."""
        x = self.x[i] >> 8
        if x <= 0:
            return "gone"
        if x >= 344:
            return "hidden"
        return (self.y[i] >> 8) + 50

    def move(self, i):
        t, c = self.t, self.c
        if self.on[i] == FREE:
            return
        beh = self.beh(i)
        if self.on[i] == CAPSULE:
            self.capsule(i)
            return
        if self.on[i] == BOOM:
            if beh != PATH:
                self.x[i] -= self.cam_step
            self.left[i] += 1
            if self.left[i] == c["EXPLOSION_FRAMES"]:
                self.count("explosion over")
                if self.cap[i]:
                    self.on[i] = CAPSULE
                    self.count(f"capsule {LETTERS[self.cap[i] - 1]} "
                               "left")
                    self.capsule(i)
                    return
                self.on[i] = FREE
                return
            where = self.place(i)
            if where == "gone":
                self.on[i] = FREE
            elif where != "hidden":
                self.show_boom(i, where)
            return
        if self.delay[i]:
            self.delay[i] -= 1
            return
        self.x[i] += self.vx[i]
        if beh != PATH:
            self.x[i] -= self.cam_step
            if beh == HOP:
                self.leap(i)
        else:
            self.y[i] = (self.y[i] + self.vy[i]) & 0xFFFF
            self.left[i] -= 1
            if self.left[i] == 0:
                self.seg[i] += 1
                self.load(i)
                if self.left[i] == 0:
                    self.on[i] = FREE
                    self.count("Varkon at the path's end")
                    return
        where = self.place(i)
        if where == "gone":
            self.on[i] = FREE
            self.count("Varkon gone left")
            return
        if where == "hidden":
            return
        yreg = where
        if self.is_near(yreg) and beh != FIELD:   # a field:
            self.meet(i, yreg)                  # the shots go through
            if self.on[i] == BOOM:
                self.show_boom(i, yreg)
                return
        if beh == MINE and self.mine_near(i):   # it bursts
            self.show_boom(i, yreg)
            return
        k = self.kind[i]
        if beh == TURRET:
            self.aim_at(i)
            block = t["kind_block"][k] + self.aim[i]
        elif beh == BOSS:                  # a boss's part
            block = self.boss.part_block(i)
        elif beh == FIELD:                 # two pictures
            block = t["kind_block"][k] + (self.anim3 & 1)
            self.field_touch(i, yreg)
        elif beh == HANG:                  # by its aim
            self.aim_at(i)
            block = t["kind_block"][k] + self.aim[i]
        else:                              # four or two
            block = t["kind_block"][k] + (self.anim3 & t["kind_pmask"][k])
        # The station's: its place shown first (a crawler's step shows the
        # frame after); before the colour and the period: the guardian's
        # shell and the barrier have no flash, an egg hatched has the
        # drone's colour and period
        xreg = (self.x[i] >> 8) & 0x1FF
        if beh >= CRAWL:                   # (a barrier's piece
            block, yreg = self.p3_part(i, beh, yreg, block)   # its
            k = self.kind[i]               # line, or not shown)
        if self.flash[i]:
            self.flash[i] -= 1
            colour = 1
        elif self.own[i] is not None:      # set by the boss
            colour = self.own[i]
        else:
            colour = t["kind_colour"][k]
        self.objs[i] = (yreg, xreg, block, colour, 1) if yreg else NONE
        period = self.period[i]            # its own: the
        if period:                         # SHIELD CORE's bursts
            self.fire[i] = (self.fire[i] - 1) & 255
            if self.fire[i] == 0:
                self.fire[i] = period
                self.shoot(i)

    def capsule(self, i):
        """A capsule: on its place of the rock; the ship takes it."""
        c, t = self.c, self.t
        self.x[i] -= self.cam_step
        where = self.place(i)
        if where == "gone":
            self.on[i] = FREE
            self.count("capsule gone left")
            return
        if where == "hidden":
            return
        yreg, xreg = where, (self.x[i] >> 8) & 0x1FF
        if self.box and self.ship.mode == 0:
            left, right, s_top, s_bottom = self.box
            top = (yreg + c["CAP_BOX_Y"]) & 255
            x0 = ((xreg >> 1) + c["CAP_BOX_X"]) & 255
            if top < s_bottom and top + c["CAP_BOX_H"] > s_top and \
                    x0 < right and x0 + c["CAP_BOX_W"] > left:
                self.on[i] = FREE
                if self.ship.blink:
                    self.ship.count("capsule taken while blinking")
                letter = LETTERS[self.cap[i] - 1]
                if self.ship.take_capsule(letter):
                    if self.score.value < 999990:
                        self.ship.count(f"capsule {letter} past its "
                                        "most: 500 points")
                    k = c["KIND_BONUS"]
                    self.score.add(int(f"{t['kind_pts_hi'][k]:02x}"
                                       f"{t['kind_pts_lo'][k]:02x}"),
                                   self.ship)
                return
        self.objs[i] = (yreg, xreg,
                        c["CAPSULE_BLOCK"] + self.cap[i] - 1,
                        t["capsule_colour"][(self.anim >> 2) & 3], 1)

    def show_boom(self, i, yreg):
        t = self.t
        f = self.left[i]
        self.objs[i] = (yreg, (self.x[i] >> 8) & 0x1FF,
                        t["explosion_block"][f] + 1,
                        t["explosion_own"][f], 1)

    def leap(self, i):
        c, t = self.c, self.t
        if self.left[i] == 0:
            xr = (self.x[i] >> 8) & 0xFFFF
            back = 24 - c["LEAP_FOOT"] + c["HOP_FRAMES"] // 2
            col = ((xr + self.next - back) & 0xFFFF) >> 3
            floor = t["floor_lo"][col] if col < 256 else \
                t["floor_hi"][col - 256]
            if floor == 255:
                d = 0
            else:
                d = signed8((floor - (c["LEAP_FEET"] + 1)
                             - (self.y[i] >> 8)) & 255)
            self.vy[i] = (8 * d - c["HOP_UP"]) & 0xFFFF
            self.left[i] = c["HOP_FRAMES"]
            self.count("leaper hops")
        self.left[i] -= 1
        self.y[i] = (self.y[i] + self.vy[i]) & 0xFFFF
        self.vy[i] = (self.vy[i] + c["HOP_G"]) & 0xFFFF

    def aim_at(self, i):
        ship = self.ship
        dx = (ship.x + 24) - (self.x[i] >> 8)
        side = self.c["AIM_SIDE"]
        self.aim[i] = 0 if dx < -side else 2 if dx > side else 1

    def meet(self, i, yreg):
        """Varkon i, shown, near the targets: the shots, the ship."""
        t, k = self.t, self.kind[i]
        e_top = (yreg + t["kind_box_y"][k]) & 255
        e_h, e_w = t["kind_box_h"][k], t["kind_box_w"][k]
        e_left = (((self.x[i] >> 8) & 0x1FF) >> 1) + t["kind_box_x"][k]
        e_left &= 255
        top, bottom = self.hs
        if not (bottom < e_top or e_top + e_h <= top):
            for s in range(4):
                if self.hit[s] is None:
                    continue
                hx, hy = self.hit[s]
                if (hy - e_top) & 255 < e_h and (hx - e_left) & 255 < e_w:
                    self.shot_hit(i, s)
                    if self.on[i] == BOOM:
                        return
            if self.mp:
                hx, hy = self.mp
                if (hy - e_top) & 255 < e_h and (hx - e_left) & 255 < e_w:
                    self.ship.missile = None
                    self.mp = None
                    self.count("missile on a Varkon")
                    self.damage(i, self.c["MISSILE_DAMAGE"])
                    if self.on[i] == BOOM:
                        self.count("missile on a Varkon: destroyed")
                        return
            b = self.blast
            if b and i != b.skip and e_top < b.bottom and \
                    e_top + e_h > b.top and e_left < b.right and \
                    e_left + e_w > b.left:
                self.count("blast on a Varkon")
                self.damage(i, b.damage)
                if self.on[i] == BOOM:
                    return
        if self.sb:
            left, right, s_top, s_bottom = self.sb
            if e_top < s_bottom and e_top + e_h > s_top and \
                    e_left < right and e_left + e_w > left:
                self.sb = None
                self.count(f"Varkon {k} on the ship")
                if self.beh(i) < BOSS:         # a part stays,
                    self.destroy(i)            # a core too
                self.ship.hurt(1, "a Varkon")

    def shot_hit(self, i, s):
        """Shot s on Varkon i: a laser flies on (once a Varkon), a
        Gauss shot bursts, the others end; the kind's damage."""
        t, ship = self.t, self.ship
        shot = ship.shots[s]
        kind = shot.kind
        segment = self.kind[i] == self.c["KIND_SEGMENT"]
        if segment:                        # a shield's segment:
            self.count("a shot on a shield's segment")   # it stops
            if t["shot_pierce"][kind]:
                self.count("a laser stops on a shield's segment")
            elif t["shot_blast"][kind]:
                self.count("a Gauss shot bursts on a shield's segment")
        if t["shot_pierce"][kind] and not segment:       # even a laser
            if i in shot.pierced:
                self.count("laser: a Varkon pierced already")
                return
            shot.pierced.add(i)
            self.count("laser through a Varkon")
        elif t["shot_blast"][kind]:
            ship.start_blast(shot, i)
            self.hit[s] = None
            self.count("a shot bursts on a Varkon")
        else:
            ship.shots[s] = None
            self.hit[s] = None
        self.count(f"shot {kind} on a Varkon")
        self.damage(i, t["shot_damage"][kind])

    def damage(self, i, hits):
        life = self.life[i] - hits
        self.life[i] = life & 255
        if life <= 0:
            self.count(f"Varkon {self.kind[i]} shot down")
            self.destroy(i)
            if self.kind[i] == self.c["KIND_ROCK"]:
                self.split(i)
        else:
            self.flash[i] = self.c["FLASH_FRAMES"]
            self.count(f"Varkon {self.kind[i]} hit")

    def destroy(self, i):
        t, k = self.t, self.kind[i]
        self.on[i] = BOOM
        self.left[i] = 0
        self.flash[i] = 0
        points = int(f"{t['kind_pts_hi'][k]:02x}{t['kind_pts_lo'][k]:02x}")
        self.score.add(points, self.ship)
        if t["kind_beh"][k] == STAND:      # its field with it
            self.fields_down(i)
        self.sound("boom")

    def shoot(self, i):
        t = self.t
        k = self.kind[i]
        if t["kind_fan"][k]:                # a gunship's fan
            self.count(f"Varkon {k} fires its fan")
            for e in range(3):
                self.shoot_entry(i, t["kind_fan"][k] + e)
            return
        entry = k
        if self.beh(i) == TURRET:
            entry = t["aim_entry"][self.aim[i]]
        self.shoot_entry(i, entry)

    def shoot_entry(self, i, entry):
        """Varkon i fires from the fire entry (fire_entry; a cannon's
        fan gives it)."""
        t, c = self.t, self.c
        for j in range(ESHOTS):
            if not self.s_on[j]:
                break
        else:
            self.count("Varkon shot: no free place")
            return
        self.sound("plasma")
        k = self.kind[i]
        if self.beh(i) == TURRET:
            self.count(f"turret fires {('left', 'up', 'right')[self.aim[i]]}")
        xr = self.x[i] >> 8
        self.s_on[j] = 1
        self.s_x[j] = (xr + signed8(t["fire_dx"][entry])) << 8
        y = ((self.y[i] >> 8) + t["fire_dy"][entry]) & 255
        self.s_y[j] = y << 8 | (self.y[i] & 255)
        self.s_vx[j] = signed8(t["fire_vx"][entry]) << 8
        vy = t["fire_vyl"][entry] | t["fire_vyh"][entry] << 8
        if t["fire_aim"][entry]:
            if y + c["AIM_DEAD"] < self.ship.y:
                vy = c["AIM_VY"]
            elif self.ship.y + c["AIM_DEAD"] < y:
                vy = -c["AIM_VY"] & 0xFFFF
        self.s_vy[j] = vy
        self.count(f"Varkon {k} fires")
        if not self.place_shot(j):
            self.s_on[j] = 0
            self.objs[ENEMIES + j] = NONE

    def spawn(self, w):
        t, c = self.t, self.c
        count = t["wave_count"][w]
        delay = fire = 0
        y = t["wave_y"][w]
        for k in range(count):
            for i in range(ENEMIES):
                if self.on[i] == FREE:
                    break
            else:
                self.count("wave: no free Varkon")
                i = None
            if i is not None:
                kind = t["wave_kind"][w]
                self.on[i] = FLYING
                self.kind[i] = kind
                self.own[i] = None
                self.cap[i] = t["wave_cap"][w] if \
                    parts.has("weapons") else 0    # (D.2: from step 6)
                self.seg[i] = t["wave_path"][w]
                self.delay[i] = delay
                self.flash[i] = 0
                self.life[i] = t["kind_life"][kind]
                period = t["kind_period"][kind]
                self.period[i] = period
                self.fire[i] = ((period >> 1) + fire) & 255 if period \
                    else 0
                self.load(i)
                self.wave_pri(i)
                wx = t["wave_x_lo"][w] | t["wave_x_hi"][w] << 8
                self.y[i] = y << 8
                beh = t["kind_beh"][kind]
                if beh == PATH:            # 16 bits (from x -20)
                    self.x[i] = signed16((wx + 24) & 0xFFFF) << 8
                else:
                    xr = signed16((wx + 24 - self.next) & 0xFFFF)
                    self.x[i] = xr << 8 | (255 - self.next_frac)
                    self.left[i] = 0
                    self.vx[i] = c["LEAP_VX"] if beh == HOP else 0
                self.count(f"Varkon {kind} in")
            delay = (delay + t["wave_spacing"][w]) & 255
            y = (y + t["wave_dy"][w]) & 255
            fire = (fire + 7) & 255

    # --- the station's (station.asm) -----------------------------------

    def p3_part(self, i, beh, yreg, block):
        """A Varkon of phase 3, shown (its place in its object): the
        crawler runs on along its floor (CRAWL_VX against the rock); the
        laser mine, rested, the ship flying on its line and ahead of it,
        fires its ray (its kind's fan); the hanging turret fires by its
        aim at its own period. Level 6's guardian, egg and barrier's
        piece (guard, egg, bar); the escape's falling piece (its own
        code, escape.asm: escape_part): down FALL_VY a frame, at
        FALL_END it breaks (a fireball, no points). Its picture and its
        object's y register (None: not shown)."""
        c, t, k = self.c, self.t, self.kind[i]
        if beh == CRAWL:
            self.x[i] += signed16(c["CRAWL_VX"])
            return block, yreg
        if beh == LMINE:
            if self.fire[i]:
                self.fire[i] -= 1
                return block, yreg
            ship = self.ship
            if ship.mode != 0:
                return block, yreg
            line = (self.y[i] >> 8) & 255
            if abs(ship.y - line) > c["LMINE_BAND"]:
                return block, yreg
            mine = signed16((self.x[i] >> 8) & 0xFFFF)
            if (ship.x + 24) >= mine:
                return block, yreg
            self.fire[i] = c["LMINE_REST"]
            self.count("a laser mine fires its ray")
            self.shoot(i)
            return block, yreg
        if beh == GUARD:
            return self.guard(i), yreg
        if beh == EGG:
            self.egg(i)
            return block, yreg
        if beh == FALL:                    # its y on (the
            self.y[i] = (self.y[i] + c["FALL_VY"]) & 0xFFFF   # place
            if self.y[i] >> 8 >= c["FALL_END"]:    # shown is the one
                self.on[i] = BOOM                  # before)
                self.left[i] = self.flash[i] = self.cap[i] = 0
                self.count("a falling piece breaks on the floor")
            return block, yreg
        if beh == BAR:
            return self.bar(i)
        # HANG
        if self.fire[i] == 0:
            self.fire[i] = c["HANG_FIRST"]
        self.fire[i] -= 1
        if self.fire[i]:
            return block, yreg
        self.fire[i] = c["HANG_PERIOD"]
        self.count(f"a hanging turret fires "
                   f"{('down-left', 'down', 'down-right')[self.aim[i]]}")
        self.shoot_entry(i, t["kind_fan"][k] + self.aim[i])
        return block, yreg

    # --- level 6's (station.asm) ---------------------------------------

    def guard(self, i):
        """The core's guardian: its state (en_vyl: 0 new, 1 coming in,
        2 shut, 3 open, 4 leaving; a Varkon on the rock does not use
        its y velocity) and its frames (en_vyh) in vy, its life aside
        in aim, its openings left in seg. Shut, its life is its shell
        (GUARD_SHELL, no flash); open, its own, its fan as it opens.
        Its picture: shut the kind's first, open the next."""
        c = self.c
        block = self.t["kind_block"][self.kind[i]]
        state, timer = self.vy[i] & 255, self.vy[i] >> 8
        if state == 0:
            self.aim[i] = self.life[i]
            self.seg[i] = c["GUARD_TIMES"]
            state = 1
        if state == 3:
            self.stand(i)
            timer = (timer - 1) & 255
            if timer:
                self.vy[i] = state | timer << 8
                return block + 1
            self.aim[i] = self.life[i]     # it shuts: its life aside
            self.life[i] = c["GUARD_SHELL"]
            timer = c["GUARD_SHUT"]
            self.seg[i] = (self.seg[i] - 1) & 255
            state = 2 if self.seg[i] else 4
            self.count("the guardian shuts" if state == 2 else
                       "the guardian shuts and leaves")
            self.vy[i] = state | timer << 8
            return block
        self.life[i] = c["GUARD_SHELL"]    # shut: its shell
        self.flash[i] = 0
        if state == 2:
            self.stand(i)
            timer = (timer - 1) & 255
            if timer:
                self.vy[i] = state | timer << 8
                return block
            state, timer = 3, c["GUARD_OPEN"]   # it opens: its life,
            self.life[i] = self.aim[i]          # its fan
            self.vy[i] = state | timer << 8
            self.count("the guardian opens: its fan")
            self.shoot(i)
            return block + 1
        if state == 1:                     # coming in
            self.drift(i, c["GUARD_IN_VX"])
            x = self.x[i] >> 8
            if (x >> 8) & 255 == 0 and x & 255 <= c["GUARD_STOP_X"]:
                state, timer = 2, c["GUARD_SHUT"]
                self.count("the guardian stops, shut")
            self.vy[i] = state | timer << 8
            return block
        self.drift(i, c["GUARD_OUT_VX"])   # leaving
        self.vy[i] = state | timer << 8
        return block

    def stand(self, i):
        """The guardian still on the screen; its line a line nearer the
        ship's every other frame, within GUARD_TOP-GUARD_LOW."""
        c = self.c
        self.drift(i, 0)
        if self.anim & 1:
            return
        y = (self.y[i] >> 8) & 255
        ship = self.ship.y
        if y == ship:
            return
        if y > ship:
            if y < c["GUARD_TOP"] + 1:
                return
            y -= 1
        else:
            if y >= c["GUARD_LOW"]:
                return
            y += 1
        self.y[i] = y << 8 | (self.y[i] & 255)

    def drift(self, i, v):
        """Its x velocity against the rock: the camera's speed less v
        (256ths a frame to the left on the screen)."""
        self.vx[i] = self.speed - v

    def egg(self, i):
        """The egg: the ship flying, its x register less than EGG_NEAR
        pixels to the left of the egg's (or to its right): it hatches,
        a drone (new_part) in its place, on its path out of it: up from
        the floor (line 88 or lower), down from the ceiling."""
        c, t = self.c, self.t
        ship = self.ship
        if ship.mode != 0:
            return
        near = signed16((ship.x + 24 + c["EGG_NEAR"]) & 0xFFFF)
        if near < signed16((self.x[i] >> 8) & 0xFFFF):
            return
        line = (self.y[i] >> 8) & 255
        path = c["PATH_EMERGE_UP"] if line >= 88 else \
            c["PATH_EMERGE_DOWN"]
        kind = c["KIND_DRONE"]
        self.mux.set_pri(FIRST_ENEMY + i, 2)
        self.kind[i] = kind
        self.own[i] = None
        self.delay[i] = self.flash[i] = self.cap[i] = 0
        self.vx[i] = self.vy[i] = 0
        self.y[i] &= 0xFF00
        self.life[i] = t["kind_life"][kind]
        self.period[i] = t["kind_period"][kind]
        self.seg[i] = path
        self.load(i)
        self.fire[i] = (self.period[i] >> 1) | 1
        self.count("an egg hatches: a drone " +
                   ("up" if line >= 88 else "down"))

    def bar(self, i):
        """A barrier's piece: its look by the barriers' cycle (anim, by
        sixteenth: varkon.py, BAR_MID_LOOKS): on, at its line (kept in
        aim), its sparks, pushing the ship; dimmed, its threads at its
        line, its own line BAR_AWAY; off, not shown, BAR_AWAY. Never
        destroyed, no flash. (picture, y register or None)."""
        c, t = self.c, self.t
        import varkon
        if not self.vy[i] & 255:
            self.aim[i] = (self.y[i] >> 8) & 255
            self.vy[i] = (self.vy[i] & 0xFF00) | 1
        mid = varkon.BAR_MID_LOOKS[(self.anim >> 4) & 15]
        self.life[i] = c["BARRIER_LIFE"]
        self.flash[i] = 0
        first = t["kind_block"][self.kind[i]]
        line = self.aim[i]
        if mid == 2:
            self.y[i] = line << 8 | (self.y[i] & 255)
            yreg = line + 50
            self.field_touch(i, yreg)
            return first + (self.anim3 & 1), yreg
        self.y[i] = c["BAR_AWAY"] << 8 | (self.y[i] & 255)
        if mid == 1:
            return first + 2 + (self.anim3 & 1), line + 50
        return first, None

    def module_beams(self, state):
        """Level 6's beams (st_beams, from beam_step: before the
        Varkon): the energy above and below the corridor (BAR_TOP,
        BAR_LOW) with the barriers' cycle (BAR_TOP_LOOKS,
        BAR_LOW_LOOKS), written when it changes (beam_timer keeps what
        was written); none in the arena."""
        import varkon
        c = self.c
        if state.boss.arena:
            return
        k = (self.anim >> 4) & 15
        top, low = varkon.BAR_TOP_LOOKS[k], varkon.BAR_LOW_LOOKS[k]
        looks = top | low << 2
        if looks == state.beam_timer:
            return
        state.beam_timer = looks
        state.set_beam(c["BAR_TOP"], top)
        state.set_beam(c["BAR_LOW"], low)
        self.count(f"the barriers: above {LOOKS[top]}, below "
                   f"{LOOKS[low]}")

    # --- level 2's towers ---------------------------------------------

    def wave_pri(self, i):
        """Varkon i's priority as it comes in: a tower's core or field
        BOSS_PRI; another Varkon its class (2) if its place had
        BOSS_PRI."""
        o = FIRST_ENEMY + i
        if self.beh(i) >= STAND:
            self.mux.set_pri(o, BOSS_PRI)
        elif self.mux.pri[o] == BOSS_PRI:
            self.mux.set_pri(o, 2)

    def field_touch(self, i, yreg):
        """A field's piece and the ship, flying: their boxes meet, the
        ship is pushed back as from a wall and loses two notches (none
        if it blinks)."""
        ship, t, c = self.ship, self.t, self.c
        if ship.mode != 0 or not self.box:
            return
        left, right, s_top, s_bottom = self.box
        k = self.kind[i]
        top = (yreg + t["kind_box_y"][k]) & 255
        if top >= s_bottom:
            return
        if (top + t["kind_box_h"][k]) & 255 <= s_top:
            return
        x0 = ((((self.x[i] >> 8) & 0xFFFF) >> 1) + t["kind_box_x"][k]) \
            & 255
        if x0 >= right:
            return
        if (x0 + t["kind_box_w"][k]) & 255 <= left:
            return
        ship.push_dx, ship.push_dy = -c["PUSH_SPEED"], 0
        ship.push = c["PUSH_FRAMES"]
        if ship.blink:
            self.count("a field on the ship while it blinks")
        elif not ship.invuln:
            self.count("a field on the ship: pushed back, two notches")
        ship.hurt(2, "a field")

    def fields_down(self, i):
        """Core i destroyed: the field's pieces flying within
        FIELD_REACH pixels of it (x registers; a distance under 0 one
        less: the program's) explode, without points."""
        xi = (self.x[i] >> 8) & 0xFFFF
        for j in range(ENEMIES - 1, -1, -1):
            if self.on[j] != FLYING or self.beh(j) != FIELD:
                continue
            d = (((self.x[j] >> 8) & 0xFFFF) - xi) & 0xFFFF
            if d & 0x8000:
                d ^= 0xFFFF
            if d < self.c["FIELD_REACH"]:
                self.on[j] = BOOM
                self.left[j] = 0
                self.flash[j] = 0
                self.count("a field goes down with its core")

    # --- level 3's mines and rocks ------------------------------------

    def mine_near(self, i):
        """Mine i, shown: the ship flying, near it? Then it bursts: its
        shrapnel, it explodes, no points (True)."""
        c, ship = self.c, self.ship
        if ship.mode != 0:
            return False
        dx = ((ship.x + 24) & 0xFFFF) - ((self.x[i] >> 8) & 0xFFFF)
        dx = signed16(dx & 0xFFFF)
        if not -c["MINE_REACH_X"] < dx < c["MINE_REACH_X"]:
            return False
        line = (self.y[i] >> 8) & 255
        dy = (ship.y - line) & 255
        if ship.y < line:
            dy = (-dy) & 255
        if dy >= c["MINE_REACH_Y"]:
            return False
        self.count("a mine bursts near the ship")
        for e in range(c["MINE_FAN_COUNT"]):
            self.shoot_entry(i, c["MINE_FAN_FIRST"] + e)
        self.on[i] = BOOM
        self.left[i] = 0
        self.flash[i] = 0
        self.sound("boom")
        return True

    def split(self, i):
        """Rock i destroyed: its two shards, in the first free Varkon
        (none: no shard)."""
        t, c = self.t, self.c
        for path, dy in ((c["PATH_SHARD_UP"], c["SHARD_DY_UP"]),
                         (c["PATH_SHARD_DOWN"], c["SHARD_DY_DOWN"])):
            for j in range(ENEMIES):
                if self.on[j] == FREE:
                    break
            else:
                self.count("a shard: no free Varkon")
                continue
            kind = c["KIND_SHARD"]
            self.on[j] = FLYING
            self.kind[j] = kind
            self.own[j] = None
            self.cap[j] = self.delay[j] = self.flash[j] = 0
            self.life[j] = t["kind_life"][kind]
            self.period[j] = self.fire[j] = 0
            self.x[j] = (self.x[i] >> 8) << 8
            self.y[j] = (((self.y[i] >> 8) + dy) & 255) << 8
            self.seg[j] = path
            self.load(j)
            self.wave_pri(j)
            self.count("a shard from a rock")
            self.count(f"Varkon {kind} in")
