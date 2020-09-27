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
        self.opportunity_sounds = []
        self.player = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        self.opportunity_state = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

        path = "clips/edgeguard/jumpstolen/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.jumpstolen_sounds.append(pygame.mixer.Sound(path+file))

        path = "clips/edgeguard/opportunity/"
        for file in [f for f in listdir(path) if isfile(join(path, f))]:
            self.opportunity_sounds.append(pygame.mixer.Sound(path+file))

    def check(self, gamestate, stats):
        # Perform all the checks here!

        # Only works on the 6 tournament stages
        if gamestate.stage not in [melee.Stage.POKEMON_STADIUM, melee.Stage.FINAL_DESTINATION,
                                   melee.Stage.BATTLEFIELD, melee.Stage.DREAMLAND,
                                   melee.Stage.FOUNTAIN_OF_DREAMS, melee.Stage.YOSHIS_STORY]:
            return

        # These are time sensitive. If there's already something playing, don't queue
        if not self.channel.get_busy():
            if self._jump_stolen(gamestate):
                if self.jumpstolen_sounds:
                    self.channel.play(random.choice(self.jumpstolen_sounds))

            if self._opportunity(gamestate):
                # This one can happen a lot. So only run it half the time
                if self.opportunity_sounds and random.random() > 0.5:
                    self.channel.play(random.choice(self.opportunity_sounds))

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

    def _opportunity(self, gamestate):
        """Did an edge guard opportunity just start?

        We're looking to see if a player is:
            1) Off the stage
            2) Being launched further off stage
            3) Below 30 y
            4) Not being launched too fast
        """
        for port, player in gamestate.player.items():
            # Keep track of this state so we only play the sound once per edge guard
            #   Resets if the player lands
            if player.on_ground:
                self.opportunity_state[port] = 0
            # Is the player off the stage
            if abs(player.x) < melee.EDGE_POSITION[gamestate.stage]:
                continue
            if player.y > 30:
                continue
            if 0.1 < abs(player.speed_x_attack) < 4 and self.opportunity_state[port] != 1:
                self.opportunity_state[port] = 1
                return True
        return False
