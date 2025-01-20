// Import the WinnerStorage contract artifact
const TournamentScore = artifacts.require("TournamentScore");

module.exports = function (deployer) {

	const winnerAddress = "0x5c37Dd916cCd0c8C9a04931ae017e9A4A094c654"; // Replace with actual address
    const loserAddress = "0xB732cC5ab65fa3e64516772a5F8842e59F162168";  
  // Deploy the WinnerStorage contract
  deployer.deploy(TournamentScore, winnerAddress, loserAddress);
};
