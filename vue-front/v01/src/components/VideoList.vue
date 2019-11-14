<template>
  <div>
    <h2>关注的视频列表</h2>
    <div class="desc">点击名称或者封面查看详细数据</div>
    <div class="query">
      <el-form ref="form" label-width="40px">
        <el-form-item label="筛选">
          <el-input v-model="query" placeholder="标题/AV号/分类/作者UID"></el-input>
        </el-form-item>
      </el-form>
    </div>
    <ul class="videolist">
      <li class="video-item" v-for="video in computedVideoList" :key="video.id">
        <el-card class="box-card">
          <router-link :to="'/videoinfo/'+video.id">
            <img :src="video.pic" class="pic" />
          </router-link>
          <div class="right">
            <div>
              <div class="title">
                <router-link class="title-link" :to="'/videoinfo/'+video.id">{{video.title}}</router-link>
                <div class="av">av : {{video.id}}</div>
                <div class="clearfix"></div>
              </div>
              <div class="in-line">
                <div class="tname atr">分类 : {{video.tname}}</div>
                <div class="owner_mid atr">UP主UID : <router-link class="title-link" :to="'/upinfo/'+video.owner_mid">{{video.owner_mid}}</router-link></div>
                <div class="pubdate atr">发布时间 : {{tsToDateStr(video.pubdate*1000)}}</div>
                <div class="clearfix"></div>
              </div>
            </div>
            <div class="desc">{{video.desc}}</div>
          </div>
          <div class="clearfix"></div>
        </el-card>
      </li>
    </ul>
  </div>
</template>

<script>
import {tsToDateStr} from '../utils.js'
import * as config from "../config.js";
export default {
  data() {
    return {
      query: "",
      videolist: [
//         {
//           id: 67590648,
//           owner_mid: 177291194,
//           tname: "VOCALOID·UTAU",
//           pic:
//             "http://i0.hdslb.com/bfs/archive/12e684f377e47674b9a3913661deb55fc81df447.jpg",
//           title: "DECO*27 - 新世界安内所 feat. 初音未来",
//           desc: `DECO*27 - 新世界安内所 feat. 初音未来

// Music: DECO*27
// Arrangement: Rockwell

// Movie by OTOIRO
// Director, Cinematographer &amp; Editor: Yuma Saito
// Animator: akka

// インスト: 

// OTOIRO Website
// http://otoiro.co.jp/
// インスト: 

// OTOIRO Website
// http://otoiro.co.jp/
// インスト: 

// OTOIRO Website
// http://otoiro.co.jp/`,
//           pubdate: 1568384113
//         },
//         {
//           id: 67590632,
//           owner_mid: 1772912494,
//           tname: "VOCALOID·UTAU",
//           pic:
//             "http://i0.hdslb.com/bfs/archive/12e684f377e47674b9a3913661deb55fc81df447.jpg",
//           title: "DECO*27 - 新世界安内实得分所 feat. 初音未来",
//           desc: `DECO*27 - 新啊啊啊啊啊世界安内实得分所 feat. 初音未来

// Music: DECO*27
// Arrangement: Rockwell

// Movie by OTOIRO
// Director, Cinematographer &amp; Editor: Yuma Saito放屁
// Animator: akka

// インスト: 

// OTOIRO Website
// http://otoiro.co.jp/
// インスト: 

// OTOIRO Website
// http://otoiro.co.jp/
// インスト: 

// OTOIRO Website
// http://otoiro.co.jp/`,
//           pubdate: 1568384113
//         }
      ]
    };
  },
  computed: {
    computedVideoList: function() {
      let vm = this;
      return this.videolist.filter(function(item) {
        return (
          item.title.toLowerCase().indexOf(vm.query.toLowerCase()) !== -1 ||
          item.id.toString().indexOf(vm.query.toLowerCase()) !== -1 ||
          item.owner_mid.toString().indexOf(vm.query.toLowerCase()) !== -1 ||
          item.tname.toLowerCase().indexOf(vm.query.toLowerCase()) !== -1 ||
          item.desc.toLowerCase().indexOf(vm.query.toLowerCase()) !== -1
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
    tsToDateStr:tsToDateStr,
    fetchData() {
      this.$http.get(config.HOST + config.API_URLS.video_list).then(res => {
        // console.log(res)
        this.videolist = res.data
      });
    },
  }
};
</script>

<style lang='scss' scoped>
.desc {
  // height: 48px;
  // overflow: hidden;
  // float:none;
  font-size: 12px;
  color: #999;
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
.video-item {
  margin-top: 20px;
  font-size: 12px;
  img {
    float: left;
    margin-left: 5px;
    height: 100px;
    width: 160px;
    border-radius: 4px;
    border: 1px solid #8fc1f3;
  }
  .right {
    margin-left: 20px;
    width: 650px;
    float: left;
  }
  .title {
    width: 100%;
    font-size: 14px;
    float: left;
    .title-link {
      float: left;
      text-decoration: none;
      font-weight: bold;
      color: #80a9d3;
      transition: 0.15s ease-out;
      &:hover {
        color: #409eff;
      }
    }
    .av {
      float: left;
      margin-left: 30px;
    }
  }
  .in-line {
    float: none;
    .atr{
      float: left;
      margin-right: 40px;
    }
  }

}
</style>