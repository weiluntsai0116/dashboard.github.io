"""
tests/conftest.py
"""
import pytest


def pytest_addoption(parser):
    parser.addoption("--app", action="store", help="input app name(including directory and filename without extension)"
                                                   "ex: template.app")

@pytest.fixture
def params(request):
    params = {}
    params['app_name'] = request.config.getoption('--app')
    if params['app_name'] is None:
        pytest.skip()
    return params



