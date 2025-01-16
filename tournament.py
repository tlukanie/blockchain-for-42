import pandas as pd
import json
from solcx import compile_standard
from web3 import Web3

player1_addr = "0x5088E4721F2f41CE08a285EFe7ec78d240f60029"
player1_prvt_key = "0xf7f078b25a08f3a827c50941de2167c44924161cf5d89563af562370bf784562"

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
contract_address = "0x48a8d6474a19f523Cf4ec2D8aFC9911EA1A1638b"

# Connect to the Ethereum provider
web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# Initialize the contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)




for index, first_row in df.iterrows():
    tx = contract.functions.addGame(
        first_row['tournament_id'],
        int(first_row['game_id']),
        first_row['game_type'],
        first_row['loser_name'],
        int(first_row['loser_score']),
        first_row['winner_name'],
        int(first_row['winner_score'])
    ).build_transaction({
        'from': player1_addr,
        'gas': 200000,
		'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(player1_addr)
    })


	# Sign and send the transaction for player1
private_key = player1_prvt_key
signed_tx = web3.eth.account.sign_transaction(tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("Transaction for Player #1 sent with hash:", tx_hash.hex())

    # signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    # tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # print(f"Transaction hash: {tx_hash.hex()}")


