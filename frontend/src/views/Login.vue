<template>
  <div>
  <div class="container text-dark">
    <div class="row justify-content-md-center">
      <div class="col-md-5 p-3 login justify-content-md-center">
        <h1 class="h3 mb-3 font-weight-normal text-center">Please Login</h1>

        <form v-on:submit.prevent="login">
          <div class="form-group">
            <input type="text" name="username" id="user" v-model="username" class="form-control" placeholder="Username">
          </div>
          <div class="form-group">
            <input type="password" name="password" id="pass" v-model="password" class="form-control" placeholder="Password">
          </div>
          <button type="submit" class="btn btn-lg btn-primary btn-block">Login</button>
          <a :href="googleoauth2"><img src="../assets/btn_google_signin.png" width="" height="45" class="d-inline-block align-top" alt="" loading="lazy"></a>
          <p class="p3 mb-3 font-weight-normal text-center" v-if="incorrectAuth">login fail</p>
        </form>
        
        <router-link :to = "{ name:'reset' }" exact> forget your password? </router-link>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
  export default {
    name: 'login',
    data () {
      return {
        username: '',
        password: '',
        incorrectAuth: false,
        client_id: '673717759805-6tdf9dpra96brad4vv97q970sds829og.apps.googleusercontent.com',
        redirect_uri: 'http://localhost:8080/login',
        state: '',
        googleoauth2: ''
      }
    },
    created () {
      if (this.$route.query.code != undefined & this.$route.query.state == localStorage.getItem('state')){
        localStorage.removeItem('state')
        this.$store.dispatch('googleLogin', {
          code: this.$route.query.code
        })        
        .then(() => {
          this.$router.push({ name: 'cart' })
        })
        .catch((err) => {
          this.incorrectAuth = true
          console.log(err)
        })
      } else {
        this.state = Math.random().toString(36).slice(2)
        localStorage.setItem('state', this.state)
        this.googleoauth2 = 'https://accounts.google.com/o/oauth2/auth?client_id='+this.client_id+'&redirect_uri='+this.redirect_uri
          +'&state='+this.state+'&response_type=code&scope=openid+email+profile'
      }
    },

    methods: {
      login () { 
        this.$store.dispatch('userLogin', {
          username: this.username,
          password: this.password
        })
                .then(() => {
          this.$router.push({ name: 'cart' })
        })
        .catch((err) => {
          this.incorrectAuth = true
          console.log(err)
        })
        }
      }
  }
</script>

<style>
body { 
  background-color:#f4f4f4;
  text-align: center;
}
.login{
  background-color:#fff;
  margin-top:10%;
}
.router-link-exact{
   color: red;
}
  input {
    padding: 25px 10px;
}
  

</style>
