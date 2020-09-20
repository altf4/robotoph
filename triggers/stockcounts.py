"""Triggers based on stock count"""

from os import listdir
from os.path import isfile, join
import random

import melee
import pygame

class StockCountTrigger:
    def __init__(self):
        self.four_stock = []
        self.last_stock = []
        self.two_one = []
        self.two_two = []
        self.three_one = []
        self.three_two = []
        self.three_three = []
        self.four_two = []
        self.four_three = []

        path = "clips/stockcounts/4-1/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.four_stock.append(pygame.mixer.Sound(path+file))
        path = "clips/stockcounts/1-1/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.last_stock.append(pygame.mixer.Sound(path+file))
        path = "clips/stockcounts/2-1/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.two_one.append(pygame.mixer.Sound(path+file))
        path = "clips/stockcounts/2-2/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.two_two.append(pygame.mixer.Sound(path+file))
        path = "clips/stockcounts/3-1/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.three_one.append(pygame.mixer.Sound(path+file))
        path = "clips/stockcounts/3-2/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.three_two.append(pygame.mixer.Sound(path+file))
        path = "clips/stockcounts/3-3/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.three_three.append(pygame.mixer.Sound(path+file))
        path = "clips/stockcounts/4-2/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.four_two.append(pygame.mixer.Sound(path+file))
        path = "clips/stockcounts/4-3/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.four_three.append(pygame.mixer.Sound(path+file))

    def check(self, gamestate):
        # Perform all the checks here!
        if self._spawning_with(gamestate, [[4,1], [1,4]]):
            if self.four_stock:
                sound = self.four_stock[random.randint(0, len(self.four_stock)-1)]
                pygame.mixer.Sound.play(sound)

        if self._spawning_with(gamestate, [[1,1]]):
            if self.last_stock:
                sound = self.last_stock[random.randint(0, len(self.last_stock)-1)]
                pygame.mixer.Sound.play(sound)

        if self._spawning_with(gamestate, [[2,1], [1,2]]):
            if self.two_one:
                sound = self.two_one[random.randint(0, len(self.two_one)-1)]
                pygame.mixer.Sound.play(sound)

        if self._spawning_with(gamestate, [[2,2]]):
            if self.two_two:
                sound = self.two_two[random.randint(0, len(self.two_two)-1)]
                pygame.mixer.Sound.play(sound)

        if self._spawning_with(gamestate, [[3,1], [1,3]]):
            if self.three_one:
                sound = self.three_one[random.randint(0, len(self.three_one)-1)]
                pygame.mixer.Sound.play(sound)

        if self._spawning_with(gamestate, [[3,2], [2,3]]):
            if self.three_two:
                sound = self.three_two[random.randint(0, len(self.three_two)-1)]
                pygame.mixer.Sound.play(sound)

        if self._spawning_with(gamestate, [[3,3]]):
            if self.three_three:
                sound = self.three_three[random.randint(0, len(self.three_three)-1)]
                pygame.mixer.Sound.play(sound)

        if self._spawning_with(gamestate, [[4,2], [2,4]]):
            if self.four_two:
                sound = self.four_two[random.randint(0, len(self.four_two)-1)]
                pygame.mixer.Sound.play(sound)

        if self._spawning_with(gamestate, [[4,3], [3,4]]):
            if self.four_three:
                sound = self.four_three[random.randint(0, len(self.four_three)-1)]
                pygame.mixer.Sound.play(sound)

    def _spawning_with(self, gamestate, stock_count):
        """Check to see if the stock count just became the given count"""
        # Only relevant for 1v1
        if len(gamestate.player) != 2:
            return False
        stocks = []
        on_halo_platform = False
        for _, player in gamestate.player.items():
            stocks.append(player.stock)
            if player.action == melee.Action.ON_HALO_DESCENT and player.action_frame == 1:
                on_halo_platform = True
        if on_halo_platform and stocks in stock_count:
            return True

        return False
