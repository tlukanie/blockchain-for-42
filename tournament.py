import pandas as pd
import json
from solcx import compile_standard
from web3 import Web3

player1_addr = "0x080851476334dbD780f33dAEf459b7604E7eFDdf"
player1_prvt_key = "0x76f4d16a89093d5c9e8a7e43520343f6ff6b8577e3e9a2ffb6290fbbb67b6e53"

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
contract_address = "0x5ccEF16e23DF50401195C3b7a45dE9781AA42029"

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

    #index +=1

    # signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    # tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # print(f"Transaction hash: {tx_hash.hex()}")


