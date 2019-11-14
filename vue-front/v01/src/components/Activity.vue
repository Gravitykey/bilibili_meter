<template>
  <div class="activity-wrapper">
    <h2>全站活跃度数据</h2>
    <div class="activity-block"></div>
    <div class="desc">
      <p class="b">数值说明</p>
      <p>数值单位：平均每小时活跃事件（包括弹幕，评论等）数量</p>
      <p>计算方式：当前时间点的值 = (当前时间点活跃累计量 - 前一时间点活跃累计量) / 间隔</p>
      <p>注：由于计算规则所致，第一个数据项值与第二个相同</p>
      <br>
      <p>在图表中使用鼠标滚轮或者拖拽下方滑块可缩放数据范围</p>
    </div>
    <div class="activity-block">
      <div class="chart continuous"></div>
      <div class="time">原始数据时间范围: {{tsToDateStr(c_dateBegin)}} 到 {{tsToDateStr(c_dateEnd)}}</div>
      <div class="clearfix"></div>
    </div>
    <div class="activity-block">
      <div class="chart byday"></div>
    </div>
    <div class="activity-block">
      <div class="chart byday-pie"></div>
      <div class="time">原始数据时间范围: {{tsToDateStr(byday_dateBegin)}} 到 {{tsToDateStr(byday_dateEnd)}}</div>
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
      c_dateBegin: 0,
      c_dateEnd: 0,
      byday_dateBegin: 0,
      byday_dateEnd: 0
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
      this.charts[c].clear();
      this.charts[c].dispose();
    }
  },
  methods: {
    tsToDateStr: chartDataProcess.tsToDateStr,
    initCharts() {
      this.rawData = {
        c: [],
        byday: []
      };

      // 初始化
      let el = document.querySelector(".activity-wrapper .chart.continuous");
      let op = onlineChartsOption.chartActivityContinuous;
      let el2 = document.querySelector(".activity-wrapper .chart.byday");
      let op2 = onlineChartsOption.chartActivityByday;
      let el3 = document.querySelector(".activity-wrapper .chart.byday-pie");
      let op3 = onlineChartsOption.activityBydayPie;

      //
      let chart1 = this.initEchart(el, op);
      let chart2 = this.initEchart(el2, op2);
      let chart3 = this.initEchart(el3, op3);
      this.charts = { chart1: chart1, chart2: chart2, chart3: chart3 };
      // 绑定回调
      let editPie = chartDataProcess.debounce((idx, chart) => {
        let pieData = chartDataProcess.makePieData(this.datasetByday, idx);
        chart.setOption({
          series: {
            type: "pie",
            id: "pie",
            name: "活跃比例" + pieData.time,
            data: pieData.data
          },
          title: {
            text: "活跃比例" + pieData.time
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
    },
    initEchart(el, option) {
      let myChart = this.$echarts.init(el);
      myChart.setOption(option);
      return myChart;
    },
    fetchData() {
      this.$http.get(config.HOST + config.API_URLS.activity).then(res => {
        let raw = { c: res.data.data.c, byday: res.data.data.byday };
        this.rawData = raw;
        this.setDataset();
      });
    },
    setDataset() {
      let datasetContinuous = chartDataProcess.makeActivityDataset(
        this.rawData.c
      );
      let datasetByday = chartDataProcess.makeActivityDataset(
        this.rawData.byday
      );
      let activitySeries = chartDataProcess.makeActivitySeries();
      // 单独留出来，供饼图使用
      this.datasetByday = datasetByday;
      this.charts.chart1.setOption({
        dataset: { source: datasetContinuous },
        series: activitySeries
      });
      this.charts.chart2.setOption({
        dataset: { source: datasetByday },
        series: activitySeries
      });

      // 原始数据时间范围处理
      if (this.rawData.c.length > 0) {
        this.c_dateBegin = this.rawData.c[0].time * 1000;
        this.c_dateEnd = this.rawData.c[this.rawData.c.length - 1].time * 1000;
      } else {
        this.c_dateBegin = 0;
        this.c_dateEnd = 0;
      }
      if (this.rawData.byday.length > 0) {
        this.byday_dateBegin = this.rawData.byday[0].time * 1000;
        this.byday_dateEnd =
          this.rawData.byday[this.rawData.byday.length - 1].time * 1000;
      } else {
        this.byday_dateBegin = 0;
        this.byday_dateEnd = 0;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.desc{
  .b{
    font-weight: bold;
  }
  padding-left: 25px;
  // color: #999;
  font-size: 12px;
  line-height: 2em;
}
.activity-block {
  margin-top: 50px;
}
.chart {
  width: 100%;
  height: 500px;
  &.byday {
    width: 70%;
    float: left;
  }
  &.byday-pie {
    width: 29%;
    float: left;
  }
}
.activity-block {
  // border:1px solid #ddd;
  font-size: 12px;
  text-align: center;
}
</style>