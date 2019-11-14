<template>
  <div class="about">
    <h2>项目说明</h2>
    <br />
    <div class="desc">
      <p>本项目可用于统计Bilibili的各种视频和UP主的状态数据</p>
      <p>可定向跟踪热度变化情况，观察用户习性</p>
      <br />
      <p>本项目使用Vue + VueCli + ElementUI + Echarts构建前端</p>
      <p>使用Python Flask + mysql 构建后端Service，提供API支持。</p>
      <br />
      <p>数据模型方面，魔改了廖雪峰的简易异步ORM，改为了多线程可用，并且借助DBUtils实现连接池</p>
      <br />
      <p>爬虫方面，自行实现了分布式的爬虫系统，爬虫worker通过轮询服务器领取任务，爬取后提交。</p>
      <p>手写了低开销的加密算法来实现WORKER与服务器间的通信认证</p>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
.desc {
  font-size: 14px;
}
</style>