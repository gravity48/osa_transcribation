<template>
  <div>
    <h3>Соединение {{ connection.alias }}</h3>
    <div id='conn-params' class="flex flex-row">
      <div id="required-params">
        <Dropdown
          v-model="connection.db_system"
          :options="conn_system"
          optionValue="code"
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
import {useRoute, useStore, useContext, useAsync, ssrRef, computed, watch} from "@nuxtjs/composition-api";
import {useConnection} from '~/composables/connection';
import Dropdown from "primevue/dropdown/Dropdown";

const route = useRoute();
const store = useStore();
const {$axios} = useContext();

const conn_system = computed(() => store.getters['conn_system']);
const conn_status = computed(() => store.getters['conn_status']);

const {connection, fetchConnection, watcherConnection} = useConnection();

useAsync(
  async () => {
    connection.value = await fetchConnection(route.value.params.id)
    await store.dispatch('fetch');
  }
);

watch(connection, watcherConnection, {deep: true, flush: 'post'});

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
