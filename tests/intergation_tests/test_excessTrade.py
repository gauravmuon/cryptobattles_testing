#!/usr/bin/python3

import brownie
import pytest
import time
from helpers import helper_complete_first_round


# checking the allowed limit trade boundry
def test_trade_more_than_allowed_limit(upVsDownGameV2, accounts, ether, irrevelent_num):

    helper_complete_first_round(
        upVsDownGameV2,
        accounts,
        ether,
        irrevelent_num
    )

    try:
        # trading more than allowed limit(100 ethers) should crash the call
        trade_1 = upVsDownGameV2.makeTrade(
            (bytes(1), "avatar1", "IN", True, "id1"),
            {"from": accounts[5], "value": 101*ether}
        )
        assert False
    except brownie.exceptions.VirtualMachineError:
        pass

