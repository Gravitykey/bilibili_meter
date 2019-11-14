<template>
  <div class="sitedata-wrapper">
    <h2>全站在线数据</h2>
    <div class="sitedata-block"></div>
    <el-switch v-model="byDay" @change="fetchData" active-text="按天统计" inactive-text="连续数据"></el-switch>
    <div class="desc">
    在图表中使用鼠标滚轮或者拖拽下方滑块可缩放数据范围
    </div>
    <div class="sitedata-block">
      <div class="chart online"></div>
      <div class="time">原始数据时间范围: {{tsToDateStr(dateBegin)}} 到 {{tsToDateStr(dateEnd)}}</div>
      <div class="clearfix"></div>
    </div>
    <div class="sitedata-block">
      <div class="chart upload"></div>
    </div>
    <div class="sitedata-block">
      <div class="chart upload-pie"></div>
      <div class="time">原始数据时间范围: {{tsToDateStr(dateBegin)}} 到 {{tsToDateStr(dateEnd)}}</div>
      <div class="clearfix"></div>
    </div>
  </div>
</template>

<script>
import * as config from "../config.js";
// import * as echarts from "../echarts.custom.js";
import * as chartDataProcess from "./chartDataProcess.js";
import { onlineChartsOption } from "./chartOptions.js";
export default {
  data() {
    return {
      // onlineChartsOption: onlineChartsOption,
      byDay: false,
      dateBegin: 0,
      dateEnd: 0
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initCharts();
      this.fetchData();
    });
  },
  beforeDestroy() {
    // 防止潜在内存泄漏隐患，清理掉图表
    for (var c in this.charts) {
      // console.log(c);
      this.charts[c].clear();
      this.charts[c].dispose();
    }
  },
  methods: {
    tsToDateStr:chartDataProcess.tsToDateStr,
    initCharts() {
      // console.log(onlineChartsOption);
      this.rawData = {
        nowUse: [],
        continuous: [],
        byDay: []
      };

      // 初始化
      let el = document.querySelector(".sitedata-wrapper .chart.online");
      let op = onlineChartsOption.chartOnline;
      let el2 = document.querySelector(".sitedata-wrapper .chart.upload");
      let op2 = onlineChartsOption.chartCount;
      let el3 = document.querySelector(".sitedata-wrapper .chart.upload-pie");
      let op3 = onlineChartsOption.countPie;

      //
      let chart1 = this.initEchart(el, op);
      let chart2 = this.initEchart(el2, op2);
      let chart3 = this.initEchart(el3, op3);
      this.$echarts.connect([chart1, chart2]);
      this.charts = { chart1: chart1, chart2: chart2, chart3: chart3 };
      // 绑定回调
      let editPie = chartDataProcess.debounce((idx, chart) => {
        let pieData = chartDataProcess.makePieData(this.countDataset, idx);
        chart.setOption({
          series: {
            type: "pie",
            id: "pie",
            name: "投稿" + pieData.time,
            data: pieData.data
          },
          title: {
            text: "投稿" + pieData.time
          }
        });
      }, 300);
      this.charts.chart2.on("updateAxisPointer", event => {
        var xAxisInfo = event.axesInfo[0];
        if (xAxisInfo) {
          var idx = event.dataIndex;
          editPie(idx, this.charts.chart3);
        }
      });
      this.charts.chart2.setOption(op2);
      // console.log(this);
    },

    //-------------init结束-------------

    initEchart(el, option) {
      let myChart = this.$echarts.init(el);
      myChart.setOption(option);
      return myChart;
    },

    setDataset() {
      // // console.log(this.rawData.nowUse, 265);
      let onlineDataset = chartDataProcess.makeOnlineDataset(
        this.rawData.nowUse
      );
      let countDataset = chartDataProcess.makeCountDataset(this.rawData.nowUse);
      let countSeries = chartDataProcess.makeCountSeries();
      // 单独留出来，供饼图使用
      this.countDataset = countDataset;
      this.charts.chart1.setOption({ dataset: { source: onlineDataset } });
      // // console.log(countDataset, 271);
      this.charts.chart2.setOption({
        dataset: { source: countDataset },
        series: countSeries
      });
      if (this.rawData.nowUse.length > 0) {
        this.dateBegin = this.rawData.nowUse[0].time * 1000;
        this.dateEnd = this.rawData.nowUse[this.rawData.nowUse.length - 1].time * 1000;
      } else{
        this.dateBegin=0
        this.dateEnd=0
      }
    },

    fetchData() {
      // console.log("fetchdata");
      if (this.byDay && this.rawData.byDay.length != 0) {
        // console.log(this.rawData, 278);
        this.rawData.nowUse = this.rawData.byDay;
        this.setDataset();
      } else if (!this.byDay && this.rawData.continuous.length != 0) {
        // console.log(this.rawData, 282);
        this.rawData.nowUse = this.rawData.continuous;
        this.setDataset();
      } else {
        // console.log(this.rawData, 286);
        this.$http
          .get(config.HOST + config.API_URLS.online, {
            params: { byday: this.byDay ? 1 : 0 }
          })
          .then(res => {
            let raw = res.data.data;
            if (this.byDay) {
              // console.log("fetched,byday=true!");
              this.rawData.byDay = raw;
              this.rawData.nowUse = raw;
              this.setDataset();
            } else {
              // console.log("fetched,byday=false!");
              this.rawData.continuous = raw;
              this.rawData.nowUse = raw;
              this.setDataset();
            }
          });
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.sitedata-block {
  margin-top: 50px;
}
.desc{
  .b{
    font-weight: bold;
  }
  padding-left: 25px;
  // color: #AAA;
  font-size: 12px;
  line-height: 2em;
}
.chart {
  width: 100%;
  height: 400px;
  &.upload {
    width: 70%;
    float: left;
  }
  &.upload-pie {
    width: 29%;
    float: left;
  }
}
.sitedata-block {
  // border:1px solid #ddd;
  font-size: 12px;
  text-align: center;
}
.el-switch{
  margin-left: 25px;
}
</style>