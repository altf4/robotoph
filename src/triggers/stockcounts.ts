import { FrameEntryType } from '@slippi/slippi-js';
const _ = require("lodash");

// Returns the clip (dir) to play, or null if no clip to play
export function StockCount (frameEntry: FrameEntryType): string | null {
  var clip: string = null
  var highStock: number = 0
  var lowStock: number = 0
  var onHalo: boolean = false

  _.forEach(frameEntry.players, (player: any, port: number) => {
    if (player !== null) {
      if (player.post.stocksRemaining > highStock) {
        lowStock = highStock;
        highStock = player.post.stocksRemaining;
      } else {
        lowStock = player.post.stocksRemaining;
      }

      // HALO DESCENT
      if (player.post.actionStateId === 12) {
        onHalo = true;
      }
    }
  });

  if (onHalo) {
    clip = "clips/stockcounts/" + highStock.toString() + "-" + lowStock.toString() + "/"
  }
  return clip
}
