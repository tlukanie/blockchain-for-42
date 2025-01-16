// Import the WinnerStorage contract artifact
const TournamentScore = artifacts.require("TournamentScore");

module.exports = function (deployer) {
  // Deploy the WinnerStorage contract
  deployer.deploy(TournamentScore, 42);
};
