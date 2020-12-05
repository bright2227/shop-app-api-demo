<template>
  <div>
  <div class="container text-dark">
    <div class="row justify-content-md-center">
      <div class="col-md-5 p-3 login justify-content-md-center">
        <h1 class="h3 mb-3 font-weight-normal text-center">Reset password</h1>

        <form v-on:submit.prevent="resetrequest" v-if="Request">
          <div class="form-group">
            <input type="text" name="username" id="user" v-model="username" class="form-control" placeholder="Username">
          </div>
          <div class="form-group">
            <input type="email" name="email"  v-model="email" class="form-control" placeholder="email">
          </div>                                       
          <button type="submit" class="btn btn-lg btn-primary btn-block">Request reset</button>
          <p class="p3 mb-3 font-weight-normal text-center">{{inccorrectmsg}}</p>
        </form>       

        <form v-on:submit.prevent="resetpass" v-if="Resetpass">
          <div class="form-group">
            <input type="password" name="newpassword" v-model="newpassword" class="form-control" placeholder="Newpassword at least 6 characters">
          </div>
          <div class="form-group">
            <input type="password" name="password_check" v-model="password_check" class="form-control" placeholder="Password Double Check">
          </div>                                    
          <button type="submit" class="btn btn-lg btn-primary btn-block">Set new password</button>
          <p class="p3 mb-3 font-weight-normal text-center">{{inccorrectmsg}}</p>
        </form>

        <h6> {{aftermsg}} </h6>

        <div v-if="Resetsuccess">
          <div class="col text-center">
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
  name: 'reset',
  data () {
    return {
      username: '',
      email: '',
      newpassword: '',
      password_check: '',
      inccorrectmsg: '',
      aftermsg: '',
      Resetpass: false,
      Request: true,
      Resetsuccess: false
    }
  },

  created () {
    if (this.$route.params.id != undefined){
      this.Request = false
      this.Resetpass = true
    }
  },

  methods: {
      tologin(){
        this.$router.push({ name: 'login' })
      },
      resetpass (){ 
      if (this.password_check == '' | this.newpassword == ''){
          this.inccorrectmsg = 'some field is empty'
        } else if (this.newpassword.length < 6){
          this.inccorrectmsg = 'password should have at least 6 characters'
        } else if (this.newpassword != this.password_check){
          this.inccorrectmsg = 'password double check fail'
        } else {
          getAPI.patch('/api/user/passreset/setpass/'+this.$route.params.id,{
          password: this.newpassword
        })
        .then(() => {
          this.Resetpass = false
          this.Resetsuccess = true
          this.aftermsg = 'password reset success, please back to login'
        })
        .catch((err) => {
          this.inccorrectmsg = 'token fail'
          console.log(err)
        })
        }
      },
      resetrequest (){ 
        const reg = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        if (this.username == '' | this.email == ''){
          this.inccorrectmsg = 'some field is empty'
        } else if (!reg.test(this.email)){
          this.inccorrectmsg = 'email format wrong'
        } else {
          getAPI.post('/api/user/passreset/request',{
          username: this.username,
          email: this.email,          
        })
        .then(() => {
          this.Request = false
          this.aftermsg = 'please click mail to access reset password'
        })
        .catch((err) => {
          this.inccorrectmsg = 'username or email is wrong'
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
  .login{
    background-color:#fff;
    margin-top:10%;
  }
  input {
    padding: 25px 10px;
}
</style>
