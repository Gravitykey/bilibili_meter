<template>
  <ul class="nav-left">
    <li>
      <ul class="sub-nav">
        <li>
          <router-link class="nav-item" to="/status">运行状态</router-link>
        </li>
        <li>
          <router-link class="nav-item" to="/sitedata">全站在线数据</router-link>
        </li>
        <li>
          <router-link class="nav-item" to="/activity">全站活跃度数据</router-link>
        </li>
        <li>
          <router-link class="nav-item" to="/uplist">关注的UP</router-link>
        </li>
        <li>
          <router-link class="nav-item" to="/videolist">关注的视频</router-link>
        </li>
        <li>
          <router-link class="nav-item" to="/admin">管理</router-link>
        </li>
      </ul>
    </li>
    <li class="info">
      <router-link class="nav-item" to="/about">关于项目</router-link>
    </li>
    <li class="links">
        <span>我的</span>
      <div class="link-item" style="line-height:40px;">
        <img src="../assets/gh.png" width="40" height="40" />
        <a href="https://github.com/gravitykey" target="_blank" class="nav-item">github</a>     
      </div>
      <div class="link-item">
        <a href="https://gravitykey.top/" target="_blank" class="nav-item">个人站点</a>
      </div>
      <div class="link-item">
        <a href="https://www.cnblogs.com/gk2017" target="_blank" class="nav-item">很久没管的blog</a></div>
    </li>
    <li></li>
  </ul>
</template>

<script>
export default {
  data() {
    return {};
  }
};
</script>

<style lang="scss">
.nav-item {
  height: 40px;
  line-height: 40px;
  text-decoration: none;
  color: #444;
  font-size: 14px;
  transition: 0.15s ease-out;
  &:hover {
    color: #409eff;
  }
}
.sub-nav :hover {
  background: #e6f0fa;
  transition: 0.4s ease-out;
}
ul.nav-left {
  padding-top: 50px;
}
.links {
  margin-top: 50px;
  font-size: 14px;
  .link-item {
    margin-top: 20px;
  }
  span{
      font-size: 14px;
      font-weight: bold;
      color:#444;
  }
  img{
      vertical-align: middle;
  }
}
.info {
  margin-top: 20px;
}
a.router-link-active, li.router-link-active a {
  color: #409eff;
}
</style>