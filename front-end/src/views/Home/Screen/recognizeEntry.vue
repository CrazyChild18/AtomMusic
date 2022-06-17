<template>
  <div
    v-if="loading"
    v-loading="loading"
    element-loading-text="Recognizing......"
    element-loading-background="rgba(0, 0, 0, 0.7)"
    style="width: 80vw; height: 85vh; position: absolute; font-weight: bold;"
  >
  </div>
  <div
    v-if="uploading"
    v-loading="uploading"
    element-loading-text="Uploading... Please wait..."
    element-loading-background="rgba(0, 0, 0, 0.7)"
    style="width: 80vw; height: 85vh; position: absolute; font-weight: bold;"
  >
  </div>

  <el-tabs v-model="activeName" class="demo-tabs">
    <el-tab-pane label="Music File Upload" name="first">
      <el-steps :active="active" finish-status="success" simple style="margin-top: 20px">
        <el-step title="Upload Music" />
        <el-step title="Check before Recognize" />
        <el-step title="Music Result" />
      </el-steps>

      <div v-show="active == 0">
        <el-upload
          class="upload-demo"
          drag
          action=""
          ref="upload"
          accept=".mp3"
          limit="1"
          auto-upload="false"
          :http-request="uploadHttp"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            Drop file here or <em>click to upload</em>
          </div>
          <template #tip>
            <div class="el-upload__tip" style="margin-bottom: 15px">
              mp3 files with a size less than 20M
            </div>
          </template>
        </el-upload>
      </div>
      <div v-show="active == 1">
        <div class="info" v-if="updateFinish == true" style="height: 70%">
          <div><h1>Upload Successful!</h1></div>
          <div style="color: black">
            <h4>
              The system has received your uploaded song.
              <br>
              Next you will choose whether to identify or go back to the previous step to re-upload
            </h4>
          </div>
          <br>
          <div style="width: 40%; display: inline-block">
            <h3>Upload Detail</h3>
            <h5>Song upload accepted: {{ fileName }}</h5>
          </div>
          <div style="width: 40%; display: inline-block;">
            <el-button type="success" plain class="recognize" @click="recognize()">Start Recognize</el-button>
            <el-button type="danger" plain class="recognize" @click="turnToUpload()">Back To Upload</el-button>
          </div>
        </div>
      </div>
      <div v-show="active == 2">
        <div class="info2" v-if="recognizeFinish == true">
          <div style="background: linear-gradient(to right, rgba(34, 47, 196, 0.63), rgba(122,66,166,0.8), pink); width: 100%; height: 100%">
            <svg style="padding-top: 8%" width="40%" height="80%" viewBox="0 0 837 1045" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns">
              <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">
                  <path d="M353,9 L626.664028,170 L626.664028,487 L353,642 L79.3359724,487 L79.3359724,170 L353,9 Z" id="Polygon-1" stroke="#007FB2" stroke-width="6" sketch:type="MSShapeGroup"></path>
                  <path d="M78.5,529 L147,569.186414 L147,648.311216 L78.5,687 L10,648.311216 L10,569.186414 L78.5,529 Z" id="Polygon-2" stroke="#EF4A5B" stroke-width="6" sketch:type="MSShapeGroup"></path>
                  <path d="M773,186 L827,217.538705 L827,279.636651 L773,310 L719,279.636651 L719,217.538705 L773,186 Z" id="Polygon-3" stroke="#795D9C" stroke-width="6" sketch:type="MSShapeGroup"></path>
                  <path d="M639,529 L773,607.846761 L773,763.091627 L639,839 L505,763.091627 L505,607.846761 L639,529 Z" id="Polygon-4" stroke="#F2773F" stroke-width="6" sketch:type="MSShapeGroup"></path>
                  <path d="M281,801 L383,861.025276 L383,979.21169 L281,1037 L179,979.21169 L179,861.025276 L281,801 Z" id="Polygon-5" stroke="#36B455" stroke-width="6" sketch:type="MSShapeGroup"></path>
              </g>
            </svg>
            <div class="message-box">
              <h1>Recognizing Result:</h1>
              <h1 style="color:#002afa;">{{result}}</h1>
              <p style="font-size: 1.1em">Due to the limitations of our database, it is possible that your song has not been identified, or has been identified incorrectly. We have recorded your uploaded song and reported it to the administrator. Thanks for helping us expand our library.</p>
              <div class="buttons-con">
                <div class="action-link-wrap">
                  <el-button type="success" @click="restartUpload()">Restart Process</el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-tab-pane>

    <el-tab-pane label="Audio File Record" name="second">
      <el-steps :active="activeType2" finish-status="success" simple style="margin-top: 20px">
        <el-step title="Record Music" />
        <el-step title="Check before Recognize" />
        <el-step title="Music Result" />
      </el-steps>

      <div v-show="activeType2 == 0">
          <div style="padding:  15vh 20px 20px 20vw;">
            <div style="font-size:14px">
              <h3 style="color: cornflowerblue">Recording Duration：{{ recorder && recorder.duration.toFixed(4) }}</h3>
              <br />
              <el-button type="primary" @click="handleStart">Start Record</el-button>
              <el-button type="info" @click="handlePause">Pause Record</el-button>
              <el-button type="success" @click="handleResume">Continue</el-button>
              <el-button type="warning" @click="handleStop">Stop Record</el-button>
              <br />
              <br />
              <h3 style="color: cornflowerblue">
                Play Duration: {{
                  recorder &&
                    (playTime > recorder.duration
                      ? recorder.duration.toFixed(4)
                      : playTime.toFixed(4))
                }}
              </h3>
              <br />
              <el-button type="primary" @click="handlePlay">Play</el-button>
              <el-button type="info" @click="handlePausePlay">Pause</el-button>
              <el-button type="success" @click="handleResumePlay">Continue</el-button>
              <el-button type="warning" @click="handleStopPlay">Stop</el-button>
              <el-button type="error" @click="handleDestroy">Destroy</el-button>
              <el-button type="primary" @click="uploadRecord">Update</el-button>
            </div>
          </div>
      </div>
      <div v-show="activeType2 == 1">
        <div class="info" v-if="reacordUpdateFinish == true">
          <div><h1>Upload Successful!</h1></div>
          <div style="color: black">
            <h4>
              The system has received your uploaded song.
              <br>
              Next you will choose whether to identify or go back to the previous step to re-upload
            </h4>
          </div>
          <br>
          <div style="width: 40%; display: inline-block">
            <h3>Upload Detail</h3>
            <h5>Song upload accepted: {{ fileName }}</h5>
          </div>
          <div style="width: 40%; display: inline-block;">
            <el-button type="success" plain class="recognize" @click="recognizeRecord()">Start Recognize</el-button>
            <el-button type="danger" plain class="recognize" @click="turnToUpload()">Back To Upload</el-button>
          </div>
        </div>
      </div>
      <div v-show="activeType2 == 2">
        <div class="info2" v-if="recognizeFinish == true">
          <div style="background: linear-gradient(to right, rgba(34, 47, 196, 0.63), rgba(122,66,166,0.8), pink); width: 100%; height: 100%">
            <svg style="padding-top: 8%" width="40%" height="80%" viewBox="0 0 837 1045" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns">
              <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">
                  <path d="M353,9 L626.664028,170 L626.664028,487 L353,642 L79.3359724,487 L79.3359724,170 L353,9 Z" id="Polygon-1" stroke="#007FB2" stroke-width="6" sketch:type="MSShapeGroup"></path>
                  <path d="M78.5,529 L147,569.186414 L147,648.311216 L78.5,687 L10,648.311216 L10,569.186414 L78.5,529 Z" id="Polygon-2" stroke="#EF4A5B" stroke-width="6" sketch:type="MSShapeGroup"></path>
                  <path d="M773,186 L827,217.538705 L827,279.636651 L773,310 L719,279.636651 L719,217.538705 L773,186 Z" id="Polygon-3" stroke="#795D9C" stroke-width="6" sketch:type="MSShapeGroup"></path>
                  <path d="M639,529 L773,607.846761 L773,763.091627 L639,839 L505,763.091627 L505,607.846761 L639,529 Z" id="Polygon-4" stroke="#F2773F" stroke-width="6" sketch:type="MSShapeGroup"></path>
                  <path d="M281,801 L383,861.025276 L383,979.21169 L281,1037 L179,979.21169 L179,861.025276 L281,801 Z" id="Polygon-5" stroke="#36B455" stroke-width="6" sketch:type="MSShapeGroup"></path>
              </g>
            </svg>
            <div class="message-box">
              <h1>Recognizing Result:</h1>
              <h1 style="color:#002afa;">{{result}}</h1>
              <p style="font-size: 1.1em">Due to the limitations of our database, it is possible that your song has not been identified, or has been identified incorrectly. We have recorded your uploaded song and reported it to the administrator. Thanks for helping us expand our library.</p>
              <div class="buttons-con">
                <div class="action-link-wrap">
                  <el-button type="success" @click="restartRecord()">Restart Process</el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import { UploadFilled } from '@element-plus/icons-vue'
