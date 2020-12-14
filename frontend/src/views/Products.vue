<template>
  <div class="products">
    <Navbar></Navbar> 
      <div class="album py-5 bg-light">
          <div class="container">
            <div class="row">
              <div v-for="product in ProductData" :key="product.id" class="col-md-4">
                <div class="card mb-4 box-shadow">
                  <img class="card-img-top" :src="product.image" alt="Card image cap">
                  <div class="card-body text-center">
                      <h5 class="card-text"> {{product.name}} | {{product.price}} $</h5><br>
                      <div class="d-flex justify-content-center align-items-center">
                        <button type="button" class="btn btn-light" v-on:click="decreaseQuantity(product.id)"> - </button>
                        <input type="number" :id="product.id" class="form-control input-number" value="1" min="1" :max="product.quantity">
                        <button type="button" class="btn btn-light" v-on:click="addQuantity(product.id, product.quantity)"> + </button>
                      </div>
                      <div class="d-flex justify-content-center">
                        <button type="button" class="btn btn-primary" v-on:click="addtoCart(product.id)"> add to cart </button>
                      </div>
                      <small class="card-text" :id="product.id+'sign'"></small>
                  </div>
                </div>
              </div>
            </div>
          </div>
      </div>
  </div>
</template>

<script>
  import Navbar from '../components/Navbar'
  import { getAPI, getAPIwithToken} from '../axios-api'

  export default {
    name: 'Products',

    data () {
      return {
          ProductData: []
        }
    },
  
    components: {
      Navbar
    },

    created () {
      getAPI.get('/api/product/',)
      .then(response => {
        this.ProductData = response.data.results
      })
      .catch(err => {
        console.log(err)
      })
    },

    methods: {
      addQuantity(id, max){
        if (document.getElementById(id).value < max){
          document.getElementById(id).value ++
        }
      },
      decreaseQuantity(id){
        if (document.getElementById(id).value > 1){
          document.getElementById(id).value --
        }
      },
      addtoCart(id, quantity){
        if (!this.$store.getters.isValidaccess){
          this.$router.push({ name: 'login' })
        }else if (!this.$store.state.cart_set.has(id)){

          quantity = document.getElementById(id).value
          getAPIwithToken.post('/api/orderitem/', {item: id, quantity: quantity})
        .then(response => {
          this.$store.state.cart.push(response.data)
          this.$store.state.cart_set.add(id)
          document.getElementById(id).value  = 1
          document.getElementById(id+'sign').innerHTML = 'buy success'
        })
        .catch(err => {
          console.log(err)
          document.getElementById(id+'sign').innerHTML = 'bad request'
        })

        }else{
          quantity = document.getElementById(id).value
          var orderitemid = this.$store.state.cart.find(function(ele){
              return ele.item == id;          
          }).id

          getAPIwithToken.patch('/api/orderitem/'+orderitemid+'/', {quantity: quantity})
        .then((response) => {
          var index = this.$store.state.cart.findIndex(x => x.id == response.data.id)
          this.$store.state.cart[index].quantity = response.data.quantity
          document.getElementById(id).value  = 1
          document.getElementById(id+'sign').innerHTML = 'change request amount'
        })
        .catch(err => {
          console.log(err)
          document.getElementById(id+'sign').innerHTML = 'bad request'
        })
        }
      },

    },
  
  }
</script>

<style scoped>
  input {
    text-align: center;
  }
</style>

