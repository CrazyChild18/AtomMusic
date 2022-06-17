<template>
  <el-aside width="250px">
    <div style="margin-left: 12%; height: 20%; margin-top: 15%;">
      <!--标题-->
      <h2 style="display: inline;color: white;font-size: x-large" class="apple-font">Atom Cloud Music</h2>
      <!--      <h2 style="display: inline; color: cornflowerblue;background-color: black">Hub</h2>-->
      <!--Logo-->
      <div class="demo-basic--circle">
        <div class="block" style="margin-left: 15%; margin-top: 15%">
          <!--          <el-avatar :size="70" :src="circleUrl"></el-avatar>-->
          <el-image style="width: 100px; height: 47px" :src="circleUrl"/>
        </div>
      </div>
    </div>

    <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        router="True"
        text-color="#fff"
        active-text-color="#6103E9"
    >

      <!-- 歌曲界面链接 -->
      <router-link v-bind:to="{ name: 'music', params: { id: sharedState.user_id }}" class="barItem">
        <el-menu-item>
          <el-icon>
            <headset/>
          </el-icon>
          <el-link>
            <div>Play Music</div>
          </el-link>
        </el-menu-item>
      </router-link>

      <!-- Account link -->
      <router-link v-bind:to="{ name: 'info', params: { id: sharedState.user_id }}" class="barItem">
        <el-menu-item>
          <el-icon>
            <avatar/>
          </el-icon>
          <el-link>
            <div>Account</div>
          </el-link>
        </el-menu-item>
      </router-link>

      <!-- Recognize link -->
      <router-link v-bind:to="{ name: 'recognize'}" class="barItem">
        <el-menu-item>
          <el-icon>
            <search/>
          </el-icon>
          <el-link>
            <div>Recognize Songs</div>
          </el-link>
        </el-menu-item>
      </router-link>

      <!-- Recommend link -->
      <router-link v-bind:to="{ name: 'recommend'}" class="barItem">
        <el-menu-item>
          <el-icon>
            <help-filled/>
          </el-icon>
          <el-link>
            <div>Recommendation</div>
          </el-link>
        </el-menu-item>
      </router-link>

      <!-- Data Visualization link -->
      <router-link v-bind:to="{ name: 'userDataVisualization', params: { id: sharedState.user_id }}"
                   class="barItem">
        <el-menu-item>
          <el-icon>
            <Histogram/>
          </el-icon>
          <el-link>
            <div>Footprint</div>
          </el-link>
        </el-menu-item>
      </router-link>

      <!-- Log out link -->
      <el-menu-item v-on:click="handlerLogout" index="/login">
        <el-icon>
          <circle-close-filled/>
        </el-icon>
        <el-link>
          <div>Log out</div>
        </el-link>
      </el-menu-item>
    </el-menu>

  </el-aside>
</template>

<script setup>
import {
  Monitor,
  Avatar,
  Search,
  CircleCloseFilled,
  Histogram, Service, Promotion, Headset, Help, HelpFilled,
} from '@element-plus/icons-vue'
import {reactive, toRefs} from 'vue'
import store from '../store.js'
import axios from "axios";
import {ref} from "@vue/reactivity";
import {message} from "@/utils/message";


const sharedState = store.state

const state = reactive({
  circleUrl: 'white-logo.png',
  sizeList: ['large', 'default', 'small'],
})

const {circleUrl} = toRefs(state)

function handlerLogout(e) {
  store.logoutAction()
  message.info('You have logged out!')
  this.$router.push('/login')
}

</script>

<style>
.el-aside {
  height: 100vh;
  background-image: linear-gradient(to bottom, #6103E9, #1B76D3);
}

.el-menu {
  background-image: linear-gradient(to bottom, #511fe3, #3847db);
}

.barItem {
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
}

.el-menu-item:hover div {
  color: #6103E9;
}

.el-menu-item:hover i {
  color: #6103E9;
}

a:hover {
  text-decoration: none;
}

</style>