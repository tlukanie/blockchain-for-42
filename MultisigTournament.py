import pandas as pd
import json
from solcx import compile_standard
from web3 import Web3

# Player and loser details
player1_addr = "0xdA95FE8C72182b8A01FC948CA6675577568e664E"
player1_prvt_key = "0x46f984c865b7d10800a66816f786b2a6a2de6d95139eee53054928970f62b58d"

loser_addr = "0xf487e94f21A4f7a8B997793a6D3985789756824A"
loser_prvt_key = "0x3d90f29aa2ac72216cd1b56a6d8c98023a41482e249f2c99891707fe4f8f59e7"

# Load CSV into a DataFrame
csv_file = "multisig_oneline.csv"
df = pd.read_csv(csv_file)

# Display the data
print("Loaded Data:")
print(df.head())

# Load the contract JSON file (update the path to your file)
with open("./build/contracts/MultisigTournament.json", "r") as file:
    contract_json = json.load(file)

# Extract the ABI from the JSON file
contract_abi = contract_json["abi"]

# Define the contract address
contract_address = "0xFcc642f1924C09c46e0D286533389f6A877b2155"  # Replace with your deployed address

# Connect to the Ethereum provider
web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# Initialize the contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Get the starting nonce for both users
player1_nonce = web3.eth.get_transaction_count(player1_addr)
loser_nonce = web3.eth.get_transaction_count(loser_addr)

# Iterate through the CSV rows
for index, row in df.iterrows():
    print(f"Processing row {index}...")

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

    # Step 1: Add a game dynamically
    try:
        tx_add_game = contract.functions.addGame(
            row["tournament_id"],
            int(row["game_id"]),
            row["game_type"],
            row["loser_name"],
            int(row["loser_score"]),
            row["winner_name"],
            int(row["winner_score"]),
            player1_addr,
            loser_addr
        ).build_transaction({
            'from': player1_addr,
            'gas': 300000,
            'gasPrice': web3.eth.gas_price,
            'nonce': player1_nonce
        })

        signed_tx_add_game = web3.eth.account.sign_transaction(tx_add_game, player1_prvt_key)
        tx_hash_add_game = web3.eth.send_raw_transaction(signed_tx_add_game.raw_transaction)
        print(f"Game added. Transaction hash: {tx_hash_add_game.hex()}")

        player1_nonce += 1

    except Exception as e:
        print(f"Error adding game: {e}")
        continue

    # Step 2: Approvals
    try:
        # Player 1 approves
        tx_approve_1 = contract.functions.approve(row["tournament_id"], int(row["game_id"])).build_transaction({
            'from': player1_addr,
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'nonce': player1_nonce
        })

        signed_tx_approve_1 = web3.eth.account.sign_transaction(tx_approve_1, player1_prvt_key)
        tx_hash_approve_1 = web3.eth.send_raw_transaction(signed_tx_approve_1.raw_transaction)
        print(f"Player 1 approval sent: {tx_hash_approve_1.hex()}")

        player1_nonce += 1

        # Loser approves
        tx_approve_2 = contract.functions.approve(row["tournament_id"], int(row["game_id"])).build_transaction({
            'from': loser_addr,
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'nonce': loser_nonce
        })

        signed_tx_approve_2 = web3.eth.account.sign_transaction(tx_approve_2, loser_prvt_key)
        tx_hash_approve_2 = web3.eth.send_raw_transaction(signed_tx_approve_2.raw_transaction)
        print(f"Loser approval sent: {tx_hash_approve_2.hex()}")

        loser_nonce += 1

    except Exception as e:
        print(f"Error during approvals: {e}")
        continue

    # Step 3: Execute the transaction
    try:
        tx_execute = contract.functions.execute(
            row["tournament_id"],
            int(row["game_id"]),
            row["game_type"],
            row["loser_name"],
            int(row["loser_score"]),
            row["winner_name"],
            int(row["winner_score"]),
            player1_addr,
            loser_addr
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

# Retrieve and display tournament data
tournament_id = "her_dream"  # Replace with a valid tournament ID
print(f"\nRetrieving games for Tournament ID: {tournament_id}")

for game_id in range(1, 4):
    # is_approved = contract.functions.getApproval(tournament_id, game_id).call()
    # print(is_approved)
    try:
        game = contract.functions.getGame(tournament_id, game_id).call()
        if game[1] != 0:  # If the game ID is non-zero, it exists
            print(f"Game {game_id}: {game}")
    except Exception as e:
        print(f"Error retrieving game {game_id}: {e}")

# testing whether info is fully approved
is_approved = contract.functions.getApproval("her_dream", 2).call()
print(is_approved)
is_approved = contract.functions.getApproval("her_dream", 3).call()
print(is_approved)