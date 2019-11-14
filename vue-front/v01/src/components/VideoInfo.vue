<template>
  <div>
    <h2>视频数据</h2>
    <div v-show="loading" class="loading">获取 av号：{{this.id}} 的数据中</div>
    <div v-show="notfound" class="notfound">
      请求的av号：{{this.id}}
      <br />获取失败，或者并没有关注此视频 o(╥﹏╥)o
    </div>
    <!-- 内容主体 -->
    <div v-show="loaded" class="info-wrapper">
      <div class="pic">
        <img :src="videoinfo.pic" alt />
      </div>
      <div class="right">
        <div class="line">
          <span class="title">{{videoinfo.title}}</span>
          <span class="av">av : {{videoinfo.id}}</span>
        </div>
        <div class="line">
          <div class="desc">{{videoinfo.desc}}</div>
        </div>
        <div class="line">
          <router-link class="space-link" :to="'/upinfo/'+videoinfo.owner_mid">
            <i class="el-icon-user"></i>
            {{videoinfo.owner_mid}}
          </router-link>
          <a
            class="space-link"
            :href="'https://www.bilibili.com/video/av'+videoinfo.id"
            target="_blank"
          >
            <i class="el-icon-link"></i>
            {{'av'+videoinfo.id}}
          </a>
          <a
            class="space-link"
            :href="'https://space.bilibili.com/'+videoinfo.owner_mid"
            target="_blank"
          >
            <i class="el-icon-link"></i>
            {{'https://space.bilibili.com/'+videoinfo.owner_mid}}
          </a>
        </div>
      </div>
      <div class="clearfix"></div>
      <!-- 头像和下方的分割线 -->
      <!-- <hr /> -->
      <div class="chart-block">
        <div class="chart upinfo"></div>
      </div>
      <!-- 图表和视频列表分割线 -->
      <!-- <div>up主信息，UID{{this.id}}</div> -->
      <!-- loaded末尾 -->
    </div>
    <!-- 分割线 -->
  </div>
</template>

<script>
// import * as echarts from "../echarts.custom.js";
import * as config from "../config.js";
import { videoInfoChartOption } from "./chartOptions.js";
export default {
  data() {
    return {
      id: 0,
      loading: true,
      notfound: false,
      loaded: false,
      videoinfo: {
        id: 0,
        owner_mid: 0,
        tname: "loading",
        pic: "",
        title: "loading",
        desc: "loading",
        pubdate: 0
      }
    };
  },
  methods: {
    getID() {
      this.id = this.$route.params.id;
    },
    initEchart(el, option) {
      let myChart = this.$echarts.init(el);
      myChart.setOption(option);
      return myChart;
    },
    fetchData() {
      this.$http
        .get(config.HOST + config.API_URLS.video_info, {
          params: { av: this.id }
        })
        .then(res => {
          console.log(res);
          res.data.data.forEach(i => {
            i.time *= 1000;
          });
          this.chart1.setOption({
            dataset: {
              source: res.data.data
            }
          });
          this.videoinfo = res.data.videoinfo;
          this.loading = false;
          this.loaded = true;
        })
        .catch(error => {
          // console.log('err_f')
          // console.log(error.response)
          this.loading = false;
          this.loaded = false;
          this.notfound = true;
        });
    }
  },
  mounted() {
    console.log("mounted");

    let el = document.querySelector(".chart-block .chart.upinfo");
    let op = videoInfoChartOption;
    this.chart1 = this.initEchart(el, op);
    this.fetchData();
  },

  beforeMount() {
    this.getID();
  },
  beforeDestroy() {
    this.chart1.clear();
    this.chart1.dispose();
  },
  watch: {
    $route(to, from) {
      this.getID();
    }
  }
};
</script>

<style lang="scss" scoped>
.notfound,
.loading {
  text-align: center;
  font-size: 16px;
  line-height: 2em;
  margin-top: 40px;
}
.info-wrapper {
  // background: #e6f0fa;
  margin-top: 40px;
  width: 100%;
  hr {
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .pic {
    float: left;
    img {
      width: 240px;
      height: 150px;
      border: 2px solid #ccc;
      border-radius: 10px;
    }
  }
  .right {
    float: left;
    margin-left: 30px;
    padding-top: 10px;
    min-height: 100px;
    width: 60%;
    // background: #ffddff;
  }
  .title {
    font-size: 16px;
    font-weight: bold;
    color: #80a9d3;
  }
  .av {
    margin-left: 20px;
    font-size: 12px;
  }
  i {
    margin-left: 10px;
    font-weight: bold;
  }
  .desc {
    font-size: 12px;
    color: #aaa;
    height: 72px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
  }
  .space-link {
    margin-right: 20px;
    padding-top: 15px;
    text-decoration: none;
    font-size: 12px;
    color: #409eff;
    i {
      margin-left: 0;
      margin-right: 2px;
    }
  }
}

.line {
  width: 100%;
  // background: #e6f0fa;
}

.chart-block {
  margin-top: 30px;
  font-size: 12px;
  text-align: center;
}
.chart {
  width: 920px;
  height: 450px;
  &.upload {
    width: 70%;
    float: left;
  }
  &.upload-pie {
    width: 29%;
    float: left;
  }
}
.videolists {
  margin-top: 20px;
  font-size: 14px;
  h3 {
    margin-top: 20px;
  }
}
</style>