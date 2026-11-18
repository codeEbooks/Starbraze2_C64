"""The model of the Varkon's flight and of the multiplexer.

Varkon: the waves come in when the camera reaches their column; each
Varkon follows its path (stretches of so many frames at a velocity,
256ths of a pixel), fires its plasma shots, leaves on the left. They
move at the end of the turn, for the next frame.

Objects: what the multiplexer shows on sprites 2-7: the ship's four
shots (0-3), the twelve Varkon (4-15), their six shots (16-21), the
satellite (22) and the missile (23), all multicolour. Each has a sprite
place (x register, 9 bits; y register), a block, a colour; here y 0: not
shown (the program keeps 255). Two banks: the turn writes the ship's
shots into this frame's bank, the Varkon into the next one's (the
interrupts still read this frame's).

The plan of a frame (Mux.plan):
  1. order: two lists kept from frame to frame, each put in order of y
     by insertion (objects not shown last), stable: the Varkon's and
     their shots' (4-21), at the end of each turn for the next frame's
     bank; the ship's (0-3, 22, 23), at the plan; the plan takes them
     together, the lower y first (equal: the Varkon's);
  2. entries: in that order, each object becomes the plan's next
     entry i, on sprite 2 + i mod 6. From the seventh on, its
     registers are written when the sprite's entry before it has been
     drawn (line y + MUX_FREE), the writes MUX_COST lines each, one
     after the other, each done within MUX_DONE lines and before the
     entry's own line;
  3. an object that cannot be written in time gets no entry: of it and
     the last six entries, the one with the lowest priority is left
     out (class: shots of the Varkon 3, Varkon 2, shots of the ship 1;
     + STARVE if the plan before left it out; equal: the later one).
     If that is an entry, the object takes its place: the same
     sprite, the same write, for a later line (it still comes in
     time: its y is not less). The program keeps each object's
     priority for the next plan (obj_pri).
"""

ENEMIES, ESHOTS = 12, 6
OBJECTS = 4 + ENEMIES + ESHOTS + 2
FIRST_ENEMY, FIRST_ESHOT = 4, 4 + ENEMIES
FIRST_SAT = FIRST_ESHOT + ESHOTS          # the satellite, the missile
HARDWARE = 6                    # sprites 2-7
MUX_FREE = 22                   # the line after a sprite's last
MUX_COST = 4                    # lines from a write to the next
MUX_DONE = 5                    # lines a write may take, at most
FIELD_LINE = 70                 # the first interrupt of the field
STARVE = 4


def signed16(v):
    return v - 65536 if v & 0x8000 else v


