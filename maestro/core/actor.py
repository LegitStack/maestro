'''
actors add entries to msgboard to:
1. submit training votes (training)
2. commit suicide (training)
3. invalidate or validate others work proposals (work)
4. propose a work path (work)

actors always listens to it for:
1. training state change (training)
2. issuance of a state to goal (work)
3. others proposals for analysis (work)

actors listen directly to master for:
1. master to change their mode

So the ator has 3 threads that all run concurrently.
    1.  listens to master
    2.  listens to the messageboard
    3.  performs serial computation at the behest of the others
        (mostly finds paths, analyses paths, or produces votes)
'''

import sys
import time
from threading import Thread

from maestro.lib import memory
from maestro.lib import message_board

def start_actor(
        state: dict,
        attention: list,
        actions: 'list(dict)',
        msgboard: message_board.MSGBoard,
        verbose: bool,
    ) -> bool:
    actor = ActorNode(state, attention, actions, msgboard, verbose)
    return True


class ActorNode():
    ''' unit of reactive memory/computation '''

    def __init__(self,
        state: dict,
        attention: list,
        actions: 'list(dict)',
        msgboard: message_board.MSGBoard,
        verbose: bool = False,
    ):
        ''' actor nodes contain little memory '''
        self.structure = memory.create_memory_from_input(state, actions[0])
        self.attention = attention
        self.actions = actions
        self.msgboard = msgboard
        self.verbose = verbose
        self.exit = False
        self.listen_to()

    def quit(self):
        self.exit = True
        sys.exit()

    def listen_to(self):
        ''' concurrent listening '''

        def message_board():
            ''' upon notification will take actions, modulated by configuration '''
            print(f'\nactor {self.attention} listening to message_board input forever') if self.verbose else None
            seen_ids = []
            while True:
                if self.exit:
                    print(f'\nactor {self.attention} shutting down message_board listening thread') if self.verbose else None
                    sys.exit()
                all_messages = self.msgboard.get_messages(0)
                all_ids = [msg['id'] for msg in all_messages]
                new_ids = sorted(set(all_ids) - set(seen_ids))
                for new_id in new_ids:
                    message = [msg for msg in all_messages if msg['id'] == new_id][0]
                    self.handle_msg(message)
                    seen_ids.append(new_id)
                # TODO: optimize by pulling incrementally, by only pulling whats missing:
                #missing_ids = sorted(set(range(min(seen_ids), max(seen_ids) + 1)).difference(seen_ids))
                # TODO: optimize by clearing memory when msgboard gets cleared

        def main_loop():
            while True:
                if self.exit:
                    print(f'\nactor {self.attention} shutting down main_loop thread') if self.verbose else None
                    self.quit()
                # TODO: enry to training and goal oriented behaviors

        threads = []
        threads.append(Thread(target=message_board))
        threads.append(Thread(target=main_loop))
        try:
            for thread in threads:
                thread.start()
        except (KeyboardInterrupt, SystemExit):
            self.exit = True
            self.quit(1)

    def handle_msg(self, msg):
        ''' message from master or other actors - what should we do with it? '''
        if msg['from'] == 'master' and 'command' in msg.keys():
            return self.handle_master_command(msg)
        elif msg['from'] == 'master' and 'goal' in msg.keys():
            return self.handle_master_goal(msg)
        elif msg['from'] == 'master' and 'state' in msg.keys():
            self.save_memory(msg)
            return self.handle_master_state(msg)


    ### specific handlers ######################################################

    def handle_master_command(self, msg):
        '''{'from':'master', 'to':keys, 'command':'die'}'''
        if (msg['command'] == 'ping' and
        (msg['to'] == self.attention or msg['to'] == 'all')):
            self.msgboard.add_message({'from':self.attention, 'to':'master', 'response':'ping'})
        if (msg['command'] == 'die' and
        (msg['to'] == self.attention or msg['to'] == 'all')):
            quit(self)
        # TODO: other commands ...

    def handle_master_goal(self, msg):
        '''{'from':'master', 'state':{}, 'goal':{}}'''
        # TODO: signal main loop thread to start distirbuted path finding process!
        pass

    def handle_master_state(self, msg):
        '''{'from':'master', 'last state':{}, 'state':{}, action:{} }'''
        # TODO: in simplest algorithm do nothing.
        pass

    ### helper #################################################################

    def parse_state(self, state: dict):
        ''' trim state down to only what we pay attention to '''
        return {name: state[name] for name in self.attention}

    def save_memory(self, msg):
        ''' parse state. if I remember a preivous state save a memory (append action
            and state as result), if not make a partial memory (input only). '''
        last = None if 'last state' not in msg.keys() else self.parse_state(msg['last state'])
        action = None if 'action' not in msg.keys() else msg['action']
        current = self.parse_state(msg['state'])
        self.update_memory(state=current, action=action, last=last)

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
