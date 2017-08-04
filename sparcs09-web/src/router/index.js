import Vue from 'vue';
import Router from 'vue-router';
import Hello from '@/components/Hello';
import auth from '../pages/auth';
import error from '../pages/error';
import item from '../pages/item';
import user from '../pages/user';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Hello,
    },
    ...auth,
    ...error,
    ...item,
    ...user,
  ],
});
