'''
unit tests for a module in the project
run with:
/maestro> pytest tests
optional arguments: -vv --html=report.html
'''
import pytest
from maestro.core import user

@pytest.mark.skip
def test_some_function_in_core():
    assert user.entry() == True
