import Vue from 'vue'
import VueRouter from 'vue-router'
import Products from './views/Products'
import Register from './views/Register'
import Cart from './views/Cart'
import Login from './views/Login'
import Logout from './views/Logout'

Vue.use(VueRouter)

export default new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
        path: '/',
        name: 'product',
        component: Products,
        },
        {
        path: '/cart',
        name: 'cart',
        component: Cart,
        meta: {
            requiresLogin: true
          }
        },
        {
        path: '/login',
        name: 'login',
        component: Login,
        },
        {
        path: '/register',
        name: 'register',
        component: Register,
        },
        {
        path: '/logout',
        name: 'logout',
        component: Logout,
        },
    ]
})
