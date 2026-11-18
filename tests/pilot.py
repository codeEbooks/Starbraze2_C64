"""An automatic pilot for the test's route (milestone 0.6; from 0.7 it
fetches the capsules).

It looks at the model's state before a turn (tests/scroll_model.py:
the program's state is the same, the test proves it frame by frame)
and chooses the joystick, Fire always held:
  - away from a plasma shot or a Varkon that will reach the ship in
    the next frames (up or down, where there is no rock);
  - else to a capsule on the screen, if there is one;
  - else towards the line of the nearest Varkon ahead of it, to shoot
    it, and back towards its own column;
  - never into the rock (the ship's five points, one move ahead).
From 0.8, in the arena, against the boss: in front of its body (never
over it), on the line of its nearest part alive (a cannon, then the
core), firing; away from the threats as everywhere. And, for the
test, into the boss at a line (into()), to be pushed by its body and
touch a cannon. From 0.8.2, in level 2: a field's pieces are not its
targets (its shots go through them to their core), they are threats
like the other Varkon; a beam drawn, dimmed or on, is rock to it (it
may come on); against a threat it looks further up and down, and goes
right if the threat comes from behind (the interceptors); and into()
can dodge the Varkon and their shots on its way into a field or a
beam. (Only in level 2: level 1's route stays as it was.)
From 0.8.6, against the GRAVEYARD WARDEN: its front is its guns'
(in front of its body), its parts the gun out and the core. From
0.8.8, against the VARKON CORVETTE: its front is its bow, its parts
the turrets left (the nearest by its line first: the deck's, then the
keel's, or the other way), then the bridge's dome; away from a threat
it goes up or down towards that line first, and it waits rather than
move up or down into a threat (its hangar's scouts cross the screen
between the deck's line and the keel's). From 0.8.10, against the
DEFENSE TURRET ARRAY: its front is its wall's, its parts the turrets of
the open row (the nearest by its line first), then the lens; while the
lens warns or fires its ray it keeps off the ray's lines (above them
or below, the nearer), else on the lens's line. From 0.8.11, level 6's
timed barriers, three pieces, two on at a time (the energy above the
corridor, the middle piece in it, the energy below it; the gap moving
by the frame counter): it goes to the piece that is off long enough to
fly through (or the one off first, and waits before the barrier), and
then through, right, without stopping (dimmed is not rock); a barrier
passed, it keeps clear of it. From 0.8.12, against the SUPER-COMPUTER
VARKON: its front is its outer ring's; its parts the turning ring's
plates left of the core (once they all turn), then the turrets out,
then the core, the nearest by its line first. From 0.8.13, in the
escape, it keeps to another column (home): on the left (the time runs
out) or in the screen's right half (the scroll a pixel a frame); the
falling pieces are threats that fall (FALL_VY a frame), not its
targets.
It is not a good player: it is a way to make the fights happen in a
route that is the same every time.
"""

UP, DOWN, LEFT, RIGHT, FIRE = 1, 2, 4, 8, 16
HOME_X = 64                    # the column it keeps to
CORRIDOR = 90                  # its line in the corridor (rows 10-14)
LOOK = 14                      # frames ahead, for the threats
AHEAD = 3                      # frames ahead, for the rock
MARGIN = 6                     # lines/pixels around the ship's box
FIELD = 5                      # (0.8.2) a field's behaviour
BAR = 12                       # (0.8.11) a barrier's middle piece
FALL = 13                      # (0.8.13) the escape's falling pieces
BAR_LOOK = 150                 # pixels ahead: a barrier's way
BAR_GAP = 6                    # pixels before its energy, waiting


def ship_box(state):
    """The ship's box on the screen: x0, y0, x1, y1 (excluded)."""
    t, ship = state.t, state.ship
    s = ship.type
    x0 = ship.x + 2 * t["ship_box_x"][s]
    y0 = ship.y + t["ship_box_y"][s]
    return (x0, y0, x0 + 2 * t["ship_box_w"][s],
            y0 + t["ship_box_h"][s])


