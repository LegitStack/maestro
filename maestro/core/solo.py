'''
SoloNode:
    creates a explicity simple memory structure of environment states
    path-finds using an explicity simple algorithm
'''

from maestro.lib import memory


class SoloNode():
    ''' A solo artist works alone '''

    def __init__(
        self,
        state: dict,
        attention: list,
        actions: 'list(dict)',
        verbose: bool = False,
    ):
        self.attention = attention
        self.structure = memory.create_memory_from_input(
            input=state,
            action=actions[0])
        self.actions = actions
        self.verbose = verbose
        self.exit = False
        self.inbox = []

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
        ''' message from conductor - what should we do with it? '''
        if msg['from'] == 'conductor' and 'command' in msg.keys():
            return self.handle_conductor_command(msg)
        elif msg['from'] == 'conductor' and 'goal' in msg.keys():
            return self.handle_conductor_goal(msg)
        elif msg['from'] == 'conductor' and 'state' in msg.keys():
            self.save_memory(msg)

    def handle_conductor_goal(self, msg) -> list:
        ''' {'from':'conductor', 'state':{}, 'goal':{}} '''
        path = self.get_path(start=msg['state'], goal=msg['goal'])
        print(path)
        return path

    # helper #################################################################

    def save_memory(self, msg):
        ''' if I remember a preivous state save a memory '''
        last = None if 'last state' not in msg.keys() else msg['last state']
        action = None if 'action' not in msg.keys() else msg['action']
        current = msg['state']
        if last and action:
            self.update_memory(state=current, action=action, last=last)

    def update_memory(
        self,
        state: dict,
        action: dict = None,
        last: dict = None
    ):
        '''save a memory (append action and state as result) '''
        self.structure = memory.append_memory_action_result(
            memory=self.structure,
            input=last,
            action=action,
            result=state,)
        self.structure = memory.append_input(
            memory=self.structure,
            input=state)

    def get_path(self, start: dict, goal: dict) -> list:
            return memory.forward_search(
                memory=self.structure,
                inputs=[start],
                goal=goal,
                counter=0,
                max_counter=5,)
