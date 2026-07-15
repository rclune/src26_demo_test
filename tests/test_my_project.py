"""Dummy tests for the example package.

These exist to give the ``tests`` workflow something to run and to prove the
CI pipeline works end to end. They exercise the example ``my_project`` package
rather than testing real logic.
"""

import my_project
from my_project import common_function


def test_demo_data_constant():
    assert my_project.DEMO_DATA == "THIS IS A DEMONSTRATION"


def test_common_function_appends():
    assert common_function("foo") == "foo appended to the string!"
