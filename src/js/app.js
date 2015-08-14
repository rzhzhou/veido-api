/* global moment , echarts */

'use strict';


//
// configuration
//

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

//
// plugins
//
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


//
// Application
//

var App = {
  // Modules
  module: {},

  // Pages
  page: {},

  // Router
  route: function () {
    var module  = this.module,
        page    = this.page,
        path    = location.pathname,
        rule    = /^\/(?:(\w+)\/)?(?:(\d+)\/)?/,
        match   = rule.exec(path).slice(1),
        type    = match[0] === undefined ? 'dashboard' : match[0],
        id      = match[1] === undefined ? undefined : +match[1];

    // console.log('type: ' + type);
    // console.log('id: ' + id);

    if (type === 'login') {
      return page.login(module);
    }

    // common
    module.search();
    module.menu(path, type);

    if (type === 'search') {
      return page.search(module, path);
    }

    if (id === undefined) {
      return page[type](module, path, type);
    } else {
      return page[type + 'Detail'](module, path, type, id);
    }
  }
};


//
// Modules
//

// user
App.module.login = function () {
  var form     = document.forms.login,
      action   = form.action,
      elements = form.elements,
      username = elements.username,
      password = elements.password,
      submit   = elements[2],
      $msg     = $(form).find('p'),

      enableSubmit = function() {
        submit.disabled = !(username.value && password.value);
      },

      processLogin = function(event) {
        event.preventDefault();

        $.post(action, $(form).serialize(), function(response) {
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

      enableSubmit = function() {
        submit.disabled = !(username.value && password.value && retype.value);
      },

      processAdd   = function(event) {
        event.preventDefault();

        var processResponse = function(response) {
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

      action = function(obj, api) {
        obj.click(function() {
          id.length = 0;

          $input.filter(':checked').each(function(index, element) {
            id.push( $(element).parent().next().data('id') );
          });

          if (id.length) {
            $.post(api, {id: id.toString()}, function(response) {
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


      enableSubmit = function() {
        submit.disabled = !(username.value && oldPassword.value && newPassword.value && retype.value);
      },

      processChange = function(event) {
        event.preventDefault();

        var processResponse = function(response) {
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

App.module.map = function (path) {
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
        formatter: function(a) {
          for (var i in city) {
            if (a[1] == city[i].region_name) {
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
        formatter: function(v, v2) {
          if (v2 == '1') {
            return 'A' + '-低风险';
          } else if (v2 == '2') {
            return 'B' + '-中风险';
          } else if (v2 == '3') {
            return 'C' + '-高风险';
          }
        },
        x: "right"
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

  $(form).submit(function(event) {
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

App.module.infoBox = function () {
  var animate = function (index, element) {
    var infoBoxNumber = $(element).find('.info-box-number'),
        progressBar = $(element).find('.progress-bar'),
        progressDescription = $(element).find('.progress-description'),

        duration = 2000,
        refreshInterval = 100,
        loop = Math.floor(duration / refreshInterval),
        loopCount = 0,

        numberValue = 0,
        numberFinal = $(element).data('number'),
        numberIncrement = Math.floor(numberFinal / loop),

        percentValue = 0,
        percentFinal = $(element).data('percent'),
        percentIncrement = Math.floor(percentFinal / loop),

        intervalID,

        countTo = function() {
          numberValue += numberIncrement;
          percentValue += percentIncrement;

          loopCount++;

          if (loopCount >= loop) {
            clearInterval(intervalID);
            numberValue = numberFinal;
            percentValue = percentFinal;
          }

          infoBoxNumber.text( numberValue.toFixed() );
          progressBar.width( percentValue + '%' );
          progressDescription.text( '占总数据 ' + percentValue.toFixed() + '%' );
        };

    intervalID = setInterval(countTo, refreshInterval);
  };

  $('.info-box-content').each(animate);
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

App.module.table = function (module, path) {
  $('.table-custom').each(function () {
    var $this       = $(this),
        $pagination = $this.parent(),
        content     = this.tBodies[0],
        type        = this.id,

        renderTable = function(data) {
          var items = data.data,

              table = $.map(items, function(item) {
                var url       = '/' + type + '/' + item.id + '/',
                    title     = '<td><a href="' + url + '" title="' + item.title + '" target="_blank">' + item.title + '</a></td>',
                    source    = '<td>' + item.source   + '</td>',
                    location  = '<td>' + item.location + '</td>',
                    time      = '<td>' + item.time     + '</td>',
                    hot       = '<td class="text-center">' + item.hot + '</td>',
                    row       = '<tr>' + title + source + location + time + hot + '</tr>';

                return row;
              });

          $(content).html(table);
        };

    $.getJSON('/api' + path + type + '/1/', function(data) {
      renderTable(data);

      $pagination.twbsPagination({
        totalPages: data.total,
        visiblePages: 7,
        onPageClick: function(event, page) {
          module.returnTop($this);

          $.getJSON('/api' + path + type + '/' + page + '/', function(data) {
            renderTable(data);
            $pagination.twbsPagination({totalPages: data.total});
          });
        }
      });
    });
  });
};

App.module.collect = function (type, id) {
  $('.collection').click(function () {
    var star = $(this).find('i'),
        text = $(this).find('span'),

        collect = function(api, nextAction) {
          var data = {
                type: type === 'news' ? 'article' : 'topic',
                id: id
              };

          $.post(api, data, function(response) {
            if (response.status) {
              star.toggleClass('fa-star-o');
              star.toggleClass('fa-star');
              text.text(nextAction);
            }
          });
        };

    if ( star.hasClass('fa-star') ) {
      collect('/api/collection/remove/', '添加收藏');
    } else {
      collect('/api/collection/add/', '取消收藏');
    }
  });
};

App.module.sns = function (module, path, type) {
  var $sns = $('.sns');

  $sns.each(function(index, element) {
    var $content    = $(element),
        $pagination = $content.parent().next(),

        snsType = function() {
          if (type === 'weixin' || type === 'weibo') {
            return $pagination.data('type');
          } else {
            return $pagination.data('type').replace('-', '/');
          }
        };

    $.getJSON('/api' + path + snsType() + '/1/', function(data) {
      $content.html(data.html);

      $pagination.twbsPagination({
        totalPages: data.total,
        onPageClick: function (event, page) {
          module.returnTop($sns);
          $.getJSON('/api' + path + snsType() + '/' + page + '/', function(data) {
            $content.html(data.html);
            $pagination.twbsPagination({totalPages: data.total});
          });
        }
      });
    });
  });
};

App.module.dataTable = function (path) {
  $.fn.dataTable.ext.errMode = 'throw';

  $('.initDataTable').each(function () {
    var table = $(this).DataTable({
      'ajax': {
        'url': '/api' + path,
        'dataSrc': this.id,
        'cache': true
      },
      'autoWidth': false,
      'pageLength': 25,
      'order': [],
      'language': {
        'processing':         '处理中...',
        'search':             '',
        'searchPlaceholder':  '输入关键字过滤...',
        'lengthMenu':         '显示 _MENU_ 条',
        'info':               '显示第 _START_ 至 _END_ 条，共 _TOTAL_ 条',
        'infoEmpty':          '信息空',
        'infoFiltered':       '(由 _MAX_ 项结果过滤)',
        'infoPostFix':        '',
        'loadingRecords':     '载入中...',
        'zeroRecords':        '无匹配结果',
        'emptyTable':         '无结果',
        'paginate': {
          'first':            '第一页',
          'previous':         '上一页',
          'next':             '下一页',
          'last':             '最后一页'
        },
        'aria': {
          'sortAscending':    '正序排列',
          'sortDescending':   '倒序排列'
        }
      },
      // "columnDefs": [{
      //   "className": "star",
      //   "targets": 0,
      //   "searchable": false,
      //   "orderable": false
      // },{
      //   "className": "index",
      //   "targets": -1
      // }],
      'deferLoading': 100,
      'drawCallback': function () {
        $('[data-toggle="tooltip"]').tooltip();
      }
    });

    table.on('click', 'tbody > tr', function () {
      if ( $(this).hasClass('selected') ) {
        $(this).removeClass('selected');
      } else {
        table.$('tr.selected').removeClass('selected');
        $(this).addClass('selected');
      }
    });
  });


  // table.on('draw.dt', function () {
  //   var collection = function(obj, api) {
  //     obj.each(function(index, element) {
  //       $(element).click(function(event) {
  //         event.preventDefault();

  //         var $this = $(this);

  //         var article = $this.parent().next().find('a');
  //         var data = {
  //           id: article.data('id'),
  //           type: article.data('type')
  //         };

  //         var action = function(status) {
  //           if (status) {
  //             $this.toggleClass('fa-star-o');
  //             $this.toggleClass('fa-star');
  //             table.ajax.reload(null, false);
  //           }
  //         };

  //         $.post(api, data, action);
  //       });
  //     });
  //   };

  //   collection( $('.fa-star-o'), '/api/collection/add/');
  //   collection( $('.fa-star'), '/api/collection/remove/');
  // });
};

App.module.custom = function () {
  var form     = document.forms.addKeyword,
      action   = form.action,
      elements = form.elements,
      fieldset = elements[0],
      keyword  = elements[1],
      button   = elements[2],
      $msg     = $(form).prev(),
      $list    = $(form).parent().prev().find('li'),

      enableSubmit = function() {
        button.disabled = !(keyword.value);
      },

      processAdd = function(event) {
        event.preventDefault();

        $.post(action, $(form).serialize(), function(response) {
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

App.module.statistic = function ($el, api) {
  var $total = $el.find('.statistic-total > span'),
      $risk = $el.find('.statistic-risk > span');

  $el.on('show.statistic', function (event, start, end) {
    $.getJSON(api, {
      type: 'statistic',
      start: start,
      end: end
    }, function (statistic) {
      $total.text(statistic.total);
      $risk.text(statistic.risk);
    });
  });
};

App.module.dataList = function (module, $dataList, api, start, end) {
  $dataList.on('showDataList', function () {
    var $paginationContainer = $dataList.parent(),

        toParam = function (pageNumber) {
          if (typeof pageNumber === 'undefined') {
            pageNumber = 1;
          }

          return {
            type: 'data-list',
            start: start,
            end: end,
            page: pageNumber,
          };
        },

        renderTable = function (pageContent) {
          $('<tbody/>')
            .html(pageContent)
            .replaceAll($dataList.find('tbody'));
        };

    $.get(api, toParam(), function (data) {
      renderTable(data.html);

      $paginationContainer.twbsPagination({
        totalPages: data.total,
        visiblePages: 7,
        first: '第一页',
        prev: '上一页',
        next: '下一页',
        last: '最后一页',
        paginationClass: 'pagination pagination-sm no-margin pull-right',
        onPageClick: function(event, pageNumber) {
          module.returnTop($(this));
          $.get(api, toParam(pageNumber), function(data) {
            renderTable(data.html);
            $paginationContainer.twbsPagination({totalPages: data.total});
          });
        }
      });
    });
  });
};


//
// Pages
//

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
App.page.search = function (module, path) {
  module.dataTable(path);
};

App.page.dashboard = function (module, path) {
  module.infoBox();
  module.map(path);
  $('.table-risk').showRisk();
  module.line(path);
  module.pie(path);
  module.inspection();
};

App.page.news = function (module, path) {
  module.table(module, path);
};

App.page.newsDetail = function (module, path, type, id) {
  module.collect(type, id);
};

App.page.event = function (module, path) {
  module.table(module, path);
};

App.page.eventDetail = function (module, path, type, id) {
  module.collect(type, id);
  module.line(path, type);
  module.pie(path, type);
  module.table(module, path);
  module.sns(module, path, type);
};

App.page.weixin = function (module, path, type) {
  module.sns(module, path, type);
};

App.page.weixinDetail = function () {
  // placeholder for future usage
};

App.page.weibo = function (module, path, type) {
  module.sns(module, path, type);
};

App.page.categoryDetail = function (module, path) {
  module.table(module, path);
};

App.page.locationDetail = function (module, path, type) {
  module.table(module, path);
  module.sns(module, path, type);
};

App.page.inspection = function (module, path) {
  module.dataTable(path);
};

App.page.custom = function (module) {
  module.custom();
};

App.page.customDetail = function (module, path, type) {
  module.table(module, path);
  module.sns(module, path, type);
};

App.page.collection = function (module, path) {
  module.table(module, path);
};

App.page.risk = function (module) {
  var $risk = $('#risk'),
      $paginationContainer = $risk.parent(),

      toAPI = function (pageNumber) {
        if (typeof pageNumber === 'undefined') {
          pageNumber = 1;
        }

        return '/api/risk/news/' + pageNumber + '/';
      },

      renderTable = function (pageContent) {
        $('<tbody/>')
          .html(pageContent)
          .showRisk()
          .replaceAll($risk.find('tbody'));
      };

  $.get(toAPI(), function (data) {
    renderTable(data.html);

    $paginationContainer.twbsPagination({
      totalPages: data.total,
      visiblePages: 7,
      onPageClick: function(event, pageNumber) {
        module.returnTop($(this));
        $.get(toAPI(pageNumber), function(data) {
          renderTable(data.html);
          $paginationContainer.twbsPagination({totalPages: data.total});
        });
      }
    });
  });
};

App.page.riskDetail = function (module, path, type, id) {
  module.collect(type, id);
  module.line(path, type);
  module.pie(path, type);
  module.table(module, path);
  module.sns(module, path, type);
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
        name = $(this).find('.tab-pane.active')[0].id.slice(6);

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
              mark: {
                show: false
              },
              dataView: {
                show: true,
                readOnly: false
              },
              magicType: {
                show: false,
                type: ['line']
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
              dataView: {
                show: true,
                readOnly: false
              },
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
              dataView: {
                show: true,
                readOnly: false
              },
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
            }, ]
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
            text: ['高', '低'], // 文本，默认为数值文本
            calculable: true
          },
          toolbox: {
            show: false,
            orient: 'vertical',
            x: 'right',
            y: 'center',
            feature: {
              mark: {
                show: true
              },
              dataView: {
                show: true,
                readOnly: false
              },
              restore: {
                show: true
              },
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
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
              type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
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
              dataView: {
                show: true,
                readOnly: false
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
  $chart.on('shown.bs.tab', function () {
    $chart.trigger('show.chart', [start, end]);
  });

  $dateRange.on('apply.daterangepicker', function (event, picker) {
    start = picker.startDate.format();
    end = picker.endDate.format();

    $dateRange.trigger('show.dateRange', [start, end]);
    $chart.trigger('show.chart', [start, end]);
    $statistic.trigger('show.statistic', [start, end]);
  });
};


//
// Initialization
//

$(function () {
  App.route();
});
