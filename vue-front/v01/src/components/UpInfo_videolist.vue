<template>
  <div>
    <!-- {{uid}} -->
    <div v-if="!videos.length" class="notfound">Bilibili Meter 当前好像没有关注该UP的视频</div>
    <ul v-if="videos.length" class="up-video-list">
      <li v-for="video in videos" :key="video.id">
        <router-link :to="'/videoinfo/'+video.id">
          <img :src="video.pic" class="pic" />
        </router-link>
        <div>
          <div class="title">
            <router-link class="title-link" :to="'/videoinfo/'+video.id">{{video.title}}</router-link>
          </div>
          <div class="in-line">
            <div class="tname atr">分类 : {{video.tname}}</div>
            <div class="pubdate atr">{{tsToDateStr(video.pubdate*1000)}}</div>
          </div>
        </div>
      </li>
      <div class="clearfix"></div>
    </ul>
  </div>
</template>

<script>
import { tsToDateStr } from "../utils.js";
export default {
  props: { videos: Array },
  data() {
    return {
      loaded: false,
      notfound: false
    };
  },
  methods: {
    tsToDateStr
  },
};
</script>

<style lang="scss" scoped>
.loading,
.notfound {
  text-align: center;
  font-size: 14px;
  margin-top: 30px;
}
.up-video-list {
  img {
    border: 1px solid #80a9d3;
    border-radius: 5px;
    width: 160px;
    height: 100px;
  }
  .title a {
    font-size: 12px;
    text-decoration: none;
    color: #80a9d3;
  }
  .in-line {
    font-size: 12px;
    color: #666;
  }
  li {
    float: left;
    margin-right: 20px;
    margin-top: 20px;
    width: 160px;
  }
}
</style>