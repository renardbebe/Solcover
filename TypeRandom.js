const { isArray } = require('underscore')
const { getType } = require('solidity-types')


function flipBitAt(buf, position) {
  buf[position >> 3] ^= (128 >> (position & 7))
}

function flipByteAt(buf, position) {
  buf[position] ^= 0xFF
}

function flipTwoBytesAt(buf, position) {
  buf[position] ^= 0xFF
  buf[position + 1] ^= 0xFF
}

function flipFourBytesAt(buf, position) {
  buf[position] ^= 0xFF
  buf[position + 1] ^= 0xFF
  buf[position + 2] ^= 0xFF
  buf[position + 3] ^= 0xFF
}

function mutate(buf) {
  const len = buf.length
  const position = Math.floor((Math.random() * len) + 1)
  const strategy = Math.floor((Math.random() * 4) + 1)
  switch (strategy) {
    case 1: {
      flipBitAt(buf, position)
      break
    }
    case 2: {
      flipByteAt(buf, position)
      break
    }
    case 3: {
      flipTwoBytesAt(buf, position)
      break
    }
    case 4: {
      flipFourBytesAt(buf, position)
      break
    }
    default: {
      throw new Error('Unknown case')
    }
  }
}

function getEachTypeRandom(type) {
  this.type = type
  this.input = ''
  const t = this.type.startsWith('address')
    ? getType(this.type.replace('address', 'address-with-type'), 24)
    : getType(this.type)
  const buf = t.getValue()
  mutate(buf)
  t.setValue(buf)
  const inputValue = t.decode()
  if (this.type.startsWith('address')) {
    if (isArray(inputValue)) {
      if (isArray(inputValue[0])) {
        // Array of array
        this.input = inputValue.map(iv => iv.map((ii) => {
          const balance = `0x${ii.slice(ii.length - 8)}`
          const address = ii.slice(0, ii.length - 8)
          this.accounts.push({ balance, address })
        }))
      }
      // Array
      this.input = inputValue.map((iv) => {
        const address = iv.slice(0, iv.length - 8)
      })
    }
    // Plain
    const address = inputValue.slice(0, inputValue.length - 8)
    this.input = address
  } else if (this.type.startsWith('bool')) {
    const randomNum = Math.floor((Math.random() * 10) + 1)
    if (randomNum > 5) {
      this.input = '0'
    } else {
      this.input = '1'
    }
  } else {
    this.input = inputValue
  }
  return this.input
}

function toNonExponential(num) {  // str
  return (num-0).toLocaleString().toString().replace(/\$|\,/g, '')
}

function getTypeRandom(typelist) {
  const ret = []
  for (let i = 0; i < typelist.length; i++) {
    // console.log(typelist[i])
    data = getEachTypeRandom(typelist[i])
    if (typelist[i].indexOf("uint") >= 0 ) {
      // uint
      if (typelist[i].indexOf("[]") >= 0 ) {  // array
        for (let j = 0; j < data.length; j++) {
          data[j] = toNonExponential(parseInt(data[j]))
        }
      }
      else {
        data = toNonExponential(parseInt(data))
      }
    }
    ret.push(data)
  }
  return ret
}

// var arguments = ['address', 'uint8[]', 'uint8', 'uint256', 'bool']
// randomData = getTypeRandom(arguments)
// console.log(arguments, randomData)