/* jshint camelcase: false, unused: false, latedef: false */
/* globals FastClick */

/*! AdminLTE app.js
 * ================
 * Main JS application file for AdminLTE v2. This file
 * should be included in all pages. It controls some layout
 * options and implements exclusive AdminLTE plugins.
 *
 * @Author  Almsaeed Studio
 * @Support <http://www.almsaeedstudio.com>
 * @Email   <support@almsaeedstudio.com>
 * @version 2.0.5
 * @license MIT <http://opensource.org/licenses/MIT>
 */

'use strict';

//Make sure jQuery has been loaded before app.js
if (typeof jQuery === 'undefined') {
  throw new Error('AdminLTE requires jQuery');
}

/* AdminLTE
 *
 * @type Object
 * @description $.AdminLTE is the main object for the template's app.
 *              It's used for implementing functions and options related
 *              to the template. Keeping everything wrapped in an object
 *              prevents conflict with other plugins and is a better
 *              way to organize our code.
 */
$.AdminLTE = {};

/* --------------------
 * - AdminLTE Options -
 * --------------------
 * Modify these options to suit your implementation
 */
$.AdminLTE.options = {
  //Add slimscroll to navbar menus
  //This requires you to load the slimscroll plugin
  //in every page before app.js
  navbarMenuSlimscroll: false,
  navbarMenuSlimscrollWidth: '3px', //The width of the scroll bar
  navbarMenuHeight: '200px', //The height of the inner menu
  //Sidebar push menu toggle button selector
  sidebarToggleSelector: '[data-toggle="offcanvas"]',
  //Activate sidebar push menu
  sidebarPushMenu: true,
  //Activate sidebar slimscroll if the fixed layout is set (requires SlimScroll Plugin)
  sidebarSlimScroll: false,
  //BoxRefresh Plugin
  enableBoxRefresh: false,
  //Bootstrap.js tooltip
  enableBSToppltip: true,
  BSTooltipSelector: '[data-toggle="tooltip"]',
  //Enable Fast Click. Fastclick.js creates a more
  //native touch experience with touch devices. If you
  //choose to enable the plugin, make sure you load the script
  //before AdminLTE's app.js
  enableFastclick: false,
  //Box Widget Plugin. Enable this plugin
  //to allow boxes to be collapsed and/or removed
  enableBoxWidget: false,
  //Box Widget plugin options
  boxWidgetOptions: {
    boxWidgetIcons: {
      //The icon that triggers the collapse event
      collapse: 'fa fa-minus',
      //The icon that trigger the opening event
      open: 'fa fa-plus',
      //The icon that triggers the removing event
      remove: 'fa fa-times'
    },
    boxWidgetSelectors: {
      //Remove button selector
      remove: '[data-widget="remove"]',
      //Collapse button selector
      collapse: '[data-widget="collapse"]'
    }
  },
  //Direct Chat plugin options
  directChat: {
    //Enable direct chat by default
    enable: false,
    //The button to open and close the chat contacts pane
    contactToggleSelector: '[data-widget="chat-pane-toggle"]'
  },
  //Define the set of colors to use globally around the website
  colors: {
    lightBlue: '#3c8dbc',
    red: '#f56954',
    green: '#00a65a',
    aqua: '#00c0ef',
    yellow: '#f39c12',
    blue: '#0073b7',
    navy: '#001F3F',
    teal: '#39CCCC',
    olive: '#3D9970',
    lime: '#01FF70',
    orange: '#FF851B',
    fuchsia: '#F012BE',
    purple: '#8E24AA',
    maroon: '#D81B60',
    black: '#222222',
    gray: '#d2d6de'
  },
  //The standard screen sizes that bootstrap uses.
  //If you change these in the variables.less file, change
  //them here too.
  screenSizes: {
    xs: 480,
    sm: 768,
    md: 992,
    lg: 1200
  }
};

/* ------------------
 * - Implementation -
 * ------------------
 * The next block of code implements AdminLTE's
 * functions and plugins as specified by the
 * options above.
 */