class Varkon:
    def __init__(self, files):
        self.c = files["constants"]
        self.t = files["tables"]
        self.stats = {}
        self.sound = lambda effect: None   # sfx_start (player_model)
        self.reset()

    def reset(self):
        self.on = [0] * ENEMIES
        self.kind = [0] * ENEMIES
        self.delay = [0] * ENEMIES
        self.seg = [0] * ENEMIES
        self.left = [0] * ENEMIES
        self.vx = [0] * ENEMIES          # signed, 256ths
        self.vy = [0] * ENEMIES
        self.x = [0] * ENEMIES           # x register, 256ths, signed
        self.y = [0] * ENEMIES           # 256ths
        self.fire = [0] * ENEMIES
        self.s_on = [0] * ESHOTS
        self.s_x = [0] * ESHOTS
        self.s_y = [0] * ESHOTS
        self.s_vx = [0] * ESHOTS
        self.s_vy = [0] * ESHOTS
        self.wave = 0
        self.anim = 0

    def count(self, what):
        self.stats[what] = self.stats.get(what, 0) + 1

    def load(self, i):
        t, s = self.t, self.seg[i]
        self.left[i] = t["seg_frames"][s]
        self.vx[i] = signed16(t["seg_vxl"][s] | t["seg_vxh"][s] << 8)
        self.vy[i] = signed16(t["seg_vyl"][s] | t["seg_vyh"][s] << 8)

    def update(self, ship_y, column):
        """One frame, at the end of the turn: the shots, the Varkon,
        the waves."""
        t, c = self.t, self.c
        for j in range(ESHOTS):
            if not self.s_on[j]:
                continue
            self.s_x[j] += self.s_vx[j]
            self.s_y[j] = (self.s_y[j] + self.s_vy[j]) & 0xFFFF
            if self.s_x[j] >> 8 <= 0 or \
                    self.s_y[j] >> 8 > c["VARKON_Y_MAX"]:
                self.s_on[j] = 0
                self.count("plasma gone")
        for i in range(ENEMIES):
            if not self.on[i]:
                continue
            if self.delay[i]:
                self.delay[i] -= 1
                continue
            self.x[i] += self.vx[i]
            self.y[i] = (self.y[i] + self.vy[i]) & 0xFFFF
            self.left[i] -= 1
            if self.left[i] == 0:
                self.seg[i] += 1
                self.load(i)
                if self.left[i] == 0:
                    self.on[i] = 0
                    self.count("Varkon at the path's end")
                    continue
            if self.x[i] >> 8 <= 0:
                self.on[i] = 0
                self.count("Varkon gone left")
                continue
            period = t["kind_period"][self.kind[i]]
            if period:
                self.fire[i] -= 1
                if self.fire[i] == 0:
                    self.fire[i] = period
                    self.shoot(i, ship_y)
        while True:
            w = self.wave
            col = t["wave_col_lo"][w] | t["wave_col_hi"][w] << 8
            if column < col:
                break
            self.spawn(w)
            self.wave += 1
        self.anim = (self.anim + 1) & 255

    def shoot(self, i, ship_y):
        t, c = self.t, self.c
        for j in range(ESHOTS):
            if not self.s_on[j]:
                break
        else:
            self.count("Varkon shot: no free place")
            return
        self.sound("plasma")
        k = self.kind[i]
        self.s_on[j] = 1
        self.s_x[j] = self.x[i] + (signed8(c["SHOT_DX"]) << 8)
        self.s_y[j] = (self.y[i] + (c["SHOT_DY"] << 8)) & 0xFFFF
        self.s_vx[j] = -(t["kind_shot_speed"][k] << 8)   # whole pixels
        vy = 0
        if t["kind_aim"][k]:
            y = self.s_y[j] >> 8
            if ship_y > y + c["AIM_DEAD"]:
                vy = c["AIM_VY"]
            elif ship_y + c["AIM_DEAD"] < y:
                vy = -c["AIM_VY"]
        self.s_vy[j] = vy
        self.count("Varkon shot")

    def spawn(self, w):
        t = self.t
        count = t["wave_count"][w]
        for k in range(count):
            for i in range(ENEMIES):
                if not self.on[i]:
                    break
            else:
                self.count("wave: no free Varkon")
                continue
            kind = t["wave_kind"][w]
            self.on[i] = 1
            self.kind[i] = kind
            self.delay[i] = k * t["wave_spacing"][w]
            self.seg[i] = t["wave_path"][w]
            self.load(i)
            x = signed16(t["wave_x_lo"][w] | t["wave_x_hi"][w] << 8)
            self.x[i] = (x + 24) << 8         # the x register
            step = signed8(t["wave_dy"][w])
            self.y[i] = ((t["wave_y"][w] + k * step) & 255) << 8
            period = t["kind_period"][kind]
            self.fire[i] = (period >> 1) + 7 * k if period else 0
            self.count(f"Varkon {kind} in")

    def objects(self):
        """The Varkon and their shots as objects 4-21: (y register or
        0, x register 9 bits, block, colour, multicolour). x is kept
        as the program keeps it, as the x register (screen x + 24):
        shown if 1-343, gone if 0 or less."""
        t, c = self.t, self.c
        out = []
        for i in range(ENEMIES):
            x = self.x[i] >> 8
            if self.on[i] and not self.delay[i] and 0 < x < 344:
                k = self.kind[i]
                out.append(((self.y[i] >> 8) + 50, x & 0x1FF,
                            t["kind_block"][k] + ((self.anim >> 3) & 3),
                            t["kind_colour"][k], 1))
            else:
                out.append((0, 0, 0, 0, 0))
        for j in range(ESHOTS):
            x = self.s_x[j] >> 8
            if self.s_on[j] and 0 < x < 344:
                out.append(((self.s_y[j] >> 8) + 50, x & 0x1FF,
                            c["PLASMA_BLOCK"] + ((self.anim >> 2) & 3),
                            c["PLASMA_COLOUR"], 1))
            else:
                out.append((0, 0, 0, 0, 0))
        return out


def signed8(v):
    return v - 256 if v & 0x80 else v


