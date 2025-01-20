// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract TournamentScore {
    // Event to emit when a game is added
    event GameAdded(
        string tournament_id,
        uint256 game_id,
        string game_type,
        string loser_name,
        uint256 loser_score,
        string winner_name,
        uint256 winner_score
    );

	// event TournamentInfoTracked(
	// 	string	tournament_id,
	// 	uint256 game_id
	// );

    // Struct definition
    struct Tournament {
        string tournament_id;
        uint256 game_id;
        string game_type;
        string loser_name;
        uint256 loser_score;
        string winner_name;
        uint256 winner_score;
    }

    // Mapping to store games by tournament ID and game ID
    mapping(string => mapping(uint256 => Tournament)) public tournaments;

	// // Mapping to track all game IDs in a tournament
    // mapping(string => uint256[]) public tournamentGameIds;

    // Function to add a game
    function addGame(
        string memory _tournament_id,
        uint256 _game_id,
        string memory _game_type,
        string memory _loser_name,
        uint256 _loser_score,
        string memory _winner_name,
        uint256 _winner_score
    ) public {
        // Ensure the game doesn't already exist
        require(
            bytes(tournaments[_tournament_id][_game_id].tournament_id).length == 0,
            "Game already exists"
        );

        // Add the game to the mapping
        tournaments[_tournament_id][_game_id] = Tournament(
            _tournament_id,
            _game_id,
            _game_type,
            _loser_name,
            _loser_score,
            _winner_name,
            _winner_score
        );

        // Emit the GameAdded event
        emit GameAdded(
            _tournament_id,
            _game_id,
            _game_type,
            _loser_name,
            _loser_score,
            _winner_name,
            _winner_score
        );
    }

    // // Function to retrieve a game
    // function getGame(string memory _tournament_id, uint256 _game_id)
    //     public
    //     view
    //     returns (Tournament memory)
    // {
    //     return tournaments[_tournament_id][_game_id];
    // }

	function getGame(string memory _tournament_id, uint256 _game_id)
		public
		view
		returns (Tournament memory)
	{
		Tournament memory game = tournaments[_tournament_id][_game_id];
		return game;
	}

	function getTournamentInfo(string memory _tournament_id, uint256 _game_id)
		public
		returns (Tournament memory)
	{
		Tournament memory all_data = tournaments[_tournament_id][_game_id];
		return all_data;

		// emit TournamentInfoTracked(_tournament_id, _game_id);
	}


}




