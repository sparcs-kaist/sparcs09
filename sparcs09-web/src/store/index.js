import Vue from 'vue';
import Vuex from 'vuex';
import * as types from './types';
import auth from './modules/auth';
import user from './modules/user';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
  },

  actions: {
  },

  mutations: {
  },

  getters: {
    [types.IS_AUTHENTICATED]: (state, getters) => getters[types.AUTH_IS_TOKEN_EXISTS]
        && getters[types.USER_IS_TERMS_AGREED],
  },

  modules: {
    auth,
    user,
  },
});

export default store;
