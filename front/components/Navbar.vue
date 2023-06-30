<template>
  <div>
    <Menubar :model="items">
      <template #start>
        <img alt="logo" src="/images/logo.svg" height="40" class="mr-2"/>
      </template>
      <template #end>
        <ul role="menubar" class="p-menubar-root-list">
          <li role="none" class="p-menuitem"><a @click.prevent="logout" href="" role="menuitem" class="p-menuitem-link"><span
            class="p-menuitem-icon pi pi-fw pi-power-off"></span> <span class="p-menuitem-text">Выход</span></a>
          </li>
        </ul>
      </template>
    </Menubar>

  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Menubar from 'primevue/menubar';


interface MenuItem {
  label: string,
  icon: string,
  to: string,
  items?: Array<MenuItem>,
  style?: string
}

let connections: MenuItem = {
  label: 'Подключения',
  icon: 'pi pi-fw pi-database',
  to: '/connections',
}


let tasks: MenuItem = {
  label: 'Задачи',
  icon: 'pi pi-fw pi-wrench',
  to: '/tasks',
}

export default Vue.extend( {
  name: "Navbar",
  data: () => {
    return {
      items: [
        connections,
        tasks
      ] as Array<MenuItem>
    }
  },
  components: {
    Menubar
  },
  methods: {
    async logout(){
      await this.$auth.logout();
    }
  }
})
</script>

<style scoped>

</style>
