function _init(){$.AdminLTE.layout={activate:function(){var t=this;t.fix(),t.fixSidebar(),$(window,".wrapper").resize(function(){t.fix(),t.fixSidebar()})},fix:function(){var t=$(".main-header").outerHeight()+$(".main-footer").outerHeight(),e=$(window).height(),i=$(".sidebar").height();$("body").hasClass("fixed")?$(".content-wrapper, .right-side").css("min-height",e-$(".main-footer").outerHeight()):e>=i?$(".content-wrapper, .right-side").css("min-height",e-t):$(".content-wrapper, .right-side").css("min-height",i)},fixSidebar:function(){return $("body").hasClass("fixed")?("undefined"==typeof $.fn.slimScroll&&console&&console.error("Error: the fixed layout requires the slimscroll plugin!"),void($.AdminLTE.options.sidebarSlimScroll&&"undefined"!=typeof $.fn.slimScroll&&($(".sidebar").slimScroll({destroy:!0}).height("auto"),$(".sidebar").slimscroll({height:$(window).height()-$(".main-header").height()+"px",color:"rgba(0,0,0,0.2)",size:"3px"})))):void("undefined"!=typeof $.fn.slimScroll&&$(".sidebar").slimScroll({destroy:!0}).height("auto"))}},$.AdminLTE.pushMenu=function(t){var e=this.options.screenSizes;$(t).click(function(t){t.preventDefault(),$(window).width()>e.sm-1?$("body").toggleClass("sidebar-collapse"):$("body").hasClass("sidebar-open")?($("body").removeClass("sidebar-open"),$("body").removeClass("sidebar-collapse")):$("body").addClass("sidebar-open")}),$(".content-wrapper").click(function(){$(window).width()<=e.sm-1&&$("body").hasClass("sidebar-open")&&$("body").removeClass("sidebar-open")})},$.AdminLTE.tree=function(t){var e=this;$("li a",$(t)).click(function(t){var i=$(this),a=i.next();if(a.is(".treeview-menu")&&a.is(":visible"))a.slideUp("normal",function(){a.removeClass("menu-open")}),a.parent("li").removeClass("active");else if(a.is(".treeview-menu")&&!a.is(":visible")){var n=i.parents("ul").first(),o=n.find("ul:visible").slideUp("normal");o.removeClass("menu-open");var s=i.parent("li");a.slideDown("normal",function(){a.addClass("menu-open"),n.find("li.active").removeClass("active"),s.addClass("active"),e.layout.fix()})}a.is(".treeview-menu")&&t.preventDefault()})},$.AdminLTE.boxWidget={activate:function(){var t=$.AdminLTE.options,e=this;$(t.boxWidgetOptions.boxWidgetSelectors.collapse).click(function(t){t.preventDefault(),e.collapse($(this))}),$(t.boxWidgetOptions.boxWidgetSelectors.remove).click(function(t){t.preventDefault(),e.remove($(this))})},collapse:function(t){var e=t.parents(".box").first(),i=e.find(".box-body, .box-footer");e.hasClass("collapsed-box")?(t.children(".fa-plus").removeClass("fa-plus").addClass("fa-minus"),i.slideDown(300,function(){e.removeClass("collapsed-box")})):(t.children(".fa-minus").removeClass("fa-minus").addClass("fa-plus"),i.slideUp(300,function(){e.addClass("collapsed-box")}))},remove:function(t){var e=t.parents(".box").first();e.slideUp()},options:$.AdminLTE.options.boxWidgetOptions}}if(function(e){e.fn.extend({slimScroll:function(i){var a={width:"auto",height:"250px",size:"7px",color:"#000",position:"right",distance:"1px",start:"top",opacity:.4,alwaysVisible:!1,disableFadeOut:!1,railVisible:!1,railColor:"#333",railOpacity:.2,railDraggable:!0,railClass:"slimScrollRail",barClass:"slimScrollBar",wrapperClass:"slimScrollDiv",allowPageScroll:!1,wheelStep:20,touchScrollStep:200,borderRadius:"7px",railBorderRadius:"7px"},n=e.extend(a,i);return this.each(function(){function a(t){if(u){var t=t||window.event,i=0;t.wheelDelta&&(i=-t.wheelDelta/120),t.detail&&(i=t.detail/3);var a=t.target||t.srcTarget||t.srcElement;e(a).closest("."+n.wrapperClass).is(w.parent())&&o(i,!0),t.preventDefault&&!$&&t.preventDefault(),$||(t.returnValue=!1)}}function o(t,e,i){$=!1;var a=t,o=w.outerHeight()-k.outerHeight();if(e&&(a=parseInt(k.css("top"))+t*parseInt(n.wheelStep)/100*k.outerHeight(),a=Math.min(Math.max(a,0),o),a=t>0?Math.ceil(a):Math.floor(a),k.css({top:a+"px"})),m=parseInt(k.css("top"))/(w.outerHeight()-k.outerHeight()),a=m*(w[0].scrollHeight-w.outerHeight()),i){a=t;var s=a/w[0].scrollHeight*w.outerHeight();s=Math.min(Math.max(s,0),o),k.css({top:s+"px"})}w.scrollTop(a),w.trigger("slimscrolling",~~a),l(),c()}function s(){window.addEventListener?(this.addEventListener("DOMMouseScroll",a,!1),this.addEventListener("mousewheel",a,!1)):document.attachEvent("onmousewheel",a)}function r(){g=Math.max(w.outerHeight()/w[0].scrollHeight*w.outerHeight(),P),k.css({height:g+"px"});var t=g==w.outerHeight()?"none":"block";k.css({display:t})}function l(){if(r(),clearTimeout(p),m==~~m){if($=n.allowPageScroll,v!=m){var t=0==~~m?"top":"bottom";w.trigger("slimscroll",t)}}else $=!1;return v=m,g>=w.outerHeight()?void($=!0):(k.stop(!0,!0).fadeIn("fast"),void(n.railVisible&&A.stop(!0,!0).fadeIn("fast")))}function c(){n.alwaysVisible||(p=setTimeout(function(){n.disableFadeOut&&u||d||h||(k.fadeOut("slow"),A.fadeOut("slow"))},1e3))}var u,d,h,p,f,g,m,v,b="<div></div>",P=30,$=!1,w=e(this);if(w.parent().hasClass(n.wrapperClass)){var C=w.scrollTop();if(k=w.parent().find("."+n.barClass),A=w.parent().find("."+n.railClass),r(),e.isPlainObject(i)){if("height"in i&&"auto"==i.height){w.parent().css("height","auto"),w.css("height","auto");var y=w.parent().parent().height();w.parent().css("height",y),w.css("height",y)}if("scrollTo"in i)C=parseInt(n.scrollTo);else if("scrollBy"in i)C+=parseInt(n.scrollBy);else if("destroy"in i)return k.remove(),A.remove(),void w.unwrap();o(C,!1,!0)}}else if(!(e.isPlainObject(i)&&"destroy"in i)){n.height="auto"==n.height?w.parent().height():n.height;var x=e(b).addClass(n.wrapperClass).css({position:"relative",overflow:"hidden",width:n.width,height:n.height});w.css({overflow:"hidden",width:n.width,height:n.height,"-ms-touch-action":"none"});var A=e(b).addClass(n.railClass).css({width:n.size,height:"100%",position:"absolute",top:0,display:n.alwaysVisible&&n.railVisible?"block":"none","border-radius":n.railBorderRadius,background:n.railColor,opacity:n.railOpacity,zIndex:90}),k=e(b).addClass(n.barClass).css({background:n.color,width:n.size,position:"absolute",top:0,opacity:n.opacity,display:n.alwaysVisible?"block":"none","border-radius":n.borderRadius,BorderRadius:n.borderRadius,MozBorderRadius:n.borderRadius,WebkitBorderRadius:n.borderRadius,zIndex:99}),S="right"==n.position?{right:n.distance}:{left:n.distance};A.css(S),k.css(S),w.wrap(x),w.parent().append(k),w.parent().append(A),n.railDraggable&&k.bind("mousedown",function(i){var a=e(document);return h=!0,t=parseFloat(k.css("top")),pageY=i.pageY,a.bind("mousemove.slimscroll",function(e){currTop=t+e.pageY-pageY,k.css("top",currTop),o(0,k.position().top,!1)}),a.bind("mouseup.slimscroll",function(t){h=!1,c(),a.unbind(".slimscroll")}),!1}).bind("selectstart.slimscroll",function(t){return t.stopPropagation(),t.preventDefault(),!1}),A.hover(function(){l()},function(){c()}),k.hover(function(){d=!0},function(){d=!1}),w.hover(function(){u=!0,l(),c()},function(){u=!1,c()}),window.navigator.msPointerEnabled?(w.bind("MSPointerDown",function(t,e){t.originalEvent.targetTouches.length&&(f=t.originalEvent.targetTouches[0].pageY)}),w.bind("MSPointerMove",function(t){if(t.originalEvent.preventDefault(),t.originalEvent.targetTouches.length){var e=(f-t.originalEvent.targetTouches[0].pageY)/n.touchScrollStep;o(e,!0),f=t.originalEvent.targetTouches[0].pageY}})):(w.bind("touchstart",function(t,e){t.originalEvent.touches.length&&(f=t.originalEvent.touches[0].pageY)}),w.bind("touchmove",function(t){if($||t.originalEvent.preventDefault(),t.originalEvent.touches.length){var e=(f-t.originalEvent.touches[0].pageY)/n.touchScrollStep;o(e,!0),f=t.originalEvent.touches[0].pageY}})),r(),"bottom"===n.start?(k.css({top:w.outerHeight()-k.outerHeight()}),o(0,!0)):"top"!==n.start&&(o(e(n.start).position().top,null,!0),n.alwaysVisible||k.hide()),s()}}),this}}),e.fn.extend({slimscroll:e.fn.slimScroll})}(jQuery),"undefined"==typeof jQuery)throw new Error("AdminLTE requires jQuery");$.AdminLTE={},$.AdminLTE.options={navbarMenuSlimscroll:!0,navbarMenuSlimscrollWidth:"3px",navbarMenuHeight:"200px",sidebarToggleSelector:"[data-toggle='offcanvas']",sidebarPushMenu:!0,sidebarSlimScroll:!0,enableBoxRefresh:!0,enableBSToppltip:!0,BSTooltipSelector:"[data-toggle='tooltip']",enableFastclick:!0,enableBoxWidget:!0,boxWidgetOptions:{boxWidgetIcons:{collapse:"fa fa-minus",open:"fa fa-plus",remove:"fa fa-times"},boxWidgetSelectors:{remove:'[data-widget="remove"]',collapse:'[data-widget="collapse"]'}},directChat:{enable:!0,contactToggleSelector:'[data-widget="chat-pane-toggle"]'},colors:{lightBlue:"#3c8dbc",red:"#f56954",green:"#00a65a",aqua:"#00c0ef",yellow:"#f39c12",blue:"#0073b7",navy:"#001F3F",teal:"#39CCCC",olive:"#3D9970",lime:"#01FF70",orange:"#FF851B",fuchsia:"#F012BE",purple:"#8E24AA",maroon:"#D81B60",black:"#222222",gray:"#d2d6de"},screenSizes:{xs:480,sm:768,md:992,lg:1200}},$(function(){var t=$.AdminLTE.options;_init(),$.AdminLTE.layout.activate(),$.AdminLTE.tree(".sidebar"),t.navbarMenuSlimscroll&&"undefined"!=typeof $.fn.slimscroll&&$(".navbar .menu").slimscroll({height:"200px",alwaysVisible:!1,size:"3px"}).css("width","100%"),t.sidebarPushMenu&&$.AdminLTE.pushMenu(t.sidebarToggleSelector),t.enableBSToppltip&&$(t.BSTooltipSelector).tooltip(),t.enableBoxWidget&&$.AdminLTE.boxWidget.activate(),t.enableFastclick&&"undefined"!=typeof FastClick&&FastClick.attach(document.body),t.directChat.enable&&$(t.directChat.contactToggleSelector).click(function(){var t=$(this).parents(".direct-chat").first();t.toggleClass("direct-chat-contacts-open")}),$('.btn-group[data-toggle="btn-toggle"]').each(function(){var t=$(this);$(this).find(".btn").click(function(e){t.find(".btn.active").removeClass("active"),$(this).addClass("active"),e.preventDefault()})})}),function(t){t.fn.boxRefresh=function(e){function i(t){t.append(o),n.onLoadStart.call(t)}function a(t){t.find(o).remove(),n.onLoadDone.call(t)}var n=t.extend({trigger:".refresh-btn",source:"",onLoadStart:function(t){},onLoadDone:function(t){}},e),o=t('<div class="overlay"><div class="fa fa-refresh fa-spin"></div></div>');return this.each(function(){if(""===n.source)return void(console&&console.log("Please specify a source first - boxRefresh()"));var e=t(this),o=e.find(n.trigger).first();o.click(function(t){t.preventDefault(),i(e),e.find(".box-body").load(n.source,function(){a(e)})})})}}(jQuery),function(t){t.fn.todolist=function(e){var i=t.extend({onCheck:function(t){},onUncheck:function(t){}},e);return this.each(function(){"undefined"!=typeof t.fn.iCheck?(t("input",this).on("ifChecked",function(e){var a=t(this).parents("li").first();a.toggleClass("done"),i.onCheck.call(a)}),t("input",this).on("ifUnchecked",function(e){var a=t(this).parents("li").first();a.toggleClass("done"),i.onUncheck.call(a)})):t("input",this).on("change",function(e){var a=t(this).parents("li").first();a.toggleClass("done"),i.onCheck.call(a)})})}}(jQuery),function(t,e,i,a){"use strict";var n=t.fn.twbsPagination,o=function(i,a){if(this.$element=t(i),this.options=t.extend({},t.fn.twbsPagination.defaults,a),this.options.startPage<1||this.options.startPage>this.options.totalPages)throw new Error("Start page option is incorrect");if(this.options.totalPages=parseInt(this.options.totalPages),isNaN(this.options.totalPages))throw new Error("Total pages option is not correct!");if(this.options.visiblePages=parseInt(this.options.visiblePages),isNaN(this.options.visiblePages))throw new Error("Visible pages option is not correct!");if(this.options.totalPages<this.options.visiblePages&&(this.options.visiblePages=this.options.totalPages),this.options.onPageClick instanceof Function&&this.$element.first().bind("page",this.options.onPageClick),this.options.href){var n,o=this.options.href.replace(/[-\/\\^$*+?.|[\]]/g,"\\$&");o=o.replace(this.options.hrefVariable,"(\\d+)"),null!=(n=new RegExp(o,"i").exec(e.location.href))&&(this.options.startPage=parseInt(n[1],10))}var s="function"==typeof this.$element.prop?this.$element.prop("tagName"):this.$element.attr("tagName");return this.$listContainer="UL"===s?this.$element:t("<ul></ul>"),this.$listContainer.addClass(this.options.paginationClass),"UL"!==s&&this.$element.append(this.$listContainer),this.render(this.getPages(this.options.startPage)),this.setupEvents(),this};o.prototype={constructor:o,destroy:function(){return this.$element.empty(),this.$element.removeData("twbs-pagination"),this.$element.unbind("page"),this},show:function(t){if(1>t||t>this.options.totalPages)throw new Error("Page is incorrect.");return this.render(this.getPages(t)),this.setupEvents(),this.$element.trigger("page",t),this},buildListItems:function(e){var i=t();if(this.options.first&&(i=i.add(this.buildItem("first",1))),this.options.prev){var a=e.currentPage>1?e.currentPage-1:this.options.loop?this.options.totalPages:1;i=i.add(this.buildItem("prev",a))}for(var n=0;n<e.numeric.length;n++)i=i.add(this.buildItem("page",e.numeric[n]));if(this.options.next){var o=e.currentPage<this.options.totalPages?e.currentPage+1:this.options.loop?1:this.options.totalPages;i=i.add(this.buildItem("next",o))}return this.options.last&&(i=i.add(this.buildItem("last",this.options.totalPages))),i},buildItem:function(e,i){var a=t("<li></li>"),n=t("<a></a>"),o=null;switch(e){case"page":o=i,a.addClass(this.options.pageClass);break;case"first":o=this.options.first,a.addClass(this.options.firstClass);break;case"prev":o=this.options.prev,a.addClass(this.options.prevClass);break;case"next":o=this.options.next,a.addClass(this.options.nextClass);break;case"last":o=this.options.last,a.addClass(this.options.lastClass)}return a.data("page",i),a.data("page-type",e),a.append(n.attr("href",this.makeHref(i)).html(o)),a},getPages:function(t){var e=[],i=Math.floor(this.options.visiblePages/2),a=t-i+1-this.options.visiblePages%2,n=t+i;0>=a&&(a=1,n=this.options.visiblePages),n>this.options.totalPages&&(a=this.options.totalPages-this.options.visiblePages+1,n=this.options.totalPages);for(var o=a;n>=o;)e.push(o),o++;return{currentPage:t,numeric:e}},render:function(e){this.$listContainer.children().remove(),this.$listContainer.append(this.buildListItems(e));var i=this.$listContainer.children();i.filter(function(){return t(this).data("page")===e.currentPage&&"page"===t(this).data("page-type")}).addClass(this.options.activeClass),i.filter(function(){return"first"===t(this).data("page-type")}).toggleClass(this.options.disabledClass,1===e.currentPage),i.filter(function(){return"last"===t(this).data("page-type")}).toggleClass(this.options.disabledClass,e.currentPage===this.options.totalPages),i.filter(function(){return"prev"===t(this).data("page-type")}).toggleClass(this.options.disabledClass,!this.options.loop&&1===e.currentPage),i.filter(function(){return"next"===t(this).data("page-type")}).toggleClass(this.options.disabledClass,!this.options.loop&&e.currentPage===this.options.totalPages)},setupEvents:function(){var e=this;this.$listContainer.find("li").each(function(){var i=t(this);return i.off(),i.hasClass(e.options.disabledClass)||i.hasClass(e.options.activeClass)?void i.click(function(t){t.preventDefault()}):void i.click(function(t){!e.options.href&&t.preventDefault(),e.show(parseInt(i.data("page"),10))})})},makeHref:function(t){return this.options.href?this.options.href.replace(this.options.hrefVariable,t):"#"}},t.fn.twbsPagination=function(e){var i,n=Array.prototype.slice.call(arguments,1),s=t(this),r=s.data("twbs-pagination"),l="object"==typeof e&&e;return r||s.data("twbs-pagination",r=new o(this,l)),"string"==typeof e&&(i=r[e].apply(r,n)),i===a?s:i},t.fn.twbsPagination.defaults={totalPages:0,startPage:1,visiblePages:5,href:!1,hrefVariable:"{{number}}",first:"First",prev:"Previous",next:"Next",last:"Last",loop:!1,onPageClick:null,paginationClass:"pagination",nextClass:"next",prevClass:"prev",lastClass:"last",firstClass:"first",pageClass:"page",activeClass:"active",disabledClass:"disabled"},t.fn.twbsPagination.Constructor=o,t.fn.twbsPagination.noConflict=function(){return t.fn.twbsPagination=n,this}}(jQuery,window,document),require.config({paths:{echarts:"/vendor/echarts"}});var APP={};APP.url=location.pathname,APP.type=function(){var t=APP.url.split("/").slice(1,-1),e="";switch(t.length){case 0:e="dashboard";break;case 1:e=t[0];break;case 2:e=t[0]+"Item"}return e}(),APP.user={login:function(){var t=document.forms.login,e=t.action,i=t.elements,a=i.username,n=i.password,o=i[2],s=$(t).find("p"),r=function(){o.disabled=!(a.value&&n.value)},l=function(i){i.preventDefault(),$.post(e,$(t).serialize(),function(t){t.status?location.href=location.search?location.search.substr(1).split("=")[1]:"/":(s.text("用户名或密码错误！"),o.disabled=!0,n.value="")})};$(t).keyup(r).submit(l)},change:function(){var t=document.forms.info,e=t.action,i=t.elements,a=i.username,n=i.oldPassword,o=i.newPassword,s=i.retype,r=i[4],l=$(t).find("p"),c=function(){r.disabled=!(a.value&&n.value&&o.value&&s.value)},u=function(t){t.preventDefault();var i=function(t){t.status?(l.text("更新成功！").show(),location.href="/login/"):(l.text("原密码错误！").show(),n.value="",o.value="",s.value="")};o.value===s.value?$.post(e,$([a,n,o]).serialize(),i):(l.text("两次输入密码不一致！").show(),o.value="",s.value="")};$(t).keyup(c).submit(u)},admin:function(){var t=$(".user-admin"),e=t.find("input"),i=t.find("button"),a=i.eq(0),n=i.eq(1),o=[],s=function(t,i){t.click(function(){o.length=0,e.filter(":checked").each(function(t,e){o.push($(e).parent().next().data("id"))}),o.length&&$.post(i,{id:o.toString()},function(t){t.status&&location.reload()})})};s(a,"/api/user/reset/"),s(n,"/api/user/remove/")},add:function(){var t=document.forms.add,e=t.action,i=t.elements,a=i.username,n=i.password,o=i.retype,s=i[3],r=$(t).find("p"),l=function(){s.disabled=!(a.value&&n.value&&o.value)},c=function(t){t.preventDefault();var i=function(t){t.status?location.reload():r.text("抱歉，添加失败！").show()};n.value===o.value?$.post(e,$([a,n]).serialize(),i):(r.text("两次输入密码不一致！").show(),s.disabled=!0,n.value="",o.value="")};$(t).keyup(l).submit(c)}},APP.search=function(){var t=document.forms.search,e=t.elements.keywords;$(t).submit(function(i){i.preventDefault();var a=$.trim(e.value);a&&(t.reset(),location.href="/search/"+a+"/")})},APP.menu=function(){var t=$(".sidebar-menu"),e=t.parent(),i=function(){var t=this.getAttribute("href");return"dashboard"===APP.type||"categoryItem"===APP.type||"locationItem"===APP.type?t===APP.url:t.split("/")[1]===APP.url.split("/")[1]};t.detach().find("a").filter(i).parent().addClass("active").closest(".treeview-menu").addClass("menu-open").closest(".treeview").addClass("active"),t.appendTo(e)},APP.chart={line:function(){require(["echarts","echarts/chart/line"],function(t){$.getJSON("/api/line"+APP.url,function(e){t.init(document.getElementById("line-chart"),"macarons").setOption({color:["#00a65a","#00c0ef","#dd4b39"],tooltip:{trigger:"axis"},legend:{data:["正面","中性","负面"]},grid:{x:40,y:30,x2:25,y2:30},xAxis:[{type:"category",boundaryGap:!1,data:e.date}],yAxis:[{type:"value"}],series:[{name:"正面",type:"line",data:e.positive},{name:"中性",type:"line",data:e.neutral},{name:"负面",type:"line",data:e.negative}]})})})},pie:function(){require(["echarts","echarts/chart/pie"],function(t){$.getJSON("/api/pie"+APP.url,function(e){t.init(document.getElementById("pie-chart"),"macarons").setOption({tooltip:{trigger:"item",formatter:"{a} <br/>{b} : {c} ({d}%)"},legend:{data:e.name},series:[{name:"信息比例",type:"pie",radius:"55%",center:["50%","60%"],data:e.value}]})})})},map:function(){require(["echarts","echarts/chart/map"],function(t){require("echarts/util/mapData/params").params.wh={getGeoJson:function(t){$.getJSON("/static/wh.json",t)}},t.init(document.getElementById("map-chart"),"macarons").setOption({title:{subtext:""},tooltip:{trigger:"item",formatter:function(t){return t[1]+"<br>"+t[2]}},legend:{orient:"vertical",x:"right",data:[""]},dataRange:{min:0,max:1e3,color:["orange","yellow"],text:["高","低"],calculable:!0},series:[{name:"数据名称",type:"map",mapType:"wh",selectedMode:"single",itemStyle:{normal:{label:{show:!1}},emphasis:{label:{show:!0}}},data:[{name:"江岸区",value:Math.round(1e3*Math.random())},{name:"江汉区",value:Math.round(1e3*Math.random())},{name:"硚口区",value:Math.round(1e3*Math.random())},{name:"汉阳区",value:Math.round(1e3*Math.random())},{name:"武昌区",value:Math.round(1e3*Math.random())},{name:"洪山区",value:Math.round(1e3*Math.random())},{name:"青山区",value:Math.round(1e3*Math.random())},{name:"东西湖区",value:Math.round(1e3*Math.random())},{name:"蔡甸区",value:Math.round(1e3*Math.random())},{name:"江夏区",value:Math.round(1e3*Math.random())},{name:"黄陂区",value:Math.round(1e3*Math.random())},{name:"新洲区",value:Math.round(1e3*Math.random())},{name:"汉南区",value:Math.round(1e3*Math.random())}]}]})})}},APP.returnTop=function(t){var e=t.offset().top,i=e>160?e-120:0;$("body").animate({scrollTop:i})},APP.table=function(){$(".table-custom").each(function(){var t=$(this),e=t.parent(),i=this.tBodies[0],a=this.id,n=function(t){var e=t.data,n=$.map(e,function(t){var e="/"+a+"/"+t.id+"/",i='<td><a href="'+e+'" title="'+t.title+'" target="_blank">'+t.title+"</a></td>",n="<td>"+t.source+"</td>",o="<td>"+t.location+"</td>",s="<td>"+t.time+"</td>",r='<td class="text-center">'+t.hot+"</td>",l="<tr>"+i+n+o+s+r+"</tr>";return l});$(i).html(n)};$.getJSON("/api"+APP.url+a+"/1/",function(i){n(i),e.twbsPagination({totalPages:i.total,visiblePages:7,first:"第一页",prev:"上一页",next:"下一页",last:"最后一页",paginationClass:"pagination pagination-sm no-margin pull-right",onPageClick:function(i,o){APP.returnTop(t),$.getJSON("/api"+APP.url+a+"/"+o+"/",function(t){n(t),e.twbsPagination({totalPages:t.total})})}})})})},APP.dataTable=function(){$.fn.dataTable.ext.errMode="throw",$(".initDataTable").each(function(){var t=$(this).DataTable({ajax:{url:"/api"+location.pathname,dataSrc:this.id,cache:!0},autoWidth:!1,pageLength:25,order:[],language:{processing:"处理中...",search:"",searchPlaceholder:"输入关键字过滤...",lengthMenu:"显示 _MENU_ 条",info:"显示第 _START_ 至 _END_ 条，共 _TOTAL_ 条",infoEmpty:"信息空",infoFiltered:"(由 _MAX_ 项结果过滤)",infoPostFix:"",loadingRecords:"载入中...",zeroRecords:"无匹配结果",emptyTable:"无结果",paginate:{first:"第一页",previous:"上一页",next:"下一页",last:"最后一页"},aria:{sortAscending:"正序排列",sortDescending:"倒序排列"}},deferLoading:100,drawCallback:function(){$('[data-toggle="tooltip"]').tooltip()}});t.on("click","tbody > tr",function(){$(this).hasClass("selected")?$(this).removeClass("selected"):(t.$("tr.selected").removeClass("selected"),$(this).addClass("selected"))})})},APP.sns=function(){var t=$(".sns");t.each(function(e,i){var a=$(i),n=a.parent().next(),o=function(){return"weixin"===APP.type||"weibo"===APP.type?n.data("type"):n.data("type").replace("-","/")};$.getJSON("/api"+APP.url+o()+"/1/",function(e){a.html(e.html),n.twbsPagination({totalPages:e.total,first:"第一页",prev:"上一页",next:"下一页",last:"最后一页",paginationClass:"pagination pagination-sm no-margin pull-right",onPageClick:function(e,i){APP.returnTop(t),$.getJSON("/api"+APP.url+o()+"/"+i+"/",function(t){a.html(t.html),n.twbsPagination({totalPages:t.total})})}})})})},APP.custom=function(){var t=document.forms.addKeyword,e=t.action,i=t.elements,a=i[0],n=i[1],o=i[2],s=$(t).prev(),r=$(t).parent().prev().find("li"),l=function(){o.disabled=!n.value},c=function(i){i.preventDefault(),$.post(e,$(t).serialize(),function(t){t.status?(s.text("关键词添加成功！").show(),location.reload()):(s.text("关键词添加失败！").show(),n.value="")})};r.length>=5?a.disabled=!0:$(t).keyup(l).submit(c)},APP.collection=function(){$(".collection").click(function(){var t=$(this).find("i"),e=$(this).find("span"),i=function(i,a){var n=APP.url.split("/"),o={type:"news"===n[1]?"article":"topic",id:n[2]};$.post(i,o,function(i){i.status&&(t.toggleClass("fa-star-o"),t.toggleClass("fa-star"),e.text(a))})};t.hasClass("fa-star")?i("/api/collection/remove/","添加收藏"):i("/api/collection/add/","取消收藏")})},APP.dashboard=function(){$(".info-box-content").each(function(t,e){var i,a=$(e).find(".info-box-number"),n=$(e).find(".progress-bar"),o=$(e).find(".progress-description"),s=2e3,r=100,l=Math.floor(s/r),c=0,u=0,d=$(e).data("number"),h=Math.floor(d/l),p=0,f=$(e).data("percent"),g=Math.floor(f/l),m=function(){u+=h,p+=g,c++,c>=l&&(clearInterval(i),u=d,p=f),a.text(u.toFixed()),n.width(p+"%"),o.text("占总数据 "+p.toFixed()+"%")};i=setInterval(m,r)})},APP.product=function(){$(".filter-list").find("a").filter(function(){return this.href===location.href}).parent().addClass("active")},APP.inspection=function(){var t=$("#inspection"),e=t.children(".box-body").find("tbody");e.load("/api/dashboard/local-inspection/"),t.on("click","button",function(t){return t.preventDefault(),$(this).hasClass("active")?!1:($(this).addClass("active").siblings().removeClass("active"),void e.load("/api/dashboard/"+this.id+"/"))})},function(t){t.fn.showRisk=function(){var e=this.find("td.risk-score"),i=this.find("td.local-relevance"),a=function(e){return function(i,a){var n=t(a).data("num"),o=t(a).find("i");o.slice(0,n).removeClass(e+"-o").addClass(e)}};return e.each(a("fa-star")),i.each(a("fa-square")),this}}(jQuery),APP.riskList=function(){var t=$("#risk"),e=t.parent(),i=function(t){return"undefined"==typeof t&&(t=1),"/api/risk/news/"+t+"/"},a=function(e){$("<tbody/>").html(e).showRisk().replaceAll(t.find("tbody"))};$.get(i(),function(t){a(t.html),e.twbsPagination({totalPages:t.total,visiblePages:7,first:"第一页",prev:"上一页",next:"下一页",last:"最后一页",paginationClass:"pagination pagination-sm no-margin pull-right",onPageClick:function(t,n){APP.returnTop($(this)),$.get(i(n),function(t){a(t.html),e.twbsPagination({totalPages:t.total})})}})})},$(function(){var t={common:function(){APP.search(),APP.menu()},login:function(){APP.user.login()},dashboard:function(){this.common(),APP.dashboard(),APP.inspection(),APP.chart.map(),$(".table-risk").showRisk(),APP.chart.line(),APP.chart.pie()},news:function(){this.common(),APP.table()},newsItem:function(){this.common(),APP.collection()},event:function(){this.common(),APP.table()},eventItem:function(){this.common(),APP.collection(),APP.chart.line(),APP.chart.pie(),APP.table(),APP.sns()},weixin:function(){this.common(),APP.sns()},weibo:function(){this.weixin()},weixinItem:function(){this.common()},categoryItem:function(){this.common(),APP.table()},locationItem:function(){this.common(),APP.table(),APP.sns()},inspection:function(){this.common(),APP.dataTable()},custom:function(){this.common(),APP.custom()},customItem:function(){this.common(),APP.table(),APP.sns()},product:function(){this.common(),APP.product(),APP.table()},productItem:function(){this.common(),this.product()},risk:function(){this.common(),APP.riskList()},collection:function(){this.common(),APP.table()},settings:function(){this.common(),APP.user.change()},user:function(){this.common(),APP.user.admin(),APP.user.add()},searchItem:function(){this.common(),APP.dataTable()}};return t[APP.type]()});