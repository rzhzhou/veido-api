if(function(e){e.fn.extend({slimScroll:function(i){var a={width:"auto",height:"250px",size:"7px",color:"#000",position:"right",distance:"1px",start:"top",opacity:.4,alwaysVisible:!1,disableFadeOut:!1,railVisible:!1,railColor:"#333",railOpacity:.2,railDraggable:!0,railClass:"slimScrollRail",barClass:"slimScrollBar",wrapperClass:"slimScrollDiv",allowPageScroll:!1,wheelStep:20,touchScrollStep:200,borderRadius:"7px",railBorderRadius:"7px"},o=e.extend(a,i);return this.each(function(){function a(t){if(d){var t=t||window.event,i=0;t.wheelDelta&&(i=-t.wheelDelta/120),t.detail&&(i=t.detail/3);var a=t.target||t.srcTarget||t.srcElement;e(a).closest("."+o.wrapperClass).is(x.parent())&&n(i,!0),t.preventDefault&&!w&&t.preventDefault(),w||(t.returnValue=!1)}}function n(e,t,i){w=!1;var a=e,n=x.outerHeight()-D.outerHeight();if(t&&(a=parseInt(D.css("top"))+e*parseInt(o.wheelStep)/100*D.outerHeight(),a=Math.min(Math.max(a,0),n),a=e>0?Math.ceil(a):Math.floor(a),D.css({top:a+"px"})),m=parseInt(D.css("top"))/(x.outerHeight()-D.outerHeight()),a=m*(x[0].scrollHeight-x.outerHeight()),i){a=e;var s=a/x[0].scrollHeight*x.outerHeight();s=Math.min(Math.max(s,0),n),D.css({top:s+"px"})}x.scrollTop(a),x.trigger("slimscrolling",~~a),l(),c()}function s(){window.addEventListener?(this.addEventListener("DOMMouseScroll",a,!1),this.addEventListener("mousewheel",a,!1)):document.attachEvent("onmousewheel",a)}function r(){g=Math.max(x.outerHeight()/x[0].scrollHeight*x.outerHeight(),$),D.css({height:g+"px"});var e=g==x.outerHeight()?"none":"block";D.css({display:e})}function l(){if(r(),clearTimeout(h),m==~~m){if(w=o.allowPageScroll,v!=m){var e=0==~~m?"top":"bottom";x.trigger("slimscroll",e)}}else w=!1;return v=m,g>=x.outerHeight()?void(w=!0):(D.stop(!0,!0).fadeIn("fast"),void(o.railVisible&&S.stop(!0,!0).fadeIn("fast")))}function c(){o.alwaysVisible||(h=setTimeout(function(){o.disableFadeOut&&d||u||p||(D.fadeOut("slow"),S.fadeOut("slow"))},1e3))}var d,u,p,h,f,g,m,v,b="<div></div>",$=30,w=!1,x=e(this);if(x.parent().hasClass(o.wrapperClass)){var y=x.scrollTop();if(D=x.parent().find("."+o.barClass),S=x.parent().find("."+o.railClass),r(),e.isPlainObject(i)){if("height"in i&&"auto"==i.height){x.parent().css("height","auto"),x.css("height","auto");var C=x.parent().parent().height();x.parent().css("height",C),x.css("height",C)}if("scrollTo"in i)y=parseInt(o.scrollTo);else if("scrollBy"in i)y+=parseInt(o.scrollBy);else if("destroy"in i)return D.remove(),S.remove(),void x.unwrap();n(y,!1,!0)}}else if(!(e.isPlainObject(i)&&"destroy"in i)){o.height="auto"==o.height?x.parent().height():o.height;var T=e(b).addClass(o.wrapperClass).css({position:"relative",overflow:"hidden",width:o.width,height:o.height});x.css({overflow:"hidden",width:o.width,height:o.height,"-ms-touch-action":"none"});var S=e(b).addClass(o.railClass).css({width:o.size,height:"100%",position:"absolute",top:0,display:o.alwaysVisible&&o.railVisible?"block":"none","border-radius":o.railBorderRadius,background:o.railColor,opacity:o.railOpacity,zIndex:90}),D=e(b).addClass(o.barClass).css({background:o.color,width:o.size,position:"absolute",top:0,opacity:o.opacity,display:o.alwaysVisible?"block":"none","border-radius":o.borderRadius,BorderRadius:o.borderRadius,MozBorderRadius:o.borderRadius,WebkitBorderRadius:o.borderRadius,zIndex:99}),E="right"==o.position?{right:o.distance}:{left:o.distance};S.css(E),D.css(E),x.wrap(T),x.parent().append(D),x.parent().append(S),o.railDraggable&&D.bind("mousedown",function(i){var a=e(document);return p=!0,t=parseFloat(D.css("top")),pageY=i.pageY,a.bind("mousemove.slimscroll",function(e){currTop=t+e.pageY-pageY,D.css("top",currTop),n(0,D.position().top,!1)}),a.bind("mouseup.slimscroll",function(){p=!1,c(),a.unbind(".slimscroll")}),!1}).bind("selectstart.slimscroll",function(e){return e.stopPropagation(),e.preventDefault(),!1}),S.hover(function(){l()},function(){c()}),D.hover(function(){u=!0},function(){u=!1}),x.hover(function(){d=!0,l(),c()},function(){d=!1,c()}),window.navigator.msPointerEnabled?(x.bind("MSPointerDown",function(e){e.originalEvent.targetTouches.length&&(f=e.originalEvent.targetTouches[0].pageY)}),x.bind("MSPointerMove",function(e){if(e.originalEvent.preventDefault(),e.originalEvent.targetTouches.length){var t=(f-e.originalEvent.targetTouches[0].pageY)/o.touchScrollStep;n(t,!0),f=e.originalEvent.targetTouches[0].pageY}})):(x.bind("touchstart",function(e){e.originalEvent.touches.length&&(f=e.originalEvent.touches[0].pageY)}),x.bind("touchmove",function(e){if(w||e.originalEvent.preventDefault(),e.originalEvent.touches.length){var t=(f-e.originalEvent.touches[0].pageY)/o.touchScrollStep;n(t,!0),f=e.originalEvent.touches[0].pageY}})),r(),"bottom"===o.start?(D.css({top:x.outerHeight()-D.outerHeight()}),n(0,!0)):"top"!==o.start&&(n(e(o.start).position().top,null,!0),o.alwaysVisible||D.hide()),s()}}),this}}),e.fn.extend({slimscroll:e.fn.slimScroll})}(jQuery),"undefined"==typeof jQuery)throw new Error("AdminLTE requires jQuery");$.AdminLTE={},$.AdminLTE.options={navbarMenuSlimscroll:!0,navbarMenuSlimscrollWidth:"3px",navbarMenuHeight:"200px",sidebarToggleSelector:"[data-toggle='offcanvas']",sidebarPushMenu:!0,sidebarSlimScroll:!0,enableBoxRefresh:!0,enableBSToppltip:!0,BSTooltipSelector:"[data-toggle='tooltip']",enableFastclick:!0,enableBoxWidget:!0,boxWidgetOptions:{boxWidgetIcons:{collapse:"fa fa-minus",open:"fa fa-plus",remove:"fa fa-times"},boxWidgetSelectors:{remove:'[data-widget="remove"]',collapse:'[data-widget="collapse"]'}},directChat:{enable:!0,contactToggleSelector:'[data-widget="chat-pane-toggle"]'},colors:{lightBlue:"#3c8dbc",red:"#f56954",green:"#00a65a",aqua:"#00c0ef",yellow:"#f39c12",blue:"#0073b7",navy:"#001F3F",teal:"#39CCCC",olive:"#3D9970",lime:"#01FF70",orange:"#FF851B",fuchsia:"#F012BE",purple:"#8E24AA",maroon:"#D81B60",black:"#222222",gray:"#d2d6de"},screenSizes:{xs:480,sm:768,md:992,lg:1200}},$(function(){var e=$.AdminLTE.options;$.AdminLTE.layout.activate(),$.AdminLTE.tree(".sidebar"),e.navbarMenuSlimscroll&&"undefined"!=typeof $.fn.slimscroll&&$(".navbar .menu").slimscroll({height:"200px",alwaysVisible:!1,size:"3px"}).css("width","100%"),e.sidebarPushMenu&&$.AdminLTE.pushMenu(e.sidebarToggleSelector),e.enableBSToppltip&&$(e.BSTooltipSelector).tooltip(),e.enableBoxWidget&&$.AdminLTE.boxWidget.activate(),e.enableFastclick&&"undefined"!=typeof FastClick&&FastClick.attach(document.body),e.directChat.enable&&$(e.directChat.contactToggleSelector).click(function(){var e=$(this).parents(".direct-chat").first();e.toggleClass("direct-chat-contacts-open")}),$('.btn-group[data-toggle="btn-toggle"]').each(function(){var e=$(this);$(this).find(".btn").click(function(t){e.find(".btn.active").removeClass("active"),$(this).addClass("active"),t.preventDefault()})})}),$.AdminLTE.layout={activate:function(){var e=this;e.fix(),e.fixSidebar(),$(window,".wrapper").resize(function(){e.fix(),e.fixSidebar()})},fix:function(){var e=$(".main-header").outerHeight()+$(".main-footer").outerHeight(),t=$(window).height(),i=$(".sidebar").height();$("body").hasClass("fixed")?$(".content-wrapper, .right-side").css("min-height",t-$(".main-footer").outerHeight()):t>=i?$(".content-wrapper, .right-side").css("min-height",t-e):$(".content-wrapper, .right-side").css("min-height",i)},fixSidebar:function(){return $("body").hasClass("fixed")?("undefined"==typeof $.fn.slimScroll&&console&&console.error("Error: the fixed layout requires the slimscroll plugin!"),void($.AdminLTE.options.sidebarSlimScroll&&"undefined"!=typeof $.fn.slimScroll&&($(".sidebar").slimScroll({destroy:!0}).height("auto"),$(".sidebar").slimscroll({height:$(window).height()-$(".main-header").height()+"px",color:"rgba(0,0,0,0.2)",size:"3px"})))):void("undefined"!=typeof $.fn.slimScroll&&$(".sidebar").slimScroll({destroy:!0}).height("auto"))}},$.AdminLTE.pushMenu=function(e){var t=this.options.screenSizes;$(e).click(function(e){e.preventDefault(),$(window).width()>t.sm-1?$("body").toggleClass("sidebar-collapse"):$("body").hasClass("sidebar-open")?($("body").removeClass("sidebar-open"),$("body").removeClass("sidebar-collapse")):$("body").addClass("sidebar-open")}),$(".content-wrapper").click(function(){$(window).width()<=t.sm-1&&$("body").hasClass("sidebar-open")&&$("body").removeClass("sidebar-open")})},$.AdminLTE.tree=function(e){var t=this;$("li a",$(e)).click(function(e){var i=$(this),a=i.next();if(a.is(".treeview-menu")&&a.is(":visible"))a.slideUp("normal",function(){a.removeClass("menu-open")}),a.parent("li").removeClass("active");else if(a.is(".treeview-menu")&&!a.is(":visible")){var o=i.parents("ul").first(),n=o.find("ul:visible").slideUp("normal");n.removeClass("menu-open");var s=i.parent("li");a.slideDown("normal",function(){a.addClass("menu-open"),o.find("li.active").removeClass("active"),s.addClass("active"),t.layout.fix()})}a.is(".treeview-menu")&&e.preventDefault()})},$.AdminLTE.boxWidget={activate:function(){var e=$.AdminLTE.options,t=this;$(e.boxWidgetOptions.boxWidgetSelectors.collapse).click(function(e){e.preventDefault(),t.collapse($(this))}),$(e.boxWidgetOptions.boxWidgetSelectors.remove).click(function(e){e.preventDefault(),t.remove($(this))})},collapse:function(e){var t=e.parents(".box").first(),i=t.find(".box-body, .box-footer");t.hasClass("collapsed-box")?(e.children(".fa-plus").removeClass("fa-plus").addClass("fa-minus"),i.slideDown(300,function(){t.removeClass("collapsed-box")})):(e.children(".fa-minus").removeClass("fa-minus").addClass("fa-plus"),i.slideUp(300,function(){t.addClass("collapsed-box")}))},remove:function(e){var t=e.parents(".box").first();t.slideUp()},options:$.AdminLTE.options.boxWidgetOptions},function(e){e.fn.boxRefresh=function(t){function i(e){e.append(n),o.onLoadStart.call(e)}function a(e){e.find(n).remove(),o.onLoadDone.call(e)}var o=e.extend({trigger:".refresh-btn",source:"",onLoadStart:function(){},onLoadDone:function(){}},t),n=e('<div class="overlay"><div class="fa fa-refresh fa-spin"></div></div>');return this.each(function(){if(""===o.source)return void(console&&console.log("Please specify a source first - boxRefresh()"));var t=e(this),n=t.find(o.trigger).first();n.click(function(e){e.preventDefault(),i(t),t.find(".box-body").load(o.source,function(){a(t)})})})}}(jQuery),function(e){e.fn.todolist=function(t){var i=e.extend({onCheck:function(){},onUncheck:function(){}},t);return this.each(function(){"undefined"!=typeof e.fn.iCheck?(e("input",this).on("ifChecked",function(){var t=e(this).parents("li").first();t.toggleClass("done"),i.onCheck.call(t)}),e("input",this).on("ifUnchecked",function(){var t=e(this).parents("li").first();t.toggleClass("done"),i.onUncheck.call(t)})):e("input",this).on("change",function(){var t=e(this).parents("li").first();t.toggleClass("done"),i.onCheck.call(t)})})}}(jQuery),require.config({paths:{echarts:"/vendor/echarts"}}),$.fn.Do=function(e){return this.length&&e.apply(this),this},$.fn.Trim=function(){var e=this.find("input").val(),t=$.trim(e);return t};var app={};app.user={login:function(){var e=this.find("form"),t=this.find("p");e.submit(function(e){e.preventDefault();var i={username:$("#username").Trim(),password:$("#password").Trim()},a=function(e){e.status?location.href=location.search.length?location.search.substr(1).split("=")[1]:"/":t.text("用户名或密码错误！")};i.username.length&&i.password.length?$.post("/api/login/",i,a,"json"):t.text("请输入用户名和密码！")})},register:function(){var e=this.find("form"),t=this.find("p");e.submit(function(e){e.preventDefault();var i={username:$("#username").Trim(),password:$("#password").Trim(),retype:$("#retype-password").Trim()},a=function(e){e.status?location.href="/":t.text("抱歉，注册失败！")};switch(0){case i.username.length:t.text("请输入用户名！");break;case i.password.length:t.text("请输入密码!");break;case i.retype.length:t.text("请确认密码！");break;case Number(i.password===i.retype):t.text("两次输入密码不一致！");break;default:$.post("/api/register/",{username:i.username,password:i.password},a,"json")}})},icon:function(){console.log("change icon function")},info:function(){{var e=this.find("form");this.find("p")}e.submit(function(e){e.preventDefault();({username:$("#username").Trim(),oldPassword:$("#old-password").Trim(),newPassword:$("#new-password").Trim(),retype:$("#retype-password").Trim()})})}},app.chart={line:function(){require(["echarts","echarts/chart/line"],function(e){e.init(document.getElementById("line-chart"),"macarons").setOption({tooltip:{trigger:"axis"},legend:{data:["标准化","稽查打假","质量监管","科技兴检","特种设备"]},grid:{x:40,y:30,x2:10,y2:30},xAxis:[{type:"category",boundaryGap:!1,data:["周一","周二","周三","周四","周五","周六","周日"]}],yAxis:[{type:"value"}],series:[{name:"标准化",type:"line",stack:"总量",data:[120,132,101,134,90,230,210]},{name:"稽查打假",type:"line",stack:"总量",data:[220,182,191,234,290,330,310]},{name:"质量监管",type:"line",stack:"总量",data:[150,232,201,154,190,330,410]},{name:"科技兴检",type:"line",stack:"总量",data:[320,332,301,334,390,330,320]},{name:"特种设备",type:"line",stack:"总量",data:[820,932,901,934,1290,1330,1320]}]})})},pie:function(){require(["echarts","echarts/chart/pie"],function(e){e.init(document.getElementById("pie-chart"),"macarons").setOption({tooltip:{trigger:"item",formatter:"{a} <br/>{b} : {c} ({d}%)"},legend:{data:["江岸","洪山","江夏","东西湖"]},series:[{name:"信息比例",type:"pie",radius:"55%",center:["50%","60%"],data:[{value:335,name:"江岸"},{value:310,name:"洪山"},{value:234,name:"江夏"},{value:135,name:"东西湖"}]}]})})}},app.table=function(){$.fn.dataTable.ext.errMode="throw";var e=this.DataTable({ajax:{url:"/api"+location.pathname,dataSrc:this[0].id,cache:!0},autoWidth:!1,pageLength:25,order:[],language:{processing:"处理中...",search:"",searchPlaceholder:"输入关键字过滤...",lengthMenu:"显示 _MENU_ 条",info:"显示第 _START_ 至 _END_ 条，共 _TOTAL_ 条",infoEmpty:"信息空",infoFiltered:"(由 _MAX_ 项结果过滤)",infoPostFix:"",loadingRecords:"载入中...",zeroRecords:"无匹配结果",emptyTable:"无结果",paginate:{first:"第一页",previous:"上一页",next:"下一页",last:"最后一页"},aria:{sortAscending:"正序排列",sortDescending:"倒序排列"}},columnDefs:[{className:"star",targets:0,searchable:!1,orderable:!1}],deferLoading:100,drawCallback:function(){$('[data-toggle="tooltip"]').tooltip()}});e.on("click","tr",function(){$(this).hasClass("selected")?$(this).removeClass("selected"):(e.$("tr.selected").removeClass("selected"),$(this).addClass("selected"))}),e.on("draw.dt",function(){$.fn.articleData=function(){var e=this.parent().next().find("a"),t={id:e.data("id"),type:e.data("type")};return t};var t=function(t,i){$(i).on("click",function(t){t.preventDefault();var i=$(this),a=$(this).articleData(),o=function(t){t&&(i.removeClass("fa-star-o").addClass("fa-star"),e.ajax.reload(null,!1))};$.post("/api/collection/add/",a,o)})},i=function(t,i){$(i).on("click",function(t){t.preventDefault();var i=$(this),a=$(this).articleData(),o=function(t){t&&(i.removeClass("fa-star").addClass("fa-star-o"),e.ajax.reload(null,!1))};$.post("/api/collection/remove/",a,o)})};$(".fa-star-o").each(t),$(".fa-star").each(i)})},$(function(){$(".login-box").Do(app.user.login),$(".register-box").Do(app.user.register),$("#line-chart").Do(app.chart.line),$("#pie-chart").Do(app.chart.pie),$("#news").Do(app.table),$("#event").Do(app.table)});