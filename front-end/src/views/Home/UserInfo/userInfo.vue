<template>
  <div class="card">
    <!--此部分为鼠标悬停前显示内容-->
    <div class="beforeShow" style="color: red">
      <img class="userAvatar" :src="userAvatarSrc"/>
      <h1 class="Username">{{ user.username }}</h1>
      <h4 class="hint">
        Welcome, my friend
        <br>
        <br>
        <br>
        <br>
        <br>
        Music-Hub
      </h4>
    </div>
     <div class="afterShow">
       <ul class="InfoList" style="list-style: none">
         <li class="InfoListItem">
           <span class="InfoTitle">Username:</span>
           <span class="InfoContent">{{ user.username }}</span>
         </li>
         <li class="InfoListItem">
           <span class="InfoTitle">Email Address:</span>
           <span class="InfoContent">{{ user.email }}</span>
         </li>
         <li class="InfoListItem">
           <span class="InfoTitle">Sex:</span>
           <span class="InfoContent">{{ user.sex }}</span>
         </li>
         <li class="InfoListItem">
           <span class="InfoTitle">Phone:</span>
           <span class="InfoContent">{{ user.phone }}</span>
         </li>
         <li class="InfoListItem">
           <span class="InfoTitle">Location:</span>
           <span class="InfoContent" style="font-size: 20px">{{ user.location }}</span>
         </li>
         <li class="InfoListItem">
           <span class="InfoTitle">Sign Time:</span>
           <span class="InfoContent">{{ $moment(user.create_time).format('LLL') }}</span>
         </li>
         <li class="InfoListItem">
           <span class="InfoTitle">About Me:</span>
           <span class="InfoContent" style="font-size: 20px">{{ user.about_me }}</span>
         </li>
       </ul>
       <el-button class="button_edit">
        <router-link v-bind:to="{name:'infoEdit', params:{id:sharedState.user_id }}">Edit Information</router-link>
       </el-button>
    </div>
</div>
</template>

<script>
import store from "@/store";

export default {
  name: "userInfo",
  data(){
    return{
      userAvatarSrc: '',
      sharedState: store.state,
      id: '',
      user: {
        username: '',
        email: '',
        name: '',
        location: '',
        phone: '',
        sex: '',
        about_me: '',
        create_time: '',
        _links: {
          self: '',
          avatar: ''
        }
      }
    }
  },
  methods: {
    // 获取用户头像
    setUserAvatar(){
      if(this.user._links.avatar == ''){
        this.userAvatarSrc = 'loginBackground.jpg'
      }else{
        const path = '/api/getUserAvatar'
        const payload = {
            picName: this.user._links.avatar,
          }
        this.$http.post(path, payload, {
          responseType: "arraybuffer", // 最为关键
        })
          .then((response) => {
            this.userAvatarSrc = "data:image/jpeg;base64," + this.arrayBufferToBase64(response.data);
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error)
          });
      }
    },

    // ArrayBuffer转为base64字符串
    arrayBufferToBase64(buffer) {
      //第一步，将ArrayBuffer转为二进制字符串
      var binary = "";
      var bytes = new Uint8Array(buffer);
      var len = bytes.byteLength;
      for (var i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
      }
      //将二进制字符串转为base64字符串
      return window.btoa(binary);
    },

    getUser(){
      const path = '/api/getUserDetail'
      const payload = {
          userId: this.id,
        }
      this.$http.post(path, payload)
        .then((response) => {
          console.log(response.data)
          this.user = response.data
          this.setUserAvatar()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
        });
    },
  },
  created () {
    this.id = this.$route.params.id
    this.getUser()
  },
}
</script>

<style scoped>
.button_edit{
  display: none;
}
.card:hover .button_edit{
  background-color: transparent;
  display: block;
  transition: 1s;
  position: absolute;
  top: -20%;
  right: -15%;
}
.card:hover .button_edit:active{
  transition: 0.5s;
  background-color: gray;
  border-color: gray;
  color: white;
}


