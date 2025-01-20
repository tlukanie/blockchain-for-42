import pandas as pd
import json
from solcx import compile_standard
from web3 import Web3

# Player and loser details
player1_addr = "0x5c37Dd916cCd0c8C9a04931ae017e9A4A094c654"
player1_prvt_key = "0xcec5ae10620cb46a42eceb04a2f0e581ff1f07c7f469bde8d7b41f2147e80d77"

loser_addr = "0xB732cC5ab65fa3e64516772a5F8842e59F162168"
loser_prvt_key = "0x2f1c8e69244d21cbae697a81f3b1f04b5052bd2bb830f9300201999781297e87"

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