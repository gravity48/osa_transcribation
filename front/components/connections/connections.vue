<template>
  <div>
    <h3>{{ item }}</h3>
  </div>

</template>

<script lang="ts">
import Vue from 'vue';

export default  Vue.extend({
  name: "Connections",
  props:{
    item: String,
  },

})
</script>

<style scoped>

</style>
