pragma solidity >=0.4.25 <0.9.0;

contract ValueStorage {
	enum StateType_vs {Request}

    StateType_vs public  State;
    address public  Requestor;
    //address public  Responder;

    string public RequestMessage;
    //string public ResponseMessage;

    constructor(string memory message) {
        Requestor = msg.sender;
        RequestMessage = message;
        State = StateType_vs.Request;
    }

    // call this function to send a request
    function SendRequest(string memory requestMessage) public {

        if (Requestor != msg.sender) {
            revert();
        }

        RequestMessage = requestMessage;
        State = StateType_vs.Request;
    }
}
