'''
entry point for the maestro project
'''

from maestro.core import user


def main():
    '''
    main entry point for the maestro project; runs the entire workflow
    '''
    print('running maestro!')
    print(user.entry())


if __name__ == '__main__':
    main()
