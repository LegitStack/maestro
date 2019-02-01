'''
actors add entries to msgboard to:
1. submit training votes (training)
2. commit suicide (training)
3. invalidate or validate others work proposals (work)
4. propose a work path (work)

actors always listens to it for:
1. training state change (training)
2. issuance of a state to goal (work)
3. others proposals for analysis (work)

actors listen directly to master for:
1. master to change their mode

So the ator has 3 threads that all run concurrently.
    1.  listens to master
    2.  listens to the messageboard
    3.  performs serial computation at the behest of the others
        (mostly finds paths, analyses paths, or produces votes)
'''

import sys
from threading import Thread

class ActorNode():
    ''' unit of reactive memory/computation '''

    def __init__(self,
        verbose: bool = False,
        accepts_user_input: bool = False,
    ):
        ''' actor nodes contain little memory '''
        self.verbose = verbose
        self.exit = False
        if accepts_user_input:
            self.listen_to_user()




    def quit(self):
        self.exit = True
        exit()

    def listen_to_user(self):
        ''' concurrent listening '''
        def wire():
            print(f'listening to user input forever') if self.verbose else None
            commands = {
                'exit':self.quit, 'help':self.help_me,
                'start':self.help_me, 'explore':self.help_me, 'stop':self.help_me,
                'sleep':self.help_me, 'do':self.help_me,
            }

            while True:
                command = input('maestro> ')
                if command in commands.keys():
                    print(commands[command]())
                else:
                    print('invalid command. \n',self.help_me())

        threads = []
        threads.append(Thread(target=wire))

        try:
            threads[-1].start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

        print('listening to user input now') if self.verbose else None
        import time

        while True:
            time.sleep(10)
            if self.exit:
                sys.exit()
            print('sleeping')
