<template>
  <user-form :user="user" :submitCallback="updateCallback"></user-form>
</template>


<script>
import { mapGetters, mapActions } from 'vuex';
import UserForm from '@/components/forms/UserForm';
import * as types from '../../store/types';

function update(updateData) {
  const data = {
    name: updateData.name,
    address: updateData.address,
    kakao_id: updateData.kakao_id,
    phone: updateData.phone,
  };

  this.updateUser({
    sid: updateData.sid,
    user: data,
  });
}

export default {
  name: 'MyPage',

  methods: {
    updateCallback: update,
    ...mapActions({
      updateUser: types.USER_PATCH_USER_WITH_SID,
    }),
  },

  computed: {
    ...mapGetters({
      user: types.USER_GET_USER,
    }),
  },

  components: {
    'user-form': UserForm,
  },
};
</script>

<style>

</style>
