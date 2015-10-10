'use strict';

var App = App || {};

// user
App.page.login = function (module) {
  module.login();
};

App.page.settings = function (module) {
  module.settings();
};

App.page.user = function (module) {
  module.admin();
  module.register();
};

// util
App.page.dashboard = function (module, path) {
  $('.info-box-content').each(function (index, element) {
    var infoBoxNumber = $(element).find('.info-box-number'),
        progressBar = $(element).find('.progress-bar'),
        progressDescription = $(element).find('.progress-description'),

        duration = 2000,
        refreshInterval = 100,
        loop = Math.floor(duration / refreshInterval),
        loopCount = 0,

        numberValue = 0,
        numberFinal = $(element).data('number'),
        numberIncrement = numberFinal / loop,

        percentValue = 0,
        percentFinal = $(element).data('percent'),
        percentIncrement = percentFinal / loop,

        render = function (numberValue, percentValue) {
          infoBoxNumber.text(numberValue);
          progressBar.width(percentValue + '%');
          progressDescription.text('占总数据 ' + percentValue + '%');
        },

        increaseTo = function () {
          if (loopCount < loop) {
            numberValue += numberIncrement;
            percentValue += percentIncrement;
            render(numberValue.toFixed(), percentValue.toFixed());

            loopCount++;
            setTimeout(increaseTo, refreshInterval);
          } else {
            numberValue = numberFinal;
            percentValue = percentFinal;
            render(numberValue, percentValue);
          }
        };

    setTimeout(increaseTo, refreshInterval);
  });

  module.abstract({
    feature: 'risk',
    container: '#risk > tbody',
    render: function (container, content) {
      $('<tbody/>')
        .html(content)
        .showRisk()
        .replaceAll($(container));
    }
  });

  module.inspection();

  module.abstract({
    feature: 'news',
    container: '#news'
  });

  module.abstract({
    feature: 'event',
    container: '#event'
  });

  module.abstract({
    feature: 'weixin',
    container: '#weixin',
    render: function (container, content) {
      $(container).html(content);
    }
  });

  module.abstract({
    feature: 'weibo',
    container: '#weibo',
    render: function (container, content) {
      $(container).html(content);
    }
  });

  module.line(path);
  module.pie(path);
};

App.page.news = function (module) {
  module.list({
    feature: 'news',
    container: '#news > tbody'
  });
};

App.page.newsDetail = function (module, path, type, id) {
  module.collect(type, id);
};

App.page.event = function (module) {
  module.list({
    feature: 'event',
    container: '#event > tbody'
  });
};

App.page.eventDetail = function (module, path, type, id) {
  module.collect(type, id);
  module.line(path, type);
  module.pie(path, type);

  module.detail({
    path: path,
    feature: 'news',
    container: '#news > tbody'
  });

  module.detail({
    path: path,
    feature: 'weixin',
    container: '#weixin'
  });

  module.detail({
    path: path,
    feature: 'weibo',
    container: '#weibo'
  });
};

App.page.weixin = function (module) {
  module.list({
    feature: 'weixin',
    filter: {
      sort: 'new'
    },
    container: '#weixin-new',
    visiblePages: 3
  });

  module.list({
    feature: 'weixin',
    filter: {
      sort: 'hot'
    },
    container: '#weixin-hot',
    visiblePages: 3
  });
};

App.page.weixinDetail = function () {
  // placeholder for future usage
};

App.page.weibo = function (module) {
  module.list({
    feature: 'weibo',
    filter: {
      sort: 'new'
    },
    container: '#weibo-new',
    visiblePages: 3
  });

  module.list({
    feature: 'weibo',
    filter: {
      sort: 'hot'
    },
    container: '#weibo-hot',
    visiblePages: 3
  });
};

App.page.categoryDetail = function (module, path) {
  module.detail({
    path: path,
    feature: 'news',
    container: '#news > tbody'
  });
};

App.page.locationDetail = function (module, path) {
  module.detail({
    path: path,
    feature: 'news',
    container: '#news > tbody'
  });

  module.detail({
    path: path,
    feature: 'weixin',
    container: '#weixin'
  });

  module.detail({
    path: path,
    feature: 'weibo',
    container: '#weibo'
  });
};

App.page.inspection = function (module, path) {
  module.dataTable(path);
};

