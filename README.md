# maestro
================

maestro is an actor-model framework for creating intelligent autonomous actors.


## Current Status

maestro is currently in a prototype phase.


## Theory

Each actor has 4 things: behaviors as predefined functions, input data which is
ultimately derived from the external environment, contextual information
received from fellow actors, and a specific goal in terms of what they should
get their input data to look like.

Once you have a system defined with each actor having functionality and set to
receive messages from the correct other actors, you train the actors by letting
them explore their behaviors at random, attempting to achieve their goals in the
most efficient way possible. This training is done in an isolated environment.

Once the actors are trained they are put to work in the real environment. The
idea behind this is that they can maintain, or bring about any state of that
environment by working together and coordinating their efforts in the way they
learned during training.


## Example

A perfect use case is a web server supervisor. It is given a goal to make sure
the website is up and that not more than one instance of the webserver is
running. This is a single actor example. During training it can learn how its
behaviors manipulate the environment: one function it can call kills all
instances of the webserver while another function starts one.

After it learns how to restart the server as soon as it crashes it can be
deployed to the real world. It could be trained to supervise more servers than
one and learn which functions restart which servers or what to do when there are
complications and when it is appropriate to get a human involved.

Its functions can even be masks over sending messages to other actors (for
instance to inform them of a context). If you have an distant actor trained to
monitor or use a service that relies on the website to be up, for example, it
can learn that when it detects the server goes down it should notify that
distant actor so that the distant actor takes the appropriate behavior.


## Philosophy

The important thing is that these connections are learned by the actors. With
the advent of the internet, and distributed systems we expect the actor model to
become more and more popular because of its added layer of abstraction. We
expect computing in general to be seen more as a protocol on a network than as
serial instructions to one machine.

We expect to see more microservices and more intelligence to be injected into
our distributed systems to make them adaptable, autonomous, resilient and
robust. We see, therefore, the role of the programmer changing from one of
micromanager to be one of steward and incentive designer, almost growing a
system rather than engineering it. Less procedural and more declarative; putting
things together before they exist.

We view intelligence, or at least general intelligence as a network effect, an
emergent property of arising out of the interactions of nodes on a network.
There is a feedback loop between the protocol, or language of a network and the
structures that the network generates both in its internal connections and in
the composition of each node. This feedback loop is the means of amplification
of the inherent intelligence of the system. It is a strange loop, inherently,
homeostatic (for a time), yet inherently chaotic and unpredictable because it's
causes recede to the edges of the environment in which it is placed and the
depths of the nuances in its internal dialogue.

maestro represents an attempt to exemplify the above interpretation of what 
intelligence fundamentally is by creating a network of entirely naive nodes that
work together to achive a certain goal. Their protocol does not evolve nor does
their connections or internal computational structure to any significant degree
but once these elements are statically created, different ways in which they can
effect one another can be explored.


## Constraints

maestro only works in environment that are static - that is the state space does
not change. If maestro is in the same location in the state space and does the
exact same behavior as last time it should always get the same result. The
environment also, therefore, needs to be fully observable. Only in this simple
environment can the maestro learn, as it's understanding is (at least in its
prototypical iteration) entirely naïve and unsophisticated.


## How maestro works

maestro can work in one of two ways: manual and automatic. An example of a
manual setup is shown above. Each actor is designed and placed in a specific
role. This set up is best for situations where the entire environment may not
be able to be replicated in a simulation.

If the environment is completely simulated, though, (or if the training
environment is the working environment) maestro can run in automatic mode. In
this setup one actor is initially created who is the "master" of all other
actors.

The master node has 2 important roles:

1. Create all other actors as required by the environment. One actor will be
created for each combination of inputs from the environment. if the environment
is represented as 3 data points, A B and C maestro will make 6 subordinate
worker actors: one for A, one for B, C, AB, AC, BC. The master node is
automatically assigned ABC.

2. Interface with the human operator and relay goals to the actors. The master
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





## Installation

coming soon


## Getting Started

coming soon


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
    ├── venv              <-- Virtual Environments folder for `virtualenv`.
    │
    ├── web               <-- Flask app web front end. Possible uses: make
    |                         documentation available or call workflow remotely.
    │
    ├── README.md         <-- README.md for developers using this project.
    ├── make.bat          <-- Sphinx make file. `/maestro> make html`
    ├── setup.py          <-- `/maestro> python setup.py develop`
    └── Dockerfile        <-- Skeleton Dockerfile for creating portable image.

--------

## Documentation

to remake documentation:
- delete contents of docs folder
- run sphinx-quickstart
- specify docs folder or move files into docs folder and modify make files after
- run make html
