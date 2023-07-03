#!/usr/bin/python3

import brownie
import pytest
import time
import helpers

# one trader should win in the second round out of 6 traders,
# because he is betting down and other up, and final price will decrease
def test_big_trade_1(upVsDownGameV2, accounts, ether, irrevelent_num):

    helpers.complete_first_round(
        upVsDownGameV2,
        accounts,
        ether,
        irrevelent_num
    )

    trade_id_amount = {
        # id : {amount_to_bet, is_winner, account_index}
        "id1": (10*ether, False, 4),
        "id2": (5*ether, True, 5),
        "id3": (50*ether, True, 6),
        "id4": (10*ether, False, 7),
        "id5": (25*ether, False, 8),
        "id6": (30*ether, False, 9)
    }
    original_amt_before_trade = {} # dictionary for storing the inital balance of account

    print(original_amt_before_trade)

    winners_list = [] # will hold the ids of winner account ["id2","id3"..etc]
    for id in trade_id_amount:
        original_amt_before_trade[id] = accounts[trade_id_amount[id][2]].balance()
        # converting the trade_id_amount dict in actual txn
        upVsDownGameV2.makeTrade(
            (bytes(1), "avatar_"+id, "IN", not trade_id_amount[id][1], id),
            {"from": accounts[trade_id_amount[id][2]],
                "value": trade_id_amount[id][0]}
        )
        if trade_id_amount[id][1] == True:
            winners_list.append(id)

    # calculating the price, which will be distribute by the game contract
    winnings_list = helpers.calculate_winnings(
        upVsDownGameV2, 
        accounts, 
        trade_id_amount, 
        winners_list
    )

    # ========= starting the second round and closing it ================
    round_2_args_start = {
        "poolId": bytes(1),
        "timeMS": time.time(),
        "tradesStartTimeMS": time.time(),
        "tradesEndTimeMS": time.time() + 10,
        "price": 300,
        "batchSize": irrevelent_num
    }
    round_2_started = upVsDownGameV2.trigger(
        *round_2_args_start.values(), 
        {"from": accounts[1]}
    )

    round_2_args_end = {
        "poolId": bytes(1),
        "timeMS": time.time(),
        "tradesStartTimeMS": time.time(),
        "tradesEndTimeMS": time.time() + 10,
        "price": 200,
        "batchSize": len(winners_list)
    }
    round_2_ended = upVsDownGameV2.trigger(
        *round_2_args_end.values(), 
        {"from": accounts[1]}
    )

    print(str(round_2_ended.events))
    # print(str((round_2_ended.events["TradeWinningsSent"][0]["winningsAmount"])))

    assert (len(round_2_ended.events["TradeWinningsSent"]) == len(winners_list))

    # validating the distribute amount price, with the calculated price 
    for i in range(len(winners_list)):
        assert (round_2_ended.events["TradeWinningsSent"][i]["winningsAmount"] 
                == winnings_list[winners_list[i]])

    # validating balance of the non winners traders
    for id in trade_id_amount:
        if not trade_id_amount[id][1]:
            assert (accounts[trade_id_amount[id][2]].balance() ==
                    original_amt_before_trade[id] - trade_id_amount[id][0])

    # validating the accounts balance, after winning the bet
    for id in winnings_list:
        assert (accounts[trade_id_amount[id][2]].balance() == 
                winnings_list[id] + original_amt_before_trade[id])

    assert (len(round_2_ended.events["RoundDistributed"]) == 1)
    assert (round_2_ended.events["RoundDistributed"][0]["totalWinners"] 
            == len(winners_list))

# # in the below test, same trader is allowed to place multiple trades
# # irrespective of any argument, makeTrade function takes
# # five traders should win in the second round out of 6 traders,
# # because they are betting up and other up, and final price will increase
# def test_big_trade_2(upVsDownGameV2, accounts, ether, irrevelent_num):

#     helpers.complete_first_round(
#         upVsDownGameV2,
#         accounts,
#         ether,
#         irrevelent_num
#     )

#     # doing some trades
#     trade_1 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar1", "IN", True, "id1"),
#         {"from": accounts[4], "value": 10*ether}
#     )
#     print("trade 1:" + str(trade_1.events))

#     # this trade should win
#     trade_2 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar2", "IN", False, "id1"),
#         {"from": accounts[4], "value": 5*ether}
#     )
#     print("trade 2:" + str(trade_2.events))

