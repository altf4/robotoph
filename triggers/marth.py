"""Marth-specific triggers"""

from os import listdir
from os.path import isfile, join
import random

import melee
import pygame

class MarthTrigger:
    def __init__(self):
        self.channel = pygame.mixer.Channel(0)
        self.tipper_sounds = []

        path = "clips/character_specific/marth/monster_tipper/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.tipper_sounds.append(pygame.mixer.Sound(path+file))

    def check(self, gamestate):
        # Perform all the checks here!
        if not self.channel.get_busy() and self._monster_tipper(gamestate):
            if self.tipper_sounds:
                self.channel.queue(random.choice(self.tipper_sounds))

    def _monster_tipper(self, gamestate):
        """Did we just see a monster tipper?
        """
        # Two conditions need to be true. Marth fsmashing and opponent with high
        halfway_there = False
        for port, player in gamestate.player.items():
            if player.character == melee.Character.MARTH and \
                player.action == melee.Action.FSMASH_MID:
                if halfway_there:
                    return True
                else:
                    halfway_there = True
            if player.hitstun_frames_left > 75:
                if halfway_there:
                    return True
                else:
                    halfway_there = True
        return False
