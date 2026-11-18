"""(D.3) The route of break 16x, a pause that flickers: the step's
route (the 1.0's) with SPACE held three frames at the pause, where it
is pushed for one."""


def use(step_routes, verify_game):
    route = verify_game.ROUTE
    at = next(k for k, entry in enumerate(route)
              if entry[3].startswith("SPACE: the pause"))
    _, joy, keys, what = route[at]
    route[at] = (3, joy, keys, what + " (held three frames)")
