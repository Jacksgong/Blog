var assign = require('object-assign');

hexo.config.uglify = assign({
  mangle: true,
  output: {},
  compress: {},
  exclude: ['*.min.js']
}, hexo.config.uglify);

hexo.extend.filter.register('after_render:js', require('./lib/filter'));