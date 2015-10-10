'use strict';

App.route = function () {
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
};


//
// Initialization
//

$(function () {
  App.route();
});