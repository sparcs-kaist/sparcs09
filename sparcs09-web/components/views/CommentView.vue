<template>
  <article class="media">
    <figure class="media-left">
      <p>김슈타인: </p>
    </figure>
    <div class="media-content">
      {{data.content}}
      <a class="button is-primary" @click="callback(data)">삭제</a>
    </div>
  </article>
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
