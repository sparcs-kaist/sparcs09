const stateKey = 'state_secret';
const tokenKey = 'token';
const sidKey = 'sid';

export const setSsoState = state => window.localStorage.setItem(stateKey, state);

export const checkSsoState = state => window.localStorage.getItem(stateKey) === state;

export const setToken = token => window.localStorage.setItem(tokenKey, token);
export const setSid = sid => window.localStorage.setItem(sidKey, sid);

export const getToken = () => window.localStorage.getItem(tokenKey);
export const getSid = () => window.localStorage.getItem(sidKey);

export const resetToken = () => {
  window.localStorage.removeItem(stateKey);
  window.localStorage.removeItem(tokenKey);
  window.localStorage.removeItem(sidKey);
};

export const getLoginUrl = state => `${process.env.SSO_SERVER_DOMAIN}/${process.env.SSO_API_PREFIX}\
${process.env.SSO_VERSION_PREFIX}/token/require?client_id=${process.env.SSO_CLIENT_ID}&state=${state}`;
