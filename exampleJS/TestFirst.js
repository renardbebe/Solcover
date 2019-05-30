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

            const value = await testContract.R_Signature()

            // write expected output to file
            const filename = 'expectOut'
            fs.writeFileSync(path+filename, value)
        })
    })
})