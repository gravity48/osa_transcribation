<template>
  <div>
    <nuxt-link to="/login"> Login Page</nuxt-link>
    <button id="logout-btn"  @click.prevent="logout">Logout Btn</button>
    <button id="test-btn" @click.prevent="test_connections"> Test Btn </button>
  </div>

</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'IndexPage',
  data: ()=>{
    return {
      connections: []
    }
  },
  methods:{
    logout(){
      this.$auth.logout().catch(err =>{
      });
    },
    test_connections(){
      this.$axios.get('api/v1/connections/connections/').then(response=>{
        console.log(response.data);
      })
    }
  },
  async mounted() {
    //setInterval(this.test_connections, 3000);
    // await this.$axios.get('api/v1/connections/connections/');
  }
})
</script>