#     trade_3 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar1", "IN", True, "id3"),
#         {"from": accounts[4], "value": 50*ether}
#     )
#     print("trade 3:" + str(trade_1.events))

#     trade_4 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar1", "US", True, "id4"),
#         {"from": accounts[4], "value": 10*ether}
#     )
#     print("trade 4:" + str(trade_1.events))

#     trade_5 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar1", "PK", True, "id5"),
#         {"from": accounts[4], "value": 25*ether}
#     )
#     print("trade 5:" + str(trade_1.events))

#     trade_6 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar1", "UK", True, "id6"),
#         {"from": accounts[4], "value": 30*ether}
#     )
#     print("trade 6:" + str(trade_1.events))

#     round_2_started = upVsDownGameV2.trigger(bytes(1), time.time(
#     ), time.time(), time.time() + 10, 300, irrevelent_num, {"from": accounts[1]})

#     round_2_ended = upVsDownGameV2.trigger(bytes(1), time.time(
#     ), time.time(), time.time() + 10, 400, 5, {"from": accounts[1]})

#     print(str(round_2_ended.events))
#     print(str((round_2_ended.events["TradeWinningsSent"][0]["winningsAmount"])))

#     # in the above trade there has to be 5 winners
#     assert (len(round_2_ended.events["TradeWinningsSent"]) == 5)

#     winnings = [0.38*ether, 1.9*ether, 0.38*ether, 0.95*ether, 1140000000000000000,]
#     for i in range(5):
#         assert (round_2_ended.events["TradeWinningsSent"]
#                 [i]["winningsAmount"] == winnings[i])

#     assert (len(round_2_ended.events["RoundDistributed"]) == 1)
#     assert (round_2_ended.events["RoundDistributed"][0]["totalWinners"] == 5)


# # five traders should win in the second round out of 6 traders,
# # because they are betting up and other up, and final price will increase
# @pytest.mark.parametrize("idx", range(0,3))
# def test_big_trade_3(upVsDownGameV2, accounts, ether, irrevelent_num, idx):

#     helpers.complete_first_round(
#         upVsDownGameV2,
#         accounts,
#         ether,
#         irrevelent_num
#     )

#     # doing some trades
#     trade_1 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar1", "IN", True, "id1"),
#         {"from": accounts[idx+0], "value": 10*ether}
#     )

#     # should lose
#     trade_2 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar2", "IN", False, "id2"),
#         {"from": accounts[idx+1], "value": 5*ether}
#     )
#     print("trade 2:" + str(trade_2.events))

#     trade_3 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar1", "IN", True, "id3"),
#         {"from": accounts[idx+2], "value": 50*ether}
#     )
#     print("trade 3:" + str(trade_1.events))

#     trade_4 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar1", "US", True, "id4"),
#         {"from": accounts[idx+3], "value": 10*ether}
#     )
#     print("trade 4:" + str(trade_1.events))

#     trade_5 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar1", "PK", True, "id5"),
#         {"from": accounts[idx+4], "value": 25*ether}
#     )
#     print("trade 5:" + str(trade_1.events))

#     trade_6 = upVsDownGameV2.makeTrade(
#         (bytes(1), "avatar1", "UK", True, "id6"),
#         {"from": accounts[idx+5], "value": 30*ether}
#     )
#     print("trade 6:" + str(trade_1.events))

#     round_2_started = upVsDownGameV2.trigger(bytes(1), time.time(
#     ), time.time(), time.time() + 10, 300, irrevelent_num, {"from": accounts[1]})

#     round_2_ended = upVsDownGameV2.trigger(bytes(1), time.time(
#     ), time.time(), time.time() + 10, 400, 5, {"from": accounts[1]})

#     print(str(round_2_ended.events))
#     print(str((round_2_ended.events["TradeWinningsSent"][0]["winningsAmount"])))

#     # in the above trade there has to be 5 winners
#     assert (len(round_2_ended.events["TradeWinningsSent"]) == 5)

#     winnings = [0.38*ether, 1.9*ether, 0.38*ether, 0.95*ether, 1140000000000000000,]
#     for i in range(5):
#         assert (round_2_ended.events["TradeWinningsSent"]
#                 [i]["winningsAmount"] == winnings[i])

#     assert (len(round_2_ended.events["RoundDistributed"]) == 1)
#     assert (round_2_ended.events["RoundDistributed"][0]["totalWinners"] == 5)
