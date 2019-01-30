'''
Work: The user issues a goal to the system and the system attempts to achieve
the goal. The master will pass the state and the goal down to the actors. the
actors then begin a communication process whereby they come up with a plan to
achieve that goal by a series of actions. They pass up the plan and the master
executes the actions, if everything goes according to plan it carries forward
will the goal is met, otherwise it will stop and tell the workers about any
suprizes it finds, then the workers will formulate a new plan. In Work mode the
actors are doing the vast majority of the work. when an actor receives a state
and a goal he first of all does a shallow path finding in his internal memory.
the shallowness of the search is, at first, merely a configuration setting the
user sets for the project. The worker then, having found a path to the goal, or
having found a path to something that looks most like the goal he can find
proposes the entire path to the group in a broadcast message. if it's approved
they will send that list of states and behaviors to the master, more likely,
someone will say, 'if you do this action, here it will mess me up and I cannot
get to the goal.' so they'll take that partial list, starting at the beginning
and path find towards the goal. then propose a new list (referencing the old one
of course). everyone will continue in this manner until a path to the goal will
be agreed upon and everyone will think it will work, even though it's not the
most efficient way for any one of them. This can also, simultaneously be done
coming from the other end too. doing that should reduce the number of paths the
system has to explore, because they should meet in the middle faster. Lastly, it
should be understood that this is a generalized case of the simple, no path
finding case I had in mind earlier. the no path finding, was still path finding,
with a max exploration of 0 steps. each actor would only look at the proposed
action and see if they would get him to the goal or not. There is one more thing
to consider with these actors. they have overlapping bits. so if they propose
just one action they can ask just the 3 other actors to explore the idea that
the action effects. (I'm thinking now specifically of the cube, but it works the
same way in any case.) So without path finding they don't need to broadcast the
message, but merely send it to those that are effected. the receiving actors
would not approve or deny right away, they would instead look further into this
option and do the same, send subsequent moves to particular other actors.
eventually someone would say, this action would get me to my goal,... well, we'll
have to think more on this but I'm pretty sure the path finding strat is the more
general and more effecient case as it can bundle up several steps together.
'''
from maestro.lib import memory

# TODO: make concurrent to listen for negations on proposals, and master.

class Work():
    ''' class used to persist memory of previous state '''
    def __init__(self, structure: "pd.DataFrame", attention: list, actions: list):
        self.state = None
        self.structure = structure
        self.attention = attention
        self.actions = actions
        self.goal = None


    def handle_msg(self, msg):
        ''' message from master or peers? '''
        if msg['from'] == 'master':
            return self.handle_master(msg)
        else:
            return self.handle_peers(msg)


    def handle_master(self, msg):
        ''' we could turn learning on, but for the poc we're going to keep it
            as simple as possible instead. when a master talks to us he's telling
            us three things: the current state and the goal state. here we should
            persist that info and it should trigger us to start looking for a
            path towards that end. '''
        self.state = self.parse_state(msg['state'])
        self.goal = self.parse_state(msg['goal'])
        return self.generate_proposal(
            state=self.state,
            goal=self.goal,)


    def handle_peers(self, msg):
        ''' peers have proposed a set of actions. take there proposal and see if
        it'll work for you. if not negate it, later make a counter offer. '''
        # TODO: if failure, then generate counter proposal, using as many of
        # these actions as possible, handle that when concurrent:
        return self.generate_proposal_response(actions=msg['actions'])


    def parse_state(self, state: dict) -> dict:
        ''' trim state down to only what we pay attention to '''
        parsed = {}
        for name in self.attention:
            parsed[name] = state[name]
        return parsed


    def parse_states(self, states: 'list(dict)') -> 'list(dict)':
        ''' trim state down to only what we pay attention to '''
        parsed = []
        for state in states:
            parsed.append(self.parse_state(state))
        return parsed


    # TODO: test
    def generate_proposal(self,
            state: dict,
            goal: dict,
        ) -> 'tuple(list(dict(states)), list(dict(actions))) or None':
        '''
        search for a path to the goal, if none is found simply don't propose
        in naive POC version, and wait for someone else to.
        '''
        found, states, actions = forward_search(
                memory=self.structure,
                inputs=[state],
                goal=goal,
                max_counter=5,)
        if found:
            return actions
        else:
            # TODO: if not exact match: propose a path to a similar goal,
            # or wait for all others to fail their search first, maybe...
            return None

        # TODO: search backwards here too or just make another search function
        # that integrates backwards and forwards togther? probably that. then
        # eventually replace forward_search above with that.


    # TODO: test
    def generate_proposal_response(self, actions: 'list(dict)') -> 't.Union[bool, None]':
        ''' creates response '''
        return simulate_actions(
            memory=self.structure,
            input=self.state,
            actions=actions,
            goal=self.goal,)
