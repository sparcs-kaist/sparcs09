<template>
  <div class="container">
    <table class="table is-fullwidth">
      <tbody>
        <tr>
          <td>이름</td>
          <td>{{host.name}}</td>
        </tr>
        <tr>
          <td>연락처</td>
          <td>{{host.phone}}</td>
        </tr>
        <tr>
          <td>이메일</td>
          <td>{{host.email}}</td>

        </tr>
        <tr>
          <td>주소</td>
          <td>{{host.address}}</td>

        </tr>
        <tr>
          <td>카카오톡 아이디</td>
          <td>{{host.kakao_id}}</td>
        </tr>
      </tbody>
    </table>
  </div>
  </template>

<script>
export default {
  props: {
    host: {
      type: Object,
      required: true,
    },
  },
  computed: {
  },
};
</script>

