<template>
  <div class="products">
    <Navbar></Navbar> 
      <div class="album py-5 bg-light">
          <div class="container">
            <div class="row">
              <div v-for="(product, index) in ProductData" :key="index" class="col-md-4">
                <div class="card mb-4 box-shadow">
                  <img class="card-img-top" :src="product.image" alt="Card image cap">
                  <div class="card-body text-center">
                      <h5 class="card-text"> {{product.name}} | {{product.price}} $</h5><br>
                      <div class="d-flex justify-content-center align-items-center">
                        <button type="button" class="btn btn-light" v-on:click="decreaseQuantity(index)"> - </button>
                        <input type="number" v-model="ProductQuantiy[index]" class="form-control input-number" min="0" :max="product.quantity">
                        <button type="button" class="btn btn-light" v-on:click="addQuantity(index)"> + </button>
                      </div>
                      <div class="d-flex justify-content-center">
                        <button type="button" class="btn btn-primary" v-on:click="addtoCart(index)"> add to cart </button>
                      </div>
                      <small class="card-text" >{{ProductMessage[index]}}</small>
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
          ProductData: [],
          ProductQuantiy: [],
          ProductMessage: []
        }
    },
  
    components: {
      Navbar
    },

    created () {
      getAPI.get('/api/product/',)
      .then(response => {
        this.ProductData = response.data.results
        this.ProductQuantiy = Array(this.ProductData.length).fill(0)
        this.ProductMessage = Array(this.ProductData.length).fill('')
      })
      .catch(err => {
        console.log(err)
      })
    },

    methods: {
      addQuantity(index){
        if (this.ProductQuantiy[index] < this.ProductData[index].quantity){
          this.ProductQuantiy.splice(index, index+1, this.ProductQuantiy[index]+1)  //vue can't watch over Array[index] = quantity
        }
      },
      decreaseQuantity(index){
        if (this.ProductQuantiy[index] > 0){
          this.ProductQuantiy.splice(index, index+1, this.ProductQuantiy[index]-1)
        }
      },
      addtoCart(index){
        var id = this.ProductData[index].id
        var quantity = this.ProductQuantiy[index]

        if (!this.$store.getters.isValidaccess){
          this.$router.push({ name: 'login' })
        }else if (!this.$store.state.cart_set.has(id)){

          getAPIwithToken.post('/api/orderitem/', {item: id, quantity: quantity})
        .then(response => {
          this.$store.state.cart.push(response.data)
          this.$store.state.cart_set.add(id)
          this.ProductQuantiy.splice(index, index+1, 0)
          this.ProductMessage.splice(index, index+1, 'buy success')
        })
        .catch(err => {
          console.log(err)
          this.ProductMessage.splice(index, index+1, 'bad request')
        })
        }else{
          let cart_index = this.$store.state.cart.findIndex(x => x.item == id)
          let orderitemid = this.$store.state.cart[cart_index].id

          getAPIwithToken.patch(`/api/orderitem/${orderitemid}/`, {quantity: quantity})
        .then((response) => {
          this.$store.state.cart[cart_index].quantity = response.data.quantity
          this.ProductQuantiy.splice(index, index+1, 0)
          this.ProductMessage.splice(index, index+1, 'change request amount')
        })
        .catch(err => {
          console.log(err)
          this.ProductMessage.splice(index, index+1, 'bad request')
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

