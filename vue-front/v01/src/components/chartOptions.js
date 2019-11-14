let onlineChartsOption = {
    chartOnline: {
        title: {
            text: "在线人数统计"
        },
        dataZoom: [
            {
                show: true,
                realtime: true,
                // start: 20,
                // end: 100
            },
            {
                type: "inside",
                realtime: true,
                // start: 20,
                // end: 100
            }
        ],
        tooltip: { trigger: "axis" },
        legend: {
            top: '7%',
            width: '95%',
        },
        // dataset: {

        //     source: {}
        // },
        grid: {
            // top: '20%',
            // left: '8%',
            // right: '10%',
            bottom: '18%',
        },
        xAxis:
            { type: 'time' },

        yAxis: [{ name: "人数", scale: true, }],
        series: [{
            name: '在线人数',
            type: 'line',
            encode: {
                y: 'webOnline',
            },
        },
        {
            name: '在线播放数',
            type: 'line',
            encode: {
                y: 'playOnline',
            },
        },
        ]
    },
    chartCount: {
        title: {
            text: "投稿量（每日0点置零）"
        },
        // dataset: {
        //     source: {}
        // },
        dataZoom: [
            {
                show: true,
                realtime: true,
                // start: 20,
                // end: 100
            },
            {
                type: "inside",
                realtime: true,
                start: 20,
                end: 100
            }
        ],
        grid: {
            top: '23%',
            bottom: '18%',
        },
        tooltip: { trigger: "axis" },
        legend: {
            top: '10%',
            width: '95%',
        },
        xAxis: {
            type: 'time'
        },
        yAxis: [{ scale: true }],
        // series: countSeries,
    },
    countPie: {
        title: {
            text: "投稿构成"
        },
        tooltip: {
            trigger: "item",
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            bottom: 0,
        },
        series: [
            {
                id: 'pie',
                name: "投稿构成",
                type: "pie",
                radius: ["50%", "70%"],
                center: ["50%", "40%"],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: "center",
                    },
                    emphasis: {
                        show: true,
                        formatter: '{b}: {d}%\n值：{c}',
                        textStyle: {
                            fontSize: "18",
                            fontWeight: "bold"
                        }
                    },
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },

                data: [
                    { name: "1", value: 2430 },
                ]
            }
        ]
    },
    chartActivityContinuous: {
        title: {
            text: "活跃度(连续)"
        },
        dataZoom: [
            {
                show: true,
                realtime: true,
            },
            {
                type: "inside",
                realtime: true,
            }
        ],
        tooltip: { trigger: "axis" },
        legend: {
            top: '10%',
            width: '95%',
        },
        // dataset: {
        //     source: datasetContinuous
        // },
        grid: {
            top: '23%',
            // left: '8%',
            // right: '10%',
            bottom: '18%',
        },
        xAxis:
            { type: 'time' },

        yAxis: [{ scale: true, }],
        // series: activitySeries
    },
    chartActivityByday: {
        title: {
            text: "活跃度(每日平均)"
        },
        // dataset: {
        //     source: datasetByday
        // },
        dataZoom: [
            {
                show: true,
                realtime: true,
                // start: 20,
                // end: 100
            },
            {
                type: "inside",
                realtime: true,
                // start: 20,
                // end: 100
            }
        ],
        grid: {
            top: '23%',
            bottom: '18%',
        },
        tooltip: { trigger: "axis" },
        legend: {
            top: '10%',
            width: '95%',
        },
        xAxis: {
            type: 'time'
        },
        yAxis: [{ scale: true }],
        // series: activitySeries,
    },
    activityBydayPie: {
        title: {
            text: "活跃构成"
        },
        tooltip: {
            trigger: "item",
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            bottom: 0,
        },
        series: [
            {
                id: 'pie',
                name: "活跃构成",
                type: "pie",
                radius: ["50%", "80%"],
                center: ["50%", "40%"],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: "center",
                    },
                    emphasis: {
                        show: true,
                        formatter: '{b}: {d}%\n值：{c}',
                        textStyle: {
                            fontSize: "18",
                            fontWeight: "bold"
                        }
                    },
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },

                data: [
                    { name: "1", value: 2430 },
                ]
            }
        ]
    }
}

let upInfoChartOption = {
    title: {
        text: "播放趋势以及粉丝趋势"
    },
    dataZoom: [
        {
            show: true,
            realtime: true,
            // start: 0,
            // end: 100
        },
        {
            type: "inside",
            realtime: true,
            // start: 0,
            // end: 100
        }
    ],
    dataset: {
        source: [],
        dimensions: [
            { name: "time", type: "time" },
            { name: "d_follower" },
            { name: "d_total_video_view" },
        ]
    },
    tooltip: { trigger: "axis" },
    legend: {
        data: ["总播放数", "粉丝数"]
    },
    xAxis: {
        type: 'time'
    },
    yAxis: [{ scale: true, name: '播放数' }, { scale: true, name: '粉丝数' }],
    series: [
        {
            name: "总播放数",
            type: "line",
            encode: {
                x: 'time',
                y: 'd_total_video_view'
            }
        },
        {
            name: "粉丝数",
            type: "line",
            yAxisIndex: 1,
            encode: {
                x: 'time',
                y: 'd_follower'
            }
        }
    ]
}

let videoInfoChartOption = {
    title: {
        text: "视频信息统计"
    },
    dataZoom: [
        {
            show: true,
            realtime: true,
            // start: 0,
            // end: 100
        },
        {
            type: "inside",
            realtime: true,
            // start: 20,
            // end: 100
        }
    ],
    grid: {
        top: "20%",
        left: "8%",
        right: "5%",
        bottom: "16%",
    },
    tooltip: { trigger: "axis" },
    legend: {
        x: "right"
    },
    dataset: {
        dimensions: [
            { name: 'time', type: 'time' },
            { name: 'd_view' },
            { name: 'd_share' },
            { name: 'd_reply' },
            { name: 'd_like' },
            { name: 'd_favorite' },
            { name: 'd_danmaku' },
            { name: 'd_coin' },
        ],
        source: []
    },
    xAxis: { type: 'time' },
    yAxis: [{ name: "播放数" }, { name: "其它项" }],
    series: [
        {
            name: "播放",
            type: "line",
            encode: {
                x: 'time',
                y: 'd_view'
            }
        },
        {
            name: "弹幕",
            type: "line",
            encode: {
                x: 'time',
                y: 'd_danmaku'
            },
            yAxisIndex: 1
        },
        {
            name: "评论",
            type: "line",
            encode: {
                x: 'time',
                y: 'd_reply'
            },
            yAxisIndex: 1
        },
        {
            name: "投币",
            type: "line",
            encode: {
                x: 'time',
                y: 'd_coin'
            },
            yAxisIndex: 1
        },
        {
            name: "转发",
            type: "line",
            encode: {
                x: 'time',
                y: 'd_share'
            },
            yAxisIndex: 1
        }, {
            name: "点赞",
            type: "line",
            encode: {
                x: 'time',
                y: 'd_like'
            },
            yAxisIndex: 1
        },
        {
            name: "收藏",
            type: "line",
            encode: {
                x: 'time',
                y: 'd_favorite'
            },
            yAxisIndex: 1
        }
    ]
}

export { onlineChartsOption, upInfoChartOption, videoInfoChartOption }