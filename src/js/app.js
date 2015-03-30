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
              stack: '总量',
              data: data.positive
            },
            {
              name: '中性',
              type: 'line',
              stack: '总量',
              data: data.neutral
            },
            {
              name: '负面',
              type: 'line',
              stack: '总量',
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

app.table = function() {
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
    "columnDefs": [{
      "className": "star",
      "targets": 0,
      "searchable": false,
      "orderable": false
    },{
      "className": "index",
      "targets": -1
    }],
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

  table.on('draw.dt', function() {
    var collection = function(obj, api) {
      obj.each(function(index, element) {
        $(element).click(function(event) {
          event.preventDefault();

          var $this = $(this);

          var article = $this.parent().next().find('a');
          var data = {
            id: article.data('id'),
            type: article.data('type')
          };

          var action = function(status) {
            if (status) {
              $this.toggleClass('fa-star-o');
              $this.toggleClass('fa-star');
              table.ajax.reload(null, false);
            }
          };

          $.post(api, data, action);
        });
      });
    };

    collection( $('.fa-star-o'), '/api/collection/add/');
    collection( $('.fa-star'), '/api/collection/remove/');
  });
};


/*
 * run function when element exists
 */
$(function() {
  switch (app.url) {
    case "/login/":
      $('.login-box').Do(app.user.login);
      break;
    case "/settings/":
      $('.sidebar-form').Do(app.search);
      $('.user-info').Do(app.user.change);
      break;
    case "/user/":
      $('.sidebar-form').Do(app.search);
      $('.user-management').Do(app.user.management);
      $('.user-add').Do(app.user.add);  
      break;
    default:
      $('.sidebar-form').Do(app.search);
      $('#line-chart').Do(app.chart.line);
      $('#pie-chart').Do(app.chart.pie);
      $('#news').Do(app.table);
      $('#event').Do(app.table);          
      break;
  }
});