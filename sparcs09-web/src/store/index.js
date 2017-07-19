import Vue from 'vue';
import Vuex from 'vuex';
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
  },

  modules: {
    auth,
    user,
  },
});

export default store;
