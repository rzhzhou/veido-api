function _init(){$.AdminLTE.layout={activate:function(){var e=this;e.fix(),e.fixSidebar(),$(window,".wrapper").resize(function(){e.fix(),e.fixSidebar()})},fix:function(){var e=$(".main-header").outerHeight()+$(".main-footer").outerHeight(),t=$(window).height(),a=$(".sidebar").height();$("body").hasClass("fixed")?$(".content-wrapper, .right-side").css("min-height",t-$(".main-footer").outerHeight()):t>=a?$(".content-wrapper, .right-side").css("min-height",t-e):$(".content-wrapper, .right-side").css("min-height",a)},fixSidebar:function(){return $("body").hasClass("fixed")?("undefined"==typeof $.fn.slimScroll&&console&&console.error("Error: the fixed layout requires the slimscroll plugin!"),void($.AdminLTE.options.sidebarSlimScroll&&"undefined"!=typeof $.fn.slimScroll&&($(".sidebar").slimScroll({destroy:!0}).height("auto"),$(".sidebar").slimscroll({height:$(window).height()-$(".main-header").height()+"px",color:"rgba(0,0,0,0.2)",size:"3px"})))):void("undefined"!=typeof $.fn.slimScroll&&$(".sidebar").slimScroll({destroy:!0}).height("auto"))}},$.AdminLTE.pushMenu=function(e){var t=this.options.screenSizes;$(e).click(function(e){e.preventDefault(),$(window).width()>t.sm-1?$("body").toggleClass("sidebar-collapse"):$("body").hasClass("sidebar-open")?($("body").removeClass("sidebar-open"),$("body").removeClass("sidebar-collapse")):$("body").addClass("sidebar-open")}),$(".content-wrapper").click(function(){$(window).width()<=t.sm-1&&$("body").hasClass("sidebar-open")&&$("body").removeClass("sidebar-open")})},$.AdminLTE.tree=function(e){var t=this;$("li a",$(e)).click(function(e){var a=$(this),i=a.next();if(i.is(".treeview-menu")&&i.is(":visible"))i.slideUp("normal",function(){i.removeClass("menu-open")}),i.parent("li").removeClass("active");else if(i.is(".treeview-menu")&&!i.is(":visible")){var s=a.parents("ul").first(),n=s.find("ul:visible").slideUp("normal");n.removeClass("menu-open");var o=a.parent("li");i.slideDown("normal",function(){i.addClass("menu-open"),s.find("li.active").removeClass("active"),o.addClass("active"),t.layout.fix()})}i.is(".treeview-menu")&&e.preventDefault()})},$.AdminLTE.boxWidget={activate:function(){var e=$.AdminLTE.options,t=this;$(e.boxWidgetOptions.boxWidgetSelectors.collapse).click(function(e){e.preventDefault(),t.collapse($(this))}),$(e.boxWidgetOptions.boxWidgetSelectors.remove).click(function(e){e.preventDefault(),t.remove($(this))})},collapse:function(e){var t=e.parents(".box").first(),a=t.find(".box-body, .box-footer");t.hasClass("collapsed-box")?(e.children(".fa-plus").removeClass("fa-plus").addClass("fa-minus"),a.slideDown(300,function(){t.removeClass("collapsed-box")})):(e.children(".fa-minus").removeClass("fa-minus").addClass("fa-plus"),a.slideUp(300,function(){t.addClass("collapsed-box")}))},remove:function(e){var t=e.parents(".box").first();t.slideUp()},options:$.AdminLTE.options.boxWidgetOptions}}if(function(e){e.fn.extend({slimScroll:function(a){var i={width:"auto",height:"250px",size:"7px",color:"#000",position:"right",distance:"1px",start:"top",opacity:.4,alwaysVisible:!1,disableFadeOut:!1,railVisible:!1,railColor:"#333",railOpacity:.2,railDraggable:!0,railClass:"slimScrollRail",barClass:"slimScrollBar",wrapperClass:"slimScrollDiv",allowPageScroll:!1,wheelStep:20,touchScrollStep:200,borderRadius:"7px",railBorderRadius:"7px"},s=e.extend(i,a);return this.each(function(){function i(t){if(d){var t=t||window.event,a=0;t.wheelDelta&&(a=-t.wheelDelta/120),t.detail&&(a=t.detail/3);var i=t.target||t.srcTarget||t.srcElement;e(i).closest("."+s.wrapperClass).is($.parent())&&n(a,!0),t.preventDefault&&!x&&t.preventDefault(),x||(t.returnValue=!1)}}function n(e,t,a){x=!1;var i=e,n=$.outerHeight()-D.outerHeight();if(t&&(i=parseInt(D.css("top"))+e*parseInt(s.wheelStep)/100*D.outerHeight(),i=Math.min(Math.max(i,0),n),i=e>0?Math.ceil(i):Math.floor(i),D.css({top:i+"px"})),m=parseInt(D.css("top"))/($.outerHeight()-D.outerHeight()),i=m*($[0].scrollHeight-$.outerHeight()),a){i=e;var o=i/$[0].scrollHeight*$.outerHeight();o=Math.min(Math.max(o,0),n),D.css({top:o+"px"})}$.scrollTop(i),$.trigger("slimscrolling",~~i),l(),c()}function o(){window.addEventListener?(this.addEventListener("DOMMouseScroll",i,!1),this.addEventListener("mousewheel",i,!1)):document.attachEvent("onmousewheel",i)}function r(){g=Math.max($.outerHeight()/$[0].scrollHeight*$.outerHeight(),w),D.css({height:g+"px"});var e=g==$.outerHeight()?"none":"block";D.css({display:e})}function l(){if(r(),clearTimeout(h),m==~~m){if(x=s.allowPageScroll,v!=m){var e=0==~~m?"top":"bottom";$.trigger("slimscroll",e)}}else x=!1;return v=m,g>=$.outerHeight()?void(x=!0):(D.stop(!0,!0).fadeIn("fast"),void(s.railVisible&&T.stop(!0,!0).fadeIn("fast")))}function c(){s.alwaysVisible||(h=setTimeout(function(){s.disableFadeOut&&d||p||u||(D.fadeOut("slow"),T.fadeOut("slow"))},1e3))}var d,p,u,h,f,g,m,v,b="<div></div>",w=30,x=!1,$=e(this);if($.parent().hasClass(s.wrapperClass)){var C=$.scrollTop();if(D=$.parent().find("."+s.barClass),T=$.parent().find("."+s.railClass),r(),e.isPlainObject(a)){if("height"in a&&"auto"==a.height){$.parent().css("height","auto"),$.css("height","auto");var y=$.parent().parent().height();$.parent().css("height",y),$.css("height",y)}if("scrollTo"in a)C=parseInt(s.scrollTo);else if("scrollBy"in a)C+=parseInt(s.scrollBy);else if("destroy"in a)return D.remove(),T.remove(),void $.unwrap();n(C,!1,!0)}}else if(!(e.isPlainObject(a)&&"destroy"in a)){s.height="auto"==s.height?$.parent().height():s.height;var S=e(b).addClass(s.wrapperClass).css({position:"relative",overflow:"hidden",width:s.width,height:s.height});$.css({overflow:"hidden",width:s.width,height:s.height,"-ms-touch-action":"none"});var T=e(b).addClass(s.railClass).css({width:s.size,height:"100%",position:"absolute",top:0,display:s.alwaysVisible&&s.railVisible?"block":"none","border-radius":s.railBorderRadius,background:s.railColor,opacity:s.railOpacity,zIndex:90}),D=e(b).addClass(s.barClass).css({background:s.color,width:s.size,position:"absolute",top:0,opacity:s.opacity,display:s.alwaysVisible?"block":"none","border-radius":s.borderRadius,BorderRadius:s.borderRadius,MozBorderRadius:s.borderRadius,WebkitBorderRadius:s.borderRadius,zIndex:99}),k="right"==s.position?{right:s.distance}:{left:s.distance};T.css(k),D.css(k),$.wrap(S),$.parent().append(D),$.parent().append(T),s.railDraggable&&D.bind("mousedown",function(a){var i=e(document);return u=!0,t=parseFloat(D.css("top")),pageY=a.pageY,i.bind("mousemove.slimscroll",function(e){currTop=t+e.pageY-pageY,D.css("top",currTop),n(0,D.position().top,!1)}),i.bind("mouseup.slimscroll",function(e){u=!1,c(),i.unbind(".slimscroll")}),!1}).bind("selectstart.slimscroll",function(e){return e.stopPropagation(),e.preventDefault(),!1}),T.hover(function(){l()},function(){c()}),D.hover(function(){p=!0},function(){p=!1}),$.hover(function(){d=!0,l(),c()},function(){d=!1,c()}),window.navigator.msPointerEnabled?($.bind("MSPointerDown",function(e,t){e.originalEvent.targetTouches.length&&(f=e.originalEvent.targetTouches[0].pageY)}),$.bind("MSPointerMove",function(e){if(e.originalEvent.preventDefault(),e.originalEvent.targetTouches.length){var t=(f-e.originalEvent.targetTouches[0].pageY)/s.touchScrollStep;n(t,!0),f=e.originalEvent.targetTouches[0].pageY}})):($.bind("touchstart",function(e,t){e.originalEvent.touches.length&&(f=e.originalEvent.touches[0].pageY)}),$.bind("touchmove",function(e){if(x||e.originalEvent.preventDefault(),e.originalEvent.touches.length){var t=(f-e.originalEvent.touches[0].pageY)/s.touchScrollStep;n(t,!0),f=e.originalEvent.touches[0].pageY}})),r(),"bottom"===s.start?(D.css({top:$.outerHeight()-D.outerHeight()}),n(0,!0)):"top"!==s.start&&(n(e(s.start).position().top,null,!0),s.alwaysVisible||D.hide()),o()}}),this}}),e.fn.extend({slimscroll:e.fn.slimScroll})}(jQuery),"undefined"==typeof jQuery)throw new Error("AdminLTE requires jQuery");$.AdminLTE={},$.AdminLTE.options={navbarMenuSlimscroll:!0,navbarMenuSlimscrollWidth:"3px",navbarMenuHeight:"200px",sidebarToggleSelector:"[data-toggle='offcanvas']",sidebarPushMenu:!0,sidebarSlimScroll:!0,enableBoxRefresh:!0,enableBSToppltip:!0,BSTooltipSelector:"[data-toggle='tooltip']",enableFastclick:!0,enableBoxWidget:!0,boxWidgetOptions:{boxWidgetIcons:{collapse:"fa fa-minus",open:"fa fa-plus",remove:"fa fa-times"},boxWidgetSelectors:{remove:'[data-widget="remove"]',collapse:'[data-widget="collapse"]'}},directChat:{enable:!0,contactToggleSelector:'[data-widget="chat-pane-toggle"]'},colors:{lightBlue:"#3c8dbc",red:"#f56954",green:"#00a65a",aqua:"#00c0ef",yellow:"#f39c12",blue:"#0073b7",navy:"#001F3F",teal:"#39CCCC",olive:"#3D9970",lime:"#01FF70",orange:"#FF851B",fuchsia:"#F012BE",purple:"#8E24AA",maroon:"#D81B60",black:"#222222",gray:"#d2d6de"},screenSizes:{xs:480,sm:768,md:992,lg:1200}},$(function(){var e=$.AdminLTE.options;_init(),$.AdminLTE.layout.activate(),$.AdminLTE.tree(".sidebar"),e.navbarMenuSlimscroll&&"undefined"!=typeof $.fn.slimscroll&&$(".navbar .menu").slimscroll({height:"200px",alwaysVisible:!1,size:"3px"}).css("width","100%"),e.sidebarPushMenu&&$.AdminLTE.pushMenu(e.sidebarToggleSelector),e.enableBSToppltip&&$(e.BSTooltipSelector).tooltip(),e.enableBoxWidget&&$.AdminLTE.boxWidget.activate(),e.enableFastclick&&"undefined"!=typeof FastClick&&FastClick.attach(document.body),e.directChat.enable&&$(e.directChat.contactToggleSelector).click(function(){var e=$(this).parents(".direct-chat").first();e.toggleClass("direct-chat-contacts-open")}),$('.btn-group[data-toggle="btn-toggle"]').each(function(){var e=$(this);$(this).find(".btn").click(function(t){e.find(".btn.active").removeClass("active"),$(this).addClass("active"),t.preventDefault()})})}),function(e){e.fn.boxRefresh=function(t){function a(e){e.append(n),s.onLoadStart.call(e)}function i(e){e.find(n).remove(),s.onLoadDone.call(e)}var s=e.extend({trigger:".refresh-btn",source:"",onLoadStart:function(e){},onLoadDone:function(e){}},t),n=e('<div class="overlay"><div class="fa fa-refresh fa-spin"></div></div>');return this.each(function(){if(""===s.source)return void(console&&console.log("Please specify a source first - boxRefresh()"));var t=e(this),n=t.find(s.trigger).first();n.click(function(e){e.preventDefault(),a(t),t.find(".box-body").load(s.source,function(){i(t)})})})}}(jQuery),function(e){e.fn.todolist=function(t){var a=e.extend({onCheck:function(e){},onUncheck:function(e){}},t);return this.each(function(){"undefined"!=typeof e.fn.iCheck?(e("input",this).on("ifChecked",function(t){var i=e(this).parents("li").first();i.toggleClass("done"),a.onCheck.call(i)}),e("input",this).on("ifUnchecked",function(t){var i=e(this).parents("li").first();i.toggleClass("done"),a.onUncheck.call(i)})):e("input",this).on("change",function(t){var i=e(this).parents("li").first();i.toggleClass("done"),a.onCheck.call(i)})})}}(jQuery),function(e,t){e.fn.bootpag=function(t){function a(t,a){a=parseInt(a,10);var o,r=0==n.maxVisible?1:n.maxVisible,l=1==n.maxVisible?0:1,c=Math.floor((a-1)/r)*r,d=t.find("li");n.page=a=0>a?0:a>n.total?n.total:a,d.removeClass(n.activeClass),o=1>a-1?1:n.leaps&&a-1>=n.maxVisible?Math.floor((a-1)/r)*r:a-1,n.firstLastUse&&d.first().toggleClass(n.disabledClass,1===a);var p=d.first();n.firstLastUse&&(p=p.next()),p.toggleClass(n.disabledClass,1===a).attr("data-lp",o).find("a").attr("href",i(o));var l=1==n.maxVisible?0:1;o=a+1>n.total?n.total:n.leaps&&a+1<n.total-n.maxVisible?c+n.maxVisible+l:a+1;var u=d.last();n.firstLastUse&&(u=u.prev()),u.toggleClass(n.disabledClass,a===n.total).attr("data-lp",o).find("a").attr("href",i(o)),d.last().toggleClass(n.disabledClass,a===n.total);var h=d.filter("[data-lp="+a+"]"),f="."+[n.nextClass,n.prevClass,n.firstClass,n.lastClass].join(",.");if(!h.not(f).length){var g=c>=a?-n.maxVisible:0;d.not(f).each(function(t){o=t+1+c+g,e(this).attr("data-lp",o).toggle(o<=n.total).find("a").html(o).attr("href",i(o))}),h=d.filter("[data-lp="+a+"]")}h.not(f).addClass(n.activeClass),s.data("settings",n)}function i(e){return n.href.replace(n.hrefVariable,e)}var s=this,n=e.extend({total:0,page:1,maxVisible:null,leaps:!0,href:"javascript:void(0);",hrefVariable:"{{number}}",next:"&raquo;",prev:"&laquo;",firstLastUse:!1,first:'<span aria-hidden="true">&larr;</span>',last:'<span aria-hidden="true">&rarr;</span>',wrapClass:"pagination",activeClass:"active",disabledClass:"disabled",nextClass:"next",prevClass:"prev",lastClass:"last",firstClass:"first"},s.data("settings")||{},t||{});return n.total<=0?this:(e.isNumeric(n.maxVisible)||n.maxVisible||(n.maxVisible=parseInt(n.total,10)),s.data("settings",n),this.each(function(){var t,o,r=e(this),l=['<ul class="',n.wrapClass,' bootpag">'];n.firstLastUse&&(l=l.concat(['<li data-lp="1" class="',n.firstClass,'"><a href="',i(1),'">',n.first,"</a></li>"])),n.prev&&(l=l.concat(['<li data-lp="1" class="',n.prevClass,'"><a href="',i(1),'">',n.prev,"</a></li>"]));for(var c=1;c<=Math.min(n.total,n.maxVisible);c++)l=l.concat(['<li data-lp="',c,'"><a href="',i(c),'">',c,"</a></li>"]);n.next&&(o=n.leaps&&n.total>n.maxVisible?Math.min(n.maxVisible+1,n.total):2,l=l.concat(['<li data-lp="',o,'" class="',n.nextClass,'"><a href="',i(o),'">',n.next,"</a></li>"])),n.firstLastUse&&(l=l.concat(['<li data-lp="',n.total,'" class="last"><a href="',i(n.total),'">',n.last,"</a></li>"])),l.push("</ul>"),r.find("ul.bootpag").remove(),r.append(l.join("")),t=r.find("ul.bootpag"),r.find("li").click(function(){var t=e(this);if(!t.hasClass(n.disabledClass)&&!t.hasClass(n.activeClass)){var i=parseInt(t.attr("data-lp"),10);s.find("ul.bootpag").each(function(){a(e(this),i)}),s.trigger("page",i)}}),a(t,n.page)}))}}(jQuery,window),require.config({paths:{echarts:"/vendor/echarts"}}),$.fn.Do=function(e){return this.length&&e.apply(this),this},$.fn.Trim=function(){var e=this.find("input").val(),t=$.trim(e);return t};var app={};app.url=location.pathname,app.user={login:function(){var e=this.find("form"),t=this.find("p");e.submit(function(e){e.preventDefault();var a={username:$("#username").Trim(),password:$("#password").Trim()},i=function(e){e.status?location.href=location.search.length?location.search.substr(1).split("=")[1]:"/":t.text("用户名或密码错误！")};a.username.length&&a.password.length?$.post("/api/login/",a,i,"json"):t.text("请输入用户名和密码！")})},change:function(){var e=this.find("form"),t=this.find("p");e.submit(function(e){e.preventDefault();var a={username:$("#username").Trim(),oldPassword:$("#old-password").Trim(),newPassword:$("#new-password").Trim(),retype:$("#retype-password").Trim()},i=function(e){e.status?(t.text("更新成功！").show(),location.href="/login/"):t.text("原密码错误！").show()};switch(0){case a.username.length:t.text("请输入姓名！").show();break;case a.oldPassword.length:t.text("请输入原密码！").show();break;case a.newPassword.length:t.text("请输入新密码！").show();break;case a.retype.length:t.text("请确认密码！").show();break;case Number(a.newPassword===a.retype):t.text("两次输入密码不一致！").show();break;default:var s={username:a.username,oldPassword:a.oldPassword,newPassword:a.newPassword};$.post("/api/settings/change/",s,i,"json")}})},management:function(){var e=this,t=e.find("button"),a=t.eq(0),i=t.eq(1),s=[],n=function(t,a){t.click(function(){s.length=0,e.find("input:checked").each(function(e,t){var a=$(t).parent().next().data("id");s.push(a)});var t=function(e){e.status&&(location.href="/user/")};s.length&&$.post(a,{id:s.toString()},t,"json")})};n(a,"/api/user/reset/"),n(i,"/api/user/remove/")},add:function(){var e=this.find("form"),t=this.find("p");e.submit(function(e){e.preventDefault();var a={username:$("#username").Trim(),password:$("#password").Trim(),retype:$("#retype-password").Trim()},i=function(e){e.status?location.href="/user/":t.text("抱歉，注册失败！").show()};switch(0){case a.username.length:t.text("请输入用户名！").show();break;case a.password.length:t.text("请输入密码!").show();break;case a.retype.length:t.text("请确认密码！").show();break;case Number(a.password===a.retype):t.text("两次输入密码不一致！").show();break;default:var s={username:a.username,password:a.password};$.post("/api/user/add/",s,i,"json")}})}},app.search=function(){this.submit(function(e){e.preventDefault();var t=$(this).Trim();t.length&&(location.href="/search/"+t+"/")})},app.menu=function(){var e=$(this).find("a").filter(function(){return this.href===location.href});e.parent().addClass("active"),e.closest(".treeview-menu").addClass("menu-open"),e.closest(".treeview").addClass("active")},app.chart={line:function(){require(["echarts","echarts/chart/line"],function(e){$.getJSON("/api/line"+app.url,function(t){e.init(document.getElementById("line-chart"),"macarons").setOption({tooltip:{trigger:"axis"},legend:{data:["正面","中性","负面"]},grid:{x:40,y:30,x2:25,y2:30},xAxis:[{type:"category",boundaryGap:!1,data:t.date}],yAxis:[{type:"value"}],series:[{name:"正面",type:"line",data:t.positive},{name:"中性",type:"line",data:t.neutral},{name:"负面",type:"line",data:t.negative}]})})})},pie:function(){require(["echarts","echarts/chart/pie"],function(e){$.getJSON("/api/pie"+app.url,function(t){e.init(document.getElementById("pie-chart"),"macarons").setOption({tooltip:{trigger:"item",formatter:"{a} <br/>{b} : {c} ({d}%)"},legend:{data:t.name},series:[{name:"信息比例",type:"pie",radius:"55%",center:["50%","60%"],data:t.value}]})})})}},app.table=function(){$.fn.dataTable.ext.errMode="throw";var e=this.DataTable({ajax:{url:"/api"+location.pathname,dataSrc:this[0].id,cache:!0},autoWidth:!1,pageLength:25,order:[],language:{processing:"处理中...",search:"",searchPlaceholder:"输入关键字过滤...",lengthMenu:"显示 _MENU_ 条",info:"显示第 _START_ 至 _END_ 条，共 _TOTAL_ 条",infoEmpty:"信息空",infoFiltered:"(由 _MAX_ 项结果过滤)",infoPostFix:"",loadingRecords:"载入中...",zeroRecords:"无匹配结果",emptyTable:"无结果",paginate:{first:"第一页",previous:"上一页",next:"下一页",last:"最后一页"},aria:{sortAscending:"正序排列",sortDescending:"倒序排列"}},columnDefs:[{className:"star",targets:0,searchable:!1,orderable:!1},{className:"index",targets:-1}],deferLoading:100,drawCallback:function(){$('[data-toggle="tooltip"]').tooltip()}});e.on("click","tr",function(){$(this).hasClass("selected")?$(this).removeClass("selected"):(e.$("tr.selected").removeClass("selected"),$(this).addClass("selected"))}),e.on("draw.dt",function(){var t=function(t,a){t.each(function(t,i){$(i).click(function(t){t.preventDefault();var i=$(this),s=i.parent().next().find("a"),n={id:s.data("id"),type:s.data("type")},o=function(t){t&&(i.toggleClass("fa-star-o"),i.toggleClass("fa-star"),e.ajax.reload(null,!1))};$.post(a,n,o)})})};t($(".fa-star-o"),"/api/collection/add/"),t($(".fa-star"),"/api/collection/remove/")})},app.media=function(){var e=this;$(".media-list").each(function(t,a){var i=$(a),s=i.parent().next(),n=s.data("total"),o=s.data("type");s.bootpag({total:n,maxVisible:5,leaps:!0,firstLastUse:!0,first:"←",last:"→",wrapClass:"pagination pagination-sm no-margin pull-right"}).on("page",function(t,a){var s="/api"+e.url+o+"/"+a+"/";$.getJSON(s,function(e){i.html(e)})})})},$(function(){switch(app.url){case"/login/":$(".login-box").Do(app.user.login);break;case"/weixin/":$(".sidebar-form").Do(app.search),$(".sidebar-menu").Do(app.menu),app.media();break;case"/settings/":$(".sidebar-form").Do(app.search),$(".sidebar-menu").Do(app.menu),$(".user-info").Do(app.user.change);break;case"/user/":$(".sidebar-form").Do(app.search),$(".sidebar-menu").Do(app.menu),$(".user-management").Do(app.user.management),$(".user-add").Do(app.user.add);break;default:$(".sidebar-form").Do(app.search),$(".sidebar-menu").Do(app.menu),$("#line-chart").Do(app.chart.line),$("#pie-chart").Do(app.chart.pie),$("#news").Do(app.table),$("#event").Do(app.table),$("#inspection").Do(app.table)}});