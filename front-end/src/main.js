import {createApp} from 'vue'
import App from './App.vue'
import router from './router/router'
import {message} from './utils/message'
import 'bootstrap/dist/css/bootstrap.css';

// 引入EmelemtPlus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from './http'

// 登陆页面的粒子效果
// 环境安装: npm install vue-particles --save-dev
// Reference: https://blog.csdn.net/weixin_42201180/article/details/111941697
import VueParticles from 'vue-particles'

// register the vue-toasted plugin on vue
import VueToasted from 'vue-toasted'

// 引入vuex
import Vuex from 'vuex'

// 引入全拼滚动插件
import 'fullpage.js/vendors/scrolloverflow' // Optional. When using scrollOverflow:true
import VueFullPage from 'vue-fullpage.js'
import moment from 'moment'

const app = createApp(App)

// 网易云音乐API全局变量地址
app.config.globalProperties.netEaseURL = 'https://autumnfish.cn/'

app.config.globalProperties.$moment = moment

app.use(router).use(VueFullPage).use(Vuex).use(VueParticles)
app.use(ElementPlus)

// 自定义的全局message函数，替换了Element的默认message函数
app.config.globalProperties.$message = message

// 将自定义的axios实例设置为全局变量
app.config.globalProperties.$http = axios

app.mount('#app')

// 以下是实际上没用到的代码
// app.filter('dateFormat', function (dateStr, pattern = "YYYY-MM-DD HH:mm:ss") {
//     return moment(dateStr).format(pattern);
// })

// window.addEventListener('load', () => {
//     app.use(VueToasted, {
//         // 主题样式 primary/outline/bubble
//         theme: 'bubble',
//         // 显示在页面哪个位置
//         position: 'top-center',
//         // 显示多久时间（毫秒）
//         duration: 3000,
//         // 支持哪个图标集合
//         iconPack: 'material', // set your iconPack, defaults to material. material|fontawesome|custom-class
//         // 可以执行哪些动作
//         action: {
//             text: 'Cancel',
//             onClick: (e, toastObject) => {
//                 toastObject.goAway(0)
//             }
//         },
//     });
// });
