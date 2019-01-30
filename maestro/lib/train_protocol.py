'''
Train: the default mode. When a worker is created it is in training mode because
workers are only created when the master is in training mode. In this mode, upon
receiving an input it searches it's database to see what action it should take.
It wants to do actions in situations it's never done before so it'll search for
this input or, if it has never seen this input before it'll search for inputs
like this, then vote on an action that has been least done across the group of
them. Therefore it can vote for multiple actions. that really means it just has
multiple votes. how many? as many as there are actions. it will usually put all
its votes to a particular action, but if it doesn't care, it'll put equal number
of votes in each action's category. The master will count the votes (he may not
count all of them if it looks like its going in a certain direction, but that's
an optimization) then he will perform some action. Then he will send back down
the state of what he sees. One last thing. As the training is going an actor may
see the same input-action pair but they lead to different outputs. If this happens
that actor kills himself. He sends a message to the master to let him know, and
kills his process. this is because if he can't make sense of the environment he's
of no use to the system, and is just a drain on resources. In less naive versions
he may have some value but in this one he's useless. in training most of the
work is done by the master as he has the responsibility to create actors (creates
one with every new combination of input changes), remove dead ones from his
registry, and count the votes.
'''
from maestro.lib import memory

class Train():
    ''' class used to persist memory of previous state '''
    def __init__(self, structure: "pd.DataFrame", attention: list, actions: list):
        self.state = None
        self.structure = structure
        self.attention = attention  # list of state-bits it cares about.
        self.actions = actions

    def handle_msg(self, msg):
        ''' message from master or peers? '''
        if msg['from'] == 'master':
            self.handle_master(msg)
        else:
            self.handle_peers(msg)


    def handle_master(self, msg):
        ''' parse state. if I remember a preivous state save a memory (append action
            and state as result), if not make a partial memory (input only). '''
        state = self.parse_state(msg['state'])
        action = msg['action']
        vote = self.generate_vote(state)
        self.update_memory(state, action)
        return vote


    # TODO: test
    def generate_vote(self, state):
        ''' look through the memory for this state. if it is found, vote for an
            action that we've never done from here before, if it is not found
            search for the most similar states upto a certain threshold and vote
            on the least used action across the group '''
        matches = memory.find_input(memory=self.structure, input=state)
        actions = self.actions
        if matches.shape[0] > 0:
            #used_actions = [dict(row) for ix, row in matches['action'].iterrows()]
            used_actions = matches.to_dict('records')
            for ua in used_actions:
                actions.remove(ua)
            if len(actions) > 0:
                vote = actions[0]
            else:
                vote = None
        else:
            matches = memory.find_similar(memory=self.structure, input=state, limit=100)
            used_actions = matches.to_dict('records')
            actions_count = {k:0 for k in self.actions.keys()}
            for item in used_actions:
                actions_count[item] += 1
            vote = min(actions_count, key=actions_count.get)
        return vote


    def update_memory(self, state, action):
        ''' parse state. if I remember a preivous state save a memory (append action
            and state as result), if not make a partial memory (input only). '''
        if self.state is None:
            self.structure = memory.append_input(
                memory=self.structure, input=state)
        else:
            self.structure = memory.append_memory_action_result(
                memory=self.structure,
                input=self.state,
                action=action,
                result=state,)
        self.state = state


    def parse_state(self, state):
        ''' trim state down to only what we pay attention to '''
        parsed = {}
        for name in self.attention:
            parsed[name] = state[name]
        return parsed
