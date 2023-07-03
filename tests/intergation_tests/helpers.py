import time

# this not test case but helper, it is used for starting and ending the first round
def helper_complete_first_round(upVsDownGameV2, accounts, ether, irrevelent_num):
    # starting the game by owner account
    game_started = upVsDownGameV2.startGame({"from": accounts[0]})
    # creating a pool by game controller account
    pool_1 = upVsDownGameV2.createPool(
        bytes(1), 5*ether, 100*ether, 50*ether, {"from": accounts[1]})

    round_1_started = upVsDownGameV2.trigger(bytes(1), time.time(
    ), time.time(), time.time() + 10, 300, irrevelent_num, {"from": accounts[1]})

    round_1_ended = upVsDownGameV2.trigger(bytes(1), time.time() + 10, time.time(
    ) + 10, time.time() + 10, 400, 0, {"from": accounts[1]})

    # confirm if no pending distributions
    has_pending_distribution = upVsDownGameV2.hasPendingDistributions(bytes(1))
    assert has_pending_distribution == False

    return [game_started, pool_1, round_1_started, round_1_ended]