<template>
  <div class="status-wrapper">
    <h2>运行状态</h2>

    <div class="line">
      <el-card class="box-card">
        <div class="t">总共关注用户数</div>
        <div class="v">{{stat.total_user}}</div>
      </el-card>
      <el-card class="box-card">
        <div class="t">总关注视频数</div>
        <div class="v">{{stat.total_video}}</div>
      </el-card>
      <el-card class="box-card">
        <div class="t">今日worker累计提交</div>
        <div class="v">{{stat.today_submit}}</div>
      </el-card>
      <el-card class="box-card">
        <div class="t">当前活动task数</div>
        <div class="v">{{stat.total_enabled_task}}</div>
      </el-card>
      <el-card class="box-card">
        <div class="t">今日任务报错数</div>
        <div class="v">{{stat.today_task_failed}}</div>
      </el-card>
      <div class="clearfix"></div>
    </div>
    <h3>今日活动的worker</h3>

    <div class="workers-table">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="worker_name" label="名称" width="220"></el-table-column>
        <el-table-column prop="last_sub_time" label="最近提交时间" width="260"></el-table-column>
        <el-table-column prop="last_query_time" label="最近轮询时间" width="260"></el-table-column>
        <el-table-column prop="day_submit_count" label="今日总提交"></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import * as config from "../config.js";
import {tsToDateStr} from "../utils.js"
export default {
  data() {
    return {
      tableData: [
        {
          worker_name: "暂无数据",
          last_sub_time: "暂无数据",
          last_query_time: "暂无数据",
          day_submit_count: 0
        }
      ],
      stat: {
        today_submit: "载入中",
        today_task_failed: "载入中",
        total_enabled_task: "载入中",
        total_user: "载入中",
        total_video: "载入中"
      }
    };
  },
  mounted() {
    this.$nextTick(()=>{
      this.fetchData();
    })
  },
  methods: {
    fetchData: function() {
      // console.log("fetch~~~");
      this.$http.get(config.HOST + config.API_URLS.running_stat).then(res => {
        // console.log(res);
        let d = res.data
        for(var key in this.stat){
          this.stat[key]=d[key]
        }
        let wStat = res.data.workers_stat
        wStat.forEach(item=>{
          item.last_sub_time = tsToDateStr(item.last_sub_time*1000)
          item.last_query_time = tsToDateStr(item.last_query_time*1000)
        })
        this.tableData = wStat
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.status-wrapper {
  // background:#888;
  font-size: 14px;
}
.line {
  margin-top: 20px;
  margin-bottom: 30px;
  .box-card {
    margin-top: 20px;
    margin-right: 50px;
    width: 250px;
    height: 150px;
    float: left;
    .t {
      font-size: 16px;
      color: #888;
    }
    .v {
      margin-top: 55px;
      font-size: 30px;
      // font-weight: bold;
      text-align: right;
      color: #67a1db;
    }
  }
}
h2 {
  font-size: 18px;
  font-weight: bold;
}
h3 {
  font-size: 18px;
}
.workers-table {
  margin-top: 10px;
}
</style>