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

we really want the system to always be learning. it should be default, perhaps
a default that you can't turn off, that is, it is, by definition a sensori-
motor inference engine by its very nature. what I'm making here is not just the
engine but the framework.

therefore, the master should aways inform the actors of all states it has
recieved, and all actions it performs. also, training should just be a special
case of work, that means ... that means during training the actors vote on the
state they want to visit, then work to get there

also a vote during work is important to understand that it's a 3 option vote.
an actor can say, "no, this will definately not work" or "I don't actually know
if this will work" or "this works for me." Since this is the framework and not
just the engine the actors decision making can be swapped out for more sophisticated
technologies and return a spectrum of agreement. I should perhaps program it that
way in the first place. with the master never taking actions that have a 0 vote
that would be 'no, I know that wouldnt work.' the next step might be a naive
bayes approach on each actor.
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
        self.actions = self.env.get_actions()

        self.state = self.env.see()
        self.registry = {}
        self.action = {}

        self.goal = None
        self.train = train_master.TrainMaster(self.state_keys, self.actions)
        # train responsibilities are:
        #   1. manage a registry of actors
        #   2. count votes for behaviors
        self.work = work_master.WorkMaster(self.state_keys, self.actions)
        # work responsibilities are:
        #   1. ask for goal from workers
        #   2. execute returned behaviors
        self.listen_to()

        self.voters = self.registry.keys()

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
        threads.append(Thread(target=user))
        try:
            for thread in threads:
                thread.start()
        except (KeyboardInterrupt, SystemExit):
            self.quit(1)
        # instead of spinning off a new thread, just start listening to board:
        message_board()

    def handle_command(self, command: str):
        ''' message from user, what should we do? '''
        commands = {
            'exit': self.quit,
            'help': self.help_me,
            'info': self.get_info,
            'mode': self.set_mode,
            'send': self.send_message,
            'goal': self.set_goal,
            'do': self.perform_action,
            'debug': self.debug,
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
        ''' message from actors - what should we do with it? '''
        print('for debug NEW MESSAGE:', message)
        if self.goal == 'play':
            #vote__msg = {'id':1, 'from':[1,2,3], 'vote':{0:'up'}}

            #if msg['from'] in
            # TODO:
            # count the votes or
            # hanle a death
            # birth
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

    def set_mode(self, *mode: str):
        mode = mode[0]
        self.goal = mode
        return self.goal

    def set_goal(self, *goal):
        if self.mode != 'work':
            self.set_mode('work')
        if len(goal) == self.state_keys:
            self.working_master.goal = {k:v for k,v in zip(self.state_keys, goal)}
        else:
            return f'error:\nspecified goal {goal} is not of the same length ({len(goal)}) as the state representation for this environment ({len(self.state_keys)}).\nplease specify a value for each index in order:\n{self.state_keys}'

    def send_message(self, *message):
        message = ' '.join(message)
        return self.msgboard.add_message({'user':message})

    def debug(self, *code):
        code = ' '.join(code)
        return exec(code)

    def perform_action(self, *action):
        action = ' '.join(action)
        return self.act(action)

    def act(self, action):
        #st = self.env.act(action)
        #for k,v in st.items():
        #    print(k, self.state[k], v)
        return self.analyze_state(self.env.act(action))

    def analyze_state(self, state) -> 'state':
        diff_keys = tuple([k
            for (k,v),(_,vv) in
            zip(sorted(self.state.items()), sorted(state.items()))
            if vv != v])
        print(diff_keys, self.registry.keys())
        if diff_keys not in self.registry.keys():
            self.make_actor(state=state, attention=diff_keys)
        return state

    def make_actor(self, state: dict, attention: list):
        ''' make a new actor, initialize it with state, attention and actions '''
        self.registry[attention] = True
        self.voters = self.registry.keys()
        # TODO: actually start the actor after we finish programming actor.
        #actor.start_actor(
        #    input=self.state,
        #    action=self.action,
        #    state=state,
        #    attention=attention,
        #    actions=self.actions)
        # TODO: turn off and kill any key that is a subset of another key in the registry.
        #       you only want to keep the longest key of any version in theory...
