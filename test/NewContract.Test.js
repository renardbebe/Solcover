/* eslint-env mocha */
/* eslint-disable no-console */
/* global artifacts, contract, describe, it, expect */

const chai = require('chai')
const { assert } = chai
const chaiAsPromised = require('chai-as-promised')
chai.use(chaiAsPromised)

const TestContract = artifacts.require('NewContract')

contract('NewContract', (accounts) => {
    let testContract
    describe('', () => {
        it('contract should deploy', async () => {
            testContract = await TestContract.new()
        })
        it('should return 1+1 = 2', async () => {
            testContract = await TestContract.new()

            const value = await testContract.sum(1,1)

            assert.equal(
                value.toNumber(),
                2
            )
        })
    })
})