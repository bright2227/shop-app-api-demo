import Vue from 'vue'
import App from './App.vue'
import router from './routes.js'
import store from './store.js'
import 'bootstrap/dist/css/bootstrap.min.css'

Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  if (!store.state.islocalload){
    store.dispatch('localLoad')
  }
  if (to.matched.some(record => record.meta.requiresLogin)) {
    if (!store.getters.isValidaccess) {
      if (!store.getters.isValidrefresh) {
        next({ name: 'login' })
      } else {
        store.dispatch('userReLogin')
        next()
      }
    } else {
      next()
    }
  } else {
    next()
  }
})

//  next doesn't finish function at first time
//  next()
//  console.log(1)
//  next()
//  console.log(2)
//  ---------
//  1
//  2

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
