var assign = require('object-assign');

hexo.config.clean_css = assign({
  exclude: ['*.min.css']
}, hexo.config.clean_css);

hexo.extend.filter.register('after_render:css', require('./lib/filter'));