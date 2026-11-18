"""The levels' data, packed: an LZ with its numbers in bits (Elias
gamma), that the program unpacks with a short routine (level.asm,
lz_unpack). (Tokens of whole bytes would make it a fourth bigger.)

A packed stream mixes bits and bytes. The bits come from bit bytes, read
from the stream when the reader needs a bit and has none left, highest
bit first; the other bytes (literals, an offset's low part) are read
from the stream when they are needed. A number n (1-255) in gamma: as
many 0 bits as n has bits after its highest, then n's bits from the
highest. The tokens:

  0, gamma(k), k bytes        k literals (1-255), copied as they are;
  1, gamma(h + 1), a byte l,  a match: L bytes (2-255) copied from those
     gamma(L - 1)             already unpacked, `offset` back, where
                              offset - 1 = 128 h + l (l 0-127; up to
                              4 096 back).
After literals a match always comes: its 1 is not written. A match may
overlap what it writes (offset smaller than its length): the copy goes
a byte at a time, from the first. The stream has no end mark: the
program stops when it has written the stream's length.

pack() finds the shortest stream (in bits), going back from the end:
at each place the best of any run of literals or any match there (the
latest places with the same two bytes, the longest of each offset's
128s).
"""

MAX_RUN = 255                  # literals in a run, a match's length
WINDOW = 32 * 128              # the farthest offset
CANDIDATES = 512


def gamma_bits(n):
    return 2 * n.bit_length() - 1


def match_bits(offset, length):
    h = (offset - 1) >> 7
    return gamma_bits(h + 1) + 8 + gamma_bits(length - 1)


def matches(data):
    """For each place: [(length, offset)], the longest of each h."""
    n = len(data)
    places, out = {}, []
    for j in range(n):
        key = data[j:j + 2]
        found = {}
        if len(key) == 2:
            for p in reversed(places.get(key, [])[-CANDIDATES:]):
                offset = j - p
                if offset > WINDOW:
                    break
                length = 0
                while (j + length < n and length < MAX_RUN and
                       data[p + length] == data[j + length]):
                    length += 1
                h = (offset - 1) >> 7
                if length >= 2 and found.get(h, (0, 0))[0] < length:
                    found[h] = (length, offset)
            places.setdefault(key, []).append(j)
        out.append(sorted(found.values()))
    return out


def pack(data):
    data = bytes(data)
    n = len(data)
    near = matches(data)
    big = 1 << 60
    # free[j]: the bits from j when any token may come; after[j]: when a
    # match must come (after literals), its 1 not written; at the end 0
    free, after = [big] * (n + 1), [big] * (n + 1)
    free[n] = after[n] = 0
    how_free, how_after = [None] * (n + 1), [None] * (n + 1)
    for j in range(n - 1, -1, -1):
        best, how = big, None
        for length, offset in near[j]:
            for k in range(2, length + 1):
                c = match_bits(offset, k) + free[j + k]
                if c < best:
                    best, how = c, ("match", k, offset)
        after[j], how_after[j] = best, how
        best, how = best + 1, how             # a match: its 1
        for k in range(1, min(MAX_RUN, n - j) + 1):
            c = 1 + gamma_bits(k) + 8 * k + after[j + k]
            if c < best:
                best, how = c, ("literals", k)
        free[j], how_free[j] = best, how
    writer = Writer()
    j, must_match = 0, False
    while j < n:
        how = how_after[j] if must_match else how_free[j]
        if how[0] == "literals":
            k = how[1]
            writer.bit(0)
            writer.gamma(k)
            for b in data[j:j + k]:
                writer.byte(b)
            j += k
            must_match = True
            continue
        _, k, offset = how
        if not must_match:
            writer.bit(1)
        h, low = (offset - 1) >> 7, (offset - 1) & 127
        writer.gamma(h + 1)
        writer.byte(low)
        writer.gamma(k - 1)
        j += k
        must_match = False
    packed = bytes(writer.out)
    assert unpack(packed, n) == data
    return packed


class Writer:
    def __init__(self):
        self.out = bytearray()
        self.at = None                 # the bit byte being filled
        self.left = 0

    def bit(self, b):
        if not self.left:
            self.at = len(self.out)
            self.out.append(0)
            self.left = 8
        self.left -= 1
        self.out[self.at] |= b << self.left

    def gamma(self, n):
        assert 1 <= n <= 255
        bits = n.bit_length()
        for _ in range(bits - 1):
            self.bit(0)
        for k in range(bits - 1, -1, -1):
            self.bit(n >> k & 1)

    def byte(self, b):
        self.out.append(b)


def unpack(packed, length):
    """What the program does: the stream into `length` bytes."""
    out = bytearray()
    state = {"i": 0, "bits": 0, "left": 0}

    def byte():
        b = packed[state["i"]]
        state["i"] += 1
        return b

    def bit():
        if not state["left"]:
            state["bits"], state["left"] = byte(), 8
        state["left"] -= 1
        return state["bits"] >> state["left"] & 1

    def gamma():
        zeros = 0
        while not bit():
            zeros += 1
        n = 1
        for _ in range(zeros):
            n = n << 1 | bit()
        return n

    after_literals = False
    while len(out) < length:
        if not after_literals and not bit():
            for _ in range(gamma()):
                out.append(byte())
            after_literals = True
            continue
        h = gamma() - 1
        offset = (h << 7 | byte()) + 1
        count = gamma() + 1
        for _ in range(count):
            out.append(out[-offset])
        after_literals = False
    assert len(out) == length, "a stream that overruns its length"
    return bytes(out)
