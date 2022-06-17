<template>
  <!--加载-->
  <div
      v-if="!isReady"
      v-loading="!isReady"
      element-loading-text="Loading music, please wait......"
      element-loading-background="rgba(0, 0, 0, 0.6)"
      style="width: 80vw; height: 85vh; position: absolute; font-weight: bold;"
  >
  </div>

  <div class="music">
    <ul class="music-list" @mousewheel="changeMusic" :style="{transform: `translate(0,${musicCur * -100}%)`}">
      <template v-if="musicList.length != 0">
        <li v-for="item in musicList" :key="item.name">
          <!--左半侧-->
          <aside class="music-left">
            <h2 class="MusicTitle" style="margin-bottom: 20%">{{ item.name }}</h2>
            <ul v-for="w in item.writer" :key="w">
              <li style="text-align: right; margin-right: 5%; list-style: none; color: black"><h4>{{ w }}</h4></li>
            </ul>
          </aside>
          <!--右半侧-->
          <div class="music-right">
            <!--歌曲详情按钮-->
            <el-button type="primary" class="float-right" round @click="turnDetailPage(item.id)">
              <span class="detailButton">Go for Detail</span>
              <el-icon class="el-icon--right">
                <ArrowRight/>
              </el-icon>
            </el-button>
            <img class="musicPic" :src="item.picUrl"/>
            <!--音频-->
            <audio controls
                   class="musicAudio"
                   v-bind:src="item.url"
                   ref="musicAudioControl"
            >
            </audio>
            <!--            <audio controls-->
            <!--                   class="musicAudio"-->
            <!--                   v-bind:src="item.url"-->
            <!--            >-->
            <!--            </audio>-->
          </div>
        </li>
      </template>
    </ul>
  </div>

  <!--提醒-->
  <div id="error-box" ref="alert_box">
    <div class="face2">
      <div class="eye"></div>
      <div class="eye right"></div>
      <div class="mouth sad"></div>
    </div>
    <div class="shadow move"></div>
    <div class="message"><h1 class="alert">Ohhhh!</h1>
      <p>You've been listening to music for too long. Quit and rest.</p></div>
    <button class="button-box" @click="restNow()"><h1 class="red">Still Listen</h1></button>
  </div>
</template>

<script>
import store from "@/store";

import {
  ArrowRight
} from '@element-plus/icons-vue';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function waitFunc(time) {
  await sleep(time)
}

