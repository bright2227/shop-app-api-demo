  
<template>
  <div class="nav-bar">
    <nav class="navbar navbar-expand-lg navbar-light bg-white nav-1">
      <div class="container mw-0 px-3">

        <a class="navbar-brand" href="#">
        <!-- <img src="../assets/brand-name.png" width="" height="27" class="d-inline-block align-top" alt="" loading="lazy"> -->
        <h2> Shop-app-demo </h2>
        </a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <router-link :to = "{ name:'product' }" exact>Products</router-link>
            </li>
          </ul>
        </div>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <router-link :to = "{ name:'cart' }" exact>Carts</router-link>
            </li>
          </ul>
        </div>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <router-link :to = "{ name:'login' }" exact>Login</router-link>
            </li>
          </ul>
        </div>

        <div class="collapse navbar-collapse" id="navbarSupportedContent" v-if="!isLogin">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <router-link :to = "{name:'register'}" exact>Register</router-link>
            </li>
          </ul>
        </div>

      </div>
    </nav>
  </div>
</template>

<script>
  export default {
    name: 'Navbar',
    data () {
      return {
      isLogin: false
      }
    },
    created () {
      // console.log(this.$store.state.cart)
      this.isLogin = (this.$store.state.cart != null)
      // console.log(this.isLogin)

    },    
  }
</script>

<style scoped>
    a {
      color:#000;
  } 
    h2 {
    margin-right: 50px; /* Creates space on the outside of the element */
}
</style>