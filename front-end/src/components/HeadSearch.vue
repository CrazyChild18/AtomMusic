<template>
  <span class="tagLeft">Is there a song you want to find?</span>

  <input
      v-model="search"
      class="input_box"
      @keyup.enter="search_input(), disShowBox()"
      @click="showBox()">
  <div class="select-panel" v-show="isShow">
    <div style="float: right">
      <button style="border: none" @click="disShowBox">X</button>
    </div>
    <div style="margin-left: 45%; display: inline-block">Hot List</div>
    <ul style="list-style: none; margin: 0; padding: 0">
      <li v-for="i in hotList" :key="i" class="select-panel-item" @click="searchHotList(i)">{{ i }}</li>
    </ul>
  </div>
  <span class="tagRight">Click the search box to search!</span>

  <div class="container" v-if="isResult">
    <div class="background-img">
      <div class="box">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <div class="content">
          <button @click="isResult=false" style="float: right; background: transparent">X</button>
          <h2>Search Result:</h2>
          <br>
          <ul class="resultList">
            <li class="resultListItemTitle">
              <div style="display: inline-block; width: 50%">Music Name</div>
              <div style="display: inline-block; width: 50%; text-align: right; padding-right: 5%">Artist</div>
            </li>
            <li v-for="i in resultListShow" :key="i" class="resultListItem" @click="turnDetailPage(i.id)">
              <div style="display: inline-block; width: 50%; ">{{ i.musicName }}</div>
              <div style="display: inline-block; width: 50%; text-align: right; padding-right: 5%">{{
                  i.musicArtist
                }}
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      search: '',
      isShow: false,
      isResult: false,
      hotList: ['Loading...Please wait'],
      resultListShow: [],
    }
  },
  methods: {
    // 搜索
    search_input() {
      const user_input = this.search;
      this.search = "";
      this.isShow = false
      this.searchResult(user_input);
    },
    showBox() {
      this.isShow = true
    },
    disShowBox() {
      this.isShow = false
    },
    // 获取搜索结果
    searchResult(keyWord) {
      const path = "/api/searchWord";
      const payload = {
        // 获取歌曲地址（当前设置为个性化新歌）
        url: "https://autumnfish.cn/cloudsearch?keywords=",
        // 加载歌曲数量
        keyword: keyWord,
      }
      axios.post(path, payload)
          .then((response) => {
            // console.log(response);
            this.resultListShow = response.data
            this.isResult = true
          })
          .catch((error) => {
            console.log("搜索出现问题:" + error);
          })
    },
    // 向后端请求热搜列表
    getSearchHotList() {
      const path = '/api/searchHostList'
      axios.post(path)
          .then((response) => {
            this.hotList = response.data
          })
          .catch((error) => {
            console.log("获取热搜列表出现问题:" + error);
          })
    },
    // 页面跳转函数
    turnDetailPage(musicId) {
      this.$router.push({
        path: '/musicDetail',
        query: {
          musicId: musicId
        }
      })
    },
    // 点击推荐内容
    searchHotList(words) {
      this.searchResult(words);
      this.isShow = false
    },
  },
  created() {
    this.getSearchHotList()
  }
}

</script>

<style scoped>
.tagLeft {
  position: absolute;
  z-index: -1;
  margin-left: 20%;
  margin-top: 2%;
  color: gray;
  font-style: italic;
}

.tagRight {
  position: absolute;
  right: 22%;
  z-index: -1;
  margin-top: 2%;
  color: gray;
  font-style: italic;
}

.input_box {
  margin-top: 20px;
  width: 5%;
  height: 40px;
  margin-left: 47.5%;
  transition: 1.5s;
  border-color: #5fa0fd;
  border-width: 3px;
  border-radius: 10px;
  border-style: solid;
  text-align: center;
}

.input_box:hover {
  margin-top: 20px;
  width: 60%;
  height: 40px;
  margin-left: 20%;
  placeholder: "Please Input Search Text";
  transition: 1.5s;
  border-color: #ee0053;
  border-width: 3px;
  border-radius: 10px;
  border-style: solid;
}

.input_box:focus {
  margin-top: 20px;
  width: 60%;
  height: 40px;
  margin-left: 20%;
  placeholder: "Please Input Search Text";
  transition: 1.5s;
  border-color: #ee0053;
  border-width: 3px;
  border-radius: 10px;
  border-style: solid;
}

.select-panel {
  width: 40%;
  height: 250px;
  margin-left: 21%;
  transition: 1s;
  position: absolute;
  margin-top: 10px;
  border-top: none;
  overflow: scroll;
  z-index: 999;
  box-shadow: 0px 5px 10px 0px rgba(31, 34, 84, 0.7);
  background-color: rgba(255, 255, 255, 0.8);
  animation: animate 1.5s ease-out;
  -ms-overflow-style: none; /* IE 10+ */
  scrollbar-width: none; /* Firefox */
}

::-webkit-scrollbar {
  display: none; /* Chrome Safari */
}

.select-panel-item {
  text-align: center;
  padding-left: 10%;
  padding-right: 10%;
  display: flex;
  margin: 7px auto;
  font-size: large;
  font-family: "Times New Roman";
  cursor: pointer;
}

.select-panel-item:hover {
  background-color: gray;
  text-align: center;

}

@keyframes animate {
  from {
    height: 0px;
  }
  to {
    height: 250px;
  }
}

.content h2 {
  font-size: 19px;
}

.box {
  position: absolute;
  z-index: 999;
  width: 35vw;
  height: 70vh;
  overflow: hidden;
  top: 50%;
  left: 58%;
  transform: translate(-50%, -50%);
  background: #111845a6;
  box-sizing: border-box;
  box-shadow: 0 20px 50px rgb(23, 32, 90);
  border: 2px solid #2a3cad;
  color: white;
  padding: 20px;
}

.box .content {
  position: absolute;
  top: 15px;
  left: 15px;
  right: 15px;
  bottom: 15px;
  border: 1px solid #f0a591;
  padding: 20px;
  text-align: center;
  box-shadow: 0 5px 10px rgba(9, 0, 0, 0.5);
}

.box span {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: block;
  box-sizing: border-box;

}

.box span:nth-child(1) {
  transform: rotate(0deg);
}

.box span:nth-child(3) {
  transform: rotate(180deg);
}

.box span:before {
  content: '';
  position: absolute;
  width: 100%;
  height: 2px;
  background: #50dfdb;
  animation: animate111 4s linear infinite;
}

@keyframes animate111 {
  0% {
    transform: scaleX(0);
    transform-origin: left;
  }
  50% {
    transform: scaleX(1);
    transform-origin: left;
  }
  50.1% {
    transform: scaleX(1);
    transform-origin: right;

  }

  100% {
    transform: scaleX(0);
    transform-origin: right;

  }
}

.resultList {
  list-style: none;
  text-align: left;
}

.resultListItem {
  margin-top: 12px;
}

resultListItemTitle {
  margin-top: 12px;
}

.resultListItem:hover {
  font-size: 18px;
  color: #50dfdb;
  cursor: pointer;
}
</style>