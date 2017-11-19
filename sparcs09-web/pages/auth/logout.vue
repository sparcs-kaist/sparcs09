<template>
    <div>
        <p>Logout sparcs09, wait...(</p>
    </div>
</template>
<script>
export default {
  async fetch({ store, redirect }) {
    await store.dispatch('auth/logout');
    redirect('/');
  },
};
</script>
