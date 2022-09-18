<template>
  <div class="block">
    <nav>
      <ul class="vertical-menu">
        <li>
          <div class="osa-menu-icons">
            <img src="../assets/logo.png">
          </div>
        </li>
        <li :class="{active: this.$store.state.activeTab === 'Home'}">
          <router-link id='logotype-main'  :to="{name: 'Home'}"><span id="logotype-name">OSA</span>
            <span id="logotype-proj-name">transcribation</span></router-link>
        </li>
        <li :class="{active: this.$store.state.activeTab === 'Connections' }">
          <router-link :to="{name: 'Connections'}">Connections</router-link>
        </li>
        <li :class="{active: this.$store.state.activeTab === 'Tasks'}">
          <router-link :to="{name: 'Tasks'}">Tasks</router-link>
        </li>
        <li class="filler">
        </li>
        <li><a id="logout-href" href="javascript:;" @click="logout">Logout</a></li>
      </ul>
    </nav>
    <div id="content">
      <Greetings v-if="this.$store.state.activeTab === 'Home'" :username="username"/>
      <router-view @show_users_data="(status) => show_users_data = status"></router-view>
    </div>
  </div>
</template>

<script>
import viewService from "@/services/view-service";
import authService from "@/services/auth-service";
import Greetings from "@/components/Greetings";
import Comp from "@/assets/js/comp";
import $ from 'jquery';

export default {
  name: "HomeView",
  components: {
    Greetings,
  },
  data() {
    return {
      'info': '',
      'username': String,
      'is_staff': Boolean
    }
  },
  methods: {
    logout() {
      authService.logout();
      location.reload();
    },
  },
  mounted() {
    $(document).ready(Comp);
    viewService.users_api().then(response => {
      this.username = response.data.username;
      this.is_staff = response.data.is_staff;
    });
  },
  updated() {

  }
}
</script>

<style scoped>
.block {
  display: flex;
  flex-wrap: wrap;
}

.block nav {
  background-color: #eee; /* Grey background color */
  text-align: left;
}

.vertical-menu {
  position: fixed;
  padding: 0;
  margin: 0;
  height: 65px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  list-style-type: none;
}

#content {
  width: 100%;
  margin-top: 50px;
}

.vertical-menu li{
  display: flex;
  align-items: center;
  justify-content: center;

}
.vertical-menu li a {
  height: 100%;
  display: block;
  text-align: center;
  color: black; /* Black text color */
  padding: 12px; /* Add some padding */
  text-decoration: none; /* Remove underline from links */
  width: 115px;
  box-sizing: border-box;
  line-height: 38px;
}

#settings-href {
  max-width: 0;
  padding: 12px;
  overflow: hidden;
  box-sizing: border-box;
  transition: max-width 0.2s ease-out;
}

.vertical-menu li:not(:nth-child(4n+1)):hover {
  background-color: #ccc; /* Dark grey background on mouse-over */
}

.vertical-menu li.active, .vertical-menu li.active:hover {
  background-color: #4CAF50; /* Add a green color to the "active/current" link */
  color: white;
}


.filler {
  flex-grow: 1;
}

.filler.active:hover{
  background-color: transparent;
}

#logotype-main {
  text-align: center;
  padding: 15px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

#logotype-name {
  display: block;
  font-size: 32px;
  line-height: 31px;
}

#logotype-proj-name {
  display: block;
  font-size: 10px;
  line-height: 10px;
  margin-top: -2px;
}

.osa-menu-icons {
  display: block;
  height: 100%;
}

.osa-menu-icons > img {
  height: 100%;
}

</style>