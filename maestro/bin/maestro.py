''' commandline entry point for the maestro project '''

from maestro.core import conductor
from maestro.simulations import cube

def main():
    ''' start a maestro ai '''
    conductor_node = conductor.ConductorNode(
        environment=cube.RubiksCube(),
        verbose=True)

if __name__ == '__main__':
    main()
