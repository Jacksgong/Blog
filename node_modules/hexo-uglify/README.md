# hexo-uglify

Minify JavaScript files with [UglifyJS].

## Installation

``` bash
$ npm install hexo-uglify --save
```

## Options

``` yaml
uglify:
  mangle: true
  output:
  compress:
  exclude: 
    - *.min.js
```

- **mangle**: Mangle file names
- **output**: Output options
- **compress**: Compress options
- **exclude**: Exclude files

[UglifyJS]: http://lisperator.net/uglifyjs/