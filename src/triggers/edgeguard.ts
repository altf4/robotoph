import { FrameEntryType } from '@slippi/slippi-js';
const _ = require("lodash");

var playerStates: number[] = [0, 0, 0, 0];

// Returns the clip (dir) to play, or null if no clip to play
export function EdgeGuard(frameEntry: FrameEntryType): string | null {
  // Jump stolen
  //   If someone is hit out of their last double-jump while off stage
  var clip: string = null
  _.forEach(frameEntry.players, (player: any, port: number) => {
    if (player !== null) {

      var state = playerStates[port];
      // On ground
      if (player.post.isAirborne) {
        playerStates[port] = 0;
      }
      // Double-jumping off stage
      if ((player.post.actionStateId === 0x1B || player.post.actionStateId === 0x1C) && (Math.abs(player.post.positionX) > 80)) {
        playerStates[port] = 1;
      }
      // Gets damaged from jump
      if ((state === 1) && (0x4B <= player.post.actionStateId && player.post.actionStateId <= 0x5B) && (player.post.jumpsRemaining === 0)) {
        playerStates[port] = 2;
        clip = "clips/edgeguard/jumpstolen/"
      }
    }
  });

  // EdgeGuard opportunity
  _.forEach(frameEntry.players, (player: any, port: number) => {
    if (player !== null) {

      // Flying away from stage from a hit
      if (player.post.isAirborne && (Math.abs(player.post.positionX) > 80) &&
          (0.1 < Math.abs(player.post.selfInducedSpeeds.attackX) && Math.abs(player.post.selfInducedSpeeds.attackX) < 4)) {
        clip = "clips/edgeguard/opportunity/"
      }
    }
  });

  return clip
}
