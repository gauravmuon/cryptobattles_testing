#!/usr/bin/python3

import brownie
import pytest
import time
from helpers import helper_complete_first_round


# one trader should win in the second round out of 6 traders,
# because he is betting down and other up, and final price will decrease
def test_big_trade_1(upVsDownGameV2, accounts, ether, irrevelent_num):

    helper_complete_first_round(
        upVsDownGameV2,
        accounts,
        ether,
        irrevelent_num
    )

    # doing some trades
    trade_1 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "IN", True, "id1"),
        {"from": accounts[4], "value": 10*ether}
    )
    print("trade 1:" + str(trade_1.events))

    # should win
    trade_2 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar2", "IN", False, "id2"),
        {"from": accounts[5], "value": 5*ether}
    )
    print("trade 2:" + str(trade_2.events))

    trade_3 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "IN", True, "id3"),
        {"from": accounts[6], "value": 50*ether}
    )
    print("trade 3:" + str(trade_1.events))

    trade_4 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "US", True, "id4"),
        {"from": accounts[7], "value": 10*ether}
    )
    print("trade 4:" + str(trade_1.events))

    trade_5 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "PK", True, "id5"),
        {"from": accounts[8], "value": 25*ether}
    )
    print("trade 5:" + str(trade_1.events))

    trade_6 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "UK", True, "id6"),
        {"from": accounts[9], "value": 30*ether}
    )
    print("trade 6:" + str(trade_1.events))

    round_2_started = upVsDownGameV2.trigger(bytes(1), time.time(
    ), time.time(), time.time() + 10, 300, irrevelent_num, {"from": accounts[1]})

    round_2_ended = upVsDownGameV2.trigger(bytes(1), time.time(
    ), time.time(), time.time() + 10, 200, 1, {"from": accounts[1]})

    print(str(round_2_ended.events))
    print(
        str((round_2_ended.events["TradeWinningsSent"][0]["winningsAmount"])))

    assert (len(round_2_ended.events["TradeWinningsSent"]) == 1)
    assert (round_2_ended.events["TradeWinningsSent"]
            [0]["winningsAmount"] == 118.75*ether)
    assert (len(round_2_ended.events["RoundDistributed"]) == 1)
    assert (round_2_ended.events["RoundDistributed"][0]["totalWinners"] == 1)

# in the below test, same trader is allowed to place multiple trades
# irrespective of any argument, makeTrade function takes
# five traders should win in the second round out of 6 traders,
# because they are betting up and other up, and final price will increase
def test_big_trade_2(upVsDownGameV2, accounts, ether, irrevelent_num):

    helper_complete_first_round(
        upVsDownGameV2,
        accounts,
        ether,
        irrevelent_num
    )

    # doing some trades
    trade_1 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "IN", True, "id1"),
        {"from": accounts[4], "value": 10*ether}
    )
    print("trade 1:" + str(trade_1.events))

    # this trade should win 
    trade_2 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar2", "IN", False, "id1"),
        {"from": accounts[4], "value": 5*ether}
    )
    print("trade 2:" + str(trade_2.events))

    trade_3 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "IN", True, "id3"),
        {"from": accounts[4], "value": 50*ether}
    )
    print("trade 3:" + str(trade_1.events))

    trade_4 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "US", True, "id4"),
        {"from": accounts[4], "value": 10*ether}
    )
    print("trade 4:" + str(trade_1.events))

    trade_5 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "PK", True, "id5"),
        {"from": accounts[4], "value": 25*ether}
    )
    print("trade 5:" + str(trade_1.events))

    trade_6 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "UK", True, "id6"),
        {"from": accounts[4], "value": 30*ether}
    )
    print("trade 6:" + str(trade_1.events))

    round_2_started = upVsDownGameV2.trigger(bytes(1), time.time(
    ), time.time(), time.time() + 10, 300, irrevelent_num, {"from": accounts[1]})

    round_2_ended = upVsDownGameV2.trigger(bytes(1), time.time(
    ), time.time(), time.time() + 10, 400, 5, {"from": accounts[1]})

    print(str(round_2_ended.events))
    print(str((round_2_ended.events["TradeWinningsSent"][0]["winningsAmount"])))

    # in the above trade there has to be 5 winners
    assert (len(round_2_ended.events["TradeWinningsSent"]) == 5)

    winnings = [0.38*ether, 1.9*ether, 0.38*ether, 0.95*ether, 1140000000000000000,]
    for i in range(5):
        assert (round_2_ended.events["TradeWinningsSent"]
                [i]["winningsAmount"] == winnings[i])

    assert (len(round_2_ended.events["RoundDistributed"]) == 1)
    assert (round_2_ended.events["RoundDistributed"][0]["totalWinners"] == 5)



# five traders should win in the second round out of 6 traders,
# because they are betting up and other up, and final price will increase
@pytest.mark.parametrize("idx", range(0,3)) 
def test_big_trade_3(upVsDownGameV2, accounts, ether, irrevelent_num, idx):

    helper_complete_first_round(
        upVsDownGameV2,
        accounts,
        ether,
        irrevelent_num
    )

    # doing some trades
    trade_1 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "IN", True, "id1"),
        {"from": accounts[idx+0], "value": 10*ether}
    )
    print("trade 1:" + str(trade_1.events))

    # should win
    trade_2 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar2", "IN", False, "id2"),
        {"from": accounts[idx+1], "value": 5*ether}
    )
    print("trade 2:" + str(trade_2.events))

    trade_3 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "IN", True, "id3"),
        {"from": accounts[idx+2], "value": 50*ether}
    )
    print("trade 3:" + str(trade_1.events))

    trade_4 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "US", True, "id4"),
        {"from": accounts[idx+3], "value": 10*ether}
    )
    print("trade 4:" + str(trade_1.events))

    trade_5 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "PK", True, "id5"),
        {"from": accounts[idx+4], "value": 25*ether}
    )
    print("trade 5:" + str(trade_1.events))

    trade_6 = upVsDownGameV2.makeTrade(
        (bytes(1), "avatar1", "UK", True, "id6"),
        {"from": accounts[idx+5], "value": 30*ether}
    )
    print("trade 6:" + str(trade_1.events))

    round_2_started = upVsDownGameV2.trigger(bytes(1), time.time(
    ), time.time(), time.time() + 10, 300, irrevelent_num, {"from": accounts[1]})

    round_2_ended = upVsDownGameV2.trigger(bytes(1), time.time(
    ), time.time(), time.time() + 10, 400, 5, {"from": accounts[1]})

    print(str(round_2_ended.events))
    print(str((round_2_ended.events["TradeWinningsSent"][0]["winningsAmount"])))

    # in the above trade there has to be 5 winners
    assert (len(round_2_ended.events["TradeWinningsSent"]) == 5)

    winnings = [0.38*ether, 1.9*ether, 0.38*ether, 0.95*ether, 1140000000000000000,]
    for i in range(5):
        assert (round_2_ended.events["TradeWinningsSent"]
                [i]["winningsAmount"] == winnings[i])

    assert (len(round_2_ended.events["RoundDistributed"]) == 1)
    assert (round_2_ended.events["RoundDistributed"][0]["totalWinners"] == 5)
