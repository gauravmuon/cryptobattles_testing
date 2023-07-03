#!/usr/bin/python3

import pytest

@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass

@pytest.fixture(scope="module")
def upVsDownGameV2(UpVsDownGameV2, accounts):
    # address 0 will be owner ie (msg.sender), and 1 will be game controller
    return UpVsDownGameV2.deploy(accounts[1], {'from': accounts[0]})

@pytest.fixture
def ether():
   return 1e18

@pytest.fixture
def irrevelent_num():
   return 1
