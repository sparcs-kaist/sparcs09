<template>
</template>
<script>
import { checkSsoState } from '../../utils/sparcs-sso';
/* eslint-disable object-shorthand */
export default {
  async fetch({
    store, route, redirect, error,
  }) {
    if (!checkSsoState(route.query.state)) {
      return error(403);
    }
    await store.dispatch('auth/loginWithSsoCode', route.query);
    const returnPath = store.getters['user/termsAgreed'] ? '/' : '/auth/signup';
    return redirect(returnPath);
  },
};
</script>
