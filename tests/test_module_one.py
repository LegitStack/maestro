'''
unit tests for a module in the project
run with:
/maestro> pytest tests
optional arguments: -vv --html=report.html
'''

from maestro.core import core_functionality


def test_some_function_in_core():
    something = core_functionality.some_function()
    assert something == True
