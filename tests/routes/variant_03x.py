"""(D.3) The route of break 03x, the ninth bit: the ship flown to the
right from its start, past screen x 232, where its x register goes
past 255 and needs the ninth bit ($d010). No aids, no captures but
the break's."""


def use(step_routes, verify_game):
    verify_game.ROUTE = [(400, step_routes.R, 0,
                          "right, past the x register's 255")]
    verify_game.POKES, verify_game.LIFE_POKES = {}, {}
    verify_game.SHIELD_POKES, verify_game.BLINK_POKES = set(), set()
    verify_game.LEVEL_POKES, verify_game.SHIP_POKES = {}, {}
    verify_game.CAPTURES = []
