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
        <div class="container">
          <h2 class="title is-2">댓글</h2>
          <comment-form :callback="addComment"></comment-form>
          <comment-view v-for="(comment, i) in comments" :key="i" :data="comment" :callback="removeComment"></comment-view>
        </div>
      </section>
    </div>
  </section>
</template>

<script>
  import ItemView from '~/components/views/ItemView.vue';
  import ItemContentView from '~/components/views/ItemContentView.vue';
  import HostView from '~/components/views/HostView.vue';
  import RecordForm from '~/components/forms/RecordForm.vue';
  import RecordView from '~/components/views/RecordView.vue';
  import CommentForm from '~/components/forms/CommentForm.vue';
  import CommentView from '~/components/views/CommentView.vue';

  import client from '../../utils/api-client';

  async function getItemWithId(id) {
    const response = await client.request({
      method: 'get',
      url: `items/${id}/`,
    });
    return response.data;
  }

  async function getContentsWithItemId(itemId) {
    const response = await client.request({
      method: 'get',
      url: `items/${itemId}/contents`,
    });
    return response.data.contents;
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
        comments: [],
      };
    },

    async asyncData({ params, error }) {
      try {
        const item = await getItemWithId(params.id);
        const contents = await getContentsWithItemId(params.id);
        item.contents = contents;
        return {
          item,
        };
      } catch (e) {
        console.log(e);
        error({ statusCode: params.statusCode, message: 'Error occurred' });
        return null;
      }
    },

    methods: {
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
      addComment(comment) {
        const commentCopy = JSON.parse(JSON.stringify(comment));
        comment.content = '';
        this.comments.push(commentCopy);
      },
      removeComment(commentIndex) {
        this.comments.splice(commentIndex, 1);
      },
    },

    head: {
      title: 'iPhone X 공동구매',
    },
  };
</script>