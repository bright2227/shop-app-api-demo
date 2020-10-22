<template>
  <div class="products">
    <Navbar></Navbar> 
      <div class="album py-5 bg-light">
          <div class="container">
            <h2> Cart </h2>
            <div class="card">
                <div class="row" v-if="CartData.length==0">
                    <div class="col-md-12 text-left">
                        <h5 class="card-text text-left">there is no item in cart.</h5>
                    </div>
                </div>
                <div class="row" v-for="cart in CartData" :key="cart.id">
                  <div class="col-sm-12 d-flex justify-content-between">
                    <h5> {{cart.name}} | {{cart.price}} $</h5>
                    <h5> {{cart.quantity}} pcs</h5>
                    <button type="button" class="btn btn-light" v-on:click="deleteItem(cart.id)">Delete</button>
                  </div>
                </div>

            </div>
            <br><br>
            <h2> Orders </h2>
            <div class="card">
                <div class="row" v-if="OrderData.length==0">
                    <div class="col-md-6 text-left">
                        <h5 class="card-text text-left">there is no order formed yet.</h5>
                    </div>
                </div>
                <div class="row" v-for="order in OrderData" :key="order.id">
                    <div class="col-md-6 text-left">
                        <h5 class="card-text text-left">Order id:
                          <span style="float:right;">{{order.id}} </span>
                        </h5>
                        <h5 class="card-text text-left">Order state:
                          <span style="float:right;">{{order.state}} </span>
                        </h5>
                        <h5 class="card-text text-left">Order address:
                          <span style="float:right;">{{order.address}} </span>
                        </h5>
                        <h5 class="card-text text-left">Order total:
                          <span style="float:right;">{{order.total}} </span>
                        </h5>
                    </div>
                    <div class="col-md-6 text-left">
                        <h5> Orders Items:</h5>
                        <div v-for="item in order.orderitem_set" :key="item.id">
                          <div class="col-sm-12 d-flex justify-content-between">
                            <h5> {{ProductData[item.id].name}} | {{ProductData[item.id].price}} $</h5>
                            <h5>{{item.quantity}} pcs</h5>
                            <button type="button" class="btn btn-light" v-on:click="deleteItem(item.id)">Delete</button>
                          </div>
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
  // import { mapState } from 'vuex'

  export default {
    name: 'Cart',

    data () {
      return {
          CartData: this.$store.state.cart,
          OrderData: this.$store.state.order,
          ProductData: {'1':'a'}, // 似乎要觸發變動 ProductData才會顯現，如果只有 {} 那Template也只會出現{}
        }
    },

    components: {
      Navbar
    },

    created () {
      getAPI.get('/api/product/',)
      .then(response => {
        response.data.results.forEach(ele => (this.ProductData[ele.id]=ele))
        this.CartData.forEach(ele => this.iteminform(ele))
      })
      .catch(err => {
        console.log(err)
      })
    },

    methods: {
      deleteItem(id){
        getAPIwithToken.delete('/api/orderitem/', {id: id})
        .then(response => {
          console.log(response)
          this.$router.push({ name: 'cart' })
        })
        .catch(err => {
          console.log(err)
        })
      },
      iteminform(ele){
        ele['name'] = this.ProductData[ele.item].name
        ele['price'] = this.ProductData[ele.item].price
      }

    },
  
  }
</script>

<style scoped>
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