class Mux:
    def __init__(self, files):
        self.t = files["tables"]
        self.stats = {"frames": 0, "left out": 0, "crowded": 0,
                      "left out: the object itself": 0,
                      "left out: an entry, for a later one": 0,
                      "most shown": 0, "most objects": 0,
                      "frames with some left out": 0}
        self.left_out_by_class = {1: 0, 2: 0, 3: 0}
        self.reset()

    def reset(self):
        self.order_v = list(range(FIRST_ENEMY, FIRST_SAT))
        self.order_s = [0, 1, 2, 3, FIRST_SAT, FIRST_SAT + 1]
        self.before = set()              # left out by the plan before
        self.out = set()                 # left out by this plan
        # the priorities as the program keeps them (obj_pri): the class, +
        # STARVE for those the last plan left out; BOSS_PRI for a boss's
        # part (boss_model, set_pri)
        self.pri = [self.t["obj_class"][o] for o in range(OBJECTS)]
        self.plan = []                   # (object, y, x, block, colour, mc)
        self.trig = []                   # from the seventh: the line it
        self.starts = []                 # may be written from, its write

    def priority(self, o):
        return self.pri[o]

    def set_pri(self, o, value):
        """Object o's priority (a boss's part: over all the
        others)."""
        self.pri[o] = value

    def update_priorities(self):
        """At the end of the turn (priorities): those the plan before
        left out have their class again, those this plan left out
        their class + STARVE."""
        cls = self.t["obj_class"]
        for o in self.before:
            self.pri[o] = cls[o]
        for o in self.out:
            self.pri[o] = cls[o] + STARVE
        self.before = self.out

    def priorities(self):
        """What the program keeps for the next plan (obj_pri)."""
        return list(self.pri)

    @property
    def order(self):
        """Both lists, as the program keeps them (order)."""
        return self.order_v + self.order_s

    @staticmethod
    def insertion(order, key):
        for i in range(1, len(order)):
            o, j = order[i], i
            while j > 0 and key[order[j - 1]] > key[o]:
                order[j] = order[j - 1]
                j -= 1
            order[j] = o

    def sort(self, objects):
        """The Varkon's order of y, at the end of each turn, for the
        next frame's bank."""
        self.insertion(self.order_v, [o[0] if o[0] else 255
                                      for o in objects])

    def merged(self, key):
        """The two lists together: the lower y first, equal: the
        Varkon's."""
        out, i, j = [], 0, 0
        v, s = self.order_v, self.order_s
        while i < len(v) or j < len(s):
            kv = key[v[i]] if i < len(v) else 256
            ks = key[s[j]] if j < len(s) else 256
            if kv <= ks:
                out.append(v[i])
                i += 1
            else:
                out.append(s[j])
                j += 1
        return out

    def make_plan(self, objects):
        """objects: 24 tuples (y, x, block, colour, mc), y 0 = none:
        the ship's order sorted, then the plan."""
        key = [o[0] if o[0] else 255 for o in objects]
        self.insertion(self.order_s, key)
        order = self.merged(key)
        plan, trig, starts, done = [], [], [], FIELD_LINE - MUX_COST
        out = set()
        crowded = 0
        for o in order:
            if key[o] == 255:
                break
            n = len(plan)
            if n >= HARDWARE:
                free = key[plan[n - HARDWARE]] + MUX_FREE
                start = max(free, done + MUX_COST)
                if start + MUX_DONE > key[o]:
                    crowded += 1
                    victim, at = o, None
                    low = self.priority(o)
                    for k in range(n - 1, n - HARDWARE - 1, -1):
                        if self.priority(plan[k]) < low:
                            victim, at = plan[k], k
                            low = self.priority(plan[k])
                    out.add(victim)
                    if at is not None:
                        plan[at] = o
                        self.stats["left out: an entry, for a later one"] += 1
                    else:
                        self.stats["left out: the object itself"] += 1
                    continue
                trig.append(free)
                starts.append(start)
                done = start
            plan.append(o)
        plan = [(o,) + tuple(objects[o]) for o in plan]
        shown = len(plan)
        active = sum(1 for k in key if k != 255)
        s = self.stats
        s["frames"] += 1
        s["left out"] += len(out)
        s["crowded"] += crowded
        s["most shown"] = max(s["most shown"], shown)
        s["most objects"] = max(s["most objects"], active)
        if out:
            s["frames with some left out"] += 1
        for o in out:
            self.left_out_by_class[self.t["obj_class"][o]] += 1
        self.plan, self.trig, self.starts = plan, trig, starts
        self.out = out
        return plan
