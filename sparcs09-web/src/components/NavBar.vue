<template>
  <div class="nav-container column is-10 is-offset-1">
    <nav class="nav">
      <div class="nav-left">
        <router-link :to="{ name: 'Home' }" class="nav-item">
          SPARCS 09
        </router-link>
      </div>
      <div class="nav-right nav-menu">

        <router-link v-if="isAuthenticated" :to="{ name: 'MyPage' }" class="nav-item is-tab">
          <span>Logged as {{ userName }}</span>
        </router-link>

        <router-link v-if="isAuthenticated" :to="{ name: 'Logout' }" class="nav-item is-tab">
          <span>Logout</span>
        </router-link>
        <router-link v-else :to="{ name: 'AuthSso' }" class="nav-item is-tab">
          <span>Login</span>
        </router-link>

      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'NavBar',

  props: {
    redirectPath: {
      type: String,
      required: false,
    },
    isAuthenticated: {
      type: Boolean,
      required: true,
    },
    userName: {
      type: String,
      required: false,
    },
  },
};
</script>

<style scoped>
.nav {
  margin: 10px;
}
</style>
