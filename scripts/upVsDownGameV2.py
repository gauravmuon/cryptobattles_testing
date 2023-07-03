#!/usr/bin/python3
from brownie import UpVsDownGameV2, accounts

# mind in accounts address 0 is owner and address 1 is game controller
def main():
    return UpVsDownGameV2.deploy(accounts[1], {'from': accounts[0]})
