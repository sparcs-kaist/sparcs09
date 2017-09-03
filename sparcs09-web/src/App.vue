<template>
  <div id="app">
    <nav-bar :is-authenticated="isAuthenticated" :user-name="loggedUser && loggedUser.name"/>
    <router-view></router-view>
  </div>
</template>

<script>
/* eslint-disable object-shorthand */
import { mapGetters } from 'vuex';
import NavBar from '@/components/NavBar';
import * as types from './store/types';

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
