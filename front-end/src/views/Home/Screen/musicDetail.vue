<template>
  <div class="common-layout">
    <el-container>
      <!-- 歌曲播放控制部分 -->
      <el-aside class="leftBody">
        <img class="musicPic" :src="musicPic">
        <div style="display: inline-block; width: 70%">
          <h4 class="musicTitle">{{ musicName }}</h4>
          <div class="musicAuthor">
            <ul v-for="w in musicWriter" :key="w" style="display: inline-block">
              <li style="text-align: left; margin-left: 0px; list-style: none; display: inline-block"><h6>{{ w }}</h6>
              </li>
            </ul>
          </div>
        </div>
        <div class="likeButtonBox">
          <div class="likeButton" id="unlike" v-show="!isLike" @click="likeMusic"><i class="iconfont icon-aixin"
                                                                                     style="font-size: 20px; color: #ffffff"></i>
          </div>
          <div class="likeButton" id="like" v-show="isLike" @click="unlikeMusic"><i class="iconfont icon-aixin"
                                                                                    style="font-size: 20px; color: #ff0000"></i>
          </div>
        </div>
        <audio ref="player" :src="musicUrl"></audio>
        <!-- 播放与暂停按钮 -->
        <div class="playButton">
          <div id="pause" v-show="isPlaying" @click="pauseMusic"><i class="iconfont icon-24gf-pause2"
                                                                    style="font-size: 30px; color: #FFFFFF"></i></div>
          <div id="play" v-show="!isPlaying" @click="playMusic"><i class="iconfont icon-24gf-play"
                                                                   style="font-size: 30px; color: #FFFFFF"></i></div>
        </div>
        <!-- 播放进度条 -->
        <div class="musicPlay">
          <span class="currentTimeSpan">{{ currentTimeShow }}</span>
          <div id="playSlider">
            <el-slider
                v-model="currentTime"
                :max="durationTime"
                :show-tooltip="false"
                @change="changeMusicDuration"
                @mousedown="isChange=true"
                @mouseup="isChange=false"></el-slider>
          </div>
          <span class="durationTimeSpan">{{ durationTimeShow }}</span>
        </div>
      </el-aside>

      <!-- 歌词部分 -->
      <el-main class="rightBody">
        <div class="lrcSide">
          <lrc-show
              :songId="this.$route.query.musicId"
              :currentTime="currentTime"
              :durationTime="durationTime"
          ></lrc-show>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import LrcShow from "@/components/lrcShow";
import '@/assets/icon/iconfont.css';
import {format} from "@/utils/timeFormat";

