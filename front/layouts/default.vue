<template>
  <div>
    <div class="navbar">
       <Navbar />
    </div>
    <nuxt />
  </div>

</template>

<script lang="ts">
import Navbar from '~/components/Navbar.vue';

export default {
  name: "default",
  components: {
    Navbar,
  }
}
</script>

<style scoped>

</style>
