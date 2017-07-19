<template>
  <form>
    <div class="field">
      <label class="label">Name</label>
      <p class="control">
        <input class="input" type="text">
      </p>
    </div>
  </form>
</template>
<script>
import { mapGetters } from 'vuex';
import * as types from '../../store/types';

export default {
  name: 'SignUp',

  computed: {
    ...mapGetters({
      user: types.USER_GET_USER,
    }),
  },
};
</script>
