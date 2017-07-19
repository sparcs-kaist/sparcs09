var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  SSO_CLIENT_ID: '""',
  SPARCS09_API_DOMAIN: '""',
})
