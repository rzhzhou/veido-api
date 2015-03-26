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
      ec.init(document.getElementById('line-chart'), 'macarons').setOption({
        tooltip : {
          trigger: 'axis'
        },
        legend: {
          data:['正面','中性','负面']
        },
        grid: {
          x: 40,
          y: 30,
          x2: 20,
          y2: 30
        },
        xAxis : [
          {
            type : 'category',
            boundaryGap : false,
            data : ['03-20','03-21','03-22','03-23','03-24','03-25','03-26']
          }
        ],
        yAxis : [
          {
            type : 'value'
          }
        ],
        series : [
          {
            name:'正面',
            type:'line',
            stack: '总量',
            data:[120, 132, 101, 134, 90, 230, 210]
          },
          {
            name:'中性',
            type:'line',
            stack: '总量',
            data:[220, 182, 191, 234, 290, 330, 310]
          },
          {
            name:'负面',
            type:'line',
            stack: '总量',
            data:[150, 232, 201, 154, 190, 330, 410]
          }
        ]
      });
    });
  },
  pie: function() {
    require(['echarts', 'echarts/chart/pie'], function(ec) {
      ec.init(document.getElementById('pie-chart'), 'macarons').setOption({
        tooltip : {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          data:['江岸','洪山','江夏','东西湖']
        },
        series : [
            {
              name:'信息比例',
              type:'pie',
              radius : '55%',
              center: ['50%', '60%'],
              data:[
                {value:335, name:'江岸'},
                {value:310, name:'洪山'},
                {value:234, name:'江夏'},
                {value:135, name:'东西湖'}
              ]
            }
        ]
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
    $.fn.articleData = function() {
      var article = this.parent().next().find('a');
      var data = {
        id: article.data('id'),
        type: article.data('type')
      };
      return data;
    };

    var addCollection = function(index, element) {
      $(element).on('click', function(event) {
        event.preventDefault();
        var that = $(this);
        var data = $(this).articleData();
        var add = function(status) {
          if (status) {
            that.removeClass('fa-star-o').addClass('fa-star');
            table.ajax.reload(null, false);
          }
        };

        $.post('/api/collection/add/', data, add);
      });
    };

    var removeCollection = function(index, element) {
      $(element).on('click', function(event) {
        event.preventDefault();
        var that = $(this);
        var data = $(this).articleData();
        var remove = function(status) {
          if (status) {
            that.removeClass('fa-star').addClass('fa-star-o');
            table.ajax.reload(null, false);
          }
        };

        $.post('/api/collection/remove/', data, remove);
      });
    };

    $('.fa-star-o').each(addCollection);
    $('.fa-star').each(removeCollection);
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