pragma solidity >=0.6.0 <0.9.0;

contract WinnerStorage {
    uint256 public score;

    // Event to emit when score is updated
    event scoreUpdated(uint256 oldscore, uint256 newscore);

    // Function to store a score
    function storeScore(uint256 _score) public {
        uint256 oldscore = score; // Store the current score value
        score = _score; // Update the score variable
        emit scoreUpdated(oldscore, _score); // Emit the event
    }

    // Function to retrieve the score
    function retrieve() public view returns (uint256) {
        return score;
    }
}