<template>
  <nav class="nav">
    <div class="nav-left">
      <router-link :to="{ name: 'Home' }" class="nav-item">
        SPARCS 09
      </router-link>
    </div>
    <div class="nav-right nav-menu">
      <div class="field is-grouped" v-if="isAuthenticated">
        <p class="control">
          <router-link :to="{ name: 'Logout' }" class="button is-info">
            Logout
          </router-link>
        </p>
      </div>
      <div class="field is-grouped" v-else>
        <p class="control">
          <router-link :to="{ name: 'AuthSso' }" class="button is-primary">
            Login
          </router-link>
        </p>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',

  props: {
    redirectPath: String,
    isAuthenticated: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style>
.nav {
  margin: 10px;
}
</style>
