'''
the master node is the first one created. she creates all other nodes.

Prototype version
creates an actor for each combination of bits that she sees change with one
aciton. (the actors are responsible for killing themselves and letting her know.)
sends all living actors each state and last action when in training mode, also
counts their votes and does actions. when in working mode she sends all living
actors state and goal state, and accomplishes their plans.

When creating a new actor she initializes it with current state, list of available
actions and the bits it should attend to.

It should be noted somewhere that this Prototype design constrains the environment
even more than originally supposed. Instead of being able to handle any environment
that has the markov property and is fully observable, it, in addition, need to
have every one of its actions always affect a subset, and the same subset at that,
of state bits. Such as a rubiks cube. What if there was a move that changed all
the bits sometimes, depending on the current configuration. That would not be good.
I'm trying to say, to get around this constraint the system needs to become more
sophisticated. instead of throwing away every actor it has to keep all actors it
creates and they have to learn one additional important thing that complicates the
entire system exponentially: in what situations can they expect to have the markov
property? In those situtations they're as good as prime if they can predict them
correctly. right now we're saying, "that's too hard to figure out. only keep actors
that always have the markov property." It could be that for the naive version of
maestro it remains that way and we acknowledge this additional constraint to the
environment it can work with. Unfortunate, but what can you expect from naivete?

Basic Functions:
1. tell actors to shutdown.
2. take actions.

Training Mode:
1. create actors (initialize with state, available ations, attention indices)
2. count votes
3. remove actors from registry upon death

Working Mode:
1. set actors into working mode
2. send actors information (current state, goal state)
3. manage mistakes in the plan (goto 2. when more sophisticated, tell them what went wrong.)

Ideally training mode and working mode could be combined into one mode of being.
However, they're separated right now for simplicity and efficiency purposes.

the registry should look like this
{actor by unique attention indices: alive or dead}
'''

'''
master adds entries to msgboard to:
1. tell actors of training state change (training)
2. ask actors for a path towards a goal (work)

He always listens to it for:
1. training votes (training)
2. worker deaths (training)
3. working consensus (vaidated path by all actors) (work)

master talks directly to actors:
1. set actors modes

master always listens directly to user for:
1. any command (mode change, goal, shutdown, etc)

So the master has 3 threads that all run concurrently.
    1.  listens to user
    2.  listens to the messageboard
    3.  performs serial computation at the behest of the others
        (mostly interacts with env)
'''
import sys
import time
from threading import Thread

from maestro.lib import memory
from maestro.lib import train_master
from maestro.lib import work_master
from maestro.core import actor
# only needed for typing annotation:
from maestro.simulations import env
from maestro.lib import message_board

class MasterNode():
    ''' MasterNode Object: there can be only one '''

    def __init__(self,
            msgboard: message_board.MSGBoard,
            environment: env.Environment,
            verbose: bool = False
        ):
        self.msgboard = msgboard
        self.env = environment
        self.verbose = verbose
        self.exit = False
        self.mode = 'sleeping'
        self.state_keys = self.env.get_state_indexes()
        # TODO: finish: get the state_keys and actions list from env
        #self.train = train_master.TrainMaster(state_keys: list, actions: list)
        #self.work = work_master.WorkMaster(state_keys: list, actions: list)
        self.listen_to()

    ### listen #################################################################

    def listen_to(self):
        ''' concurrent listening '''

        def user():
            ''' listens to user, upon command will modify configuration '''
            print('\nlistening to user input forever') if self.verbose else None
            while True:
                self.handle_command(command=input('\nmaestro> '))

        def message_board():
            ''' upon notification will take actions, modulated by configuration '''
            print('\nlistening to message_board input forever') if self.verbose else None
            seen_ids = []
            while True:
                time.sleep(1)
                if self.exit:
                    print('\nshutting down message_board listening thread') if self.verbose else None
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

        threads = []
        threads.append(Thread(target=message_board))
        threads.append(Thread(target=user))
        try:
            for thread in threads:
                thread.start()
        except (KeyboardInterrupt, SystemExit):
            self.quit(1)

    def handle_command(self, command: str):
        ''' message from user, what should we do? '''
        commands = {
            'exit': self.quit,
            'help': self.help_me,
            'info': self.get_info,
            'mode train': self.set_mode,
            'mode work': self.set_mode,
            'mode sleep': self.set_mode,
            'do': self.set_goal,}
        if command in commands.keys() and ' ' not in command:
            print('\n', commands[command]())
        elif command.split()[0] in [com.split()[0] for com in commands.keys()]:
            print('\n', commands[command.split()[0]](*command.split()[1:]))
        else:
            print(f'\ninvalid command: {command}\n', self.help_me())

    def handle_msg(self, msg):
        ''' message from actors - what should we do with it? '''
        if self.mode == 'train':
            # TODO:
            # count the votes or
            # hanle a death
            pass
        else: # working mode
            # TODO:
            # check if this message signals we have reached consensus or
            # if its a new proposal add it to the list
            pass

    ### commands ###############################################################


    def get_info(self):
        return f'''
    maestro system information:

    master:
        mode: {self.mode}
        verbosity: {self.verbose}
        exit status: {self.exit}
        uptime: coming soon
        actor count: comming soon
        registry: comming soon

    message board:
        latest message id: {self.msgboard.id}
        latest message: {self.msgboard.get_message()}

    environment:
        env: {self.env}
        state indicies: {self.state_keys}
        available actions: {self.env.get_actions()}

    actors:
        comming soon

            '''

    @staticmethod
    def help_me():
        return '''
    commands:
    help        - displays this message
    info        - display maestro system information
    mode sleep  - tells workers to stop all activity
    mode train  - tells workers to explore and learn
    mode work   - tells workers to collaborate
    do {goal}   - tells workers to achieve a goal
    exit        - exits maestro
            '''
    def quit(self, err: int = 0):
        self.exit = True
        sys.exit()

    def set_mode(self, mode: str):
        if mode == 'train':
            # TODO:
            # erase the memory for work
            # initialize the memory for train
            pass
        elif mode == 'work':
            # TODO:
            # erase the memory for train
            # initialize the memory for work
            pass
        else:
            # TODO:
            # assume sleep - stop all activity, clear all memory
            pass
        self.mode = mode

    def set_goal(self, *goal):
        if self.mode != 'work':
            self.set_mode('work')
        if len(goal) == self.state_keys:
            self.working_master.goal = {k:v for k,v in zip(self.state_keys, goal)}
        else:
            return f'error:\nspecified goal {goal} is not of the same length ({len(goal)}) as the state representation for this environment ({len(self.state_keys)}).\nplease specify a value for each index in order:\n{self.state_keys}'