export default {
  name: "musicShow",

  components: {
    ArrowRight,
  },

  data() {
    return {
      isReady: false, // 检测是否完成歌曲加载
      otimer: null,
      counter: 1,
      isLike: false,
      userID: '',
      iSDetail: false,
      musicCur: 0,	//当前显示的是第几条
      musicTime: 0, //理论上是控制滑动速度的
      musicList: [], //初始化数据，插入10条
    };
  },

  methods: {
    // 休息
    restNow() {
      this.$refs.alert_box.style.display = "none";
      this.otimer = setInterval(() => {
        this.counter += 1   //这个this.counter指向的就是data中的counter
        const path = "/api/accDuration";
        const payload = {
          userID: this.userID,
          counter: this.counter,
        }
        this.$http.post(path, payload)
            .then((response) => {
            })
            .catch((error) => {
              console.log("更新累积时长出现问题:" + error);
            })
        if (this.counter % 300 === 0) {
          // 暂停音乐则释放此段代码
          // this.$refs.musicAudioControl[this.musicCur].pause()
          this.$refs.alert_box.style.display = "block";
          clearInterval(this.otimer)
        }
        // console.log('111')
      }, 1000);
    },

    // 切换音乐
    async changeMusic({deltaY}) {

      // 取消当前播放器播放
      const now = new Date().getTime()
      if (this.musicTime + 2000 > now) return;
      this.$refs.musicAudioControl[this.musicCur].pause();
      this.musicTime = now
      // 在此处完成页数更改
      this.musicCur += (deltaY > 0 ? 1 : -1)
      // 首页不允许向上
      if (this.musicCur < 0) this.musicCur = 0;
      // 重新插入5组数据
      // 在显示倒数第二个页面时开始加载
      if (this.musicCur >= this.musicList.length - 5) {
        const currentLength = this.musicList.length;
        const targetLength = currentLength * 2;
        const path = "/api/getMusic";
        const payload = {
          // 获取歌曲地址（当前设置为个性化新歌）
          url: this.netEaseURL + "personalized/newsong?limit=",
          // 加载歌曲数量
          musicNum: targetLength,
        }
        this.$http.post(path, payload)
            .then((response) => {
              console.log("更新歌曲成功");
              console.log(response);
              this.musicList = response.data
            })
            .catch((error) => {
              console.log("更新歌曲出现问题:" + error);
            })
      }
      // 播放当前页面
      console.log("当前播放页面: " + this.musicCur)

      //Avoid the Promise Error

      this.$refs.musicAudioControl[this.musicCur].currentTime = 0;

      let interval = setTimeout(() => {
        const playPromise = this.$refs.musicAudioControl[this.musicCur].play();
        if (playPromise !== undefined) {
          playPromise.then(_ => {
            // Automatic playback started!
          })
              .catch(error => {
                // Auto-play was prevented
                this.$refs.musicAudioControl[this.musicCur].play();
              }, 200);
        }
      }, 200)

      // await sleep(300)
      // clearInterval(interval)
      // await sleep(1700)
    },


    // 页面跳转函数
    turnDetailPage: function (musicId) {
      this.iSDetail = true
      console.log("点击进入歌曲详情")
      let routeData = this.$router.resolve({
        path: '/musicDetail',
        query: {
          musicId: musicId,
          userID: this.userID,
        }
      });
      window.open(routeData.href, '_blank');
    },

    // 初始化歌曲列表
    initMusicList: function () {
      const path = "/api/getMusic";
      const payload = {
        // 获取歌曲地址（当前设置为个性化新歌）
        url: this.netEaseURL + "/top/song?type=96",
        // 加载歌曲数量
        musicNum: 10,
      }
      this.$http.post(path, payload)
          .then((response) => {
            console.log(response);
            this.musicList = response.data
            this.isReady = true
          })
          .catch((error) => {
            console.log("获取歌曲阶段出现问题:" + error);
          })
    },

    beforeRouteLeave() {
      console.log('关闭该页面')
      clearInterval(this.otimer)
      return undefined;
    }
  },

  // 在页面加载之前
  created() {
    this.isReady = false;
    this.initMusicList();
    this.userID = this.$route.params.id
    this.iSDetail = false
  },

  // 页面完成加载
  mounted() {
    // this.$refs.musicAudioControl[this.musicCur].play()
    const path = "/api/cleanDuration";
    const payload = {
      userID: this.userID,
    }
    this.$http.post(path, payload)
        .then((response) => {
          // console.log(response);
        })
        .catch((error) => {
          console.log("清除累积时长出现问题:" + error);
        })
    this.otimer = setInterval(() => {
      this.counter += 1
      const path = "/api/accDuration";
      const payload = {
        userID: this.userID,
        counter: this.counter,
      }
      this.$http.post(path, payload)
          .then((response) => {
            // console.log(response, this.counter);
          })
          .catch((error) => {
            console.log("更新累积时长出现问题:" + error);
          })
      if (this.counter % 300 === 0) {
        // this.$refs.musicAudioControl[this.musicCur].pause()
        this.$refs.alert_box.style.display = "block";
        clearInterval(this.otimer)
      }
    }, 1000);
  },

  // 页面跳转前执行函数
  beforeUnmount() {
    this.beforeRouteLeave()
  },

}
</script>

<style>
.el-main {
  height: 0;
}
</style>
<style lang="scss" scoped>
* {
}

.music {
  height: 100%;
  width: 100%;
  overflow: hidden;

  .music-list {
    width: 100%;
    overflow: visible;
    height: 100%;
    padding: 0;
    position: relative;
    transition: all 0.5s;
    color: #fff;

    > li {
      list-style: none;
      width: 100%;
      height: 100%;
      position: relative;
      display: flex;
      align-items: stretch;

      .music-left {
        width: 30%;
        font-size: 50px;
        border-style: double;
        border-color: orange;
        border-radius: 50px;
        border-width: 15px;
        border-right: none;
        background-color: transparent;
      }

      .music-right {
        flex: 1;
        height: 100%;
        border-style: double;
        border-color: orange;
        border-radius: 50px;
        border-width: 15px;
        border-left: none;
        border-top: none;
        border-bottom: none;
        background-color: transparent;
      }
    }
  }
}

.MusicTitle {
  text-align: center;
  margin-top: 60%;
  margin-bottom: 10%;
  border-bottom-style: dashed;
  border-bottom-color: #5fa0fd;
  padding-bottom: 20px;
  border-bottom-width: 4px;
  border-top-style: dashed;
  border-top-color: #5fa0fd;
  padding-top: 20px;
  border-top-width: 4px;
  color: #1679fd;
  font-weight: bolder;
}

.musicPic {
  width: 50%;
  margin-top: 15%;
  margin-left: 25%;
  border-radius: 50%;
  -webkit-transform: rotate(360deg);
  animation: rotation 10s linear infinite;
  -moz-animation: rotation 10s linear infinite;
  -webkit-animation: rotation 10s linear infinite;
  -o-animation: rotation 10s linear infinite;
  box-shadow: 0 10px 60px rgba(53, 53, 53, 0.53);
}

