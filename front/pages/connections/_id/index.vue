<template>
  <div>
    <h3>Соединение {{ con_detail.alias }}</h3>
    <div id='conn-params' class="flex flex-row">
      <div id="required-params">
        <Dropdown
          v-model="con_detail.db_status"
          :options="conn_system"
          style="min-width: 14rem"
          optionLabel="name"
          placeholder="Select a City"
        />
      </div>
      <div id="non-required-params">

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">


// import Vue from 'vue';
// import {mapActions, mapGetters} from "vuex"
// import Dropdown from 'primevue/dropdown';



// export default Vue.extend({
//   name: "index",
//   async fetch({store}) {
//     await store.dispatch("fetch");
//   },
//   components: {
//     Dropdown,
//   },
//   methods: {
//     ...mapActions('connections', ['retrieveConnection'])
//   },
//   mounted() {
//     this.retrieveConnection(this.$route.params.id);
//   },
//   computed: {
//     ...mapGetters('connections', ['con_detail']),
//     ...mapGetters(['conn_status', 'conn_system']),
//   }
// })
</script>

<style scoped>

h3 {
  text-align: center;
}

#conn-params > #required-params {
  border: 1px solid black;
}

#conn-params > #non-required-params {
  border: 1px solid red;
}
</style>
