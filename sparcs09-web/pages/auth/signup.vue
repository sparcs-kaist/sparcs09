<template>
    <user-form :user="user" :submitCallback="signupCallback"></user-form>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
import UserForm from '~/components/forms/UserForm.vue';

async function signup(newUser) {
  const payload = {
    sid: newUser.sid,
    user: {
      name: newUser.name,
      address: newUser.address,
      kakao_id: newUser.kakao_id,
      phone: newUser.phone,
      terms_agreed: newUser.terms_agreed,
    },
  };
  await this.updateUser(payload);
  this.$router.push('/');
}

export default {
  components: {
    UserForm,
  },

  methods: {
    signupCallback: signup,
    ...mapActions({
      updateUser: 'user/patchUserWithSid',
    }),
  },

  computed: {
    ...mapGetters({
      user: 'user/getUser',
    }),
  },
};
</script>
