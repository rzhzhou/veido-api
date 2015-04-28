/*
 * configuration
 */
require.config({
  paths: {
    echarts: "/vendor/echarts"
  }
});


/*
 * custom plugin
 */
$.fn.Do = function(func) {
  this.length && func.apply(this);
  return this;
};

$.fn.Trim = function() {
  var _value = this.find('input').val();
  var value  = $.trim(_value);
  return value;
};


/*
 * functions
 */
var app = {};

app.url = location.pathname;

app.type = location.pathname.split('/')[1] || 'dashboard';

app.user = {
  login: function() {
    var form = this.find('form');
    var msg  = this.find('p');

    form.submit(function(event) {
      event.preventDefault();

      var data = {
        username: $('#username').Trim(),
        password: $('#password').Trim()
      };

      var response = function(data) {
        if (data.status) {
          location.href = location.search.length ? location.search.substr(1).split("=")[1] : "/";
        } else {
          msg.text('用户名或密码错误！');
        }
      };

      if (data.username.length && data.password.length) {
        $.post('/api/login/', data, response, 'json');
      } else {
        msg.text('请输入用户名和密码！');
      }
    });
  },
  change: function() {
    var form = this.find('form');
    var msg  = this.find('p');

    form.submit(function(event) {
      event.preventDefault();

      var data = {
        username:    $('#username').Trim(),
        oldPassword: $('#old-password').Trim(),
        newPassword: $('#new-password').Trim(),
        retype:      $('#retype-password').Trim()
      };

      var response = function(data) {
        if (data.status) {
          msg.text('更新成功！').show();
          location.href = '/login/';
        } else{
          msg.text('原密码错误！').show();
        }
      };

      switch (0) {
        case data.username.length:
          msg.text('请输入姓名！').show();
          break;
        case data.oldPassword.length:
          msg.text('请输入原密码！').show();
          break;
        case data.newPassword.length:
          msg.text('请输入新密码！').show();
          break;
        case data.retype.length:
          msg.text('请确认密码！').show();
          break;
        case Number( data.newPassword === data.retype ):
          msg.text('两次输入密码不一致！').show();
          break;
        default:
          var _data = {
            username:    data.username,
            oldPassword: data.oldPassword,
            newPassword: data.newPassword
          };
          $.post('/api/settings/change/', _data, response, 'json');
          break;
      }
    });
  },
  management: function() {
    var $this  = this;

    var button = $this.find('button');
    var reset  = button.eq(0);
    var remove = button.eq(1);

    var id   = [];

    var action = function(obj, api) {
      obj.click(function() {
        id.length = 0;

        $this.find('input:checked').each(function(index, element) {
          var _id = $(element).parent().next().data('id');
          id.push(_id);
        });

        var response = function(data) {
          if (data.status) {
            location.href = '/user/';
          }
        };

        if (id.length) {
          $.post(api, {id: id.toString()}, response, 'json');
        }
      });
    };

    action(reset, '/api/user/reset/');
    action(remove, '/api/user/remove/');
  },
  add: function() {
    var form = this.find('form');
    var msg  = this.find('p');

    form.submit(function(event) {
      event.preventDefault();

      var data = {
        username: $('#username').Trim(),
        password: $('#password').Trim(),
        retype:   $('#retype-password').Trim()
      };

      var response = function(data) {
        if (data.status) {
          location.href = "/user/";
        } else {
          msg.text('抱歉，注册失败！').show();
        }
      };

      switch (0) {
        case data.username.length:
          msg.text('请输入用户名！').show();
          break;
        case data.password.length:
          msg.text('请输入密码!').show();
          break;
        case data.retype.length:
          msg.text('请确认密码！').show();
          break;
        case Number( data.password === data.retype ):
          msg.text('两次输入密码不一致！').show();
          break;
        default:
          var _data = {
            username: data.username,
            password: data.password
          };
          $.post('/api/user/add/', _data, response, 'json');
          break;
      }
    });
  }
};

app.search = function() {
  this.submit(function(event) {
    event.preventDefault();

    var keywords = $(this).Trim();

    if (keywords.length) {
      location.href = '/search/' + keywords + '/';
    }
  });
};

app.menu = function() {
  var menu  = this.find('a').filter(function() { return this.href === location.href });
  menu.parent().addClass('active');
  menu.closest('.treeview-menu').addClass('menu-open');
  menu.closest('.treeview').addClass('active');
};

