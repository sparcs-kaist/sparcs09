<template>
  <article class="media">
    <figure class="media-left">
      <p>{{comment.writer.name}}: </p>
    </figure>
    <div class="media-content">
      {{comment.content}}
      <a class="button is-primary" @click="callback(comment)">삭제</a>
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
    index: {
      type: Number,
      required: true,
    },
    comment: {
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