$(function () {
  //Easy access to options
  var o = $.AdminLTE.options;

  //Set up the object
  _init();

  //Activate the layout maker
  $.AdminLTE.layout.activate();

  //Enable sidebar tree view controls
  $.AdminLTE.tree('.sidebar');

  //Add slimscroll to navbar dropdown
  if (o.navbarMenuSlimscroll && typeof $.fn.slimscroll !== 'undefined') {
    $('.navbar .menu').slimscroll({
      height: '200px',
      alwaysVisible: false,
      size: '3px'
    }).css('width', '100%');
  }

  //Activate sidebar push menu
  if (o.sidebarPushMenu) {
    $.AdminLTE.pushMenu(o.sidebarToggleSelector);
  }

  //Activate Bootstrap tooltip
  if (o.enableBSToppltip) {
    $(o.BSTooltipSelector).tooltip();
  }

  //Activate box widget
  if (o.enableBoxWidget) {
    $.AdminLTE.boxWidget.activate();
  }

  //Activate fast click
  if (o.enableFastclick && typeof FastClick !== 'undefined') {
    FastClick.attach(document.body);
  }

  //Activate direct chat widget
  if (o.directChat.enable) {
    $(o.directChat.contactToggleSelector).click(function () {
      var box = $(this).parents('.direct-chat').first();
      box.toggleClass('direct-chat-contacts-open');
    });
  }

  /*
   * INITIALIZE BUTTON TOGGLE
   * ------------------------
   */
  $('.btn-group[data-toggle="btn-toggle"]').each(function () {
    var group = $(this);
    $(this).find('.btn').click(function (e) {
      group.find('.btn.active').removeClass('active');
      $(this).addClass('active');
      e.preventDefault();
    });

  });
});

/* ----------------------------------
 * - Initialize the AdminLTE Object -
 * ----------------------------------
 * All AdminLTE functions are implemented below.
 */
