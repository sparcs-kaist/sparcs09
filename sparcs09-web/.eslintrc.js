module.exports = {
  root: true,
  parser: 'babel-eslint',
  env: {
    browser: true,
    node: true
  },
  extends: 'airbnb-base',
  // required to lint *.vue files
  plugins: [
    'html'
  ],
  // add your custom rules here
  rules: {
    'no-param-reassign': 0,
    'no-restricted-globals': 0,
    'no-shadow': 0,
    'no-unused-vars': [2, {'vars': 'all', 'args': 'none'}],
    'import/extensions': 0,
    'import/no-extraneous-dependencies': 0,
    'import/no-unresolved': 0,
  },
  globals: {}
}
