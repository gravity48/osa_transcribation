<template>
  <img alt="Vue logo" src="../assets/logo.png">
  <h1>OSA Auth</h1>
  <div id="block1">
    <div class="center-block">
      <form id="login_form" @keyup.enter="sendAuth">
        <label for="login">Username: </label>
        <input v-model='user.username' id='login' type="text" name="login" required>
        <label for="password">Password: </label>
        <input v-model='user.password' id="password" name="password" type="password" required>
        <button type="button" @click="sendAuth">Submit</button>
        <p v-if="error_txt">{{ error_txt }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import TokenService from "@/services/token.service";
import AuthService from "@/services/auth-service";


export default {
  name: "LoginView",
  data() {
    return {
      user: {
        username:'',
        password:''
      },
      'error_txt': '',
    }
  },
  methods: {
    sendAuth() {
      AuthService.login(this.user).then(response => {
        let user = {
          'token': response.data.access,
          'refresh': response.data.refresh
        }
        TokenService.setUser(user);
        this.$store.commit('setAuthenticate', true);
        this.$router.push({name: 'App'});
      }).catch(reason => {
        this.error_txt = 'Неверный логин/пароль';
      });
    }
  },
  mounted() {
    if (this.$store.state.isAuthenticate != null) {
      this.$router.push({name: 'Home'});
    }
  }
}
</script>

<style scoped>

input {
  height: 100%;
  width: 100%;
  margin: 5px 0;
}

.center-block {
  display: flex;
  align-items: center;
  justify-content: center;
}

#login_form {
  max-width: 200px;
  max-height: 200px;
}


</style>