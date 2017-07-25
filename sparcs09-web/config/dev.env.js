var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  SSO_CLIENT_ID: '"test08e7cfee1d52da64"',
  SPARCS09_API_DOMAIN: '"http://127.0.0.1:12345/api/"',
})
