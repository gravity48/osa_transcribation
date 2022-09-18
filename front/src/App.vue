<template>
  <router-view></router-view>
</template>

<script>
import TokenService from "@/services/token.service";

export default {
  name: 'App',
  data() {
    return {
    }
  },
  components: {
  },
  mounted() {
    this.$router.beforeEach(async (to, from)  => {
      this.$store.commit('setActiveTab', to.name);
    });
    if(!TokenService.getUser()){
        this.$router.push('/login');
    }
    else {
      if (window.location.pathname === '/'){
        this.$router.push('/home');
      }
      else{
        this.$router.push(window.location.pathname);
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
html{
  min-height: 100vh;
}
body{
  margin: 0;
}
</style>
