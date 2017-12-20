<template>
  <article class="media">
    <figure class="media-left">
      <p>{{user.name}}: </p>
    </figure>
    <div class="media-content">
      <textarea class="textarea" v-model="comment_input.content" placeholder="댓글을 작성하세요"></textarea>
      <div class="level">
        <div class="level-right">
          <div class="level-item">
            <a class="button is-primary" @click="callback(comment_input)">제출</a>
          </div>
        </div>
      </div>
    </div>
  </article>
</template>

<script>
export default {
  data() {
    return {
      comment_input: {
        content: '',
      },
    };
  },
  props: {
    user: {
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
