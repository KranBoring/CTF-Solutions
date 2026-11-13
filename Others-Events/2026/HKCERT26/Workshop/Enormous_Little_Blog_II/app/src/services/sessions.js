const crypto = require('crypto')
const jwt = require('jsonwebtoken')
const { getUserByUsername } = require('./users')

const SECRET = crypto.randomBytes(8).toString('hex')

function signToken (user) {
  const token = jwt.sign({ username: user.username }, SECRET)
  return token
}

function getUserByToken (token) {
  const { username } = jwt.verify(token, SECRET)
  if (!username) throw new Error('invalid user')

  const user = getUserByUsername(username)
  if (!user) throw new Error('invalid user')

  return user
}

module.exports = {
  signToken,
  getUserByToken
}