import Recorder from 'js-audio-recorder'

export default {
  name: "recognizeEntry",
  data(){
    return{
      activeName: "first",
      reacordUpdateFinish: false,
      activeType2: 0,
      recognizeFinish: false,
      active: 0,
      uploading: false,
      loading: false,
      updateFinish: false,
      result: '',
      inputType: true, // true代表录音，false代表文件
      fileName: '',
      recorder: null,
      playTime: 0,
      timer: null,
      src: null
    }
  },
  components:{
    UploadFilled,
  },
  created() {
    this.recorder = new Recorder()
  },
  methods:{
    // restartRecord
    restartRecord(){
      this.handleDestroy()
      this.activeType2 = 0
    },

    restartUpload(){
      this.$refs.upload.handleRemove(this.fileName)
      this.active = 0
    },

    // 步骤条切换
    next(){
      if (this.active++ > 2){
        this.active = 3
      }
    },

    // 退回上传按钮
    turnToUpload(){
      this.active = this.active-1
    },

    // 开始录音
    handleStart() {
      console.log("123")
      this.recorder = new Recorder()
      Recorder.getPermission().then(() => {
        console.log('开始录音')
        this.recorder.start() // 开始录音
      }, (error) => {
        this.$message({
          message: 'Please allow this page to use the microphone first',
          type: 'info'
        })
        console.log(`${error.name} : ${error.message}`)
      })
    },
    handlePause() {
      console.log('暂停录音')
      this.recorder.pause() // 暂停录音
    },
    handleResume() {
      console.log('恢复录音')
      this.recorder.resume() // 恢复录音
    },
    handleStop() {
      console.log('停止录音')
      this.recorder.stop() // 停止录音
    },
    handlePlay() {
      console.log('播放录音')
      console.log(this.recorder)
      this.recorder.play() // 播放录音

      // 播放时长
      this.timer = setInterval(() => {
        try {
          this.playTime = this.recorder.getPlayTime()
        } catch (error) {
          this.timer = null
        }
      }, 100)
    },
    handlePausePlay() {
      console.log('暂停播放')
      this.recorder.pausePlay() // 暂停播放
      // 播放时长
      this.playTime = this.recorder.getPlayTime()
      this.time = null
    },
    handleResumePlay() {
      console.log('恢复播放')
      this.recorder.resumePlay() // 恢复播放

      // 播放时长
      this.timer = setInterval(() => {
        try {
          this.playTime = this.recorder.getPlayTime()
        } catch (error) {
          this.timer = null
        }
      }, 100)
    },
    handleStopPlay() {
      console.log('停止播放')
      this.recorder.stopPlay() // 停止播放
      // 播放时长
      this.playTime = this.recorder.getPlayTime()
      this.timer = null
    },
    handleDestroy() {
      console.log('销毁实例')
      this.recorder.destroy() // 毁实例
      this.timer = null
    },
    uploadRecord() {
      if (this.recorder == null || this.recorder.duration === 0) {
        this.$message({
          message: 'Please recording first',
          type: 'error'
        })
        return false
      }
      this.activeType2 = this.activeType2 + 1
      this.uploading = true
      this.recorder.pause() // 暂停录音
      this.timer = null
      console.log('上传录音')// 上传录音

      const formData = new FormData()
      const blob = this.recorder.getWAVBlob()// 获取wav格式音频数据
      // 此处获取到blob对象后需要设置fileName满足当前项目上传需求，其它项目可直接传把blob作为file塞入formData
      const newbolb = new Blob([blob], { type: 'audio/wav' })
      const fileOfBlob = new File([newbolb], new Date().getTime() + '.wav')
      formData.append('file', fileOfBlob)
      const url = window.URL.createObjectURL(fileOfBlob)
      this.src = url
      const path = '/api/uploadWAVMusic'
      this.$http.post(path, formData, {
        headers: {'Content-Type': 'multipart/form-data'}
      })
          .then(res => {
            console.log(res.data)
            this.updateFinish2 = true
            this.fileName = res.data
            this.uploading = false
            this.reacordUpdateFinish = true
          }).catch(response => {
            console.log(response)
          })
    },

    // 开始识别按钮
    recognize(){
      this.loading = true
      this.active = this.active + 1
      const musicPath = '/api/recognizeMusic'
      const payload = {
          fileName: this.fileName,
        }
      this.$http.post(musicPath, payload)
          .then(data => {
            console.log(data)
            this.result = data.data
            this.recognizeFinish = true
            this.loading = false
          }).catch(response => {
            console.log(response)
          })
    },

    // 开始识别按钮
    recognizeRecord(){
      this.loading = true
      this.activeType2 = this.activeType2 + 1
      const musicPath = '/api/recognizeMusic'
      const payload = {
          fileName: this.fileName,
        }
      this.$http.post(musicPath, payload)
          .then(data => {
            console.log(data)
            this.result = data.data
            this.recognizeFinish = true
            this.loading = false
          }).catch(response => {
            console.log(response)
          })
    },

    // 上传音频
    uploadHttp(){
      this.active = this.active + 1
      this.uploading = true
      const formData = new FormData()
      formData.append('file', this.$refs.upload.uploadFiles[0].raw)
      const musicPath = '/api/uploadMusic'
      this.$http.post(musicPath, formData, {
        headers: {'Content-Type': 'multipart/form-data'},
      })
          .then(data => {
            console.log(data)
            this.updateFinish = true
            this.fileName = data.data
            this.uploading = false
          }).catch(response => {
            console.log(response)
          })
    },
  }
}
</script>

