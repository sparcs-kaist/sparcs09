<template>
  <div class="box">
    <div v-for="(option_category, i) in option_categories" :key="option_category.id" class="level">
      <div class="level-left">
        <div class="level-item">
          {{option_category.name}}: 
        </div>
        <div class="level-item">
          <div class="select">
            <select v-model="record_input.option_items[i]">
              <option selected disabled value="record_input.option_items[i]">{{option_category.name}} 선택</option>
              <option v-for="item in option_category.items" :key="item.id" :value="item">{{item.name}} (+ {{item.price_delta}} 원)</option>
            </select>
          </div>
        </div>
      </div>
    </div>
    <div class="level">
      <div id="input-quantity" class="level-left">
        <div class="level-item">
          수량:
        </div>
        <div class="level-item">
          <a class="button" @click="increaseQuantity()"> + </a>
        </div>
        <div class="level-item">
          {{record_input.quantity}}
        </div>
        <div class="level-item">
          <a class="button" @click="decreaseQuantity()"> - </a>
        </div>
      </div>
    </div>
    <div class="level">
      <div class="level-left">
        <a class="button is-primary" @click="submitButtonListener()">추가</a>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    // iterate through option_categories
    // put true if category is required, false if not.
    return {
      record_input: {
        option_items: this.option_categories.map(x => x.required),
        quantity: 0,
      },
    };
  },
  props: {
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
    increaseQuantity() {
      this.record_input.quantity += 1;
    },
    decreaseQuantity() {
      if (this.record_input.quantity > 0) {
        this.record_input.quantity -= 1;
      }
    },
    submitButtonListener() {
      // remove -1's
      // check all the required option selected.
      const rec = this.record_input;
      if (rec.option_items.indexOf(true) === -1 && rec.quantity > 0) {
        // remove false elements and call callback function.
        rec.option_items = rec.option_items.filter(x => (x !== false));
        this.callback(rec);
      }
    },
  },
};
</script>
