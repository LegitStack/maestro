'''
Training Mode:
1. create actors (initialize with state, available ations, attention indices)
2. count votes
3. remove actors from registry upon death
'''
from maestro.lib import memory

# TODO: make concurrent to listen for negations on proposals, and master.

class TrainMaster():
    ''' class used to persist memory of previous state '''
    def __init__(self, state_keys: list, actions: list):
        self.state_keys = state_keys
        self.actions = actions
        self.registry = None
        self.action = None


    def handle_msg(self, msg):
        ''' message from env or actors? '''
        if msg['from'] == 'env':
            return self.handle_env(msg)
        return self.handle_actors(msg)


    def handle_env(self, msg):
        ''' env has given you a new state, tell workers '''
        for actor, alive in self.registry.items():
            pass
            #produce message
            # msg['state']
            # self.action
        #return list of messages


    def handle_actors(self, msg):
        ''' an actor has died or they have votes for you '''
        if 'died' in msg.keys():
            self.registry[msg['from']] = False
            return  # acknowledgement message
        return self.count_votes(msg)


    def count_votes(self, msg):
        ''' count them and do what it says. '''
        actions_count = {k: 0 for k in self.actions}
        for item in msg['votes']:
            actions_count[item] += 1
        return max(actions_count, key=actions_count.get)


    def make_actor(self, msg: dict, attention: list):
        ''' make a new actor, initialize it with state, attention and actions '''
        self.registry[attention] = True
        #CreateActor(
        #    state=msg['state'],
        #    attention=attention,
        #    actions=self.actions,)
        #tell all actors that this actor exists
