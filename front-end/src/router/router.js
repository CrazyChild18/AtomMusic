import {createRouter, createWebHashHistory} from 'vue-router'

const routes = [
    {
        // path: '/music/:id',
        path: '/',
        name: 'home',
        component: () => import('../views/Home/indexHome'),
        meta: {
            requiresAuth: true,
            title: 'Home - Atom Cloud Music'
        },
        children: [
            {
                path: '/music/:id',
                name: 'music',
                component: () => import('../views/Home/Screen/musicShow'),
                meta:{
                    title: 'Music Show - Atom Cloud Music'
                }
            },
            {
                path: '/info/:id',
                name: 'info',
                component: () => import('../views/Home/UserInfo/userInfo'),
                meta:{
                    title: 'Info - Atom Cloud Music'
                }
            },
            {
                path: '/infoEdit/:id',
                name: 'infoEdit',
                component: () => import('../views/Home/UserInfo/userInfoEdit'),
                meta:{
                    title: 'Info Edit - Atom Cloud Music'
                }

            },
            {
                path: '/musicDetail',
                name: 'musicDetail',
                component: () => import('../views/Home/Screen/musicDetail'),
                meta:{
                    title: 'Music Show - Atom Cloud Music'
                }

            },
            {
                path: '/recognize',
                name: 'recognize',
                component: () => import('../views/Home/Screen/recognizeEntry'),
                meta:{
                    title: 'Music Recognition - Atom Cloud Music'
                }
            },
            {
                path: '/recognize_notfound',
                name: 'recognize_notfound',
                component: () => import('../views/Home/Screen/Recognize_404'),
                meta:{
                    title: 'Music Recognition - Atom Cloud Music'
                }

            },
            {
                path: '/userDataVisualization/:id',
                name: 'userDataVisualization',
                component: () => import('../views/Home/UserInfo/userDataView'),
                meta:{
                    title: 'Footprint - Atom Cloud Music'
                }

            },
            {
                path: '/recommend',
                name: 'recommend',
                component: () => import('../views/Home/Screen/recommendSongs'),
                meta:{
                    title: 'Music Recommendation - Atom Cloud Music'
                }

            }
        ]
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('../views/Login/loginPage'),
    },
    {
        path: '/enter',
        name: 'enter',
        component: () => import('../views/Login/enterPage'),
    },
    {
        path: '/out',
        name: 'out',
        component: () => import('../views/Login/outPage'),
    },
]
const router = createRouter({
    history: createWebHashHistory(),
    routes
})
router.beforeEach((to, from, next) => {
    const token = window.localStorage.getItem('atom-token')
    if (to.matched.some(record => record.meta.requiresAuth) && (!token)) {
        console.log('Token: ' + token)
        next({
            path: '/login',
            query: {redirect: to.fullPath}
        })
    } else if (token && to.name === 'login') {
        // 用户已登录，但又去访问登录页面时不让他过去
        next({
            path: from.fullPath
        })
    } else {
        next()
    }
     if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

export default router