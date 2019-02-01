''' commandline entry point for the maestro project '''

from maestro.core import master
from maestro.lib import message_board
from maestro.simulations import cube

def main():
    ''' start a maestro ai '''

    master_node = master.MasterNode(
        msgboard=message_board.MSGBoard(),
        environment=cube.RubiksCube(),
        verbose=True)

    master_node.set_mode('train')


if __name__ == '__main__':
    main()
