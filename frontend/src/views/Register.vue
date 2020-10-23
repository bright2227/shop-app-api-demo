<template>
  <div>
  <div class="container text-dark">
    <div class="row justify-content-md-center">
      <div class="col-md-5 p-3 login justify-content-md-center">
        <h1 class="h3 mb-3 font-weight-normal text-center">Register</h1>

        <form v-on:submit.prevent="register" v-if="!waitActivate">
          <div class="form-group">
            <input type="text" name="username" id="user" v-model="username" class="form-control" placeholder="Username">
          </div>
          <div class="form-group">
            <input type="password" name="password" id="pass" v-model="password" class="form-control" placeholder="Password, at least 6 characters">
          </div>
          <div class="form-group">
            <input type="password" name="password_check"  v-model="password_check" class="form-control" placeholder="Password Double Check">
          </div>   
          <div class="form-group">
            <input type="text" name="first_name"  v-model="first_name" class="form-control" placeholder="first_name">
          </div>
          <div class="form-group">
            <input type="text" name="last_name" v-model="last_name" class="form-control" placeholder="last_name">
          </div>
          <div class="form-group">
            <input type="email" name="email"  v-model="email" class="form-control" placeholder="email">
          </div>                                       
          <button type="submit" class="btn btn-lg btn-primary btn-block">Register</button>
          <p class="p3 mb-3 font-weight-normal text-center">{{inccorrectmsg}}</p>
        </form>
        <div v-if="waitActivate">
          <h6> {{afterRegistermsg}}</h6>
          <div class="col text-center" v-if="afterActivate">
            <button type="submit" class="btn btn-default" v-on:click="tologin()"> return to login page</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import { getAPI } from '../axios-api'

  export default {
    name: 'register',
    data () {
      return {
        username: '',
        password: '',
        password_check: '',
        first_name: '',
        last_name: '',
        email: '',
        inccorrectmsg: '',
        afterRegistermsg: '',
        afterActivate: false,
        waitActivate: false
      }
    },

    created () {
      if (this.$route.query.token != undefined){
          getAPI.get('/api/user/verification?token='+this.$route.query.token,)
          .then(() => {
            this.waitActivate = true
            this.afterActivate = true
            this.afterRegistermsg = 'activation success, please login.'
          })
          .catch(err => {
            this.inccorrectmsg = 'activation fail'
            console.log(err)
          })
      }
    },

methods: {
      tologin(){
        this.$router.push({ name: 'login' })
      },
      register () { 
        const reg = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        if (this.password == ''| this.username == '' | this.password_check == ''| 
            this.first_name == ''| this.last_name == ''| this.email == ''){
          this.inccorrectmsg = 'some field is empty'
        } else if (!reg.test(this.email)){
          this.inccorrectmsg = 'email format wrong'
        } else if(this.username.length < 4) {
          this.inccorrectmsg = 'username should have at least 4 characters'
        } else if(this.password.length < 6) {
          this.inccorrectmsg = 'password should have at least 6 characters'
        } else if(this.password != this.password_check) {
          this.inccorrectmsg = 'password double check fail'
        } else {
          getAPI.post('/api/user/register', {
          username: this.username,
          password: this.password,
          password_check: this.password_check,
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,          
        })
        .then(() => {
          this.waitActivate = true
          this.afterRegistermsg = 'please click activation mail to verify your account'
        })
        .catch((err) => {
          this.inccorrectmsg = 'username or email repeat'
          console.log(err)
        })
        }
        }
    }
  }
</script>

<style>
body { 
  background-color:#f4f4f4;
}
input {
    padding: 25px 10px;
}
</style>
