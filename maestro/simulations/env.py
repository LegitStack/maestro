class Environment():
    ''' environment object '''
    def __init__(self):
        self.state = {0:0}
        self.actions = [{0:0},{0:1}]
        self.name = 'simulated_environment'

    def act(self, action: dict) -> dict:
        ''' send action to the environment, return mutated env state '''
        action = self.clean_act(action)
        # for key, value in action.items(): mutate the state in some way
        return self.state

    def see(self) -> dict:
        ''' returns current state '''
        return self.state

    def clean_act(self, action) -> dict:
        if isinstance(action, list):
            return {k: a for k, a in zip(self.actions[0].keys(), action)}
        elif not isinstance(action, dict) and len(self.actions[0].keys()) == 1:
            return {sorted(self.actions[0].keys())[0]: action}

    def get_actions(self) -> dict:
        ''' returns avilable actions so agents can properly initialize '''
        return self.actions

    def get_state_indexes(self) -> list:
        ''' returns state keys so agents can properly initialize '''
        return sorted(list(self.state.keys()))
