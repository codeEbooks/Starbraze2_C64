"""The model of the SUPER-COMPUTER VARKON, level 6's boss
(game/src/supercomp.asm, game/assets/supercomp.py), written again from
the program's rules and comments, without the program: a part of the
boss's model (boss_model.py's Boss takes it), compared with the program
frame by frame by the test (verify_game.py).

  - draw (boss_draw, a turn): the area's cells to draw, SC_CELLS_TURN
    a turn at most; else in ENTER a row of the housing, then a row of
    the area (its cells: the back plate comes); else an element whose
    state changed (its cells); else the lights' new step;
  - step (boss_update, after the bar's step): WAIT (its codes, four a
    turn: their lines and their rock, their lines AND their masks;
    no Varkon flying or exploding, its pictures over level 6's, 64
    bytes a turn; then its start), ENTER (the housing closes in, the
    area, its elements one by one, the outer ring's plates one by
    one, turning), FIGHT (the ring turns, its plates placed, the gaps
    of the rings waiting where its gap is; the core's shot through
    them while they face the ship; its last plate gone, the next ring:
    its segments go, its plates come one a frame), OPEN (the turrets
    in pairs: out, their fans aimed at the ship, back in; all four
    destroyed, the shell opens, the core comes), CORE (its fan turns,
    a fan of three while it is towards the left; faster under half
    its life), CHAIN (on it);
  - paint: the housing's colours (its own with the lights at their
    step, white, the wreck's);
  - the bar every fourth frame.
"""

import varkon_model

ST_WAIT, ST_ENTER, ST_FIGHT, ST_OPEN, ST_CORE = range(5)
ST_CHAIN, ST_WRECK = 5, 6
FREE, FLYING, BOOM = 0, 1, 2


