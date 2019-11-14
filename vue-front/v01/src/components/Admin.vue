<template>
  <div>
    <h2>管理</h2>
    <el-tabs @tab-click="handleClick" v-if="elementCreated" class="tabs" v-model="activeName">
      <el-tab-pane label="快速添加" name="fastadd">
        <vc-admin-fastaddtask></vc-admin-fastaddtask>
      </el-tab-pane>
      <el-tab-pane label="添加任务" name="add">
        <vc-admin-addtask></vc-admin-addtask>
      </el-tab-pane>
      <el-tab-pane label="任务管理" name="list">
        <vc-admin-tasklist  ref="tasklist"></vc-admin-tasklist>
      </el-tab-pane>
      <el-tab-pane label="错误日志" name="log">
        <vc-admin-faillog></vc-admin-faillog>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeName: "fastadd",
      elementCreated: false
    };
  },
  methods: {
    handleClick(tab, event) {
      if(tab.name=='list'){
        this.$refs.tasklist.fetch()
      }
    },
  },
  beforeMount() {
    let u = sessionStorage.getItem("username");
    if (!u) {
      this.$router.push({ path: "/login" });
    } else {
      this.elementCreated = true;
    }
  }
};
</script>

<style lang="scss" scoped>
.tabs {
  margin-top: 20px;
}
</style>