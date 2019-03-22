import copy

from numpy.random import randint

from maestro.simulations import env
from maestro.lib import maze_maker


class Maze(env.Environment):
    ''' a two-dimensional maze '''

    def __init__(self):
        self.name = '2D Maze'
        size_x = 80
        size_y = 40
        self.structure = maze_maker.generate_maze(size_x, size_y)
        x, y = self.get_valid_location()
        self.state = {1: str(x), 2:str(y)}
        self.original_state = {1: str(x), 2:str(y)}
        self.actions = [
            {0: 'up'},
            {0: 'down'},
            {0: 'left'},
            {0: 'right'}, ]

    def act(self, action: dict) -> dict:
        action = self.clean_act(action)
        state_x = int(self.state[1])
        state_y = int(self.state[2])
        if action == {0: 'up'}:
            state_x += 1
        elif action == {0: 'down'}:
            state_x -= 1
        elif action == {0: 'left'}:
            state_y -= 1
        elif action == {0: 'right'}:
            state_y += 1
        if not self.structure[state_y][state_x]:
            self.state[1] = str(state_x)
            self.state[2] = str(state_y)
        return self.see()

    def get_valid_location(self):
        print(self.structure.shape)
        while True:
            x = randint(0, self.structure.shape[1])
            y = randint(0, self.structure.shape[0])
            if not self.structure[y][x]:
                return x, y

    def display_maze(self):
        maze_maker.display_maze(self.structure)
