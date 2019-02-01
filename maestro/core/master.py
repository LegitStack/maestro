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
'''

from maestro.lib import memory
from maestro.lib import train_master
from maestro.lib import work_master

# TODO: make concurrent to listen for negations on proposals, and master.

class MasterNode():
    ''' Needs to be made concurrent '''
    def __init__(self):
        self.mode = 'waiting'
        #set up train_master mode
        #set up work_master mode
        pass

    def start(self):
        self.mode = 'training'
        return 'at your service'

    def handle_msg(self, msg):
        ''' message from env or actors? '''
        if msg['from'] == 'user':
            return self.handle_user(msg)
        else:
            pass # if mode is worker mode, pass to handle message worker mode, etc.


    def handle_user(self, msg):
        ''' do whatever the user says (explore, acheive goal, shutdown, etc) '''
        pass
