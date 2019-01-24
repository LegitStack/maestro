'''
entry point for the maestro project
'''

from maestro.core import core_functionality


def run_workflow():
    '''
    main entry point for the maestro project; runs the entire workflow
    '''
    print('running maestro!')
    print(core_functionality.some_function())
