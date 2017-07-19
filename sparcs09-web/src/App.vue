<template>
  <div id="app">
    <nav-bar :is-authenticated="isAuthenticated"/>
    <router-view></router-view>
  </div>
</template>

<script>
/* eslint-disable object-shorthand */

import { mapGetters, mapMutations, mapActions } from 'vuex';
import NavBar from '@/components/NavBar';
import { getToken, getSid } from './utils/sparcs-sso';
import client from './utils/api-client';
import * as types from './store/types';

function appInitCallback() {
  const token = getToken();
  const sid = getSid();
  // check user already logged in..
  if (!!token && !!sid) {
    this.setToken({ token: token });
    client.setToken(token);
    this.getUserWithSid({ sid: sid }).then(() => {
    }).catch(() => {});
  }
}

export default {
  name: 'app',

  components: {
    'nav-bar': NavBar,
  },

  computed: {
    ...mapGetters({
      isAuthenticated: types.AUTH_IS_AUTHENTICATED,
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
