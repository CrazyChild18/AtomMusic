import Vue from 'vue'
import axios from 'axios'
import router from './router/router'
import store from './store'
import app from "@/App";

// 基础配置
// axios.defaults.timeout = 5000  // 超时时间
if (process.env.NODE_ENV === 'production') {
    axios.defaults.baseURL = 'http://csi420-01-vm3.ucd.ie'
} else {
    axios.defaults.baseURL = 'http://127.0.0.1:8082';
}
// axios.defaults.baseURL = 'http://137.43.49.49:5000/api'//服务器要用，本地运行注掉本行
axios.defaults.headers['token'] = window.localStorage.getItem("atom-token")

// export default axios
// Add a request interceptor
axios.interceptors.request.use(function (config) {
    // Do something before request is sent
    const token = window.localStorage.getItem('atom-token')
    console.log(token)
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
}, function (error) {
    // Do something with request error
    return Promise.reject(error)
})

// Add a response interceptor
axios.interceptors.response.use(function (response) {
    // Do something with response data
    return response
}, function (error) {
    // Do something with response error
    switch (error.response.status) {
        case 401:
            // 清除 Token 及 已认证 等状态
            store.logoutAction()
            // 跳转到登录页
            if (router.currentRoute.path !== '/login') {
                app.toasted.error('401: 认证已失效，请先登录', {icon: 'fingerprint'})
                router.replace({
                    path: '/login',
                    query: {redirect: router.currentRoute.path},
                })
            }
            break

        case 404:
            app.toasted.error('404: NOT FOUND', {icon: 'fingerprint'})
            router.back()
            break
    }
    return Promise.reject(error)
})

export default axios // 导出axios实例