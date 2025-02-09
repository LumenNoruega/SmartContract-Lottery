# Smart Contract Lottery 

Este proyecto es una lotería basada en Ethereum con integración de Chainlink VRF para selección aleatoria de ganadores. 

1- los usuarios podran entran en la loteria usando ETH cuyo precio estará basado en USD -> 50$
2- un admin va a decidir cuando la loteria se termina
3- la loteria va a seleccionar un ganador de manera aleatoria

- tests:
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
