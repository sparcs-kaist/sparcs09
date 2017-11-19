import client from '../utils/api-client';

export const state = () => ({
  user: null,
});

export const getters = {
  getUser: state => state.user,
  termsAgreed: (state) => {
    if (state.user) {
      return state.user.terms_agreed;
    }
    return false;
  },
};

export const mutations = {
  setUser(state, { user }) {
    state.user = user;
  },
};

export const actions = {
  async getUserWithSid({ commit }, { sid }) {
    const response = await client.request({
      method: 'get',
      url: `users/${sid}/`,
    });
    commit('user/setUser', { user: response.data.user }, { root: true });
  },

  async patchUserWithSid({ commit }, { sid, user }) {
    const response = await client.request({
      method: 'patch',
      url: `users/${sid}/`,
      data: user,
    });
    if (response.code === 200) {
      commit('user/setUser', { user: response.data.user }, { root: true });
    }
  },
};
