<template>
  <div class="add-task">
    <div class="notice">
      <h3>任务类型说明：</h3>

      <p class="line">
        <span>全局在线</span>：全局唯一任务，统计网站在线人数和播放数，投稿量
      </p>
      <p class="line">
        <span>全局活跃</span>：全局唯一任务，统计网站各分区的弹幕/评论数据
      </p>
      <p class="line">———— 上面这两项只需添加一次 ————</p>
      <p class="line">
        <span>视频信息</span>：想要观察的视频，包括标题，描述，作者，分区，等
      </p>
      <p class="line">
        <span>视频状态</span>：视频实时的播放量，评论，投币，转发等
      </p>
      <p class="line">
        <span>UP主信息</span>：想要观察的UP主，采集头像，昵称，描述等等
      </p>
      <p class="line">
        <span>UP主状态</span>：UP主实时的粉丝数，总播放量等
      </p>
      <br />
      <h3>选项说明:</h3>

      <p class="line">
        <span>参数</span>：此处填任务类型的UID/AV号，全局任务填0即可
      </p>
      <p class="line">
        <span>周期</span>：数据采集间隔，即多长时间爬取一次数据。全局建议填1800秒，视频信息和UP主信息建议填43200（12小时），UP主状态建议填14400（4小时），视频状态根据实际情况填写，比如极热门视频可以填600（10分钟），冷门可以填14400（4小时）
      </p>
      <p class="line">
        <span>相位</span>：在当前周期中的第XX秒激活任务，比如全站投稿数据在每日零点会清零，可以把相位设置到1700来获取更加准确的每日投稿数。如果添加任务较多，可以分散不同任务的相位数值，保证请求不会扎堆，防止被反爬
      </p>
    </div>
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="任务类型">
        <el-select v-model="form.type" placeholder="请选择任务类型">
          <el-option label="全局在线" value="Online"></el-option>
          <el-option label="全局活跃" value="RegionActivity"></el-option>
          <el-option label="视频信息" value="VideoInfo"></el-option>
          <el-option label="视频状态" value="VideoStat"></el-option>
          <el-option label="UP主信息" value="UpInfo"></el-option>
          <el-option label="UP主状态" value="UpStat"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="任务设置">
        <el-col :span="8">
          <el-input placeholder="参数(UID或者AV号，纯数字)" v-model="form.param" style="width: 90%;"></el-input>
        </el-col>

        <el-col :span="8">
          <el-input placeholder="执行间隔周期(秒)" v-model="form.period" style="width: 90%;"></el-input>
        </el-col>
        <el-col :span="8">
          <el-input placeholder="相位(秒)" v-model="form.phase" style="width: 90%;"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">立即创建</el-button>
        <el-button>取消</el-button>
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
        type: "",
        param: "",
        period: "",
        phase: ""
      }
    };
  },
  methods: {
    onSubmit() {
      if (this.form.type && this.form.param && this.form.period) {
        this.$http
          .get(config.HOST + config.API_URLS.task_add, {
            params: {
              type: this.form.type,
              param: this.form.param,
              period: this.form.period,
              phase: this.form.phase
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
            }else{
              this.$notify({
                title: "出现问题",
                message: "出现问题："+res.data.message,
                type: "warning"
              });
            }
          }).catch(error=>{
            this.$notify.error({
                title: "警告",
                message: "与服务器的通信出现问题，请检查网络和服务器",
              });
          });
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