<template>
<div class="slide" id="slide5" data-slide="5" data-stellar-background-ratio="0.5">
	<div class="container clearfix">
    <div style="width: auto; margin-left: 25%;">
      <div class="content grid_2 contactype" id="contact-carClick" :class="{ activite: isBasicActivite }" @click="basicClick()">
			<i class="icon-car"></i>
			<p>Basic Information</p>
		</div>
      <div class="content grid_2 contactype" id="contact-busClick" :class="{ activite: isPasswordActivite }" @click="passwordClick()">
        <i class="icon-bus"></i>
        <p>Change Password</p>
      </div>
      <div class="content grid_2 contactype" id="contact-phoneClick" :class="{ activite: isLocationActivite }" @click="locationClick()">
        <div class="icon-phone"></div>
        <p>Location</p>
      </div>
      <div class="content grid_2 contactype omega" id="contact-mailClick" :class="{ activite: isAboutMeActivite }" @click="aboutmeClick()">
			<div class="icon-mail"></div>
			<p>About Me</p>
		</div>
    </div>

		<div class="content grid_12 contactmap dn" id="contact-car" v-if="isBasicCard">
			<div class="grid_4">
				<h1 style="margin-top: 20%">Basic Information</h1>
        <p style="margin-top: 15%">This is your basic information in the system.</p>
        <button class="btn" @click="changeBasicInfor()">Submit</button>
			</div>
			<div class="grid_8 omega">
        <el-descriptions
          class="margin-top"
          :column="1"
          border
          style="margin-top: 5px"
        >
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon :style="iconStyle">
                  <user />
                </el-icon>
                Username
              </div>
            </template>
            <input type="text" class="InfoContent" v-model="user.username" ref="username_input">
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon :style="iconStyle">
                  <iphone />
                </el-icon>
                Telephone
              </div>
            </template>
            <input class="InfoContent" v-model="user.phone" ref="phone_input" >
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon :style="iconStyle">
                  <Male />
                </el-icon>
                Sex
              </div>
            </template>
            <el-radio-group v-model="user.sex" size="large" style="margin-left: 30%; margin-top: 20px; margin-bottom: 20px">
              <el-radio-button label="Male"/>
              <el-radio-button label="Female"/>
            </el-radio-group>
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon :style="iconStyle">
                  <location />
                </el-icon>
                Email Address
              </div>
            </template>
            <input type="email" class="InfoContent" v-model="user.email" ref="email_input">
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon :style="iconStyle">
                  <location />
                </el-icon>
                Avater
              </div>
            </template>
            <el-upload
                ref="upload"
                action=""
                accept=".jpg,.png"
                list-type="picture-card"
                :auto-upload="false"
                :http-request="uploadHttp"
                :limit="1">
              <el-icon><Plus /></el-icon>
              <template #file="{ file }">
                <div>
                  <img ref="showPic" class="el-upload-list__item-thumbnail" :src="file.url" alt="" />
                  <span class="el-upload-list__item-actions">
                    <span
                      class="el-upload-list__item-delete"
                      @click="handleRemove(file)"
                    >
                      <el-icon><Delete /></el-icon>
                    </span>
                  </span>
                </div>
              </template>
            </el-upload>
          </el-descriptions-item>
        </el-descriptions>
			</div>
		</div>
		<div class="content grid_12 contactmap dn" id="contact-bus" v-if="isPasswordCard">
			<div class="grid_4">
				<h1 style="margin-top: 20%">Change Your Password Here</h1>
				<p style="margin-top: 15%">We will not store your password directly, so your password will not be disclosed from our server. Please make sure you confirm the old password and the correct new password and click the submit button</p>
				<button class="btn" @click="changePassword()">Submit</button>
			</div>
			<div class="grid_8 omega">
        <el-descriptions
          class="margin-top"
          :column="1"
          border
          style="margin-top: 20px"
        >
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon :style="iconStyle">
                  <lock />
                </el-icon>
                Current Password
              </div>
            </template>
            <el-input
              v-model="currentPassword"
              type="password"
              placeholder="Please input current password"
              show-password
            />
            <div class="warrning" ref="currentPassword_warning">Current password incorrect</div>
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon :style="iconStyle">
                  <iphone />
                </el-icon>
                New Password
              </div>
            </template>
            <el-input
              v-model="newPassword"
              type="password"
              placeholder="Please input new password"
              show-password
            />
            <div class="warrning" ref="newPassword_warning">The two passwords are inconsistent</div>
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">
                <el-icon :style="iconStyle">
                  <Male />
                </el-icon>
                New Password Again
              </div>
            </template>
            <el-input
              v-model="newPassword2"
              type="password"
              placeholder="Please input current password again"
              show-password
            />
            <div class="warrning" ref="newPassword2_warning">The two passwords are inconsistent</div>
          </el-descriptions-item>
        </el-descriptions>
			</div>
		</div>
		<div class="content grid_12 contactmap dn" id="contact-bike" v-if="isLocationCard">
			<div class="grid_4">
				<h1 style="margin-top: 20%">Your Location Information</h1>
				<p style="margin-top: 15%">Your location information will help us match users related to you and provide more accurate song recommendations</p>
        <button class="btn" @click="changeLocation()">Submit</button>
      </div>
			<div class="grid_8 omega">
        <div style="height: 30%;">
          <span class="InfoTitle" style="padding-left: 5%">Current Location:</span>
          <span class="InfoContent">{{ user.location }}</span>
        </div>
        <div>
          <div class="InfoTitle" style="margin-bottom: 10%; padding-left: 5%">Do you change your location? Quickly update:</div>
          <el-cascader
          size="large"
          :options="options"
          v-model="newLocation"
          style="display: flex; margin-left: auto; margin-right: auto; width: 70%"
          @change="handleChange">
        </el-cascader>
        </div>
			</div>
		</div>
		<div class="content grid_12 contactmap dn" id="contact-phone" v-if="isAboutMeCard">
			<div class="grid_4">
				<h1 style="margin-top: 20%">Personal Description</h1>
				<p style="margin-top: 15%">Here, make a brief and personalized self introduction to yourself. also
