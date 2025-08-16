from web3 import Web3
import sys

# Connect to Monad Testnet RPC
rpc_url = "https://rpc.ankr.com/monad_testnet"
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Verify connection
if not w3.is_connected():
    with open("result.txt", "w") as f:
        f.write("Failed to connect to Monad Testnet RPC\n")
    sys.exit(1)

# Read addresses from diachi.txt
try:
    with open("diachi.txt", "r") as file:
        addresses = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    with open("result.txt", "w") as f:
        f.write("Error: diachi.txt not found\n")
    sys.exit(1)
except Exception as e:
    with open("result.txt", "w") as f:
        f.write(f"Error reading diachi.txt: {e}\n")
    sys.exit(1)

# Open result.txt for writing
with open("result.txt", "w") as f:
    # Check balance for each address
    for address in addresses:
        try:
            # Validate and convert to checksum address
            if not w3.is_address(address):
                f.write(f"Invalid address: {address}\n\n")
                continue
            checksum_address = w3.to_checksum_address(address)
            
            # Get balance in Wei
            balance_wei = w3.eth.get_balance(checksum_address)
            
            # Convert Wei to MON (1 MON = 10^18 Wei)
            balance_mon = w3.from_wei(balance_wei, 'ether')
            
            # Write to file
            f.write(f"Address: {checksum_address}\n")
            f.write(f"Balance: {balance_mon} MON\n\n")
            
        except Exception as e:
            f.write(f"Error checking balance for {address}: {e}\n\n")