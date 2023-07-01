<template>
  <div class="flex flex-column ">
    <div class="col-10 flex align-items-center justify-content-end">
      <div id="add-connection">
        <p><i class="pi pi-plus"></i> Добавить соединение</p>
      </div>
    </div>
    <div id="connections-content">
      <ul>
        <li v-for="connection in connections">
          <div class="flex align-items-center justify-content-center">
            <p>{{ connection.alias }}</p>

          </div>
          <div class="flex align-items-center justify-content-center">
            <p>{{ connection.db_status }}</p>
            <i class="pi pi-refresh"></i>
            <i class="pi pi-cog"></i>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';
import {mapActions, mapGetters} from 'vuex';

export default Vue.extend({
  name: "index",
  middleware: ['auth'],
  computed: {
    ...mapGetters('connections', ['connections'])
  },
  methods: {
    ...mapActions('connections', ['fetchConnections'])
  },
  mounted() {
    this.fetchConnections();
  }
})
</script>

<style scoped>

#add-connection {
  cursor: pointer;
  padding: 5px;
  border: solid black 1px;
  border-radius: 40px;
}

#add-connection:hover, ul li:hover {
  background-color: #e9ecef;
}

ul {
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: start;
  padding: 0;
  margin: 0 10px;
}

ul li {
  display: flex;
  justify-content: space-between;
  width: 100%;
  border-radius: 25px;
  border: 1px solid black;
  padding: 10px 25px;
  margin: 10px 0;
}

ul li div:first-child {
  user-select: none;
}

ul li div:last-child i {
  display: block;
  font-size: 1.4em;
  cursor: pointer;
  margin: 0 5px;
}
ul li div:last-child p{
  user-select: none;
  padding-right: 10px;
}


</style>
