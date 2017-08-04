/* eslint-disable no-param-reassign */
import * as types from '../types';
import client from '../../utils/api-client';

export default {
  state: {
    token: null,
  },

  getters: {
    [types.AUTH_IS_TOKEN_EXISTS]: state => !!state.token,
    [types.AUTH_GET_TOKEN]: state => state.token,
  },

  mutations: {
    /*
     * payload
     *  - token: sparcs09 auth token, string
     */
    [types.AUTH_SET_TOKEN](state, payload) {
      state.token = payload.token || null;
    },
  },

  actions: {
    /*
     * payload
     *  - code: sparcs sso code
     */
    [types.AUTH_LOGIN_WITH_SSO_CODE]({ commit }, payload) {
      return new Promise((resolve, reject) => {
        client.request({
          method: 'post',
          url: 'sessions/',
          data: {
            code: payload.code,
          },
        }).then((response) => {
          commit(types.USER_SET_USER, { user: response.data.user });
          commit(types.AUTH_SET_TOKEN, { token: response.data.token });
          client.setToken(response.data.token);
          resolve();
        }).catch(err => reject(err));
      });
    },

    /*
     * payload
     */
    [types.AUTH_LOGOUT]({ state, commit }) {
      return new Promise((resolve, reject) => {
        client.request({
          method: 'delete',
          url: `sessions/${state.token}`,
        }).then(() => {
          commit(types.AUTH_SET_TOKEN, { user: null });
          commit(types.USER_SET_USER, { token: null });
          resolve();
        }).catch(err => reject(err));
      });
    },
  },
};
