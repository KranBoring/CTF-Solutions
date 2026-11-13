const { getUserByToken } = require("./services/sessions")

function injectUser (req, res, next) {
  const { 'elb2_token': token } = req.cookies
  if (!token) return next()

  try {
    req.user = getUserByToken(token)
  } catch (err) {
    // Whatever...
  }

  return next()
}

module.exports = {
  injectUser
}
