# The level's song again

Step 17 (`chain/17-complete`), where it breaks: a mistake made on
purpose.

F1-F7 start the level's song again, as in steps 07-16, where the
complete game keeps the song that plays.

## What changes

In `game/src/player.asm`:

```
        jmp mode_set            ; the song it plays
```

becomes

```
        jmp sound_set           ; the song it plays
```

## What you see

(To be heard.) An F key pushed while the bosses' theme plays brings the
canyons' theme back: the boss is fought to the level's song. Nothing to
see: the capture is of the fight, 4 frames after the test stopped.

## Why

In steps 07-16 a new sound mode starts the level's song again
(`sound_set`: the level's song into `mus_song`, then `mode_set`). The
complete game has songs that are not the level's, the title's theme, the
bosses', the jingles, so its F keys go straight to `mode_set` and keep
the song that plays. With `jmp sound_set` the steps' way is back. The
test compares the sound with the model's at every frame: it stops at
frame 5 992, the first F key in the SIEGE CRAWLER's fight (song 0, the
canyons' theme, where the model has song 2, the bosses').

## How the test stops it

The test of step 17 (`tests/verify_game.py --step 17 --fail-fast`) fails
first at "the sound as the model: the SID's copy, the voices of the
music, the effects": frame 5992: mus_song+0 0 instead of 2, v_list_lo+0
91 instead of 140, v_list_lo+1 103 instead of 174, v_list_lo+2 177
instead of 208, v_list_hi+0 241 instead of 135, v_list_hi+1 241 instead
of 135.

The route goes on 4 frames, then the capture:
`evidence/level-song-again.png`.

To repair it, undo the change above.
