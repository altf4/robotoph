"""Triggers around edgeguarding"""

from os import listdir
from os.path import isfile, join
import random

import melee
import pygame

class EdgeGuardTrigger:
    def __init__(self):
        self.channel = pygame.mixer.Channel(0)
        self.jumpstolen_sounds = []
        self.player = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

        path = "clips/edgeguard/jumpstolen/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.jumpstolen_sounds.append(pygame.mixer.Sound(path+file))

    def check(self, gamestate):
        # Perform all the checks here!

        # Only works on the 6 tournament stages
        if gamestate.stage not in [melee.Stage.POKEMON_STADIUM, melee.Stage.FINAL_DESTINATION,
                                   melee.Stage.BATTLEFIELD, melee.Stage.DREAMLAND,
                                   melee.Stage.FOUNTAIN_OF_DREAMS, melee.Stage.YOSHIS_STORY]:
            return

        if self._jump_stolen(gamestate):
            if self.jumpstolen_sounds:
                self.channel.queue(random.choice(self.jumpstolen_sounds))

    def _jump_stolen(self, gamestate):
        """Check to see if someone got hit out of their jump, off stage

        We call it missed when a player goes through these steps in order:
            1) off stage and uses double jump
            2) gets hit while in jump animation

            Phase 0 is N/A
        """
        for port, player in gamestate.player.items():
            if player.on_ground:
                self.player[port] = 0
                continue

            # Is the player off the stage
            if abs(player.x) < melee.EDGE_POSITION[gamestate.stage]:
                self.player[port] = 0
                continue

            if player.action in [melee.Action.JUMPING_ARIAL_FORWARD,
                                 melee.Action.JUMPING_ARIAL_BACKWARD]:
                self.player[port] = 1
                continue

            # Must be in phase 2 or later to proceed
            if self.player[port] >= 1:
                if player.hitstun_frames_left > 0 and player.jumps_left == 0:
                    self.player[port] = 0
                    return True
        return False