App.page.custom = function () {
  var form     = document.forms.addKeyword,
      action   = form.action,
      elements = form.elements,
      fieldset = elements[0],
      keyword  = elements[1],
      button   = elements[2],
      $msg     = $(form).prev(),
      $list    = $(form).parent().prev().find('li'),

      enableSubmit = function () {
        button.disabled = !(keyword.value);
      },

      processAdd = function (event) {
        event.preventDefault();

        $.post(action, $(form).serialize(), function (response) {
          if (response.status) {
            $msg.text('关键词添加成功！').show();
            location.reload();
          } else {
            $msg.text('关键词添加失败！').show();
            keyword.value = '';
          }
        });
      };

  if ($list.length >= 5) {
    fieldset.disabled = true;
  } else {
    $(form).keyup(enableSubmit).submit(processAdd);
  }
};

App.page.customDetail = function (module, path) {
  module.detail({
    path: path,
    feature: 'news',
    container: '#news > tbody'
  });

  module.detail({
    path: path,
    feature: 'weixin',
    container: '#weixin'
  });

  module.detail({
    path: path,
    feature: 'weibo',
    container: '#weibo'
  });
};

App.page.collection = function (module, path) {
  module.detail({
    path: path,
    feature: 'news',
    container: '#news > tbody'
  });

  module.detail({
    path: path,
    feature: 'event',
    container: '#event > tbody'
  });
};

App.page.risk = function (module) {
  module.list({
    feature: 'risk',
    container: '#risk > tbody',
    render: function (container, content) {
      $('<tbody/>')
        .html(content)
        .showRisk()
        .replaceAll($(container));
    }
  });
};

App.page.riskDetail = function (module, path, type, id) {
  module.collect(type, id);
  module.line(path, type);
  module.pie(path, type);

  module.detail({
    path: path,
    feature: 'news',
    container: '#news > tbody'
  });

  module.detail({
    path: path,
    feature: 'weixin',
    container: '#weixin'
  });

  module.detail({
    path: path,
    feature: 'weibo',
    container: '#weibo'
  });
};

