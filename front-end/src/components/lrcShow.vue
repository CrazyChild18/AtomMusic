<template>
<div class="lrcContainer">
  <div class="lrc" ref="lrc">
    {{getAllKey}}
    <p
      class="lrc-p"
      :class="{active:parseInt(currentTime) >= keyArr[index] && parseInt(currentTime) < keyArr[index+1]}"
      v-for="(item,key,index) in lrcData"
      :key="index">
      {{ item }} {{ scrollLrc(key,index) }}
    </p>
  </div>
</div>
</template>

<script>
import axios from "axios";

export default {
  name: "lrcShow",
  props: {
    songId:{},
    currentTime:{},
    durationTime:{},
  },

  data(){
    return{
      lrcData: {},
      keyArr: [],
    }
  },

  methods:{
    scrollLrc(key, index){
      const lrcDiv = this.$refs.lrc;
      if(key < this.currentTime && key > this.currentTime - (this.keyArr[index+1] - this.keyArr[index])){
        lrcDiv.style.top = -((index-3)*45) + "px";
      }
    }
  },

  mounted() {
    const path = "/api/getMusiclyric";
    const payload = {
        // 获取歌曲地址（当前设置为个性化新歌）
        url: "https://autumnfish.cn/lyric?id=",
        // 加载歌曲数量
        id: this.songId,
      }
      axios.post(path, payload)
        .then((response) => {
          // console.log(response);
          const lyc = response.data;
          const lyrics = lyc.split("\n");
          const lrcObj = {};
          for (let i=0; i<lyrics.length; i++) {
            const lyric = decodeURIComponent(lyrics[i]);
            const timeReg = /\[\d*:\d*((\.|:)\d*)*\]/g;
            const timeRegExpArr = lyric.match(timeReg);
            if (!timeRegExpArr) continue;
            const clause = lyric.replace(timeReg, '');
            for (let k = 0, h = timeRegExpArr.length; k < h; k++) {
              const t = timeRegExpArr[k];
              const min = Number(String(t.match(/\[\d*/i)).slice(1)),
                  sec = Number(String(t.match(/:\d*/i)).slice(1));
              const time = min * 60 + sec;
              lrcObj[time] = clause;
            }
          }
          this.lrcData = lrcObj;
        })
        .catch((error) => {
          console.log("歌词获取失败: " + error);
        })
  },

  computed:{
    // eslint-disable-next-line vue/return-in-computed-property
    getAllKey(){
      for(let i in this.lrcData){
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        this.keyArr.push(i)
      }
    }
  },

}
</script>

<style scoped>
.lrcContainer{
  width: 100%;
  height: 320px;
  margin-top: auto;
  margin-bottom: auto;
  overflow: hidden;
  position: relative;
}
.lrc{
  width: 100%;
  position: absolute;
  top: 0;
  font-size: 20px;
  color: rgba(111, 89, 117, 0.8);
  text-align: center;
}
.active{
  color: white !important;
  font-size: 25px;
  font-weight: bold;
  background-color: rgba(152, 158, 164, 0.17);
}
.lrc-p{
  height: 45px;
  line-height: 45px;
}
p{
  margin-bottom: 0px;
}
</style>