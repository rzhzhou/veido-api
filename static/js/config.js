'use strict';

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
