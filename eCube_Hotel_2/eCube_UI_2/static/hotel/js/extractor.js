(function() {
  var fs, page, system,
    __slice = [].slice;

  system = require('system');

  fs = require('fs');

  page = require('webpage').create();

  page.viewportSize = {
    width: 1600,
    height: 4000
  };

  page.onResourceRequested = function(request) {
    system.stderr.write(JSON.stringify(request, void 0, 2));
    return system.stderr.write('\n\n');
  };

  page.onResourceReceived = function(response) {
    system.stderr.write(JSON.stringify(response, void 0, 2));
    return system.stderr.write('\n\n');
  };

  page.onConsoleMessage = function(message) {
    system.stderr.write(message);
    return system.stderr.write('\n\n');
  };

  page.onLoadFinished = function(status) {
    var data;
    fs.write(system.args[2] + '.html', page.content, 'w');
    if (status === !'success') {
      return phantom.exit();
    }
    page.evaluate(function() {
      String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g, '');
      };
      (function(window) {
        'use strict';
        var namespace;
        window.__slice = [].slice;
        namespace = function(target, name, block) {
          var item, top, _i, _len, _ref, _ref1;
          if (arguments.length < 3) {
            _ref = [window].concat(__slice.call(arguments)), target = _ref[0], name = _ref[1], block = _ref[2];
          }
          top = target;
          _ref1 = name.split('.');
          for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
            item = _ref1[_i];
            target = target[item] || (target[item] = {});
          }
          return block(target, top);
        };
        return namespace('spider', function(exports, top) {
          return exports.namespace = namespace;
        });
      })(window);
      return spider.namespace('spider.utils', function(exports) {
        'use strict';
        exports.is_valid = function(value) {
          var re;
          re = /^[a-zA-Z][a-zA-Z0-9\-_]+$/;
          return value && re.test(value);
        };
        exports.element = function(element, is_name_only) {
          var c, classes, data, name, _i, _len, _ref;
          name = element.tagName.toLowerCase();
          if (is_name_only) {
            return name;
          }
          classes = [];
          _ref = element.classList;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            c = _ref[_i];
            if (exports.is_valid(c)) {
              classes.push(c);
            }
          }
          data = {
            name: name,
            id: exports.is_valid(element.id) ? element.id : '',
            classes: classes.sort()
          };
          return data;
        };
        exports.path = function(element, is_name_only) {
          var path;
          path = [];
          while (element) {
            if (element === document.body) {
              break;
            }
            path.splice(0, 0, exports.element(element, is_name_only));
            element = element.parentElement;
          }
          return path;
        };
        exports.bound = function(element) {
          var bound, rect, scrollLeft, scrollTop;
          scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
          scrollLeft = document.documentElement.scrollLeft || document.body.scrollLeft;
          rect = element.getBoundingClientRect();
          bound = {
            width: rect.width,
            height: rect.height,
            left: rect.left + scrollLeft,
            top: rect.top + scrollTop
          };
          return bound;
        };
        return exports.computed = function(element) {
          var computed, data, defaults, key, _i, _len;
          defaults = document.defaultView.getComputedStyle(document.body);
          computed = document.defaultView.getComputedStyle(element);
          data = {};
          for (_i = 0, _len = computed.length; _i < _len; _i++) {
            key = computed[_i];
            if (key === 'width' || key === 'height' || key === 'top' || key === 'left' || key === 'right' || key === 'bottom') {
              continue;
            }
            if (key.charAt(0) === '-') {
              continue;
            }
            if (computed[key] === defaults[key]) {
              continue;
            }
            data[key] = computed[key];
          }
          return data;
        };
      });
    });
    data = page.evaluate(function() {
      var computed, descriptions, key, meta, title, titles, _i, _len, _ref;
      titles = (function() {
        var _i, _len, _ref, _results;
        _ref = document.querySelectorAll('title');
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          title = _ref[_i];
          _results.push(title.innerText);
        }
        return _results;
      })();
      descriptions = (function() {
        var _i, _len, _ref, _results;
        _ref = document.querySelectorAll('meta[name="description"]');
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          meta = _ref[_i];
          _results.push(meta.content);
        }
        return _results;
      })();
      titles.push.apply(titles, (function() {
        var _i, _len, _ref, _results;
        _ref = document.querySelectorAll('meta[name="og:title"], meta[property="og:title"]');
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          meta = _ref[_i];
          _results.push(meta.content);
        }
        return _results;
      })());
      descriptions.push.apply(descriptions, (function() {
        var _i, _len, _ref, _results;
        _ref = document.querySelectorAll('meta[name="og:description"], meta[property="og:description"]');
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          meta = _ref[_i];
          _results.push(meta.content);
        }
        return _results;
      })());
      titles.push.apply(titles, (function() {
        var _i, _len, _ref, _results;
        _ref = document.querySelectorAll('meta[name="twitter:title"], meta[property="twitter:title"]');
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          meta = _ref[_i];
          _results.push(meta.content);
        }
        return _results;
      })());
      descriptions.push.apply(descriptions, (function() {
        var _i, _len, _ref, _results;
        _ref = document.querySelectorAll('meta[name="twitter:description"], meta[property="twitter:description"]');
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          meta = _ref[_i];
          _results.push(meta.content);
        }
        return _results;
      })());
      computed = {};
      _ref = document.defaultView.getComputedStyle(document.body);
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        key = _ref[_i];
        if (key.charAt(0) === '-') {
          continue;
        }
        computed[key] = document.defaultView.getComputedStyle(document.body)[key];
      }
      data = {
        url: window.location.href,
        titles: titles,
        descriptions: descriptions,
        body: {
          scroll: {
            top: document.documentElement.scrollTop || document.body.scrollTop,
            left: document.documentElement.scrollLeft || document.body.scrollLeft
          },
          bound: spider.utils.bound(document.body),
          computed: computed
        }
      };
      return data;
    });
    data.links = page.evaluate(function() {
      var link, _i, _len, _ref, _results;
      _ref = document.querySelectorAll('a[href]');
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        link = _ref[_i];
        _results.push(link.href);
      }
      return _results;
    });
    data.texts = page.evaluate(function() {
      var bound, computed, node, text, texts, walker;
      texts = [];
      walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
      while (text = walker.nextNode()) {
        if (!(text.nodeValue.trim().length > 0)) {
          continue;
        }
        node = text.parentElement;
        bound = spider.utils.bound(node);
        if (!(bound.width * bound.height > 0)) {
          continue;
        }
        while (node) {
          computed = document.defaultView.getComputedStyle(node);
          if (parseInt(computed.width) * parseInt(computed.height) > 0) {
            break;
          }
          node = node.parentElement;
        }
        if (!node) {
          continue;
        }
        if (node.spider) {
          node.spider.text.push(text.nodeValue);
          continue;
        }
        node.spider = {
          element: spider.utils.element(node),
          path: spider.utils.path(node, true),
          selector: spider.utils.path(node),
          text: [text.nodeValue],
          html: node.innerHTML,
          bound: spider.utils.bound(node),
          computed: spider.utils.computed(node)
        };
        texts.push(node.spider);
        node.style.border = '1px solid red';
      }
      return texts;
    });
    data.images = page.evaluate(function() {
      var bound, images, node, _i, _len, _ref;
      images = [];
      _ref = document.querySelectorAll('img[src]');
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        node = _ref[_i];
        bound = spider.utils.bound(node);
        if (!(bound.width * bound.height > 0)) {
          continue;
        }
        images.push({
          src: node.src,
          element: spider.utils.element(node),
          path: spider.utils.path(node, true),
          selector: spider.utils.path(node),
          bound: bound,
          computed: spider.utils.computed(node)
        });
      }
      return images;
    });
    fs.write(system.args[2] + '.json', JSON.stringify(data, void 0, 2));
    page.render(system.args[2] + '.png');
    return phantom.exit();
  };

  if (system.args.length !== 3) {
    system.stderr.write('Usage: phantomjs ' + system.args[0] + ' <url> <label>\n\n');
    phantom.exit();
  }

  page.open(system.args[1]);

}).call(this);