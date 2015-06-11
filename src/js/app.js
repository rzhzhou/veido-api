'use strict';

/*
 * configuration
 */
require.config({
  paths: {
    echarts: '/vendor/echarts'
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
var APP = {};

APP.url = location.pathname;

APP.type = location.pathname.split('/')[1] || 'dashboard';

APP.user = {
  login: function() {
    var form     = document.forms.login,
        action   = form.action,
        elements = form.elements,
        username = elements.username,
        password = elements.password,
        submit   = elements[2],
        $msg     = $(form).find('p');

    var enableSubmit = function() {
      submit.disabled = !(username.value.length && password.value.length);
    };

    var processLogin = function(event) {
      event.preventDefault();

      $.post(action, $(form).serialize(), function(response) {
        if (response.status) {
          location.href = location.search.length ? location.search.substr(1).split('=')[1] : '/';
        } else {
          $msg.text('用户名或密码错误！');
          submit.disabled = true;
          password.value  = '';
        }
      });
    };

    $(form).keyup(enableSubmit).submit(processLogin);
  },

  change: function() {
    var form        = document.forms.info,
        action      = form.action,
        elements    = form.elements,
        username    = elements.username,
        oldPassword = elements.oldPassword,
        newPassword = elements.newPassword,
        retype      = elements.retype,
        submit      = elements[4],
        $msg        = $(form).find('p');


    var enableSubmit = function() {
      submit.disabled = !(username.value.length && oldPassword.value.length && newPassword.value.length && retype.value.length);
    };

    var processChange = function(event) {
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
  },

  admin: function() {
    var $admin  = $('.user-admin'),
        $input  = $admin.find('input'),
        $button = $admin.find('button'),
        $reset  = $button.eq(0),
        $remove = $button.eq(1),
        id      = [];

    var action = function(obj, api) {
      obj.click(function() {
        id.length = 0;

        $input.filter(':checked').each(function(index, element) {
          id.push( $(element).parent().next().data('id') );
        });

        var processResponse = function(data) {
          if (data.status) {
            location.reload();
          }
        };

        if (id.length) {
          $.post(api, {id: id.toString()}, processResponse, 'json');
        }
      });
    };

    action($reset, '/api/user/reset/');
    action($remove, '/api/user/remove/');
  },

  add: function() {
    var form     = document.forms.add,
        action   = form.action,
        elements = form.elements,
        username = elements.username,
        password = elements.password,
        retype   = elements.retype,
        submit   = elements[3],
        $msg     = $(form).find('p');

    var enableSubmit = function() {
      submit.disabled = !(username.value.length && password.value.length && retype.value.length);
    };

    var processAdd   = function(event) {
      event.preventDefault();

      var processResponse = function(response) {
        if (response.status) {
          location.href = '/user/';
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
  }
};

APP.search = function() {
  this.submit(function(event) {
    event.preventDefault();

    var keywords = $(this).Trim();

    if (keywords.length) {
      location.href = '/search/' + keywords + '/';
    }
  });
};

APP.menu = function() {
  var menu  = this.find('a').filter(function() { return this.href === location.href; });
  menu.parent().addClass('active');
  menu.closest('.treeview-menu').addClass('menu-open');
  menu.closest('.treeview').addClass('active');
};

APP.chart = {
  line: function() {
    require(['echarts', 'echarts/chart/line'], function(ec) {
      $.getJSON('/api/line' + APP.url, function(data) {
        ec.init(document.getElementById('line-chart'), 'macarons').setOption({
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
    });
  },
  pie: function() {
    require(['echarts', 'echarts/chart/pie'], function(ec) {
      $.getJSON('/api/pie' + APP.url, function(data) {
        ec.init(document.getElementById('pie-chart'), 'macarons').setOption({
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
    });
  }
};

APP.returnTop = function(el) {
  var top = el.offset().top;
  var scrollTop = 0;

  if (top > 160) {
    scrollTop = top - 120;
  }

  $('body').animate({scrollTop: scrollTop});
};

APP.table = function() {
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

  $.getJSON('/api' + APP.url + type + '/1/', function(data) {
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
        APP.returnTop(_this);

        $.getJSON('/api' + APP.url + type + '/' + page + '/', function(data) {
          renderTable(data);
          $pagination.twbsPagination({totalPages: data.total});
        });
      }
    });
  });
};

APP.dataTable = function() {
  $.fn.dataTable.ext.errMode = 'throw';

  var table = this.DataTable({
    'ajax': {
      'url': '/api' + location.pathname,
      'dataSrc': this[0].id,
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
    'drawCallback': function() {
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

APP.sns = function() {
  var _this = this;

  this.each(function(index, element) {
    var $content    = $(element);
    var $pagination = $content.parent().next();

    var type = function() {
      if (APP.type === 'weixin' || APP.type === 'weibo') {
        return $pagination.data('type');
      } else {
        return $pagination.data('type').replace('-', '/');
      }
    };

    $.getJSON('/api' + APP.url + type() + '/1/', function(data) {
      $content.html(data.html);

      $pagination.twbsPagination({
        totalPages: data.total,
        first: '第一页',
        prev: '上一页',
        next: '下一页',
        last: '最后一页',
        paginationClass: 'pagination pagination-sm no-margin pull-right',
        onPageClick: function(event, page) {
          APP.returnTop(_this);
          $.getJSON('/api' + APP.url + type() + '/' + page + '/', function(data) {
            $content.html(data.html);
            $pagination.twbsPagination({totalPages: data.total});
          });
        }
      });
    });
  });
};

APP.custom = function() {
  var $custom   = $('.custom'),
      $list     = $custom.find('li'),
      $form     = $custom.find('form'),
      $msg      = $form.prev(),
      $fieldset = $form.find('fieldset'),
      api       = $form.attr('action');

  var response = function(data) {
    if (data.status) {
      $msg.text('关键词添加成功！').show();
    } else {
      $msg.text('关键词添加失败！').show();
    }

    setTimeout(function() {
      location.reload();
    }, 1000);
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

  // console.log($list.length >= 5);

  if ( $list.length >= 5 ) {
    $fieldset.prop('disabled', true);
  } else {
    addKeyword();
  }
};


APP.collection = function() {
  var _this = this;

  $('.collection').click(function() {
    var star = $(this).find('i');
    var text = $(this).find('span');

    var collect = function(api, nextAction) {
      var urlArray = _this.url.split('/');
      var data = {
        type: urlArray[1] === 'news' ? 'article' : 'topic',
        id: urlArray[2]
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

APP.dashboard = function() {
  $('.info-box-content').each(function(index, element) {
    var infoBoxNumber = $(element).find('.info-box-number'),
        progressBar = $(element).find('.progress-bar'),
        progressDescription = $(element).find('.progress-description');

    var duration = 3000,
        refreshInterval = 100,
        loop = Math.floor( duration / refreshInterval ),
        loopCount = 0;

    var numberValue = 0,
        numberFinal = $(element).data('number'),
        numberIncrement = Math.floor( numberFinal / loop );

    var percentValue = 0,
        percentFinal = $(element).data('percent'),
        percentIncrement = Math.floor( percentFinal / loop );

    var interval = setInterval(countTo, refreshInterval);

    function countTo() {
      numberValue += numberIncrement;
      percentValue += percentIncrement;

      loopCount++;

      if ( loopCount >= loop ) {
        clearInterval(interval);
        numberValue = numberFinal;
        percentValue = percentFinal;
      }

      infoBoxNumber.text( numberValue.toFixed() );
      progressBar.width( percentValue + '%' );
      progressDescription.text( '占总数据 ' + percentValue.toFixed() + '%' );
    }
  });
};


APP.product = function() {
  $('.filter-list')
    .find('a').filter(function() { return this.href === location.href; })
    .parent().addClass('active');
};

/*
 * run function when element exists
 */
$(function() {
  if (APP.type === 'login') {
    APP.user.login();
  } else {
    $('aside').find('form').Do(APP.search);
    $('aside').Do(APP.menu);
    switch (APP.type) {
      case 'dashboard':
        APP.dashboard();
        $('#line-chart').Do(APP.chart.line);
        $('#pie-chart').Do(APP.chart.pie);
        break;
      case 'news':
        $('#news').Do(APP.table);
        APP.collection();
        break;
      case 'event':
        $('#event').Do(APP.table);
        $('#line-chart').Do(APP.chart.line);
        $('#pie-chart').Do(APP.chart.pie);
        $('#news').Do(APP.table);
        $('.sns').Do(APP.sns);
        APP.collection();
        break;
      case 'weixin':
        // run function on 'weixin' and 'weibo'
      case 'weibo':
        $('.sns').Do(APP.sns);
        break;
      case 'category':
        // run function on 'category' and 'location'
      case 'location':
        $('#news').Do(APP.table);
        $('.sns').Do(APP.sns);
        break;
      case 'inspection':
        $('#inspection').Do(APP.dataTable);
        break;
      case 'custom':
        APP.custom();
        $('#news').Do(APP.table);
        $('.sns').Do(APP.sns);
        break;
      case 'product':
        APP.product();
        $('#news').Do(APP.table);
        break;
      case 'collection':
        $('#news').Do(APP.table);
        $('#event').Do(APP.table);
        break;
      case 'settings':
        APP.user.change();
        break;
      case 'user':
        APP.user.admin();
        APP.user.add();
        break;
      case 'search':
        $('#news').Do(APP.dataTable);
        $('#event').Do(APP.dataTable);
        break;
      default:
        console.log('unknown type');
        break;
    }
  }
});