<template>
  <div id="app">
    <div class="header-wrapper">
      <div class="header">
        <div class="logo-wrapper">
          <img src="./assets/logo.png" class="nav-logo" />
        </div>
        <div class="login-status">
          <router-link v-if="!username" to="/login">登录</router-link>
          <div v-if="username">
            {{username}}
            <el-button @click="logout" size="mini" round>登出</el-button>
          </div>
        </div>
      </div>
    </div>
    <div class="wrapper">
      <div class="left-wrapper">
        <vc-leftnav></vc-leftnav>
      </div>
      <div class="main-wrapper">
        <div class="main-content">
          <router-view @loginSuccess="handleLogin"></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as config from "./config.js";
export default {
  name: "app",
  data() {
    return {
      username: ""
    };
  },
  methods: {
    loginCheck() {
      this.$http
        .get(config.HOST + config.API_URLS.login_stat,{withCredentials:true})
        .then(res => {
          if (res.data.logged_in) {
            sessionStorage.setItem("username", res.data.name);
            this.username = res.data.name;
          } else {
            this.username = "";
            sessionStorage.setItem("username", "");
          }
        })
        .catch(error => {
          this.username = "";
          sessionStorage.setItem("username", "");
        });
    },
    handleLogin(name) {
      // console.log('handled!~login')
      // console.log(name)
      this.username = name;
      sessionStorage.setItem("username", name);
    },
    logout() {
      this.$http.get(config.HOST + config.API_URLS.login_logout,{withCredentials:true}).then(res => {
        if (res.data.message == "ok") {
          this.username = "";
          sessionStorage.setItem("username", "");
          this.$notify({
                title: "成功",
                message: "登出成功",
                type: "success"
              });
          setTimeout(()=>{
                  this.$router.push({path:'/stat'})
                },50)
        } else{
          console.log(res)
          this.$notify({
                title: "警告",
                message: "登出失败，原因未知",
                type: "warning"
              });
        }
      }).catch((error)=>{
        console.log(error)
        this.$notify.error({
                title: "错误",
                message: "登出失败，服务器或通信错误",
              });
      });
    }
  },mounted(){
    this.loginCheck()
  }
};
</script>

<style lang="scss">
#app {
  // width: 1140px;
  height: 100%;
  // overflow: hidden;
  position: static;
}
a {
  text-decoration: none;
}
h2 {
  font-size: 18px;
  font-weight: bold;
}
.wrapper {
  margin: 0 auto;
  margin-top: 80px;
  width: 1140px;
}
.header-wrapper {
  left: 0;
  top: 0;
  width: 100%;
  position: fixed;
  background: #fff;
  z-index: 10;
}
.header {
  width: 1140px;
  height: 80px;
  line-height: 80px;
  background: #fff;
  margin: 0 auto;
  color: #888;
  border-bottom: 1px solid #dcdfe6;
}
.left-wrapper {
  top: 0;
  bottom: 0;
  margin-top: 80px;
  width: 200px;
  position: fixed;
  height: 100%;
  // background: lightgray;
}
.main-wrapper {
  padding-left: 220px;
  padding-top: 55px;
  width: 100%;
  // background: lightsteelblue;
}
.main-content {
  // background: #fdd;
  color: #5e6d82;
  line-height: 1.5em;
  padding-bottom: 80px;
}
.logo-wrapper {
  float: left;
  .nav-logo {
    vertical-align: middle;
    width: 146px;
    height: 38px;
  }
}
.header .login-status {
  float: right;
  line-height: 80px;
  font-size: 14px;
}
</style>
