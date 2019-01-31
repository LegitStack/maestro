import sys
from threading import Thread

class ActorNode():
    '''  '''

    def __init__(self,
        verbose: bool = False,
        accepts_user_input: bool = False,
    ):
        '''  '''
        self.verbose = verbose
        self.exit = False
        if accepts_user_input:
            self.listen_to_user()


    @staticmethod
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
