import requests
import pytest


def setup_module(module):
    # init_something()
    pass


def teardown_module(module):
    pass


def test_get():
    assert str(requests.get('http://localhost:5000/api/request/2')) == "<Response [200]>"


def test_dell():
    assert str(requests.delete('http://localhost:5000/api/request/1')) == "<Response [200]>"


def test_get_all():
    assert str(requests.get('http://localhost:5000/api/requests')) == "<Response [200]>"
