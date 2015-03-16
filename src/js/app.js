$.fn.Do = function(func) {
  this.length && func.apply(this);
  return this;
}

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

$(function() {
  $('#news').Do(myTable);
  $('#event').Do(myTable);  
});