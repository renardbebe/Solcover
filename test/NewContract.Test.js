/* eslint-env mocha */
/* eslint-disable no-console */
/* global artifacts, contract, describe, it, expect */

const chai = require('chai')
const { assert } = chai
const chaiAsPromised = require('chai-as-promised')
chai.use(chaiAsPromised)

const NewContract = artifacts.require('NewContract')

contract('NewContract', (accounts) => {
    let newContract
    describe('New contract ', () => {
        it('contract should deploy', async () => {
            newContract = await NewContract.new()
        })
        it('should return 1+1 = 2', async () => {
            newContract = await NewContract.new()

            const value = await newContract.sum(1,1)

            assert.equal(
                value.toNumber(),
                2
            )
        })
    })
})