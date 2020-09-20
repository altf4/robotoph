# RoboToph

Auto-commentary program for your Melee netplay matches, powered by libmelee.

## Nice Back Air!

RoboToph is a trigger-based system that plays audio clips when defined in-game events occur. For example, a clip can play "You hate to see it..." when someone misses a ledge dash, or "Nice back air" when someone gets a kill off a bair.

## How to Add a Clip

Simply record an audio clip (in OGG or lossless WAV format) and drop it in the right folder in `clips/`. RoboToph will pick a clip from the right folder at random during the game.

For example, you can record a clip saying `This is looking like a 4-stock!` and then just drop it in `clips/stockcounts/4-1/`.

That's all!

## How to Add a Trigger

This takes a minor amount of Python programming, but not much.

What you need to do is make a new Python file in `triggers/`. Define a class in it that has a `self.check(gamestate)` function.

Each frame of the game, your `check()` function will be called, with the current `libmelee` gamestate passed in as an argument. So you can inspect that for whatever conditions you want and play audio clips.

Just check out existing trigger files for examples, it's quite simple.
