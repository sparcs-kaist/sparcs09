<template>
    <user-form :user="user" :submitCallback="updateCallback"></user-form>
</template>
<script>
import { mapGetters } from 'vuex';
import UserForm from '~/components/forms/UserForm.vue';

async function update(updateData) {
  const payload = {
    sid: updateData.sid,
    user: {
      name: updateData.name,
      address: updateData.address,
      kakao_id: updateData.kakao_id,
      phone: updateData.phone,
    },
  };

  await this.$store.dispatch('user/patchUserWithSid', payload);
}

export default {
  components: {
    UserForm,
  },

  computed: {
    ...mapGetters({
      user: 'user/getUser',
    }),
  },

  methods: {
    updateCallback: update,
  },
};
</script>
