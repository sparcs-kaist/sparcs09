<template>
  <div class="box">
    <div v-for="(category, index) in option_categories" :key="category.id" class="level">
      <div class="level-left">
        <div class="level-item">
          {{category.name}}:
        </div>
        <div class="level-item">
          {{record.option_items[index].name}}
        </div>
      </div>
    </div>
    <div class="level">
      <div class="level-left">
        <div class="level-item">
          수량:
        </div>
        <div class="level-item">
          {{record.quantity}}
        </div>
      </div>
    </div>
    <div class="level">
      <div class="level-left">
        <div class="level-item"
          <a class="button is-danger" @click="callback(index)">삭제</a>
        </div>
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
    index: {
      type: Number,
      required: true,
    },
    record: {
      type: Object,
      required: true,
    },
    callback: {
      type: Function,
      required: true,
    },
    option_categories: {
      type: Array,
      required: true,
    },
  },
  methods: {
  },
};
</script>
