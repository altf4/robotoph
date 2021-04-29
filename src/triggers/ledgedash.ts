import { FrameEntryType } from '@slippi/slippi-js';
const _ = require("lodash");

var playerStates: number[] = [0, 0, 0, 0];

// Returns the clip (dir) to play, or null if no clip to play
export function LedgeDash(frameEntry: FrameEntryType): string | null {
  // To be a missed ledge dash, a character needs to
  //  1) Hang on edge
  //  2) Airdodge
  //  3) Dead fall
  //  Landing on stage puts the player in state 0

  var clip: string = null
  _.forEach(frameEntry.players, (player: any, port: number) => {
    if (player !== null) {

      var state = playerStates[port];
      // On ground
      if (player.post.isAirborne === 0) {
        playerStates[port] = 0;
      }
      // Hanging on edge
      if (player.post.actionStateId === 0xFD) {
        playerStates[port] = 1;
      }
      // Airdodge
      if ((state === 1) && (player.post.actionStateId === 0xEC)) {
        playerStates[port] = 2;
      }
      // Dead fall
      if ((state === 2) && (player.post.actionStateId === 0x23)) {
        playerStates[port] = 3;
        clip = "clips/ledgedash/missed/"
      }
    }
  });
  return clip
}
