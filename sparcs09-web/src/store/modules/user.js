/* eslint-disable no-param-reassign */
import * as types from '../types';
import client from '../../utils/api-client';

export default {
  state: {
    user: null,
  },

  getters: {
    [types.USER_GET_USER]: state => state.user,
    [types.USER_IS_TERMS_AGREED]: (state) => {
      if (state.user) {
        return state.user.terms_agreed;
      }
      return false;
    },
  },

  mutations: {
    /*
     * payload
     *  - user: sparcs09 user object, object
     */
    [types.USER_SET_USER](state, payload) {
      state.user = payload.user || null;
    },
  },

  actions: {
    /*
     * payload
     *  - sid: sid for sparcs09 user
     */
    [types.USER_GET_USER_WITH_SID]({ commit }, payload) {
      return new Promise((resolve, reject) => {
        client.request({
          method: 'get',
          url: `users/${payload.sid}/`,
        }).then((response) => {
          commit(types.USER_SET_USER, { user: response.data.user });
          resolve();
        }).catch(err => reject(err));
      });
    },

    /*
     * payload
     *  - sid: sid for spark09 user
     *  - user: new user info
     */
    [types.USER_PATCH_USER_WITH_SID]({ commit }, payload) {
      return new Promise((resolve, reject) => {
        client.request({
          method: 'patch',
          url: `users/${payload.sid}/`,
          data: payload.user,
        }).then((response) => {
          commit(types.USER_SET_USER, { user: response.data.user });
          resolve();
        }).catch(err => reject(err));
      });
    },
  },
};
