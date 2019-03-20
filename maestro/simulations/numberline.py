from maestro.simulations import env


class NumberLine(env.Environment):
    ''' a 0 to 999 number line, traversable by +1 -1 +2 -5 '''

    def __init__(self):
        self.name = 'numberline_base_10_3_digits'
        self.state = {1: '0', 2: '0', 3: '0'}
        self.original_state = {1: '0', 2: '0', 3: '0'}
        self.actions = [
            {0: 'up'},
            {0: 'down'},
            {0: 'tenup'},
            {0: 'sevendown'},
            {0: 'threedown'}]

    def act(self, action: dict) -> dict:
        action = self.clean_act(action)
        state = int(f'{self.state[1]}{self.state[2]}{self.state[3]}')
        if action == {0: 'up'}:
            state += 1
        elif action == {0: 'down'}:
            state -= 1
        elif action == {0: 'tenup'}:
            state += 10
        elif action == {0: 'sevendown'}:
            state -= 7
        elif action == {0: 'threedown'}:
            state -= 3
        if state > 999:
            state = 999
        if state < 0:
            state = 0
        if state < 10:
            self.state[1] = '0'
            self.state[2] = '0'
            self.state[3] = str(state)[0]
        elif state < 100:
            self.state[1] = '0'
            self.state[2] = str(state)[0]
            self.state[3] = str(state)[1]
        else:
            self.state[1] = str(state)[0]
            self.state[2] = str(state)[1]
            self.state[3] = str(state)[2]
        return self.see()
