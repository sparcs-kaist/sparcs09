// define constants for vuex store (getter, action, mutation)
// naming rule is MODULE_NAME(black if root module)_CONSTANT_NAME

// getters

export const IS_AUTHENTICATED = 'IS_AUTHENTICATED';
export const AUTH_IS_TOKEN_EXISTS = 'auth/IS_AUTHENTICATED';
export const AUTH_GET_TOKEN = 'auth/GET_TOKEN';

export const USER_GET_USER = 'user/GET_USER_INFO';
export const USER_IS_TERMS_AGREED = 'user/IS_TERMS_AGREED';

// mutations
export const AUTH_SET_TOKEN = 'auth/SET_TOKEN';

export const USER_SET_USER = 'user/SET_USER_INFO';

// actions
export const AUTH_LOGIN_WITH_SSO_CODE = 'auth/LOGIN_WITH_SSO_CODE';
export const AUTH_LOGOUT = 'auth/LOGOUT';

export const USER_GET_USER_WITH_SID = 'user/GET_USER_WITH_SID';
export const USER_PATCH_USER_WITH_SID = 'user/PATCH_USER_WITH_SID';
