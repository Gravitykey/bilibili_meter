<template>
  <div>
    <h2>关注的UP</h2>
    <div class="desc">点击头像或用户名查看详细数据</div>
    <div class="query">
      <el-form ref="form" label-width="40px">
        <el-form-item label="筛选">
          <el-input v-model="query" placeholder="输入用户名或者UID包含的字符"></el-input>
        </el-form-item>
      </el-form>
    </div>
    <ul class="uplist">
      <li class="up-item" v-for="up in computedUpList" :key="up.id">
        <el-card class="box-card">
          <router-link :to="'/upinfo/'+up.id">
            <img :src="up.face" class="face" />
          </router-link>
          <div class="right">
            <div>
              <div class="name">
                <router-link class="name-link" :to="'/upinfo/'+up.id">{{up.name}}</router-link>
              </div>
              <div class="uid">UID : {{up.id}}</div>
              <div class="sex">性别 : {{up.sex}}</div>
            </div>
            <div class="sign">{{up.sign}}</div>
          </div>
          <div class="clearfix"></div>
        </el-card>
      </li>
    </ul>
  </div>
</template>

<script>
import * as config from "../config.js";
export default {
  data() {
    return {
      query: "",
      uplist: [
        // {
        //   face:
        //     "http://i2.hdslb.com/bfs/face/99fb31ee22f627b2e93b31cc8a80ac8d121290b1.jpg",
        //   sign: "我爱火锅!!!!!!!!",
        //   name: "DECO27_Official",
        //   id: 177291194,
        //   sex: "保密"
        // },
        // {
        //   face:
        //     "http://i2.hdslb.com/bfs/face/99fb31ee22f627b2e93b31cc8a80ac8d121290b1.jpg",
        //   sign: "我爱火锅!!!!!!!!",
        //   name: "DECO28_Official",
        //   id: 177291193,
        //   sex: "保密"
        // }
      ]
    };
  },
  computed: {
    computedUpList: function() {
      let vm = this;
      return this.uplist.filter(function(item) {
        return (
          item.name.toLowerCase().indexOf(vm.query.toLowerCase()) !== -1 ||
          item.id.toString().indexOf(vm.query.toLowerCase()) !== -1
        );
      });
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.fetchData();
    });
  },
  methods:{
    fetchData() {
      this.$http.get(config.HOST + config.API_URLS.up_list).then(res => {
        // console.log(res)
        this.uplist = res.data
      });
    },
  }
};
</script>

<style lang='scss' scoped>
.desc{
    font-size: 12px;
    color:#999;
}
.uplist {
  margin-top: 30px;
  &li {
    margin-top: 20px;
  }
}
.query {
  width: 500px;
  margin: 20px auto 20px auto;
}
.up-item {
  margin-top: 20px;
  font-size: 12px;
  img {
    float: left;
    margin-left: 20px;
    height: 60px;
    width: 60px;
    border-radius: 10%;
    border: 1px solid #8fc1f3;
  }
  .right {
    margin-left: 20px;
    float: left;
  }
  .name {
    width: 200px;
    font-size: 14px;
    float: left;
    .name-link {
      text-decoration: none;
      font-weight: bold;
      color: #80a9d3;
      transition: 0.15s ease-out;
      &:hover {
        color: #409eff;
      }
    }
  }
  .sex {
    float: left;
    margin-left: 30px;
  }
  .uid {
    float: left;
    margin-left: 30px;
  }
}
</style>