<template>
  <button v-on:click="ssoRedirect">Login</button>
</template>
<script>
  import uuid from 'uuid';
  import { setSsoState, getLoginUrl } from '../utils/sparcs-sso';

  export default {
    methods: {
      ssoRedirect(event) {
        const ssoState = uuid.v4().replace('-', '');
        setSsoState(ssoState);
        const loginUrl = getLoginUrl(ssoState);
        history.pushState(loginUrl);
      },
    },
  };
</script>
