<template>
  <el-row>
    <el-col :span="8">
      <div class="grid-content bg-purple-light" style="padding: 5px; text-align: center; font-size: 15px;">
        <img style="width: 30px; height: 30px; margin-right: 5px" src="time.png"><span style="font-weight: bold">Registered Duration:</span>
        {{ continueDays }} Days
      </div>
    </el-col>
    <el-col :span="8">
      <div class="grid-content bg-purple-light" style="padding: 5px; text-align: center; font-size: 15px;">
        <img style="width: 30px; height: 30px; margin-right: 5px" src="calander.png"><span style="font-weight: bold">Last Login:</span>
        {{ $moment(user.last_login_time).format('LLL') }}
      </div>
    </el-col>
    <el-col :span="8">
      <div class="grid-content bg-purple-light" style="padding: 5px; text-align: center; font-size: 15px;">
        <img style="width: 30px; height: 30px; margin-right: 5px" src="totalTime.png"><span style="font-weight: bold">Continuous Use Duration:</span>
        {{ (user.accumulate_duration / 60).toFixed(1) }} Minus
      </div>
    </el-col>
  </el-row>

  <!--具体信息展示-->
  <el-row>
    <el-col :span="10">
      <div class="grid-content">
        <div id="chartBar" class="bar-wrap" style="margin-left: 15px;margin-right: 15px; height: 300px"></div>
        <div class="chartDetail">
          <div class="content">
            <h4>Listening Ranking List</h4>
            <p style="color: darkgray">The chart shows the top 5 songs and times you have listened to in history</p>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :span="2"></el-col>
    <el-col :span="11">
      <div class="grid-content">
        <div id="chartPie" class="pie-wrap" style="margin-left: 15px;margin-right: 15px; height: 300px"></div>
        <div class="chartDetail">
          <div class="content">
            <h4>Proportion of Like Song</h4>
            <p style="color: darkgray">This chart shows the proportion of users' favorite songs and all songs in history</p>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>

  <el-row>
    <el-col :span="16">
      <div class="grid-content" style="height: 220px">
        <div id="chartLine" ref="chartLine" class="line-wrap" style="height: 240px"></div>
        <div class="lineChartDetail">
          <div class="content">
            <h4>Trend of listening</h4>
            <p style="color: darkgray">Show the trend of the number of songs you have listened to in the past 5 days here</p>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :span="8"></el-col>
  </el-row>
</template>

<script>
import * as echarts from 'echarts';

require('echarts/theme/macarons');//引入主题
require('echarts/theme/shine');//引入主题
require('echarts/lib/chart/bar');

