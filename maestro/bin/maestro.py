''' commandline entry point for the maestro project '''

from maestro.core import conductor
from maestro.core import solo
from maestro.simulations import cube


def main():
    ''' start a maestro ai '''
    conductor.ConductorNode(
        environment=cube.RubiksCubeTwo(),
        verbose=True)


def main_solo():
    ''' start a maestro ai '''
    solo.SoloNode(
        environment=cube.RubiksCubeTwo(),
        verbose=True)


if __name__ == '__main__':
    # main()
    main_solo()
