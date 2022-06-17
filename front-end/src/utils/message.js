import {ElMessage} from 'element-plus'

export const message = {
    success: (str) => {
        ElMessage({
            showClose: true, // 设置可关闭
            duration: 2000, // 显示时间，单位毫秒
            message: str,
            type: 'success', // 成功
        })
    },
    info: (str) => {
        ElMessage({
            showClose: true, // 设置可关闭
            duration: 2000, // 显示时间，单位毫秒
            message: str // 默认灰色
        })
    },
    warning: (str) => {
        ElMessage({
            showClose: true, // 设置可关闭
            duration: 2000, // 显示时间，单位毫秒
            message: str,
            type: 'warning', // 警告
        })
    },
    error: (str) => {
        ElMessage({
            showClose: true, // 设置可关闭
            duration: 2000, // 显示时间，单位毫秒
            message: str,
            type: 'error', // 红色错误
        })
    },
}