
class Stats:
    def __init__(self):
        self.input_count = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        self._latest_frame = -124
        self._last_gamestate = None
        self.current_combo = None

    def process(self, gamestate):
        self._latest_frame = gamestate.frame

        for port, player in gamestate.player.items():
            if self._last_gamestate and port in self._last_gamestate.player:
                self.input_count[port] += self._count_inputs(self._last_gamestate.player[port].controller_state,
                                                       player.controller_state)

        self.calculateCombo(gamestate)

        # Do this last
        if self._latest_frame == -123:
            self.input_count = {
                1: 0,
                2: 0,
                3: 0,
                4: 0
            }
        self._last_gamestate = gamestate


    def calculateCombo(self, gamestate):
        # Don't bother frame 1
        if self._last_gamestate is None:
            return

        # Only try if there's a player 1 and 2
        if 1 not in gamestate.player or 2 not in gamestate.player:
            return
        if 1 not in self._last_gamestate.player or 2 not in self._last_gamestate.player:
            return

        # See if a new combo has started
        for i in range(2):
            is_damaged = 0x4B <= gamestate.player[i+1].action.value <= 0x5B
            is_grabbed = 0xDF <= gamestate.player[i+1].action.value <= 0xE8
            damage_taken = gamestate.player[i+1].percent - self._last_gamestate.player[i+1].percent

            if is_damaged or is_grabbed:
                if self.current_combo:
                    self.current_combo["reset_counter"] = 0
                    self.current_combo["damage"] = gamestate.player[i+1].percent - self.current_combo["starting_damage"]
                else:
                    self.current_combo = {
                        "player": i+1,
                        "hits": 0,
                        "reset_counter": 0,
                        "damage": damage_taken,
                        "starting_damage": self._last_gamestate.player[i+1].percent
                    }
            else:
                if self.current_combo:
                    self.current_combo["reset_counter"] += 1
                    if self.current_combo["reset_counter"] > 45:
                        self.current_combo = None

            if not self.current_combo:
                continue

            # TODO Don't count multi hit attacks
            if damage_taken > 0:
                self.current_combo["hits"] += 1

    def get_apm(self, port):
        minutes = (self._latest_frame + 123)/3600
        return self.input_count[port] / minutes

    def _count_inputs(self, before, after):
        """Compare two controller states and return the number of new 'inputs'

        For APM calculation. Roughly follows the method in the official SLP parser
        """
        count = 0
        for button, pressed in before.button.items():
            if not pressed and after.button[button]:
                count += 1

        if self._region(*before.main_stick) != self._region(*after.main_stick):
            if self._region(*after.main_stick) > 0:
                count += 1

        if self._region(*before.c_stick) != self._region(*after.c_stick):
            if self._region(*after.c_stick) > 0:
                count += 1

        # TODO shoulder analog

        return count

    def _region(self, x, y):
        """Given an x,y stick coord, return the general region its in"""
        region = 0
        if (x >= 0.2875 and y >= 0.2875):
            region = 1
        elif (x >= 0.2875 and y <= -0.2875):
            region = 2
        elif (x <= -0.2875 and y <= -0.2875):
            region = 3
        elif (x <= -0.2875 and y >= 0.2875):
            region = 4
        elif (y >= 0.2875):
            region = 5
        elif (x >= 0.2875):
            region = 6
        elif (y <= -0.2875):
            region = 7
        elif (x <= -0.2875):
            region = 8
        return region