def threats(state, box, dy, look=LOOK, fields=True):
    """Will a plasma shot or a Varkon meet the ship's box moved by dy
    lines in the next `look` frames (LOOK; from 0.8 longer against the
    boss)? (Straight lines: a guess.) fields (0.8.2): a field's pieces
    count. Returns where the threat is: "behind" (on the ship's left),
    True (elsewhere) or False."""
    v = state.varkon
    x0, y0, x1, y1 = box
    y0, y1 = y0 + dy - MARGIN, y1 + dy + MARGIN
    x0, x1 = x0 - MARGIN, x1 + MARGIN
    for j in range(len(v.s_on)):
        if not v.s_on[j]:
            continue
        sx = (v.s_x[j] >> 8) - 24 + 12
        sy = (v.s_y[j] >> 8) + 10
        vx = v.s_vx[j] / 256
        vy = (v.s_vy[j] - 65536 if v.s_vy[j] & 0x8000 else
              v.s_vy[j]) / 256
        for k in range(look):
            px, py = sx + vx * k, sy + vy * k
            if x0 <= px < x1 and y0 <= py < y1:
                return "behind" if sx < x0 else True
    for i in range(len(v.on)):
        if v.on[i] != 1 or v.delay[i] or \
                (not fields and v.beh(i) == FIELD):
            continue
        ex = (v.x[i] >> 8) - 24
        ey = v.y[i] >> 8
        vx = v.vx[i] / 256
        if v.beh(i):                   # on the rock: with the camera
            vx -= state.speed(0) / 256
        vy = state.c["FALL_VY"] / 256 if v.beh(i) == FALL else 0
        for k in range(0, look, 2):
            px, py = ex + vx * k, ey + vy * k
            if px < x1 and px + 24 > x0 and py < y1 and py + 21 > y0:
                return "behind" if ex + 24 <= x0 + MARGIN else True
    return False


def rock(state, dx, dy):
    """Would one of the ship's points be in the rock, moved by dx,
    dy? (From 0.8.2 a beam drawn counts.)"""
    ship, t, c = state.ship, state.t, state.c
    first = ship.type * 5
    beams = (c["BEAM_DOWN"], c["BEAM_UP"]) if c["BEAM_DOWN"] else \
        (c["BAR_TOP"], c["BAR_LOW"]) if state.level == 5 else ()
    # (0.8.11: level 6's, the station's module's)
    for k in range(5):
        px = ship.x + dx + t["ship_spot_x"][first + k]
        py = ship.y + dy + t["ship_spot_y"][first + k]
        if ship.solid(state, px, py):
            return True
        if beams:
            found = ship.point_cell(state, px, py)
            if found and found[0] in beams and \
                    any(state.charset[found[0] * 8:found[0] * 8 + 8]):
                return True
    return False


def target_line(state):
    """The y the ship wants: the nearest Varkon ahead, by its line."""
    v, ship = state.varkon, state.ship
    best, want = None, None
    for i in range(len(v.on)):
        if v.on[i] != 1 or v.delay[i] or v.beh(i) in (FIELD, FALL):
            continue
        ex = (v.x[i] >> 8) - 24
        if ex < ship.x + 16 or ex > 300:
            continue
        ey = v.y[i] >> 8
        score = (ex - ship.x) + 2 * abs(ey - ship.y)
        if best is None or score < best:
            best, want = score, ey
    return want


def capsule(state):
    """The nearest capsule on the screen: its sprite's x, y; or None."""
    v = state.varkon
    best = None
    for i in range(len(v.on)):
        if v.on[i] != 3:
            continue
        x = (v.x[i] >> 8) - 24
        if 0 <= x <= 300 and (best is None or x < best[0]):
            best = (x, v.y[i] >> 8)
    return best


def clear(state, jx, jy, step):
    """No rock on the ship's points in the next AHEAD frames, moving
    jx, jy (-1, 0, 1) at step pixels a frame, the rock coming at the
    camera's speed (from milestone 0.7)."""
    cam = state.speed(0) / 256
    for k in range(1, AHEAD + 1):
        if rock(state, round((jx * step + cam) * k), jy * step * k):
            return False
    return True


def move(state, jx, jy, step, base):
    """The wanted move (jx, jy), or the nearest one without rock: the
    joystick bits."""
    for mx, my in ((jx, jy), (0, jy), (jx, 0), (-1, jy), (0, 0),
                   (-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1)):
        y = state.ship.y + my * step
        if (mx or my or (mx, my) == (jx, jy)) and \
                not 0 <= y <= 154:
            continue
        if clear(state, mx, my, step):
            break
    else:
        mx, my = jx, jy
    return base | (RIGHT if mx > 0 else LEFT if mx < 0 else 0) | \
        (DOWN if my > 0 else UP if my < 0 else 0)


def toward(goal, now, slack):
    return 1 if goal > now + slack else -1 if goal < now - slack else 0


