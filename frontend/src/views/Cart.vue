<template>
  <div class="products">
    <Navbar></Navbar> 
      <div class="album py-5 bg-light">
          <div class="container">
            <h2> Cart </h2>
            <div class="card" v-if="CartData.length==0">
                <h5 class="card-text text-center">there is no item in cart.</h5>
            </div>            
            <div class="card">
                <div class="card-group" v-for="cart in CartData" :key="cart.id">
                  <div class="col-sm-10 d-flex justify-content-between">
                    <h5> {{ProductData[cart.item-1]['name']}}</h5> 
                    <h5> {{ProductData[cart.item-1]['price']}} $ / {{cart.quantity}} pcs</h5>
                    <button type="button" class="btn btn-light" v-on:click="deleteItem(cart.id)">Delete</button>
                  </div>
                </div>
                <div class="col text-right" v-if="CartData.length!=0">
                  <br>
                  <p>Enter the address to confirm order: 
                    <input type="text" id="address" name="address" value="" style="width:300px;height:10px">
                    <button type="button" class="btn btn-light" v-on:click="formOrder()">Send Order</button>
                  </p>
                </div>
            </div>
            <br><br>
            <h2> Orders </h2>
            <div class="card" v-if="OrderData.length==0">
                <h5 class="card-text text-center">there is no order formed yet.</h5>
            </div>            
            <div class="container" >
                <div class="card" v-for="order in OrderData" :key="order.id">
                  <dir class="row">
                    <div class="col-md-6 text-left">
                        <h5 class="card-text text-left">Order id:
                          <span style="float:right;">{{order.id}} </span>
                        </h5>
                        <h5 class="card-text text-left">Order state:
                          <span style="float:right;">{{order.state}} </span>
                        </h5>
                        <h5 class="card-text text-left">Order created_date:
                          <span style="float:right;">{{order.created_date.slice(0, 10)}}</span>
                        </h5>                        
                        <h5 class="card-text text-left">Order address:
                          <span style="float:right;">{{order.address}} </span>
                        </h5>
                        <h5 class="card-text text-left">Order total:
                          <span style="float:right;">{{order.total}} $</span>
                        </h5>
                        <br>
                    </div>
                    <br>
                    
                    <div class="col-md-5 text-left">
                        <h5> Orders Items:</h5>
                        <div v-for="item in order.orderitem_set" :key="item.id">
                          <div class="col-sm-12 d-flex justify-content-between">
                            <h5> {{ProductData[item.item-1].name}}</h5>
                            <h5>{{ProductData[item.item-1].price}} $ / {{item.quantity}} pcs</h5>
                          </div>
                        </div>
                        <br>
                    </div>
                  </dir>
              </div>
            </div>
            
          </div>
      </div>
  </div>
</template>

<script>
  import Navbar from '../components/Navbar'
  import { getAPI, getAPIwithToken} from '../axios-api'
  // import { mapState } from 'vuex'

  export default {
    name: 'Cart',

    data () {
      return {
          CartData: this.$store.state.cart,
          OrderData: this.$store.state.order,
          // ProductData: [{name:'d', price:'d'},{name:'d', price:'d'},{name:'d', price:'d'},{name:'d', price:'d'},{name:'d', price:'d'},{name:'d', price:'d'},{name:'d', price:'d'},{name:'d', price:'d'},{name:'d', price:'d'},{name:'d', price:'d'}], 
          ProductData: [],
        }
    },

    components: {
      Navbar
    },


    created () {
      // console.log('created')
      getAPI.get('/api/product/',)
      .then(response => {
        // console.log('created1')
        this.ProductData = response.data.results
        // console.log('created2')
      })
      .catch(err => {
        console.log(err)
      })
    },

    methods: {
      deleteItem(id){
        getAPIwithToken.delete('/api/orderitem/'+id+'/')
        .then(() => {
          var index = this.$store.state.cart.findIndex(x => x.id == id)
          this.$store.state.cart.splice(index, 1)
          this.$router.push({ name: 'cart' })
        })
        .catch(err => {
          console.log(err)
        })
      },
      formOrder(){
        var address = document.getElementById("address").value
        getAPIwithToken.post('/api/order/', {address: address})
        .then(() => {
          this.$store.dispatch('userReLogin').then(response => {
            this.$router.go(0)
            }).catch(err => {
            console.log(err)
            })
        })
        .catch(err => {
          console.log(err)
        })
      }
    },

  }
</script>

<style scoped>
  .card{
    margin-bottom: 10px;   
  }
  .card-group {
    margin-left: 2em;
  }

  button {
    width:100px;
    height:30px;
    position:relative;
    padding:0em
  }

  input {
    text-align: center;
  }
</style>

