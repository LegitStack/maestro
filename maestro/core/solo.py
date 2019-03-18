'''
SoloNode:
    creates a explicity simple memory structure of environment states
    path-finds using an explicity simple algorithm
'''
import os
import sys
import time
import copy
import random
import threading

from maestro.lib import memory
# only needed for typing annotation:
from maestro.simulations import env


class SoloNode():
    ''' A solo artist works alone '''

    def __init__(
        self,
        environment: env.Environment,
        verbose: bool = False
    ):
        self.env = environment
        self.verbose = verbose
        self.exit = False
        self.state_keys = self.env.get_state_indexes()
        self.actions = self.env.get_actions()
        self.state = self.env.see()
        self.last_state = self.state
        self.action = {}
        self.goal = None
        self.last_print = ''
        self.structure = memory.create_memory_from_input(
            input=self.state,
            action=self.actions[0])
        self.display_welcome()
        self.listen_to()

    def display_welcome(self):
        print('Welcome to Maestro AI, the naive sensorimotor inferece engine!')
        print('\nMaestro is are running in Solo mode.\n')
        print(
            'env', self.env.name,
            'allows for', len(self.env.get_actions()), 'actions',
            'and has', len(self.state_keys), 'state indicies.\n')
        print('maximum number of nodes:', 2 ** (len(self.state_keys)) - 2)

    # listen #################################################################

    def listen_to(self):
        ''' concurrent listening '''

        def user():
            ''' listens to user, upon command will modify configuration '''
            if self.verbose:
                print('\n maestro listening to user input forever')
            while True:
                if self.exit:
                    if self.verbose:
                        print('\nmaestro shutting down user thread')
                    sys.exit()
                try:
                    self.handle_command(command=input('\nmaestro> '))
                except Exception:
                    self.quit()

        threads = []
        threads.append(threading.Thread(target=user))
        try:
            for thread in threads:
                thread.start()
            self.main_loop()
        except (KeyboardInterrupt, SystemExit):
            self.exit = True
            self.quit(1)

    def main_loop(self):
        while True:
            if self.exit:
                if self.verbose:
                    print('\nshutting down main_loop thread')
                self.quit()
            if self.goal == 'tune':
                msg = self.tune()
                if self.verbose:
                    self.show(msg)
            elif self.goal == 'play':
                self.play()
            elif self.goal is None:
                self.sleep()
            else:
                self.play()
                self.set_stop()

    def handle_command(self, command: str):
        ''' message from user, what should we do? '''
        commands = {
            'exit': self.quit,
            'help': self.help_me,
            'info': self.get_info,
            'tune': self.set_tune,
            'stop': self.set_stop,
            # 'sleep': self.rest,
            'dream': self.examine_sleep,
            'play': self.set_goal,
            'goal': self.set_goal,
            'do': self.perform_action,
            # 'send': self.send_message,
            'debug': self.debug,
            'clear': self.clear_screen,
            'pickle': self.export_pickle,
        }
        try:
            self.last_print = ''
            if command in commands.keys() and ' ' not in command:
                print('\n', commands[command]())
            elif command.split()[0] in [
                com.split()[0] for com in commands.keys()
            ]:
                print('\n', commands[command.split()[0]](*command.split()[1:]))
            else:
                print(f'\ninvalid command: {command}\n', self.help_me())
        except Exception as e:
            print(e)

    # commands ###############################################################

    def get_info(self):
        return f'''
    maestro system information:

    maestro:
        mode: {'sleep' if self.goal==None else (
            'tune' if self.goal == 'tune' else 'play')}
        verbosity: {self.verbose}
        exit status: {self.exit}
        uptime: coming soon
        current state: {self.state}
        latest action: {self.action}

    environment:
        name: {self.env.name}
        env: {self.env}
        state indicies: {self.state_keys}
        available actions: {self.env.get_actions()}

    '''

    def export_pickle(self):
        print('fix me.')

    def examine_sleep(self):
        print('fix me.')

    @staticmethod
    def help_me():
        return '''
    infomational commands:
    help        - display this message
    info        - display maestro system information
    clear       - clears screen

    behavioral commands:
    tune        - tells musicians to explore and learn
    stop        - tells musicians to stop all activity
    sleep       - tells musicians to condense memory
    play <goal> - tells maestro to achieve a goal
    exit        - exits maestro

    debug commands:
    do <goal>   - tells musicians to do an action
    send <msg>  - tells maestro to send a message
    debug <code>- tells maestro to execute code
    pickle      - exports pickles of musicians minds
    '''

    def quit(self, err: int = 0):
        self.exit = True
        sys.exit()

    def set_tune(self):
        self.goal = 'tune'
        return self.goal

    def set_stop(self):
        self.goal = None
        return self.goal

    def set_goal(self, *goal):
        if self.goal == 'tune' or self.goal is None:
            self.goal == ''
        print(len(goal), len(self.state_keys), len(goal) == len(self.state_keys))
        if len(goal) == len(self.state_keys):
            self.goal = {k: v for k, v in zip(self.state_keys, goal)}
        else:
            return (
                f'error:\nspecified goal {goal} is not of the same length '
                + f'({len(goal)}) as the state representation for this'
                + f'environment ({len(self.state_keys)}).\nplease specify a'
                + f'value for each index in order:\n{self.state_keys}')

    def debug(self, *code):
        code = ' '.join(code)
        return exec(code)

    def clear_screen(self):
        return os.system('cls')

    def perform_action(self, *action):
        action = ' '.join(action)
        return self.env.act(action)

    # main ###################################################################

    def show(self, msg: dict = None):
        if msg is None:
            info = 'state: {s}  |  action: {a}'.format(
                s=str(self.state)[:10], a=str(self.action)[:10])
        else:
            info = ''
            for k, v in msg.items():
                info = f'{info}{k}:{str(v)[:10]},'
                if len(info) >= 70:
                    break
        if self.last_print == 'show':
            print(info, end="\r", flush=True)
        else:
            print('')
            print(info, end="\r", flush=True)
            self.last_print = 'show'

    def tune(self):
        self.last_state = copy.deepcopy(self.state)
        self.action = random.choice(self.actions)
        self.state = self.env.act(self.action[0])
        self.update_memory()

    def sleep(self):
        time.sleep(1)

    def play(self):
        print(self.get_path(start=self.state, goal=self.goal))

    # helper #################################################################

    def update_memory(self):
        '''save a memory (append action and state as result) '''
        self.structure = memory.append_memory_action_result(
            memory=self.structure,
            input=self.last_state,
            action=self.action,
            result=self.state,)
        self.structure = memory.append_input(
            memory=self.structure,
            input=self.state)

    def get_path(self, start: dict, goal: dict) -> list:
            return memory.forward_search(
                memory=self.structure,
                inputs=[start],
                goal=goal,
                counter=0,
                max_counter=5,)