class SuperComputer:
    """The SUPER-COMPUTER VARKON's part of the boss (a mixin of
    boss_model.Boss: its self.c, self.t, self.v, self.state_, its
    engine's routines)."""

    def s_reset_values(self):
        """Its variables (page 2, 0 at the level's start: boss_reset)."""
        most = self.c["SC_MOST"]
        self.sc_ring = 0
        self.sc_ang = 0
        self.sc_pv = [0] * most
        self.sc_shown = [0, 0, 0]
        self.sc_want = [0, 0, 0]
        self.sc_have = [0, 0, 0]
        self.sc_hrows = self.sc_hdrawn = 0
        self.sc_arows = self.sc_adrawn = 0
        self.sc_made = self.sc_estep = self.sc_count = 0
        self.sc_cyc = self.sc_fire = 0
        self.sc_light = self.sc_lshown = self.sc_mode = 0
        self.sc_pair = self.sc_slide = 0
        self.sc_tv = [0] * 4
        self.sc_tlife = [0] * 4
        self.sc_tlive = self.sc_tgone = 0
        self.sc_way = self.sc_wt = self.sc_ft = 0
        self.sc_di = self.sc_dn = 0
        self.sc_t = 0

    def sc_memory(self):
        """$0258 on: arena_chars, its variables (sc_ring ... sc_dn; its
        scratch after them left out)."""
        return bytes([self.arena_chars, self.sc_ring, self.sc_ang & 255,
                      self.sc_ang >> 8] + self.sc_pv + self.sc_shown +
                     self.sc_want + self.sc_have +
                     [self.sc_hrows, self.sc_hdrawn, self.sc_arows,
                      self.sc_adrawn, self.sc_made, self.sc_estep,
                      self.sc_count, self.sc_cyc, self.sc_fire,
                      self.sc_light, self.sc_lshown, self.sc_mode,
                      self.sc_pair, self.sc_slide] + self.sc_tv +
                     self.sc_tlife +
                     [self.sc_tlive, self.sc_tgone, self.sc_way,
                      self.sc_wt, self.sc_ft, self.sc_di, self.sc_dn])

    # --- the screen (boss_draw) ------------------------------------

    def s_draw(self, state):
        c, t = self.c, self.t
        if self.state == ST_WAIT:
            return "none"
        if self.sc_di < self.sc_dn:
            self.s_cells(state)
            return "sc cells"
        if self.sc_hdrawn < self.sc_hrows:
            self.s_house_row(state)
            return "sc housing row"
        if self.sc_adrawn < self.sc_arows:
            x = self.sc_adrawn
            self.sc_adrawn += 1
            self.sc_di = t["sc_r_first"][x]
            self.sc_dn = t["sc_r_first"][x + 1]
            self.s_cells(state)
            self.count("the SUPER-COMPUTER: a row of its area")
            return "sc area row"
        for x in (2, 1, 0):
            bits = self.sc_want[x] ^ self.sc_have[x]
            if bits:
                e = 8 * x + ((bits & -bits).bit_length() - 1)
                self.sc_have[x] ^= t["sc_e_bit"][e]
                self.sc_di = t["sc_e_first"][e]
                self.sc_dn = t["sc_e_first"][e + 1]
                self.s_cells(state)
                on = self.sc_have[x] & t["sc_e_bit"][e]
                self.count("the SUPER-COMPUTER: " + (
                    "its shell" if e == c["SC_SHELL"] else
                    f"a segment of ring {1 + e // 8}") +
                    (" drawn" if on else " drawn away"))
                return "sc element"
        if self.sc_light != self.sc_lshown and not self.sc_mode:
            self.sc_lshown = self.sc_light
            self.s_lamps(state)
            return "sc lights"
        return "none"

    def s_cells(self, state):
        """SC_CELLS_TURN of the area's cells to draw, at most."""
        t = self.t
        for _ in range(self.c["SC_CELLS_TURN"]):
            if self.sc_di >= self.sc_dn:
                return
            self.s_cell(state, t["sc_lists"][self.sc_di])
            self.sc_di += 1

    def s_cell(self, state, k):
        """Cell k of the area: its code by the state drawn of the
        elements it touches, its colour."""
        t = self.t
        index, bit = 0, 1
        for i in range(4):
            e = t["sc_d_el"][4 * k + i]
            if e & 0x80:
                break
            if self.sc_have[t["sc_e_byte"][e]] & t["sc_e_bit"][e]:
                index |= bit
            bit <<= 1
        code = t["sc_d_codes"][t["sc_d_first"][k] + index]
        at = t["sc_d_lo"][k] | t["sc_d_hi"][k] << 8
        state.screens[0][at] = code
        state.colour[at] = t["sc_d_col"][k] & 15

    def s_hues(self):
        """The housing's colours: each group of lights' (the step less
        the group), then sc_fixed's."""
        t = self.t
        return [t["sc_cycle"][(self.sc_light - g) & 3]
                for g in range(4)] + t["sc_fixed"]

    def s_house_row(self, state):
        c, t = self.c, self.t
        hues = self.s_hues()
        row = t["sc_closing"][self.sc_hdrawn]
        self.sc_hdrawn += 1
        first = 5 * row
        for col in range(c["SC_HOUSE_COLS"]):
            at = (c["SC_HOUSE_ROW0"] + row) * 40 + c["SC_HOUSE_COL0"] + col
            state.screens[0][at] = t["sc_house"][first + col]
            state.colour[at] = hues[t["sc_hsrc"][first + col]] & 15
        self.count("the SUPER-COMPUTER's housing: a row")

    def s_lamps(self, state):
        """The lights at their step: each its group's colour."""
        hues = self.s_hues()
        for at, g in self.files["supercomp"]["lights"]:
            state.colour[at] = hues[g] & 15
        self.count("the SUPER-COMPUTER's lights: a step")

    def s_paint(self, state, which):
        """Its colours: 0 its own, 1 white, 2 the wreck's, in the
        housing's cells; its own: the lights at their step."""
        c, t = self.c, self.t
        self.sc_mode = which
        hues = self.s_hues()
        for row in range(c["SC_HOUSE_ROWS"]):
            for col in range(c["SC_HOUSE_COLS"]):
                k = row * 5 + col
                colour = (hues[t["sc_hsrc"][k]], c["SC_FLASH_OWN"],
                          c["SC_WRECK_OWN"])[which]
                at = (c["SC_HOUSE_ROW0"] + row) * 40 + \
                    c["SC_HOUSE_COL0"] + col
                state.colour[at] = colour & 15

    # --- its turn (boss_update) ------------------------------------

    def s_step(self):
        self.part_x = self.c["SC_PART_X"]
        (self.s_wait, self.s_enter, self.s_rings, self.s_defences,
         self.s_core, self.s_chain, self.step_wreck, self.step_clear,
         self.step_done)[self.state]()

    def s_place(self, i, x, y):
        """Varkon i at x register x, line y (its line's fraction
        kept)."""
        v = self.v
        v.x[i] = (x & 0xFFFF) << 8
        v.y[i] = (y & 255) << 8 | (v.y[i] & 255)

    def s_step_lights(self):
        if not self.v.anim & (self.c["SC_LIGHT_EVERY"] - 1):
            self.sc_light = (self.sc_light + 1) & 3

    def s_wait(self):
        v, c = self.v, self.c
        self.s_codes()
        if any(on in (FLYING, BOOM) for on in v.on):
            self.timer = 0
            return
        self.s_picture()
        self.timer = (self.timer + 1) & 255
        groups = (c["SC_CODES"] + 3) // 4
        if self.timer >= c["ARENA_WAIT"] and \
                self.sc_made >= groups + c["SC_PICTURE_BYTES"] // 64:
            self.s_begin()

    def s_codes(self):
        """Four of its codes: their lines, their rock (their lines AND
        their masks)."""
        c, t, state = self.c, self.t, self.state_
        groups = (c["SC_CODES"] + 3) // 4
        if self.sc_made >= groups:
            return
        first = 4 * self.sc_made
        self.sc_made += 1
        for k in range(first, min(first + 4, c["SC_CODES"])):
            code = t["sc_code"][k]
            data = t["sc_chars"][8 * k:8 * k + 8]
            m = t["sc_mask"][k]
            mask = t["sc_mbytes"][8 * m:8 * m + 8]
            state.charset[code * 8:code * 8 + 8] = bytes(data)
            for line in range(8):
                state.rock_lines[line * 256 + code] = \
                    data[line] & mask[line]
        self.count("the SUPER-COMPUTER: four of its codes made")

    def s_picture(self):
        c, state = self.c, self.state_
        groups = (c["SC_CODES"] + 3) // 4
        k = self.sc_made - groups
        if not 0 <= k < c["SC_PICTURE_BYTES"] // 64:
            return
        self.sc_made += 1
        d = self.files["supercomp"]
        at = d["sprite_at"] - c["SPRITES2"] + 64 * k
        state.sprites2[at:at + 64] = bytes(d["pictures"][64 * k:
                                                          64 * k + 64])
        self.count("the SUPER-COMPUTER: a picture of its parts made")

    def s_begin(self):
        """Rows 10-14 rock, the far layer's codes not; no plates yet,
        the turrets' lives, the outer ring's angle; the bar; ENTER."""
        c, t, state = self.c, self.t, self.state_
        self.air_rock = 1
        for code in t["sc_far"]:
            for line in range(8):
                state.rock_lines[line * 256 + code] = 0
        self.sc_pv = [0xFF] * c["SC_MOST"]
        self.sc_tlife = [c["SC_TURRET_LIFE"]] * 4
        self.sc_ang = c["SC_START"] << 8
        self.timer = self.parts = self.sc_mode = 0
        self.part[2] = 0xFF
        self.bar_on()
        self.state = ST_ENTER
        self.count("the SUPER-COMPUTER VARKON comes")

    def s_enter(self):
        c, t, v = self.c, self.t, self.v
        if self.sc_estep == 0:                       # the housing
            if self.sc_hrows < c["SC_HOUSE_ROWS"]:
                self.timer = (self.timer + 1) & 255
                if self.timer >= c["SC_HOUSE_EVERY"]:
                    self.timer = 0
                    self.sc_hrows += 1
                return
            if self.sc_hdrawn >= c["SC_HOUSE_ROWS"]:
                self.sc_estep += 1
            return
        if self.sc_estep == 1:                       # the area
            if self.sc_arows < c["SC_AREA_ROWS"]:
                self.sc_arows += 1
                return
            if self.sc_adrawn < c["SC_AREA_ROWS"] or \
                    self.sc_di < self.sc_dn:
                return
            self.sc_estep += 1
            self.timer = self.sc_count = 0
            return
        if self.sc_estep == 2:                       # its elements
            if self.sc_count < c["SC_ELEMENTS"]:
                self.timer = (self.timer + 1) & 255
                if self.timer >= c["SC_ELEMENT_EVERY"]:
                    self.timer = 0
                    e = t["sc_order"][self.sc_count]
                    self.sc_count += 1
                    self.sc_shown[t["sc_e_byte"][e]] |= t["sc_e_bit"][e]
                self.s_wants()
                return
            self.s_wants()
            if self.sc_di < self.sc_dn or self.sc_want != self.sc_have:
                return
            self.sc_estep += 1
            self.sc_count = 1
            self.timer = 0
            self.count("the SUPER-COMPUTER: its rings, its shell drawn")
            return
        self.s_turn()                                # the plates
        self.s_wants()
        self.timer = (self.timer + 1) & 255
        if self.timer >= c["SC_PLATE_EVERY"]:
            i = self.free_varkon()
            if i is None:
                self.count("the SUPER-COMPUTER: a plate waits for a "
                           "free Varkon")
            else:
                self.timer = 0
                self.sc_pv[self.sc_count] = i
                self.new_part(i, self.kind("PLATE"))
                self.sc_count += 1
                self.count("the SUPER-COMPUTER: a plate of the outer "
                           "ring")
        self.s_plates()
        if self.sc_count < t["sc_places"][0]:
            return
        v.sound("boom")
        self.sc_cyc = 0
        self.sc_fire = t["sc_every"][0]
        self.state = ST_FIGHT
        self.count("the SUPER-COMPUTER: the fight")
        self.s_bar_rings()

    # --- FIGHT: the rings --------------------------------------------

    def s_rings(self):
        if self.sc_cyc:
            self.s_next_ring()
            return
        self.s_turn()
        self.s_plates()
        self.s_wants()
        if not self.sc_t:
            self.s_ring_done()
            return
        self.s_gap_shot()
        self.s_step_lights()
        self.s_bar_rings()

    def s_ring_done(self):
        c = self.c
        self.s_step_lights()
        x = self.sc_ring
        self.count(f"the SUPER-COMPUTER: ring {x} destroyed")
        if x >= 2:
            self.sc_ring = 3
            self.s_wants()
            self.sc_cyc = self.sc_pair = 0
            self.timer = c["SC_PAIR_WAIT"]
            self.state = ST_OPEN
            self.count("the SUPER-COMPUTER: its defences")
            self.s_bar_open()
            return
        self.sc_ring = x + 1
        self.sc_shown[x] = 0
        self.sc_cyc = 1
        self.s_wants()
        self.s_bar_rings()

    def s_next_ring(self):
        t = self.t
        self.s_step_lights()
        self.s_wants()
        x = self.sc_ring
        if self.sc_cyc < 2:
            if self.sc_have[x - 1] or self.sc_di < self.sc_dn:
                self.s_bar_rings()
                return
            hi = ((self.sc_ang >> 8) + 16) & 0xE0
            self.sc_ang = hi << 8
            self.sc_cyc = 2
            self.sc_count = 1
            self.count(f"the SUPER-COMPUTER: ring {x}'s characters gone")
        i = self.free_varkon()
        if i is None:
            self.count("the SUPER-COMPUTER: a plate waits for a free "
                       "Varkon")
            self.s_bar_rings()
            return
        self.sc_pv[self.sc_count] = i
        self.new_part(i, t["sc_plate_kind"][x])
        self.s_plates()
        self.sc_count += 1
        self.count(f"the SUPER-COMPUTER: a plate of ring {x}")
        if self.sc_count >= t["sc_places"][x]:
            self.sc_cyc = 0
            self.sc_fire = t["sc_every"][x]
            self.count(f"the SUPER-COMPUTER: ring {x} turns")
        self.s_bar_rings()

    def s_turn(self):
        t = self.t
        x = self.sc_ring
        speed = t["sc_speed_lo"][x] | t["sc_speed_hi"][x] << 8
        self.sc_ang = (self.sc_ang + speed) & 0xFFFF

    def s_plates(self):
        """Its plates: a destroyed one out of sc_pv, the others at their
        places; sc_t: how many are left."""
        c, t, v = self.c, self.t, self.v
        x = self.sc_ring
        base = (0, 128, 192)[x]
        quarter, mask = ((32, 127), (16, 63), (16, 63))[x]
        most = c["SC_MOST"]
        self.sc_t = 0
        for j in range(1, t["sc_places"][x]):
            i = self.sc_pv[j]
            if i & 0x80:
                continue
            if v.on[i] != FLYING:
                self.sc_pv[j] = 0xFF
                self.count(f"the SUPER-COMPUTER: a plate of ring {x} "
                           "destroyed")
                continue
            self.sc_t += 1
            a = (t["sc_offs"][x * most + j] + (self.sc_ang >> 8)) & 255
            k = a >> 1
            if quarter != 32:
                k >>= 1
            xr = t["sc_cos"][base + k] + c["SC_MIDX"]
            y = t["sc_cos"][base + ((k - quarter) & mask)] + c["SC_MIDY"]
            self.s_place(i, xr, y)

    def s_wants(self):
        """The elements wanted: those shown, less the gap's segments in
        the rings waiting."""
        g = ((((self.sc_ang >> 8) + 16) & 255) >> 5) & 7
        b = ~(1 << g) & 255
        x = self.sc_ring
        self.sc_want = [self.sc_shown[0] & (b if x < 1 else 255),
                        self.sc_shown[1] & (b if x < 2 else 255),
                        self.sc_shown[2]]

    def s_gap_shot(self):
        c, t = self.c, self.t
        d = ((self.sc_ang >> 8) - (c["SC_GAP_LEFT"] -
                                   c["SC_GAP_WINDOW"])) & 255
        if d < 2 * c["SC_GAP_WINDOW"] + 1:
            self.sc_fire = (self.sc_fire - 1) & 255
            if self.sc_fire:
                return
            self.sc_fire = t["sc_every"][self.sc_ring]
            self.s_shoot()
            return
        self.sc_fire = t["sc_every"][self.sc_ring]

    def s_shoot(self):
        """The core's shot through the gaps: fire_entry's way, from the
        core's place."""
        c, t, v = self.c, self.t, self.v
        for j in range(varkon_model.ESHOTS):
            if not v.s_on[j]:
                break
        else:
            self.count("the SUPER-COMPUTER's shot: no free place")
            return
        v.sound("plasma")
        entry = c["POD_FAN_FIRST"] + 16
        xr = c["SC_MIDX"] + 128
        v.s_on[j] = 1
        v.s_x[j] = ((xr + varkon_model.signed8(t["fire_dx"][entry]))
                    & 0xFFFF) << 8
        y = (c["SC_CORE_Y"] + t["fire_dy"][entry]) & 255
        v.s_y[j] = y << 8
        v.s_vx[j] = varkon_model.signed8(t["fire_vx"][entry]) << 8
        vy = t["fire_vyl"][entry] | t["fire_vyh"][entry] << 8
        if t["fire_aim"][entry]:
            if y + c["AIM_DEAD"] < v.ship.y:
                vy = c["AIM_VY"]
            elif v.ship.y + c["AIM_DEAD"] < y:
                vy = -c["AIM_VY"] & 0xFFFF
        v.s_vy[j] = vy
        self.count("the SUPER-COMPUTER's core fires through the gaps")
        if not v.place_shot(j):
            v.s_on[j] = 0
            v.objs[varkon_model.ENEMIES + j] = varkon_model.NONE

    # --- the bar (every fourth frame) --------------------------------

    def s_bar_set(self, total):
        self.bar_want = self.t["sc_bar_of"][total >> 2]

    def s_bar_rings(self):
        t, v = self.t, self.v
        if v.anim & 3:
            return
        x = self.sc_ring
        if self.sc_cyc:
            total = t["sc_full_lo"][x] | t["sc_full_hi"][x] << 8
        else:
            total = t["sc_rest_lo"][x] | t["sc_rest_hi"][x] << 8
            for j in range(1, t["sc_places"][x]):
                i = self.sc_pv[j]
                if not i & 0x80:
                    total += v.life[i]
        self.s_bar_set(total & 0xFFFF)

    def s_bar_open(self):
        if self.v.anim & 3:
            return
        self.s_bar_set(self.c["SC_CORE_LIFE"] + sum(self.sc_tlife))

    def s_bar_core(self):
        if self.v.anim & 3:
            return
        self.s_bar_set(self.v.life[self.part[2]])

    # --- OPEN: the defences ------------------------------------------

    def s_defences(self):
        c, t, v = self.c, self.t, self.v
        self.s_step_lights()
        self.s_tcheck()
        if self.sc_cyc >= 4:
            self.s_opening()
            return
        if self.sc_tgone == 0x0F:
            self.sc_cyc = 4
            self.timer = c["SC_CORE_WAIT"]
            self.count("the SUPER-COMPUTER's turrets all destroyed")
            self.s_bar_open()
            return
        if self.sc_cyc == 0:                         # the wait
            self.timer = (self.timer - 1) & 255
            if self.timer:
                self.s_bar_open()
                return
            if not self.s_pair_on():
                self.timer = (self.timer + 1) & 255
                self.count("the SUPER-COMPUTER's turrets wait for free "
                           "Varkon")
                self.s_bar_open()
                return
            self.sc_slide = 0
            self.sc_cyc = 1
            self.s_tplace()
            self.count(f"the SUPER-COMPUTER's pair {self.sc_pair} comes "
                       "out")
            self.s_bar_open()
            return
        if self.sc_cyc == 1:                         # out
            if not self.sc_tlive:
                self.s_next_pair()
                self.s_bar_open()
                return
            self.sc_slide += 1
            self.s_tplace()
            if self.sc_slide < c["SC_SLIDES"] - 1:
                self.s_bar_open()
                return
            self.sc_cyc = 2
            self.timer = c["SC_TURRET_OUT"]
            for y in range(3, -1, -1):
                if self.sc_tlive >> y & 1:
                    v.fire[self.sc_tv[y]] = t["sc_fan_first"][y & 1]
            self.count("the SUPER-COMPUTER's turrets out")
            self.s_bar_open()
            return
        if self.sc_cyc == 2:                         # their fans
            if not self.sc_tlive:
                self.s_next_pair()
                self.s_bar_open()
                return
            self.s_fans()
            self.timer = (self.timer - 1) & 255
            if not self.timer:
                self.sc_cyc = 3
                self.count("the SUPER-COMPUTER's turrets go back in")
            self.s_bar_open()
            return
        if not self.sc_tlive:                        # back in
            self.s_next_pair()
            self.s_bar_open()
            return
        self.sc_slide -= 1
        self.s_tplace()
        if self.sc_slide:
            self.s_bar_open()
            return
        for y in range(3, -1, -1):
            if self.sc_tlive >> y & 1:
                v.on[self.sc_tv[y]] = FREE
                self.count("a turret of the SUPER-COMPUTER back in")
        self.sc_tlive = 0
        self.s_next_pair()
        self.s_bar_open()

    def s_opening(self):
        c, v = self.c, self.v
        if self.sc_cyc == 4:
            self.timer = (self.timer - 1) & 255
            if self.timer:
                self.s_bar_open()
                return
            self.sc_shown[2] &= 0xFE
            self.s_wants()
            self.sc_cyc = 5
            self.timer = c["SC_CORE_ANIM"]
            self.count("the SUPER-COMPUTER's shell opens")
            self.s_bar_open()
            return
        if self.sc_have[2] or self.sc_di < self.sc_dn:
            self.s_bar_open()
            return
        self.timer = (self.timer - 1) & 255
        if self.timer:
            self.s_bar_open()
            return
        i = self.free_varkon()
        if i is None:
            self.timer = (self.timer + 1) & 255
            self.count("the SUPER-COMPUTER's core waits for a free Varkon")
            self.s_bar_open()
            return
        self.part[2] = i
        self.new_part(i, self.kind("SCCORE"))
        self.s_place(i, self.part_x + c["SC_CORE_DX"], c["SC_CORE_Y"])
        self.parts |= 4
        self.sc_way = c["SC_FIRST_WAY"]
        self.sc_wt = c["SC_TURN_EVERY"]
        self.sc_ft = c["SC_FAN_EVERY"]
        self.state = ST_CORE
        self.count("the SUPER-COMPUTER's core uncovered")
        self.s_bar_core()

    def s_tcheck(self):
        v = self.v
        for y in range(3, -1, -1):
            if not self.sc_tlive >> y & 1:
                continue
            i = self.sc_tv[y]
            if v.on[i] != FLYING:
                self.sc_tgone |= 1 << y
                self.sc_tlive ^= 1 << y
                self.sc_tlife[y] = 0
                self.count(f"turret {y} of the SUPER-COMPUTER destroyed")
            else:
                self.sc_tlife[y] = v.life[i]

    def s_next_pair(self):
        t = self.t
        self.sc_pair ^= 1
        bits = t["sc_pair_bits"][self.sc_pair]
        if self.sc_tgone & bits == bits:
            self.sc_pair ^= 1
        self.sc_cyc = 0
        self.timer = self.c["SC_PAIR_WAIT"]

    def s_pair_on(self):
        v = self.v
        first = 2 * self.sc_pair
        wanted = [y for y in (first, first + 1)
                  if not self.sc_tgone >> y & 1]
        if sum(1 for on in v.on if on == FREE) < len(wanted):
            return False
        for y in wanted:
            i = self.free_varkon()
            self.sc_tv[y] = i
            self.sc_tlive |= 1 << y
            self.new_part(i, self.kind("STURRET"))
            v.life[i] = self.sc_tlife[y]
        return True

    def s_tplace(self):
        c, t = self.c, self.t
        for y in range(3, -1, -1):
            if not self.sc_tlive >> y & 1:
                continue
            k = t["sc_tfirst"][y] + self.sc_slide
            self.s_place(self.sc_tv[y], t["sc_slide_x"][k] + c["SC_MIDX"],
                         t["sc_slide_y"][k])

    def s_fans(self):
        c, v = self.c, self.v
        for y in range(3, -1, -1):
            if not self.sc_tlive >> y & 1:
                continue
            i = self.sc_tv[y]
            v.fire[i] = (v.fire[i] - 1) & 255
            if v.fire[i]:
                continue
            v.fire[i] = c["SC_FAN_PERIOD"]
            way = self.s_aim(i)
            first = c["POD_FAN_FIRST"] + way - 1
            for e in range(first, first + 3):
                v.shoot_entry(i, e)
            self.count(f"a turret of the SUPER-COMPUTER fires its fan, "
                       f"way {way}")

    def s_aim(self, i):
        """Varkon i's way to the ship (4-12)."""
        v, ship = self.v, self.state_.ship
        sx = (ship.x + 24) & 0xFFFF
        d = ((v.x[i] >> 8) - sx) & 0xFFFF
        if d & 0x8000:
            q = 8
        elif d >> 8:
            q = 255
        else:
            q = max(d, 8)
        sy, ey = ship.y & 255, (v.y[i] >> 8) & 255
        if sy >= ey:
            p, higher = sy - ey, 0
        else:
            p, higher = ey - sy, 1
        k = 0
        if not p < (q >> 2) - (q >> 4):
            k = 1
            if not p < (q >> 1) + (q >> 3) + (q >> 5):
                k = 2
                if q < 104 and not p < (q >> 1) + q:
                    k = 3
                    if q < 32 and not p < 5 * q:
                        k = 4
        return 8 + k if higher else 8 - k

    # --- CORE ----------------------------------------------------------

    def s_core(self):
        c, v = self.c, self.v
        self.s_step_lights()
        i = self.part[2]
        if v.on[i] != FLYING:
            self.count("the SUPER-COMPUTER's core destroyed")
            self.dies()
            return
        rage = 0
        if v.life[i] < c["SC_RAGE_LIFE"] + 1:
            v.own[i] = c["SC_RAGE_OWN"]
            rage = 1
        self.sc_wt = (self.sc_wt - 1) & 255
        if not self.sc_wt:
            self.sc_wt = (c["SC_TURN_EVERY"], c["SC_TURN_RAGE"])[rage]
            self.sc_way = (self.sc_way - 1) & 15
        self.sc_ft = (self.sc_ft - 1) & 255
        if not self.sc_ft:
            self.sc_ft = (c["SC_FAN_EVERY"], c["SC_FAN_RAGE"])[rage]
            if c["SC_FAN_LO"] <= self.sc_way <= c["SC_FAN_HI"]:
                first = c["POD_FAN_FIRST"] + self.sc_way - 1
                for e in range(first, first + 3):
                    v.shoot_entry(i, e)
                self.count(f"the SUPER-COMPUTER's core fires its fan, "
                           f"way {self.sc_way}" +
                           (", raging" if rage else ""))
        self.s_bar_core()

    # --- CHAIN -----------------------------------------------------

    def s_chain(self):
        c, t, v = self.c, self.t, self.v
        self.timer = (self.timer + 1) & 255
        if self.timer < c["CHAIN_EVERY"]:
            return
        self.timer = 0
        i = self.free_varkon()
        if i is not None:
            self.set_pri(i, 2)
            v.on[i] = BOOM
            v.kind[i] = self.kind("SCCORE")
            v.left[i] = v.flash[i] = v.cap[i] = 0
            k = self.chain_k
            self.s_place(i, self.part_x + t["sc_chain_dx"][k],
                         t["sc_chain_y"][k])
            self.count("a fireball of the chain")
        else:
            self.count("the chain: no free Varkon")
        v.sound("explode")
        self.flash = 3
        self.paint(self.state_, 1)
        self.chain_k += 1
        if self.chain_k >= c["CHAIN_COUNT"]:
            self.state = ST_WRECK
