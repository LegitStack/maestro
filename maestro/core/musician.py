'''
MusicianNode:
    learns
    collaborates with those near him
    under the direction of the conductor
'''
import os
import sys
import time
from threading import Thread

from maestro.lib import memory
from maestro.lib import message_board


# TODO: make musician a subscriber.
# https://www.protechtraining.com/blog/post/tutorial-the-observer-pattern-in-python-879

class MusicianNode():
    ''' unit of memory/computation '''

    def __init__(self,
        state: dict,
        attention: list,
        actions: 'list(dict)',
        verbose: bool = False,
    ):
        self.structure = memory.create_memory_from_input(state, actions[0])
        self.attention = attention
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

    def parse_state(self, state: dict):
        ''' trim state down to only what we pay attention to '''
        return {name: state[name] for name in self.attention}

    def save_memory(self, msg):
        ''' parse state. if I remember a preivous state save a memory (append action
            and state as result), if not make a partial memory (input only). '''
        last = None if 'last state' not in msg.keys() else self.parse_state(msg['last state'])
        action = None if 'action' not in msg.keys() else msg['action']
        current = self.parse_state(msg['state'])
        print(action)
        self.update_memory(state=current, action=action, last=last)

    def update_memory(self, state: dict, action: dict = None, last: dict = None):
        ''' if preivous state is not given make a partial memory (input only)
            else save a memory (append action and state as result) '''
        if last is None or action is None:
            self.structure = memory.append_input(
                memory=self.structure,
                input=state)
        else:
            print('IN ELSE',last)
            self.structure = memory.append_memory_action_result(
                memory=self.structure,
                input=last,
                action=action,
                result=state,)
