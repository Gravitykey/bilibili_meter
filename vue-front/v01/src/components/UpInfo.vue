<template>
  <div>
    <h2>个人详情数据</h2>
    <div v-show="loading" class="loading">获取 UID：{{this.id}} 的数据中</div>
    <div v-show="notfound" class="notfound">
      请求的UID：{{this.id}}
      <br />获取失败，或者并没有关注此用户 o(╥﹏╥)o
    </div>
    <!-- 内容主体 -->
    <div v-show="loaded" class="info-wrapper">
      <div class="face">
        <img :src="upinfo.face" alt />
      </div>
      <div class="right">
        <div class="line">
          <span class="name">{{upinfo.name}}</span>
          <i v-if="upinfo.sex=='男'" class="el-icon-male"></i>
          <i v-if="upinfo.sex=='女'" class="el-icon-female"></i>
          <span class="uid">UID : {{upinfo.id}}</span>
        </div>
        <div class="line">
          <span class="sign">{{upinfo.sign}}</span>
        </div>
        <div class="line">
          <a class="space-link" :href="'https://space.bilibili.com/'+upinfo.id" target="_blank">
            <i class="el-icon-link"></i>
            {{'https://space.bilibili.com/'+upinfo.id}}
          </a>
        </div>
      </div>
      <div class="clearfix"></div>
      <!-- 头像和下方的分割线 -->
      <hr />
      <div class="chart-block">
        <div class="chart upinfo"></div>
      </div>
      <!-- 图表和视频列表分割线 -->
      <!-- <div>up主信息，UID{{this.id}}</div> -->
      <div class="videolists">
        <hr />
        <h3>关注的该用户的视频列表</h3>
        <vc-upinfo-videolist :videos="videos"></vc-upinfo-videolist>
      </div>
      <!-- loaded末尾 -->
    </div>
    <!-- 分割线 -->
  </div>
</template>

<script>
// import * as echarts from "../echarts.custom.js";
import * as config from "../config.js";
import { upInfoChartOption } from "./chartOptions.js";
export default {
  data() {
    return {
      id: 0,
      loading: true,
      notfound: false,
      loaded: false,
      upinfo: {
        face: "",
        sign: "loading",
        name: "loading",
        id: 0,
        sex: "loading"
      },
      videos: []
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
        .get(config.HOST + config.API_URLS.up_info, {
          params: { uid: this.id }
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
          this.upinfo = res.data.upinfo;
          this.videos = res.data.videos;
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
    let op = upInfoChartOption;
    console.log(op);
    this.chart1= this.initEchart(el, op);
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
      this.fetchData();
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
    background-color: #ccc;
    height: 1px;
    border: 0;
  }
  .face {
    float: left;
    img {
      width: 100px;
      height: 100px;
      border: 2px solid #ccc;
      border-radius: 50%;
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
  .name {
    font-size: 16px;
    font-weight: bold;
    color: #80a9d3;
  }
  .uid {
    margin-left: 20px;
    font-size: 12px;
  }
  i {
    margin-left: 10px;
    font-weight: bold;
  }
  .sign {
    font-size: 12px;
    color: #888;
  }
  .space-link {
    padding-top: 15px;
    text-decoration: none;
    font-size: 12px;
    color: #409eff;
    i {
      margin-left: 0;
      margin-right: 5px;
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
  height: 400px;
}
.videolists {
  margin-top: 20px;
  font-size: 14px;
  h3 {
    margin-top: 20px;
  }
}
</style>