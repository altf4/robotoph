"""Triggers around ledge dashes"""

from os import listdir
from os.path import isfile, join
import random

import melee
import pygame

class LedgeDashTrigger:
    def __init__(self):
        self.channel = pygame.mixer.Channel(0)
        self.player = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        """What phase of the ledge dash the player is in"""

        self.missed_ledgedash = []

        path = "clips/ledgedash/missed/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.missed_ledgedash.append(pygame.mixer.Sound(path+file))

    def check(self, gamestate):
        # Perform all the checks here!
        if self._is_missed(gamestate):
            if self.missed_ledgedash:
                self.channel.queue(random.choice(self.missed_ledgedash))

    def _is_missed(self, gamestate):
        """Check to see if someone just missed a ledge dash

        We call it missed when a player goes through these steps in order:
            1) edge catch/hanging
            2) falling/jumping
            3) air dodge
            4) dead falls below -5 without landing

            Phase 0 is "not ledge dashing"
        """
        for port, player in gamestate.player.items():
            if player.on_ground:
                self.player[port] = 0
                continue
            if player.action in [melee.Action.EDGE_CATCHING, melee.Action.EDGE_HANGING]:
                self.player[port] = 1
                continue
            # Must be in phase 1 or later to proceed
            if self.player[port] >= 1:
                if player.action in [melee.Action.FALLING,
                                     melee.Action.FALLING_FORWARD,
                                     melee.Action.FALLING_BACKWARD]:
                    self.player[port] = 2
                    continue
                # Must be in phase 2 or later to proceed
                if self.player[port] >= 2:
                    if player.action in [melee.Action.AIRDODGE]:
                        self.player[port] = 3
                        continue
                    # Must be in phase 3 or later to proceed
                    if self.player[port] >= 3:
                        if player.action in [melee.Action.DEAD_FALL] and player.y < -5:
                            self.player[port] = 0
                            return True
        return False
