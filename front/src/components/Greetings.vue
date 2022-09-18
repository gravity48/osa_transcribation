<template>
  <h1>Добро пожаловать {{username}}</h1>
  <div id="change_list">
    <h2>Список изменений в системе версии 1.0.0</h2>
    <h3>Техническая оптимизация</h3>
    <h3>Изменения интерфейса</h3>
    <p>1) Перенесен пользовательский интерфейс приложения на фреймворк Vue </p>
  </div>
</template>

<script>
export default {
  name: "GreetingsView",
  props:{
    'username': String
  }
}
</script>

<style scoped>
#change_list h2{
  text-align: left;
}
#change_list h3{
  text-align: left;
}
#change_list p{
  text-align: justify;
}

</style>