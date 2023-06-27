<template>
  <div>
    <nuxt-link to="/login"> Login Page</nuxt-link>
    <button id="logout-btn"  @click.prevent="logout">Logout Btn</button>
  </div>

</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'IndexPage',
  middleware: ['auth'],
  data: ()=>{
    return {
      connections: []
    }
  },
  methods:{
    logout(){
      this.$auth.logout();
      this.$router.push('/login');
    },
    test_connections(){
      this.$axios.get('api/v1/connections/connections/').then(response=>{
        console.log(response.data);
      }).catch(error=>{
        console.error(error);
      })
    }
  },
  mounted() {
    setInterval(this.test_connections, 3000);
  }
})
</script>
