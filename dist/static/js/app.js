function _init(){$.AdminLTE.layout={activate:function(){var t=this;t.fix(),t.fixSidebar(),$(window,".wrapper").resize(function(){t.fix(),t.fixSidebar()})},fix:function(){var t=$(".main-header").outerHeight()+$(".main-footer").outerHeight(),e=$(window).height(),i=$(".sidebar").height();$("body").hasClass("fixed")?$(".content-wrapper, .right-side").css("min-height",e-$(".main-footer").outerHeight()):e>=i?$(".content-wrapper, .right-side").css("min-height",e-t):$(".content-wrapper, .right-side").css("min-height",i)},fixSidebar:function(){return $("body").hasClass("fixed")?("undefined"==typeof $.fn.slimScroll&&console&&console.error("Error: the fixed layout requires the slimscroll plugin!"),void($.AdminLTE.options.sidebarSlimScroll&&"undefined"!=typeof $.fn.slimScroll&&($(".sidebar").slimScroll({destroy:!0}).height("auto"),$(".sidebar").slimscroll({height:$(window).height()-$(".main-header").height()+"px",color:"rgba(0,0,0,0.2)",size:"3px"})))):void("undefined"!=typeof $.fn.slimScroll&&$(".sidebar").slimScroll({destroy:!0}).height("auto"))}},$.AdminLTE.pushMenu=function(t){var e=this.options.screenSizes;$(t).click(function(t){t.preventDefault(),$(window).width()>e.sm-1?$("body").toggleClass("sidebar-collapse"):$("body").hasClass("sidebar-open")?($("body").removeClass("sidebar-open"),$("body").removeClass("sidebar-collapse")):$("body").addClass("sidebar-open")}),$(".content-wrapper").click(function(){$(window).width()<=e.sm-1&&$("body").hasClass("sidebar-open")&&$("body").removeClass("sidebar-open")})},$.AdminLTE.tree=function(t){var e=this;$("li a",$(t)).click(function(t){var i=$(this),a=i.next();if(a.is(".treeview-menu")&&a.is(":visible"))a.slideUp("normal",function(){a.removeClass("menu-open")}),a.parent("li").removeClass("active");else if(a.is(".treeview-menu")&&!a.is(":visible")){var s=i.parents("ul").first(),n=s.find("ul:visible").slideUp("normal");n.removeClass("menu-open");var o=i.parent("li");a.slideDown("normal",function(){a.addClass("menu-open"),s.find("li.active").removeClass("active"),o.addClass("active"),e.layout.fix()})}a.is(".treeview-menu")&&t.preventDefault()})},$.AdminLTE.boxWidget={activate:function(){var t=$.AdminLTE.options,e=this;$(t.boxWidgetOptions.boxWidgetSelectors.collapse).click(function(t){t.preventDefault(),e.collapse($(this))}),$(t.boxWidgetOptions.boxWidgetSelectors.remove).click(function(t){t.preventDefault(),e.remove($(this))})},collapse:function(t){var e=t.parents(".box").first(),i=e.find(".box-body, .box-footer");e.hasClass("collapsed-box")?(t.children(".fa-plus").removeClass("fa-plus").addClass("fa-minus"),i.slideDown(300,function(){e.removeClass("collapsed-box")})):(t.children(".fa-minus").removeClass("fa-minus").addClass("fa-plus"),i.slideUp(300,function(){e.addClass("collapsed-box")}))},remove:function(t){var e=t.parents(".box").first();e.slideUp()},options:$.AdminLTE.options.boxWidgetOptions}}if(function(e){e.fn.extend({slimScroll:function(i){var a={width:"auto",height:"250px",size:"7px",color:"#000",position:"right",distance:"1px",start:"top",opacity:.4,alwaysVisible:!1,disableFadeOut:!1,railVisible:!1,railColor:"#333",railOpacity:.2,railDraggable:!0,railClass:"slimScrollRail",barClass:"slimScrollBar",wrapperClass:"slimScrollDiv",allowPageScroll:!1,wheelStep:20,touchScrollStep:200,borderRadius:"7px",railBorderRadius:"7px"},s=e.extend(a,i);return this.each(function(){function a(t){if(c){var t=t||window.event,i=0;t.wheelDelta&&(i=-t.wheelDelta/120),t.detail&&(i=t.detail/3);var a=t.target||t.srcTarget||t.srcElement;e(a).closest("."+s.wrapperClass).is(C.parent())&&n(i,!0),t.preventDefault&&!$&&t.preventDefault(),$||(t.returnValue=!1)}}function n(t,e,i){$=!1;var a=t,n=C.outerHeight()-D.outerHeight();if(e&&(a=parseInt(D.css("top"))+t*parseInt(s.wheelStep)/100*D.outerHeight(),a=Math.min(Math.max(a,0),n),a=t>0?Math.ceil(a):Math.floor(a),D.css({top:a+"px"})),b=parseInt(D.css("top"))/(C.outerHeight()-D.outerHeight()),a=b*(C[0].scrollHeight-C.outerHeight()),i){a=t;var o=a/C[0].scrollHeight*C.outerHeight();o=Math.min(Math.max(o,0),n),D.css({top:o+"px"})}C.scrollTop(a),C.trigger("slimscrolling",~~a),l(),p()}function o(){window.addEventListener?(this.addEventListener("DOMMouseScroll",a,!1),this.addEventListener("mousewheel",a,!1)):document.attachEvent("onmousewheel",a)}function r(){g=Math.max(C.outerHeight()/C[0].scrollHeight*C.outerHeight(),w),D.css({height:g+"px"});var t=g==C.outerHeight()?"none":"block";D.css({display:t})}function l(){if(r(),clearTimeout(u),b==~~b){if($=s.allowPageScroll,m!=b){var t=0==~~b?"top":"bottom";C.trigger("slimscroll",t)}}else $=!1;return m=b,g>=C.outerHeight()?void($=!0):(D.stop(!0,!0).fadeIn("fast"),void(s.railVisible&&k.stop(!0,!0).fadeIn("fast")))}function p(){s.alwaysVisible||(u=setTimeout(function(){s.disableFadeOut&&c||d||h||(D.fadeOut("slow"),k.fadeOut("slow"))},1e3))}var c,d,h,u,f,g,b,m,v="<div></div>",w=30,$=!1,C=e(this);if(C.parent().hasClass(s.wrapperClass)){var x=C.scrollTop();if(D=C.parent().find("."+s.barClass),k=C.parent().find("."+s.railClass),r(),e.isPlainObject(i)){if("height"in i&&"auto"==i.height){C.parent().css("height","auto"),C.css("height","auto");var y=C.parent().parent().height();C.parent().css("height",y),C.css("height",y)}if("scrollTo"in i)x=parseInt(s.scrollTo);else if("scrollBy"in i)x+=parseInt(s.scrollBy);else if("destroy"in i)return D.remove(),k.remove(),void C.unwrap();n(x,!1,!0)}}else if(!(e.isPlainObject(i)&&"destroy"in i)){s.height="auto"==s.height?C.parent().height():s.height;var P=e(v).addClass(s.wrapperClass).css({position:"relative",overflow:"hidden",width:s.width,height:s.height});C.css({overflow:"hidden",width:s.width,height:s.height,"-ms-touch-action":"none"});var k=e(v).addClass(s.railClass).css({width:s.size,height:"100%",position:"absolute",top:0,display:s.alwaysVisible&&s.railVisible?"block":"none","border-radius":s.railBorderRadius,background:s.railColor,opacity:s.railOpacity,zIndex:90}),D=e(v).addClass(s.barClass).css({background:s.color,width:s.size,position:"absolute",top:0,opacity:s.opacity,display:s.alwaysVisible?"block":"none","border-radius":s.borderRadius,BorderRadius:s.borderRadius,MozBorderRadius:s.borderRadius,WebkitBorderRadius:s.borderRadius,zIndex:99}),S="right"==s.position?{right:s.distance}:{left:s.distance};k.css(S),D.css(S),C.wrap(P),C.parent().append(D),C.parent().append(k),s.railDraggable&&D.bind("mousedown",function(i){var a=e(document);return h=!0,t=parseFloat(D.css("top")),pageY=i.pageY,a.bind("mousemove.slimscroll",function(e){currTop=t+e.pageY-pageY,D.css("top",currTop),n(0,D.position().top,!1)}),a.bind("mouseup.slimscroll",function(t){h=!1,p(),a.unbind(".slimscroll")}),!1}).bind("selectstart.slimscroll",function(t){return t.stopPropagation(),t.preventDefault(),!1}),k.hover(function(){l()},function(){p()}),D.hover(function(){d=!0},function(){d=!1}),C.hover(function(){c=!0,l(),p()},function(){c=!1,p()}),window.navigator.msPointerEnabled?(C.bind("MSPointerDown",function(t,e){t.originalEvent.targetTouches.length&&(f=t.originalEvent.targetTouches[0].pageY)}),C.bind("MSPointerMove",function(t){if(t.originalEvent.preventDefault(),t.originalEvent.targetTouches.length){var e=(f-t.originalEvent.targetTouches[0].pageY)/s.touchScrollStep;n(e,!0),f=t.originalEvent.targetTouches[0].pageY}})):(C.bind("touchstart",function(t,e){t.originalEvent.touches.length&&(f=t.originalEvent.touches[0].pageY)}),C.bind("touchmove",function(t){if($||t.originalEvent.preventDefault(),t.originalEvent.touches.length){var e=(f-t.originalEvent.touches[0].pageY)/s.touchScrollStep;n(e,!0),f=t.originalEvent.touches[0].pageY}})),r(),"bottom"===s.start?(D.css({top:C.outerHeight()-D.outerHeight()}),n(0,!0)):"top"!==s.start&&(n(e(s.start).position().top,null,!0),s.alwaysVisible||D.hide()),o()}}),this}}),e.fn.extend({slimscroll:e.fn.slimScroll})}(jQuery),"undefined"==typeof jQuery)throw new Error("AdminLTE requires jQuery");$.AdminLTE={},$.AdminLTE.options={navbarMenuSlimscroll:!0,navbarMenuSlimscrollWidth:"3px",navbarMenuHeight:"200px",sidebarToggleSelector:"[data-toggle='offcanvas']",sidebarPushMenu:!0,sidebarSlimScroll:!0,enableBoxRefresh:!0,enableBSToppltip:!0,BSTooltipSelector:"[data-toggle='tooltip']",enableFastclick:!0,enableBoxWidget:!0,boxWidgetOptions:{boxWidgetIcons:{collapse:"fa fa-minus",open:"fa fa-plus",remove:"fa fa-times"},boxWidgetSelectors:{remove:'[data-widget="remove"]',collapse:'[data-widget="collapse"]'}},directChat:{enable:!0,contactToggleSelector:'[data-widget="chat-pane-toggle"]'},colors:{lightBlue:"#3c8dbc",red:"#f56954",green:"#00a65a",aqua:"#00c0ef",yellow:"#f39c12",blue:"#0073b7",navy:"#001F3F",teal:"#39CCCC",olive:"#3D9970",lime:"#01FF70",orange:"#FF851B",fuchsia:"#F012BE",purple:"#8E24AA",maroon:"#D81B60",black:"#222222",gray:"#d2d6de"},screenSizes:{xs:480,sm:768,md:992,lg:1200}},$(function(){var t=$.AdminLTE.options;_init(),$.AdminLTE.layout.activate(),$.AdminLTE.tree(".sidebar"),t.navbarMenuSlimscroll&&"undefined"!=typeof $.fn.slimscroll&&$(".navbar .menu").slimscroll({height:"200px",alwaysVisible:!1,size:"3px"}).css("width","100%"),t.sidebarPushMenu&&$.AdminLTE.pushMenu(t.sidebarToggleSelector),t.enableBSToppltip&&$(t.BSTooltipSelector).tooltip(),t.enableBoxWidget&&$.AdminLTE.boxWidget.activate(),t.enableFastclick&&"undefined"!=typeof FastClick&&FastClick.attach(document.body),t.directChat.enable&&$(t.directChat.contactToggleSelector).click(function(){var t=$(this).parents(".direct-chat").first();t.toggleClass("direct-chat-contacts-open")}),$('.btn-group[data-toggle="btn-toggle"]').each(function(){var t=$(this);$(this).find(".btn").click(function(e){t.find(".btn.active").removeClass("active"),$(this).addClass("active"),e.preventDefault()})})}),function(t){t.fn.boxRefresh=function(e){function i(t){t.append(n),s.onLoadStart.call(t)}function a(t){t.find(n).remove(),s.onLoadDone.call(t)}var s=t.extend({trigger:".refresh-btn",source:"",onLoadStart:function(t){},onLoadDone:function(t){}},e),n=t('<div class="overlay"><div class="fa fa-refresh fa-spin"></div></div>');return this.each(function(){if(""===s.source)return void(console&&console.log("Please specify a source first - boxRefresh()"));var e=t(this),n=e.find(s.trigger).first();n.click(function(t){t.preventDefault(),i(e),e.find(".box-body").load(s.source,function(){a(e)})})})}}(jQuery),function(t){t.fn.todolist=function(e){var i=t.extend({onCheck:function(t){},onUncheck:function(t){}},e);return this.each(function(){"undefined"!=typeof t.fn.iCheck?(t("input",this).on("ifChecked",function(e){var a=t(this).parents("li").first();a.toggleClass("done"),i.onCheck.call(a)}),t("input",this).on("ifUnchecked",function(e){var a=t(this).parents("li").first();a.toggleClass("done"),i.onUncheck.call(a)})):t("input",this).on("change",function(e){var a=t(this).parents("li").first();a.toggleClass("done"),i.onCheck.call(a)})})}}(jQuery),function(t,e,i,a){"use strict";var s=t.fn.twbsPagination,n=function(i,a){if(this.$element=t(i),this.options=t.extend({},t.fn.twbsPagination.defaults,a),this.options.startPage<1||this.options.startPage>this.options.totalPages)throw new Error("Start page option is incorrect");if(this.options.totalPages=parseInt(this.options.totalPages),isNaN(this.options.totalPages))throw new Error("Total pages option is not correct!");if(this.options.visiblePages=parseInt(this.options.visiblePages),isNaN(this.options.visiblePages))throw new Error("Visible pages option is not correct!");if(this.options.totalPages<this.options.visiblePages&&(this.options.visiblePages=this.options.totalPages),this.options.onPageClick instanceof Function&&this.$element.first().bind("page",this.options.onPageClick),this.options.href){var s,n=this.options.href.replace(/[-\/\\^$*+?.|[\]]/g,"\\$&");n=n.replace(this.options.hrefVariable,"(\\d+)"),null!=(s=new RegExp(n,"i").exec(e.location.href))&&(this.options.startPage=parseInt(s[1],10))}var o="function"==typeof this.$element.prop?this.$element.prop("tagName"):this.$element.attr("tagName");return this.$listContainer="UL"===o?this.$element:t("<ul></ul>"),this.$listContainer.addClass(this.options.paginationClass),"UL"!==o&&this.$element.append(this.$listContainer),this.render(this.getPages(this.options.startPage)),this.setupEvents(),this};n.prototype={constructor:n,destroy:function(){return this.$element.empty(),this.$element.removeData("twbs-pagination"),this.$element.unbind("page"),this},show:function(t){if(1>t||t>this.options.totalPages)throw new Error("Page is incorrect.");return this.render(this.getPages(t)),this.setupEvents(),this.$element.trigger("page",t),this},buildListItems:function(e){var i=t();if(this.options.first&&(i=i.add(this.buildItem("first",1))),this.options.prev){var a=e.currentPage>1?e.currentPage-1:this.options.loop?this.options.totalPages:1;i=i.add(this.buildItem("prev",a))}for(var s=0;s<e.numeric.length;s++)i=i.add(this.buildItem("page",e.numeric[s]));if(this.options.next){var n=e.currentPage<this.options.totalPages?e.currentPage+1:this.options.loop?1:this.options.totalPages;i=i.add(this.buildItem("next",n))}return this.options.last&&(i=i.add(this.buildItem("last",this.options.totalPages))),i},buildItem:function(e,i){var a=t("<li></li>"),s=t("<a></a>"),n=null;switch(e){case"page":n=i,a.addClass(this.options.pageClass);break;case"first":n=this.options.first,a.addClass(this.options.firstClass);break;case"prev":n=this.options.prev,a.addClass(this.options.prevClass);break;case"next":n=this.options.next,a.addClass(this.options.nextClass);break;case"last":n=this.options.last,a.addClass(this.options.lastClass)}return a.data("page",i),a.data("page-type",e),a.append(s.attr("href",this.makeHref(i)).html(n)),a},getPages:function(t){var e=[],i=Math.floor(this.options.visiblePages/2),a=t-i+1-this.options.visiblePages%2,s=t+i;0>=a&&(a=1,s=this.options.visiblePages),s>this.options.totalPages&&(a=this.options.totalPages-this.options.visiblePages+1,s=this.options.totalPages);for(var n=a;s>=n;)e.push(n),n++;return{currentPage:t,numeric:e}},render:function(e){this.$listContainer.children().remove(),this.$listContainer.append(this.buildListItems(e));var i=this.$listContainer.children();i.filter(function(){return t(this).data("page")===e.currentPage&&"page"===t(this).data("page-type")}).addClass(this.options.activeClass),i.filter(function(){return"first"===t(this).data("page-type")}).toggleClass(this.options.disabledClass,1===e.currentPage),i.filter(function(){return"last"===t(this).data("page-type")}).toggleClass(this.options.disabledClass,e.currentPage===this.options.totalPages),i.filter(function(){return"prev"===t(this).data("page-type")}).toggleClass(this.options.disabledClass,!this.options.loop&&1===e.currentPage),i.filter(function(){return"next"===t(this).data("page-type")}).toggleClass(this.options.disabledClass,!this.options.loop&&e.currentPage===this.options.totalPages)},setupEvents:function(){var e=this;this.$listContainer.find("li").each(function(){var i=t(this);return i.off(),i.hasClass(e.options.disabledClass)||i.hasClass(e.options.activeClass)?void i.click(function(t){t.preventDefault()}):void i.click(function(t){!e.options.href&&t.preventDefault(),e.show(parseInt(i.data("page"),10))})})},makeHref:function(t){return this.options.href?this.options.href.replace(this.options.hrefVariable,t):"#"}},t.fn.twbsPagination=function(e){var i,s=Array.prototype.slice.call(arguments,1),o=t(this),r=o.data("twbs-pagination"),l="object"==typeof e&&e;return r||o.data("twbs-pagination",r=new n(this,l)),"string"==typeof e&&(i=r[e].apply(r,s)),i===a?o:i},t.fn.twbsPagination.defaults={totalPages:0,startPage:1,visiblePages:5,href:!1,hrefVariable:"{{number}}",first:"First",prev:"Previous",next:"Next",last:"Last",loop:!1,onPageClick:null,paginationClass:"pagination",nextClass:"next",prevClass:"prev",lastClass:"last",firstClass:"first",pageClass:"page",activeClass:"active",disabledClass:"disabled"},t.fn.twbsPagination.Constructor=n,t.fn.twbsPagination.noConflict=function(){return t.fn.twbsPagination=s,this}}(jQuery,window,document),require.config({paths:{echarts:"/vendor/echarts"}}),$.fn.Do=function(t){return this.length&&t.apply(this),this},$.fn.Trim=function(){var t=this.find("input").val(),e=$.trim(t);return e};var app={};app.url=location.pathname,app.type=location.pathname.split("/")[1]||"dashboard",app.user={login:function(){var t=this.find("form"),e=this.find("p");t.submit(function(t){t.preventDefault();var i={username:$("#username").Trim(),password:$("#password").Trim()},a=function(t){t.status?location.href=location.search.length?location.search.substr(1).split("=")[1]:"/":e.text("用户名或密码错误！")};i.username.length&&i.password.length?$.post("/api/login/",i,a,"json"):e.text("请输入用户名和密码！")})},change:function(){var t=this.find("form"),e=this.find("p");t.submit(function(t){t.preventDefault();var i={username:$("#username").Trim(),oldPassword:$("#old-password").Trim(),newPassword:$("#new-password").Trim(),retype:$("#retype-password").Trim()},a=function(t){t.status?(e.text("更新成功！").show(),location.href="/login/"):e.text("原密码错误！").show()};switch(0){case i.username.length:e.text("请输入姓名！").show();break;case i.oldPassword.length:e.text("请输入原密码！").show();break;case i.newPassword.length:e.text("请输入新密码！").show();break;case i.retype.length:e.text("请确认密码！").show();break;case Number(i.newPassword===i.retype):e.text("两次输入密码不一致！").show();break;default:var s={username:i.username,oldPassword:i.oldPassword,newPassword:i.newPassword};$.post("/api/settings/change/",s,a,"json")}})},management:function(){var t=this,e=t.find("button"),i=e.eq(0),a=e.eq(1),s=[],n=function(e,i){e.click(function(){s.length=0,t.find("input:checked").each(function(t,e){var i=$(e).parent().next().data("id");s.push(i)});var e=function(t){t.status&&(location.href="/user/")};s.length&&$.post(i,{id:s.toString()},e,"json")})};n(i,"/api/user/reset/"),n(a,"/api/user/remove/")},add:function(){var t=this.find("form"),e=this.find("p");t.submit(function(t){t.preventDefault();var i={username:$("#username").Trim(),password:$("#password").Trim(),retype:$("#retype-password").Trim()},a=function(t){t.status?location.href="/user/":e.text("抱歉，注册失败！").show()};switch(0){case i.username.length:e.text("请输入用户名！").show();break;case i.password.length:e.text("请输入密码!").show();break;case i.retype.length:e.text("请确认密码！").show();break;case Number(i.password===i.retype):e.text("两次输入密码不一致！").show();break;default:var s={username:i.username,password:i.password};$.post("/api/user/add/",s,a,"json")}})}},app.search=function(){this.submit(function(t){t.preventDefault();var e=$(this).Trim();e.length&&(location.href="/search/"+e+"/")})},app.menu=function(){var t=this.find("a").filter(function(){return this.href===location.href});t.parent().addClass("active"),t.closest(".treeview-menu").addClass("menu-open"),t.closest(".treeview").addClass("active")},app.chart={line:function(){require(["echarts","echarts/chart/line"],function(t){$.getJSON("/api/line"+app.url,function(e){t.init(document.getElementById("line-chart"),"macarons").setOption({tooltip:{trigger:"axis"},legend:{data:["正面","中性","负面"]},grid:{x:40,y:30,x2:25,y2:30},xAxis:[{type:"category",boundaryGap:!1,data:e.date}],yAxis:[{type:"value"}],series:[{name:"正面",type:"line",data:e.positive},{name:"中性",type:"line",data:e.neutral},{name:"负面",type:"line",data:e.negative}]})})})},pie:function(){require(["echarts","echarts/chart/pie"],function(t){$.getJSON("/api/pie"+app.url,function(e){t.init(document.getElementById("pie-chart"),"macarons").setOption({tooltip:{trigger:"item",formatter:"{a} <br/>{b} : {c} ({d}%)"},legend:{data:e.name},series:[{name:"信息比例",type:"pie",radius:"55%",center:["50%","60%"],data:e.value}]})})})}},app.table=function(){var t=this,e=this.find("tbody"),i=this.parent(),a=this[0].id,s=function(t){var i=t.data,s=$.map(i,function(t,e){var i='<td><a href="/'+a+"/"+t.id+'/" title="'+t.title+'" target="_blank">'+t.title+"</a></td>",s="<td>"+t.source+"</td>",n="<td>"+t.location+"</td>",o="<td>"+t.time+"</td>",r='<td class="text-center">'+t.hot+"</td>",l="<tr>"+i+s+n+o+r+"</tr>";return l});e.html(s)},n=function(){var e=t.offset().top,i=0;160!==e&&(i=e-120),$("body").animate({scrollTop:i},"fast")};$.getJSON("/api"+app.url+a+"/1/",function(t){s(t),i.twbsPagination({totalPages:t.total,visiblePages:7,first:"第一页",prev:"上一页",next:"下一页",last:"最后一页",paginationClass:"pagination pagination-sm no-margin pull-right",onPageClick:function(t,e){$.getJSON("/api"+app.url+a+"/"+e+"/",function(t){s(t),i.twbsPagination({totalPages:t.total}),n()})}})})},app.dataTable=function(){$.fn.dataTable.ext.errMode="throw";var t=this.DataTable({ajax:{url:"/api"+location.pathname,dataSrc:this[0].id,cache:!0},autoWidth:!1,pageLength:25,order:[],language:{processing:"处理中...",search:"",searchPlaceholder:"输入关键字过滤...",lengthMenu:"显示 _MENU_ 条",info:"显示第 _START_ 至 _END_ 条，共 _TOTAL_ 条",infoEmpty:"信息空",infoFiltered:"(由 _MAX_ 项结果过滤)",infoPostFix:"",loadingRecords:"载入中...",zeroRecords:"无匹配结果",emptyTable:"无结果",paginate:{first:"第一页",previous:"上一页",next:"下一页",last:"最后一页"},aria:{sortAscending:"正序排列",sortDescending:"倒序排列"}},columnDefs:[{className:"star",targets:0,searchable:!1,orderable:!1},{className:"index",targets:-1}],deferLoading:100,drawCallback:function(){$('[data-toggle="tooltip"]').tooltip()}});t.on("click","tr",function(){$(this).hasClass("selected")?$(this).removeClass("selected"):(t.$("tr.selected").removeClass("selected"),$(this).addClass("selected"))})},app.sns=function(){this.each(function(t,e){var i=$(e),a=i.parent().next(),s=function(){return"weixin"===app.type||"weibo"===app.type?a.data("type"):a.data("type").replace("-","/")};$.getJSON("/api"+app.url+s()+"/1/",function(t){i.html(t.html),a.twbsPagination({totalPages:t.total,href:"#top",first:"第一页",prev:"上一页",next:"下一页",last:"最后一页",paginationClass:"pagination pagination-sm no-margin pull-right",onPageClick:function(t,e){$.getJSON("/api"+app.url+s()+"/"+e+"/",function(t){i.html(t.html),a.twbsPagination({totalPages:t.total})})}})})})},$(function(){if("login"===app.type)$(".login-box").Do(app.user.login);else switch($("aside").find("form").Do(app.search),$("aside").Do(app.menu),app.type){case"dashboard":$("#line-chart").Do(app.chart.line),$("#pie-chart").Do(app.chart.pie);break;case"news":$("#news").Do(app.table);break;case"event":$("#event").Do(app.table),$("#line-chart").Do(app.chart.line),$("#pie-chart").Do(app.chart.pie),$("#news").Do(app.table),$(".sns").Do(app.sns);break;case"weixin":case"weibo":$(".sns").Do(app.sns);break;case"category":case"location":$("#news").Do(app.table),$(".sns").Do(app.sns);break;case"inspection":$("#inspection").Do(app.dataTable);break;case"custom":$("#news").Do(app.table),$(".sns").Do(app.sns);break;case"collection":$("#news").Do(app.table),$("#event").Do(app.table);break;case"settings":$(".user-info").Do(app.user.change);break;case"user":$(".user-management").Do(app.user.management),$(".user-add").Do(app.user.add);break;case"search":$("#news").Do(app.table),$("#event").Do(app.table);break;default:console.log("unknown type")}});