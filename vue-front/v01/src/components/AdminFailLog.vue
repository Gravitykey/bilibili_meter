<template>
  <div class="faillog">
    <div class="desc">最近300条失败记录</div>
    <el-table :data="tableData" style="width: 100%">
      <el-table-column prop="fail_time" label="日期" width="240"></el-table-column>
      <el-table-column prop="fail_type" label="类型" width="180"></el-table-column>
      <el-table-column prop="task_id" label="任务ID" ></el-table-column>
      <el-table-column prop="worker" label="WORKER名称" width="180"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import * as config from "../config.js";
import {tsToDateStr}from '../utils';
export default {
  data() {
    return {
      tableData: []
    };
  },
  methods: {
    fetchData() {
      this.$http
        .get(config.HOST + config.API_URLS.task_get_fail_log, {
          withCredentials: true
        })
        .then(res => {
            res.data.data.forEach(item => {
                item.fail_time = tsToDateStr(item.fail_time*1000)
            });
          this.tableData = res.data.data;
        })
        .catch(error => {
          this.$notify.error({
            title: "警告",
            message: "通信出现问题，请检查服务器状态和网络状态"
          });
        });
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style lang='scss' scoped>
.desc {
  font-size: 14px;
  padding: 10px;
}
</style>