import {Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, Chart} from 'chart.js'
import {DArrowLeft, DArrowRight} from "@element-plus/icons-vue";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'BarChart',
  components: {
    DArrowRight,
    DArrowLeft,
  },
  data() {
    return {
      likeMusicInHistory: [],
      historyMusic: [],
      lineChartDataList: [],
      lineChartCountList: [],
      chartPie: null,
      chartLine: null,
      id: '',
      continueDays: '',
      user: {
        username: '',
        email: '',
        name: '',
        location: '',
        phone: '',
        sex: '',
        about_me: '',
        create_time: '',
        last_login_time: '',
        accumulate_duration: '',
        _links: {
          self: '',
          avatar: ''
        }
      },
      userAvatarSrc: '',
      barLabel: [],
      barData: [],
    }
  },
  created() {
    this.id = this.$route.params.id
    this.getUser()
    this.getCreateTimeToNow()
    this.getHistoryAndCount()
    this.getPerDayAmount()
    this.getLikeAndHistory()
  },

  mounted() {},

  methods: {
    // 获取用户已注册时长
    getCreateTimeToNow() {
      const path = '/api/countTime'
      const payload = {
        userId: this.id,
      }
      this.$http.post(path, payload)
          .then((response) => {
            // console.log(response.data)
            this.continueDays = response.data
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error)
          });
    },

    // 获取用户头像
    setUserAvatar() {
      if (this.user._links.avatar == '') {
        this.userAvatarSrc = 'loginBackground.jpg'
      } else {
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

    // 获取用户信息
    getUser() {
      const path = '/api/getUserDetail'
      const payload = {
        userId: this.id,
      }
      this.$http.post(path, payload)
          .then((response) => {
            // console.log(response.data)
            this.user = response.data
            this.setUserAvatar()
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error)
          });
    },

    // 获取用户历史记录和每一个的数量
    getHistoryAndCount() {
      const path = '/api/getHistoryAndCount'
      const payload = {
        userId: this.id,
      }
      this.$http.post(path, payload)
          .then((response) => {
            this.barLabel = response.data.musicList
            this.barData = response.data.countList
            this.drawbarChart()
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error)
          });
    },

    // 获取每日用户听歌数量
    getPerDayAmount() {
      const path = '/api/getPerDayAmount'
      const payload = {
        userId: this.id,
      }
      this.$http.post(path, payload)
          .then((response) => {
            console.log(response.data)
            this.lineChartCountList = response.data[0]
            this.lineChartDataList = response.data[1]
            this.drawLineChart();
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error)
          });
    },

    // 柱状图绘制
    drawbarChart(){
      let mylabel = {
        show: true,
        position: "top",
        offset: [30, -20],
        formatter: '{b} : {c}',
        textStyle: {
          color: "#ffffff",
          fontSize: 18,
        }
      };
      this.chartBar = echarts.init(document.getElementById('chartBar'), 'macarons');
      this.chartBar.setOption({
        xAxis: {
          data: this.barLabel,
          axisLabel : {    //  X 坐标轴标签相关设置
            interval:0,
            rotate:"45",
            color: "#ffffff"
          }
        },

        yAxis: {
          axisLabel : {
            color: "#ffffff"
          }
        },
        series: [{
          type: 'bar',
          data: this.barData,
          label: {
            emphasis: mylabel
          },
          itemStyle: {
            "color":function(params){
                var colorarrays = ["#ffffff","#ffffff","#ffffff","#ffffff","#ffffff"];
                return colorarrays[params.dataIndex];
              }
          },
        }],
      });
    },

    // 折线图绘制函数
    drawLineChart() {
      this.chartLine = echarts.init(this.$refs.chartLine, 'shine');// 基于准备好的dom，初始化echarts实例
      let option = {
        tooltip: {
          trigger: 'axis'
        },
        calculable: true,
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            axisTick: {
              show: false
            },
            data: this.lineChartDataList,
            axisLabel: {
              show: true,
              textStyle: {
                 color: '#fff'
               }
            },
          }
        ],
        yAxis: [
          {
            type: 'value',
            axisTick: {
              show: false
            },
            name: '(Times)',
            axisLabel: {
              show: true,
              textStyle: {
                 color: '#fff'
               }
            },
          }
        ],
        series: [
          {
            name: 'pageviews',
            type: 'line',
            stack: '总量',
            data: this.lineChartCountList,
            itemStyle: {
              normal: {
                color: "#ffffff",//折线点的颜色
                lineStyle: {
                  color: "#ffffff"//折线的颜色
                }
              }
            },
          }
        ]
      };
      // 使用刚指定的配置项和数据显示图表
      this.chartLine.setOption(option);
    },

    // 获取用户听歌数量与喜欢歌曲数量比
    getLikeAndHistory() {
      const path = '/api/getLikeAndHistory'
      const payload = {
        userId: this.id,
      }
      this.$http.post(path, payload)
          .then((response) => {
            console.log(response.data)
            this.likeMusicInHistory = response.data[0]
            this.historyMusic = response.data[1]
            this.drawPieChart()
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error)
          });
    },

    // 饼图绘制函数
    drawPieChart() {
      let mytextStyle = {
        color: "#ffffff",
        fontSize: 18,
      };
      let mylabel = {
        show: true,
        position: "right",
        offset: [30, 40],
        formatter: '{b} : {c}',
        textStyle: mytextStyle
      };
      this.chartPie = echarts.init(document.getElementById('chartPie'), 'macarons');
      this.chartPie.setOption({
        title: {
          x: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: "{b} : {c}",
          backgroundColor: '#ffffff',
        },
        series: [
          {
             // 修改字体颜色的代码begin
            itemStyle: {
                  normal: {
                      label: {
                          textStyle: {
                            color:'#ffffff',
                              fontSize: 14,
                              fontWeight:'bolder'
                          }
                      },
                    labelLine : {
                          lineStyle:{
                            color:'#ffffff'
                          }
                      }
                  }
              },
            type: 'pie',
            radius: ['40%', '60%'],
            center: ['50%', '50%'],
            data: [
              this.likeMusicInHistory,
              this.historyMusic,
            ],
            animationEasing: 'cubicInOut',
            animationDuration: 2000,
            label: {
              emphasis: mylabel
            }
          }
        ]
      });
    },
  }
}
</script>

<style scoped>
.userAvatar {
  display: inline-block;
  width: 2.5em;
  height: 2.5em;
  border-radius: 1.25em;
}

.el-row {
  margin-bottom: 20px;
}

.el-row:last-child {
  margin-bottom: 0;
}

.el-col {
  border-radius: 4px;
}

.bg-purple-dark {
  background: #99a9bf;
}

.bg-purple {
  background: #d3dce6;
}

.bg-purple-light {
  background: #e5e9f2;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

.pie-wrap {
  font-weight: bold;
  border: #41e182 3px solid;
  background-color: #41e182;
  height: 250px;
  border-radius: 15px;
}

.line-wrap {
  font-weight: bold;
  border: #262629 3px solid;
  background-color: #262629;
  height: 250px;
  margin-top: -120px;
  border-radius: 15px;
}

.bar-wrap {
  font-weight: bold;
  border: #5fa0fd 3px solid;
  background-color: #5fa0fd;
  height: 250px;
  border-radius: 15px;
}
.chartDetail{
  border: #FFFFFF 2px solid;
  background-color: white;
  height: 250px;
  box-shadow: 0 0 25px gray;
  position: relative;
  top: -120px;
  z-index: -1;
  border-radius: 20px;
  padding-left: 5px;
  padding-right: 5px;
}
.chartDetail .content{
  position: absolute;
  bottom: 5px;
  text-align: left;
}
.lineChartDetail{
  border: #FFFFFF 2px solid;
  background-color: white;
  height: 230px;
  box-shadow: 0 0 25px gray;
  position: relative;
  top: -235px;
  right: -320px;
  z-index: -1;
  border-radius: 20px;
  padding-top: 20px;
  padding-right: 10px;
}
.lineChartDetail .content{
  width: 290px;
  position: absolute;
  right: 5px;
  text-align: left;
}
</style>