app.chart = {
  line: function() {
    require(['echarts', 'echarts/chart/line'], function(ec) {
      $.getJSON('/api/line' + app.url, function(data) {
        ec.init(document.getElementById('line-chart'), 'macarons').setOption({
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
    });
  },
  pie: function() {
    require(['echarts', 'echarts/chart/pie'], function(ec) {
      $.getJSON('/api/pie' + app.url, function(data) {
        ec.init(document.getElementById('pie-chart'), 'macarons').setOption({
          tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
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
    });
  }
};

app.returnTop = function(el) {
  var top = el.offset().top;
  var scrollTop = 0;

  if (top > 160) {
    scrollTop = top - 120;
  }

  $('body').animate({scrollTop: scrollTop});
};

app.table = function() {
  var _this       = this;

  var $content    = this.find('tbody');
  var $pagination = this.parent();
  var type        = this[0].id;

  var renderTable = function(data) {
    var items = data.data;
    var table = $.map(items, function(item, index) {
      var title     = '<td><a href="/' + type + '/' + item.id + '/" title="' + item.title + '" target="_blank">' + item.title + '</a></td>';
      var source    = '<td>' + item.source   + '</td>';
      var location  = '<td>' + item.location + '</td>';
      var time      = '<td>' + item.time     + '</td>';
      var hot       = '<td class="text-center">' + item.hot      + '</td>';

      var row       = '<tr>' + title + source + location + time + hot + '</tr>';
      return row;
    });
    $content.html(table);
  };

  $.getJSON('/api' + app.url + type + '/1/', function(data) {
    renderTable(data);

    $pagination.twbsPagination({
      totalPages: data.total,
      visiblePages: 7,
      first: '第一页',
      prev: '上一页',
      next: '下一页',
      last: '最后一页',
      paginationClass: 'pagination pagination-sm no-margin pull-right',
      onPageClick: function(event, page) {
        app.returnTop(_this);

        $.getJSON('/api' + app.url + type + '/' + page + '/', function(data) {
          renderTable(data);
          $pagination.twbsPagination({totalPages: data.total});
        });
      }
    });
  });
};

app.dataTable = function() {
  $.fn.dataTable.ext.errMode = 'throw';

  var table = this.DataTable({
    "ajax": {
      "url": '/api' + location.pathname,
      "dataSrc": this[0].id,
      "cache": true
    },
    "autoWidth": false,
    "pageLength": 25,
    "order": [],
    "language": {
      "processing":         "处理中...",
      "search":             "",
      "searchPlaceholder":  "输入关键字过滤...",
      "lengthMenu":         "显示 _MENU_ 条",
      "info":               "显示第 _START_ 至 _END_ 条，共 _TOTAL_ 条",
      "infoEmpty":          "信息空",
      "infoFiltered":       "(由 _MAX_ 项结果过滤)",
      "infoPostFix":        "",
      "loadingRecords":     "载入中...",
      "zeroRecords":        "无匹配结果",
      "emptyTable":         "无结果",
      "paginate": {
        "first":            "第一页",
        "previous":         "上一页",
        "next":             "下一页",
        "last":             "最后一页"
      },
      "aria": {
        "sortAscending":    "正序排列",
        "sortDescending":   "倒序排列"
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
    "deferLoading": 100,
    "drawCallback": function() {
      $('[data-toggle="tooltip"]').tooltip();
    }
  });

  table.on('click', 'tr', function() {
    if ( $(this).hasClass('selected') ) {
      $(this).removeClass('selected');
    } else {
      table.$('tr.selected').removeClass('selected');
      $(this).addClass('selected');
    }
  });

  // table.on('draw.dt', function() {
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

app.sns = function() {
  var _this = this;

  this.each(function(index, element) {
    var $content    = $(element);
    var $pagination = $content.parent().next();

    var type = function() {
      if (app.type === 'weixin' || app.type === 'weibo') {
        return $pagination.data('type');
      } else {
        return $pagination.data('type').replace('-', '/');
      }
    };

    $.getJSON('/api' + app.url + type() + '/1/', function(data) {
      $content.html(data.html);

      $pagination.twbsPagination({
        totalPages: data.total,
        first: '第一页',
        prev: '上一页',
        next: '下一页',
        last: '最后一页',
        paginationClass: 'pagination pagination-sm no-margin pull-right',
        onPageClick: function(event, page) {
          app.returnTop(_this);
          $.getJSON('/api' + app.url + type() + '/' + page + '/', function(data) {
            $content.html(data.html);
            $pagination.twbsPagination({totalPages: data.total});
          });
        }
      });
    });
  });
};

app.custom = function() {
  var $custom   = $('.custom'),
      $list     = $custom.find('li'),
      $form     = $custom.find('form'),
      $msg      = $form.prev(),
      $fieldset = $form.find('fieldset'),
      api       = $form.attr('action');

  var response = function(data) {
    if (data.status) {
      $msg.text('关键词添加成功！').show();
      location.reload();
    } else {
      $msg.text('关键词添加失败！').show();
    }
  };

  var addKeyword = function() {
    $form.submit(function(event) {
      event.preventDefault();

      var keyword = $form.Trim();

      if (keyword.length) {
        $.post(api, {keyword: keyword}, response, 'json');
      } else {
        $msg.text('请输入关键词！').show();
      }
    });
  };

  if ( $list.length > 6 ) {
    $fieldset.prop('disabled', true);
  } else {
    addKeyword();
  }
};


/*
 * run function when element exists
 */
$(function() {
  if (app.type === 'login') {
    $('.login-box').Do(app.user.login);
  } else {
    $('aside').find('form').Do(app.search);
    $('aside').Do(app.menu);
    switch (app.type) {
      case 'dashboard':
        $('#line-chart').Do(app.chart.line);
        $('#pie-chart').Do(app.chart.pie);
        break;
      case 'news':
        $('#news').Do(app.table);
        break;
      case 'event':
        $('#event').Do(app.table);
        $('#line-chart').Do(app.chart.line);
        $('#pie-chart').Do(app.chart.pie);
        $('#news').Do(app.table);
        $('.sns').Do(app.sns);
        break;
      case 'weixin':
        // run function on 'weixin' and 'weibo'
      case 'weibo':
        $('.sns').Do(app.sns);
        break;
      case 'category':
        // run function on 'category' and 'location'
      case 'location':
        $('#news').Do(app.table);
        $('.sns').Do(app.sns);
        break;
      case 'inspection':
        $('#inspection').Do(app.dataTable);
        break;
      case 'custom':
        app.custom();
        $('#news').Do(app.table);
        $('.sns').Do(app.sns);
        break;
      case 'collection':
        $('#news').Do(app.table);
        $('#event').Do(app.table);
        break;
      case 'settings':
        $('.user-info').Do(app.user.change);
        break;
      case 'user':
        $('.user-management').Do(app.user.management);
        $('.user-add').Do(app.user.add);
        break;
      case 'search':
        $('#news').Do(app.table);
        $('#event').Do(app.table);
        break;
      default:
        console.log('unknown type');
        break;
    }
  }
});