'''
I'm not exactly sure how the protocol module should look yet. should I start by
building the actual infrastructure of communication? probably not, we may want
to simulate separate nodes with mere objects. We may just use different processes
or we might use an actor framework like rx or whatever it is or akka or something.
so we need to define here the rules about what to do with messages, not the actual
passing of messages themselves.

It basically comes down to 3 cases. I get a message from the master node and
start searching, or I get a message from fellow workers and collaborate or I
stop what I'm doing because the answer has been achieved.

During training I also want to do things such as record what the last state was
and so on, so training is a bit different. perhaps I should just work on the
training protocol first? I'll sleep on it.

Each actor will have 3 modes, I'm only going to create the first two to start
out with though, the third being a combination of the other two. They are Train
Work and Play modes. Here's the gist of all three:

Train: the default mode. When a worker is created it is in training mode because
workers are only created when the master is in training mode. In this mode, upon
receiving an input it searches it's database to see what action it should take.
It wants to do actions in situations it's never done before so it'll search for
this input or, if it has never seen this input before it'll search for inputs
like this, then vote on an action that has been least done across the group of
them. Therefore it can vote for multiple actions. that really means it just has
multiple votes. how many? as many as there are actions. it will usually put all
its votes to a particular action, but if it doesn't care, it'll put equal number
of votes in each action's category. The master will count the votes (he may not
count all of them if it looks like its going in a certain direction, but that's
an optimization) then he will perform some action. Then he will send back down
the state of what he sees. One last thing. As the training is going an actor may
see the same input-action pair but they lead to different outputs. If this happens
that actor kills himself. He sends a message to the master to let him know, and
kills his process. this is because if he can't make sense of the environment he's
of no use to the system, and is just a drain on resources. In less naive versions
he may have some value but in this one he's useless. in training most of the
work is done by the master as he has the responsibility to create actors (creates
one with every new combination of input changes), remove dead ones from his
registry, and count the votes.

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

Play: play is a combination of work and training, the actors vote on goals, they
both want to see things they've never seen before and do them in a way they've
never done them before. (new paths through the environment). Its really just
training with longer term goals and it could end up just being the more general
case of training, but theres many ways we could implement so we wont worry about
it now.

In this naive version of the protocol the entire state is passed to everyone and
they parse out what they care about.
'''
