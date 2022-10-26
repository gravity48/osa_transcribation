<template>
  <notifications position="bottom right">
  </notifications>
  <router-view></router-view>
  <div class="preloader hidden">
    <div class="osa-ico-preloader">
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
  </div>
</template>

<script>
import TokenService from "@/services/token.service";

export default {
  name: 'App',
  data() {
    return {
    }
  },
  components: {
  },
  mounted() {
    this.$router.beforeEach(async (to, from)  => {
      this.$store.commit('setActiveTab', to.name);
    });
    if(!TokenService.getUser()){
        this.$router.push('/login');
    }
    else {
      if (window.location.pathname === '/'){
        this.$router.push('/home');
      }
      else{
        this.$router.push(window.location.pathname);
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
html{
  min-height: 100vh;
}
body{
  margin: 0;
}

.vue-notification-wrapper{
  height: 100px;
  font-size: 14px;
  margin: 0 0 2px 0 !important;
}

.vue-notification-template{
  height: 100%;
}

.notification-title{
  padding: 5px 0;
}


.preloader{
  position: fixed;
  top: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgb(220,220,220, 0.5);
}

.preloader > .osa-ico-preloader{
  width: 50px;
  height: 50px;
}

.preloader svg{
  animation: pulse1 1.5s ease-in-out infinite;
}

@keyframes pulse1 {
  0% {
    opacity: 0;
    transform: scale(0.7);
  }

  30% {
    opacity: 1;
    transform: scale(1);
  }

  60% {
    opacity: 1;
    transform: scale(1.5);
  }

  100% {
    opacity: 0;
    transform: scale(2);
  }
}

.hidden{
  display: none;
}


</style>
