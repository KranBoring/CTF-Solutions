const crypto = require('crypto')

const { safeEqual } = require('../utils/safeEqual')

const users = [{
  username: 'admin',
  hashedPassword: 'Y3IfvoeyvgzlEtL6xSTXOY/rJSE='
}]

function getUserByUsername (username) {
  const user = users.find(user => user.username === username)
  if (!user) return null

  return user
}

function getUserByUsernameAndPassword (username, password) {
  const user = getUserByUsername(username)
  if (!user) return null

  const hashedPassword = crypto.createHash('sha1').update(password).digest('base64')
  if (!safeEqual(user.hashedPassword, hashedPassword)) return null

  return user
}

function resetPasswordByUsername (username) {
  const user = getUserByUsername(username)
  if (!user) return false

  const password = crypto.randomBytes(8).toString('hex')
  const hashedPassword = crypto.createHash('sha1').update(password).digest('base64')

  user.hashedPassword = hashedPassword
  return true
}

module.exports = {
  getUserByUsername,
  getUserByUsernameAndPassword,
  resetPasswordByUsername
}
