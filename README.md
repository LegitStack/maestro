[![Open Source Helpers](https://www.codetriage.com/legitstack/maestro/badges/users.svg)](https://www.codetriage.com/legitstack/maestro)

# maestro

https://www.maestroai.com

maestro is an actor-model framework for creating intelligent autonomous actors.


## Current Status

maestro is currently in a prototype phase.


## Project Details:

### What is the basic idea?
We are creating a "Markov compatible sensorimotor inference engine."

### What does that mean?
"Sensorimotor" refers to a program that gets input (sensory data) and produces output (motor commands). In other words, it's in a continuous loop with the environment (the environment being a puzzle or maze).

"Inference engine" means that it figures out how its motor commands affect the environment. It does this by paying close attention to how its sensory input changes based upon what its motor commands were.

Lastly, being "Markov compatible" simply means the environment is constrained to be simple: a static state-space that is fully observable, even though it may be very large. The proof of concept won't be able to handle anything more complex than that.

### What is the basic design?
The proof of concept design can be understood as a network of nodes that all talk to each other and share information to understand the environment they're placed in.

Each node can see a portion of the environment, remembers certain things about the past, and can talk to any or all of the other nodes.

They basically propose and vote on what choices to make in order for the majority of them to make sense of the world, though each only sees a small portion of it.

### What makes it General AI as opposed to regular AI?
The idea is that you can categorize environments based upon their features and complexity. Thus if the AI can learn how to manipulate a certain type of environment it can learn to manipulate every possible environment, ever possible puzzle, that conforms to that type. Thus it is generalized.

We have identified the following key features of environments that can be combined define its type:

1. Environments can be large or small. If it's large they are too big for one node to ever possibly understand, if they are small they are not memory intensive; one node can memorize the whole thing.

2. Environments can have symmetric/repeating sensory patterns or the state space can be arranged somewhat randomly. This is talking about an environment's entropy.

3. Environments behaviors (what the AI can do) can have symmetric effects on the environment (such as going right undoes the effect of going left) or non-symmetric effects.

4. Environments can have a static state-space that is fully observable or a non-static one. This essentially means there are other actors changing things in the environment, and that the Maestro AI actor is not the only agent acting on the environment.

This creates a matrix of 8 different types of environments ranging from simple to complex. For example, here's the simplest possible environment (2x2 rubix cube):

- small state-space
- symmetric/repeating sensory patterns
- behaviors have symmetric effects
- static state-space, fully observable

Here is the environment type we hope to be able to manage with our proof of concept (3x3 rubix cube):

- large or infinite state-space (memory intensive, multiple nodes required).
- symmetric/repeating sensory patterns
- behaviors have symmetric effects 
- static state-space, fully observable

And here is a complex environment that we someday hope to have Maestro AI manage effectively:

- large or infinite state-space (memory intensive)
- non-symmetric and not repeating sensory patterns (sensory input is high in entropy)
- behaviors do not have symmetric effects (motor effects is high in entropy).
- static state-space, fully observable

### What is the basic philosophy?
We consider an environment that is not a fully observable static state space to be the most difficult problem to solve and should be left out of consideration for the time being. However, interestingly enough, we have noticed that is the problem others have tried to solve first. Chess, for example, is an environment with another player, therefore the state-space is not static, one state does not always lead to the same next state.

We feel that solving AGI for simple environments is possible and should be done first; that it is an 'early optimization' mistake not to. The world is full of static systems that an AGI, such as ours, could be in charge of managing according to the goals we provide it. We feel this is an obvious niche that has been overlooked.

### What does success look like?
We will know that our proof of concept for this design is a success if we give the AGI a variety of very simple puzzles (such as a Rubix Cube, or Atari video games) and it automatically learns how to solve them without any instruction or help.



## Theory

It is our belief that AGI is _necessarily_ **computation upon distributed memory** (on a network).

Some evidence for this belief is that most sophisticated machine learning algorithms such as Neural Nets are merely simulations of a network architecture. Even simple machine learning algorithms such as decision trees are represented as a network of nodes, in a particular hierarchical structure that produces a directed acyclic graph of computation.

Thus, Maestro AI is essentially just being a network of nodes, simulated in some way such as the "actor model" of programming. Maestro AI is an attempt to produce a simple, generalized method of computation upon a network of nodes. This is to be done by working in two containing paradigms:

1. Maestro is to be a Sensorimotor engine, in constant communion with its environment. That is to say it's not merely a model, applied to data, but can be thought of as a living model, constantly changing through interaction with its environment; as an actor.

2. Maestro is to be given, and made to understand the simplest category of environments first. There are simple environments (essentially static state spaces) and complex environment (essentially environments that change overtime regardless of maestro's actions). The Maestro Proof of Concept should first learn how to manage simple ones, rather than complex ones. This is because we want to, as its creators, learn step by step how to manage the communication of the network in order to most optimally achieve the appropriate distributed computation on distributed information for each type of environment. We need to learn the relationship between the complexity of Maestro's environment and the complexity of each node's memory and ability to communicate with the rest of the network (distributed memory).

Each actor has 4 things: behaviors as predefined functions, input data which is ultimately derived from the external environment, contextual information (communication with fellow actors), and a specific goal in terms of what they should get their input data to look like.

Once you have a system defined with each actor having functionality and set to receive messages from the correct other actors, you train the actors by letting them explore their behaviors at random, attempting to achieve their goals in the most efficient way possible. This training is done in an isolated environment.

Once the actors are trained they are put to work in the real environment. The idea behind this is that they can maintain, or bring about any state of that environment by working together and coordinating their efforts in the way they learned during training.

Maestro AI's distributed memory, and computational infrastructure acts as an efficient path finding algorithm which can find a path from one state to any other state in the environment's state space.


## Real World Example

How is Maestro useful? Many structures in the world today are essentially puzzles. They're static, fully observable state-spaces in which a Maestro AI bot can be place and can naturally (unsupervised) learn how to manipulate the environment to achieve any state of the environment it is given as a goal. Thus, Maestro, Even a naive version of it could prove very powerful as specific programming would not need to be employed. 

A perfect and extremely simple use case is a web server supervisor. Maestro would be given a goal to make sure the website is up and that not more than one instance of the webserver is running. That is a specific state-space within all possible states of the environment. During training it can learn how its behaviors manipulate the environment: one function it can call kills all instances of the webserver while another function starts one.

After it learns how to restart the server as soon as it crashes it can be deployed to the real world. It could be trained to supervise more servers than one and learn which functions restart which servers or what to do when there are complications and when it is appropriate to get a human involved.

Its functions can even be masks over sending messages to other actors (for instance to inform them of a context). If you have an distant actor trained to monitor or use a service that relies on the website to be up, for example, it can learn that when it detects the server goes down it should notify that distant actor so that the distant actor takes the appropriate behavior.


## Philosophy

The important thing is that these connections are learned by the actors. With the advent of the internet, and distributed systems we expect the actor model to become more and more popular because of its added layer of abstraction. We expect computing in general to be seen more as a protocol on a network than as serial instructions to one machine.

We expect to see more microservices and more intelligence to be injected into our distributed systems to make them adaptable, autonomous, resilient and robust. We see, therefore, the role of the programmer changing from one of micromanager to be one of steward and incentive designer, almost growing a system rather than engineering it. Less procedural and more declarative; putting things together before they exist.

We view intelligence, or at least general intelligence as a network effect, an emergent property of arising out of the interactions of nodes on a network. There is a feedback loop between the protocol, or language of a network and the structures that the network generates both in its internal connections and in the composition of each node. This feedback loop is the means of amplification of the inherent intelligence of the system. It is a strange loop, inherently, homeostatic (for a time), yet inherently chaotic and unpredictable because it's causes recede to the edges of the environment in which it is placed and the depths of the nuances in its internal dialogue.

Maestro represents an attempt to exemplify the above interpretation of what intelligence fundamentally is by creating a network of entirely naïve nodes that work together to achieve a certain goal. Their protocol does not evolve nor does their connections or internal computational structure to any significant degree but once these elements are statically created, different ways in which they can effect one another can be explored.


## Constraints

maestro, being a _naïve_ sensorimotor inference engine has a very limited scope
of environment which it can accurately model and command.

The most important constraint is that the environment have the Markov principle;
that the state space of its various configurations be a static structure.
maestro will explore this state space, it need not see it in it's entirety, but
it must be static in order to be predictable. If maestro is in a location in the
state space it has seen before and it does the exact behavior that it performed
last time, at that location, it should always get the same result.

The second constraint is that the environment be fully observable; that it has
no hidden variables. This is almost a restatement of the Markov property, but
its technically a different constraint - that is, it must have the Markov
property and it must be known to have the Markov property.

The third constraint is that the environment does not change state on its own.
That is, the maestro, when acting upon the system should be the only actor upon
the system. This, again, is almost a restating of the previous constraints.

The last constraint upon the environment is that the actions maestro can perform
upon it change only a specific subset the environment's representation and that
said actions always have an effect on the same subset.

This may look like a very constrained environment, however most logic puzzles
fit into this category of environments: an isolated (from any external force),
fully observable, static state-space, where all actions upon it alter only a
subset of its informational representation.

The Rubiks Cube, being a quintessential example of an environment like this,
has been chosen as our primary testing environment as it is a vast state-space,
somewhat complex, but uniform enough to not require a full exploration of the
space, that is, it's underlying relationships needn't be logically deduced.


## How maestro works

Maestro proof of concept is essentially a 2 layer higherarchy. One actor is 
initially created who is the "master" of all other actors. The Master node has
very different responsibilities than the network of nodes. His role is to create
the appropraite size of other nodes and serve as a conduit between the network
and the outside environment, passing information from the environment to the 
nodes and carrying out the will of the network upon the environment (performing
behaviors). The master node is the mother of the network, the eyes and voice of
the group.

The master node has 2 important roles:

1. Create all other actors as required by the environment. One actor will be
created for each combination of inputs from the environment. if the environment
is represented as 3 data points, A B and C maestro will make 6 subordinate
worker actors: one for A, one for B, C, AB, AC, BC. No node sees the entire 
picture, thus no node is assigned ABC. If B never changes unless C changes then 
B and C nodes can be removed, leaving only nodes A, AB, AC, and BC. 

2. Interface with the human operator and relay goals to the actors. And interface
with the environment to pass state representations to the actors. The master
node is the maestro. It doesn't know how to do anything, it makes little memory.
When a goal is given it is given in the form of how the environment should look
to the master node: 101. If the current state of the environment is 000 the
master node is tasked with the responsibility to choose the appropriate actions
to move the input state from 000 -> 101. It does this by relaying the task to
subordinate actors and waits for them to work it out amongst themselves. When a
consensus is reached about what action to take next the master node implements
the behavior and if the goal is reached notifies the human controller, if not,
the process repeats.

The way in which actors coordinate is naïve and simple as is their memory. Each
actor memorizes all environment-state-inputs paired with all behaviors taken
and the resulting outputs it has ever seen. Actors that have complete
consistency, that is the same input always leads to the same output, are prime
members of the society. Their input matters the most because in theory they're
the only ones that need to communicate with each other in order to visit any
desired state of the environment.

Goals are sent to this group first and only if they fail to achieve the goal are
other actors consulted. This prime group of actors broadcast the states closest
to the goal state that they know they can get to with actions. Other prime
actors listen to the broadcasts and see if any of the states correspond to an
input state that, given a certain action, can lead to the goal state. They
continue in this cacophony until either a hard limit of broadcasts are achieved
or a goal state is found.

If the goal state is found a special broadcast is made and that thread gets
passed up to the master node. The master node parses out the actions and does
the behaviors. If a goal state is not found, the closest one to the goal is
selected and passed up to the master. The master then decides how many of the
suggested actions to do, from at least the first, to all of them. Then he passes
back down to the prime actors the new state of the environment and the goal.

If too many failures to find the goal state are accrued, the master will start
speaking to the non-prime actors to get their input. If they fail to find a
solution the master will tell the human it has failed to achieve the desired
goal.


## Maestro Overview

[![Maestro Overview](https://github.com/LegitStack/maestro/blob/master/Maestro-overview.png)](https://github.com/LegitStack/maestro/blob/master/Maestro-overview.png)


## Installation

    maestro> python setup.py develop


## Getting Started

    maestro> maestro                # maestro is instantiated with one node by default
    maestro> tune                   # explore the environment with one node learning how many nodes need to be instantiated
    maestro> stop                   # stop all behaviors and activity, instantiate the right number of worker nodes
    maestro> tune                   # explore the environment with all nodes learning how the environment works
    maestro> stop                   # stop all behaviors and activity
    maestro> play <specific state>  # nodes work together with their learned memory to find a path to the goal

## Project Layout

maestro comes with a directory structure for the importation of external
modules, a package structure for the creation of internal modules, a notebooks
and playground area for data exploration and visualization, a models folder for
finished models, a tests folder for the creation of a test suite, documentation
folders and sphinx setup, and the skeleton of a flask web app front end.

Project Organization
--------------------
    maestro
    |
    ├── maestro           <-- Source code for use in this project.
    │   ├── bin           <-- Module: command line entry point into project.
    │   ├── config        <-- Module: configuration or settings files.
    │   ├── lib           <-- Module: common functions used by other modules.
    |   ├── simulations   <-- Module: environment simulations.
    │   └── core          <-- Module: core functionality.
    │
    ├── database          <-- Holds state of the actors upon shutdown.
    |
    ├── docs              <-- Holds all documentation (see sphinx-doc.org).
    │
    ├── notebooks         <-- Jupyter notebooks area for data exploration and
    │                         manual model creation.
    │
    ├── playground        <-- Exploration and experimentation area
    |                         (is ignored by git).
    │
    ├── tests             <-- Tests for source code.
    │
    ├── web               <-- Flask app web front end. Possible uses: make
    |                         documentation available or call workflow remotely.
    │
    ├── README.md         <-- README.md for developers using this project.
    ├── make.bat          <-- Skeleton Sphinx make file. `/maestro> make html`
    ├── setup.py          <-- Skeleton `/maestro> python setup.py develop`
    └── Dockerfile        <-- Skeleton Dockerfile for creating portable image.

--------

## Documentation

to remake documentation:
- delete contents of docs folder
- run `sphinx-quickstart`
- specify docs folder or move files into docs folder and modify make files after
- run `make html`