@-webkit-keyframes rotation {
  from {
    -webkit-transform: rotate(0deg);
  }
  to {
    -webkit-transform: rotate(360deg);
  }
}

.musicAudio {
  float: bottom;
  margin-bottom: 0px;
  width: 80%;
  margin-left: 10%;
}

.float-right {
  transition: 1s;
  width: 15px;
  margin-right: 30px;
  margin-top: 10px;
}

.float-right:hover {
  width: 140px;
  transition: 1s;
}

.detailButton {
  transition: 1.5s;
  display: none;
}

.float-right:hover .detailButton {
  transition: 2s;
  display: block;
}

.likeButton {
  height: 30px;
  z-index: 999;
}


$white: #FCFCFC;
$gray: #CBCDD3;
$dark: #777777;
$error: pink;
$orange: #037ede;
$success: #B0DB7D;
$secondary: #99DBB4;

@import url('https://fonts.googleapis.com/css?family=Lato:400,700');

$font: 'Lato', sans-serif;

h1 {
  font-size: 0.9em;
  font-weight: 100;
  letter-spacing: 3px;
  padding-top: 5px;
  color: $white;
  padding-bottom: 5px;
  text-transform: uppercase;
}

.green {
  color: darken($secondary, 20%);
}

.red {
  color: darken($error, 10%);
}

.alert {
  font-weight: 700;
  letter-spacing: 5px;
}

p {
  margin-top: -5px;
  font-size: 0.5em;
  font-weight: 100;
  color: darken($dark, 10%);
  letter-spacing: 1px;
}

button, .dot {
  cursor: pointer;
}

#error-box {
  position: absolute;
  display: none;
  width: 35%;
  height: 50%;
  right: 25%;
  top: 25%;
  background: linear-gradient(to bottom left, $error 40%, $orange 100%);
  border-radius: 20px;
  box-shadow: 5px 5px 20px rgba($gray, 10%);
}

.dot {
  width: 8px;
  height: 8px;
  background: $white;
  border-radius: 50%;
  position: absolute;
  top: 4%;
  right: 6%;

  &:hover {
    background: darken($white, 20%);
  }
}

.two {
  right: 12%;
  opacity: .5;
}

.face {
  position: absolute;
  width: 22%;
  height: 22%;
  background: $white;
  border-radius: 50%;
  border: 1px solid $dark;
  top: 21%;
  left: 37.5%;
  z-index: 2;
  animation: bounce 1s ease-in infinite;
}

.face2 {
  position: absolute;
  width: 22%;
  height: 22%;
  background: $white;
  border-radius: 50%;
  border: 1px solid $dark;
  top: 21%;
  left: 37.5%;
  z-index: 2;
  animation: roll 3s ease-in-out infinite;
}

.eye {
  position: absolute;
  width: 5px;
  height: 5px;
  background: $dark;
  border-radius: 50%;
  top: 40%;
  left: 20%;
}

.right {
  left: 68%;
}

.mouth {
  position: absolute;
  top: 43%;
  left: 41%;
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.happy {
  border: 2px solid;
  border-color: transparent $dark $dark transparent;
  transform: rotate(45deg);
}

.sad {
  top: 49%;
  border: 2px solid;
  border-color: $dark transparent transparent $dark;
  transform: rotate(45deg);
}

.shadow {
  position: absolute;
  width: 21%;
  height: 3%;
  opacity: .5;
  background: $dark;
  left: 40%;
  top: 43%;
  border-radius: 50%;
  z-index: 1;
}

.scale {
  animation: scale 1s ease-in infinite;
}

.move {
  animation: move 3s ease-in-out infinite;
}


.message {
  position: absolute;
  width: 100%;
  text-align: center;
  height: 40%;
  top: 47%;
}

.button-box {
  position: absolute;
  background: $white;
  width: 50%;
  height: 15%;
  border-radius: 20px;
  top: 73%;
  left: 25%;
  outline: 0;
  border: none;
  box-shadow: 2px 2px 10px rgba($dark, .5);
  transition: all .5s ease-in-out;

  &:hover {
    background: darken($white, 5%);
    transform: scale(1.05);
    transition: all .3s ease-in-out;
  }
}

@keyframes bounce {
  50% {
    transform: translateY(-10px);
  }
}

@keyframes scale {
  50% {
    transform: scale(0.9);
  }
}

@keyframes roll {
  0% {
    transform: rotate(0deg);
    left: 25%;
  }
  50% {
    left: 60%;
    transform: rotate(168deg);
  }
  100% {
    transform: rotate(0deg);
    left: 25%;
  }
}

@keyframes move {
  0% {
    left: 25%;
  }
  50% {
    left: 60%;
  }
  100% {
    left: 25%;
  }
}
</style>