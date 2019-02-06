'''
ConductorNode:
    interacts with the environment,
    creates MusicianNodes,
    and directs their behavior.
'''
import os
import sys
import time
import copy
import random
import threading

from maestro.lib import memory
from maestro.core import musician
# only needed for typing annotation:
from maestro.simulations import env

class ConductorNode():
    ''' ConductorNode Object: there can be only one '''

    def __init__(self,
            environment: env.Environment,
            verbose: bool = False
        ):
        self.env = environment
        self.verbose = verbose
        self.exit = False
        self.state_keys = self.env.get_state_indexes()
        self.actions = self.env.get_actions()

        self.state = self.env.see()
        self.action = {}

        self.registry: 'dict(set(attention): bool)' = {}
        self.children: 'dict(set(attention): musician)' = {}

        self.goal = None

        # used in show
        self.last_print = ''

        # used to efficiently create musicians... not necessary any more...
        self.new = True
        self.voters = self.registry.keys()

        self.listen_to()

    def broadcast_message(self, msg: dict):
        if not self.new:
            for name, active in self.registry.items():
                if active:
                    self.children[name].add_message(msg)
        return msg

    def hear(self):
        if not self.new:
            for name, active in self.registry.items():
                if active:
                    self.children[name].process_last_message()

    ### listen #################################################################

    def listen_to(self):
        ''' concurrent listening '''

        def user():
            ''' listens to user, upon command will modify configuration '''
            print('\nconductor listening to user input forever') if self.verbose else None
            while True:
                if self.exit:
                    print('\nconductor shutting down user listening thread') if self.verbose else None
                    sys.exit()
                try:
                    self.handle_command(command=input('\nmaestro> '))
                except:
                    self.quit()

        threads = []
        # right now there's no need for message_board.
        # perhaps the message_board is how musicians collaborate?
        #threads.append(threading.Thread(target=message_board))
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
                print('\nshutting down main_loop thread') if self.verbose else None
                self.quit()
            if self.goal == 'tune':
                msg = self.tune()
                self.hear()
                if self.verbose: self.show(msg)
            elif self.goal == 'play':
                self.play()
            elif self.goal == None:
                self.sleep()


    def handle_command(self, command: str):
        ''' message from user, what should we do? '''
        commands = {
            'exit': self.quit,
            'help': self.help_me,
            'info': self.get_info,
            'tune': self.set_tune,
            'stop': self.set_stop,
            'play': self.set_goal,
            'goal': self.set_goal,
            'do': self.perform_action,
            'send': self.send_message,
            'debug': self.debug,
            'clear': self.clear_screen,
        }
        try:
            if command in commands.keys() and ' ' not in command:
                print('\n', commands[command]())
            elif command.split()[0] in [com.split()[0] for com in commands.keys()]:
                print('\n', commands[command.split()[0]](*command.split()[1:]))
            else:
                print(f'\ninvalid command: {command}\n', self.help_me())
        except Exception as e:
            print(e)

    def handle_msg(self, msg):
        ''' message from musicians - what should we do with it? '''
        if self.goal == 'tune':
            #vote__msg = {'id':1, 'from':[1,2,3], 'vote':{0:'up'}}
            # TODO: handle death
            # hanle a death
            # for now we decide who dies, subsets...

            # TODO:
            # count the votes or
            # for now we are not couting votes, just acting randomly
            pass
        else: # playing mode
            # TODO:
            # check if this message signals we have reached consensus or
            # if its a new proposal add it to the list
            pass

    ### commands ###############################################################


    def get_info(self):
        return f'''
    maestro system information:

    conductor:
        mode: {'sleep' if self.goal==None else ('tune' if self.goal == 'tune' else 'play')}
        verbosity: {self.verbose}
        exit status: {self.exit}
        uptime: coming soon
        registry: {[str(k) + ':' + str(len(k)) for k,v in self.registry.items() if v]}
        current state: {self.state}
        latest action: {self.action}

    musicians:
        busy musicians: {[f'{k}:{len(self.children[k].inbox)} '
            for k,v in self.registry.items()
            if v and len(self.children[k].inbox) > 0]}
        musicians memory: {[f'{k}:{len(self.children[k].structure)} '
            for k,v in self.registry.items()
            if v and len(self.children[k].structure) > 0]}


    environment:
        env: {self.env}
        state indicies: {self.state_keys}
        available actions: {self.env.get_actions()}

    musicians:
        comming soon

            '''

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
    play {goal} - tells maestro to achieve a goal
    exit        - exits maestro

    debug commands:
    do {goal}   - tells musicians to do an action
    send {msg}  - tells maestro to send a message
    debug {code}- tells maestro to execute code
    '''

    def quit(self, err: int = 0):
        # unnecessary
        #self.broadcast({'from':'conductor', 'to':'all', 'command':'die'})
        self.exit = True
        sys.exit()

    def set_tune(self):
        self.goal = 'tune'
        return self.goal

    def set_stop(self):
        if self.new:
            self.create_musicians()
            self.new = False
        self.goal = None
        return self.goal

    def set_goal(self, *goal):
        if self.goal == 'tune' or self.goal == None:
            self.goal == ''
        if len(goal) == self.state_keys:
            self.goal = {k:v for k,v in zip(self.state_keys, goal)}
        else:
            return f'error:\nspecified goal {goal} is not of the same length ({len(goal)}) as the state representation for this environment ({len(self.state_keys)}).\nplease specify a value for each index in order:\n{self.state_keys}'

    def send_message(self, *message):
        message = ' '.join(message)
        return self.broadcast_message({'user':message})

    def debug(self, *code):
        code = ' '.join(code)
        return exec(code)

    def clear_screen(self):
        return os.system('cls')

    def perform_action(self, *action):
        action = ' '.join(action)
        return self.act(action)


    ### main ###################################################################

    def show(self, msg: dict = None):
        if msg is None:
            counter = 0
            for x in self.registry:
                if self.registry[x]:
                    counter += 1
            info = f'state: {str(self.state)[:10]}  |  action: {str(self.action)[:10]}  |  registry: {counter}'
        else:
            info = ''
            for k,v in msg.items():
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
        msg = {'from':'conductor'}
        msg['last state'] = copy.deepcopy(self.state)
        self.action = random.choice(self.actions)
        self.state = self.act(self.action[0])
        msg['state'] = self.state
        msg['action'] = self.action
        return self.broadcast_message(msg)


    def sleep(self):
        time.sleep(1)

    def play(self):
        time.sleep(1)


    ### behaviors ##############################################################

    def act(self, action):
        return self.analyze_state(self.env.act(action))

    def analyze_state(self, state) -> 'state':
        def get_keys_that_changed(state):
            return tuple([
                k for (k,v),(_,vv) in
                zip(sorted(self.state.items()), sorted(state.items()))
                if vv != v])

        def manage_registry(changed_keys):
            ''' avoid creating or disable and remove musicians assigned to a subset
                of state indicies that another musician already pays attention to
                (according to the most naive algorithm). '''
            if changed_keys not in self.registry.keys():
                save = True
                for keys in self.registry.keys():
                    if len(changed_keys) < len(keys):
                        if set(changed_keys).issubset(keys):
                            save = False
                    elif set(keys).issubset(changed_keys):
                        self.registry[keys] = False
                if save:
                    self.make_musician(state=state, attention=changed_keys,)

        changed_keys = get_keys_that_changed(state)
        manage_registry(changed_keys)
        return state

    def make_musician(self, state: dict, attention: list):
        ''' make a new musician, initialize it with state, attention and actions '''
        self.registry[attention] = True
        self.voters = self.registry.keys()
        if not self.new:
            self.children[attention] = musician.MusicianNode(
                state=state,
                attention=attention,
                actions=self.actions,
                verbose=self.verbose,)

    def create_musicians(self):
        ''' create musicians for the first time afer we've quickly explored the env '''
        for attention, status in self.registry.items():
            if status:
                self.children[attention] = musician.MusicianNode(
                    state=self.state,
                    attention=attention,
                    actions=self.actions,
                    verbose=self.verbose,)
