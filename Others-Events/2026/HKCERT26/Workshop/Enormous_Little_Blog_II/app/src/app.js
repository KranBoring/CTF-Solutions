const express = require('express')
const path = require('path')
const { create, engine } = require('express-handlebars')
const cookieParser = require('cookie-parser')
const bodyParser = require('body-parser')

const { getPosts } = require('./services/posts')
const { resetPasswordByUsername, getUserByUsername, getUserByUsernameAndPassword } = require('./services/users')
const { signToken } = require('./services/sessions')
const { injectUser } = require('./middlewares')

const app = express()
const hbs = create()

hbs.handlebars.registerHelper('isPostViewable', function (currentUser, author, private) {
  if (!private) return true
  if (!currentUser) return false
  return currentUser.username === author
})

app.use(bodyParser.urlencoded())
app.use(cookieParser())

app.engine('handlebars', engine())
app.set('view engine', 'handlebars')
app.set('views', path.join(__dirname, './views'))

app.use('/', injectUser)

app.get('/', function (req, res) {
  const currentUser = req.user

  return res.render('home', {
    currentUser,
    posts: getPosts()
  })
})

app.get('/login', function (req, res) {
  const currentUser = req.user

  return res.render('login', {
    currentUser
  })
})

app.post('/login', function (req, res) {
  const currentUser = req.user
  const { username, password } = req.body

  const user = getUserByUsernameAndPassword(username, password)
  if (!user) {
    return res.render('login', {
      currentUser,
      errorMessage: 'Your username or password is incorrect.'
    })
  }

  const token = signToken(user)
  res.cookie('elb2_token', token)

  return res.render('login', {
    currentUser,
    successMessage: 'Logged in successfully.'
  })
})

app.get('/reset-password', function (req, res) {
  const currentUser = req.user

  return res.render('reset_password', {
    currentUser
  })
})

app.post('/reset-password', function (req, res) {
  const currentUser = req.user
  const { username } = req.body

  const success = resetPasswordByUsername(username)
  if (!success) {
    return res.render('reset_password', {
      currentUser,
      errorMessage: 'Cannot reset password.'
    })
  }

  return res.render('reset_password', {
    currentUser,
    successMessage: `Password resetted for ${username}.`
  })
})

app.listen(1337, function () {
  console.log('server is listening on port 1337')
})
