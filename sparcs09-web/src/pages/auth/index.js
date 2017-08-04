import LoginCallback from '@/pages/auth/login-callback';
import Login from '@/pages/auth/login';
import Logout from '@/pages/auth/logout';
import Signup from '@/pages/auth/signup';

export default [
  {
    path: '/auth/sso',
    name: 'AuthSso',
    component: Login,
  },
  {
    path: '/auth/login_callback',
    name: 'LoginCallback',
    component: LoginCallback,
  },
  {
    path: '/auth/logout',
    name: 'Logout',
    component: Logout,
  },
  {
    path: '/auth/signup',
    name: 'Signup',
    component: Signup,
  },
];
