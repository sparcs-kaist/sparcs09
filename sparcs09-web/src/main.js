// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import { mapMutations } from 'vuex';
import App from './App';
import router from './router';
import store from './store';
import { getToken, getSid, resetToken } from './utils/sparcs-sso';
import client from './utils/api-client';
import * as types from './store/types';


Vue.config.productionTip = false;

function appInit() {
  return new Promise((resolve) => {
    const token = getToken();
    const sid = getSid();
    client.setToken(token);
    if (!!token && !!sid) {
      client.request({
        method: 'get',
        url: `users/${sid}/`,
      }).then((response) => {
        const user = response.data.user;
        resolve({ token, user });
      }).catch(() => {
        resetToken();
        resolve(null);
      });
    } else {
      resolve(null);
    }
  });
}

/*
 *  Callback that after init. (when vue instance created)
 */
function appInitCallback() {
  this.setToken({ token: this.token });
  this.setUser({ user: this.user });
}

appInit().then((initData) => {
  /* eslint-disable no-new */
  new Vue({
    el: '#app',
    template: '<App/>',
    components: { App },
    router,
    store,

    data() {
      return {
        token: initData.token,
        user: initData.user,
      };
    },

    methods: {
      ...mapMutations({
        setToken: types.AUTH_SET_TOKEN,
        setUser: types.USER_SET_USER,
      }),
    },

    created: appInitCallback,

  });
});
