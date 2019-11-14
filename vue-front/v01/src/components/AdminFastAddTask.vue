<template>
  <div class="fast-add-task">
    <div class="notice">
      <h3>快速添加说明：</h3>

      <p class="line">快速添加，会自动添加一组 【视频信息+视频状态】 或者 【UP主信息+UP主状态】</p>
      <p class="line">且参数固定为 视频信息/UP主信息：12小时，视频状态/UP主状态: 4小时</p>
      <p class="line">相位会随机产生，避免请求扎堆。</p>
      <p class="line">如果相应任务已原本存在，周期和相位会改为上述状态</p>
      <br />
      <p class="line">
        <span>使用说明</span>：参数填写av开头，为添加视频相关，以u开头为UP主相关
      </p>
      <h3>其它:</h3>
      <p class="line">更详细的任务添加请使用“添加任务”选项卡</p>
    </div>
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="快速添加">
        <el-col :span="9">
          <el-input placeholder="参数(UID或者AV号，以u或者av开头)" v-model="form.param" style="width: 90%;"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="fastadd">快速添加</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import * as config from "../config.js";
export default {
  data() {
    return {
      form: {
        param: ""
      }
    };
  },
  methods: {
    submit(type, param, period, phase) {
      this.$http
        .get(config.HOST + config.API_URLS.task_add, {
          params: {
            type: type,
            param: param,
            period: period,
            phase: phase
          },
          withCredentials: true
        })
        .then(res => {
          if (res.data.status == "success") {
            this.$notify({
              title: "成功",
              message: "添加任务成功",
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
    fastadd() {
      let INFO_PERIOD = 43200;
      let STAT_PERIOD = 14400;
      let RANDOM_PHASE = Math.floor(Math.random() * STAT_PERIOD);
      let userReg = /u([0-9]+)/i;
      let videoReg = /av([0-9]+)/i;
      let rawParam = this.form.param;
      let type = null;
      let param = null;
      if (rawParam.match(userReg)) {
        type = "USER";
        param = RegExp.$1;
      } else if (rawParam.match(videoReg)) {
        type = "VIDEO";
        param = RegExp.$1;
      }
      if (type == null) {
        this.$notify.error({
          title: "警告",
          message: "参数格式不正确！"
        });
        return;
      }

      // 拿随机数，调接口

      if (type == "VIDEO") {
        this.submit("VideoInfo", param, INFO_PERIOD, RANDOM_PHASE);
        setTimeout(() => {
          this.submit("VideoStat", param, STAT_PERIOD, RANDOM_PHASE);
        }, 100);
      } else if (type == "USER") {
        this.submit("UpInfo", param, INFO_PERIOD, RANDOM_PHASE);
        setTimeout(() => {
          this.submit("UpStat", param, STAT_PERIOD, RANDOM_PHASE);
        }, 100);
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.notice {
  font-size: 14px;
  line-height: 2em;
  margin-top: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f6f6f6;
  .line {
    padding-left: 20px;
  }
  span {
    font-weight: bold;
    color: #6c8db3;
  }
  h3 {
    font-size: 14px;
    font-weight: bold;
  }
}
</style>