You can choose to fill in some meaningful sentences</p>
        <button class="btn" @click="changeAboutMe()">Submit</button>
			</div>
			<div class="grid_8 omega">
				<div style="height: 35%;">
          <span class="InfoTitle" style="padding-left: 5%">About Me:</span>
          <span class="InfoContent">{{ user.about_me }}</span>
        </div>
        <div style="margin-left: 5%; margin-right: 5%;">
          <div class="InfoTitle" style="margin-bottom: 5%">You can change here:</div>
          <el-input
            v-model="user.about_me"
            :autosize="{ minRows: 4, maxRows: 10 }"
            type="textarea"
            placeholder="Please input"
          />
        </div>
			</div>
		</div>
	</div>
</div>
</template>

<script>
import store from "@/store";
import {ElNotification} from "element-plus";
import {
  Iphone,
  Location,
  Male,
  User,
  Lock,
  Delete,
  Plus,
} from '@element-plus/icons-vue'

import {regionData,CodeToText} from 'element-china-area-data'

export default {
  name: "/api/userInfo",
  components:{
    Iphone,
    Location,
    Male,
    User,
    Lock,
    Delete,
    Plus,
  },
  data(){
    return{
      imageUrl: '',  //用于上传头像
      options: regionData,
      addtions:{},		//存储地址数据
      newLocation: [],

      isBasicActivite: true,
      isPasswordActivite: false,
      isLocationActivite: false,
      isAboutMeActivite: false,
      isBasicCard: true,
      isPasswordCard: false,
      isLocationCard: false,
      isAboutMeCard: false,

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
        creat_time: '',
        _links: {
          self: '',
          avatar: ''
        }
      },
      currentPassword: '',
      newPassword: '',
      newPassword2: '',
    }
  },
  methods: {
    uploadHttp(){
      const formData = new FormData()
      formData.append('file', this.$refs.upload.uploadFiles[0].raw)
      formData.append('id', this.id)
      console.log(this.$refs.upload.uploadFiles[0].raw)
      const avatarPath = '/api/changeAvatar'
      this.$http.post(avatarPath, formData, {
        headers: {'Content-Type': 'multipart/form-data'}
      })
          .then(data => {
            console.log(data)
          }).catch(response => {
            console.log(response)
          })
    },

    // 删除头像
		handleRemove() {
      this.$refs.upload.clearFiles();//调用element官方的方法
		},

    // 更改about me
    changeAboutMe(){
      const path = '/api/changeAboutMe'
      const payload = {
        content: this.user.about_me,
        id: this.id,
      }
      this.$http.post(path, payload)
        .then((response) => {
          this.open1("Succeeded in modifying About me")
        })
        .catch((error) => {
          alert("Change about me fail! Error: " + error)
        });
    },

    // 选择地址
    handleChange (value) {
      //我们选择地址后，newLocation 会保存对应的区域码，例如北京的区域码为'110000'
      //我们要取出区域码对应的汉字，就需要用CodeToText(区域码)进行输出
      this.addtions.newLocation = value
      this.locationCode = this.newLocation
      var name = ''
      this.newLocation.map(item => name += CodeToText[item] + '/')
      this.addtions.names = name
    },

    // 修改地址
    changeLocation(){
      const path = '/api/changeLocation'
      const payload = {
        currentLocationName: this.addtions.names,
        id: this.id,
      }
      this.$http.post(path, payload)
        .then((response) => {
          this.user.location = this.addtions.names
          this.open1("Succeeded in changing the address")
        })
        .catch((error) => {
          alert("Change location fail! Error: " + error)
        });
    },

    // 修改成功通知
    open1(message){
      ElNotification({
        title: 'Success',
        message: message,
        type: 'success',
      })
    },

    // 警告通知
    open2(message) {
      ElNotification({
        title: 'Warning',
        message: message,
        type: 'warning',
      })
    },

    // 修改失败通知
    open4(message){
      ElNotification({
        title: 'Error',
        message: message,
        type: 'error',
      })
    },

    // 修改密码
    changePassword(){
      this.$refs.newPassword_warning.style.display = 'none'
      this.$refs.newPassword2_warning.style.display = 'none'
      this.$refs.currentPassword_warning.style.display = 'none'
      if(this.newPassword == this.newPassword2){
        const path = '/api/changePassword'
        const payload = {
          currentPassword: this.currentPassword,
          newPassword: this.newPassword,
          id: this.id,
        }
        this.$http.post(path, payload)
          .then((response) => {
            if(response.data == "successful"){
              this.open1('Change Password Successful')
            }else if (response.data == "passwordError"){
              this.$refs.currentPassword_warning.style.display = 'block'
              this.open2("Current password incorrect")
            }
          })
          .catch((error) => {
            alert("Change fail! Error: " + error)
          });
      }else{
        this.$refs.newPassword_warning.style.display = 'block'
        this.$refs.newPassword2_warning.style.display = 'block'
        this.open2("The two passwords are different. Please check them and try again")
      }
    },

    // 基础信息修改按钮
    changeBasicInfor(){
      this.$refs.upload.submit()
      const path = '/api/changeUserBasicInfo'
      const payload = {
        id: this.id,
        username: this.user.username,
        email: this.user.email,
        gender: this.user.sex,
        phone: this.user.phone,
      }
      // 用户信息
      this.$http.post(path, payload)
      .then((response) => {
        if(response.data == "successful"){
          this.open1('Change Basic Information Successful')

        }
      })
      .catch((error) => {
        alert("Change fail! Error: " + error)
      });
    },

    // 获取用户信息函数
    getUser(){
      const path = `/api/getUserDetail`
      const payload = {
          userId: this.id,
        }
      this.$http.post(path, payload)
        .then((response) => {
          // console.log(response.data)
          this.user = response.data
          if(this.user.sex == "Male"){
            this.gender = "male";
          }else if(this.user.sex == "Female"){
            this.gender = "female";
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
        });
    },

    //各种切换函数
    basicClick(){
      this.isBasicActivite = true;
      this.isPasswordActivite = false;
      this.isLocationActivite = false;
      this.isAboutMeActivite = false;

      this.isBasicCard = true;
      this.isPasswordCard = false;
      this.isLocationCard = false;
      this.isAboutMeCard = false;
    },
    passwordClick(){
      this.isBasicActivite = false;
      this.isPasswordActivite = true;
      this.isLocationActivite = false;
      this.isAboutMeActivite = false;

      this.isBasicCard = false;
      this.isPasswordCard = true;
      this.isLocationCard = false;
      this.isAboutMeCard = false;
    },
    locationClick(){
      this.isBasicActivite = false;
      this.isPasswordActivite = false;
      this.isLocationActivite = true;
      this.isAboutMeActivite = false;

      this.isBasicCard = false;
      this.isPasswordCard = false;
      this.isLocationCard = true;
      this.isAboutMeCard = false;
    },
    aboutmeClick(){
      this.isBasicActivite = false;
      this.isPasswordActivite = false;
      this.isLocationActivite = false;
      this.isAboutMeActivite = true;

      this.isBasicCard = false;
      this.isPasswordCard = false;
      this.isLocationCard = false;
      this.isAboutMeCard = true;
    },
  },

  created () {
    this.id = this.$route.params.id
    this.getUser()
  },
}
</script>

