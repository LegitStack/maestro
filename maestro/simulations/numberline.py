import copy

from maestro.simulations import env


class NumberLine(env.Environment):
    ''' simulates a Rubiks Cube with a 20 cube representaiton '''
    def __init__(self):
        self.name = 'numberline_base_10_3_digits'
        self.state = 0
        self.actions = [{0:'up'}, {0:'down'}, {0:'doubleup'}, {0:'fivedown'}]

    def act(self, action: dict) -> dict:
        action = self.clean_act(action)
        if action == {0:'up'}:
            self.state += 1
        elif action == {0:'down'}:
            self.state -= 1
        elif action == {0:'doubleup'}:
            self.state += 2
        elif action == {0:'fivedown'}:
            self.state -= 5
        if self.state > 999:
            self.state = 999
        if self.state < 0:
            self.state = 0

    def see(self) -> dict:
        if self.state < 10:
            return {
                1: 0,
                2: 0,
                3: int(str(self.state)[0]),}
        if self.state < 100:
            return {
                1: 0,
                2: int(str(self.state)[0]),
                3: int(str(self.state)[1]),}
        return {
            1: int(str(self.state)[0]),
            2: int(str(self.state)[1]),
            3: int(str(self.state)[2]),}

    def scramble(self) -> dict:
        choices = ['up', 'down', 'doubleup', 'fivedown']
        for i in range(40):
            self.act(random.choice(choices))
        return self.state