<style lang="scss" scoped>
.switchButton{
  position: absolute;
  top: 5%;
  left: 40%;
}

input[type=checkbox]{
	height: 0;
	width: 0;
	visibility: hidden;
}

label {
	cursor: pointer;
	text-indent: -9999px;
	width: 200px;
	height: 100px;
	background: #1e71d3;
	display: block;
	border-radius: 100px;
	position: relative;
}

label:after {
	content: '';
	position: absolute;
	top: 5px;
	left: 5px;
	width: 90px;
	height: 90px;
	background: #fff;
	border-radius: 90px;
	transition: 0.3s;
}

input:checked + label {
	background: #6005e7;
}

input:checked + label:after {
	left: calc(100% - 5px);
	transform: translateX(-100%);
}

label:active:after {
	width: 130px;
}


.upload-demo{
  border: #6005e7 5px dashed;
  position: center;
  margin-top: 12%;
  margin-left: calc((80vw - 370px)/2);
  width: 370px;
  font-weight: bold;
}
.el-upload__tip{
  display: block;
  text-align: center;
}
.recognize{
  margin-top: 20%;
  display: block;
  margin-left: 40px;
  float: right;
}
.info{
  color: #6005e7;
  width: 80vw;
  height: 40vh;
  border: #6005e7 2px solid;
  border-radius: 10px;
  padding-left: 5%;
  padding-top: 2.5%;
  margin-top: 50px;
}
.info2{
  color: #6005e7;
  width: 80vw;
  height: 60vh;
  border: #6005e7 2px solid;
  border-radius: 10px;
  margin-top: 20px;
  margin-right: 10px;
}
.message-box {
  padding-top: 4%;
  display: inline-block;
  height: 90%;
  width: 55%;
  color: white;
  font-weight: 300;
}
.message-box h1 {
  font-size: 50px;
  /*line-height: 46px;*/
  margin-bottom: 40px;
}
.buttons-con .action-link-wrap {
  margin-top: 40px;
}
.buttons-con .action-link-wrap a {
  background: #68c950;
  padding: 8px 25px;
  border-radius: 4px;
  color: #FFF;
  font-weight: bold;
  font-size: 14px;
  transition: all 0.3s linear;
  cursor: pointer;
  text-decoration: none;
  margin-right: 10px
}
.buttons-con .action-link-wrap a:hover {
  background: #5A5C6C;
  color: #fff;
}
@keyframes float {
	100% {
    transform: translateY(20px);
  }
}
@media (max-width: 450px) {
  svg {
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -250px;
    margin-left: -190px;
  }
  .message-box {
    top: 50%;
    left: 50%;
    margin-top: -100px;
    margin-left: -190px;
    text-align: center;
  }
}
</style>