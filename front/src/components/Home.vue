<template>
  <div class="block">
    <nav>
      <ul class="vertical-menu">
        <li>
          <div class="osa-menu-icons">
            <svg  viewBox="0 0 133 145" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
              <!-- Created with SVG-edit - https://github.com/SVG-Edit/svgedit-->
              <g class="layer">
                <title>Layer 1</title>
                <ellipse cx="174" cy="18" fill="none" id="svg_1" rx="42.5" ry="43.5" stroke="#000000" stroke-width="5" transform="rotate(176.829 120 57.166)"/>
                <ellipse cx="69.5" cy="40.5" fill="none" id="svg_3" rx="15" ry="15" stroke="#000000" stroke-width="5"/>
                <line fill="none" id="svg_5" stroke="#000000" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-width="5" x1="28.5" x2="106.16595" y1="83.5" y2="83.5"/>
                <line fill="none" id="svg_7" stroke="#000000" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-width="5" x1="25.5" x2="108.71658" y1="104.5" y2="104.5"/>
                <line fill="none" id="svg_8" stroke="#000000" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-width="5" x1="32.5" x2="101.52898" y1="125.5" y2="125.5"/>
                <line fill="none" id="svg_10" stroke="#000000" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-width="5" x1="79.5" x2="98.53943" y1="25.5" y2="6.46057"/>
                <line fill="none" id="svg_13" stroke="#000000" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-width="5" transform="rotate(-88.3397 51 16.5)" x1="41.48029" x2="60.51972" y1="26.01972" y2="6.98029"/>
                <line fill="none" id="svg_14" stroke="#000000" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-width="5" x1="105.48029" x2="122.51972" y1="85.01972" y2="70.98029"/>
                <line fill="none" id="svg_15" stroke="#000000" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-width="5" transform="rotate(39.2072 120.333 104.5)" x1="111.81362" x2="128.85305" y1="111.51972" y2="97.48029"/>
                <line fill="none" id="svg_16" stroke="#000000" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-width="5" transform="rotate(80.4069 111.333 134.5)" x1="102.81362" x2="119.85305" y1="141.51972" y2="127.48029"/>
                <line fill="none" id="svg_17" stroke="#000000" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-width="5" transform="rotate(71.8473 19.3333 77.5)" x1="10.81362" x2="27.85305" y1="84.51972" y2="70.48029"/>
                <line fill="none" id="svg_18" stroke="#000000" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-width="5" transform="rotate(39.2072 13.333 104.5)" x1="4.81369" x2="21.85312" y1="111.5195" y2="97.48007"/>
                <line fill="none" id="svg_20" stroke="#000000" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-width="5" transform="rotate(167.561 28.5 134.5)" x1="19.98055" x2="37.01999" y1="141.5194" y2="127.47997"/>
                <ellipse cx="40.5" cy="5" fill="none" id="svg_21" rx="1.5" ry="1.5" stroke="#000000" stroke-width="5"/>
                <ellipse cx="99" cy="5.5" fill="none" id="svg_22" rx="1.5" ry="1.5" stroke="#000000" stroke-width="5"/>
              </g>
            </svg>
          </div>
        </li>
        <li :class="{active: this.$store.state.activeTab === 'Home'}">
          <router-link id='logotype-main' :to="{name: 'Home'}"><span id="logotype-name">OSA</span>
            <span id="logotype-proj-name">transcribation</span></router-link>
        </li>
        <li :class="{active: this.$store.state.activeTab === 'Connections' }">
          <router-link :to="{name: 'Connections'}">Подключения</router-link>
        </li>
        <li :class="{active: this.$store.state.activeTab === 'Tasks'}">
          <router-link :to="{name: 'Tasks'}">Задачи</router-link>
        </li>
        <li class="filler">
        </li>
        <li><a id="logout-href" href="javascript:;" @click="logout">Logout</a></li>
      </ul>
    </nav>
    <div id="content">
      <Greetings v-if="this.$store.state.activeTab === 'Home'" :username="username"/>
      <router-view @preloader="(show_preloader) => preloader = show_preloader"></router-view>
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
      'is_staff': Boolean,
      'preloader': false,
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
@import "../assets/css/main";

.osa-menu-icons svg{
  width: 95%;
  height: 95%;
  position: relative;
  top: 2.5%;
  left: 2.5%;
}
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

.vertical-menu li {
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
  width: 130px;
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

.filler.active:hover {
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



</style>