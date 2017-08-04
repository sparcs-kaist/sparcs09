<template>
  <form class="column is-half is-offset-one-quarter" v-on:submit.prevent="submitCallback(user_input)">
    <div class="field">
      <label class="label">Name</label>
      <p class="control">
        <input class="input" type="text" v-model="user_input.name">
      </p>
    </div>
    <div class="field">
      <label class="label">Email</label>
      <p class="control">
        <input class="input" type="text" v-model="user_input.email" disabled>
      </p>
    </div>
    <div class="field">
      <label class="label">Address</label>
      <p class="control">
        <input class="input" type="text" v-model="user_input.address">
      </p>
    </div>
    <div class="field">
      <label class="label">Phone</label>
      <p class="control">
        <input class="input" type="tel" v-model="user_input.phone">
      </p>
    </div>
    <div class="field">
      <label class="label">Kakao talk id</label>
      <p class="control">
        <input class="input" type="text" v-model="user_input.kakao_id">
      </p>
    </div>
    <div class="field" v-if="!user.terms_agreed">
      <p class="control">
        <label class="checkbox">
          <input type="checkbox" v-model="user_input.terms_agreed">
          동의 하시겠습니꽈~
        </label>
      </p>
    </div>
    <div class="field">
      <p class="control">
        <input type="submit" class="button is-primary">
      </p>
    </div>
  </form>
</template>
<script>
export default {
  name: 'UserForm',

  data() {
    return {
      user_input: {
        ...this.user,
      },
    };
  },

  props: {
    user: {
      type: Object,
      required: true,
    },
    submitCallback: {
      type: Function,
      required: true,
    },
  },
};
</script>

<style>
</style>
