<template>
  <div id="app">
    <nav-bar :is-authenticated="isAuthenticated" :user-name="loggedUser && loggedUser.name"/>
    <router-view></router-view>
  </div>
</template>

<script>
/* eslint-disable object-shorthand */
import { mapGetters, mapMutations, mapActions } from 'vuex';
import NavBar from '@/components/NavBar';
import { getToken, getSid, resetToken } from './utils/sparcs-sso';
import client from './utils/api-client';
import * as types from './store/types';

function appInitCallback() {
  return new Promise((resolve) => {
    const token = getToken();
    const sid = getSid();
    client.setToken(token);
    this.setToken({ token: token });
    if (!!token && !!sid) {
      this.getUserWithSid({
        sid: sid,
      }).then(() => {
        resolve();
      }).catch(() => {
        resetToken();
        this.setToken({ token: null });
        client.setToken(null);
        resolve();
      });
    } else {
      resolve();
    }
  });
}

export default {
  name: 'app',

  components: {
    'nav-bar': NavBar,
  },

  computed: {
    ...mapGetters({
      isAuthenticated: types.IS_AUTHENTICATED,
      loggedUser: types.USER_GET_USER,
    }),
  },

  methods: {
    ...mapMutations({
      setToken: types.AUTH_SET_TOKEN,
    }),
    ...mapActions({
      getUserWithSid: types.USER_GET_USER_WITH_SID,
    }),
  },

  created: appInitCallback,

};
</script>

<style lang="sass" src="bulma"></style>
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
