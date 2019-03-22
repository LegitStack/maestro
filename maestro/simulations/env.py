import copy
import random


class Environment():
    ''' environment object '''

    def __init__(self):
        self.original_state = {0: 0}
        self.state = {0: 0}
        self.actions = [{0: 0}, {0: 1}]
        self.name = 'simulated environment'

    def act(self, action: dict) -> dict:
        ''' send action to the environment, return mutated env state '''
        action = self.clean_act(action)
        # for key, value in action.items(): mutate the state in some way
        return self.see()

    def see(self) -> dict:
        ''' returns current state '''
        return copy.deepcopy(self.state)

    def clean_act(self, action) -> dict:
        if isinstance(action, list):
            return {k: a for k, a in zip(self.actions[0].keys(), action)}
        elif not isinstance(action, dict) and len(self.actions[0].keys()) == 1:
            return {sorted(self.actions[0].keys())[0]: action}

    def get_actions(self) -> dict:
        ''' returns avilable actions so agents can properly initialize '''
        return copy.deepcopy(self.actions)

    def get_state_indexes(self) -> list:
        ''' returns state keys so agents can properly initialize '''
        return sorted(list(self.state.keys()))

    def reset_state_indexes(self) -> list:
        ''' resets state to original state '''
        self.state = copy.deepcopy(self.original_state)

    def scramble(self, count: int = 40) -> dict:
        choices = [list(act.values())[0] for act in self.actions]
        for i in range(count):
            self.act(random.choice(choices))
        return copy.deepcopy(self.state)
