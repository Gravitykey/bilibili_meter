import Vue from 'vue'

import VueRouter from 'vue-router'
Vue.use(VueRouter)

import App from './App.vue'


// 引入elementUI，改为按需引入
// import ElementUI from 'element-ui'
// Vue.use(ElementUI)

import {
  Pagination,
  Input,
  Select,
  Option,
  Button,
  Switch,
  Table,
  TableColumn,
  Form,
  FormItem,
  Tabs,
  TabPane,
  Alert,
  Col,
  Card,
  Notification
} from 'element-ui';

Vue.use(Pagination),
Vue.use(Input),
Vue.use(Select),
Vue.use(Option),
Vue.use(Button),
Vue.use(Switch),
Vue.use(Table),
Vue.use(TableColumn),
Vue.use(Form),
Vue.use(FormItem),
Vue.use(Tabs),
Vue.use(TabPane),
Vue.use(Alert),
Vue.use(Col),
Vue.use(Card),
Vue.prototype.$notify = Notification;

// elementUI引入结束

// 引入echarts
import * as echarts from './echarts.custom.js'
Vue.prototype.$echarts = echarts

import axios from 'axios'
import VueAxios from 'vue-axios'
Vue.use(VueAxios, axios)


import './assets/css/reset.css'



// 组件
import LeftNav from './components/LeftNav.vue'
Vue.component('vc-leftnav', LeftNav)

import Status from './components/Status.vue'
Vue.component('vc-status', Status)

import SiteData from './components/SiteData.vue'
Vue.component('vc-sitedata', SiteData)

import Activity from './components/Activity.vue'
Vue.component('vc-activity', Activity)

import UpList from './components/UpList.vue'
Vue.component('vc-uplist', UpList)

import VideoList from './components/VideoList.vue'
Vue.component('vc-videolist', VideoList)

import Upinfo from './components/UpInfo.vue'
Vue.component('vc-upinfo', Upinfo)

import Videoinfo from './components/VideoInfo.vue'
Vue.component('vc-videoinfo', Videoinfo)

import About from './components/About.vue'
Vue.component('vc-about', About)

import UpinfoVideolist from './components/Upinfo_videolist.vue'
Vue.component('vc-upinfo-videolist', UpinfoVideolist)

import Admin from './components/Admin.vue'
Vue.component('vc-admin', Admin)
import AdminFastAddTask from './components/AdminFastAddTask.vue'
Vue.component('vc-admin-fastaddtask',AdminFastAddTask)
import AdminAddTask from './components/AdminAddTask.vue'
Vue.component('vc-admin-addtask', AdminAddTask)
import AdminTaskList from './components/AdminTaskList.vue'
Vue.component('vc-admin-tasklist', AdminTaskList)
import AdminFailLog from './components/AdminFailLog.vue'
Vue.component('vc-admin-faillog', AdminFailLog)

import Login from './components/Login.vue'
Vue.component('vc-admin', Login)

// 路由
const routes = [
  { path: '*', redirect:'/status' },
  { path: '/status', component: Status },
  { path: '/sitedata', component: SiteData },
  { path: '/activity', component: Activity },
  { path: '/uplist', component: UpList },
  { path: '/videolist', component: VideoList },
  { path: '/upinfo/:id', component: Upinfo },
  { path: '/videoinfo/:id', component: Videoinfo },
  { path: '/about', component: About },
  { path: '/admin', component: Admin },
  { path: '/login', component: Login },
]

const router = new VueRouter({
  routes // (缩写) 相当于 routes: routes
})

new Vue({
  el: '#app',
  render: h => h(App),
  router,
})

