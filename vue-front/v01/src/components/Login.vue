<template>
  <div class="login">
    <el-card class="box-card">
      <h2>管理员登录</h2>
      <el-form :label-position="'right'" label-width="80px" :model="login">
        <el-form-item label="账户">
          <el-input v-model="login.user"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="login.pw" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">登录</el-button>
          <el-button @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-alert title="访客登录说明" type="info" description="用户名密码填guest即可，能访问管理页面，但是不能保存修改" show-icon></el-alert>
  </div>
</template>

<script>
import * as config from "../config.js";
export default {
  data() {
    return {
      login: {
        user: "",
        pw: ""
      }
    };
  },
  methods: {
    reset() {
      this.login.user = "";
      this.login.pw = "";
    },
    onSubmit() {
      if (this.login.user.length && this.login.pw.length) {
        this.$http
          .get(config.HOST + config.API_URLS.login_auth, {
            params: { username: this.login.user, password: this.login.pw },
            withCredentials: true
          })
          .then(res => {
            if (res.data.message == "success") {
              // console.log(res);
              this.$emit("loginSuccess", res.data.name);
                this.$notify({
                  title: "成功",
                  message: "登录成功，现在可以访问管理页面",
                  type: "success"
                });
                setTimeout(()=>{
                  this.$router.push({path:'/admin'})
                },1000)
            } else {
              this.$notify({
                title: "警告",
                message: "登录失败，请检查用户名密码是否都准确填写",
                type: "warning"
              });
            }
          })
          .catch(error => {
            this.$notify.error({
              title: "警告",
              message: "通信可能出现问题，请检查服务器状态和网络状态"
            });
          });
      } else {
        this.$notify({
          title: "警告",
          message: "用户名和密码不能为空",
          type: "warning"
        });
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.login {
  margin: 0 auto;
  margin-top: 50px;
  width: 500px;
  height: 300px;
  // background-color: lightblue;
}
.box-card {
  padding-right: 10px;
  margin-bottom: 20px;
}
h2 {
  color: #5e6d82;
  line-height: 30px;
  font-size: 18px;
  font-weight: bold;
}
form {
  margin-top: 25px;
}
</style>