<template>
  <div>
    <h3>Соединение {{ connection.alias }}</h3>
    <div id='conn-params' class="flex flex-row justify-content-around">
      <div id="required-params">
        <div class="input-grp">
          <InputText v-model="connection.alias" placeholder="Alias" />
        </div>
        <div class=input-grp>
          <Dropdown
            v-model="connection.db_system"
            :options="conn_system"
            optionValue="code"
            style="min-width: 14rem"
            optionLabel="name"
            placeholder="СУБД"
          />
        </div>
        <div class=input-grp>
          <InputText v-model="connection.ip" placeholder="DB ip" />
        </div>
        <div class=input-grp>
          <InputNumber v-model="connection.port" placeholder="Db port" />
        </div>
        <div class=input-grp>
          <InputText v-model="connection.db_login" placeholder="DB login" />
        </div>
        <div class=input-grp>
          <InputText v-model="connection.db_password" placeholder="DB password" />
        </div>
      </div>
      <div id="non-required-params">
        <div class="input-grp">
          <InputText v-model="connection.options.post" placeholder="Post"></InputText>
        </div>
        <div class="input-grp">
          <Checkbox v-model="connection.options.selected" :binary="true"></Checkbox>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {useRoute, useStore, useAsync,  computed, watch} from "@nuxtjs/composition-api";
import {useConnection} from '~/composables/connection';
import Dropdown from "primevue/dropdown/Dropdown";
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Checkbox from 'primevue/checkbox';


const route = useRoute();
const store = useStore();

const conn_system = computed(() => store.getters['conn_system']);

const {connection, fetchConnection, watcherConnection} = useConnection();

useAsync(
  async () => {
    connection.value = await fetchConnection(route.value.params.id);
  }
);

watch(connection, watcherConnection, {deep: true, flush: 'post'});

</script>

<style scoped>

h3 {
  text-align: center;
}


#conn-params > div {
  border: 1px solid black;
  border-radius: 25px;
  padding: 10px;
  margin: 5px;
}

#conn-params {
  margin: 0 5%;
}

#conn-params .input-grp{
  margin: 20px 0;
}
</style>
