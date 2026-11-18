"""A canvas of C64 multicolour pixels, and the drawing tools.

The playfield of Starbraze II is drawn in the C64's multicolour
character mode: a pixel is two screen pixels wide, so a character
cell is 4 x 8 pixels here and the 40 x 22 cells of the playfield are
160 x 176 pixels. Each pixel holds a C64 colour number (0-15).

In a multicolour cell the pixels can take four colours: the
background ($d021), the two shared colours ($d022, $d023) and one
colour of the cell's own, 0-7, from the colour RAM. The drawing tools
do not know the rule: build_assets.py checks every cell.
"""

WIDTH, HEIGHT = 160, 176          # multicolour pixels
CELL_W, CELL_H = 4, 8

# C64 colour numbers, by name.
BLACK, WHITE, RED, CYAN, PURPLE, GREEN, BLUE, YELLOW = range(8)
ORANGE, BROWN, PINK, DARK_GREY, GREY, LIGHT_GREEN = range(8, 14)
LIGHT_BLUE, LIGHT_GREY = 14, 15


class Canvas:
    def __init__(self, colour=BLACK, width=WIDTH, height=HEIGHT):
        self.width, self.height = width, height
        self.pixels = [[colour] * width for _ in range(height)]
        # cells drawn as hi-res characters: (col, row) -> (bytes, colour)
        self.hires = {}
        # cells that are solid ground for the ship (col, row)
        self.solid = set()

    def plot(self, x, y, colour):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = colour

    def get(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return BLACK

    def rect(self, x0, y0, x1, y1, colour):
        """Fill the rectangle from (x0, y0) to (x1, y1), inclusive."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.plot(x, y, colour)

    def hline(self, x0, x1, y, colour):
        self.rect(min(x0, x1), y, max(x0, x1), y, colour)

    def vline(self, x, y0, y1, colour):
        self.rect(x, min(y0, y1), x, max(y0, y1), colour)

    def line(self, x0, y0, x1, y1, colour):
        """A straight line, one pixel at a time (Bresenham)."""
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        error = dx + dy
        while True:
            self.plot(x0, y0, colour)
            if x0 == x1 and y0 == y1:
                return
            twice = 2 * error
            if twice >= dy:
                error += dy
                x0 += sx
            if twice <= dx:
                error += dx
                y0 += sy

    def ellipse(self, cx, cy, rx, ry, colour, top_only=False):
        """Fill an ellipse; rx in multicolour pixels, ry in lines."""
        for y in range(cy - ry, cy + (0 if top_only else ry) + 1):
            for x in range(cx - rx, cx + rx + 1):
                dx = (x - cx) / (rx + 0.5)
                dy = (y - cy) / (ry + 0.5)
                if dx * dx + dy * dy <= 1.0:
                    self.plot(x, y, colour)

    def blit(self, x0, y0, rows, palette):
        """Copy a drawing: rows of letters, palette letter -> colour.
        '.' leaves the canvas as it is."""
        for dy, line in enumerate(rows):
            for dx, letter in enumerate(line):
                if letter != ".":
                    self.plot(x0 + dx, y0 + dy, palette[letter])

    def replace(self, x0, y0, x1, y1, old, new):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if self.get(x, y) == old:
                    self.plot(x, y, new)

    def mark_solid(self, x0, y0, x1, y1):
        """The cells under this rectangle are solid ground."""
        for row in range(max(0, y0 // CELL_H), min(21, y1 // CELL_H) + 1):
            for col in range(max(0, x0 // CELL_W),
                             min(39, x1 // CELL_W) + 1):
                self.solid.add((col, row))

    def cell_colours(self, col, row):
        return {self.pixels[row * CELL_H + y][col * CELL_W + x]
                for y in range(CELL_H) for x in range(CELL_W)}

    def cell_empty(self, col, row):
        return (col, row) not in self.hires and \
            self.cell_colours(col, row) == {BLACK}
