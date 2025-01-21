import pandas as pd
import json
from solcx import compile_standard
from web3 import Web3

# Player and loser details
player1_addr = "0x52A67D88a11F075aAefFFC4AB2bF19aF92113589"
player1_prvt_key = "0x959a851d406255ddd71d207de6009bb9ec914f9f2eb48bc1e4eba1c619d9ee80"

loser_addr = "0x62a21945dF073aB157308786CE5Da0D06741E2f2"
loser_prvt_key = "0xce6b31a9968739ee4586b9ae142c288c1f935b434531e51c313f0b42c013d39a"

# Load CSV into a DataFrame
csv_file = "multisig_oneline.csv"
df = pd.read_csv(csv_file)

# Display the data
print(df.head())

# Load the contract JSON file (update the path to your file)
with open("./build/contracts/TournamentScore.json", "r") as file:
    contract_json = json.load(file)

# Extract the ABI from the JSON file
contract_abi = contract_json["abi"]

# Define the contract address
contract_address = "0xC0F7B0699BDDd1f423099B1e6fBdF713a95A6270"

# Connect to the Ethereum provider
web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# Initialize the contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Get the starting nonce for both users
player1_nonce = web3.eth.get_transaction_count(player1_addr)
loser_nonce = web3.eth.get_transaction_count(loser_addr)

# Check winner and loser addresses in the deployed contract
contract_winner = contract.functions.winner().call()
contract_loser = contract.functions.loser().call()

print(f"Contract Winner Address: {contract_winner}")
print(f"Contract Loser Address: {contract_loser}")
print(f"Player1 Address: {player1_addr}")
print(f"Loser Address: {loser_addr}")


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

    # Step 1: Approvals
    try:
        # Player 1 approves
        tx_approve_1 = contract.functions.approve().build_transaction({
            'from': player1_addr,
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'nonce': player1_nonce
        })

        signed_tx_1 = web3.eth.account.sign_transaction(tx_approve_1, player1_prvt_key)
        tx_hash_1 = web3.eth.send_raw_transaction(signed_tx_1.raw_transaction)
        print(f"Player1 approval sent: {tx_hash_1.hex()}")

        player1_nonce += 1

        # Loser approves
        tx_approve_2 = contract.functions.approve().build_transaction({
            'from': loser_addr,
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'nonce': loser_nonce
        })

        signed_tx_2 = web3.eth.account.sign_transaction(tx_approve_2, loser_prvt_key)
        tx_hash_2 = web3.eth.send_raw_transaction(signed_tx_2.raw_transaction)
        print(f"Loser approval sent: {tx_hash_2.hex()}")

        loser_nonce += 1

    except Exception as e:
        print(f"Error during approvals: {e}")
        continue

    # Step 2: Execute the transaction
    try:
        tx_execute = contract.functions.execute(
            row['tournament_id'],
            int(row['game_id']),
            row['game_type'],
            row['loser_name'],
            int(row['loser_score']),
            row['winner_name'],
            int(row['winner_score'])
        ).build_transaction({
            'from': player1_addr,
            'gas': 300000,
            'gasPrice': web3.eth.gas_price,
            'nonce': player1_nonce
        })

        signed_tx_execute = web3.eth.account.sign_transaction(tx_execute, player1_prvt_key)
        tx_hash_execute = web3.eth.send_raw_transaction(signed_tx_execute.raw_transaction)
        print(f"Execution transaction sent for row {index}: {tx_hash_execute.hex()}")

        player1_nonce += 1

    except Exception as e:
        print(f"Error during execution: {e}")
        continue


# test retrieving the data that was stored on the blockchain!!!
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