FIGHTING = (1, 2, 3, 4)          # the boss's steps: ENTER - CORE
BOSS_GAP = 16                    # pixels from the body's front
BOSS_LOOK = 30                   # frames ahead, for the threats
RAY_GAP = 6                      # (0.8.10) lines off the ARRAY's ray


def boss_part(state):
    """The boss's part alive nearest the ship: the middle line of its
    box (the playfield's), or None."""
    b, v, t = state.boss, state.varkon, state.t
    best = None
    alive = [b.part[k] for k in range(3) if b.parts >> k & 1]
    if state.c["LEVEL_BOSS"] == 4:              # (0.8.8) the CORVETTE's
        alive = [b.cv_part[k] for k in range(4)     # turrets, its dome
                 if b.parts & 1 and b.cv_live >> k & 1] + [
                     b.part[2] for _ in (0,) if b.parts & 4]
    if state.c["LEVEL_BOSS"] == 5:              # (0.8.10) the ARRAY's
        alive = [b.dt_part[k] for k in range(6)     # turrets, its lens
                 if b.parts & 1 and b.dt_live >> k & 1] + [
                     b.part[2] for _ in (0,) if b.parts & 4]
    if state.c["LEVEL_BOSS"] == 6:              # (0.8.12) the SUPER-
        alive = [i for i in b.sc_pv if not i & 0x80   # COMPUTER's ring's
                 and b.state == 2 and not b.sc_cyc and   # plates, its
                 (v.x[i] >> 8) < state.c["SC_MIDX"] + 128] + [  # turrets,
            b.sc_tv[k] for k in range(4)                 # its core
            if b.state == 3 and b.sc_tlive >> k & 1] + [
                b.part[2] for _ in (0,) if b.parts & 4]
    near = state.c["LEVEL_BOSS"] in (4, 5, 6)   # (0.8.8) by its line
    for i in alive:
        x = (v.x[i] >> 8) - 24
        kind = v.kind[i]
        mid = (v.y[i] >> 8) + t["kind_box_y"][kind] + \
            t["kind_box_h"][kind] // 2
        if near:
            x = (abs(mid - 10 - state.ship.y), x)
        if best is None or x < best[0]:
            best = (x, mid)
    return best


def boss_front(state):
    """The boss's front: the crawler's body; (0.8.3) the SHIELD CORE's
    pods, its parts furthest left; (0.8.6) the GRAVEYARD WARDEN's guns,
    in front of its body; (0.8.8) the VARKON CORVETTE's bow."""
    b, c = state.boss, state.c
    if not b.state:
        return 320
    if c["LEVEL_BOSS"] == 6:                    # (0.8.12) its outer
        return c["SC_MIDX"] + 128 - 24 - 40     # ring's front
    if c["LEVEL_BOSS"] == 5:                    # (0.8.10) its wall
        return 8 * c["DT_COL0"]
    if c["LEVEL_BOSS"] == 4:                    # (0.8.8) its bow
        return 2 * b.shown_x
    if c["LEVEL_BOSS"] == 3:                    # (0.8.6) the WARDEN's
        return c["W_PART_X"] - 24               # guns
    if c["LEVEL_BOSS"] == 2:
        return c["CB_POD_XR"] - 24
    return 2 * b.shown_x + 7


def boss_choice(state, step, joy):
    """In the arena: away from the threats seen further ahead (the
    fans, the core's shots), else in front of the body, on the line
    of a part."""
    ship, b, c = state.ship, state.boss, state.c
    box = ship_box(state)
    part = boss_part(state)
    goal_y = part[1] - 10 if part else CORRIDOR
    corvette = c["LEVEL_BOSS"] in (4, 5, 6)     # (0.8.8; 0.8.10;
                                                # 0.8.12)
    if c["LEVEL_BOSS"] == 5 and b.dt_ray:       # (0.8.10) off its ray's
        top = c["DT_RAY_TOP"] - 50 - RAY_GAP    # lines, above or below
        bottom = c["DT_RAY_BOTTOM"] - 50 + RAY_GAP
        above = top - (box[3] - ship.y)         # its box's bottom there
        below = bottom - (box[1] - ship.y)      # its box's top there
        goal_y = above if abs(above - ship.y) <= abs(below - ship.y) \
            else below
    if threats(state, box, 0, BOSS_LOOK):
        dodges = ((-8 * step, UP), (8 * step, DOWN),
                  (-16 * step, UP), (16 * step, DOWN))
        if corvette:                            # towards its line
            dodges = sorted(dodges, key=lambda d: (
                abs(ship.y + d[0] - goal_y), abs(d[0])))
        for dy, bit in dodges:
            y = ship.y + dy
            if 0 <= y <= 154 and \
                    not threats(state, box, dy, BOSS_LOOK) and \
                    clear(state, 0, -1 if bit == UP else 1, step):
                return joy | bit
    front = boss_front(state)
    goal_x = min(HOME_X, front - 24 - BOSS_GAP)
    jx = toward(goal_x, ship.x, 2)
    if ship.x > front - 24 - 8:
        jx = -1
    jy = toward(goal_y, ship.y, 1)
    if corvette and jy and threats(state, box, 8 * step * jy,
                                   BOSS_LOOK) and \
            not (c["LEVEL_BOSS"] == 5 and b.dt_ray):
        jy = 0                                  # not into a threat (but
                                                # off the ARRAY's ray)
    return move(state, jx, jy, step, joy)


