import client from '../utils/api-client';
import { setSid, setToken, resetToken } from '../utils/sparcs-sso';

export const state = () => ({
  token: null,
});

export const getters = {
  tokenExists: state => !!state.token,
  getToken: state => state.token,
};

export const mutations = {
  setToken(state, { token }) {
    state.token = token;
  },
};

export const actions = {
  async loginWithSsoCode({ commit }, { code }) {
    const response = await client.request({
      method: 'post',
      url: 'sessions/',
      data: {
        code,
      },
    });
    // Set token and sid in cleint local storage
    const { user, token } = response.data;
    setSid(user.sid);
    setToken(token);
    commit('user/setUser', { user }, { root: true });
    commit('auth/setToken', { token }, { root: true });
    client.setToken(response.data.token);
  },

  async logout({ state, commit }) {
    await client.request({
      method: 'delete',
      url: `sessions/${state.token}`,
    });
    commit('user/setUser', { user: null }, { root: true });
    commit('auth/setToken', { token: null }, { root: true });
    client.setToken(null);
    setToken(null);
    setSid(null);
    resetToken();
  },
};
