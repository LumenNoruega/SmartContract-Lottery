# Smart Contract Lottery 

This project is an Ethereum-based lottery with Chainlink VRF integration for random winner selection.

1- Users can enter the lottery using ETH, with the entry price set at $50 USD.
2- An admin will decide when the lottery ends.
3- The lottery will randomly select a winner.

Tests:
1-'mainnet-fork'
2-'development' con mocks
3-'testnet'

---- Historial de commits: ----

2024-02-09
- Added Chainlink VRF integration for random winner selection.
- Implemented AggregatorV3Interface for ETH/USD price feed to determine entrance fee.
- Added startLottery and endLottery functions to manage lottery state.
- Implemented fulfillRandomness function to select and reward the winner.
- Integrated Ownable contract from OpenZeppelin for owner-restricted actions.


2024-02-10
- Added Files:

helpful_scripts.py:
Utility functions for interacting with the Brownie network.
get_account(): Retrieves an account based on the environment (local, testnet, or mainnet).
get_contract(): Fetches an existing contract or deploys a mock if needed.
deploy_mocks(): Deploys mock contracts for local testing.
Defines variables for handling local environments and simulations.
Configures a gas strategy using LinearScalingStrategy.

deploy_lottery.py:
Uses get_account() to select the appropriate account.
Deploys Lottery with the ETH/USD price feed contract.
Imports functions from helpful_scripts.py.


2025-02-10
- Deployed Lottery contract on BNB Testnet using Brownie.
- Verified contract deployment on BscScan (Tx Hash:  0x158061627ccac0462459b269875fa104d112bc4079937ddcbb05d8a79cba40a5).
- Added MockV3Aggregator.sol for ETH/USD price feed simulation.
- Added VRFCoordinatorMock.sol to mock Chainlink VRF for randomness testing.
- Added LinkToken.sol to simulate LINK token interactions.


2025-02-11  
- Implemented lottery functions: `start_lottery()`, `enter_lottery()`, and `end_lottery()` to handle the lottery lifecycle.  
- Added `fund_with_link()` in `helpful_scripts.py` to transfer LINK tokens to contracts for Chainlink VRF requests.  
- Fixed variable names in `fulfillRandomness()` to correctly handle randomness.  
- Added `LinkTokenInterface.sol` for interacting with LINK tokens.  
- Implemented `gas_strategy` to prevent Ganache from freezing during transactions.  
