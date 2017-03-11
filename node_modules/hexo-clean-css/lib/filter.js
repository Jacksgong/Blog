var CleanCSS = require('clean-css');
var minimatch = require('minimatch');
var Promise = require('bluebird');

module.exports = function(str, data){
  var options = this.config.clean_css;
  var path = data.path;
  var exclude = options.exclude;
  if (exclude && !Array.isArray(exclude)) exclude = [exclude];

  if (path && exclude && exclude.length){
    for (var i = 0, len = exclude.length; i < len; i++){
      if (minimatch(path, exclude[i])) return str;
    }
  }

  return new Promise(function(resolve, reject){
    new CleanCSS(options).minify(str, function(err, result){
      if (err) return reject(err);
      resolve(result.styles);
    });
  });
};