'''
Working Mode:
1. set actors into working mode
2. send actors information (current state, goal state)
3. manage mistakes in the plan (goto 2. when more sophisticated, tell them what went wrong.)
'''
from maestro.lib import memory

# TODO: make concurrent to listen for negations on proposals, and master.

class WorkMaster():
    ''' class used to persist memory of previous state '''
    def __init__(self, state_keys: list, actions: list):
        self.state_keys = state_keys
        self.actions = actions
        self.registry = None
        self.plan = None


    def handle_msg(self, msg):
        ''' message from env or actors? '''
        if msg['from'] == 'env':
            return self.handle_env(msg)
        else:
            return self.handle_actors(msg)


    def handle_env(self, msg):
        ''' env has given you a new state, decide how you ought to react '''
        # use self.plan to know if you're in the middle of a plan or at goal
        pass


    def handle_actors(self, msg):
        ''' they have a plan for you, execute it '''
        pass


    def parse_state(self, state: dict) -> dict:
        ''' trim state down to only what we pay attention to '''
        parsed = {}
        for name in self.attention:
            parsed[name] = state[name]
        return parsed
