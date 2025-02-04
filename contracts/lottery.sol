// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../interfaces/AggregatorV3Interface.sol";

contract Lottery {

    address payable[] public players;
    uint public usdEnterFee;

    AggregatorV3Interface internal ethUsdPriceFeed;

    event PriceUpdated(int256 price);

    constructor(address _ethUsdPriceFeed) {
        usdEnterFee = 50 * (10 ** 18);
        ethUsdPriceFeed = AggregatorV3Interface(_ethUsdPriceFeed);
    }

    function enter() public payable {
        players.push(payable(msg.sender));

        // Emitir el precio cuando un jugador entre
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        emit PriceUpdated(price);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        require(price > 0, "Invalid price data from price feed");
        uint256 adjustedPrice = uint256(price) * 10 ** 10;
        uint256 costToEnter = (usdEnterFee * 10 ** 18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public {}

    function endLottery() public {}
}
