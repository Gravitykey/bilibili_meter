let typedict = {
    Online: "全局在线",
    RegionActivity: "全局活跃",
    VideoInfo: "视频信息",
    VideoStat: "视频状态",
    UpInfo: "UP主信息",
    UpStat: "UP主状态"
};

function lookUpType (s){
    return typedict[s]
}
export {lookUpType};