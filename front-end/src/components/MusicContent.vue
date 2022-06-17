<template>

  <!--采用左右布局，左边为歌词，右边为图片或mv-->
  <div class="common-layout">
    <el-container>
      <el-aside width="300px" style="overflow: hidden">
        <!--歌曲名-->
        <h3 style="margin-top: 20%; margin-bottom: 10%">{{ musicName }}</h3>
        <!--歌词-->
        <div style="height: 70%; overflow: scroll;" class="wordListPart">
          <el-row type="flex" justify="center" class="lyric-contain">
            <el-col :span="23" class="song-lyric" :style="lyricMove">
              <!-- 这里用内联样式来实现当前歌词的高亮显示 -->
              <el-row
                  v-for="(item,index) in musicWordList"
                  :key="index"
                  :style="{'font-size': (index===currentRow ? '1.3rem':'.9rem')}"
                  class="lyric-row">
                {{ item.text }}
              </el-row>
            </el-col>
          </el-row>
        </div>
      </el-aside>
      <el-main>
        <audio
            :src="musicUrl"
            type="audio/mpeg"
            controls
            autoplay
            loop></audio>
      </el-main>
    </el-container>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "MusicContent",
  data() {
    return {
      musicName: "",//歌曲名称
      musicWordList: [],// 歌词
      musicList: [],// 歌曲数组，存放歌曲id
      musicUrl: "",// 歌曲地址
      musicCover: "",// 歌曲封面
      isPlaying: false,// 动画播放状态
      mvUrl: "",// mv地址
      playStatus: false, //播放状态，用来控制播放、暂停按钮的显示
      Timer: "", //定时器，我们需要实时监听到歌曲的播放进度
      currentBar: 0, //进度条长度，默认为0，根据歌曲进度同步更新
      currentText: "00:00", //进度条旁边的播放时间，同样要实时更新
      durationText: "00:00", //当前歌曲的播放时长
      currentRow: 0,
      listShow: false,  //控制播放列表的显示
    }
  },
  methods: {
    // 歌曲列表
    getMusicList: function () {
      const that = this;
      const type = 0; // 获取歌类型
      axios.get(this.netEaseURL + "top/song?type=" + type)
          .then(
              function (res) {
                // console.log(res);
                for (let i = 0; i < 10; i++) {
                  that.musicList[i] = res.data.data[i].id;
                }
                that.playMusic(that.musicList[0]);
              }, function (err) {
              });
    },

    // 歌曲播放
    playMusic: function (musicId) {
      const that = this;
      // 获取歌曲地址
      axios.get(this.netEaseURL + "song/url?id=" + musicId)
          .then(
              function (res) {
                // console.log(res);
                that.musicUrl = res.data.data[0].url;
                // console.log(that.musicUrl);
              }, function (err) {
              });
      //歌词获取
      axios.get(this.netEaseURL + "song/detail?ids=" + musicId)
          .then(
              function (res) {
                // console.log(res);
                that.musicName = res.data.songs[0].name;
                // console.log(that.musicName);
              }, function (err) {
              });
      // 获取歌词
      axios.get(this.netEaseURL + "lyric?id=" + musicId)
          .then(
              function (res) {
                // console.log(res);
                const musicWord = res.data.lrc.lyric;
                let arr = musicWord.split("\n"); //原歌词文本已经换好行了方便很多，我们直接通过换行符“\n”进行切割
                let row = arr.length; //获取歌词行数
                for (let i = 0; i < row; i++) {
                  let temp_row = arr[i]; //现在每一行格式大概就是这样"[00:04.302][02:10.00]hello world";
                  let temp_arr = temp_row.split("]");//我们可以通过“]”对时间和文本进行分离
                  //歌词文本
                  let text = temp_arr.pop();
                  //歌词时间
                  temp_arr.forEach(element => {
                    let obj = {};
                    let time_arr = element.substr(1, element.length - 1).split(":");//先把多余的“[”去掉，再分离出分、秒
                    let s = parseInt(time_arr[0]) * 60 + Math.ceil(time_arr[1]); //把时间转换成与currentTime相同的类型，方便待会实现滚动效果
                    obj.time = s;
                    obj.text = text;
                    that.musicWordList.push(obj); //每一行歌词对象存到musicWordList里
                  });
                }
                that.musicWordList.sort(that.sortRule); //以时间顺序重新排列一下
              }, function (err) {
              });
    },

    //设置一下排序规则
    sortRule(a, b) {
      return a.time - b.time;
    },

    // 歌曲播放
    play: function () {
      console.log("playing");
      // this.isPlaying = true;
    },

    //歌曲暂停
    pause: function () {
      console.log("pause");
      // this.isPlaying = false;
    },

    // // 播放MV
    // playMV:function (mvid){
    //   const that = this;
    //   // 获取MV地址
    //   axios.get("http://localhost:3000/mlog/music/rcmd")
    //       .then(function (res){
    //         // console.log(res.data.data.url);
    //         // 显示遮罩层
    //         that.isShow = true;
    //         that.mvUrl = res.data.data.url;
    //       }, function (err) {});
    // }
  },
  created() {
    this.getMusicList();
  },
}
</script>

<style scoped>
.lyric-row {
  height: 30px;
}

.wordListPart::-webkit-scrollbar {
  width: 0 !important
}
</style>