<style lang="scss" scoped>
.dn {
	display: none;
}
a:link {
	color: #61bb46;
	text-decoration: none;
}
a:hover {
	color: #61bb46;
	text-decoration: none;
}
a:visited {
	color: #61bb46;
	text-decoration: none;
}

/* Computer */
.grid_1 { width: 6.5%; }
.grid_2 { width: 15%; }
.grid_3 { width: 23.5%; }
.grid_4 { width: 32%; }
.grid_5 { width: 40.5%; }
.grid_6 { width: 49%; }
.grid_7 { width: 57.5%; }
.grid_8 { width: 66%; }
.grid_9 { width: 74.5%; }
.grid_10 { width: 83%; }
.grid_11 { width: 91.5%; }
.grid_12 { width: 100%; }

.grid_1,
.grid_2,
.grid_3,
.grid_4,
.grid_5,
.grid_6,
.grid_7,
.grid_8,
.grid_9,
.grid_10,
.grid_11,
.grid_12 {
	margin: 0 2% 1% 0;
	float: left;
	display: block;
}

.omega{
  margin-right:0;
}

.warrning{
  display: none;
  color: red;
  font-weight: bold;
  padding-left: 2%;
}

.container{
	width: 90%; /*width: 1000px;*/
	max-width: 1000px;
	margin: auto;

}

