#!/usr/bin/python3

import brownie
import pytest
import time
import helpers


# checking the allowed limit trade boundry
def test_trade_more_than_allowed_limit(upVsDownGameV2, accounts, ether, irrevelent_num):

    helpers.complete_first_round(
        upVsDownGameV2,
        accounts,
        ether,
        irrevelent_num
    )

    try:
        # trading more than allowed limit(100 ethers) should crash the call
        trade_1 = upVsDownGameV2.makeTrade(
            list({
                "poolId": bytes(1),
                "avatarUrl": "avatar_1",
                "countryCode": "IN",
                "upOrDown": True,
                "whiteLabelId": "id_1",
            }.values()),
            {"from": accounts[5], "value": 101*ether}
        )
        assert False
    except brownie.exceptions.VirtualMachineError:
        pass

