'use strict';

// twbsPagination
(function () {
  if (typeof $.fn.twbsPagination !== 'function') {
    throw new Error('twbsPagination required');
  }

  var options = {
    first: '第一页',
    prev: '上一页',
    next: '下一页',
    last: '最后一页',
    paginationClass: 'pagination pagination-sm no-margin pull-right'
  };

  $.extend($.fn.twbsPagination.defaults, options);
}());

// moment
(function () {
  if (typeof moment !== 'function') {
    throw new Error('moment required');
  }

  moment.defaultFormat = 'YYYY-MM-DD';
}());
'use strict';

// show risk
(function ($) {
  $.fn.showRisk = function () {
    var $riskScore      = this.find('td.risk-score'),
        $localRelevance = this.find('td.local-relevance'),

        replaceClass    = function (className) {
          return function (index, element) {
            var num     = $(element).data('num'),
                $item   = $(element).find('i');

            $item
              .slice(0, num)
              .removeClass(className + '-o')
              .addClass(className);
          };
        };

    $riskScore.each(replaceClass('fa-star'));
    $localRelevance.each(replaceClass('fa-square'));

    return this;
  };
}(jQuery));
'use strict';

var App = {
  module: {},
  page: {}
};

// user
App.module.login = function () {
  var form     = document.forms.login,
      action   = form.action,
      elements = form.elements,
      username = elements.username,
      password = elements.password,
      submit   = elements[2],
      $msg     = $(form).find('p'),

      enableSubmit = function () {
        submit.disabled = !(username.value && password.value);
      },

      processLogin = function (event) {
        event.preventDefault();

        $.post(action, $(form).serialize(), function (response) {
          if (response.status) {
            location.href = location.search ? location.search.substr(1).split('=')[1] : '/';
          } else {
            $msg.text('用户名或密码错误！');
            submit.disabled = true;
            password.value  = '';
          }
        });
      };

  $(form).keyup(enableSubmit).submit(processLogin);
};

App.module.register = function () {
  var form     = document.forms.add,
      action   = form.action,
      elements = form.elements,
      username = elements.username,
      password = elements.password,
      retype   = elements.retype,
      submit   = elements[3],
      $msg     = $(form).find('p'),

      enableSubmit = function () {
        submit.disabled = !(username.value && password.value && retype.value);
      },

      processAdd   = function (event) {
        event.preventDefault();

        var processResponse = function (response) {
          if (response.status) {
            location.reload();
          } else {
            $msg.text('抱歉，添加失败！').show();
          }
        };

        if (password.value === retype.value) {
          $.post(action, $([username, password]).serialize(), processResponse);
        } else {
          $msg.text('两次输入密码不一致！').show();
          submit.disabled = true;
          password.value  = '';
          retype.value    = '';
        }
      };

  $(form).keyup(enableSubmit).submit(processAdd);
};

App.module.admin = function () {
  var $admin  = $('.user-admin'),
      $input  = $admin.find('input'),
      $button = $admin.find('button'),
      $reset  = $button.eq(0),
      $remove = $button.eq(1),
      id      = [],

      action = function (obj, api) {
        obj.click(function () {
          id.length = 0;

          $input.filter(':checked').each(function (index, element) {
            id.push( $(element).parent().next().data('id') );
          });

          if (id.length) {
            $.post(api, {id: id.toString()}, function (response) {
              if (response.status) {
                location.reload();
              }
            });
          }
        });
      };

  action($reset, '/api/user/reset/');
  action($remove, '/api/user/remove/');
};

App.module.settings = function () {
  var form        = document.forms.info,
      action      = form.action,
      elements    = form.elements,
      username    = elements.username,
      oldPassword = elements.oldPassword,
      newPassword = elements.newPassword,
      retype      = elements.retype,
      submit      = elements[4],
      $msg        = $(form).find('p'),


      enableSubmit = function () {
        submit.disabled = !(username.value && oldPassword.value && newPassword.value && retype.value);
      },

      processChange = function (event) {
        event.preventDefault();

        var processResponse = function (response) {
          if (response.status) {
            $msg.text('更新成功！').show();
            location.href = '/login/';
          } else {
            $msg.text('原密码错误！').show();
            oldPassword.value = '';
            newPassword.value = '';
            retype.value      = '';
          }
        };

        if (newPassword.value === retype.value) {
          $.post(action, $([username, oldPassword, newPassword]).serialize(), processResponse);
        } else {
          $msg.text('两次输入密码不一致！').show();
          newPassword.value = '';
          retype.value      = '';
        }
      };

  $(form).keyup(enableSubmit).submit(processChange);
};

// chart
App.module.line = function (path) {
  $.getJSON('/api/line' + path, function (data) {
    echarts.init($('#line-chart')[0], 'macarons').setOption({
      color: ['#00a65a', '#00c0ef', '#dd4b39'],
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['正面','中性','负面']
      },
      grid: {
        x: 40,
        y: 30,
        x2: 25,
        y2: 30
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: false,
          data: data.date
        }
      ],
      yAxis: [
        {
          type : 'value'
        }
      ],
      series: [
        {
          name: '正面',
          type: 'line',
          data: data.positive
        },
        {
          name: '中性',
          type: 'line',
          data: data.neutral
        },
        {
          name: '负面',
          type: 'line',
          data: data.negative
        }
      ]
    });
  });
};

App.module.pie = function (path) {
  $.getJSON('/api/pie' + path, function (data) {
    echarts.init($('#pie-chart')[0], 'macarons').setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
      },
      legend: {
        data: data.name
      },
      series: [
        {
          name: '信息比例',
          type: 'pie',
          radius: '55%',
          center: ['50%', '60%'],
          data: data.value
        }
      ]
    });
  });
};

App.module.map = function () {
  $.getJSON('/api/map/' , function (result) {
    var city = result.regionData,
        data = [],
        city2;

    for (var c in city) {
      data[c] = city[c].rank;
      switch (data[c]) {
      case 'A':
        data[c] = 1;
        break;
      case 'B':
        data[c] = 1;
        break;
      case 'C':
        data[c] = 2;
        break;
      case 'D':
        data[c] = 3;
        break;
      case 'E':
        data[c] = 3;
        break;
      default:
        data[c] = 3;
        break;
      }
    }

    echarts.util.mapData.params.params.wh = {
      getGeoJson: function (callback) {
      $.getJSON('/static/wh.json', callback);
      }
    };

    echarts.init(document.getElementById('map-chart')).setOption({
      title: {
        subtext: ''
      },
      tooltip: {
        trigger: 'item',
        formatter: function (a) {
          for (var i in city) {
            if (a[1] === city[i].regionName) {
              city2 = data[i];
              switch (city2) {
              case 1:
                city2 = 'A';
                break;
              case 2:
                city2 = 'B';
                break;
              case 3:
                city2 = 'C';
                break;
              default:
                city2 = 'erro';
                break;
              }
            }
          }
          return a[1] + '<br>' + '风险等级  ' + city2;
        }
      },
      legend: {
        orient: 'vertical',
        x: 'right',
        data: ['']
      },
      dataRange: {
        min: 0,
        max: 3,
        splitNumber: 3,
        color: ['#fa9529', '#fff26e', '#cee19e', ],
        formatter: function (v, v2) {
          if (v2 === '1') {
            return 'A' + '-低风险';
          } else if (v2 === '2') {
            return 'B' + '-中风险';
          } else if (v2 === '3') {
            return 'C' + '-高风险';
          }
        },
        x: 'right'
      },
      series: [{
        name: '数据名称',
        type: 'map',
        mapType: 'wh',
        selectedMode: 'single',
        itemStyle: {
          normal: {
            label: {
              show: false
            }
          },
          //区域名称
          emphasis: {
            label: {
              show: true
            }
          }
        },
        data: [{
          name: '江岸区',
          value: data[4]
        },
        {
          name: '江汉区',
          value: data[6]
        },
        {
          name: '硚口区',
          value: data[10]
        },
        {
          name: '汉阳区',
          value: data[11]
        },
        {
          name: '武昌区',
          value: data[0]
        },
        {
          name: '洪山区',
          value: data[1]
        },
        {
          name: '青山区',
          value: data[3]
        },
        {
          name: '东西湖区',
          value: data[9]
        },
        {
          name: '蔡甸区',
          value: data[12]
        },
        {
          name: '江夏区',
          value: data[2]
        },
        {
          name: '黄陂区',
          value: data[7]
        },
        {
          name: '新洲区',
          value: data[8]
        },
        {
          name: '汉南区',
          value: data[13]
        }]
      }]
    });
  });
};

// util
App.module.search = function () {
  var form  = document.forms.search,
      input = form.elements.keywords;

  $(form).submit(function (event) {
    event.preventDefault();

    var keywords = $.trim(input.value);

    if (keywords) {
      form.reset();
      location.href = '/search/' + keywords + '/';
    }
  });
};

App.module.menu = function (path, type) {
  var menu     = $('.sidebar-menu'),
      parent   = menu.parent(),

      validate = function () {
        var href = this.getAttribute('href');

        switch (true) {
        case type === 'dashboard':
          return href === '/';
        // both 'category' and 'location' are parent treeview
        case type === 'category':
        case type === 'location':
        case type === 'analytics':
          return href === path;
        default:
          return href.split('/')[1] === type;
        }
      };

  menu
    .detach()
    .find('a').filter(validate)
    .parent().addClass('active')
    .closest('.treeview-menu').addClass('menu-open')
    .closest('.treeview').addClass('active');

  menu.appendTo(parent);
};

App.module.inspection = function () {
  var $inspection = $('#inspection'),
      $content    = $inspection.children('.box-body').find('tbody');

  $content.load('/api/dashboard/local-inspection/');

  $inspection.on('click', 'button', function (event) {
    event.preventDefault();

    if ( $(this).hasClass('active') ) {
      return false;
    }

    $(this)
      .addClass('active')
      .siblings().removeClass('active');

    $content.load('/api/dashboard/' + this.id + '/');
  });
};

App.module.returnTop = function (el) {
  var top       = el.offset().top,
      scrollTop = top > 160 ? top - 120 : 0;

  $('body').animate({scrollTop: scrollTop});
};

App.module.paginate = function (options) {
  var returnTop = this.returnTop.bind(this),
      box = $(options.container).closest('.box'),
      boxBody = $(options.container).closest('.box-body'),
      loading = $('<div class="overlay"><i class="fa fa-refresh fa-spin"></i></div>'),
      pageClick = function (event, pageNumber) {
        $.ajax({
          url: options.api,
          data: options.filter(pageNumber),
          beforeSend: function () {
            loading.appendTo(box);
          },
          success: function (data) {
            options.render(options.container, data.html);
            loading.detach();
            returnTop(boxBody);
          }
        });
      };

  $.ajax({
    url: options.api,
    data: options.filter(),
    beforeSend: function () {
      loading.appendTo(box);
    },
    success: function (data) {
      if (!data.html) {
        loading.detach();
        return false;
      }
      options.render(options.container, data.html);
      boxBody.twbsPagination({
        totalPages: data.total,
        onPageClick: pageClick
      });
      loading.detach();
    }
  });
};

App.module.abstract = function (options) {
  var loading = $('<div class="overlay"><i class="fa fa-refresh fa-spin"></i></div>');

  options = $.extend({
    feature: '',
    container: '',
    render: function (container, content) {
      $('<div/>')
        .attr({id: this.feature, class: 'list-group no-margin'})
        .html(content)
        .find('[data-toggle="tooltip"]')
          .tooltip()
        .end()
        .replaceAll($(container));
    }
  }, options);

  $.ajax({
    url: '/api/' + options.feature + '/',
    data: {
      type: 'abstract'
    },
    beforeSend: function () {
      $(options.container).closest('.box').append(loading);
    },
    success: function (data) {
      options.render(options.container, data.html);
      loading.remove();
    }
  });
};

App.module.list = function (options) {
  options = $.extend(true, {
    feature: '',
    filter: {
      type: 'list',
      page: 1
    },
    container: '',
    render: function (container, content) {
      $(container).html(content);
    },
    visiblePages: 7
  }, options);

  $.extend($.fn.twbsPagination.defaults, {visiblePages: options.visiblePages});

  var api = '/api/' + options.feature + '/',
      filter = function (pageNumber) {
        if (typeof pageNumber !== 'number') {
          return options.filter;
        } else {
          return $.extend({}, options.filter, {page: pageNumber});
        }
      };

  this.paginate({
    api: api,
    filter: filter,
    container: options.container,
    render: options.render
  });
};

App.module.detail = function (options) {
  options = $.extend(true, {
    path: '',
    feature: '',
    container: '',
    render: function (container, content) {
      $(container).html(content);
    }
  }, options);

  $.extend($.fn.twbsPagination.defaults, {visiblePages: 7});

  var api = '/api' + options.path + options.feature + '/',
      filter = function (pageNumber) {
        if (typeof pageNumber !== 'number') {
          return {page: 1};
        } else {
          return {page: pageNumber};
        }
      };

  this.paginate({
    api: api,
    filter: filter,
    container: options.container,
    render: options.render
  });
};

App.module.collect = function (type, id) {
  $('.collection').click(function () {
    var star = $(this).find('i'),
        text = $(this).find('span');

    function collect(method) {
      $.ajax({
        type: method,
        url: '/api/collection/',
        data: {
          type: type === 'news' ? 'article' : 'topic',
          id: id
        },
        success: function (data) {
          if (data.status) {
            star.toggleClass('fa-star-o');
            star.toggleClass('fa-star');
            text.text(method === 'PUT' ? '取消收藏' : '添加收藏');
          }
        }
      });
    }

    if (star.hasClass('fa-star')) {
      collect('DELETE');
    } else {
      collect('PUT');
    }
  });
};

App.module.dateRange = function ($dateRange) {
  $dateRange
    .on('show.dateRange', function (event, start, end) {
      $(this).children('span').html(start + ' ~ ' + end);
    })
    .daterangepicker({
      ranges: {
        '过去7天': [moment().subtract(6, 'days'), moment()],
        '过去30天': [moment().subtract(29, 'days'), moment()],
        '这个月': [moment().startOf('month'), moment().endOf('month')],
        '上个月': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
      },
      'locale': {
        'format': 'YYYY-MM-DD',
        'separator': ' - ',
        'applyLabel': '确定',
        'cancelLabel': '取消',
        'fromLabel': '从',
        'toLabel': '到',
        'customRangeLabel': '自定义'
      },
      'startDate': moment().subtract(6, 'days'),
      'endDate': moment(),
      'minDate': '2010-01-01',
      'maxDate': moment(),
      'opens': 'left',
      'parentEl': '.content-header',
      'applyClass': 'btn-success',
      'cancelClass': 'btn-default'
    });
};

