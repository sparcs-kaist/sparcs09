import ErrorPage from '@/pages/error/ErrorPage';
import PageNotFound from '@/pages/error/PageNotFound';

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