App.page.analyticsDetail = function (module, path) {
  var api = '/api' + path,
      $dateRange = $('.date-range-picker'),
      $chart = $('#chart'),
      $statistic = $('#statistic'),
      start = moment().subtract(6, 'days').format(),
      end = moment().format();

  // init analytics
  module.dateRange($dateRange);
  $dateRange.trigger('show.dateRange', [start, end]);

  $chart.on('show.chart', function (event, start, end) {
    var chart = {},
      name = $(this).find('.tab-pane.active')[0].id.slice(6),

      excel = function (type) {
        var myTool = {
          show: true,
          title: '保存为Excel',
          icon: 'image://../../static/img/excel.png',

          onclick: function () {
            document.getElementById('save-as-excel').src = api + '?type='+type+'&start=' + start + '&end=' + end + '&datatype=xls';
          }
        };
        return myTool;
       };

    chart.trend = function (start, end) {
      $.getJSON(api, {
        type: 'chart-trend',
        start: start,
        end: end
      }, function (data) {
        echarts.init(document.getElementById('chart-trend'), 'macarons').setOption({
          tooltip: {
            backgroundColor: 'rgba(50,50,50,0.5)',
            trigger: 'axis',
            axisPointer: {
              type: 'line',
              lineStyle: {
                color: '#008acd',
              }
            }
          },
          shadowStyle: {
            color: 'rgba(200,200,200,0.2)'
          },
          legend: {
            data: ['全部', '新闻', '微博', '微信']
          },
          grid: {
            x: 50,
            y: 30,
            x2: 25,
            y2: 65
          },
          toolbox: {
            show: true,
            feature: {
              myTool: excel('chart-trend') ,
              saveAsImage: {
                show: true
              }
            }
          },
          calculable: true,
          xAxis: [{
            type: 'category',
            boundaryGap: false,
            data: data.date
          }],
          yAxis: [{
            type: 'value'
          }],
          series: [{
            name: '全部',
            type: 'line',
            data: data.total
          }, {
            name: '新闻',
            type: 'line',
            data: data.news
          }, {
            name: '微博',
            type: 'line',
            data: data.weibo
          }, {
            name: '微信',
            type: 'line',
            data: data.weixin
          }, ]
        });
      });
    };

    chart.type = function (start, end) {
      $.getJSON(api, {
        type: 'chart-type',
        start: start,
        end: end
      }, function (data) {
        echarts.init(document.getElementById('chart-type'), 'macarons').setOption({
          tooltip: {
            backgroundColor: 'rgba(50,50,50,0.5)',
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            x: 'left',
            y: 'bottom',
            data: ['新闻', '微博', '微信']
          },
          toolbox: {
            show: true,
            feature: {
              myTool: excel('chart-type'),
              saveAsImage: {
                show: true,
              }
            }
          },
          calculable: true,
          series: [{
            name: '访问来源',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [{
              value: data.news,
              name: '新闻'
            }, {
              value: data.weibo,
              name: '微博'
            }, {
              value: data.weixin,
              name: '微信'
            }]
          }]
        });
      });
    };

    chart.emotion = function (start, end) {
      $.getJSON(api, {
        type: 'chart-emotion',
        start: start,
        end: end
      }, function (data) {
        echarts.init(document.getElementById('chart-emotion'), 'macarons').setOption({
          tooltip: {
            backgroundColor: 'rgba(50,50,50,0.5)',
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            x: 'left',
            y: 'bottom',
            data: ['正面', '中性', '负面']
          },
          toolbox: {
            show: true,
            feature: {
              mark: {
                show: false
              },
              myTool: excel('chart-emotion'),
              magicType: {
                show: false,
                type: ['pie'],
                option: {
                  funnel: {
                    x: '25%',
                    width: '50%',
                    funnelAlign: 'left',
                    max: 2000
                  }
                }
              },
              restore: {
                show: false
              },
              saveAsImage: {
                show: true
              }
            }
          },
          calculable: true,
          series: [{
            name: '访问来源',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [{
              value: data.positive,
              name: '正面'
            }, {
              value: data.normal,
              name: '中性'
            }, {
              value: data.negative,
              name: '负面'
            }]
          }]
        });
      });
    };

    chart.weibo = function (start, end) {
      $.getJSON(api, {
        type: 'chart-weibo',
        start: start,
        end: end
      }, function (data) {
        echarts.init(document.getElementById('chart-weibo-map'), 'macarons').setOption({
          tooltip: {
            trigger: 'item'
          },
          legend: {
            show: false,
            orient: 'vertical',
            x: 'left',
            data: ['微博文']
          },
          dataRange: {
            min: 0,
            max: data.value[9],
            x: 'left',
            y: 'bottom',
            text: ['高', '低'],
            calculable: true
          },
          toolbox: {
            show: true,
            orient: 'horizontal',
            x: 'left',
            y: 'top',
            feature: {
              myTool: excel('chart-weibo'),
              saveAsImage: {
                show: true
              }
            }
          },
          roamController: {
            show: true,
            x: '85%',
            mapTypeControl: {
              'china': true
            }
          },
          series: [{
            name: '微博文',
            type: 'map',
            mapType: 'china',
            roam: false,
            itemStyle: {
              normal: {
                label: {
                  show: true
                }
              },
              emphasis: {
                label: {
                  show: true
                }
              }
            },
            data: data.province
          }, ]
        });

        echarts.init(document.getElementById('chart-weibo-bar'), 'macarons').setOption({
          title: {
            text: '微博地域分析',
            x: 45
          },
          tooltip: {
            show: false,
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            show: false,
            data: ['微博文']
          },
          toolbox: {
            show: false,
            feature: {
              mark: {
                show: true
              },
              magicType: {
                show: true,
                type: ['line', 'bar', 'stack', 'tiled']
              },
              restore: {
                show: true
              },
              saveAsImage: {
                show: true
              }
            }
          },
          calculable: false,
          grid: {
            borderWidth: 0
          },
          xAxis: [{
            show: false,
            type: 'value'
          }],
          yAxis: [{
            show: true,
            axisLine: false,
            axisTick: false,
            type: 'category',
            splitLine: false,
            splitArea: {
              show: false
            },
            axisLabel: {
              show: true,
              textStyle: {
                fontSize: 14,
                fontWeight: 'bolder'
              }
            },
            data: data.name
          }],
          series: [{
            name: '微博文',
            type: 'bar',
            stack: '总量',
            barWidth: 20,
            itemStyle: {
              normal: {
                label: {
                  show: true,
                  textStyle: {
                    color: '#000000',
                    fontSize: 14,
                    fontWeight: 'bolder'
                  },
                  position: 'right'
                },
                color: '#3C8DBC'
              }
            },
            data: data.value
          }]
        });
      });
    };


        chart[name](start, end);
    });
    $chart.trigger('show.chart', [start, end]);

    module.statistic($statistic, api);
    $statistic.trigger('show.statistic', [start, end]);

    // listen for change
    $chart.on('shown.bs.tab', function() {
        $chart.trigger('show.chart', [start, end]);
    });

    $dateRange.on('apply.daterangepicker', function(event, picker) {
        start = picker.startDate.format();
        end = picker.endDate.format();

        $dateRange.trigger('show.dateRange', [start, end]);
        $chart.trigger('show.chart', [start, end]);
        $statistic.trigger('show.statistic', [start, end]);
    });
};