export default {
  name: "musicDetail",
  components: {LrcShow},
  data() {
    return {
      musicId: '', // 歌曲id
      userID: '',
      musicName: '', // 歌曲名称
      musicWord: '', // 歌词
      musicWriter: [], // 作者
      musicPic: '', // 封面
      musicUrl: '', //歌曲链接
      currentTime: 0, // 当前播放时长
      currentTimeShow: 0, // 用于显示的时间格式
      durationTime: 0, // 音乐总时长
      durationTimeShow: 0, // 用于显示的时间格式
      isPlaying: false, // 判断当前是否在播放
      isChange: false, //判断是否被拖动
      isLike: false, // 用于检测用户是否喜欢此音乐
    }
  },

  created() {
  },

  mounted: function () {
    this.musicId = this.$route.query.musicId;
    this.userID = this.$route.query.userID;
    this.queryLike();
    this.getMusicUrl();
    this.getMusicDetail();
    this.addEventListeners();
    this.RecordHistory();
  },

  methods: {
    // 用于记录用户历史
    RecordHistory() {
      const path = "/api/recordHistory";
      const payload = {
        musicID: this.musicId,
        userID: this.userID,
      }
      this.$http.post(path, payload)
          .then((response) => {
            console.log("记录历史数据成功");
          })
          .catch((error) => {
            console.log("历史记录出现问题:" + error);
          })
    },

    // 用户点击喜欢音乐
    likeMusic() {
      this.isLike = true;
      const path = "/api/setMusicLike";
      const payload = {
        musicID: this.musicId,
        userID: this.userID,
      }
      this.$http.post(path, payload)
          .then((response) => {
            console.log("点击红心成功");
          })
          .catch((error) => {
            console.log("点击喜欢出现问题:" + error);
          })
    },

    // 用户取消喜欢音乐
    unlikeMusic() {
      this.isLike = false;
      const path = "/api/setMusicDislike";
      const payload = {
        musicID: this.musicId,
        userID: this.userID,
      }
      this.$http.post(path, payload)
          .then((response) => {
            console.log("取消红心成功");
          })
          .catch((error) => {
            console.log("点击不喜欢出现问题:" + error);
          })
    },

    // 查询用户是否已经like
    queryLike() {
      const path = "/api/queryMusicLike";
      const payload = {
        musicID: this.musicId,
        userID: this.userID,
      }
      this.$http.post(path, payload)
          .then((response) => {
            // console.log(response.data);
            if (response.data == "True") {
              this.isLike = true
            } else {
              this.isLike = false
            }
          })
          .catch((error) => {
            console.log("点击不喜欢出现问题:" + error);
          })
    },

    // 播放音乐
    playMusic() {
      this.isPlaying = true
      this.$refs.player.play()
    },
    // 暂停音乐
    pauseMusic() {
      this.isPlaying = false
      this.$refs.player.pause()
    },

    //鼠标拖拽松开时
    changeMusicDuration() {
      if (this.musicAllDuration === 0) return
      this.$refs.player.currentTime = this.currentTime
      this.isChange = false
    },

    addEventListeners() {
      this.$refs.player.addEventListener('timeupdate', this._currentTime);
      this.$refs.player.addEventListener('canplay', this._durationTime);
    },

    removeEventListeners: function () {
      this.$refs.player.removeEventListener('timeupdate', this._currentTime);
      this.$refs.player.removeEventListener('canplay', this._durationTime);
    },

    // 获取当前时间方法
    _currentTime() {
      this.currentTime = this.$refs.player.currentTime;
      this.currentTimeShow = format(this.$refs.player.currentTime);
    },

    // 获取audio整体时间方法
    _durationTime() {
      this.durationTime = this.$refs.player.duration;
      this.durationTimeShow = format(this.$refs.player.duration);
    },

    // 获取歌曲链接
    getMusicUrl: function () {
      const path = "/api/getMusicUrl"
      const payload = {
        // 获取歌曲地址（当前设置为个性化新歌）
        url: this.netEaseURL + "song/url?id=",
        // 加载歌曲数量
        id: this.musicId,
      };
      this.$http.post(path, payload)
          .then((response) => {
            const result = response.data;
            this.musicUrl = result;
          })
          .catch((error) => {
            console.log("歌曲url获取失败: " + error);
          })
    },

    // 获取歌曲详情
    getMusicDetail: function () {
      const path = "/api/getMusicDetail";
      const payload = {
        // 获取歌曲地址（当前设置为个性化新歌）
        url: this.netEaseURL + "song/detail?ids=",
        // 加载歌曲数量
        id: this.musicId,
      }
      this.$http.post(path, payload)
          .then((response) => {
            const result = response.data;
            this.musicName = result["musicName"];
            this.musicPic = result["musicPic"];
            this.musicWriter = result["writers"];
          })
          .catch((error) => {
            console.log("歌曲详情获取失败: " + error);
          })
    },
  },
}
</script>

<style scoped>
.musicPic {
  width: 50%;
  margin-top: 15%;
  margin-left: 25%;
  margin-bottom: 7%;
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

.musicTitle {
  color: #FFFFFF;
  font-weight: bolder;
  margin-left: 40px;
}

.musicAuthor {
  font-weight: normal;
  color: #FFFFFF;
}

.playButton {
  display: inline-block;
  width: 3%;
  float: left;
  margin-left: 5%;
  margin-top: 3.7%;
}

.musicPlay {
  display: inline-block;
  float: right;
  width: 89%;
  margin-top: 5%;
  margin-right: 3%;
}

.currentTimeSpan {
  font-weight: bold;
  font-size: 18px;
  text-align: center;
  color: #FFFFFF;
  width: 20%;
  display: inline-block;
}

.durationTimeSpan {
  font-weight: bold;
  font-size: 18px;
  color: #FFFFFF;
  float: right;
  text-align: center;
  width: 20%;
  display: inline-block;
}

.likeButtonBox {
  display: inline-block;
  width: 30%;
  float: right;
}

.likeButton {
  display: inline-block;
  float: right;
  margin-right: 40%;
  margin-top: 10%;
}

#playSlider {
  display: inline-block;
  width: 60%;
}

.leftBody {
  width: 50%;
  height: 85vh;
  background: linear-gradient(to right, rgba(34, 47, 196, 0.63), rgba(122, 66, 166, 0.8));
}

.rightBody {
  height: 85vh;
  background: linear-gradient(to right, rgba(122, 66, 166, 0.8), pink);
}

.lrcSide {
  height: 60%;
  margin-top: 20%;
}
</style>