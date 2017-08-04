import ErrorPage from '@/pages/error/error-page';
import PageNotFound from '@/pages/error/page-not-found';

export default [
  {
    path: '/error',
    name: 'ErrorPage',
    component: ErrorPage,
  },
  {
    path: '*',
    name: 'PageNotFound',
    component: PageNotFound,
  },
];
