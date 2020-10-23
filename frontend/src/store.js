import Vue from 'vue'
import Vuex from 'vuex'
import { getAPI, getAPIwithToken } from './axios-api'

Vue.use(Vuex)

export default new Vuex.Store({
    state:{
        accessTokenExp: null,
        refreshTokenExp: null,
        islocalload: false,
        someData: '',
        cart: null,
        cart_set: null,
        order: null
    },

    mutations:{
        saveCart (state, data){
            var cart = data.slice(-1)[0].orderitem_set
            var order = data.slice(0,-1)
            var cart_set = new Set()

            cart.forEach(element => cart_set.add(element.item))
            state.cart_set = cart_set
            state.cart = cart
            state.order = order
            localStorage.setItem('cart', JSON.stringify(cart))
            localStorage.setItem('order',JSON.stringify(order))
        },
        loadCart (state){
            var cart = localStorage.getItem('cart')
            var order = localStorage.getItem('order')
            var cart_set = new Set()

            if (cart != null){
                state.cart = JSON.parse(cart)
                state.order = JSON.parse(order)
                state.cart.forEach(element => cart_set.add(element.item))
                state.cart_set = cart_set                
            } else{
                state.cart = cart
                state.order = order
            }
        },
        saveToken (state, {access, refresh}){
            if (access){
                getAPIwithToken.defaults.headers.common['Authorization'] = `Bearer ${access}` 
                var token = JSON.parse(atob(access.split('.')[1]))
                state.accessTokenExp = new Date(token.exp * 1000)
                localStorage.setItem('accessToken', access)
            } 
            if (refresh){
                var rtoken = JSON.parse(atob(refresh.split('.')[1]))
                state.refreshTokenExp = new Date(rtoken.exp * 1000) 
                localStorage.setItem('refreshToken', refresh)
            }
        },
        loadToken (state){
            var access = localStorage.getItem('accessToken')
            var refresh = localStorage.getItem('refreshToken')
            if (access){
                getAPIwithToken.defaults.headers.common['Authorization'] = `Bearer ${access}` 
                var token = JSON.parse(atob(access.split('.')[1]))
                state.accessTokenExp = new Date(token.exp * 1000)
            }
            if (refresh){
                var rtoken = JSON.parse(atob(refresh.split('.')[1]))
                state.refreshTokenExp = new Date(rtoken.exp * 1000) 
            }
        }, 

    },

    getters: {
        isValidrefresh (state) {
            var now = new Date()
            return now < state.refreshTokenExp
        },        

        isValidaccess (state) {
            var now = new Date()
            return now < state.accessTokenExp
        }
    },

    actions:{
        userLogout (){
            localStorage.removeItem('accessToken')
            localStorage.removeItem('refreshToken')
            localStorage.removeItem('cart')
            localStorage.removeItem('order')
            delete getAPIwithToken.defaults.headers.common['Authorization']
        },

        userLogin (context, user){
            return new Promise((resolve, reject) => {
                getAPI.post('/api/token/', {
                username: user.username,
                password: user.password
                })
                .then(response => {
                    context.commit('saveToken', { access: response.data.access, refresh: response.data.refresh })
                    getAPIwithToken.get('/api/order',
                    )
                    .then(response => {
                        context.commit('saveCart', response.data)
                        resolve()        
                    })        
                    .catch(err => {
                        console.log(err) 
                        reject() 
                    })
                }).catch(err => {
                    console.log(err)
                    reject() 
                })
            })
        },

        userReLogin (context){
            return new Promise((resolve, reject) => {
                getAPI.post('/api/token/refresh', {
                    refresh: localStorage.getItem('refreshToken')
                })
                .then(response => {
                    context.commit('saveToken', { access: response.data.access, refresh: null })
                    resolve()
                })
                .catch(err => {
                    reject(err) 
                })
            })
        },
        
        googleLogin (context, {code}){
            return new Promise((resolve, reject) => {
                getAPI.post('/api/user/social-auth/google-oauth2-front', {
                    code: code
                })
                .then(response => {
                    console.log(response)
                    context.commit('saveToken', { access: response.data.access, refresh: response.data.refresh })
                    resolve()
                })
                .catch(err => {
                    console.log(err)
                    reject(err) 
                })
            })
        },

        localLoad (context){
            context.commit('loadToken')
            context.commit('loadCart')
            context.state.islocalload = true
        },
    },

})