def choose(state, ram=False, pods=True, home=HOME_X):
    """The joystick for the next turn; ram: no dodging (to meet a
    Varkon with the ship); pods: to the capsules (else away from
    them); home (0.8.13): the column it keeps to."""
    ship = state.ship
    if ship.mode != 0:
        return FIRE
    speed = ship.speed() / 256
    step = max(1, round(speed))
    box = ship_box(state)
    joy = 0 if ram else FIRE
    if state.level == 5 and not ram:        # (0.8.11) level 6's
        way = barrier_choice(state, step, joy)   # barriers
        if way is not None:
            return way
    threat = not ram and threats(state, box, 0)
    if threat:
        dodges = [(-6 * step, UP), (6 * step, DOWN)]
        if state.level:                     # (0.8.2) level 2
            dodges += [(-12 * step, UP), (12 * step, DOWN),
                       (-18 * step, UP), (18 * step, DOWN)]
        for dy, bit in dodges:
            y = ship.y + dy
            if 0 <= y <= 154 and not threats(state, box, dy) and \
                    clear(state, 0, -1 if bit == UP else 1, step):
                return joy | bit
        if state.level:                     # (0.8.2) never into rock
            way = (RIGHT, 1) if threat == "behind" else (LEFT, -1)
            ok = clear(state, way[1], 0, step) and \
                (way[0] == RIGHT or ship.x > 24)
            return joy | (way[0] if ok else 0)
        return joy | (LEFT if ship.x > 24 else 0)
    if state.boss.arena and state.boss.state in FIGHTING:
        return boss_choice(state, step, joy)
    pod = None if ram else capsule(state)
    if pod and pods:                        # fetch it
        x, y = pod
        return move(state, toward(x, ship.x, 2), toward(y, ship.y, 1),
                    step, joy)
    if pod and -40 < pod[0] - ship.x < 80 and abs(pod[1] - ship.y) < 30:
        away = -1 if pod[1] >= ship.y else 1    # leave it: not its line
        if not 8 <= ship.y + away * 24 <= 146:
            away = -away
        return move(state, 0, away, step, joy)
    want = target_line(state)
    if want is None or not 24 <= want <= 130:
        want = CORRIDOR
    for ahead in (4, 10, 16):               # a wall coming: the corridor
        if rock(state, ahead, 0):
            want = CORRIDOR
            break
    jx = 1 if ship.x < home - 2 else -1 if ship.x > home + 2 else 0
    return move(state, jx, toward(want, ship.y, 1), step, joy)


def into(state, y, dodge=False):
    """From 0.8, in the arena: to the line y and to the right, into
    the boss (its body, a part), not firing, not dodging. From 0.8.2
    (dodge): into a field or a beam, away from the Varkon (not a
    field's pieces) and their shots, up or down, if it can."""
    ship = state.ship
    if ship.mode != 0:
        return 0
    if dodge:
        box = ship_box(state)
        if threats(state, box, 0, fields=False):
            for dy, bit in ((-8, UP), (8, DOWN), (-16, UP), (16, DOWN)):
                if 0 <= ship.y + dy <= 154 and \
                        not threats(state, box, dy, fields=False):
                    return RIGHT | bit
    return RIGHT | (DOWN if y > ship.y + 1 else
                    UP if y < ship.y - 1 else 0)


