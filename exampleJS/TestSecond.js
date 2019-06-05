/* eslint-env mocha */
/* eslint-disable no-console */
/* global artifacts, contract, describe, it, expect */

const PROJECT_PATH = '/home/rm/Desktop/Solcover/'

const chai = require('chai')
const { assert } = chai
const chaiAsPromised = require('chai-as-promised')
chai.use(chaiAsPromised)

const fs = require('fs')
const TestContract = artifacts.require('R_ContractName')

contract('R_ContractName', (accounts) => {
    let testContract
    describe('', () => {
        it('R_FunctionName', async () => {
            testContract = await TestContract.new()

            const value = await testContract.R_FunctionName(R_Signature)

            // read from file
            const filename = 'R_ContractName.expect.out'
            const output = fs.readFileSync(PROJECT_PATH+'scripts/'+filename).toString()

            console.log("--> ", value.toNumber(), Number(output))
            if(value.toNumber() == Number(output)) {
                console.log("* pass")
            }
            else {
                // when occurs bug / vuln
                console.log("* fail")
                var data = ['R_ContractName', 'R_FunctionName', 'R_Inter','(R_Signature)', value.toNumber().toString(), output, '\n']
                fs.writeFileSync(PROJECT_PATH+"/output/bugReport", data, {
                    flag: 'a+'
                })
            }
        })
    })
})