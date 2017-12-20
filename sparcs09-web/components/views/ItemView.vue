<template>
  <div class="container">
    <figure class="image is-16by9">
      <img src="https://cdn.macrumors.com/article-new/2017/09/iphonexdesign-1-800x597.jpg">
    </figure>
    <table class="table is-fullwidth">
      <tbody>
        <tr>
          <td>가격</td>
          <td>{{priceWithCommas}} 원</td>
        </tr>
        <tr>
          <td>결제 방법</td>
          <td>{{item.payment_method}}</td>
        </tr>
        <tr>
          <td>기한</td>
          <td>{{item.deadline}} 까지</td>
        </tr>
        <tr>
          <td>배송일</td>
          <td>{{item.delivery_date}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  computed: {
    priceWithCommas() {
      return this.item.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
  },
};
</script>
