import pandas as pd
import json
from solcx import compile_standard
from web3 import Web3

player1_addr = "0x080851476334dbD780f33dAEf459b7604E7eFDdf"
player1_prvt_key = "0x76f4d16a89093d5c9e8a7e43520343f6ff6b8577e3e9a2ffb6290fbbb67b6e53"

loser_addr = "0x0A0b552f1d7Bb140652689CF9A209637bFd58218"
loser_prvt_key = "0x267883e6844ae3b1b4b3f102f436ebab8a61f17ac4e2b6b7cce9f7171f44611d"

# Load CSV into a DataFrame
csv_file = "tournament_results.csv"
df = pd.read_csv(csv_file)

# Display the data
print(df.head())

# Load the contract JSON file (update the path to your file)
with open("./build/contracts/TournamentScore.json", "r") as file:
    contract_json = json.load(file)

# Extract the ABI from the JSON file
contract_abi = contract_json["abi"]
print(contract_abi)
# Define the contract address
contract_address = "0x33CCD09ADB0a36929BA27eC50e3d22cD356ECec9"
# Connect to the Ethereum provider
web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# Initialize the contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Get the starting nonce
nonce = web3.eth.get_transaction_count(player1_addr)




for index, row in df.iterrows():
    print(row)
    print("index: ", index)

    # Pre-check if the game already exists in the contract
    try:
        game_exists = contract.functions.getGame(
            row['tournament_id'], 
            int(row['game_id'])
        ).call()

        if game_exists[1] != 0:  # If the game ID is non-zero, it exists
            print(f"Skipping existing game: {row['tournament_id']} - {row['game_id']}")
            continue
    except Exception as e:
        print(f"Error checking game existence: {e}")
        continue

    tx = contract.functions.addGame(
        row['tournament_id'],
        int(row['game_id']),
        row['game_type'],
        row['loser_name'],
        int(row['loser_score']),
        row['winner_name'],
        int(row['winner_score'])
    ).build_transaction({
        'from': player1_addr,
        'gas': 200000,
		'gasPrice': web3.eth.gas_price,
        'nonce': nonce
    })


	# Sign and send the transaction for player1
    private_key = player1_prvt_key
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # print("Transaction for Player #1 sent with hash:", tx_hash.hex())
    print(f"Transaction for row {index} sent with hash: {tx_hash.hex()}")

    nonce += 1

	

# getting all the related information about games in the tournament
tourn_id = "dream_88"
print("Tournament_id is " + tourn_id)
for gm_ctr in range(1,4):
	try:
		# print(gm_ctr)
		game_id = contract.functions.getGame(tourn_id, gm_ctr).call()
		if game_id[1] != 0:  # If the game ID is non-zero, it exists
			tourn_info = contract.functions.getTournamentInfo(tourn_id, gm_ctr).call()
			print("Game #",end='')
			print(gm_ctr, end='')
			print(" ", end='')
			print(tourn_info)			
	except Exception as e:
		print(f"Error checking game existence: {e}")
		continue