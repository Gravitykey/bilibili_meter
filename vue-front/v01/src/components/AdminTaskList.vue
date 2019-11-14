<template>
  <div class="tasklist">
    <div class="filter">
      <el-form :inline="true" :model="filter" class="form-inline">
        <el-form-item label="任务类型">
          <el-select v-model="filter.type" placeholder="请选择任务类型">
            <el-option label="不限" value="all"></el-option>
            <el-option label="全局在线" value="Online"></el-option>
            <el-option label="全局活跃" value="RegionActivity"></el-option>
            <el-option label="视频信息" value="VideoInfo"></el-option>
            <el-option label="视频状态" value="VideoStat"></el-option>
            <el-option label="UP主信息" value="UpInfo"></el-option>
            <el-option label="UP主状态" value="UpStat"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="筛选参数">
          <el-input v-model="filter.query" placeholder="参数包含的字符"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="filterlist">筛选</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="task-table">
      <el-table
        :data="filteredTasks.slice((pagi_current -1)*pagi_size,pagi_current*pagi_size)"
        style="width: 100%"
      >
        <!-- <el-table-column label="ID" width="180">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.id }}</span>
          </template>
        </el-table-column>-->
        <el-table-column label="类型" width="180">
          <template slot-scope="scope">
            <span class="color-block" :class="scope.row.type"></span>
            {{ lookUpType(scope.row.type) }}
          </template>
        </el-table-column>
        <el-table-column label="参数 (av/UID)" width="180">
          <template slot-scope="scope">{{ scope.row.param }}</template>
        </el-table-column>
        <el-table-column label="周期" width="180">
          <template slot-scope="scope">
            <el-input size="small" type="number" v-model="scope.row.period"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="相位" width="180">
          <template slot-scope="scope">
            <el-input size="small" type="number" v-model="scope.row.phase"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="启用" width="100">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.enable"></el-switch>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleSave(scope.$index, scope.row)">保存</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="pagination">
      <el-pagination
        :page-size="pagi_size"
        layout="prev, pager, next"
        :total="pagi_total"
        @current-change="onPageChange"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { lookUpType } from "../typedict.js";
import * as config from "../config.js";
export default {
  data() {
    return {
      filter: {
        type: "all",
        query: ""
      },
      pagi_total: 0,
      pagi_size: config.ADMIN_TASKLIST_PAGI_SIZE,
      pagi_current: 1,
      tasks: [],
      filteredTasks: []
    };
  },
  methods: {
    onPageChange(val) {
      this.pagi_current = val;
      //   this.filterlist();
    },
    handleSave(index, row) {
      let id = row.id;
      let period = row.period;
      let phase = row.phase;
      let enable = row.enable ? 1 : 0;
      // console.log(id, period, phase, enable);
      this.$http
        .get(config.HOST + config.API_URLS.task_update, {
          params: {
            id: id,
            period: period,
            phase: phase,
            enable: enable
          },
          withCredentials: true
        })
        .then(res => {
          if (res.data.status == "success") {
            this.$notify({
              title: "成功",
              message: "修改成功",
              type: "success"
            });
          } else {
            this.$notify({
              title: "出现问题",
              message: "出现问题：" + res.data.message,
              type: "warning"
            });
          }
        })
        .catch(error => {
          this.$notify.error({
            title: "警告",
            message: "与服务器的通信出现问题，请检查网络和服务器"
          });
        });
    },
    lookUpType,
    filterlist() {
      this.pagi_current = 1;
      let needType = this.filter.type;
      let query = this.filter.query;
      this.filteredTasks = this.tasks.filter(item => {
        return (
          (item.type == needType || needType == "all") &&
          item.param.toString().indexOf(query.toLowerCase()) !== -1
        );
      });
      this.pagi_total = this.filteredTasks.length;
    },
    fetch() {
      this.$http
        .get(config.HOST + config.API_URLS.task_list, {
          withCredentials: true
        })
        .then(res => {
          if (res.data.status == "success") {
            this.tasks = res.data.data;
            this.filterlist();
          } else {
            this.$notify({
              title: "出现问题",
              message: "出现问题：" + res.data.message,
              type: "warning"
            });
          }
        })
        .catch(error => {
          this.$notify.error({
            title: "警告",
            message: "与服务器的通信出现问题，请检查网络和服务器"
          });
        });
    }
  },
  mounted() {
    this.fetch();
  }
};
</script>

<style lang="scss" scoped>
.filter {
  text-align: center;
}
.pagination {
  text-align: center;
}
.task-table {
  span.color-block {
    display: inline-block;
    width: 22px;
    height: 10px;
    margin-right: 5px;
  }
  .el-input {
    width: 100px;
  }
  .Online {
    background: #d6d6d6;
  }
  .RegionActivity {
    background: #ffe9d5;
  }
  .UpInfo {
    background: #2ea037;
  }
  .UpStat {
    background: #a4e0a9;
  }
  .VideoInfo {
    background: #1980c5;
  }
  .VideoStat {
    background: #a4cde0;
  }
}
</style>