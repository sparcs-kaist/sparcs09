import { getToken, getSid } from '../utils/sparcs-sso';
import client from '../utils/api-client';

export const state = () => ({ });

export const getters = {
  isAuthenticated: (state, getters) => getters['user/termsAgreed'] && getters['auth/tokenExists'],
};

export const mutations = { };

export const actions = {
  async nuxtClientInit({ commit, dispatch }, { redirect, route }) {
    if (route.path === '/auth/login_callback') {
      return;
    }
    const token = await getToken();
    const sid = await getSid();
    if (!token || !sid) {
      // no-eslint
    } else {
      client.setToken(token);
      await dispatch('user/getUserWithSid', { sid });
      commit('auth/setToken', { token });
    }
  },
};
