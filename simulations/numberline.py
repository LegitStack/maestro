import copy


class NumberLine():
    ''' simulates a Rubiks Cube with a 20 cube representaiton '''
    def __init__(self):
        self.location = 0

    def act(self, action):
        if action == 'up':
            self.location += 1
        elif action == 'down':
            self.location -= 1
        elif action == 'doubleup':
            self.location += 2
        elif action == 'fivedown':
            self.location -= 5
        if self.location > 999:
            self.location = 999
        if self.location < 0:
            self.location = 0

    def see(self) -> dict:
        if self.location < 10:
            return {
                1: 0,
                2: 0,
                3: int(str(self.location)[0]),}
        if self.location < 100:
            return {
                1: 0,
                2: int(str(self.location)[0]),
                3: int(str(self.location)[1]),}
        return {
            1: int(str(self.location)[0]),
            2: int(str(self.location)[1]),
            3: int(str(self.location)[2]),}

    def scramble(self) -> dict:
        choices = ['up', 'down', 'doubleup', 'fivedown']
        for i in range(40):
            self.act(random.choice(choices))
        return self.location
