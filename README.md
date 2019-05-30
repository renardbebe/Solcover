# play-with-solcoverage

### Requirements
```
Truffle v5.0.4 (core: 5.0.4)
Node v10.15.3
```

### setup
 
```bash
npm i
```
### Run 
```
npx solidity-coverage
Generating coverage environment
Running: truffle compile
(this can take a few seconds)...
Compiling ./contracts/Migrations.sol...
Compiling ./contracts/NewContract.sol...
Writing artifacts to ./build/contracts

Skipping instrumentation of  ./coverageEnv/contracts/Migrations.sol
Instrumenting  ./coverageEnv/contracts/NewContract.sol
Running: truffle compile
(this can take a few seconds)...
Compiling ./contracts/Migrations.sol...
Compiling ./contracts/NewContract.sol...
Writing artifacts to ./build/contracts

Launched testrpc on port 8555
Running: export ETHEREUM_RPC_PORT=8555&& truffle test --network coverage --timeout 10000
(this can take a few seconds)...
Using network 'coverage'.



  Contract: NewContract
    New contract 
      ✓ contract should deploy (50ms)
      ✓ should return 1+1 = 2 (88ms)


  2 passing (158ms)

------------------|----------|----------|----------|----------|----------------|
File              |  % Stmts | % Branch |  % Funcs |  % Lines |Uncovered Lines |
------------------|----------|----------|----------|----------|----------------|
 contracts/       |       50 |      100 |       50 |       50 |                |
  NewContract.sol |       50 |      100 |       50 |       50 |             19 |
------------------|----------|----------|----------|----------|----------------|
All files         |       50 |      100 |       50 |       50 |                |
------------------|----------|----------|----------|----------|----------------|

Istanbul coverage reports generated
Cleaning up...
Shutting down testrpc-sc (pid 12215)
Done.
``` 
