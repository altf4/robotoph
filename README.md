# RoboToph

Auto-commentary program for your Melee netplay matches.

## Nice Back Air!

RoboToph is a trigger-based system that plays audio clips when defined in-game events occur. For example, a clip can play "You hate to see it..." when someone misses a ledge dash, or "Nice back air" when someone gets a kill off a bair.

## How to Use

Install the dependencies:

`npm install`

Start your Slippi dolphin, and then run:

`npm start`

That's it.

## How to Add a Clip

Simply record an audio clip (in OGG or lossless WAV format) and drop it in the right folder in `clips/`. RoboToph will pick a clip from the right folder at random during the game.

For example, you can record a clip saying `This is looking like a 4-stock!` and then just drop it in `clips/stockcounts/4-1/`.

That's all!
