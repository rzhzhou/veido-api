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
}

$.fn.Trim = function() {
  var _value = this.find('input').val();
  var value = $.trim(_value);
  return value; 
};


/*
 * functions
 */
var user = {
  login: function() {
    var form = this.find('form');
    var msg = $('.login-box-msg');

    form.submit(function(event) {
      event.preventDefault();

      var data = {
        username: $('#username').Trim(),
        password: $('#password').Trim()
      };

      var response = function(data) {
        if (data) {
          location.href = location.search.length ? location.search.substr(1).split("=")[1] : "/";
        } else {
          msg.text('用户名或密码错误！');
        };
      };

      if (data.username.length && data.password.length) {
        $.post('/api/login', data, response);
      } else {
        msg.text('请输入用户名和密码！');
      };
    });
  }
};

var myChart = {
  line: function() {
    require(['echarts', 'echarts/chart/line'], function(ec) {
      ec.init(document.getElementById('line-chart'), 'macarons').setOption({
        tooltip : {
          trigger: 'axis'
        },
        legend: {
          data:['标准化','稽查打假','质量监管','科技兴检','特种设备']
        },
        grid: {
          x: 40,
          y: 30,
          x2: 10,
          y2: 30
        },
        xAxis : [
          {
            type : 'category',
            boundaryGap : false,
            data : ['周一','周二','周三','周四','周五','周六','周日']
          }
        ],
        yAxis : [
          {
            type : 'value'
          }
        ],
        series : [
          {
            name:'标准化',
            type:'line',
            stack: '总量',
            data:[120, 132, 101, 134, 90, 230, 210]
          },
          {
            name:'稽查打假',
            type:'line',
            stack: '总量',
            data:[220, 182, 191, 234, 290, 330, 310]
          },
          {
            name:'质量监管',
            type:'line',
            stack: '总量',
            data:[150, 232, 201, 154, 190, 330, 410]
          },
          {
            name:'科技兴检',
            type:'line',
            stack: '总量',
            data:[320, 332, 301, 334, 390, 330, 320]
          },
          {
            name:'特种设备',
            type:'line',
            stack: '总量',
            data:[820, 932, 901, 934, 1290, 1330, 1320]
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

var myTable = function() {
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
    }],
    "deferLoading": 100,
    "drawCallback": function(settings) {
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
            dataTable.ajax.reload(null, false);
          };
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
            dataTable.ajax.reload(null, false);
          };
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
  $('.login-box').Do(user.login);

  $('#line-chart').Do(myChart.line);
  $('#pie-chart').Do(myChart.pie);

  $('#news').Do(myTable);
  $('#event').Do(myTable);  
});