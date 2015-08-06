/*! Copyright (c) 2011 Piotr Rochala (http://rocha.la)
 * Dual licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
 * and GPL (http://www.opensource.org/licenses/gpl-license.php) licenses.
 *
 * Version: 1.3.3
 *
 */
(function ($) {

  $.fn.extend({
    slimScroll: function (options) {

      var defaults = {
        // width in pixels of the visible scroll area
        width: 'auto',
        // height in pixels of the visible scroll area
        height: '250px',
        // width in pixels of the scrollbar and rail
        size: '7px',
        // scrollbar color, accepts any hex/color value
        color: '#000',
        // scrollbar position - left/right
        position: 'right',
        // distance in pixels between the side edge and the scrollbar
        distance: '1px',
        // default scroll position on load - top / bottom / $('selector')
        start: 'top',
        // sets scrollbar opacity
        opacity: .4,
        // enables always-on mode for the scrollbar
        alwaysVisible: false,
        // check if we should hide the scrollbar when user is hovering over
        disableFadeOut: false,
        // sets visibility of the rail
        railVisible: false,
        // sets rail color
        railColor: '#333',
        // sets rail opacity
        railOpacity: .2,
        // whether  we should use jQuery UI Draggable to enable bar dragging
        railDraggable: true,
        // defautlt CSS class of the slimscroll rail
        railClass: 'slimScrollRail',
        // defautlt CSS class of the slimscroll bar
        barClass: 'slimScrollBar',
        // defautlt CSS class of the slimscroll wrapper
        wrapperClass: 'slimScrollDiv',
        // check if mousewheel should scroll the window if we reach top/bottom
        allowPageScroll: false,
        // scroll amount applied to each mouse wheel step
        wheelStep: 20,
        // scroll amount applied when user is using gestures
        touchScrollStep: 200,
        // sets border radius
        borderRadius: '7px',
        // sets border radius of the rail
        railBorderRadius: '7px'
      };

      var o = $.extend(defaults, options);

      // do it for every element that matches selector
      this.each(function () {

        var isOverPanel, isOverBar, isDragg, queueHide, touchDif,
                barHeight, percentScroll, lastScroll,
                divS = '<div></div>',
                minBarHeight = 30,
                releaseScroll = false;

        // used in event handlers and for better minification
        var me = $(this);

        // ensure we are not binding it again
        if (me.parent().hasClass(o.wrapperClass))
        {
          // start from last bar position
          var offset = me.scrollTop();

          // find bar and rail
          bar = me.parent().find('.' + o.barClass);
          rail = me.parent().find('.' + o.railClass);

          getBarHeight();

          // check if we should scroll existing instance
          if ($.isPlainObject(options))
          {
            // Pass height: auto to an existing slimscroll object to force a resize after contents have changed
            if ('height' in options && options.height == 'auto') {
              me.parent().css('height', 'auto');
              me.css('height', 'auto');
              var height = me.parent().parent().height();
              me.parent().css('height', height);
              me.css('height', height);
            }

            if ('scrollTo' in options)
            {
              // jump to a static point
              offset = parseInt(o.scrollTo);
            }
            else if ('scrollBy' in options)
            {
              // jump by value pixels
              offset += parseInt(o.scrollBy);
            }
            else if ('destroy' in options)
            {
              // remove slimscroll elements
              bar.remove();
              rail.remove();
              me.unwrap();
              return;
            }

            // scroll content by the given offset
            scrollContent(offset, false, true);
          }

          return;
        }
        else if ($.isPlainObject(options))
        {
          if ('destroy' in options)
          {
            return;
          }
        }

        // optionally set height to the parent's height
        o.height = (o.height == 'auto') ? me.parent().height() : o.height;

        // wrap content
        var wrapper = $(divS)
                .addClass(o.wrapperClass)
                .css({
                  position: 'relative',
                  overflow: 'hidden',
                  width: o.width,
                  height: o.height
                });

        // update style for the div
        me.css({
          overflow: 'hidden',
          width: o.width,
          height: o.height,
          //Fix for IE10
          "-ms-touch-action": "none"
        });

        // create scrollbar rail
        var rail = $(divS)
                .addClass(o.railClass)
                .css({
                  width: o.size,
                  height: '100%',
                  position: 'absolute',
                  top: 0,
                  display: (o.alwaysVisible && o.railVisible) ? 'block' : 'none',
                  'border-radius': o.railBorderRadius,
                  background: o.railColor,
                  opacity: o.railOpacity,
                  zIndex: 90
                });

        // create scrollbar
        var bar = $(divS)
                .addClass(o.barClass)
                .css({
                  background: o.color,
                  width: o.size,
                  position: 'absolute',
                  top: 0,
                  opacity: o.opacity,
                  display: o.alwaysVisible ? 'block' : 'none',
                  'border-radius': o.borderRadius,
                  BorderRadius: o.borderRadius,
                  MozBorderRadius: o.borderRadius,
                  WebkitBorderRadius: o.borderRadius,
                  zIndex: 99
                });

        // set position
        var posCss = (o.position == 'right') ? {right: o.distance} : {left: o.distance};
        rail.css(posCss);
        bar.css(posCss);

        // wrap it
        me.wrap(wrapper);

        // append to parent div
        me.parent().append(bar);
        me.parent().append(rail);

        // make it draggable and no longer dependent on the jqueryUI
        if (o.railDraggable) {
          bar.bind("mousedown", function (e) {
            var $doc = $(document);
            isDragg = true;
            t = parseFloat(bar.css('top'));
            pageY = e.pageY;

            $doc.bind("mousemove.slimscroll", function (e) {
              currTop = t + e.pageY - pageY;
              bar.css('top', currTop);
              scrollContent(0, bar.position().top, false);// scroll content
            });

            $doc.bind("mouseup.slimscroll", function (e) {
              isDragg = false;
              hideBar();
              $doc.unbind('.slimscroll');
            });
            return false;
          }).bind("selectstart.slimscroll", function (e) {
            e.stopPropagation();
            e.preventDefault();
            return false;
          });
        }

        // on rail over
        rail.hover(function () {
          showBar();
        }, function () {
          hideBar();
        });

        // on bar over
        bar.hover(function () {
          isOverBar = true;
        }, function () {
          isOverBar = false;
        });

        // show on parent mouseover
        me.hover(function () {
          isOverPanel = true;
          showBar();
          hideBar();
        }, function () {
          isOverPanel = false;
          hideBar();
        });

        if (window.navigator.msPointerEnabled) {          
          // support for mobile
          me.bind('MSPointerDown', function (e, b) {
            if (e.originalEvent.targetTouches.length)
            {
              // record where touch started
              touchDif = e.originalEvent.targetTouches[0].pageY;
            }
          });

          me.bind('MSPointerMove', function (e) {
            // prevent scrolling the page if necessary
            e.originalEvent.preventDefault();
            if (e.originalEvent.targetTouches.length)
            {
              // see how far user swiped
              var diff = (touchDif - e.originalEvent.targetTouches[0].pageY) / o.touchScrollStep;
              // scroll content
              scrollContent(diff, true);
              touchDif = e.originalEvent.targetTouches[0].pageY;
              
            }
          });
        } else {
          // support for mobile
          me.bind('touchstart', function (e, b) {
            if (e.originalEvent.touches.length)
            {
              // record where touch started
              touchDif = e.originalEvent.touches[0].pageY;
            }
          });

          me.bind('touchmove', function (e) {
            // prevent scrolling the page if necessary
            if (!releaseScroll)
            {
              e.originalEvent.preventDefault();
            }
            if (e.originalEvent.touches.length)
            {
              // see how far user swiped
              var diff = (touchDif - e.originalEvent.touches[0].pageY) / o.touchScrollStep;
              // scroll content
              scrollContent(diff, true);
              touchDif = e.originalEvent.touches[0].pageY;
            }
          });
        }

        // set up initial height
        getBarHeight();

        // check start position
        if (o.start === 'bottom')
        {
          // scroll content to bottom
          bar.css({top: me.outerHeight() - bar.outerHeight()});
          scrollContent(0, true);
        }
        else if (o.start !== 'top')
        {
          // assume jQuery selector
          scrollContent($(o.start).position().top, null, true);

          // make sure bar stays hidden
          if (!o.alwaysVisible) {
            bar.hide();
          }
        }

        // attach scroll events
        attachWheel();

        function _onWheel(e)
        {
          // use mouse wheel only when mouse is over
          if (!isOverPanel) {
            return;
          }

          var e = e || window.event;

          var delta = 0;
          if (e.wheelDelta) {
            delta = -e.wheelDelta / 120;
          }
          if (e.detail) {
            delta = e.detail / 3;
          }

          var target = e.target || e.srcTarget || e.srcElement;
          if ($(target).closest('.' + o.wrapperClass).is(me.parent())) {
            // scroll content
            scrollContent(delta, true);
          }

          // stop window scroll
          if (e.preventDefault && !releaseScroll) {
            e.preventDefault();
          }
          if (!releaseScroll) {
            e.returnValue = false;
          }
        }

        function scrollContent(y, isWheel, isJump)
        {
          releaseScroll = false;
          var delta = y;
          var maxTop = me.outerHeight() - bar.outerHeight();

          if (isWheel)
          {
            // move bar with mouse wheel
            delta = parseInt(bar.css('top')) + y * parseInt(o.wheelStep) / 100 * bar.outerHeight();

            // move bar, make sure it doesn't go out
            delta = Math.min(Math.max(delta, 0), maxTop);

            // if scrolling down, make sure a fractional change to the
            // scroll position isn't rounded away when the scrollbar's CSS is set
            // this flooring of delta would happened automatically when
            // bar.css is set below, but we floor here for clarity
            delta = (y > 0) ? Math.ceil(delta) : Math.floor(delta);

            // scroll the scrollbar
            bar.css({top: delta + 'px'});
          }

          // calculate actual scroll amount
          percentScroll = parseInt(bar.css('top')) / (me.outerHeight() - bar.outerHeight());
          delta = percentScroll * (me[0].scrollHeight - me.outerHeight());

          if (isJump)
          {
            delta = y;
            var offsetTop = delta / me[0].scrollHeight * me.outerHeight();
            offsetTop = Math.min(Math.max(offsetTop, 0), maxTop);
            bar.css({top: offsetTop + 'px'});
          }

          // scroll content
          me.scrollTop(delta);

          // fire scrolling event
          me.trigger('slimscrolling', ~~delta);

          // ensure bar is visible
          showBar();

          // trigger hide when scroll is stopped
          hideBar();
        }

        function attachWheel()
        {
          if (window.addEventListener)
          {
            this.addEventListener('DOMMouseScroll', _onWheel, false);
            this.addEventListener('mousewheel', _onWheel, false);
          }
          else
          {
            document.attachEvent("onmousewheel", _onWheel)
          }
        }

        function getBarHeight()
        {
          // calculate scrollbar height and make sure it is not too small
          barHeight = Math.max((me.outerHeight() / me[0].scrollHeight) * me.outerHeight(), minBarHeight);
          bar.css({height: barHeight + 'px'});

          // hide scrollbar if content is not long enough
          var display = barHeight == me.outerHeight() ? 'none' : 'block';
          bar.css({display: display});
        }

        function showBar()
        {
          // recalculate bar height
          getBarHeight();
          clearTimeout(queueHide);

          // when bar reached top or bottom
          if (percentScroll == ~~percentScroll)
          {
            //release wheel
            releaseScroll = o.allowPageScroll;

            // publish approporiate event
            if (lastScroll != percentScroll)
            {
              var msg = (~~percentScroll == 0) ? 'top' : 'bottom';
              me.trigger('slimscroll', msg);
            }
          }
          else
          {
            releaseScroll = false;
          }
          lastScroll = percentScroll;

          // show only when required
          if (barHeight >= me.outerHeight()) {
            //allow window scroll
            releaseScroll = true;
            return;
          }
          bar.stop(true, true).fadeIn('fast');
          if (o.railVisible) {
            rail.stop(true, true).fadeIn('fast');
          }
        }

        function hideBar()
        {
          // only hide when options allow it
          if (!o.alwaysVisible)
          {
            queueHide = setTimeout(function () {
              if (!(o.disableFadeOut && isOverPanel) && !isOverBar && !isDragg)
              {
                bar.fadeOut('slow');
                rail.fadeOut('slow');
              }
            }, 1000);
          }
        }

      });

      // maintain chainability
      return this;
    }
  });

  $.fn.extend({
    slimscroll: $.fn.slimScroll
  });

})(jQuery);

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
if (typeof jQuery === "undefined") {
  throw new Error("AdminLTE requires jQuery");
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
  navbarMenuSlimscroll: true,
  navbarMenuSlimscrollWidth: "3px", //The width of the scroll bar
  navbarMenuHeight: "200px", //The height of the inner menu
  //Sidebar push menu toggle button selector
  sidebarToggleSelector: "[data-toggle='offcanvas']",
  //Activate sidebar push menu
  sidebarPushMenu: true,
  //Activate sidebar slimscroll if the fixed layout is set (requires SlimScroll Plugin)
  sidebarSlimScroll: true,
  //BoxRefresh Plugin
  enableBoxRefresh: true,
  //Bootstrap.js tooltip
  enableBSToppltip: true,
  BSTooltipSelector: "[data-toggle='tooltip']",
  //Enable Fast Click. Fastclick.js creates a more
  //native touch experience with touch devices. If you
  //choose to enable the plugin, make sure you load the script
  //before AdminLTE's app.js
  enableFastclick: true,
  //Box Widget Plugin. Enable this plugin
  //to allow boxes to be collapsed and/or removed
  enableBoxWidget: true,
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
    enable: true,
    //The button to open and close the chat contacts pane
    contactToggleSelector: '[data-widget="chat-pane-toggle"]'
  },
  //Define the set of colors to use globally around the website
  colors: {
    lightBlue: "#3c8dbc",
    red: "#f56954",
    green: "#00a65a",
    aqua: "#00c0ef",
    yellow: "#f39c12",
    blue: "#0073b7",
    navy: "#001F3F",
    teal: "#39CCCC",
    olive: "#3D9970",
    lime: "#01FF70",
    orange: "#FF851B",
    fuchsia: "#F012BE",
    purple: "#8E24AA",
    maroon: "#D81B60",
    black: "#222222",
    gray: "#d2d6de"
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
  if (o.navbarMenuSlimscroll && typeof $.fn.slimscroll != 'undefined') {
    $(".navbar .menu").slimscroll({
      height: "200px",
      alwaysVisible: false,
      size: "3px"
    }).css("width", "100%");
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
  if (o.enableFastclick && typeof FastClick != 'undefined') {
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
    $(this).find(".btn").click(function (e) {
      group.find(".btn.active").removeClass("active");
      $(this).addClass("active");
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
      _this.fix();
      _this.fixSidebar();
      $(window, ".wrapper").resize(function () {
        _this.fix();
        _this.fixSidebar();
      });
    },
    fix: function () {
      //Get window height and the wrapper height
      var neg = $('.main-header').outerHeight() + $('.main-footer').outerHeight();
      var window_height = $(window).height();
      var sidebar_height = $(".sidebar").height();
      //Set the min-height of the content and sidebar based on the
      //the height of the document.
      if ($("body").hasClass("fixed")) {
        $(".content-wrapper, .right-side").css('min-height', window_height - $('.main-footer').outerHeight());
      } else {
        if (window_height >= sidebar_height) {
          $(".content-wrapper, .right-side").css('min-height', window_height - neg);
        } else {
          $(".content-wrapper, .right-side").css('min-height', sidebar_height);
        }
      }
    },
    fixSidebar: function () {
      //Make sure the body tag has the .fixed class
      if (!$("body").hasClass("fixed")) {
        if (typeof $.fn.slimScroll != 'undefined') {
          $(".sidebar").slimScroll({destroy: true}).height("auto");
        }
        return;
      } else if (typeof $.fn.slimScroll == 'undefined' && console) {
        console.error("Error: the fixed layout requires the slimscroll plugin!");
      }
      //Enable slimscroll for fixed layout
      if ($.AdminLTE.options.sidebarSlimScroll) {
        if (typeof $.fn.slimScroll != 'undefined') {
          //Distroy if it exists
          $(".sidebar").slimScroll({destroy: true}).height("auto");
          //Add slimscroll
          $(".sidebar").slimscroll({
            height: ($(window).height() - $(".main-header").height()) + "px",
            color: "rgba(0,0,0,0.2)",
            size: "3px"
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
   * @usage: $.AdminLTE.pushMenu("[data-toggle='offcanvas']")
   */
  $.AdminLTE.pushMenu = function (toggleBtn) {
    //Get the screen sizes
    var screenSizes = this.options.screenSizes;

    //Enable sidebar toggle
    $(toggleBtn).click(function (e) {
      e.preventDefault();

      //Enable sidebar push menu
      if ($(window).width() > (screenSizes.sm - 1)) {
        $("body").toggleClass('sidebar-collapse');
      }
      //Handle sidebar push menu for small screens
      else {
        if ($("body").hasClass('sidebar-open')) {
          $("body").removeClass('sidebar-open');
          $("body").removeClass('sidebar-collapse')
        } else {
          $("body").addClass('sidebar-open');
        }
      }
    });

    $(".content-wrapper").click(function () {
      //Enable hide menu when clicking on the content-wrapper on small screens
      if ($(window).width() <= (screenSizes.sm - 1) && $("body").hasClass("sidebar-open")) {
        $("body").removeClass('sidebar-open');
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

    $("li a", $(menu)).click(function (e) {
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
        checkElement.parent("li").removeClass("active");
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
        var parent_li = $this.parent("li");

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
      var box = element.parents(".box").first();
      //Find the body and the footer
      var bf = box.find(".box-body, .box-footer");
      if (!box.hasClass("collapsed-box")) {
        //Convert minus into plus
        element.children(".fa-minus").removeClass("fa-minus").addClass("fa-plus");
        bf.slideUp(300, function () {
          box.addClass("collapsed-box");
        });
      } else {
        //Convert plus into minus
        element.children(".fa-plus").removeClass("fa-plus").addClass("fa-minus");
        bf.slideDown(300, function () {
          box.removeClass("collapsed-box");
        });
      }
    },
    remove: function (element) {
      //Find the box parent
      var box = element.parents(".box").first();
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
 * @usage $("#box-widget").boxRefresh( options );
 */
(function ($) {

  $.fn.boxRefresh = function (options) {

    // Render options
    var settings = $.extend({
      //Refressh button selector
      trigger: ".refresh-btn",
      //File source to be loaded (e.g: ajax/src.php)
      source: "",
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
      if (settings.source === "") {
        if (console) {
          console.log("Please specify a source first - boxRefresh()");
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
        box.find(".box-body").load(settings.source, function () {
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
 * @usage $("#todo-widget").todolist( options );
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

      if (typeof $.fn.iCheck != 'undefined') {
        $('input', this).on('ifChecked', function (event) {
          var ele = $(this).parents("li").first();
          ele.toggleClass("done");
          settings.onCheck.call(ele);
        });

        $('input', this).on('ifUnchecked', function (event) {
          var ele = $(this).parents("li").first();
          ele.toggleClass("done");
          settings.onUncheck.call(ele);
        });
      } else {
        $('input', this).on('change', function (event) {
          var ele = $(this).parents("li").first();
          ele.toggleClass("done");
          settings.onCheck.call(ele);
        });
      }
    });
  };
}(jQuery));
/*!
 * jQuery pagination plugin v1.2.5
 * http://esimakin.github.io/twbs-pagination/
 *
 * Copyright 2014, Eugene Simakin
 * Released under Apache 2.0 license
 * http://apache.org/licenses/LICENSE-2.0.html
 */
;
(function ($, window, document, undefined) {

    'use strict';

    var old = $.fn.twbsPagination;

    // PROTOTYPE AND CONSTRUCTOR

    var TwbsPagination = function (element, options) {
        this.$element = $(element);
        this.options = $.extend({}, $.fn.twbsPagination.defaults, options);

        if (this.options.startPage < 1 || this.options.startPage > this.options.totalPages) {
            throw new Error('Start page option is incorrect');
        }

        this.options.totalPages = parseInt(this.options.totalPages);
        if (isNaN(this.options.totalPages)) {
            throw new Error('Total pages option is not correct!');
        }

        this.options.visiblePages = parseInt(this.options.visiblePages);
        if (isNaN(this.options.visiblePages)) {
            throw new Error('Visible pages option is not correct!');
        }

        if (this.options.totalPages < this.options.visiblePages) {
            this.options.visiblePages = this.options.totalPages;
        }

        if (this.options.onPageClick instanceof Function) {
            this.$element.first().bind('page', this.options.onPageClick);
        }

        if (this.options.href) {
            var m, regexp = this.options.href.replace(/[-\/\\^$*+?.|[\]]/g, '\\$&');
            regexp = regexp.replace(this.options.hrefVariable, '(\\d+)');
            if ((m = new RegExp(regexp, 'i').exec(window.location.href)) != null) {
                this.options.startPage = parseInt(m[1], 10);
            }
        }

        var tagName = (typeof this.$element.prop === 'function') ?
            this.$element.prop('tagName') : this.$element.attr('tagName');

        if (tagName === 'UL') {
            this.$listContainer = this.$element;
        } else {
            this.$listContainer = $('<ul></ul>');
        }

        this.$listContainer.addClass(this.options.paginationClass);

        if (tagName !== 'UL') {
            this.$element.append(this.$listContainer);
        }

        this.render(this.getPages(this.options.startPage));
        this.setupEvents();

        return this;
    };

    TwbsPagination.prototype = {

        constructor: TwbsPagination,

        destroy: function () {
            this.$element.empty();
            this.$element.removeData('twbs-pagination');
            this.$element.unbind('page');
            return this;
        },

        show: function (page) {
            if (page < 1 || page > this.options.totalPages) {
                throw new Error('Page is incorrect.');
            }

            this.render(this.getPages(page));
            this.setupEvents();

            this.$element.trigger('page', page);
            return this;
        },

        buildListItems: function (pages) {
            var $listItems = $();

            if (this.options.first) {
                $listItems = $listItems.add(this.buildItem('first', 1));
            }

            if (this.options.prev) {
                var prev = pages.currentPage > 1 ? pages.currentPage - 1 : this.options.loop ? this.options.totalPages  : 1;
                $listItems = $listItems.add(this.buildItem('prev', prev));
            }

            for (var i = 0; i < pages.numeric.length; i++) {
                $listItems = $listItems.add(this.buildItem('page', pages.numeric[i]));
            }

            if (this.options.next) {
                var next = pages.currentPage < this.options.totalPages ? pages.currentPage + 1 : this.options.loop ? 1 : this.options.totalPages;
                $listItems = $listItems.add(this.buildItem('next', next));
            }

            if (this.options.last) {
                $listItems = $listItems.add(this.buildItem('last', this.options.totalPages));
            }

            return $listItems;
        },

        buildItem: function (type, page) {
            var itemContainer = $('<li></li>'),
                itemContent = $('<a></a>'),
                itemText = null;

            switch (type) {
                case 'page':
                    itemText = page;
                    itemContainer.addClass(this.options.pageClass);
                    break;
                case 'first':
                    itemText = this.options.first;
                    itemContainer.addClass(this.options.firstClass);
                    break;
                case 'prev':
                    itemText = this.options.prev;
                    itemContainer.addClass(this.options.prevClass);
                    break;
                case 'next':
                    itemText = this.options.next;
                    itemContainer.addClass(this.options.nextClass);
                    break;
                case 'last':
                    itemText = this.options.last;
                    itemContainer.addClass(this.options.lastClass);
                    break;
                default:
                    break;
            }

            itemContainer.data('page', page);
            itemContainer.data('page-type', type);
            itemContainer.append(itemContent.attr('href', this.makeHref(page)).html(itemText));
            return itemContainer;
        },

        getPages: function (currentPage) {
            var pages = [];

            var half = Math.floor(this.options.visiblePages / 2);
            var start = currentPage - half + 1 - this.options.visiblePages % 2;
            var end = currentPage + half;

            // handle boundary case
            if (start <= 0) {
                start = 1;
                end = this.options.visiblePages;
            }
            if (end > this.options.totalPages) {
                start = this.options.totalPages - this.options.visiblePages + 1;
                end = this.options.totalPages;
            }

            var itPage = start;
            while (itPage <= end) {
                pages.push(itPage);
                itPage++;
            }

            return {"currentPage": currentPage, "numeric": pages};
        },

        render: function (pages) {
            this.$listContainer.children().remove();
            this.$listContainer.append(this.buildListItems(pages));

            var children = this.$listContainer.children();
            children.filter(function () {
                return $(this).data('page') === pages.currentPage && $(this).data('page-type') === 'page';
            }).addClass(this.options.activeClass);

            children.filter(function () {
                return $(this).data('page-type') === 'first';
            }).toggleClass(this.options.disabledClass, pages.currentPage === 1);

            children.filter(function () {
                return $(this).data('page-type') === 'last';
            }).toggleClass(this.options.disabledClass, pages.currentPage === this.options.totalPages);

            children.filter(function () {
                return $(this).data('page-type') === 'prev';
            }).toggleClass(this.options.disabledClass, !this.options.loop && pages.currentPage === 1);

            children.filter(function () {
                return $(this).data('page-type') === 'next';
            }).toggleClass(this.options.disabledClass, !this.options.loop && pages.currentPage === this.options.totalPages);
        },

        setupEvents: function () {
            var base = this;
            this.$listContainer.find('li').each(function () {
                var $this = $(this);
                $this.off();
                if ($this.hasClass(base.options.disabledClass) || $this.hasClass(base.options.activeClass)) {
                    $this.click(function (evt) {
                        evt.preventDefault();
                    });
                    return;
                }
                $this.click(function (evt) {
                    // Prevent click event if href is not set.
                    !base.options.href && evt.preventDefault();
                    base.show(parseInt($this.data('page'), 10));
                });
            });
        },

        makeHref: function (c) {
            return this.options.href ? this.options.href.replace(this.options.hrefVariable, c) : "#";
        }

    };

    // PLUGIN DEFINITION

    $.fn.twbsPagination = function (option) {
        var args = Array.prototype.slice.call(arguments, 1);
        var methodReturn;

        var $this = $(this);
        var data = $this.data('twbs-pagination');
        var options = typeof option === 'object' && option;

        if (!data) $this.data('twbs-pagination', (data = new TwbsPagination(this, options) ));
        if (typeof option === 'string') methodReturn = data[ option ].apply(data, args);

        return ( methodReturn === undefined ) ? $this : methodReturn;
    };

    $.fn.twbsPagination.defaults = {
        totalPages: 0,
        startPage: 1,
        visiblePages: 5,
        href: false,
        hrefVariable: '{{number}}',
        first: 'First',
        prev: 'Previous',
        next: 'Next',
        last: 'Last',
        loop: false,
        onPageClick: null,
        paginationClass: 'pagination',
        nextClass: 'next',
        prevClass: 'prev',
        lastClass: 'last',
        firstClass: 'first',
        pageClass: 'page',
        activeClass: 'active',
        disabledClass: 'disabled'
    };

    $.fn.twbsPagination.Constructor = TwbsPagination;

    $.fn.twbsPagination.noConflict = function () {
        $.fn.twbsPagination = old;
        return this;
    };

})(jQuery, window, document);

/* global moment */

'use strict';

//
// configuration
//

require.config({
  paths: {
    echarts: '/vendor/echarts'
  }
});


//
// functions
//

var APP = {};

APP.url = location.pathname;

APP.type = (function() {
  var path = APP.url.split('/').slice(1, -1),
      type = '';

  switch (path.length) {
    case 0:
      type = 'dashboard';
      break;
    case 1:
      type = path[0];
      break;
    case 2:
      type = path[0] + 'Item';
      break;
  }

  return type;
})();

APP.user = {
  login: function() {
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
  },

  admin: function() {
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
  },

  add: function() {
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
  }
};

APP.search = function() {
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

APP.menu = function() {
  var menu     = $('.sidebar-menu'),
      parent   = menu.parent(),
      vaildURL = function() {
        var thisHref = this.getAttribute('href');

        if (APP.type === 'categoryItem' || APP.type === 'locationItem' || APP.type === 'analyticsItem') {
          return thisHref === APP.url;
        } else {
          return thisHref.split('/')[1] === APP.url.split('/')[1];
        }
      };

  menu
    .detach()
    .find('a').filter(vaildURL)
    .parent().addClass('active')
    .closest('.treeview-menu').addClass('menu-open')
    .closest('.treeview').addClass('active');

  menu.appendTo(parent);
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
  var top       = el.offset().top,
      scrollTop = top > 160 ? top - 120 : 0;

  $('body').animate({scrollTop: scrollTop});
};

APP.table = function() {
  $('.table-custom').each(function() {
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
          APP.returnTop($this);

          $.getJSON('/api' + APP.url + type + '/' + page + '/', function(data) {
            renderTable(data);
            $pagination.twbsPagination({totalPages: data.total});
          });
        }
      });
    });
  });
};

APP.dataTable = function() {
  $.fn.dataTable.ext.errMode = 'throw';

  $('.initDataTable').each(function() {
    var table = $(this).DataTable({
      'ajax': {
        'url': '/api' + location.pathname,
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
      'drawCallback': function() {
        $('[data-toggle="tooltip"]').tooltip();
      }
    });

    table.on('click', 'tbody > tr', function() {
      if ( $(this).hasClass('selected') ) {
        $(this).removeClass('selected');
      } else {
        table.$('tr.selected').removeClass('selected');
        $(this).addClass('selected');
      }
    });
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
  var $sns = $('.sns');

  $sns.each(function(index, element) {
    var $content    = $(element),
        $pagination = $content.parent().next(),

        type = function() {
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
          APP.returnTop($sns);
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

APP.collection = function() {
  $('.collection').click(function() {
    var star = $(this).find('i'),
        text = $(this).find('span'),

        collect = function(api, nextAction) {
          var urlArray = APP.url.split('/'),
              data = {
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
  });
};

APP.product = function() {
  $('.filter-list')
    .find('a').filter(function() { return this.href === location.href; })
    .parent().addClass('active');
};


APP.inspection = function () {
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


APP.analytics = function () {
  var start = '',
      end = '',
      api = '/api' + APP.url,
      $dateRangePicker = $('.date-range-picker'),
      $dateRangeLabel = $dateRangePicker.children('span'),
      $chart = $('#chart'),
      $statistic = $('#statistic'),
      $dataList = $('#data-list'),
      $statisticTotal = $('.statistic-total').children('span'),
      $statisticRisk = $('.statistic-risk').children('span'),

      chart = {
        trend: function (start, end) {
           require(['echarts', 'echarts/chart/line','echarts/theme/macarons',], function (ec ) {
             $.getJSON(api, {type: 'chart-trend', start: start, end: end}, function (data) {
               ec.init( document .getElementById('chart-trend'), 'macarons').setOption({
                  tooltip : {
                    backgroundColor:'rgba(50,50,50,0.5)',
                    trigger:'axis',
                    axisPointer : {
                      type : 'line',
                      lineStyle : {
                        color : '#008acd',
                      }
                    }
                  },
                  shadowStyle : {
                    color : 'rgba(200,200,200,0.2)'
                  },
                  legend : {
                    data : ['全部' , '新闻' ,  '微博' ,   '微信']
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
                      stack: '总量',
                      data:data.total_data
                    },
                    {
                      name: '新闻',
                      type: 'line',
                      stack: '总量',
                      data:data.news_data
                      },
                      {
                      name: '微博',
                      type: 'line',
                      stack: '总量',
                      data:data.weibo_data
                      },
                      {
                      name: '微信',
                      type: 'line',
                      stack: '总量',
                      data:data.weixin_data
                      },
                      ]
                 });
             })
           })
        },
        type: function (start, end) {
          require(['echarts', 'echarts/chart/pie','echarts/theme/macarons',], function (ec ) {
             $.getJSON(api, {type: 'chart-type', start: start, end: end}, function (data) {
                ec.init(document.getElementById('chart-type')).setOption({
                 tooltip : {
                  backgroundColor:'rgba(50,50,50,0.5)',
                  trigger: 'item',
                  formatter: "{a} <br/>{b} : {c} ({d}%)"
                 },
                 legend: {
                   orient : 'vertical',
                   x : 'left',
                   data:['新闻','微博','微信']
                   },
                 toolbox: {
                   show : true,
                   feature : {
                     dataView : {show: true, readOnly: false},
                     saveAsImage : {show: true}
                   }
                 },
                 calculable : true,
                 series : [
                   {
                      name:'访问来源',
                      type:'pie',
                      radius : '55%',
                      center: ['50%', '60%'],
                      data:[
                        {value:data.news, name:'新闻'},
                        {value:data.weibo, name:'微博'},
                        {value:data.weixin, name:'微信'}
                      ]
                   }
                 ]
                });
             });
          });
        },

        emotion: function (start, end) {
          $('#chart-emotion').attr('style','height:400px;width:100%');
          require(['echarts', 'echarts/chart/pie'],function (ec){
            $.getJSON(api, { type : 'chart_emotion', start : start, end : end},function(data) {
                ec.init(document.getElementById('chart-emotion')).setOption({
                    title : {
                    text: '情感分析',
                    subtext: '',
                    x:'center'
                  },
                  tooltip : {
                      trigger: 'item',
                      formatter: "{a} <br/>{b} : {c} ({d}%)"
                  },
                  legend: {
                      orient : 'vertical',
                      x : 'left',
                      data:['正面','中性','负面']
                  },
                  toolbox: {
                      show : false,
                      feature : {
                          mark : {show: true},
                          dataView : {show: true, readOnly: false},
                          magicType : {
                              show: true,
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
                          restore : {show: false},
                          saveAsImage : {show: true}
                      }
                  },
                  calculable : true,
                  series : [
                      {
                          name:'访问来源',
                          type:'pie',
                          radius : '55%',
                          center: ['50%', '60%'],
                          data:
                          [
                              {value : data.positive, name:'正面'},
                              {value : data.normal, name:'中性'},
                              {value : data.negative, name:'负面'},
                          ]
                      }
                  ]
                });
            });
          });

        },

        weibo: function (start, end) {
          $('#chart-weibo').attr('style','height:400px;width:60%');
          require(['echarts', 'echarts/chart/map'],function (ec){
            $.getJSON(api, { type : 'char_weibo', start : start, end : end },function(data){
              ec.init(document.getElementById('chart-weibo')).setOption({
                title : {
                    text: '微博地域分析',
                    subtext:'纯属虚构',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item'
                },
                legend: {
                    orient: 'vertical',
                    x:'left',
                    data:['微博文']
                },
                dataRange: {
                    min: 0,
                    max: 10000,
                    x: 'left',
                    y: 'bottom',
                    text:['高','低'],           // 文本，默认为数值文本
                    calculable : true
                },
                toolbox: {
                    show: false,
                    orient : 'vertical',
                    x: 'right',
                    y: 'center',
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                roamController: {
                    show: true,
                    x: 'right',
                    mapTypeControl: {
                        'china': true
                    }
                },
                series : [
                    {
                        name: '微博文',
                        type: 'map',
                        mapType: 'china',
                        roam: false,
                        itemStyle:{
                            normal:{label:{show:true}},
                            emphasis:{label:{show:true}}
                        },
                        data:data.provice_count
                    },
                ]
              });
           });
          });
        }
      },

      showDateRange = function (start, end) {
        $dateRangeLabel.html(start + ' ~ ' + end);
      },

      showChart = function () {
        var chartType = $chart.find('.tab-pane.active')[0].id.slice(6);
        chart[chartType](start, end);
      },

      showStatistic = function () {
        $.getJSON(api, {type: 'statistic', start: start, end: end}, function (statistic) {
          $statisticTotal.text(statistic.total);
          $statisticRisk.text(statistic.risk);
        });
      },

      showDataList = function () {
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
              APP.returnTop($(this));
              $.get(api, toParam(pageNumber), function(data) {
                renderTable(data.html);
                $paginationContainer.twbsPagination({totalPages: data.total});
              });
            }
          });
        });
      },

      showAnalytics = function (startMoment, endMoment) {
        start = startMoment.format('YYYY-MM-DD');
        end   = endMoment.format('YYYY-MM-DD');

        showDateRange(start, end);

        $chart
          .trigger('showChart')
          .off('shown.bs.tab')
          .on('shown.bs.tab', showChart);

        $statistic.trigger('showStatistic');

        $dataList.trigger('showDataList');
      };

  $chart.on('showChart', showChart);

  $statistic.on('showStatistic', showStatistic);

  $dataList.on('showDataList', showDataList);

  $dateRangePicker.daterangepicker({
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
      'customRangeLabel': '自定义',
      'daysOfWeek': [
        '日',
        '一',
        '二',
        '三',
        '四',
        '五',
        '六'
      ],
      'monthNames': [
        '一月',
        '二月',
        '三月',
        '四月',
        '五月',
        '六月',
        '七月',
        '八月',
        '九月',
        '十月',
        '十一月',
        '十二月'
      ],
      'firstDay': 1
    },
    'startDate': moment().subtract(6, 'days'),
    'endDate': moment(),
    'minDate': '2010-01-01',
    'maxDate': moment(),
    'opens': 'left',
    'parentEl': '.content-header',
    'applyClass': 'btn-success',
    'cancelClass': 'btn-default'
  }, showAnalytics);

  showAnalytics(moment().subtract(6, 'days'), moment());
};


//
// url based router
//

$(function() {
  var router = {
    common: function() {
      APP.search();
      APP.menu();
    },
    login: function() {
      APP.user.login();
    },
    dashboard: function() {
      this.common();
      APP.dashboard();
      APP.inspection();
      APP.chart.line();
      APP.chart.pie();
    },
    news: function() {
      this.common();
      APP.table();
    },
    newsItem: function() {
      this.common();
      APP.collection();
    },
    event: function() {
      this.common();
      APP.table();
    },
    eventItem: function() {
      this.common();
      APP.collection();
      APP.chart.line();
      APP.chart.pie();
      APP.table();
      APP.sns();
    },
    weixin: function() {
      this.common();
      APP.sns();
    },
    weibo: function() {
      this.weixin();
    },
    weixinItem: function() {
      this.common();
    },
    categoryItem: function() {
      this.common();
      APP.table();
    },
    locationItem: function() {
      this.common();
      APP.table();
      APP.sns();
    },
    inspection: function() {
      this.common();
      APP.dataTable();
    },
    custom: function() {
      this.common();
      APP.custom();
    },
    customItem: function() {
      this.common();
      APP.table();
      APP.sns();
    },
    product: function() {
      this.common();
      APP.product();
      APP.table();
    },
    productItem: function() {
      this.common();
      this.product();
    },
    analyticsItem: function () {
      this.common();
      APP.analytics();
    },
    collection: function() {
      this.common();
      APP.table();
    },
    settings: function() {
      this.common();
      APP.user.change();
    },
    user: function() {
      this.common();
      APP.user.admin();
      APP.user.add();
    },
    searchItem: function() {
      this.common();
      APP.dataTable();
    }
  };

  return router[APP.type]();
});