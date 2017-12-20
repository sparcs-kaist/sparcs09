<template>
  <div class="box">
    <div class="level">
      <div class="level-left">
        <div class="level-item">
          색상:
        </div>
        <div class="level-item">
          {{data.option1}}
        </div>
      </div>
    </div>
    <div class="level">
      <div class="level-left">
        <div class="level-item">
          용량:
        </div>
        <div class="level-item">
          {{data.option2}}
        </div>
      </div>
    </div>
    <div class="level">
      <div class="level-left">
        <div class="level-item">
          수량:
        </div>
        <div class="level-item">
          {{data.quantity}}
        </div>
      </div>
    </div>
    <div class="level">
      <div class="level-left">
        <a class="button is-danger" @click="callback(data)">삭제</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {

    };
  },
  props: {
    data: {
      type: Object,
      required: true,
    },
    callback: {
      type: Function,
      required: true,
    },
  },
};
</script>