function _init() {

  /* Layout
   * ======
   * Fixes the layout height in case min-height fails.
   *
   * @type Object
   * @usage $.AdminLTE.layout.activate()
   *        $.AdminLTE.layout.fix()
   *        $.AdminLTE.layout.fixSidebar()
   */
  $.AdminLTE.layout = {
    activate: function () {
      var _this = this;
      $(window).load(function () {
        _this.fix();
        _this.fixSidebar();
      });
      $(window, '.wrapper').resize(function () {
        _this.fix();
        _this.fixSidebar();
      });
    },
    fix: function () {
      //Get window height and the wrapper height
      var neg = $('.main-header').outerHeight() + $('.main-footer').outerHeight();
      var window_height = $(window).height();
      var sidebar_height = $('.sidebar').height();
      //Set the min-height of the content and sidebar based on the
      //the height of the document.
      if ($('body').hasClass('fixed')) {
        $('.content-wrapper, .right-side').css('min-height', window_height - $('.main-footer').outerHeight());
      } else {
        if (window_height >= sidebar_height) {
          $('.content-wrapper, .right-side').css('min-height', window_height - neg);
        } else {
          $('.content-wrapper, .right-side').css('min-height', sidebar_height);
        }
      }
    },
    fixSidebar: function () {
      //Make sure the body tag has the .fixed class
      if (!$('body').hasClass('fixed')) {
        if (typeof $.fn.slimScroll !== 'undefined') {
          $('.sidebar').slimScroll({destroy: true}).height('auto');
        }
        return;
      } else if (typeof $.fn.slimScroll === 'undefined' && console) {
        console.error('Error: the fixed layout requires the slimscroll plugin!');
      }
      //Enable slimscroll for fixed layout
      if ($.AdminLTE.options.sidebarSlimScroll) {
        if (typeof $.fn.slimScroll !== 'undefined') {
          //Distroy if it exists
          $('.sidebar').slimScroll({destroy: true}).height('auto');
          //Add slimscroll
          $('.sidebar').slimscroll({
            height: ($(window).height() - $('.main-header').height()) + 'px',
            color: 'rgba(0,0,0,0.2)',
            size: '3px'
          });
        }
      }
    }
  };

  /* PushMenu()
   * ==========
   * Adds the push menu functionality to the sidebar.
   *
   * @type Function
   * @usage: $.AdminLTE.pushMenu('[data-toggle='offcanvas']')
   */
  $.AdminLTE.pushMenu = function (toggleBtn) {
    //Get the screen sizes
    var screenSizes = this.options.screenSizes;

    //Enable sidebar toggle
    $(toggleBtn).click(function (e) {
      e.preventDefault();

      //Enable sidebar push menu
      if ($(window).width() > (screenSizes.sm - 1)) {
        $('body').toggleClass('sidebar-collapse');
      }
      //Handle sidebar push menu for small screens
      else {
        if ($('body').hasClass('sidebar-open')) {
          $('body').removeClass('sidebar-open');
          $('body').removeClass('sidebar-collapse');
        } else {
          $('body').addClass('sidebar-open');
        }
      }
    });

    $('.content-wrapper').click(function () {
      //Enable hide menu when clicking on the content-wrapper on small screens
      if ($(window).width() <= (screenSizes.sm - 1) && $('body').hasClass('sidebar-open')) {
        $('body').removeClass('sidebar-open');
      }
    });

  };

  /* Tree()
   * ======
   * Converts the sidebar into a multilevel
   * tree view menu.
   *
   * @type Function
   * @Usage: $.AdminLTE.tree('.sidebar')
   */
  $.AdminLTE.tree = function (menu) {
    var _this = this;

    $('li a', $(menu)).click(function (e) {
      //Get the clicked link and the next element
      var $this = $(this);
      var checkElement = $this.next();

      //Check if the next element is a menu and is visible
      if ((checkElement.is('.treeview-menu')) && (checkElement.is(':visible'))) {
        //Close the menu
        checkElement.slideUp('normal', function () {
          checkElement.removeClass('menu-open');
          //Fix the layout in case the sidebar stretches over the height of the window
          //_this.layout.fix();
        });
        checkElement.parent('li').removeClass('active');
      }
      //If the menu is not visible
      else if ((checkElement.is('.treeview-menu')) && (!checkElement.is(':visible'))) {
        //Get the parent menu
        var parent = $this.parents('ul').first();
        //Close all open menus within the parent
        var ul = parent.find('ul:visible').slideUp('normal');
        //Remove the menu-open class from the parent
        ul.removeClass('menu-open');
        //Get the parent li
        var parent_li = $this.parent('li');

        //Open the target menu and add the menu-open class
        checkElement.slideDown('normal', function () {
          //Add the class active to the parent li
          checkElement.addClass('menu-open');
          parent.find('li.active').removeClass('active');
          parent_li.addClass('active');
          //Fix the layout in case the sidebar stretches over the height of the window
          _this.layout.fix();
        });
      }
      //if this isn't a link, prevent the page from being redirected
      if (checkElement.is('.treeview-menu')) {
        e.preventDefault();
      }
    });
  };

  /* BoxWidget
   * =========
   * BoxWidget is plugin to handle collapsing and
   * removing boxes from the screen.
   *
   * @type Object
   * @usage $.AdminLTE.boxWidget.activate()
   *        Set all of your option in the main $.AdminLTE.options object
   */
  $.AdminLTE.boxWidget = {
    activate: function () {
      var o = $.AdminLTE.options;
      var _this = this;
      //Listen for collapse event triggers
      $(o.boxWidgetOptions.boxWidgetSelectors.collapse).click(function (e) {
        e.preventDefault();
        _this.collapse($(this));
      });

      //Listen for remove event triggers
      $(o.boxWidgetOptions.boxWidgetSelectors.remove).click(function (e) {
        e.preventDefault();
        _this.remove($(this));
      });
    },
    collapse: function (element) {
      //Find the box parent
      var box = element.parents('.box').first();
      //Find the body and the footer
      var bf = box.find('.box-body, .box-footer');
      if (!box.hasClass('collapsed-box')) {
        //Convert minus into plus
        element.children('.fa-minus').removeClass('fa-minus').addClass('fa-plus');
        bf.slideUp(300, function () {
          box.addClass('collapsed-box');
        });
      } else {
        //Convert plus into minus
        element.children('.fa-plus').removeClass('fa-plus').addClass('fa-minus');
        bf.slideDown(300, function () {
          box.removeClass('collapsed-box');
        });
      }
    },
    remove: function (element) {
      //Find the box parent
      var box = element.parents('.box').first();
      box.slideUp();
    },
    options: $.AdminLTE.options.boxWidgetOptions
  };
}

