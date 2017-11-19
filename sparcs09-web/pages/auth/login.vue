<template>
  <div>
    <p>Login with sparcs sso. redirecting...</p>
  </div>
</template>
<script>
  import uuid from 'uuid';
  import { setSsoState, getLoginUrl } from '../../utils/sparcs-sso';

  function ssoRedirect() {
    const ssoState = uuid.v4().replace(/-/gi, '');
    setSsoState(ssoState);
    const loginUrl = getLoginUrl(ssoState);
    window.location.href = loginUrl;
  }

  export default {
    name: 'Login',

    mounted: ssoRedirect,
  };
</script>
