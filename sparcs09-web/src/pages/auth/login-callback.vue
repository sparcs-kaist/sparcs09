<template>
</template>
<script>
/* eslint-disable object-shorthand */
import { mapGetters, mapActions } from 'vuex';
import { checkSsoState, setToken, setSid } from '../../utils/sparcs-sso';
import * as types from '../../store/types';


function loginCallback() {
  this.authWithSsoToken({ code: this.code }).then(() => {
    setToken(this.token);
    setSid(this.user.sid);
    this.$router.push('/');
  });
}

export default {
  name: 'LoginCallback',

  data() {
    return {
      code: this.$route.query.code,
      state: this.$route.query.state,
    };
  },

  // router guard to check sso state
  beforeRouteEnter(to, from, next) {
    const state = to.query.state;
    if (checkSsoState(state) === false) {
      next('/error');
    }
    next();
  },

  computed: {
    ...mapGetters({
      token: types.AUTH_GET_TOKEN,
      user: types.USER_GET_USER,
    }),
  },

  methods: {
    ...mapActions({
      authWithSsoToken: types.AUTH_LOGIN_WITH_SSO_CODE,
    }),
  },

  mounted: loginCallback,
};
</script>