/* ------------------
 * - Custom Plugins -
 * ------------------
 * All custom plugins are defined below.
 */

/*
 * BOX REFRESH BUTTON
 * ------------------
 * This is a custom plugin to use with the compenet BOX. It allows you to add
 * a refresh button to the box. It converts the box's state to a loading state.
 *
 * @type plugin
 * @usage $('#box-widget').boxRefresh( options );
 */
(function ($) {

  $.fn.boxRefresh = function (options) {

    // Render options
    var settings = $.extend({
      //Refressh button selector
      trigger: '.refresh-btn',
      //File source to be loaded (e.g: ajax/src.php)
      source: '',
      //Callbacks
      onLoadStart: function (box) {
      }, //Right after the button has been clicked
      onLoadDone: function (box) {
      } //When the source has been loaded

    }, options);

    //The overlay
    var overlay = $('<div class="overlay"><div class="fa fa-refresh fa-spin"></div></div>');

    return this.each(function () {
      //if a source is specified
      if (settings.source === '') {
        if (console) {
          console.log('Please specify a source first - boxRefresh()');
        }
        return;
      }
      //the box
      var box = $(this);
      //the button
      var rBtn = box.find(settings.trigger).first();

      //On trigger click
      rBtn.click(function (e) {
        e.preventDefault();
        //Add loading overlay
        start(box);

        //Perform ajax call
        box.find('.box-body').load(settings.source, function () {
          done(box);
        });
      });
    });

    function start(box) {
      //Add overlay and loading img
      box.append(overlay);

      settings.onLoadStart.call(box);
    }

    function done(box) {
      //Remove overlay and loading img
      box.find(overlay).remove();

      settings.onLoadDone.call(box);
    }

  };

})(jQuery);

/*
 * TODO LIST CUSTOM PLUGIN
 * -----------------------
 * This plugin depends on iCheck plugin for checkbox and radio inputs
 *
 * @type plugin
 * @usage $('#todo-widget').todolist( options );
 */
(function ($) {

  $.fn.todolist = function (options) {
    // Render options
    var settings = $.extend({
      //When the user checks the input
      onCheck: function (ele) {
      },
      //When the user unchecks the input
      onUncheck: function (ele) {
      }
    }, options);

    return this.each(function () {

      if (typeof $.fn.iCheck !== 'undefined') {
        $('input', this).on('ifChecked', function (event) {
          var ele = $(this).parents('li').first();
          ele.toggleClass('done');
          settings.onCheck.call(ele);
        });

        $('input', this).on('ifUnchecked', function (event) {
          var ele = $(this).parents('li').first();
          ele.toggleClass('done');
          settings.onUncheck.call(ele);
        });
      } else {
        $('input', this).on('change', function (event) {
          var ele = $(this).parents('li').first();
          ele.toggleClass('done');
          settings.onCheck.call(ele);
        });
      }
    });
  };
}(jQuery));

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
        text = $(this).find('span'),

        collect = function (api, nextAction) {
          var data = {
                type: type === 'news' ? 'article' : 'topic',
                id: id
              };

          $.post(api, data, function (response) {
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


//
// Initialization
//

$(function () {
  App.route();
});
