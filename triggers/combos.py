"""Triggers based on combos"""

from os import listdir
from os.path import isfile, join
import random

import melee
import pygame

class Combos:
    def __init__(self):
        self.channel = pygame.mixer.Channel(0)
        # string -> list of pygame sounds
        self.sounds = {}
        self.categories = ["medium", "big"]
        self._damage_last_frame = 0
        for category in self.categories:
            self._collect_sounds(category)

    def check(self, gamestate, stats):
        # Perform all the checks here!
        for category in self.categories:
            if self._is_combo(gamestate, category, stats):
                sounds = self.sounds[category]
                if sounds:
                    self.channel.queue(random.choice(sounds))
        if stats.current_combo:
            self._damage_last_frame = stats.current_combo["damage"]
        else:
            self._damage_last_frame = 0

    def _is_combo(self, gamestate, category, stats):
        """Check to see if we have entered the given combo state

        category (string): One of the string categories in self.categories
        """
        # Only relevant for 1v1
        if len(gamestate.player) != 2:
            return False

        if category == "huge":
            if stats.current_combo and stats.current_combo["damage"] > 60:
                if self._damage_last_frame <= 60:
                    return True
        if category == "big":
            if stats.current_combo:
                if 40 < stats.current_combo["damage"] < 60 and self._damage_last_frame <= 40:
                    return True
        if category == "medium":
            if stats.current_combo:
                if 20 < stats.current_combo["damage"] < 40 and self._damage_last_frame <= 20:
                    return True
        return False

    def _collect_sounds(self, category):
        """Collect all the available clips for a given category"""
        self.sounds[category] = []
        path = "clips/combos/" + category + "/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.sounds[category].append(pygame.mixer.Sound(path+file))
