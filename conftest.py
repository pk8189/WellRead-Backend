from os import system

import pytest


@pytest.fixture(scope="session")
def clear_files_teardown():
    yield None
    system("rm -rf test.db")
