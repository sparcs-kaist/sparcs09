<template>
  <section class="section">
    <div class="container">
      <h1 class="title is-1">{{item.title}}</h1>
      <section class="section">
        <div class="container">
          <h2 class="title is-2">상품 정보</h2>
          <item-view :item="item"></item-view>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <h2 class="title is-2">호스트 정보</h2>
          <host-view :host="item.host"></host-view>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <h2 class="title is-2">상품 주문</h2>
          <record-form :option_categories="item.option_categories" :callback="addRecord"></record-form>
          <record-view v-for="(record, i) in records" :key="i" :index="i" :option_categories="item.option_categories" :record="record" :callback="removeRecord"></record-view>
          <hr>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <h2 class="title is-2">상품 상세</h2>
          <item-content-view :contents="item.contents"></item-content-view>
        </div>
      </section>
      <section class="section">
        <div class="container" @scroll="handleScroll">
          <h2 class="title is-2">댓글 ({{comments.count}})</h2>
          <comment-form v-if="user != null" :user="user" :callback="addComment"></comment-form>
          <comment-view v-for="(comment, i) in comments.comments" :key="comment.id" :index="i" :comment="comment" :callback="deleteComment"></comment-view>
        </div>
      </section>
    </div>
  </section>
</template>

<script>
  import { mapGetters } from 'vuex';

  import ItemView from '~/components/views/ItemView.vue';
  import ItemContentView from '~/components/views/ItemContentView.vue';
  import HostView from '~/components/views/HostView.vue';
  import RecordForm from '~/components/forms/RecordForm.vue';
  import RecordView from '~/components/views/RecordView.vue';
  import CommentForm from '~/components/forms/CommentForm.vue';
  import CommentView from '~/components/views/CommentView.vue';

  import client from '../../utils/api-client';

  async function getItemWithId(id) {
    try {
      const response = await client.request({
        method: 'get',
        url: `items/${id}/`,
      });
      return response.data;
    } catch (e) {
      throw e;
    }
  }

  async function getContentsWithItemId(itemId) {
    try {
      const response = await client.request({
        method: 'get',
        url: `items/${itemId}/contents`,
      });
      return response.data.contents;
    } catch (e) {
      throw e;
    }
  }

  async function getCommentsOfItem(itemId, offset) {
    try {
      const response = await client.request({
        method: 'get',
        url: `items/${itemId}/comments?offset=${offset}&sort=-created_date`,
      });
      return response.data;
    } catch (e) {
      throw e;
    }
  }


  async function addCommentToItem(itemId, comment) {
    try {
      const response = await client.request({
        method: 'post',
        url: `items/${itemId}/comments/`,
        data: comment,
      });
      return response.data.comment;
    } catch (e) {
      throw e;
    }
  }

  async function deleteCommentWithId(commentId) {
    try {
      const response = await client.request({
        method: 'delete',
        url: `comments/${commentId}`,
      });
      return response.data;
    } catch (e) {
      throw e;
    }
  }

  export default {
    components: {
      ItemView,
      ItemContentView,
      HostView,
      RecordForm,
      RecordView,
      CommentForm,
      CommentView,
    },

    data() {
      return {
        item: null,
        records: [],
        comments: { count: 0, comments: [] },
      };
    },

    computed: {
      ...mapGetters({
        user: 'user/getUser',
      }),
    },

    async asyncData({ params, error }) {
      try {
        const item = await getItemWithId(params.id);
        const contents = await getContentsWithItemId(params.id);
        item.contents = contents;
        const comments = await getCommentsOfItem(params.id, 0);
        return {
          item,
          comments,
        };
      } catch (e) {
        alert(e.response);
        error({ statusCode: e.response.status, message: e.response.statusText });
        return null;
      }
    },

    methods: {
      async handleScroll() {
        if (window.innerHeight + window.scrollY >= document.body.scrollHeight) {
          // fetch older 10 comments
          const older = await getCommentsOfItem(this.item.id, this.comments.comments.length);
          this.comments.comments = this.comments.comments.concat(older.comments);
        }
      },
      addRecord(record) {
        // add option object to page.
        const recordCopy = JSON.parse(JSON.stringify(record));
        record.quantity = 0;
        this.records.push(recordCopy);
      },
      removeRecord(recordIndex) {
        // remove option object to page.
        this.records.splice(recordIndex, 1);
      },
      async addComment(comment) {
        try {
          const resComment = await addCommentToItem(this.item.id, { content: comment.content });
          comment.content = '';
          this.comments.comments.unshift(resComment);
          this.comments.count += 1;
        } catch (e) {
          alert(e.response);
        }
      },
      async deleteComment(comment) {
        try {
          await deleteCommentWithId(comment.id);
          comment.content = 'DELETED';
        } catch (e) {
          alert(e.response);
        }
      },
    },

    created() {
      window.addEventListener('scroll', this.handleScroll);
    },

    destroyed() {
      window.removeEventListener('scroll', this.handleScroll);
    },

    head: {
      title: 'SPARCS 09',
    },
  };
</script>