.userAvatar{
  width: 4.5em;
  height: 4.5em;
  border-radius: 2.25em;
  display: flex;
  margin-top: 1.5em;
  margin-left: auto;
  margin-right: auto;
  transition: 1.5s;
}

.Username{
  font-weight: bold;
  color: cornflowerblue;
  margin-top: 10%;
}

@property --rotate {
  syntax: "<angle>";
  initial-value: 150deg;
  inherits: false;
}

.card {
  margin-top: 5%;
  transition: 1.5s;
  width: 30%;
  margin-left: 35%;
  height: 65vh;
  padding: 3px;
  position: relative;
  border-radius: 6px;
  justify-content: center;
  align-items: center;
  text-align: center;
  display: flex;
  font-size: 1.5em;
  color: rgb(88 199 250 / 0%);
  cursor: pointer;
  font-family: cursive;
}

.card:hover {
  margin-top: 0%;
  width: 90%;
  margin-left: 5%;
  height: 85vh;
  color: rgb(88 199 250 / 100%);
  transition: color 1.5s;
  transition: 1.5s;
  background: linear-gradient(to right, rgba(34, 47, 196, 0.63), rgba(122,66,166,0.8), pink);
}

.beforeShow{
  width: 100%;
  height: 100%;
}

.hint{
  font-weight: bold;
  font-style: italic;
  color: #373738;
  margin-top: 35%;
  font-size: medium;
}

.afterShow{
  position: absolute;
  top: 20%;
  right: 10%;
  width: 55%;
}
.card:hover .InfoList{
  transition: 2s;
  width: 100%;
}
.card:hover .InfoListItem{
  transition: 2s;
  width: 100%;
  float: left;
  margin-bottom: 30px;
  text-align: left;
  border-bottom-color: #FFFFFF;
  border-bottom-style: solid;
}
.card:hover .InfoTitle{
  float: left;
  transition: 2s;
  color: #FFFFFF;
  font-weight: bold;
  font-style: italic;
}
.card:hover .InfoContent{
  width: 50%;
  float: right;
  transition: 2s;
  color: #252ee3;
}

.card:hover .editButton{
  transition: 2s;
  width: 30%;
  float: right;
  font-weight: bold;
  color: #1679fd;
  font-size: large;
  border-color: #FFFFFF;
  border-style: dot-dash;
  border-radius: 7%;
  border-width: 3px;
  height: 7%;
  margin-right: -10%;
  background-color: transparent;
}



.card:hover .Username{
  display: none;
}
.card:hover .userAvatar{
  width: 10em;
  height: 10em;
  float: left;
  border-radius: 5em;
  margin-left: 2.5em;
  margin-top: 20%;
  transition: 1.5s;
}
.card:hover .hint{
  display: none;
}

.card:hover:before, .card:hover:after {
  animation: none;
  opacity: 0;
}


.card::before {
  content: "";
  width: 104%;
  height: 104%;
  border-radius: 18px;
  background-image: linear-gradient(
    var(--rotate)
    , rgba(34, 47, 196, 0.63), rgba(122,66,166,0.8), pink);
    position: absolute;
    z-index: -1;
    top: -2%;
    left: -2%;
    animation: spin 2.5s linear infinite;
}

.card::after {
  position: absolute;
  content: "";
  top: calc(65vh / 6);
  left: 0;
  right: 0;
  z-index: -1;
  height: 100%;
  width: 100%;
  margin: 0 auto;
  transform: scale(0.8);
  filter: blur(calc(65vh / 6));
  background-image: linear-gradient(
    var(--rotate)
    , rgba(34, 47, 196, 0.63), rgba(122,66,166,0.8), pink);
    opacity: 1;
  transition: opacity .5s;
  animation: spin 2.5s linear infinite;
}

@keyframes spin {
  0% {
    --rotate: 0deg;
  }
  100% {
    --rotate: 360deg;
  }
}
</style>