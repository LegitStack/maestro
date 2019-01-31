''' user setup of system '''

from maestro.core import master
from maestro.core import actor

def entry():
    master_actor = actor.ActorNode(verbose=True, accepts_user_input=True)


def entry2(args=None):
    ''' loop with user '''
    def help_me():
        return '''
            commands:
            help     - displays this message
            start    - starts workers
            explore  - tells workers to explore
            stop     - tells workers to stop all activity
            sleep    - tells workers to analyse what they've learned
            do       - tells workers to achieve a goal
            exit     - exits maestro
            '''

    master_node = master.MasterNode()
    commands = {
        'exit':exit, 'help':help_me,
        'start':master_node.start, 'explore':help_me, 'stop':help_me,
        'sleep':help_me, 'do':help_me,
    }

    while True:
        command = input('maestro> ')
        if command in commands.keys():
            print(commands[command]())
        else:
            print('invalid command. \n',help_me())

    return True
