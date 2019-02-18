'''
MusicianNode:
    learns
    collaborates with those near him
    under the direction of the conductor
'''
from maestro.lib import memory


class MusicianNode():
    ''' unit of memory/computation '''

    def __init__(
        self,
        state: dict,
        attention: list,
        actions: 'list(dict)',
        verbose: bool = False,
    ):
        self.attention = attention
        self.structure = memory.create_memory_from_input(
            input=self.parse_state(state),
            action=actions[0])
        self.actions = actions
        self.verbose = verbose
        self.exit = False
        self.inbox = []

        # memory structure index(es) values, action, results
        self.basics = memory.create_memory_from_input(
            input={k: '-' for k, _ in self.parse_state(state).items()},
            action={k: '-' for k, _ in actions[0].items()})
        self.words = {}  # indicies effected : [sequence sig, sequence sig]

    def add_message(self, msg):
        self.inbox.append(msg)

    def process_next_message(self):
        ''' used mainly during collaboration '''
        try:
            message, *self.inbox = self.inbox
        except ValueError:
            return True
        self.handle_msg(message)
        return False

    def process_last_message(self):
        ''' used mainly during exploration '''
        try:
            message = self.inbox[-1]
            self.inbox = self.inbox[:-1]
        except ValueError:
            return True
        self.handle_msg(message)
        return False

    def handle_msg(self, msg):
        ''' message from conductor or other musicians - what should we do with it? '''
        if msg['from'] == 'conductor' and 'command' in msg.keys():
            return self.handle_conductor_command(msg)
        elif msg['from'] == 'conductor' and 'goal' in msg.keys():
            return self.handle_conductor_goal(msg)
        elif msg['from'] == 'conductor' and 'state' in msg.keys():
            self.save_memory(msg)
            return self.handle_conductor_state(msg)


    ### specific handlers ######################################################

    def handle_conductor_command(self, msg):
        '''{'from':'conductor', 'to':keys, 'command':'die'}'''
        pass
        #if (msg['command'] == 'ping' and
        #(msg['to'] == self.attention or msg['to'] == 'all')):
        #    self.msgboard.add_message({'from':self.attention, 'to':'conductor', 'response':'ping'})
        # TODO: other commands ...

    def handle_conductor_goal(self, msg):
        '''{'from':'conductor', 'state':{}, 'goal':{}}'''
        # TODO: signal main loop thread to start distirbuted path finding process!
        pass

    def handle_conductor_state(self, msg):
        '''{'from':'conductor', 'last state':{}, 'state':{}, action:{} }'''
        # TODO: in simplest algorithm do nothing.
        pass

    ### helper #################################################################

    def parse_state(self, state: dict) -> dict:
        ''' trim state down to only what we pay attention to '''
        return {name: state[name] for name in self.attention}

    def save_memory(self, msg):
        ''' parse state. if I remember a preivous state save a memory (append
        action and state as result), if not make a partial memory (input only).'''
        last = None if 'last state' not in msg.keys() else self.parse_state(msg['last state'])
        action = None if 'action' not in msg.keys() else msg['action']
        current = self.parse_state(msg['state'])
        self.update_memory(state=current, action=action, last=last)

    # TODO: fix -- sometimes it will leave none in results after stop, tune.
    #       discovered this is because sometimes the action isn't saved?
    #       (current work around is to remove those during rest.)
    def update_memory(self, state: dict, action: dict = None, last: dict = None):
        ''' if preivous state is not given make a partial memory (input only)
            else save a memory (append action and state as result) '''
        if last is None or action is None:
            self.structure = memory.append_input(
                memory=self.structure,
                input=state)
        else:
            self.structure = memory.append_memory_action_result(
                memory=self.structure,
                input=last,
                action=action,
                result=state,)
            self.structure = memory.append_input(
                memory=self.structure,
                input=state)

    def rest(self):
        ''' during rest we learn from data we've seen. first we derive basics,
            then we compile words (shared models of sequence across nodes) '''
        self.derive_basics()
        self.compile_words()

    def derive_basics(self):
        ''' since this is simple environment and a naive system each input
            index(s) + action pair should have a predictable result. '''
        # clean up structure - this isn't necessary and introduces complications

        # clean up basics
        #self.basics = self.basics[]


        # figure basics out -
        #   look for things that are always the same
        #   only record the smallest grain possible
        #for index of input and action:
        #    see if it has a predictable response
        pass

    def compile_words(self):
        ''' collaborate with other musicians to compile words'''
        pass
