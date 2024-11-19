# blockchain-for-42
trascendence, blockhain, solidity, ethereum
<h2>Useful links</h2>
<h3>1. Storing Data on Ethereum Blockchain With Python</h3>
<p>Link: https://medium.com/geekculture/storing-data-on-ethereum-blockchain-with-python-c76e6d91383f . Since only two options for tests of blockchain exist, could be useful to test ganashe (not in-browser) and understand how to check data on blockchain. Not suitable for the project, because it's solutions that doesn;t require to code anything on solidity.</p>
<h3>2. Basic info about Ethereum blockchain</h3>
<p>Link: https://www.geeksforgeeks.org/how-to-store-data-on-ethereum-blockchain/</p>
<h3>3. What type of data to actually store on blockchain</h4>
<p>Link: https://stackoverflow.com/questions/50781062/storing-users-data-on-ethereum-blockchain. Only hash or all the info??? </p>
<h3>4. Blockchain deployment as 4th service in docker apart from frontend, backend, db???</h3>
<p>Link: https://www.abastos.dev/projects/transcendence/</p>
<h4>5. Running ganachee</h4>
<p>./ganache-2.7.1-linux-x86_64.AppImage </p>
<h4>6. Building solidity project using truffle for vscode</h4>
<p>Link: https://archive.trufflesuite.com/blog/build-on-web3-with-truffle-vs-code-extension/</p>
<h2>12.11.24</h2>
<h4>7. Deploy Solidity Smart Contracts with Ganache</h4>
<p>Link: https://www.youtube.com/watch?v=UnNPv6zEbwc&t=171s/p>
<p>Folder: truffle_smart_contract_1, truffle develop -> migrate -> CANT DEPLOY ToDo.sol . Maybe problems with migration .js file?</p>
<h4>8. How to use ganache gui with truffle !</h4>
<p>Link: https://www.youtube.com/watch?v=aRJA1r1Gwu0</p>
<h4>9.Website to check ethereum raw transactions</h4>
<p>Link: https://rawtxdecode.in/</p>
<h4>Commands to create smart contract + create new solidity project</h4>
<ol>
  <li>npx truffle test</li>
  <li>npx truffle init</li>
</ol>
<h4>10. Examples of blockchain implementation in other 42 transcendence projects</h4>
<p>Link: https://github.com/DGross245/42-ft_transcendence/tree/master/contracts</p>
<h2>Tasks for 19.11.24</h2>
<p>1. Instead of only creation of the contract on blockchain, test contract call, events, retrieve the stored data on blockchain</p>
<p>2.Test other frameworks and local development environments</p>
<h3>Current folder</h3>
<h4>Compilation</h4>
<p>truffle compile</p>
<h4>Deployment</h4>
<p>truffle migrate</p>
<h4>Contract interaction</h4>
<p>truffle console</p>
<p>in terminal use tests from store.js to call the function in the contract</p>
<p>if needed to call the function at the specified address use:</p>
<p>const HelloBlockchain = await artifacts.require("HelloBlockchain"); <br>
const instance = await HelloBlockchain.at("0xYourContractAddressHere");
</p>

