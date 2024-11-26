import json
from solcx import compile_standard
from web3 import Web3

player_1 = int(input("Enter number for the Player #1: "))
player_2 = int(input("Enter number for the Player #2: "))
if player_1 > player_2:
	winner = player_1
elif player_2 > player_1:
	winner = player_2
else:
	winner = 0

print(winner)

#store result on blockchain for each of the players on two separate addresses
