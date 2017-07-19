<template>
  <div>
    <p>Logout sparcs09, wait...(</p>
  </div>
</template>
<script>
import { mapActions } from 'vuex';
import * as types from '../../store/types';
import { resetToken } from '../../utils/sparcs-sso';
import client from '../../utils/api-client';

function logoutCallback() {
  this.logout().then(() => {
    resetToken();
    client.setToken(null);
    this.$router.push('/');
  });
}

export default {
  name: 'Logout',

  methods: {
    ...mapActions({
      logout: types.AUTH_LOGOUT,
    }),
  },

  mounted: logoutCallback,
};
</script>
