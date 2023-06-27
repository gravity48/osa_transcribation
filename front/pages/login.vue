<template>
  <div id="all-screen" class="flex justify-content-center align-items-center">
    <form class="lg:col-5" @keyup.enter="login" @submit.prevent="login">
      <div class="flex flex-column gap-2 ">
        <div class="flex flex-column gap-2">
          <label for="username">Логин</label>
          <InputText id="username" v-model="auth_data.username" aria-describedby="username-help"/>
        </div>
        <div class="flex flex-column gap-2">
          <label for="password">Пароль</label>
          <Password inputClass="w-12" id="password" v-model="auth_data.password" aria-describedby="username-help"
                    toggleMask
                    :feedback="false"/>
        </div>
        <Button label="Войти" type="submit" severity="success" class="xl:col-6 xl:mt-2" outlined/>
      </div>
    </form>
  </div>

</template>

<script>
import Vue from "vue";
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';


export default Vue.extend({
  name: "login",
  layout: 'empty',
  components: {
    InputText,
    Password,
    Button,
  },
  data: () => {
    return {
      auth_data: {
        username: '',
        password: ''
      },
    }
  },
  methods: {
    login() {
      this.$auth.loginWith('local', {data: this.auth_data}).then(response => {
        return this.$auth.setUserToken(response.data.access, response.data.refresh)
      })
    }
  }
})
</script>

<style scoped>

#all-screen {
  height: 100vh;
  width: 100vw;
}

#all-screen > form {
  max-width: 400px;
}

</style>
