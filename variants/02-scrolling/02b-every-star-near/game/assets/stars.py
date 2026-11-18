"""The stars of the black sky, in three planes of parallax.

The sky is rows 0-9 of the playfield. Its empty cells are not the
blank character 0 but one of three blank characters, one a plane,
drawn in hi-res: their colour in the colour RAM is the colour of the
plane's stars (blue far away, purple, white near). In each row the
stars belong to one plane and lie on one line of the row, with the
same pixel in their cell: so one character, the row's star, draws all
of them. The program moves the star's pixel inside the character and
puts the character in the cells where the stars are, if those cells
are empty sky; rock hides the stars behind it.

A plane moves at a fraction of the camera: 1/8, 1/4, 3/8. The stars
of a row are on a ring of 40 cells (320 pixels): those that leave on
the left come back on the right.
"""

# Planes: (name, colour of the stars, shift of the camera, 1/8 = 3)
PLANES = [("far", 6, "camera / 8"), ("middle", 4, "camera / 4"),
          ("near", 1, "camera * 3 / 8")]

# Rows 0-9: (plane, line of the row 0-7, pixel 0-7, cells of the stars
# on the ring of 40)
ROWS = [
    (2, 2, 5, [4, 19, 33]),
    (2, 5, 1, [11, 26]),
    (2, 1, 3, [1, 15, 30]),
    (2, 6, 6, [8, 22, 37]),
    (2, 3, 2, [17, 34]),
    (2, 6, 0, [5, 20, 28]),
    (2, 1, 4, [12, 25, 39]),
    (2, 4, 7, [2, 31]),
    (2, 2, 1, [9, 23, 36]),
    (2, 5, 3, [6, 18, 29]),
]


def shift(plane, camera):
    """How far the plane has moved, in pixels, at this camera."""
    if plane == 0:
        return camera >> 3
    if plane == 1:
        return camera >> 2
    return (camera >> 2) + (camera >> 3)