App.module.statistic = function($el, api) {
    var $total = $el.find('.statistic-total > span'),
        $risk = $el.find('.statistic-risk > span');

    $el.on('show.statistic', function(event, start, end) {
        $.getJSON(api, {
            type: 'statistic',
            start: start,
            end: end
        }, function(statistic) {
            $total.text(statistic.total);
            $risk.text(statistic.risk);
        });
    });
};
'use strict';

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

App.page.inspection = function () {
  // pending
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
'use strict';

App.route = function () {
  var module  = this.module,
      page    = this.page,
      path    = location.pathname,
      summary = /^\/(\w+)\/$/,
      detail  = /^\/(\w+)\/(\d+)\/$/,
      match   = null,
      type,
      id;

  switch (true) {
  case path === '/':
    type  = 'dashboard';
    break;
  case summary.test(path):
    match = summary.exec(path);
    type  = match[1];
    break;
  case detail.test(path):
    match = detail.exec(path);
    type  = match[1];
    id    = +match[2];
    break;
  }

  if (type === 'login') {
    return page.login(module);
  }

  // common
  module.search();
  module.menu(path, type);

  if (id === undefined) {
    return page[type](module, path, type);
  } else {
    return page[type + 'Detail'](module, path, type, id);
  }
};


//
// Initialization
//

$(function () {
  App.route();
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbImNvbmZpZy5qcyIsInBsdWdpbi5qcyIsIm1vZHVsZS5qcyIsInBhZ2UuanMiLCJyb3V0ZS5qcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUMxQkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQ3pCQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FDOXBCQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQ3BzQkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsImZpbGUiOiJhcHAuanMiLCJzb3VyY2VzQ29udGVudCI6WyIndXNlIHN0cmljdCc7XG5cbi8vIHR3YnNQYWdpbmF0aW9uXG4oZnVuY3Rpb24gKCkge1xuICBpZiAodHlwZW9mICQuZm4udHdic1BhZ2luYXRpb24gIT09ICdmdW5jdGlvbicpIHtcbiAgICB0aHJvdyBuZXcgRXJyb3IoJ3R3YnNQYWdpbmF0aW9uIHJlcXVpcmVkJyk7XG4gIH1cblxuICB2YXIgb3B0aW9ucyA9IHtcbiAgICBmaXJzdDogJ+esrOS4gOmhtScsXG4gICAgcHJldjogJ+S4iuS4gOmhtScsXG4gICAgbmV4dDogJ+S4i+S4gOmhtScsXG4gICAgbGFzdDogJ+acgOWQjuS4gOmhtScsXG4gICAgcGFnaW5hdGlvbkNsYXNzOiAncGFnaW5hdGlvbiBwYWdpbmF0aW9uLXNtIG5vLW1hcmdpbiBwdWxsLXJpZ2h0J1xuICB9O1xuXG4gICQuZXh0ZW5kKCQuZm4udHdic1BhZ2luYXRpb24uZGVmYXVsdHMsIG9wdGlvbnMpO1xufSgpKTtcblxuLy8gbW9tZW50XG4oZnVuY3Rpb24gKCkge1xuICBpZiAodHlwZW9mIG1vbWVudCAhPT0gJ2Z1bmN0aW9uJykge1xuICAgIHRocm93IG5ldyBFcnJvcignbW9tZW50IHJlcXVpcmVkJyk7XG4gIH1cblxuICBtb21lbnQuZGVmYXVsdEZvcm1hdCA9ICdZWVlZLU1NLUREJztcbn0oKSk7IiwiJ3VzZSBzdHJpY3QnO1xuXG4vLyBzaG93IHJpc2tcbihmdW5jdGlvbiAoJCkge1xuICAkLmZuLnNob3dSaXNrID0gZnVuY3Rpb24gKCkge1xuICAgIHZhciAkcmlza1Njb3JlICAgICAgPSB0aGlzLmZpbmQoJ3RkLnJpc2stc2NvcmUnKSxcbiAgICAgICAgJGxvY2FsUmVsZXZhbmNlID0gdGhpcy5maW5kKCd0ZC5sb2NhbC1yZWxldmFuY2UnKSxcblxuICAgICAgICByZXBsYWNlQ2xhc3MgICAgPSBmdW5jdGlvbiAoY2xhc3NOYW1lKSB7XG4gICAgICAgICAgcmV0dXJuIGZ1bmN0aW9uIChpbmRleCwgZWxlbWVudCkge1xuICAgICAgICAgICAgdmFyIG51bSAgICAgPSAkKGVsZW1lbnQpLmRhdGEoJ251bScpLFxuICAgICAgICAgICAgICAgICRpdGVtICAgPSAkKGVsZW1lbnQpLmZpbmQoJ2knKTtcblxuICAgICAgICAgICAgJGl0ZW1cbiAgICAgICAgICAgICAgLnNsaWNlKDAsIG51bSlcbiAgICAgICAgICAgICAgLnJlbW92ZUNsYXNzKGNsYXNzTmFtZSArICctbycpXG4gICAgICAgICAgICAgIC5hZGRDbGFzcyhjbGFzc05hbWUpO1xuICAgICAgICAgIH07XG4gICAgICAgIH07XG5cbiAgICAkcmlza1Njb3JlLmVhY2gocmVwbGFjZUNsYXNzKCdmYS1zdGFyJykpO1xuICAgICRsb2NhbFJlbGV2YW5jZS5lYWNoKHJlcGxhY2VDbGFzcygnZmEtc3F1YXJlJykpO1xuXG4gICAgcmV0dXJuIHRoaXM7XG4gIH07XG59KGpRdWVyeSkpOyIsIid1c2Ugc3RyaWN0JztcblxudmFyIEFwcCA9IHtcbiAgbW9kdWxlOiB7fSxcbiAgcGFnZToge31cbn07XG5cbi8vIHVzZXJcbkFwcC5tb2R1bGUubG9naW4gPSBmdW5jdGlvbiAoKSB7XG4gIHZhciBmb3JtICAgICA9IGRvY3VtZW50LmZvcm1zLmxvZ2luLFxuICAgICAgYWN0aW9uICAgPSBmb3JtLmFjdGlvbixcbiAgICAgIGVsZW1lbnRzID0gZm9ybS5lbGVtZW50cyxcbiAgICAgIHVzZXJuYW1lID0gZWxlbWVudHMudXNlcm5hbWUsXG4gICAgICBwYXNzd29yZCA9IGVsZW1lbnRzLnBhc3N3b3JkLFxuICAgICAgc3VibWl0ICAgPSBlbGVtZW50c1syXSxcbiAgICAgICRtc2cgICAgID0gJChmb3JtKS5maW5kKCdwJyksXG5cbiAgICAgIGVuYWJsZVN1Ym1pdCA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgc3VibWl0LmRpc2FibGVkID0gISh1c2VybmFtZS52YWx1ZSAmJiBwYXNzd29yZC52YWx1ZSk7XG4gICAgICB9LFxuXG4gICAgICBwcm9jZXNzTG9naW4gPSBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICAgICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcblxuICAgICAgICAkLnBvc3QoYWN0aW9uLCAkKGZvcm0pLnNlcmlhbGl6ZSgpLCBmdW5jdGlvbiAocmVzcG9uc2UpIHtcbiAgICAgICAgICBpZiAocmVzcG9uc2Uuc3RhdHVzKSB7XG4gICAgICAgICAgICBsb2NhdGlvbi5ocmVmID0gbG9jYXRpb24uc2VhcmNoID8gbG9jYXRpb24uc2VhcmNoLnN1YnN0cigxKS5zcGxpdCgnPScpWzFdIDogJy8nO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAkbXNnLnRleHQoJ+eUqOaIt+WQjeaIluWvhueggemUmeivr++8gScpO1xuICAgICAgICAgICAgc3VibWl0LmRpc2FibGVkID0gdHJ1ZTtcbiAgICAgICAgICAgIHBhc3N3b3JkLnZhbHVlICA9ICcnO1xuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgICB9O1xuXG4gICQoZm9ybSkua2V5dXAoZW5hYmxlU3VibWl0KS5zdWJtaXQocHJvY2Vzc0xvZ2luKTtcbn07XG5cbkFwcC5tb2R1bGUucmVnaXN0ZXIgPSBmdW5jdGlvbiAoKSB7XG4gIHZhciBmb3JtICAgICA9IGRvY3VtZW50LmZvcm1zLmFkZCxcbiAgICAgIGFjdGlvbiAgID0gZm9ybS5hY3Rpb24sXG4gICAgICBlbGVtZW50cyA9IGZvcm0uZWxlbWVudHMsXG4gICAgICB1c2VybmFtZSA9IGVsZW1lbnRzLnVzZXJuYW1lLFxuICAgICAgcGFzc3dvcmQgPSBlbGVtZW50cy5wYXNzd29yZCxcbiAgICAgIHJldHlwZSAgID0gZWxlbWVudHMucmV0eXBlLFxuICAgICAgc3VibWl0ICAgPSBlbGVtZW50c1szXSxcbiAgICAgICRtc2cgICAgID0gJChmb3JtKS5maW5kKCdwJyksXG5cbiAgICAgIGVuYWJsZVN1Ym1pdCA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgc3VibWl0LmRpc2FibGVkID0gISh1c2VybmFtZS52YWx1ZSAmJiBwYXNzd29yZC52YWx1ZSAmJiByZXR5cGUudmFsdWUpO1xuICAgICAgfSxcblxuICAgICAgcHJvY2Vzc0FkZCAgID0gZnVuY3Rpb24gKGV2ZW50KSB7XG4gICAgICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG5cbiAgICAgICAgdmFyIHByb2Nlc3NSZXNwb25zZSA9IGZ1bmN0aW9uIChyZXNwb25zZSkge1xuICAgICAgICAgIGlmIChyZXNwb25zZS5zdGF0dXMpIHtcbiAgICAgICAgICAgIGxvY2F0aW9uLnJlbG9hZCgpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAkbXNnLnRleHQoJ+aKseatie+8jOa3u+WKoOWksei0pe+8gScpLnNob3coKTtcbiAgICAgICAgICB9XG4gICAgICAgIH07XG5cbiAgICAgICAgaWYgKHBhc3N3b3JkLnZhbHVlID09PSByZXR5cGUudmFsdWUpIHtcbiAgICAgICAgICAkLnBvc3QoYWN0aW9uLCAkKFt1c2VybmFtZSwgcGFzc3dvcmRdKS5zZXJpYWxpemUoKSwgcHJvY2Vzc1Jlc3BvbnNlKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAkbXNnLnRleHQoJ+S4pOasoei+k+WFpeWvhueggeS4jeS4gOiHtO+8gScpLnNob3coKTtcbiAgICAgICAgICBzdWJtaXQuZGlzYWJsZWQgPSB0cnVlO1xuICAgICAgICAgIHBhc3N3b3JkLnZhbHVlICA9ICcnO1xuICAgICAgICAgIHJldHlwZS52YWx1ZSAgICA9ICcnO1xuICAgICAgICB9XG4gICAgICB9O1xuXG4gICQoZm9ybSkua2V5dXAoZW5hYmxlU3VibWl0KS5zdWJtaXQocHJvY2Vzc0FkZCk7XG59O1xuXG5BcHAubW9kdWxlLmFkbWluID0gZnVuY3Rpb24gKCkge1xuICB2YXIgJGFkbWluICA9ICQoJy51c2VyLWFkbWluJyksXG4gICAgICAkaW5wdXQgID0gJGFkbWluLmZpbmQoJ2lucHV0JyksXG4gICAgICAkYnV0dG9uID0gJGFkbWluLmZpbmQoJ2J1dHRvbicpLFxuICAgICAgJHJlc2V0ICA9ICRidXR0b24uZXEoMCksXG4gICAgICAkcmVtb3ZlID0gJGJ1dHRvbi5lcSgxKSxcbiAgICAgIGlkICAgICAgPSBbXSxcblxuICAgICAgYWN0aW9uID0gZnVuY3Rpb24gKG9iaiwgYXBpKSB7XG4gICAgICAgIG9iai5jbGljayhmdW5jdGlvbiAoKSB7XG4gICAgICAgICAgaWQubGVuZ3RoID0gMDtcblxuICAgICAgICAgICRpbnB1dC5maWx0ZXIoJzpjaGVja2VkJykuZWFjaChmdW5jdGlvbiAoaW5kZXgsIGVsZW1lbnQpIHtcbiAgICAgICAgICAgIGlkLnB1c2goICQoZWxlbWVudCkucGFyZW50KCkubmV4dCgpLmRhdGEoJ2lkJykgKTtcbiAgICAgICAgICB9KTtcblxuICAgICAgICAgIGlmIChpZC5sZW5ndGgpIHtcbiAgICAgICAgICAgICQucG9zdChhcGksIHtpZDogaWQudG9TdHJpbmcoKX0sIGZ1bmN0aW9uIChyZXNwb25zZSkge1xuICAgICAgICAgICAgICBpZiAocmVzcG9uc2Uuc3RhdHVzKSB7XG4gICAgICAgICAgICAgICAgbG9jYXRpb24ucmVsb2FkKCk7XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgICB9O1xuXG4gIGFjdGlvbigkcmVzZXQsICcvYXBpL3VzZXIvcmVzZXQvJyk7XG4gIGFjdGlvbigkcmVtb3ZlLCAnL2FwaS91c2VyL3JlbW92ZS8nKTtcbn07XG5cbkFwcC5tb2R1bGUuc2V0dGluZ3MgPSBmdW5jdGlvbiAoKSB7XG4gIHZhciBmb3JtICAgICAgICA9IGRvY3VtZW50LmZvcm1zLmluZm8sXG4gICAgICBhY3Rpb24gICAgICA9IGZvcm0uYWN0aW9uLFxuICAgICAgZWxlbWVudHMgICAgPSBmb3JtLmVsZW1lbnRzLFxuICAgICAgdXNlcm5hbWUgICAgPSBlbGVtZW50cy51c2VybmFtZSxcbiAgICAgIG9sZFBhc3N3b3JkID0gZWxlbWVudHMub2xkUGFzc3dvcmQsXG4gICAgICBuZXdQYXNzd29yZCA9IGVsZW1lbnRzLm5ld1Bhc3N3b3JkLFxuICAgICAgcmV0eXBlICAgICAgPSBlbGVtZW50cy5yZXR5cGUsXG4gICAgICBzdWJtaXQgICAgICA9IGVsZW1lbnRzWzRdLFxuICAgICAgJG1zZyAgICAgICAgPSAkKGZvcm0pLmZpbmQoJ3AnKSxcblxuXG4gICAgICBlbmFibGVTdWJtaXQgPSBmdW5jdGlvbiAoKSB7XG4gICAgICAgIHN1Ym1pdC5kaXNhYmxlZCA9ICEodXNlcm5hbWUudmFsdWUgJiYgb2xkUGFzc3dvcmQudmFsdWUgJiYgbmV3UGFzc3dvcmQudmFsdWUgJiYgcmV0eXBlLnZhbHVlKTtcbiAgICAgIH0sXG5cbiAgICAgIHByb2Nlc3NDaGFuZ2UgPSBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICAgICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcblxuICAgICAgICB2YXIgcHJvY2Vzc1Jlc3BvbnNlID0gZnVuY3Rpb24gKHJlc3BvbnNlKSB7XG4gICAgICAgICAgaWYgKHJlc3BvbnNlLnN0YXR1cykge1xuICAgICAgICAgICAgJG1zZy50ZXh0KCfmm7TmlrDmiJDlip/vvIEnKS5zaG93KCk7XG4gICAgICAgICAgICBsb2NhdGlvbi5ocmVmID0gJy9sb2dpbi8nO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAkbXNnLnRleHQoJ+WOn+WvhueggemUmeivr++8gScpLnNob3coKTtcbiAgICAgICAgICAgIG9sZFBhc3N3b3JkLnZhbHVlID0gJyc7XG4gICAgICAgICAgICBuZXdQYXNzd29yZC52YWx1ZSA9ICcnO1xuICAgICAgICAgICAgcmV0eXBlLnZhbHVlICAgICAgPSAnJztcbiAgICAgICAgICB9XG4gICAgICAgIH07XG5cbiAgICAgICAgaWYgKG5ld1Bhc3N3b3JkLnZhbHVlID09PSByZXR5cGUudmFsdWUpIHtcbiAgICAgICAgICAkLnBvc3QoYWN0aW9uLCAkKFt1c2VybmFtZSwgb2xkUGFzc3dvcmQsIG5ld1Bhc3N3b3JkXSkuc2VyaWFsaXplKCksIHByb2Nlc3NSZXNwb25zZSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgJG1zZy50ZXh0KCfkuKTmrKHovpPlhaXlr4bnoIHkuI3kuIDoh7TvvIEnKS5zaG93KCk7XG4gICAgICAgICAgbmV3UGFzc3dvcmQudmFsdWUgPSAnJztcbiAgICAgICAgICByZXR5cGUudmFsdWUgICAgICA9ICcnO1xuICAgICAgICB9XG4gICAgICB9O1xuXG4gICQoZm9ybSkua2V5dXAoZW5hYmxlU3VibWl0KS5zdWJtaXQocHJvY2Vzc0NoYW5nZSk7XG59O1xuXG4vLyBjaGFydFxuQXBwLm1vZHVsZS5saW5lID0gZnVuY3Rpb24gKHBhdGgpIHtcbiAgJC5nZXRKU09OKCcvYXBpL2xpbmUnICsgcGF0aCwgZnVuY3Rpb24gKGRhdGEpIHtcbiAgICBlY2hhcnRzLmluaXQoJCgnI2xpbmUtY2hhcnQnKVswXSwgJ21hY2Fyb25zJykuc2V0T3B0aW9uKHtcbiAgICAgIGNvbG9yOiBbJyMwMGE2NWEnLCAnIzAwYzBlZicsICcjZGQ0YjM5J10sXG4gICAgICB0b29sdGlwOiB7XG4gICAgICAgIHRyaWdnZXI6ICdheGlzJ1xuICAgICAgfSxcbiAgICAgIGxlZ2VuZDoge1xuICAgICAgICBkYXRhOiBbJ+ato+mdoicsJ+S4reaApycsJ+i0n+mdoiddXG4gICAgICB9LFxuICAgICAgZ3JpZDoge1xuICAgICAgICB4OiA0MCxcbiAgICAgICAgeTogMzAsXG4gICAgICAgIHgyOiAyNSxcbiAgICAgICAgeTI6IDMwXG4gICAgICB9LFxuICAgICAgeEF4aXM6IFtcbiAgICAgICAge1xuICAgICAgICAgIHR5cGU6ICdjYXRlZ29yeScsXG4gICAgICAgICAgYm91bmRhcnlHYXA6IGZhbHNlLFxuICAgICAgICAgIGRhdGE6IGRhdGEuZGF0ZVxuICAgICAgICB9XG4gICAgICBdLFxuICAgICAgeUF4aXM6IFtcbiAgICAgICAge1xuICAgICAgICAgIHR5cGUgOiAndmFsdWUnXG4gICAgICAgIH1cbiAgICAgIF0sXG4gICAgICBzZXJpZXM6IFtcbiAgICAgICAge1xuICAgICAgICAgIG5hbWU6ICfmraPpnaInLFxuICAgICAgICAgIHR5cGU6ICdsaW5lJyxcbiAgICAgICAgICBkYXRhOiBkYXRhLnBvc2l0aXZlXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBuYW1lOiAn5Lit5oCnJyxcbiAgICAgICAgICB0eXBlOiAnbGluZScsXG4gICAgICAgICAgZGF0YTogZGF0YS5uZXV0cmFsXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBuYW1lOiAn6LSf6Z2iJyxcbiAgICAgICAgICB0eXBlOiAnbGluZScsXG4gICAgICAgICAgZGF0YTogZGF0YS5uZWdhdGl2ZVxuICAgICAgICB9XG4gICAgICBdXG4gICAgfSk7XG4gIH0pO1xufTtcblxuQXBwLm1vZHVsZS5waWUgPSBmdW5jdGlvbiAocGF0aCkge1xuICAkLmdldEpTT04oJy9hcGkvcGllJyArIHBhdGgsIGZ1bmN0aW9uIChkYXRhKSB7XG4gICAgZWNoYXJ0cy5pbml0KCQoJyNwaWUtY2hhcnQnKVswXSwgJ21hY2Fyb25zJykuc2V0T3B0aW9uKHtcbiAgICAgIHRvb2x0aXA6IHtcbiAgICAgICAgdHJpZ2dlcjogJ2l0ZW0nLFxuICAgICAgICBmb3JtYXR0ZXI6ICd7YX0gPGJyLz57Yn0gOiB7Y30gKHtkfSUpJ1xuICAgICAgfSxcbiAgICAgIGxlZ2VuZDoge1xuICAgICAgICBkYXRhOiBkYXRhLm5hbWVcbiAgICAgIH0sXG4gICAgICBzZXJpZXM6IFtcbiAgICAgICAge1xuICAgICAgICAgIG5hbWU6ICfkv6Hmga/mr5TkvosnLFxuICAgICAgICAgIHR5cGU6ICdwaWUnLFxuICAgICAgICAgIHJhZGl1czogJzU1JScsXG4gICAgICAgICAgY2VudGVyOiBbJzUwJScsICc2MCUnXSxcbiAgICAgICAgICBkYXRhOiBkYXRhLnZhbHVlXG4gICAgICAgIH1cbiAgICAgIF1cbiAgICB9KTtcbiAgfSk7XG59O1xuXG5BcHAubW9kdWxlLm1hcCA9IGZ1bmN0aW9uICgpIHtcbiAgJC5nZXRKU09OKCcvYXBpL21hcC8nICwgZnVuY3Rpb24gKHJlc3VsdCkge1xuICAgIHZhciBjaXR5ID0gcmVzdWx0LnJlZ2lvbkRhdGEsXG4gICAgICAgIGRhdGEgPSBbXSxcbiAgICAgICAgY2l0eTI7XG5cbiAgICBmb3IgKHZhciBjIGluIGNpdHkpIHtcbiAgICAgIGRhdGFbY10gPSBjaXR5W2NdLnJhbms7XG4gICAgICBzd2l0Y2ggKGRhdGFbY10pIHtcbiAgICAgIGNhc2UgJ0EnOlxuICAgICAgICBkYXRhW2NdID0gMTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdCJzpcbiAgICAgICAgZGF0YVtjXSA9IDE7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnQyc6XG4gICAgICAgIGRhdGFbY10gPSAyO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ0QnOlxuICAgICAgICBkYXRhW2NdID0gMztcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdFJzpcbiAgICAgICAgZGF0YVtjXSA9IDM7XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgZGF0YVtjXSA9IDM7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgIH1cblxuICAgIGVjaGFydHMudXRpbC5tYXBEYXRhLnBhcmFtcy5wYXJhbXMud2ggPSB7XG4gICAgICBnZXRHZW9Kc29uOiBmdW5jdGlvbiAoY2FsbGJhY2spIHtcbiAgICAgICQuZ2V0SlNPTignL3N0YXRpYy93aC5qc29uJywgY2FsbGJhY2spO1xuICAgICAgfVxuICAgIH07XG5cbiAgICBlY2hhcnRzLmluaXQoZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ21hcC1jaGFydCcpKS5zZXRPcHRpb24oe1xuICAgICAgdGl0bGU6IHtcbiAgICAgICAgc3VidGV4dDogJydcbiAgICAgIH0sXG4gICAgICB0b29sdGlwOiB7XG4gICAgICAgIHRyaWdnZXI6ICdpdGVtJyxcbiAgICAgICAgZm9ybWF0dGVyOiBmdW5jdGlvbiAoYSkge1xuICAgICAgICAgIGZvciAodmFyIGkgaW4gY2l0eSkge1xuICAgICAgICAgICAgaWYgKGFbMV0gPT09IGNpdHlbaV0ucmVnaW9uTmFtZSkge1xuICAgICAgICAgICAgICBjaXR5MiA9IGRhdGFbaV07XG4gICAgICAgICAgICAgIHN3aXRjaCAoY2l0eTIpIHtcbiAgICAgICAgICAgICAgY2FzZSAxOlxuICAgICAgICAgICAgICAgIGNpdHkyID0gJ0EnO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgICBjYXNlIDI6XG4gICAgICAgICAgICAgICAgY2l0eTIgPSAnQic7XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICAgIGNhc2UgMzpcbiAgICAgICAgICAgICAgICBjaXR5MiA9ICdDJztcbiAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgICAgZGVmYXVsdDpcbiAgICAgICAgICAgICAgICBjaXR5MiA9ICdlcnJvJztcbiAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgICByZXR1cm4gYVsxXSArICc8YnI+JyArICfpo47pmannrYnnuqcgICcgKyBjaXR5MjtcbiAgICAgICAgfVxuICAgICAgfSxcbiAgICAgIGxlZ2VuZDoge1xuICAgICAgICBvcmllbnQ6ICd2ZXJ0aWNhbCcsXG4gICAgICAgIHg6ICdyaWdodCcsXG4gICAgICAgIGRhdGE6IFsnJ11cbiAgICAgIH0sXG4gICAgICBkYXRhUmFuZ2U6IHtcbiAgICAgICAgbWluOiAwLFxuICAgICAgICBtYXg6IDMsXG4gICAgICAgIHNwbGl0TnVtYmVyOiAzLFxuICAgICAgICBjb2xvcjogWycjZmE5NTI5JywgJyNmZmYyNmUnLCAnI2NlZTE5ZScsIF0sXG4gICAgICAgIGZvcm1hdHRlcjogZnVuY3Rpb24gKHYsIHYyKSB7XG4gICAgICAgICAgaWYgKHYyID09PSAnMScpIHtcbiAgICAgICAgICAgIHJldHVybiAnQScgKyAnLeS9jumjjumZqSc7XG4gICAgICAgICAgfSBlbHNlIGlmICh2MiA9PT0gJzInKSB7XG4gICAgICAgICAgICByZXR1cm4gJ0InICsgJy3kuK3po47pmaknO1xuICAgICAgICAgIH0gZWxzZSBpZiAodjIgPT09ICczJykge1xuICAgICAgICAgICAgcmV0dXJuICdDJyArICct6auY6aOO6ZmpJztcbiAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHg6ICdyaWdodCdcbiAgICAgIH0sXG4gICAgICBzZXJpZXM6IFt7XG4gICAgICAgIG5hbWU6ICfmlbDmja7lkI3np7AnLFxuICAgICAgICB0eXBlOiAnbWFwJyxcbiAgICAgICAgbWFwVHlwZTogJ3doJyxcbiAgICAgICAgc2VsZWN0ZWRNb2RlOiAnc2luZ2xlJyxcbiAgICAgICAgaXRlbVN0eWxlOiB7XG4gICAgICAgICAgbm9ybWFsOiB7XG4gICAgICAgICAgICBsYWJlbDoge1xuICAgICAgICAgICAgICBzaG93OiBmYWxzZVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH0sXG4gICAgICAgICAgLy/ljLrln5/lkI3np7BcbiAgICAgICAgICBlbXBoYXNpczoge1xuICAgICAgICAgICAgbGFiZWw6IHtcbiAgICAgICAgICAgICAgc2hvdzogdHJ1ZVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgZGF0YTogW3tcbiAgICAgICAgICBuYW1lOiAn5rGf5bK45Yy6JyxcbiAgICAgICAgICB2YWx1ZTogZGF0YVs0XVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgbmFtZTogJ+axn+axieWMuicsXG4gICAgICAgICAgdmFsdWU6IGRhdGFbNl1cbiAgICAgICAgfSxcbiAgICAgICAge1xuICAgICAgICAgIG5hbWU6ICfnoZrlj6PljLonLFxuICAgICAgICAgIHZhbHVlOiBkYXRhWzEwXVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgbmFtZTogJ+axiemYs+WMuicsXG4gICAgICAgICAgdmFsdWU6IGRhdGFbMTFdXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBuYW1lOiAn5q2m5piM5Yy6JyxcbiAgICAgICAgICB2YWx1ZTogZGF0YVswXVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgbmFtZTogJ+a0quWxseWMuicsXG4gICAgICAgICAgdmFsdWU6IGRhdGFbMV1cbiAgICAgICAgfSxcbiAgICAgICAge1xuICAgICAgICAgIG5hbWU6ICfpnZLlsbHljLonLFxuICAgICAgICAgIHZhbHVlOiBkYXRhWzNdXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBuYW1lOiAn5Lic6KW/5rmW5Yy6JyxcbiAgICAgICAgICB2YWx1ZTogZGF0YVs5XVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgbmFtZTogJ+iUoeeUuOWMuicsXG4gICAgICAgICAgdmFsdWU6IGRhdGFbMTJdXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBuYW1lOiAn5rGf5aSP5Yy6JyxcbiAgICAgICAgICB2YWx1ZTogZGF0YVsyXVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgbmFtZTogJ+m7hOmZguWMuicsXG4gICAgICAgICAgdmFsdWU6IGRhdGFbN11cbiAgICAgICAgfSxcbiAgICAgICAge1xuICAgICAgICAgIG5hbWU6ICfmlrDmtLLljLonLFxuICAgICAgICAgIHZhbHVlOiBkYXRhWzhdXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBuYW1lOiAn5rGJ5Y2X5Yy6JyxcbiAgICAgICAgICB2YWx1ZTogZGF0YVsxM11cbiAgICAgICAgfV1cbiAgICAgIH1dXG4gICAgfSk7XG4gIH0pO1xufTtcblxuLy8gdXRpbFxuQXBwLm1vZHVsZS5zZWFyY2ggPSBmdW5jdGlvbiAoKSB7XG4gIHZhciBmb3JtICA9IGRvY3VtZW50LmZvcm1zLnNlYXJjaCxcbiAgICAgIGlucHV0ID0gZm9ybS5lbGVtZW50cy5rZXl3b3JkcztcblxuICAkKGZvcm0pLnN1Ym1pdChmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuXG4gICAgdmFyIGtleXdvcmRzID0gJC50cmltKGlucHV0LnZhbHVlKTtcblxuICAgIGlmIChrZXl3b3Jkcykge1xuICAgICAgZm9ybS5yZXNldCgpO1xuICAgICAgbG9jYXRpb24uaHJlZiA9ICcvc2VhcmNoLycgKyBrZXl3b3JkcyArICcvJztcbiAgICB9XG4gIH0pO1xufTtcblxuQXBwLm1vZHVsZS5tZW51ID0gZnVuY3Rpb24gKHBhdGgsIHR5cGUpIHtcbiAgdmFyIG1lbnUgICAgID0gJCgnLnNpZGViYXItbWVudScpLFxuICAgICAgcGFyZW50ICAgPSBtZW51LnBhcmVudCgpLFxuXG4gICAgICB2YWxpZGF0ZSA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgdmFyIGhyZWYgPSB0aGlzLmdldEF0dHJpYnV0ZSgnaHJlZicpO1xuXG4gICAgICAgIHN3aXRjaCAodHJ1ZSkge1xuICAgICAgICBjYXNlIHR5cGUgPT09ICdkYXNoYm9hcmQnOlxuICAgICAgICAgIHJldHVybiBocmVmID09PSAnLyc7XG4gICAgICAgIC8vIGJvdGggJ2NhdGVnb3J5JyBhbmQgJ2xvY2F0aW9uJyBhcmUgcGFyZW50IHRyZWV2aWV3XG4gICAgICAgIGNhc2UgdHlwZSA9PT0gJ2NhdGVnb3J5JzpcbiAgICAgICAgY2FzZSB0eXBlID09PSAnbG9jYXRpb24nOlxuICAgICAgICBjYXNlIHR5cGUgPT09ICdhbmFseXRpY3MnOlxuICAgICAgICAgIHJldHVybiBocmVmID09PSBwYXRoO1xuICAgICAgICBkZWZhdWx0OlxuICAgICAgICAgIHJldHVybiBocmVmLnNwbGl0KCcvJylbMV0gPT09IHR5cGU7XG4gICAgICAgIH1cbiAgICAgIH07XG5cbiAgbWVudVxuICAgIC5kZXRhY2goKVxuICAgIC5maW5kKCdhJykuZmlsdGVyKHZhbGlkYXRlKVxuICAgIC5wYXJlbnQoKS5hZGRDbGFzcygnYWN0aXZlJylcbiAgICAuY2xvc2VzdCgnLnRyZWV2aWV3LW1lbnUnKS5hZGRDbGFzcygnbWVudS1vcGVuJylcbiAgICAuY2xvc2VzdCgnLnRyZWV2aWV3JykuYWRkQ2xhc3MoJ2FjdGl2ZScpO1xuXG4gIG1lbnUuYXBwZW5kVG8ocGFyZW50KTtcbn07XG5cbkFwcC5tb2R1bGUuaW5zcGVjdGlvbiA9IGZ1bmN0aW9uICgpIHtcbiAgdmFyICRpbnNwZWN0aW9uID0gJCgnI2luc3BlY3Rpb24nKSxcbiAgICAgICRjb250ZW50ICAgID0gJGluc3BlY3Rpb24uY2hpbGRyZW4oJy5ib3gtYm9keScpLmZpbmQoJ3Rib2R5Jyk7XG5cbiAgJGNvbnRlbnQubG9hZCgnL2FwaS9kYXNoYm9hcmQvbG9jYWwtaW5zcGVjdGlvbi8nKTtcblxuICAkaW5zcGVjdGlvbi5vbignY2xpY2snLCAnYnV0dG9uJywgZnVuY3Rpb24gKGV2ZW50KSB7XG4gICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcblxuICAgIGlmICggJCh0aGlzKS5oYXNDbGFzcygnYWN0aXZlJykgKSB7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuXG4gICAgJCh0aGlzKVxuICAgICAgLmFkZENsYXNzKCdhY3RpdmUnKVxuICAgICAgLnNpYmxpbmdzKCkucmVtb3ZlQ2xhc3MoJ2FjdGl2ZScpO1xuXG4gICAgJGNvbnRlbnQubG9hZCgnL2FwaS9kYXNoYm9hcmQvJyArIHRoaXMuaWQgKyAnLycpO1xuICB9KTtcbn07XG5cbkFwcC5tb2R1bGUucmV0dXJuVG9wID0gZnVuY3Rpb24gKGVsKSB7XG4gIHZhciB0b3AgICAgICAgPSBlbC5vZmZzZXQoKS50b3AsXG4gICAgICBzY3JvbGxUb3AgPSB0b3AgPiAxNjAgPyB0b3AgLSAxMjAgOiAwO1xuXG4gICQoJ2JvZHknKS5hbmltYXRlKHtzY3JvbGxUb3A6IHNjcm9sbFRvcH0pO1xufTtcblxuQXBwLm1vZHVsZS5wYWdpbmF0ZSA9IGZ1bmN0aW9uIChvcHRpb25zKSB7XG4gIHZhciByZXR1cm5Ub3AgPSB0aGlzLnJldHVyblRvcC5iaW5kKHRoaXMpLFxuICAgICAgYm94ID0gJChvcHRpb25zLmNvbnRhaW5lcikuY2xvc2VzdCgnLmJveCcpLFxuICAgICAgYm94Qm9keSA9ICQob3B0aW9ucy5jb250YWluZXIpLmNsb3Nlc3QoJy5ib3gtYm9keScpLFxuICAgICAgbG9hZGluZyA9ICQoJzxkaXYgY2xhc3M9XCJvdmVybGF5XCI+PGkgY2xhc3M9XCJmYSBmYS1yZWZyZXNoIGZhLXNwaW5cIj48L2k+PC9kaXY+JyksXG4gICAgICBwYWdlQ2xpY2sgPSBmdW5jdGlvbiAoZXZlbnQsIHBhZ2VOdW1iZXIpIHtcbiAgICAgICAgJC5hamF4KHtcbiAgICAgICAgICB1cmw6IG9wdGlvbnMuYXBpLFxuICAgICAgICAgIGRhdGE6IG9wdGlvbnMuZmlsdGVyKHBhZ2VOdW1iZXIpLFxuICAgICAgICAgIGJlZm9yZVNlbmQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICAgIGxvYWRpbmcuYXBwZW5kVG8oYm94KTtcbiAgICAgICAgICB9LFxuICAgICAgICAgIHN1Y2Nlc3M6IGZ1bmN0aW9uIChkYXRhKSB7XG4gICAgICAgICAgICBvcHRpb25zLnJlbmRlcihvcHRpb25zLmNvbnRhaW5lciwgZGF0YS5odG1sKTtcbiAgICAgICAgICAgIGxvYWRpbmcuZGV0YWNoKCk7XG4gICAgICAgICAgICByZXR1cm5Ub3AoYm94Qm9keSk7XG4gICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgIH07XG5cbiAgJC5hamF4KHtcbiAgICB1cmw6IG9wdGlvbnMuYXBpLFxuICAgIGRhdGE6IG9wdGlvbnMuZmlsdGVyKCksXG4gICAgYmVmb3JlU2VuZDogZnVuY3Rpb24gKCkge1xuICAgICAgbG9hZGluZy5hcHBlbmRUbyhib3gpO1xuICAgIH0sXG4gICAgc3VjY2VzczogZnVuY3Rpb24gKGRhdGEpIHtcbiAgICAgIGlmICghZGF0YS5odG1sKSB7XG4gICAgICAgIGxvYWRpbmcuZGV0YWNoKCk7XG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgIH1cbiAgICAgIG9wdGlvbnMucmVuZGVyKG9wdGlvbnMuY29udGFpbmVyLCBkYXRhLmh0bWwpO1xuICAgICAgYm94Qm9keS50d2JzUGFnaW5hdGlvbih7XG4gICAgICAgIHRvdGFsUGFnZXM6IGRhdGEudG90YWwsXG4gICAgICAgIG9uUGFnZUNsaWNrOiBwYWdlQ2xpY2tcbiAgICAgIH0pO1xuICAgICAgbG9hZGluZy5kZXRhY2goKTtcbiAgICB9XG4gIH0pO1xufTtcblxuQXBwLm1vZHVsZS5hYnN0cmFjdCA9IGZ1bmN0aW9uIChvcHRpb25zKSB7XG4gIHZhciBsb2FkaW5nID0gJCgnPGRpdiBjbGFzcz1cIm92ZXJsYXlcIj48aSBjbGFzcz1cImZhIGZhLXJlZnJlc2ggZmEtc3BpblwiPjwvaT48L2Rpdj4nKTtcblxuICBvcHRpb25zID0gJC5leHRlbmQoe1xuICAgIGZlYXR1cmU6ICcnLFxuICAgIGNvbnRhaW5lcjogJycsXG4gICAgcmVuZGVyOiBmdW5jdGlvbiAoY29udGFpbmVyLCBjb250ZW50KSB7XG4gICAgICAkKCc8ZGl2Lz4nKVxuICAgICAgICAuYXR0cih7aWQ6IHRoaXMuZmVhdHVyZSwgY2xhc3M6ICdsaXN0LWdyb3VwIG5vLW1hcmdpbid9KVxuICAgICAgICAuaHRtbChjb250ZW50KVxuICAgICAgICAuZmluZCgnW2RhdGEtdG9nZ2xlPVwidG9vbHRpcFwiXScpXG4gICAgICAgICAgLnRvb2x0aXAoKVxuICAgICAgICAuZW5kKClcbiAgICAgICAgLnJlcGxhY2VBbGwoJChjb250YWluZXIpKTtcbiAgICB9XG4gIH0sIG9wdGlvbnMpO1xuXG4gICQuYWpheCh7XG4gICAgdXJsOiAnL2FwaS8nICsgb3B0aW9ucy5mZWF0dXJlICsgJy8nLFxuICAgIGRhdGE6IHtcbiAgICAgIHR5cGU6ICdhYnN0cmFjdCdcbiAgICB9LFxuICAgIGJlZm9yZVNlbmQ6IGZ1bmN0aW9uICgpIHtcbiAgICAgICQob3B0aW9ucy5jb250YWluZXIpLmNsb3Nlc3QoJy5ib3gnKS5hcHBlbmQobG9hZGluZyk7XG4gICAgfSxcbiAgICBzdWNjZXNzOiBmdW5jdGlvbiAoZGF0YSkge1xuICAgICAgb3B0aW9ucy5yZW5kZXIob3B0aW9ucy5jb250YWluZXIsIGRhdGEuaHRtbCk7XG4gICAgICBsb2FkaW5nLnJlbW92ZSgpO1xuICAgIH1cbiAgfSk7XG59O1xuXG5BcHAubW9kdWxlLmxpc3QgPSBmdW5jdGlvbiAob3B0aW9ucykge1xuICBvcHRpb25zID0gJC5leHRlbmQodHJ1ZSwge1xuICAgIGZlYXR1cmU6ICcnLFxuICAgIGZpbHRlcjoge1xuICAgICAgdHlwZTogJ2xpc3QnLFxuICAgICAgcGFnZTogMVxuICAgIH0sXG4gICAgY29udGFpbmVyOiAnJyxcbiAgICByZW5kZXI6IGZ1bmN0aW9uIChjb250YWluZXIsIGNvbnRlbnQpIHtcbiAgICAgICQoY29udGFpbmVyKS5odG1sKGNvbnRlbnQpO1xuICAgIH0sXG4gICAgdmlzaWJsZVBhZ2VzOiA3XG4gIH0sIG9wdGlvbnMpO1xuXG4gICQuZXh0ZW5kKCQuZm4udHdic1BhZ2luYXRpb24uZGVmYXVsdHMsIHt2aXNpYmxlUGFnZXM6IG9wdGlvbnMudmlzaWJsZVBhZ2VzfSk7XG5cbiAgdmFyIGFwaSA9ICcvYXBpLycgKyBvcHRpb25zLmZlYXR1cmUgKyAnLycsXG4gICAgICBmaWx0ZXIgPSBmdW5jdGlvbiAocGFnZU51bWJlcikge1xuICAgICAgICBpZiAodHlwZW9mIHBhZ2VOdW1iZXIgIT09ICdudW1iZXInKSB7XG4gICAgICAgICAgcmV0dXJuIG9wdGlvbnMuZmlsdGVyO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIHJldHVybiAkLmV4dGVuZCh7fSwgb3B0aW9ucy5maWx0ZXIsIHtwYWdlOiBwYWdlTnVtYmVyfSk7XG4gICAgICAgIH1cbiAgICAgIH07XG5cbiAgdGhpcy5wYWdpbmF0ZSh7XG4gICAgYXBpOiBhcGksXG4gICAgZmlsdGVyOiBmaWx0ZXIsXG4gICAgY29udGFpbmVyOiBvcHRpb25zLmNvbnRhaW5lcixcbiAgICByZW5kZXI6IG9wdGlvbnMucmVuZGVyXG4gIH0pO1xufTtcblxuQXBwLm1vZHVsZS5kZXRhaWwgPSBmdW5jdGlvbiAob3B0aW9ucykge1xuICBvcHRpb25zID0gJC5leHRlbmQodHJ1ZSwge1xuICAgIHBhdGg6ICcnLFxuICAgIGZlYXR1cmU6ICcnLFxuICAgIGNvbnRhaW5lcjogJycsXG4gICAgcmVuZGVyOiBmdW5jdGlvbiAoY29udGFpbmVyLCBjb250ZW50KSB7XG4gICAgICAkKGNvbnRhaW5lcikuaHRtbChjb250ZW50KTtcbiAgICB9XG4gIH0sIG9wdGlvbnMpO1xuXG4gICQuZXh0ZW5kKCQuZm4udHdic1BhZ2luYXRpb24uZGVmYXVsdHMsIHt2aXNpYmxlUGFnZXM6IDd9KTtcblxuICB2YXIgYXBpID0gJy9hcGknICsgb3B0aW9ucy5wYXRoICsgb3B0aW9ucy5mZWF0dXJlICsgJy8nLFxuICAgICAgZmlsdGVyID0gZnVuY3Rpb24gKHBhZ2VOdW1iZXIpIHtcbiAgICAgICAgaWYgKHR5cGVvZiBwYWdlTnVtYmVyICE9PSAnbnVtYmVyJykge1xuICAgICAgICAgIHJldHVybiB7cGFnZTogMX07XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgcmV0dXJuIHtwYWdlOiBwYWdlTnVtYmVyfTtcbiAgICAgICAgfVxuICAgICAgfTtcblxuICB0aGlzLnBhZ2luYXRlKHtcbiAgICBhcGk6IGFwaSxcbiAgICBmaWx0ZXI6IGZpbHRlcixcbiAgICBjb250YWluZXI6IG9wdGlvbnMuY29udGFpbmVyLFxuICAgIHJlbmRlcjogb3B0aW9ucy5yZW5kZXJcbiAgfSk7XG59O1xuXG5BcHAubW9kdWxlLmNvbGxlY3QgPSBmdW5jdGlvbiAodHlwZSwgaWQpIHtcbiAgJCgnLmNvbGxlY3Rpb24nKS5jbGljayhmdW5jdGlvbiAoKSB7XG4gICAgdmFyIHN0YXIgPSAkKHRoaXMpLmZpbmQoJ2knKSxcbiAgICAgICAgdGV4dCA9ICQodGhpcykuZmluZCgnc3BhbicpO1xuXG4gICAgZnVuY3Rpb24gY29sbGVjdChtZXRob2QpIHtcbiAgICAgICQuYWpheCh7XG4gICAgICAgIHR5cGU6IG1ldGhvZCxcbiAgICAgICAgdXJsOiAnL2FwaS9jb2xsZWN0aW9uLycsXG4gICAgICAgIGRhdGE6IHtcbiAgICAgICAgICB0eXBlOiB0eXBlID09PSAnbmV3cycgPyAnYXJ0aWNsZScgOiAndG9waWMnLFxuICAgICAgICAgIGlkOiBpZFxuICAgICAgICB9LFxuICAgICAgICBzdWNjZXNzOiBmdW5jdGlvbiAoZGF0YSkge1xuICAgICAgICAgIGlmIChkYXRhLnN0YXR1cykge1xuICAgICAgICAgICAgc3Rhci50b2dnbGVDbGFzcygnZmEtc3Rhci1vJyk7XG4gICAgICAgICAgICBzdGFyLnRvZ2dsZUNsYXNzKCdmYS1zdGFyJyk7XG4gICAgICAgICAgICB0ZXh0LnRleHQobWV0aG9kID09PSAnUFVUJyA/ICflj5bmtojmlLbol48nIDogJ+a3u+WKoOaUtuiXjycpO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuXG4gICAgaWYgKHN0YXIuaGFzQ2xhc3MoJ2ZhLXN0YXInKSkge1xuICAgICAgY29sbGVjdCgnREVMRVRFJyk7XG4gICAgfSBlbHNlIHtcbiAgICAgIGNvbGxlY3QoJ1BVVCcpO1xuICAgIH1cbiAgfSk7XG59O1xuXG5BcHAubW9kdWxlLmRhdGVSYW5nZSA9IGZ1bmN0aW9uICgkZGF0ZVJhbmdlKSB7XG4gICRkYXRlUmFuZ2VcbiAgICAub24oJ3Nob3cuZGF0ZVJhbmdlJywgZnVuY3Rpb24gKGV2ZW50LCBzdGFydCwgZW5kKSB7XG4gICAgICAkKHRoaXMpLmNoaWxkcmVuKCdzcGFuJykuaHRtbChzdGFydCArICcgfiAnICsgZW5kKTtcbiAgICB9KVxuICAgIC5kYXRlcmFuZ2VwaWNrZXIoe1xuICAgICAgcmFuZ2VzOiB7XG4gICAgICAgICfov4fljrs35aSpJzogW21vbWVudCgpLnN1YnRyYWN0KDYsICdkYXlzJyksIG1vbWVudCgpXSxcbiAgICAgICAgJ+i/h+WOuzMw5aSpJzogW21vbWVudCgpLnN1YnRyYWN0KDI5LCAnZGF5cycpLCBtb21lbnQoKV0sXG4gICAgICAgICfov5nkuKrmnIgnOiBbbW9tZW50KCkuc3RhcnRPZignbW9udGgnKSwgbW9tZW50KCkuZW5kT2YoJ21vbnRoJyldLFxuICAgICAgICAn5LiK5Liq5pyIJzogW21vbWVudCgpLnN1YnRyYWN0KDEsICdtb250aCcpLnN0YXJ0T2YoJ21vbnRoJyksIG1vbWVudCgpLnN1YnRyYWN0KDEsICdtb250aCcpLmVuZE9mKCdtb250aCcpXVxuICAgICAgfSxcbiAgICAgICdsb2NhbGUnOiB7XG4gICAgICAgICdmb3JtYXQnOiAnWVlZWS1NTS1ERCcsXG4gICAgICAgICdzZXBhcmF0b3InOiAnIC0gJyxcbiAgICAgICAgJ2FwcGx5TGFiZWwnOiAn56Gu5a6aJyxcbiAgICAgICAgJ2NhbmNlbExhYmVsJzogJ+WPlua2iCcsXG4gICAgICAgICdmcm9tTGFiZWwnOiAn5LuOJyxcbiAgICAgICAgJ3RvTGFiZWwnOiAn5YiwJyxcbiAgICAgICAgJ2N1c3RvbVJhbmdlTGFiZWwnOiAn6Ieq5a6a5LmJJ1xuICAgICAgfSxcbiAgICAgICdzdGFydERhdGUnOiBtb21lbnQoKS5zdWJ0cmFjdCg2LCAnZGF5cycpLFxuICAgICAgJ2VuZERhdGUnOiBtb21lbnQoKSxcbiAgICAgICdtaW5EYXRlJzogJzIwMTAtMDEtMDEnLFxuICAgICAgJ21heERhdGUnOiBtb21lbnQoKSxcbiAgICAgICdvcGVucyc6ICdsZWZ0JyxcbiAgICAgICdwYXJlbnRFbCc6ICcuY29udGVudC1oZWFkZXInLFxuICAgICAgJ2FwcGx5Q2xhc3MnOiAnYnRuLXN1Y2Nlc3MnLFxuICAgICAgJ2NhbmNlbENsYXNzJzogJ2J0bi1kZWZhdWx0J1xuICAgIH0pO1xufTtcblxuQXBwLm1vZHVsZS5zdGF0aXN0aWMgPSBmdW5jdGlvbigkZWwsIGFwaSkge1xuICAgIHZhciAkdG90YWwgPSAkZWwuZmluZCgnLnN0YXRpc3RpYy10b3RhbCA+IHNwYW4nKSxcbiAgICAgICAgJHJpc2sgPSAkZWwuZmluZCgnLnN0YXRpc3RpYy1yaXNrID4gc3BhbicpO1xuXG4gICAgJGVsLm9uKCdzaG93LnN0YXRpc3RpYycsIGZ1bmN0aW9uKGV2ZW50LCBzdGFydCwgZW5kKSB7XG4gICAgICAgICQuZ2V0SlNPTihhcGksIHtcbiAgICAgICAgICAgIHR5cGU6ICdzdGF0aXN0aWMnLFxuICAgICAgICAgICAgc3RhcnQ6IHN0YXJ0LFxuICAgICAgICAgICAgZW5kOiBlbmRcbiAgICAgICAgfSwgZnVuY3Rpb24oc3RhdGlzdGljKSB7XG4gICAgICAgICAgICAkdG90YWwudGV4dChzdGF0aXN0aWMudG90YWwpO1xuICAgICAgICAgICAgJHJpc2sudGV4dChzdGF0aXN0aWMucmlzayk7XG4gICAgICAgIH0pO1xuICAgIH0pO1xufTsiLCIndXNlIHN0cmljdCc7XG5cbi8vIHVzZXJcbkFwcC5wYWdlLmxvZ2luID0gZnVuY3Rpb24gKG1vZHVsZSkge1xuICBtb2R1bGUubG9naW4oKTtcbn07XG5cbkFwcC5wYWdlLnNldHRpbmdzID0gZnVuY3Rpb24gKG1vZHVsZSkge1xuICBtb2R1bGUuc2V0dGluZ3MoKTtcbn07XG5cbkFwcC5wYWdlLnVzZXIgPSBmdW5jdGlvbiAobW9kdWxlKSB7XG4gIG1vZHVsZS5hZG1pbigpO1xuICBtb2R1bGUucmVnaXN0ZXIoKTtcbn07XG5cbi8vIHV0aWxcbkFwcC5wYWdlLmRhc2hib2FyZCA9IGZ1bmN0aW9uIChtb2R1bGUsIHBhdGgpIHtcbiAgJCgnLmluZm8tYm94LWNvbnRlbnQnKS5lYWNoKGZ1bmN0aW9uIChpbmRleCwgZWxlbWVudCkge1xuICAgIHZhciBpbmZvQm94TnVtYmVyID0gJChlbGVtZW50KS5maW5kKCcuaW5mby1ib3gtbnVtYmVyJyksXG4gICAgICAgIHByb2dyZXNzQmFyID0gJChlbGVtZW50KS5maW5kKCcucHJvZ3Jlc3MtYmFyJyksXG4gICAgICAgIHByb2dyZXNzRGVzY3JpcHRpb24gPSAkKGVsZW1lbnQpLmZpbmQoJy5wcm9ncmVzcy1kZXNjcmlwdGlvbicpLFxuXG4gICAgICAgIGR1cmF0aW9uID0gMjAwMCxcbiAgICAgICAgcmVmcmVzaEludGVydmFsID0gMTAwLFxuICAgICAgICBsb29wID0gTWF0aC5mbG9vcihkdXJhdGlvbiAvIHJlZnJlc2hJbnRlcnZhbCksXG4gICAgICAgIGxvb3BDb3VudCA9IDAsXG5cbiAgICAgICAgbnVtYmVyVmFsdWUgPSAwLFxuICAgICAgICBudW1iZXJGaW5hbCA9ICQoZWxlbWVudCkuZGF0YSgnbnVtYmVyJyksXG4gICAgICAgIG51bWJlckluY3JlbWVudCA9IG51bWJlckZpbmFsIC8gbG9vcCxcblxuICAgICAgICBwZXJjZW50VmFsdWUgPSAwLFxuICAgICAgICBwZXJjZW50RmluYWwgPSAkKGVsZW1lbnQpLmRhdGEoJ3BlcmNlbnQnKSxcbiAgICAgICAgcGVyY2VudEluY3JlbWVudCA9IHBlcmNlbnRGaW5hbCAvIGxvb3AsXG5cbiAgICAgICAgcmVuZGVyID0gZnVuY3Rpb24gKG51bWJlclZhbHVlLCBwZXJjZW50VmFsdWUpIHtcbiAgICAgICAgICBpbmZvQm94TnVtYmVyLnRleHQobnVtYmVyVmFsdWUpO1xuICAgICAgICAgIHByb2dyZXNzQmFyLndpZHRoKHBlcmNlbnRWYWx1ZSArICclJyk7XG4gICAgICAgICAgcHJvZ3Jlc3NEZXNjcmlwdGlvbi50ZXh0KCfljaDmgLvmlbDmja4gJyArIHBlcmNlbnRWYWx1ZSArICclJyk7XG4gICAgICAgIH0sXG5cbiAgICAgICAgaW5jcmVhc2VUbyA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICBpZiAobG9vcENvdW50IDwgbG9vcCkge1xuICAgICAgICAgICAgbnVtYmVyVmFsdWUgKz0gbnVtYmVySW5jcmVtZW50O1xuICAgICAgICAgICAgcGVyY2VudFZhbHVlICs9IHBlcmNlbnRJbmNyZW1lbnQ7XG4gICAgICAgICAgICByZW5kZXIobnVtYmVyVmFsdWUudG9GaXhlZCgpLCBwZXJjZW50VmFsdWUudG9GaXhlZCgpKTtcblxuICAgICAgICAgICAgbG9vcENvdW50Kys7XG4gICAgICAgICAgICBzZXRUaW1lb3V0KGluY3JlYXNlVG8sIHJlZnJlc2hJbnRlcnZhbCk7XG4gICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIG51bWJlclZhbHVlID0gbnVtYmVyRmluYWw7XG4gICAgICAgICAgICBwZXJjZW50VmFsdWUgPSBwZXJjZW50RmluYWw7XG4gICAgICAgICAgICByZW5kZXIobnVtYmVyVmFsdWUsIHBlcmNlbnRWYWx1ZSk7XG4gICAgICAgICAgfVxuICAgICAgICB9O1xuXG4gICAgc2V0VGltZW91dChpbmNyZWFzZVRvLCByZWZyZXNoSW50ZXJ2YWwpO1xuICB9KTtcblxuICBtb2R1bGUuYWJzdHJhY3Qoe1xuICAgIGZlYXR1cmU6ICdyaXNrJyxcbiAgICBjb250YWluZXI6ICcjcmlzayA+IHRib2R5JyxcbiAgICByZW5kZXI6IGZ1bmN0aW9uIChjb250YWluZXIsIGNvbnRlbnQpIHtcbiAgICAgICQoJzx0Ym9keS8+JylcbiAgICAgICAgLmh0bWwoY29udGVudClcbiAgICAgICAgLnNob3dSaXNrKClcbiAgICAgICAgLnJlcGxhY2VBbGwoJChjb250YWluZXIpKTtcbiAgICB9XG4gIH0pO1xuXG4gIG1vZHVsZS5pbnNwZWN0aW9uKCk7XG5cbiAgbW9kdWxlLmFic3RyYWN0KHtcbiAgICBmZWF0dXJlOiAnbmV3cycsXG4gICAgY29udGFpbmVyOiAnI25ld3MnXG4gIH0pO1xuXG4gIG1vZHVsZS5hYnN0cmFjdCh7XG4gICAgZmVhdHVyZTogJ2V2ZW50JyxcbiAgICBjb250YWluZXI6ICcjZXZlbnQnXG4gIH0pO1xuXG4gIG1vZHVsZS5hYnN0cmFjdCh7XG4gICAgZmVhdHVyZTogJ3dlaXhpbicsXG4gICAgY29udGFpbmVyOiAnI3dlaXhpbicsXG4gICAgcmVuZGVyOiBmdW5jdGlvbiAoY29udGFpbmVyLCBjb250ZW50KSB7XG4gICAgICAkKGNvbnRhaW5lcikuaHRtbChjb250ZW50KTtcbiAgICB9XG4gIH0pO1xuXG4gIG1vZHVsZS5hYnN0cmFjdCh7XG4gICAgZmVhdHVyZTogJ3dlaWJvJyxcbiAgICBjb250YWluZXI6ICcjd2VpYm8nLFxuICAgIHJlbmRlcjogZnVuY3Rpb24gKGNvbnRhaW5lciwgY29udGVudCkge1xuICAgICAgJChjb250YWluZXIpLmh0bWwoY29udGVudCk7XG4gICAgfVxuICB9KTtcblxuICBtb2R1bGUubGluZShwYXRoKTtcbiAgbW9kdWxlLnBpZShwYXRoKTtcbn07XG5cbkFwcC5wYWdlLm5ld3MgPSBmdW5jdGlvbiAobW9kdWxlKSB7XG4gIG1vZHVsZS5saXN0KHtcbiAgICBmZWF0dXJlOiAnbmV3cycsXG4gICAgY29udGFpbmVyOiAnI25ld3MgPiB0Ym9keSdcbiAgfSk7XG59O1xuXG5BcHAucGFnZS5uZXdzRGV0YWlsID0gZnVuY3Rpb24gKG1vZHVsZSwgcGF0aCwgdHlwZSwgaWQpIHtcbiAgbW9kdWxlLmNvbGxlY3QodHlwZSwgaWQpO1xufTtcblxuQXBwLnBhZ2UuZXZlbnQgPSBmdW5jdGlvbiAobW9kdWxlKSB7XG4gIG1vZHVsZS5saXN0KHtcbiAgICBmZWF0dXJlOiAnZXZlbnQnLFxuICAgIGNvbnRhaW5lcjogJyNldmVudCA+IHRib2R5J1xuICB9KTtcbn07XG5cbkFwcC5wYWdlLmV2ZW50RGV0YWlsID0gZnVuY3Rpb24gKG1vZHVsZSwgcGF0aCwgdHlwZSwgaWQpIHtcbiAgbW9kdWxlLmNvbGxlY3QodHlwZSwgaWQpO1xuICBtb2R1bGUubGluZShwYXRoLCB0eXBlKTtcbiAgbW9kdWxlLnBpZShwYXRoLCB0eXBlKTtcblxuICBtb2R1bGUuZGV0YWlsKHtcbiAgICBwYXRoOiBwYXRoLFxuICAgIGZlYXR1cmU6ICduZXdzJyxcbiAgICBjb250YWluZXI6ICcjbmV3cyA+IHRib2R5J1xuICB9KTtcblxuICBtb2R1bGUuZGV0YWlsKHtcbiAgICBwYXRoOiBwYXRoLFxuICAgIGZlYXR1cmU6ICd3ZWl4aW4nLFxuICAgIGNvbnRhaW5lcjogJyN3ZWl4aW4nXG4gIH0pO1xuXG4gIG1vZHVsZS5kZXRhaWwoe1xuICAgIHBhdGg6IHBhdGgsXG4gICAgZmVhdHVyZTogJ3dlaWJvJyxcbiAgICBjb250YWluZXI6ICcjd2VpYm8nXG4gIH0pO1xufTtcblxuQXBwLnBhZ2Uud2VpeGluID0gZnVuY3Rpb24gKG1vZHVsZSkge1xuICBtb2R1bGUubGlzdCh7XG4gICAgZmVhdHVyZTogJ3dlaXhpbicsXG4gICAgZmlsdGVyOiB7XG4gICAgICBzb3J0OiAnbmV3J1xuICAgIH0sXG4gICAgY29udGFpbmVyOiAnI3dlaXhpbi1uZXcnLFxuICAgIHZpc2libGVQYWdlczogM1xuICB9KTtcblxuICBtb2R1bGUubGlzdCh7XG4gICAgZmVhdHVyZTogJ3dlaXhpbicsXG4gICAgZmlsdGVyOiB7XG4gICAgICBzb3J0OiAnaG90J1xuICAgIH0sXG4gICAgY29udGFpbmVyOiAnI3dlaXhpbi1ob3QnLFxuICAgIHZpc2libGVQYWdlczogM1xuICB9KTtcbn07XG5cbkFwcC5wYWdlLndlaXhpbkRldGFpbCA9IGZ1bmN0aW9uICgpIHtcbiAgLy8gcGxhY2Vob2xkZXIgZm9yIGZ1dHVyZSB1c2FnZVxufTtcblxuQXBwLnBhZ2Uud2VpYm8gPSBmdW5jdGlvbiAobW9kdWxlKSB7XG4gIG1vZHVsZS5saXN0KHtcbiAgICBmZWF0dXJlOiAnd2VpYm8nLFxuICAgIGZpbHRlcjoge1xuICAgICAgc29ydDogJ25ldydcbiAgICB9LFxuICAgIGNvbnRhaW5lcjogJyN3ZWliby1uZXcnLFxuICAgIHZpc2libGVQYWdlczogM1xuICB9KTtcblxuICBtb2R1bGUubGlzdCh7XG4gICAgZmVhdHVyZTogJ3dlaWJvJyxcbiAgICBmaWx0ZXI6IHtcbiAgICAgIHNvcnQ6ICdob3QnXG4gICAgfSxcbiAgICBjb250YWluZXI6ICcjd2VpYm8taG90JyxcbiAgICB2aXNpYmxlUGFnZXM6IDNcbiAgfSk7XG59O1xuXG5BcHAucGFnZS5jYXRlZ29yeURldGFpbCA9IGZ1bmN0aW9uIChtb2R1bGUsIHBhdGgpIHtcbiAgbW9kdWxlLmRldGFpbCh7XG4gICAgcGF0aDogcGF0aCxcbiAgICBmZWF0dXJlOiAnbmV3cycsXG4gICAgY29udGFpbmVyOiAnI25ld3MgPiB0Ym9keSdcbiAgfSk7XG59O1xuXG5BcHAucGFnZS5sb2NhdGlvbkRldGFpbCA9IGZ1bmN0aW9uIChtb2R1bGUsIHBhdGgpIHtcbiAgbW9kdWxlLmRldGFpbCh7XG4gICAgcGF0aDogcGF0aCxcbiAgICBmZWF0dXJlOiAnbmV3cycsXG4gICAgY29udGFpbmVyOiAnI25ld3MgPiB0Ym9keSdcbiAgfSk7XG5cbiAgbW9kdWxlLmRldGFpbCh7XG4gICAgcGF0aDogcGF0aCxcbiAgICBmZWF0dXJlOiAnd2VpeGluJyxcbiAgICBjb250YWluZXI6ICcjd2VpeGluJ1xuICB9KTtcblxuICBtb2R1bGUuZGV0YWlsKHtcbiAgICBwYXRoOiBwYXRoLFxuICAgIGZlYXR1cmU6ICd3ZWlibycsXG4gICAgY29udGFpbmVyOiAnI3dlaWJvJ1xuICB9KTtcbn07XG5cbkFwcC5wYWdlLmluc3BlY3Rpb24gPSBmdW5jdGlvbiAoKSB7XG4gIC8vIHBlbmRpbmdcbn07XG5cbkFwcC5wYWdlLmN1c3RvbSA9IGZ1bmN0aW9uICgpIHtcbiAgdmFyIGZvcm0gICAgID0gZG9jdW1lbnQuZm9ybXMuYWRkS2V5d29yZCxcbiAgICAgIGFjdGlvbiAgID0gZm9ybS5hY3Rpb24sXG4gICAgICBlbGVtZW50cyA9IGZvcm0uZWxlbWVudHMsXG4gICAgICBmaWVsZHNldCA9IGVsZW1lbnRzWzBdLFxuICAgICAga2V5d29yZCAgPSBlbGVtZW50c1sxXSxcbiAgICAgIGJ1dHRvbiAgID0gZWxlbWVudHNbMl0sXG4gICAgICAkbXNnICAgICA9ICQoZm9ybSkucHJldigpLFxuICAgICAgJGxpc3QgICAgPSAkKGZvcm0pLnBhcmVudCgpLnByZXYoKS5maW5kKCdsaScpLFxuXG4gICAgICBlbmFibGVTdWJtaXQgPSBmdW5jdGlvbiAoKSB7XG4gICAgICAgIGJ1dHRvbi5kaXNhYmxlZCA9ICEoa2V5d29yZC52YWx1ZSk7XG4gICAgICB9LFxuXG4gICAgICBwcm9jZXNzQWRkID0gZnVuY3Rpb24gKGV2ZW50KSB7XG4gICAgICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG5cbiAgICAgICAgJC5wb3N0KGFjdGlvbiwgJChmb3JtKS5zZXJpYWxpemUoKSwgZnVuY3Rpb24gKHJlc3BvbnNlKSB7XG4gICAgICAgICAgaWYgKHJlc3BvbnNlLnN0YXR1cykge1xuICAgICAgICAgICAgJG1zZy50ZXh0KCflhbPplK7or43mt7vliqDmiJDlip/vvIEnKS5zaG93KCk7XG4gICAgICAgICAgICBsb2NhdGlvbi5yZWxvYWQoKTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgJG1zZy50ZXh0KCflhbPplK7or43mt7vliqDlpLHotKXvvIEnKS5zaG93KCk7XG4gICAgICAgICAgICBrZXl3b3JkLnZhbHVlID0gJyc7XG4gICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgIH07XG5cbiAgaWYgKCRsaXN0Lmxlbmd0aCA+PSA1KSB7XG4gICAgZmllbGRzZXQuZGlzYWJsZWQgPSB0cnVlO1xuICB9IGVsc2Uge1xuICAgICQoZm9ybSkua2V5dXAoZW5hYmxlU3VibWl0KS5zdWJtaXQocHJvY2Vzc0FkZCk7XG4gIH1cbn07XG5cbkFwcC5wYWdlLmN1c3RvbURldGFpbCA9IGZ1bmN0aW9uIChtb2R1bGUsIHBhdGgpIHtcbiAgbW9kdWxlLmRldGFpbCh7XG4gICAgcGF0aDogcGF0aCxcbiAgICBmZWF0dXJlOiAnbmV3cycsXG4gICAgY29udGFpbmVyOiAnI25ld3MgPiB0Ym9keSdcbiAgfSk7XG5cbiAgbW9kdWxlLmRldGFpbCh7XG4gICAgcGF0aDogcGF0aCxcbiAgICBmZWF0dXJlOiAnd2VpeGluJyxcbiAgICBjb250YWluZXI6ICcjd2VpeGluJ1xuICB9KTtcblxuICBtb2R1bGUuZGV0YWlsKHtcbiAgICBwYXRoOiBwYXRoLFxuICAgIGZlYXR1cmU6ICd3ZWlibycsXG4gICAgY29udGFpbmVyOiAnI3dlaWJvJ1xuICB9KTtcbn07XG5cbkFwcC5wYWdlLmNvbGxlY3Rpb24gPSBmdW5jdGlvbiAobW9kdWxlLCBwYXRoKSB7XG4gIG1vZHVsZS5kZXRhaWwoe1xuICAgIHBhdGg6IHBhdGgsXG4gICAgZmVhdHVyZTogJ25ld3MnLFxuICAgIGNvbnRhaW5lcjogJyNuZXdzID4gdGJvZHknXG4gIH0pO1xuXG4gIG1vZHVsZS5kZXRhaWwoe1xuICAgIHBhdGg6IHBhdGgsXG4gICAgZmVhdHVyZTogJ2V2ZW50JyxcbiAgICBjb250YWluZXI6ICcjZXZlbnQgPiB0Ym9keSdcbiAgfSk7XG59O1xuXG5BcHAucGFnZS5yaXNrID0gZnVuY3Rpb24gKG1vZHVsZSkge1xuICBtb2R1bGUubGlzdCh7XG4gICAgZmVhdHVyZTogJ3Jpc2snLFxuICAgIGNvbnRhaW5lcjogJyNyaXNrID4gdGJvZHknLFxuICAgIHJlbmRlcjogZnVuY3Rpb24gKGNvbnRhaW5lciwgY29udGVudCkge1xuICAgICAgJCgnPHRib2R5Lz4nKVxuICAgICAgICAuaHRtbChjb250ZW50KVxuICAgICAgICAuc2hvd1Jpc2soKVxuICAgICAgICAucmVwbGFjZUFsbCgkKGNvbnRhaW5lcikpO1xuICAgIH1cbiAgfSk7XG59O1xuXG5BcHAucGFnZS5yaXNrRGV0YWlsID0gZnVuY3Rpb24gKG1vZHVsZSwgcGF0aCwgdHlwZSwgaWQpIHtcbiAgbW9kdWxlLmNvbGxlY3QodHlwZSwgaWQpO1xuICBtb2R1bGUubGluZShwYXRoLCB0eXBlKTtcbiAgbW9kdWxlLnBpZShwYXRoLCB0eXBlKTtcblxuICBtb2R1bGUuZGV0YWlsKHtcbiAgICBwYXRoOiBwYXRoLFxuICAgIGZlYXR1cmU6ICduZXdzJyxcbiAgICBjb250YWluZXI6ICcjbmV3cyA+IHRib2R5J1xuICB9KTtcblxuICBtb2R1bGUuZGV0YWlsKHtcbiAgICBwYXRoOiBwYXRoLFxuICAgIGZlYXR1cmU6ICd3ZWl4aW4nLFxuICAgIGNvbnRhaW5lcjogJyN3ZWl4aW4nXG4gIH0pO1xuXG4gIG1vZHVsZS5kZXRhaWwoe1xuICAgIHBhdGg6IHBhdGgsXG4gICAgZmVhdHVyZTogJ3dlaWJvJyxcbiAgICBjb250YWluZXI6ICcjd2VpYm8nXG4gIH0pO1xufTtcblxuQXBwLnBhZ2UuYW5hbHl0aWNzRGV0YWlsID0gZnVuY3Rpb24gKG1vZHVsZSwgcGF0aCkge1xuICB2YXIgYXBpID0gJy9hcGknICsgcGF0aCxcbiAgICAgICRkYXRlUmFuZ2UgPSAkKCcuZGF0ZS1yYW5nZS1waWNrZXInKSxcbiAgICAgICRjaGFydCA9ICQoJyNjaGFydCcpLFxuICAgICAgJHN0YXRpc3RpYyA9ICQoJyNzdGF0aXN0aWMnKSxcbiAgICAgIHN0YXJ0ID0gbW9tZW50KCkuc3VidHJhY3QoNiwgJ2RheXMnKS5mb3JtYXQoKSxcbiAgICAgIGVuZCA9IG1vbWVudCgpLmZvcm1hdCgpO1xuXG4gIC8vIGluaXQgYW5hbHl0aWNzXG4gIG1vZHVsZS5kYXRlUmFuZ2UoJGRhdGVSYW5nZSk7XG4gICRkYXRlUmFuZ2UudHJpZ2dlcignc2hvdy5kYXRlUmFuZ2UnLCBbc3RhcnQsIGVuZF0pO1xuXG4gICRjaGFydC5vbignc2hvdy5jaGFydCcsIGZ1bmN0aW9uIChldmVudCwgc3RhcnQsIGVuZCkge1xuICAgIHZhciBjaGFydCA9IHt9LFxuICAgICAgbmFtZSA9ICQodGhpcykuZmluZCgnLnRhYi1wYW5lLmFjdGl2ZScpWzBdLmlkLnNsaWNlKDYpLFxuXG4gICAgICBleGNlbCA9IGZ1bmN0aW9uICh0eXBlKSB7XG4gICAgICAgIHZhciBteVRvb2wgPSB7XG4gICAgICAgICAgc2hvdzogdHJ1ZSxcbiAgICAgICAgICB0aXRsZTogJ+S/neWtmOS4ukV4Y2VsJyxcbiAgICAgICAgICBpY29uOiAnaW1hZ2U6Ly8uLi8uLi9zdGF0aWMvaW1nL2V4Y2VsLnBuZycsXG5cbiAgICAgICAgICBvbmNsaWNrOiBmdW5jdGlvbiAoKSB7XG4gICAgICAgICAgICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc2F2ZS1hcy1leGNlbCcpLnNyYyA9IGFwaSArICc/dHlwZT0nK3R5cGUrJyZzdGFydD0nICsgc3RhcnQgKyAnJmVuZD0nICsgZW5kICsgJyZkYXRhdHlwZT14bHMnO1xuICAgICAgICAgIH1cbiAgICAgICAgfTtcbiAgICAgICAgcmV0dXJuIG15VG9vbDtcbiAgICAgICB9O1xuXG4gICAgY2hhcnQudHJlbmQgPSBmdW5jdGlvbiAoc3RhcnQsIGVuZCkge1xuICAgICAgJC5nZXRKU09OKGFwaSwge1xuICAgICAgICB0eXBlOiAnY2hhcnQtdHJlbmQnLFxuICAgICAgICBzdGFydDogc3RhcnQsXG4gICAgICAgIGVuZDogZW5kXG4gICAgICB9LCBmdW5jdGlvbiAoZGF0YSkge1xuICAgICAgICBlY2hhcnRzLmluaXQoZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2NoYXJ0LXRyZW5kJyksICdtYWNhcm9ucycpLnNldE9wdGlvbih7XG4gICAgICAgICAgdG9vbHRpcDoge1xuICAgICAgICAgICAgYmFja2dyb3VuZENvbG9yOiAncmdiYSg1MCw1MCw1MCwwLjUpJyxcbiAgICAgICAgICAgIHRyaWdnZXI6ICdheGlzJyxcbiAgICAgICAgICAgIGF4aXNQb2ludGVyOiB7XG4gICAgICAgICAgICAgIHR5cGU6ICdsaW5lJyxcbiAgICAgICAgICAgICAgbGluZVN0eWxlOiB7XG4gICAgICAgICAgICAgICAgY29sb3I6ICcjMDA4YWNkJyxcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH0sXG4gICAgICAgICAgc2hhZG93U3R5bGU6IHtcbiAgICAgICAgICAgIGNvbG9yOiAncmdiYSgyMDAsMjAwLDIwMCwwLjIpJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgbGVnZW5kOiB7XG4gICAgICAgICAgICBkYXRhOiBbJ+WFqOmDqCcsICfmlrDpl7snLCAn5b6u5Y2aJywgJ+W+ruS/oSddXG4gICAgICAgICAgfSxcbiAgICAgICAgICBncmlkOiB7XG4gICAgICAgICAgICB4OiA1MCxcbiAgICAgICAgICAgIHk6IDMwLFxuICAgICAgICAgICAgeDI6IDI1LFxuICAgICAgICAgICAgeTI6IDY1XG4gICAgICAgICAgfSxcbiAgICAgICAgICB0b29sYm94OiB7XG4gICAgICAgICAgICBzaG93OiB0cnVlLFxuICAgICAgICAgICAgZmVhdHVyZToge1xuICAgICAgICAgICAgICBteVRvb2w6IGV4Y2VsKCdjaGFydC10cmVuZCcpICxcbiAgICAgICAgICAgICAgc2F2ZUFzSW1hZ2U6IHtcbiAgICAgICAgICAgICAgICBzaG93OiB0cnVlXG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9LFxuICAgICAgICAgIGNhbGN1bGFibGU6IHRydWUsXG4gICAgICAgICAgeEF4aXM6IFt7XG4gICAgICAgICAgICB0eXBlOiAnY2F0ZWdvcnknLFxuICAgICAgICAgICAgYm91bmRhcnlHYXA6IGZhbHNlLFxuICAgICAgICAgICAgZGF0YTogZGF0YS5kYXRlXG4gICAgICAgICAgfV0sXG4gICAgICAgICAgeUF4aXM6IFt7XG4gICAgICAgICAgICB0eXBlOiAndmFsdWUnXG4gICAgICAgICAgfV0sXG4gICAgICAgICAgc2VyaWVzOiBbe1xuICAgICAgICAgICAgbmFtZTogJ+WFqOmDqCcsXG4gICAgICAgICAgICB0eXBlOiAnbGluZScsXG4gICAgICAgICAgICBkYXRhOiBkYXRhLnRvdGFsXG4gICAgICAgICAgfSwge1xuICAgICAgICAgICAgbmFtZTogJ+aWsOmXuycsXG4gICAgICAgICAgICB0eXBlOiAnbGluZScsXG4gICAgICAgICAgICBkYXRhOiBkYXRhLm5ld3NcbiAgICAgICAgICB9LCB7XG4gICAgICAgICAgICBuYW1lOiAn5b6u5Y2aJyxcbiAgICAgICAgICAgIHR5cGU6ICdsaW5lJyxcbiAgICAgICAgICAgIGRhdGE6IGRhdGEud2VpYm9cbiAgICAgICAgICB9LCB7XG4gICAgICAgICAgICBuYW1lOiAn5b6u5L+hJyxcbiAgICAgICAgICAgIHR5cGU6ICdsaW5lJyxcbiAgICAgICAgICAgIGRhdGE6IGRhdGEud2VpeGluXG4gICAgICAgICAgfSwgXVxuICAgICAgICB9KTtcbiAgICAgIH0pO1xuICAgIH07XG5cbiAgICBjaGFydC50eXBlID0gZnVuY3Rpb24gKHN0YXJ0LCBlbmQpIHtcbiAgICAgICQuZ2V0SlNPTihhcGksIHtcbiAgICAgICAgdHlwZTogJ2NoYXJ0LXR5cGUnLFxuICAgICAgICBzdGFydDogc3RhcnQsXG4gICAgICAgIGVuZDogZW5kXG4gICAgICB9LCBmdW5jdGlvbiAoZGF0YSkge1xuICAgICAgICBlY2hhcnRzLmluaXQoZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2NoYXJ0LXR5cGUnKSwgJ21hY2Fyb25zJykuc2V0T3B0aW9uKHtcbiAgICAgICAgICB0b29sdGlwOiB7XG4gICAgICAgICAgICBiYWNrZ3JvdW5kQ29sb3I6ICdyZ2JhKDUwLDUwLDUwLDAuNSknLFxuICAgICAgICAgICAgdHJpZ2dlcjogJ2l0ZW0nLFxuICAgICAgICAgICAgZm9ybWF0dGVyOiAne2F9IDxici8+e2J9IDoge2N9ICh7ZH0lKSdcbiAgICAgICAgICB9LFxuICAgICAgICAgIGxlZ2VuZDoge1xuICAgICAgICAgICAgb3JpZW50OiAndmVydGljYWwnLFxuICAgICAgICAgICAgeDogJ2xlZnQnLFxuICAgICAgICAgICAgeTogJ2JvdHRvbScsXG4gICAgICAgICAgICBkYXRhOiBbJ+aWsOmXuycsICflvq7ljZonLCAn5b6u5L+hJ11cbiAgICAgICAgICB9LFxuICAgICAgICAgIHRvb2xib3g6IHtcbiAgICAgICAgICAgIHNob3c6IHRydWUsXG4gICAgICAgICAgICBmZWF0dXJlOiB7XG4gICAgICAgICAgICAgIG15VG9vbDogZXhjZWwoJ2NoYXJ0LXR5cGUnKSxcbiAgICAgICAgICAgICAgc2F2ZUFzSW1hZ2U6IHtcbiAgICAgICAgICAgICAgICBzaG93OiB0cnVlLFxuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSxcbiAgICAgICAgICBjYWxjdWxhYmxlOiB0cnVlLFxuICAgICAgICAgIHNlcmllczogW3tcbiAgICAgICAgICAgIG5hbWU6ICforr/pl67mnaXmupAnLFxuICAgICAgICAgICAgdHlwZTogJ3BpZScsXG4gICAgICAgICAgICByYWRpdXM6ICc1NSUnLFxuICAgICAgICAgICAgY2VudGVyOiBbJzUwJScsICc2MCUnXSxcbiAgICAgICAgICAgIGRhdGE6IFt7XG4gICAgICAgICAgICAgIHZhbHVlOiBkYXRhLm5ld3MsXG4gICAgICAgICAgICAgIG5hbWU6ICfmlrDpl7snXG4gICAgICAgICAgICB9LCB7XG4gICAgICAgICAgICAgIHZhbHVlOiBkYXRhLndlaWJvLFxuICAgICAgICAgICAgICBuYW1lOiAn5b6u5Y2aJ1xuICAgICAgICAgICAgfSwge1xuICAgICAgICAgICAgICB2YWx1ZTogZGF0YS53ZWl4aW4sXG4gICAgICAgICAgICAgIG5hbWU6ICflvq7kv6EnXG4gICAgICAgICAgICB9XVxuICAgICAgICAgIH1dXG4gICAgICAgIH0pO1xuICAgICAgfSk7XG4gICAgfTtcblxuICAgIGNoYXJ0LmVtb3Rpb24gPSBmdW5jdGlvbiAoc3RhcnQsIGVuZCkge1xuICAgICAgJC5nZXRKU09OKGFwaSwge1xuICAgICAgICB0eXBlOiAnY2hhcnQtZW1vdGlvbicsXG4gICAgICAgIHN0YXJ0OiBzdGFydCxcbiAgICAgICAgZW5kOiBlbmRcbiAgICAgIH0sIGZ1bmN0aW9uIChkYXRhKSB7XG4gICAgICAgIGVjaGFydHMuaW5pdChkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnY2hhcnQtZW1vdGlvbicpLCAnbWFjYXJvbnMnKS5zZXRPcHRpb24oe1xuICAgICAgICAgIHRvb2x0aXA6IHtcbiAgICAgICAgICAgIGJhY2tncm91bmRDb2xvcjogJ3JnYmEoNTAsNTAsNTAsMC41KScsXG4gICAgICAgICAgICB0cmlnZ2VyOiAnaXRlbScsXG4gICAgICAgICAgICBmb3JtYXR0ZXI6ICd7YX0gPGJyLz57Yn0gOiB7Y30gKHtkfSUpJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgbGVnZW5kOiB7XG4gICAgICAgICAgICBvcmllbnQ6ICd2ZXJ0aWNhbCcsXG4gICAgICAgICAgICB4OiAnbGVmdCcsXG4gICAgICAgICAgICB5OiAnYm90dG9tJyxcbiAgICAgICAgICAgIGRhdGE6IFsn5q2j6Z2iJywgJ+S4reaApycsICfotJ/pnaInXVxuICAgICAgICAgIH0sXG4gICAgICAgICAgdG9vbGJveDoge1xuICAgICAgICAgICAgc2hvdzogdHJ1ZSxcbiAgICAgICAgICAgIGZlYXR1cmU6IHtcbiAgICAgICAgICAgICAgbWFyazoge1xuICAgICAgICAgICAgICAgIHNob3c6IGZhbHNlXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIG15VG9vbDogZXhjZWwoJ2NoYXJ0LWVtb3Rpb24nKSxcbiAgICAgICAgICAgICAgbWFnaWNUeXBlOiB7XG4gICAgICAgICAgICAgICAgc2hvdzogZmFsc2UsXG4gICAgICAgICAgICAgICAgdHlwZTogWydwaWUnXSxcbiAgICAgICAgICAgICAgICBvcHRpb246IHtcbiAgICAgICAgICAgICAgICAgIGZ1bm5lbDoge1xuICAgICAgICAgICAgICAgICAgICB4OiAnMjUlJyxcbiAgICAgICAgICAgICAgICAgICAgd2lkdGg6ICc1MCUnLFxuICAgICAgICAgICAgICAgICAgICBmdW5uZWxBbGlnbjogJ2xlZnQnLFxuICAgICAgICAgICAgICAgICAgICBtYXg6IDIwMDBcbiAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIHJlc3RvcmU6IHtcbiAgICAgICAgICAgICAgICBzaG93OiBmYWxzZVxuICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICBzYXZlQXNJbWFnZToge1xuICAgICAgICAgICAgICAgIHNob3c6IHRydWVcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH0sXG4gICAgICAgICAgY2FsY3VsYWJsZTogdHJ1ZSxcbiAgICAgICAgICBzZXJpZXM6IFt7XG4gICAgICAgICAgICBuYW1lOiAn6K6/6Zeu5p2l5rqQJyxcbiAgICAgICAgICAgIHR5cGU6ICdwaWUnLFxuICAgICAgICAgICAgcmFkaXVzOiAnNTUlJyxcbiAgICAgICAgICAgIGNlbnRlcjogWyc1MCUnLCAnNjAlJ10sXG4gICAgICAgICAgICBkYXRhOiBbe1xuICAgICAgICAgICAgICB2YWx1ZTogZGF0YS5wb3NpdGl2ZSxcbiAgICAgICAgICAgICAgbmFtZTogJ+ato+mdoidcbiAgICAgICAgICAgIH0sIHtcbiAgICAgICAgICAgICAgdmFsdWU6IGRhdGEubm9ybWFsLFxuICAgICAgICAgICAgICBuYW1lOiAn5Lit5oCnJ1xuICAgICAgICAgICAgfSwge1xuICAgICAgICAgICAgICB2YWx1ZTogZGF0YS5uZWdhdGl2ZSxcbiAgICAgICAgICAgICAgbmFtZTogJ+i0n+mdoidcbiAgICAgICAgICAgIH1dXG4gICAgICAgICAgfV1cbiAgICAgICAgfSk7XG4gICAgICB9KTtcbiAgICB9O1xuXG4gICAgY2hhcnQud2VpYm8gPSBmdW5jdGlvbiAoc3RhcnQsIGVuZCkge1xuICAgICAgJC5nZXRKU09OKGFwaSwge1xuICAgICAgICB0eXBlOiAnY2hhcnQtd2VpYm8nLFxuICAgICAgICBzdGFydDogc3RhcnQsXG4gICAgICAgIGVuZDogZW5kXG4gICAgICB9LCBmdW5jdGlvbiAoZGF0YSkge1xuICAgICAgICBlY2hhcnRzLmluaXQoZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2NoYXJ0LXdlaWJvLW1hcCcpLCAnbWFjYXJvbnMnKS5zZXRPcHRpb24oe1xuICAgICAgICAgIHRvb2x0aXA6IHtcbiAgICAgICAgICAgIHRyaWdnZXI6ICdpdGVtJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgbGVnZW5kOiB7XG4gICAgICAgICAgICBzaG93OiBmYWxzZSxcbiAgICAgICAgICAgIG9yaWVudDogJ3ZlcnRpY2FsJyxcbiAgICAgICAgICAgIHg6ICdsZWZ0JyxcbiAgICAgICAgICAgIGRhdGE6IFsn5b6u5Y2a5paHJ11cbiAgICAgICAgICB9LFxuICAgICAgICAgIGRhdGFSYW5nZToge1xuICAgICAgICAgICAgbWluOiAwLFxuICAgICAgICAgICAgbWF4OiBkYXRhLnZhbHVlWzldLFxuICAgICAgICAgICAgeDogJ2xlZnQnLFxuICAgICAgICAgICAgeTogJ2JvdHRvbScsXG4gICAgICAgICAgICB0ZXh0OiBbJ+mrmCcsICfkvY4nXSxcbiAgICAgICAgICAgIGNhbGN1bGFibGU6IHRydWVcbiAgICAgICAgICB9LFxuICAgICAgICAgIHRvb2xib3g6IHtcbiAgICAgICAgICAgIHNob3c6IHRydWUsXG4gICAgICAgICAgICBvcmllbnQ6ICdob3Jpem9udGFsJyxcbiAgICAgICAgICAgIHg6ICdsZWZ0JyxcbiAgICAgICAgICAgIHk6ICd0b3AnLFxuICAgICAgICAgICAgZmVhdHVyZToge1xuICAgICAgICAgICAgICBteVRvb2w6IGV4Y2VsKCdjaGFydC13ZWlibycpLFxuICAgICAgICAgICAgICBzYXZlQXNJbWFnZToge1xuICAgICAgICAgICAgICAgIHNob3c6IHRydWVcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH0sXG4gICAgICAgICAgcm9hbUNvbnRyb2xsZXI6IHtcbiAgICAgICAgICAgIHNob3c6IHRydWUsXG4gICAgICAgICAgICB4OiAnODUlJyxcbiAgICAgICAgICAgIG1hcFR5cGVDb250cm9sOiB7XG4gICAgICAgICAgICAgICdjaGluYSc6IHRydWVcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9LFxuICAgICAgICAgIHNlcmllczogW3tcbiAgICAgICAgICAgIG5hbWU6ICflvq7ljZrmlocnLFxuICAgICAgICAgICAgdHlwZTogJ21hcCcsXG4gICAgICAgICAgICBtYXBUeXBlOiAnY2hpbmEnLFxuICAgICAgICAgICAgcm9hbTogZmFsc2UsXG4gICAgICAgICAgICBpdGVtU3R5bGU6IHtcbiAgICAgICAgICAgICAgbm9ybWFsOiB7XG4gICAgICAgICAgICAgICAgbGFiZWw6IHtcbiAgICAgICAgICAgICAgICAgIHNob3c6IHRydWVcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIGVtcGhhc2lzOiB7XG4gICAgICAgICAgICAgICAgbGFiZWw6IHtcbiAgICAgICAgICAgICAgICAgIHNob3c6IHRydWVcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBkYXRhOiBkYXRhLnByb3ZpbmNlXG4gICAgICAgICAgfSwgXVxuICAgICAgICB9KTtcblxuICAgICAgICBlY2hhcnRzLmluaXQoZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2NoYXJ0LXdlaWJvLWJhcicpLCAnbWFjYXJvbnMnKS5zZXRPcHRpb24oe1xuICAgICAgICAgIHRpdGxlOiB7XG4gICAgICAgICAgICB0ZXh0OiAn5b6u5Y2a5Zyw5Z+f5YiG5p6QJyxcbiAgICAgICAgICAgIHg6IDQ1XG4gICAgICAgICAgfSxcbiAgICAgICAgICB0b29sdGlwOiB7XG4gICAgICAgICAgICBzaG93OiBmYWxzZSxcbiAgICAgICAgICAgIHRyaWdnZXI6ICdheGlzJyxcbiAgICAgICAgICAgIGF4aXNQb2ludGVyOiB7XG4gICAgICAgICAgICAgIHR5cGU6ICdzaGFkb3cnXG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSxcbiAgICAgICAgICBsZWdlbmQ6IHtcbiAgICAgICAgICAgIHNob3c6IGZhbHNlLFxuICAgICAgICAgICAgZGF0YTogWyflvq7ljZrmlocnXVxuICAgICAgICAgIH0sXG4gICAgICAgICAgdG9vbGJveDoge1xuICAgICAgICAgICAgc2hvdzogZmFsc2UsXG4gICAgICAgICAgICBmZWF0dXJlOiB7XG4gICAgICAgICAgICAgIG1hcms6IHtcbiAgICAgICAgICAgICAgICBzaG93OiB0cnVlXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIG1hZ2ljVHlwZToge1xuICAgICAgICAgICAgICAgIHNob3c6IHRydWUsXG4gICAgICAgICAgICAgICAgdHlwZTogWydsaW5lJywgJ2JhcicsICdzdGFjaycsICd0aWxlZCddXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIHJlc3RvcmU6IHtcbiAgICAgICAgICAgICAgICBzaG93OiB0cnVlXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIHNhdmVBc0ltYWdlOiB7XG4gICAgICAgICAgICAgICAgc2hvdzogdHJ1ZVxuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSxcbiAgICAgICAgICBjYWxjdWxhYmxlOiBmYWxzZSxcbiAgICAgICAgICBncmlkOiB7XG4gICAgICAgICAgICBib3JkZXJXaWR0aDogMFxuICAgICAgICAgIH0sXG4gICAgICAgICAgeEF4aXM6IFt7XG4gICAgICAgICAgICBzaG93OiBmYWxzZSxcbiAgICAgICAgICAgIHR5cGU6ICd2YWx1ZSdcbiAgICAgICAgICB9XSxcbiAgICAgICAgICB5QXhpczogW3tcbiAgICAgICAgICAgIHNob3c6IHRydWUsXG4gICAgICAgICAgICBheGlzTGluZTogZmFsc2UsXG4gICAgICAgICAgICBheGlzVGljazogZmFsc2UsXG4gICAgICAgICAgICB0eXBlOiAnY2F0ZWdvcnknLFxuICAgICAgICAgICAgc3BsaXRMaW5lOiBmYWxzZSxcbiAgICAgICAgICAgIHNwbGl0QXJlYToge1xuICAgICAgICAgICAgICBzaG93OiBmYWxzZVxuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIGF4aXNMYWJlbDoge1xuICAgICAgICAgICAgICBzaG93OiB0cnVlLFxuICAgICAgICAgICAgICB0ZXh0U3R5bGU6IHtcbiAgICAgICAgICAgICAgICBmb250U2l6ZTogMTQsXG4gICAgICAgICAgICAgICAgZm9udFdlaWdodDogJ2JvbGRlcidcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIGRhdGE6IGRhdGEubmFtZVxuICAgICAgICAgIH1dLFxuICAgICAgICAgIHNlcmllczogW3tcbiAgICAgICAgICAgIG5hbWU6ICflvq7ljZrmlocnLFxuICAgICAgICAgICAgdHlwZTogJ2JhcicsXG4gICAgICAgICAgICBzdGFjazogJ+aAu+mHjycsXG4gICAgICAgICAgICBiYXJXaWR0aDogMjAsXG4gICAgICAgICAgICBpdGVtU3R5bGU6IHtcbiAgICAgICAgICAgICAgbm9ybWFsOiB7XG4gICAgICAgICAgICAgICAgbGFiZWw6IHtcbiAgICAgICAgICAgICAgICAgIHNob3c6IHRydWUsXG4gICAgICAgICAgICAgICAgICB0ZXh0U3R5bGU6IHtcbiAgICAgICAgICAgICAgICAgICAgY29sb3I6ICcjMDAwMDAwJyxcbiAgICAgICAgICAgICAgICAgICAgZm9udFNpemU6IDE0LFxuICAgICAgICAgICAgICAgICAgICBmb250V2VpZ2h0OiAnYm9sZGVyJ1xuICAgICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAgIHBvc2l0aW9uOiAncmlnaHQnXG4gICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICBjb2xvcjogJyMzQzhEQkMnXG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBkYXRhOiBkYXRhLnZhbHVlXG4gICAgICAgICAgfV1cbiAgICAgICAgfSk7XG4gICAgICB9KTtcbiAgICB9O1xuXG5cbiAgICAgICAgY2hhcnRbbmFtZV0oc3RhcnQsIGVuZCk7XG4gICAgfSk7XG4gICAgJGNoYXJ0LnRyaWdnZXIoJ3Nob3cuY2hhcnQnLCBbc3RhcnQsIGVuZF0pO1xuXG4gICAgbW9kdWxlLnN0YXRpc3RpYygkc3RhdGlzdGljLCBhcGkpO1xuICAgICRzdGF0aXN0aWMudHJpZ2dlcignc2hvdy5zdGF0aXN0aWMnLCBbc3RhcnQsIGVuZF0pO1xuXG4gICAgLy8gbGlzdGVuIGZvciBjaGFuZ2VcbiAgICAkY2hhcnQub24oJ3Nob3duLmJzLnRhYicsIGZ1bmN0aW9uKCkge1xuICAgICAgICAkY2hhcnQudHJpZ2dlcignc2hvdy5jaGFydCcsIFtzdGFydCwgZW5kXSk7XG4gICAgfSk7XG5cbiAgICAkZGF0ZVJhbmdlLm9uKCdhcHBseS5kYXRlcmFuZ2VwaWNrZXInLCBmdW5jdGlvbihldmVudCwgcGlja2VyKSB7XG4gICAgICAgIHN0YXJ0ID0gcGlja2VyLnN0YXJ0RGF0ZS5mb3JtYXQoKTtcbiAgICAgICAgZW5kID0gcGlja2VyLmVuZERhdGUuZm9ybWF0KCk7XG5cbiAgICAgICAgJGRhdGVSYW5nZS50cmlnZ2VyKCdzaG93LmRhdGVSYW5nZScsIFtzdGFydCwgZW5kXSk7XG4gICAgICAgICRjaGFydC50cmlnZ2VyKCdzaG93LmNoYXJ0JywgW3N0YXJ0LCBlbmRdKTtcbiAgICAgICAgJHN0YXRpc3RpYy50cmlnZ2VyKCdzaG93LnN0YXRpc3RpYycsIFtzdGFydCwgZW5kXSk7XG4gICAgfSk7XG59OyIsIid1c2Ugc3RyaWN0JztcblxuQXBwLnJvdXRlID0gZnVuY3Rpb24gKCkge1xuICB2YXIgbW9kdWxlICA9IHRoaXMubW9kdWxlLFxuICAgICAgcGFnZSAgICA9IHRoaXMucGFnZSxcbiAgICAgIHBhdGggICAgPSBsb2NhdGlvbi5wYXRobmFtZSxcbiAgICAgIHN1bW1hcnkgPSAvXlxcLyhcXHcrKVxcLyQvLFxuICAgICAgZGV0YWlsICA9IC9eXFwvKFxcdyspXFwvKFxcZCspXFwvJC8sXG4gICAgICBtYXRjaCAgID0gbnVsbCxcbiAgICAgIHR5cGUsXG4gICAgICBpZDtcblxuICBzd2l0Y2ggKHRydWUpIHtcbiAgY2FzZSBwYXRoID09PSAnLyc6XG4gICAgdHlwZSAgPSAnZGFzaGJvYXJkJztcbiAgICBicmVhaztcbiAgY2FzZSBzdW1tYXJ5LnRlc3QocGF0aCk6XG4gICAgbWF0Y2ggPSBzdW1tYXJ5LmV4ZWMocGF0aCk7XG4gICAgdHlwZSAgPSBtYXRjaFsxXTtcbiAgICBicmVhaztcbiAgY2FzZSBkZXRhaWwudGVzdChwYXRoKTpcbiAgICBtYXRjaCA9IGRldGFpbC5leGVjKHBhdGgpO1xuICAgIHR5cGUgID0gbWF0Y2hbMV07XG4gICAgaWQgICAgPSArbWF0Y2hbMl07XG4gICAgYnJlYWs7XG4gIH1cblxuICBpZiAodHlwZSA9PT0gJ2xvZ2luJykge1xuICAgIHJldHVybiBwYWdlLmxvZ2luKG1vZHVsZSk7XG4gIH1cblxuICAvLyBjb21tb25cbiAgbW9kdWxlLnNlYXJjaCgpO1xuICBtb2R1bGUubWVudShwYXRoLCB0eXBlKTtcblxuICBpZiAoaWQgPT09IHVuZGVmaW5lZCkge1xuICAgIHJldHVybiBwYWdlW3R5cGVdKG1vZHVsZSwgcGF0aCwgdHlwZSk7XG4gIH0gZWxzZSB7XG4gICAgcmV0dXJuIHBhZ2VbdHlwZSArICdEZXRhaWwnXShtb2R1bGUsIHBhdGgsIHR5cGUsIGlkKTtcbiAgfVxufTtcblxuXG4vL1xuLy8gSW5pdGlhbGl6YXRpb25cbi8vXG5cbiQoZnVuY3Rpb24gKCkge1xuICBBcHAucm91dGUoKTtcbn0pOyJdLCJzb3VyY2VSb290IjoiL3NvdXJjZS8ifQ==
