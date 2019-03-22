''' commandline entry point for the maestro project '''
import click

from maestro.core import conductor
from maestro.core import solo
from maestro.simulations import cube
from maestro.simulations import numberline
from maestro.simulations import maze


def get_environment(env):
    return {
        'cube1': cube.RubiksCubeOne,
        'cube2': cube.RubiksCubeTwo,
        'cube': cube.RubiksCube,
        'numberline': numberline.NumberLine,
        'maze': maze.Maze, }[env]


@click.group()
def main():
    ''' display help '''


@main.command()
@click.option(
    '-s', '--simulation',
    type=click.Choice(['cube1', 'cube2', 'cube', 'numberline', 'maze']),
    prompt=True)
def symphony(simulation):
    ''' start a maestro ai with conductor and musicians '''
    conductor.ConductorNode(
        environment=get_environment(simulation)(),
        verbose=True)


@main.command()
@click.option(
    '-s', '--simulation',
    type=click.Choice(['cube1', 'cube2', 'cube', 'numberline', 'maze']),
    prompt=True)
def artist(simulation):
    ''' start a maestro ai '''
    solo.SoloNode(
        environment=get_environment(simulation)(),
        verbose=True)
