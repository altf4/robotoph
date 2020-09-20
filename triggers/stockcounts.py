"""Triggers based on stock count"""

from os import listdir
from os.path import isfile, join
import random

import melee
import pygame

class StockCountTrigger:
    def __init__(self):
        self.channel =  pygame.mixer.Channel(0)
        # string -> list of pygame sounds
        self.sounds = {}
        self.categories = ["1-1", "2-1", "2-2", "3-1", "3-2", "3-3", "4-1", "4-2", "4-3"]
        for category in self.categories:
            self._collect_sounds(category)

    def check(self, gamestate):
        # Perform all the checks here!
        for category in self.categories:
            if self._spawning_with(gamestate, category):
                sounds = self.sounds[category]
                if sounds:
                    self.channel.queue(random.choice(sounds))

    def _spawning_with(self, gamestate, stock_count):
        """Check to see if the stock count just became the given count

        stock_count (string): One of the string categories in self.categories
        """
        # Only relevant for 1v1
        if len(gamestate.player) != 2:
            return False

        target_stocks = []
        for part in stock_count.split("-"):
            target_stocks.append(int(part))

        target_stocks = [target_stocks, target_stocks[::-1]]

        stocks = []
        on_halo_platform = False
        for _, player in gamestate.player.items():
            stocks.append(player.stock)
            if player.action == melee.Action.ON_HALO_DESCENT and player.action_frame == 1:
                on_halo_platform = True
        if on_halo_platform and stocks in target_stocks:
            return True

        return False

    def _collect_sounds(self, category):
        """Collect all the available clips for a given category"""
        self.sounds[category] = []
        path = "clips/stockcounts/" + category + "/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.sounds[category].append(pygame.mixer.Sound(path+file))