/* Mobile */
@media screen and (max-width : 480px) {
  .grid_2,
  .grid_4,
  .grid_6,
  .grid_8,
  .grid_12 {
    width:100%;
  }
}

/* Slide 5 */
#slide5 {
  border-top-width: 8px;
  border-top-color: #f48022;
  border-top-style: solid;
  padding-top: 2px;
}
.contactmap {
	background: #f48022;
	border-radius: 4px;
}
#slide5 h1 {
	margin: 13px 0 0 30px;
	color: #fff;
	font-size: 2em;
}
#slide5 p {
	line-height: 150%;
	color: #fff;
	padding: 5px 0 0 30px;
}
.contactype {
	position: relative;
	cursor: pointer;
	color: #fff;
	text-shadow: 0 1px 1px rgba(0,0,0,0.1);
	text-align: center;
	background-color: #c3c3c3;
	border-radius: 5px;
	height: 100px;
	float: left;
	transition: all .3s ease-in;
}
.contactype p {
	width: 100%;
	text-align: center;
	position: absolute;
	bottom: -7.5px;
	left: 0;
	padding: 0 !important;
}
.contactype:hover {
	background-color: #f48022;
}
.activite{
  background-color: #f48022;
}
.contactype div {
	font-size: 4em;
	position: absolute;
	width: 100%;
	left: 0;
	top: 0;
	transition: all .2s ease-in;
}
.contactmap .grid_8.omega .grid_6 {
	margin: 40px 0 0 220px;
}
.contactmap .grid_8.omega .grid_6 .btn {
	margin-top: 10px;
	border: 1px solid rgba(0,0,0,.1);
	margin-left: 0;
}
.contactmap .information span {
	font-weight: bold;
}
#contact-bus .grid_6.omega, #contact-car .grid_6.omega {
	height: 100%;
	overflow-x: hidden;
	position: relative;
}
#contact-phone .grid_6.omega {
	font-size: 2.5em;
	margin-top: 100px;
}
#contact-mail .grid_6.omega {
	padding-top: 40px;
}
.btn {
  margin-top: 30px;
	display: inline-block;
	padding-left: 56px;
	color: #626263;
	background-color: #fff;
	padding: 16px 24px 17px 24px;
	font-size: 13px;
	font-weight: bold;
	text-transform: uppercase;
	letter-spacing: 0.2em;
	text-shadow: none;
	line-height: 20px;
	text-align: center;
	border-radius: 5px;
	margin-left: 2.5em;
  box-shadow: 0 2px 25px rgba(233, 30, 99, 0.5);
  background-color: rgba(255,255,255,0.5);
  transition: all 0.5s;
  &:active{
    background-color: rgba(255,255,255,0.1);
    transition: all 0.5s;
  }
}
.btn span {
	font-size: 1em;
}


.contactmap {
	height: 550px;
  margin-top: 20px;
}
.contactmap .grid_8.omega {
	background-color: #fff;
	height: 100%;
	display: block;
	overflow: hidden;
  padding-top: 5%;
}
#contact-car .grid_10.omega {
	margin: 0 auto;
	display: block;
}


.submit {
	display: none;
	margin: 0 auto;
	width: auto;
	font-size: 16px;
	font-weight: 400;
	color: #fff;
	padding: 15px 21px;
	border: 1px solid rgba(255,255,255,0.4);
	background: transparent;
	border-radius: 9px;
	text-decoration: none;
	white-space: nowrap;
	transition: border-color .4s;
}
.submit:hover {
	color: #fff;
	border-color: #fff;
}
.basic_item_box{
  margin-left: 15%;
  margin-top: 10%;
  width: 80%;
  padding-left: 10px;
  padding-bottom: 10px;
  border-left-width: 10px;
  border-left-style: double;
  border-left-color: #1679fd;
  font-size: large;
}
.InfoTitle{
  font-weight: bolder;
  color: #1679fd;
}
.InfoContent{
  width: 100%;
  float: left;
  height: 50px;
  border: none;
  border-bottom-width: 1px;
  border-bottom-color: #1679fd;
  border-bottom-style: solid;
  text-align: center;
  font-weight: bold;
  font-size: large;
  transition: 1.5s;
}
.InfoContent:focus{
  outline: none;
  border-bottom-width: 1.5px;
  border-bottom-color: red;
  transition: 2s;
}
.item{
  height: 400px
}

</style>