def hold(state, x, y):
    """To the place (x, y) and there, not firing; away from threats
    and the rock as choose()."""
    ship = state.ship
    if ship.mode != 0:
        return 0
    step = max(1, round(ship.speed() / 256))
    box = ship_box(state)
    if threats(state, box, 0):
        for dy, bit in ((-8, UP), (8, DOWN)):
            if 0 <= ship.y + dy <= 154 and \
                    not threats(state, box, dy) and \
                    clear(state, 0, -1 if bit == UP else 1, step):
                return bit
    return move(state, toward(x, ship.x, 2), toward(y, ship.y, 1),
                step, 0)


# --- level 6's barriers (0.8.11) -------------------------------------

def barriers(state):
    """The barriers' energy on the screen: [(left, right)] (screen
    pixels; the middle piece's sprite, its energy from its pixel 4 to
    19), one a barrier."""
    v = state.varkon
    out = set()
    for i in range(len(v.on)):
        if v.on[i] == 1 and not v.delay[i] and v.beh(i) == BAR:
            left = (v.x[i] >> 8) - 24 + 4
            out.add((left, left + 15))
    return sorted(out)


def side_open(state, side):
    """Frames the barriers' piece `side` (0 above the corridor, 1 in it,
    2 below it) stays not on (off or dimmed) from the next frame; 0 if
    it is on then (the barriers' cycle by the frame counter: varkon.py,
    BAR_*_LOOKS)."""
    import varkon
    looks = (varkon.BAR_TOP_LOOKS, varkon.BAR_MID_LOOKS,
             varkon.BAR_LOW_LOOKS)[side]
    anim = state.varkon.anim
    for f in range(256):
        if looks[((anim + 1 + f) >> 4) & 15] == 2:
            return f
    return 256


def side_next(state, side):
    """Frames until the piece `side` is next not on (0: now)."""
    import varkon
    looks = (varkon.BAR_TOP_LOOKS, varkon.BAR_MID_LOOKS,
             varkon.BAR_LOW_LOOKS)[side]
    anim = state.varkon.anim
    for f in range(256):
        if looks[((anim + 1 + f) >> 4) & 15] < 2:
            return f
    return 256


def side_line(state, left, side):
    """The ship's y in the middle of the way above the corridor (0), in
    it (1: lines 80-119) or below it (2), at the barrier (its emitter's
    column, left of the energy: the ceiling's last line, the floor's
    first)."""
    ship, t = state.ship, state.t
    s = ship.type
    px = left - 4
    if side == 0:
        lo = next((y for y in range(0, 80)
                   if not ship.solid(state, px, y)), 16)
        hi = 80
    elif side == 1:
        lo, hi = 80, 120
    else:
        lo = 120
        hi = next((y for y in range(120, 176)
                   if ship.solid(state, px, y)), 152)
    return (lo + hi) // 2 - t["ship_box_y"][s] - t["ship_box_h"][s] // 2


def barrier_choice(state, step, joy):
    """Level 6: the joystick against the barriers, or None (none
    near)."""
    ship = state.ship
    x0, y0, x1, y1 = ship_box(state)
    passed = [r for l, r in barriers(state) if r < x0]
    ahead = [(l, r) for l, r in barriers(state)
             if r >= x0 and l - x1 < BAR_LOOK]
    safe = max(passed) + 10 if passed else 0
    if not ahead:
        if passed and x0 < safe + 4:            # keep clear of it
            return joy | RIGHT
        return None
    left, right = ahead[0]
    rate = step + state.speed(0) / 256           # pixels a frame
    need = int((right + 1 + 4 - x0) / rate) + 4  # to be through
    if x1 >= left - 2:                           # in it: through
        side = 0 if y1 <= 80 else 2 if y0 >= 120 else 1
        want = side_line(state, left, side)
        return joy | RIGHT | (DOWN if want > ship.y + 1 else
                              UP if want < ship.y - 1 else 0)
    go = sorted(((side_open(state, side), side) for side in range(3)
                 if side_open(state, side) >= need), reverse=True)
    if go:                                       # open long enough
        side = go[0][1]
        want = side_line(state, left, side)
        if abs(want - ship.y) <= 2:
            return joy | RIGHT | (DOWN if want > ship.y else
                                  UP if want < ship.y else 0)
        dx = 0 if x1 < left - BAR_GAP - 2 else -1
    else:                                        # the side next off
        side = min(range(3), key=lambda k: side_next(state, k))
        want = side_line(state, left, side)
        dx = 1 if x1 < left - BAR_GAP - 12 else \
            -1 if x1 > left - BAR_GAP else 0
    if x0 + 2 * dx < max(safe, 24):
        dx = 0
    return move(state, dx, toward(want, ship.y, 1), step, joy)
