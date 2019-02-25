# -*- coding: utf-8 -*-
#
# Tencent is pleased to support the open source community by making QTA available.
# Copyright (C) 2016THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the BSD 3-Clause License (the "License"); you may not use this
# file except in compliance with the License. You may obtain a copy of the License at
#
# https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
#
'''IWebDriver接口
'''


from qt4w.util import logger, general_encode, unicode_decode, ControlNotFoundError
import six

class IWebDriver(object):
    '''IWebDriver接口
    '''
    def __init__(self, webview):
        '''构造函数
        
        :param webview: 对应的WebView实例
        :type webview:  object
        '''
        raise NotImplementedError
    
    @property
    def ready_state(self):
        '''页面状态
        '''
        raise NotImplementedError
    
    def eval_script(self, frame_xpaths, script):
        '''在指定frame中执行JavaScript，并返回执行结果
        
        :param frame_xpaths: frame元素的XPATH路径，如果是顶层页面，怎传入“[]”
        :type frame_xpaths:  list
        :param script:       要执行的JavaScript语句
        :type script:        string
        '''
        raise NotImplementedError
    
    def get_attribute(self, elem_xpaths, attr_name):
        '''获取元素属性
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param attr_name:   属性名
        :type attr_name:    string
        '''
        raise NotImplementedError
    
    def set_attribute(self, elem_xpaths, attr_name, value):
        '''设置元素属性
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param attr_name:   属性名
        :type attr_name:    string
        :param value:       新的值
        :type value:        string
        '''
        raise NotImplementedError
        
    def get_elem_rect(self, elem_xpaths, rav=True):
        '''获取元素在页面中的坐标
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param rav:         是否是相对于当前frame
        :type rav:          bool
        '''
        raise NotImplementedError
    
    def get_property(self, elem_xpaths, prop_name):
        '''获取元素的特定值，例如：node.innerHTML
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param prop_name:   property名
        :type prop_name:    string
        '''
        raise NotImplementedError
    
    def set_property(self, elem_xpaths, prop_name, value):
        '''设置元素的特定值，例如：node.innerHTML
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param prop_name:   property名
        :type prop_name:    string
        :param value:       新的值
        :type value:        string
        '''
        raise NotImplementedError
    
    def get_style(self, elem_xpaths, style_name):
        '''获取元素的某一样式值
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param style_name:  样式名称
        :type style_name:   string
        '''
        raise NotImplementedError
    
    def highlight(self, elem_xpaths):
        '''使元素高亮
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        '''
        raise NotImplementedError

class WebDriverBase(IWebDriver):
    '''WebDriver基类
    '''
    driver_script = r'''
    window['qt4w_driver_lib'] = {
    getScale : function(){
        return 1;
    },
    
    getScreenSize: function(){
        var result = new Array();
        result.push(screen.availWidth);
        result.push(screen.availHeight);
        return result.toString();
    },
    
    selectNodes : function(xpath){
        var oResult = document.evaluate(xpath, document, null, XPathResult.ANY_TYPE, null);
        var aNodes = new Array();  
        if (oResult != null) {  
            var oElement = oResult.iterateNext();  
            while (oElement) {  
                aNodes.push(oElement);  
                oElement = oResult.iterateNext();  
            }  
        }
        return aNodes;
    },
    
    selectNode : function(xpath){
        var nodes = this.selectNodes(xpath);
        if(nodes.length == 0) throw new Error('Find element '+xpath+' failed');
        else if(nodes.length > 1) throw new Error('Find '+nodes.length+' elements match '+xpath);
        return nodes[0];
    },
    
    getElementZoom: function(node){
        var scale = 1;
        while(node != null && node != document.documentElement){
            var zoom = parseFloat(window.getComputedStyle(node, null).zoom);
            if(zoom != 1){
                scale *= zoom;
            }
            node = node.parentNode;
        }
        return scale;
    },
    
    getElemRect: function(xpath){
        var node = this.selectNode(xpath);
        var result = new Array();
        var rect = node.getBoundingClientRect();
        var scale = this.getScale();
        scale *= this.getElementZoom(node);
        var left = rect.left - document.body.scrollLeft;
        var top = rect.top - document.body.scrollTop;
        result.push(left * scale);
        result.push(top * scale);
        result.push(rect.width * scale);
        result.push(rect.height * scale);
        return result.toString();
    },
    
    initHighlightDiv: function(){
        this.bd0 = document.createElement("div");
        this.bd1 = document.createElement("div");
        this.bd2 = document.createElement("div");
        this.bd3 = document.createElement("div");
    },
    
    showDiv: function(cnt){
        if(cnt % 2 != 0){
            document.body.appendChild(this.bd0);
            document.body.appendChild(this.bd1);
            document.body.appendChild(this.bd2);
            document.body.appendChild(this.bd3);
        } else {
            document.body.removeChild(this.bd0);
            document.body.removeChild(this.bd1);
            document.body.removeChild(this.bd2);
            document.body.removeChild(this.bd3);
        }
        if (cnt){
            cnt--;
            if(window.console) console.log('show' + cnt);
            setTimeout("qt4w_driver_lib.showDiv(" + cnt + ")", 100);
        }
    },
    
    highlight: function(node){
        var rect = node.getBoundingClientRect();
        var left= rect.left;
        var top = rect.top;
        var width = node.offsetWidth;
        var height = node.offsetHeight;
        if(window.console) console.log(left+','+top+','+width+','+height);
        
        this.bd0.setAttribute("style", "border:solid 1px red;"
            + "left:" + (left) + "px;top:" + (top) + "px;z-index:32767;"
            + "width:" + (width) + "px;height:0px;position:fixed;");
        this.bd1.setAttribute("style", "border:solid 1px red;"
            + "left:" + (left) + "px;top:" + (top) + "px;z-index:32767;"
            + "width:0px;height:" + (height) + "px;position:fixed;");
        this.bd2.setAttribute("style", "border:solid 1px red;"
            + "left:" + (left+width) + "px;top:" + (top) + "px;z-index:32767;"
            + "width:0px;height:" + (height) + "px;position:fixed;");
        this.bd3.setAttribute("style", "border:solid 1px red;"
            + "left:" + (left) + "px;top:" + (top+height) + "px;z-index:32767;"
            + "width:" + (width) + "px;height:0px;position:fixed;");
        //console.log('style'+this.bd0.getAttribute('style')+'');
        this.showDiv(3);
    },
    
    scrollToVisible: function(node){
        if(node.scrollIntoViewIfNeeded){
            node.scrollIntoViewIfNeeded();
        }else if(node.scrollIntoView){
            node.scrollIntoView();
        }
    },
    
    logData: [],
    
    hookConsoleLog: function(){
        var self = this;
        if(window.console && window.JSON){
            var hookConsoleFunc = function(){
                var timeStr = new Date().toLocaleString();
                for(var i=1;i<arguments.length;i++){
                    var data = arguments[i];
                    if(data instanceof Array){
                        data = JSON.stringify(data);
                    }else if(data instanceof Object){
                        var jsonData = {};
                        for(var key in data){
                            jsonData[key] = data[key];
                            if(jsonData[key]) jsonData[key] = jsonData[key].toString();
                        }
                        data = JSON.stringify(jsonData);
                    }
                    self.logData.push('[' + timeStr + '][console.' + arguments[0].name + '] ' + data);
                }
                var args = Array.prototype.slice.call(arguments);
                args.splice(0, 1);
                return arguments[0].apply(this, args);
            }
            if(console.log){
                var origLog = console.log;
                console.log = function(){
                    var args = Array.prototype.slice.call(arguments);
                    args.splice(0, 0, origLog);
                    return hookConsoleFunc.apply(this, args);
                }
            }
            if(console.dir){
                var origDir = console.dir;
                console.dir = function(data){
                    var args = Array.prototype.slice.call(arguments);
                    args.splice(0, 0, origDir);
                    return hookConsoleFunc.apply(this, args);
                }
            }
            if(console.info){
                var origInfo = console.info;
                console.info = function(data){
                    var args = Array.prototype.slice.call(arguments);
                    args.splice(0, 0, origInfo);
                    return hookConsoleFunc.apply(this, args);
                }
            }
            if(console.warn){
                var origWarn = console.warn;
                console.warn = function(data){
                    var args = Array.prototype.slice.call(arguments);
                    args.splice(0, 0, origWarn);
                    return hookConsoleFunc.apply(this, args);
                }
            }
            if(console.error){
                var origError = console.error;
                console.error = function(data){
                    var args = Array.prototype.slice.call(arguments);
                    args.splice(0, 0, origError);
                    return hookConsoleFunc.apply(this, args);
                }
            }
        }
    },
    
    readLogData: function(){
        return this.logData.splice(0, 1);
    }
    
    };
    qt4w_driver_lib.initHighlightDiv();
    qt4w_driver_lib.hookConsoleLog();
    '''
    
    def __init__(self, webview):
        '''构造函数
        
        :param webview: 对应的WebView实例
        :type webview:  object
        '''
        self._webview = webview
        
    @staticmethod
    def create_driver(webview):
        '''根据webview类型创建对应的WebDriver实例
        
        :param webview: WebView实例
        :type webview:  object
        '''
        web_driver_path = webview.web_driver
        module = __import__(web_driver_path)
        for item in web_driver_path.split('.')[1:]:
            module = getattr(module, item)
        web_driver_cls = getattr(module, 'WebDriver')
        return web_driver_cls(webview)
    
    def _my_encode(self, text):
        '''对于中文，统一处理成unicode编码
        如“中国”，变成“\u4e2d\u56fd”
        '''
        text = unicode_decode(text)
        return general_encode(text.encode('raw_unicode_escape'))

    def _my_decode(self, text):
        return text.decode('raw_unicode_escape')
    
    def _xpath_encode(self, xpath):
        xpath = xpath.replace('\'', '"')
        return xpath
        # return self._my_encode(xpath)
    
    def _xpaths_encode(self, xpath_list):
        for i in range(len(xpath_list)):
            xpath_list[i] = self._xpath_encode(xpath_list[i])
    
    def _break_xpaths(self, elem_xpaths):
        '''将xpath数组分隔成frame_xpaths和elem_xpath
        '''
        if len(elem_xpaths) < 1: raise ValueError('xpath is []')
        frame_xpaths = elem_xpaths[:-1]
        self._xpaths_encode(frame_xpaths)
        elem_xpath = elem_xpaths[-1]
        elem_xpath = self._xpath_encode(elem_xpath)
        return frame_xpaths, elem_xpath
    
    def _get_dom_tree(self, frame_xpaths):
        '''获取DOM树
        '''
        try:
            from tuia.env import run_env, EnumEnvType
            if run_env != EnumEnvType.Lab: return ''
        except ImportError:
            pass
        
        result = '\nCurrent DOM Tree：\n'
        dom_tree = self.eval_script(frame_xpaths, 'document.documentElement.outerHTML;')
        if isinstance(dom_tree, six.text_type): dom_tree = dom_tree.encode('utf8')
        result += dom_tree
        return result
    
    def eval_script(self, frame_xpaths, script):
        '''在指定frame中执行JavaScript，并返回执行结果（该实现需要处理js基础库未注入情况的处理）
        
        :param frame_xpaths: frame元素的XPATH路径，如果是顶层页面，怎传入“[]”
        :type frame_xpaths:  list
        :param script:       要执行的JavaScript语句
        :type script:        string
        '''
        from qt4w.util import JavaScriptError, ControlNotFoundError, ControlAmbiguousError
        try:
            return self._webview.eval_script(frame_xpaths, script)
        except JavaScriptError as e:
            err_msg = e.message
            err_msg = err_msg.split('\n')[0]  # 错误堆栈信息可能会有影响
            err_msg = general_encode(err_msg)
            if ('ReferenceError' in err_msg or 'TypeError' in err_msg) and 'qt4w_driver_lib' in err_msg:
                # ie8 TypeError ie9 ReferenceError
                # 注入js基础库
                self.eval_script(e.frame, self.driver_script)
                return self.eval_script(frame_xpaths, script)
            elif 'Find element' in err_msg and 'failed' in err_msg:
                # 未找到元素
                raise ControlNotFoundError(err_msg)
            elif 'Find' in err_msg and 'elements match' in err_msg:
                err_msg += self._get_dom_tree(frame_xpaths)
                raise ControlAmbiguousError(err_msg)
            else:
                raise e
    
    def get_ready_state(self, frame_xpaths):
        '''获取页面状态
        '''
        return self.eval_script(frame_xpaths, 'document.readyState')
    
    def get_screen_size(self):
        '''获取屏幕大小
        '''
        result = self.eval_script([], 'qt4w_driver_lib.getScreenSize();')
        width, height = result.split(',')
        return int(width), int(height)
    
    def _get_frame_info(self, frame_xpaths):
        '''获取frame属性信息
        '''
        frame_xpath = frame_xpaths[-1].replace('\'', '"')
        js = r'''
        var frame_node = qt4w_driver_lib.selectNode('%s');
        (frame_node.getAttribute('name') || frame_node.getAttribute('id')) + ',' + frame_node.getAttribute('src');
        ''' % (frame_xpath)
        # 优先使用name，没有name使用id
        result = self.eval_script(frame_xpaths[:-1], js)
        pos = result.find(',')
        if pos < 0: raise RuntimeError('Get frame info failed')
        return result[:pos], result[pos + 1:]
    
    def get_element(self, elem_xpaths):
        '''获取控件，如果控件不存在抛出ControlNotFoundError
        
        :param elem_xpaths: 元素xpath路径
        :type elem_xpaths:  list
        '''
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)
        js = '''qt4w_driver_lib.selectNode('%s');''' % elem_xpath
        try:
            return self.eval_script(frame_xpaths, js)
        except ControlNotFoundError as e:
            logger.exception(self._get_dom_tree(frame_xpaths))
            err_msg = e.message
            raise ControlNotFoundError(err_msg)
        
    def get_element_count(self, elem_xpaths):
        '''获取满足elem_xpaths的元素个数
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        '''
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)
        js = '''qt4w_driver_lib.selectNodes('%s').length;''' % elem_xpath
        return int(self.eval_script(frame_xpaths, js))
    
    def get_attribute(self, elem_xpaths, attr_name):
        '''获取元素属性
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param attr_name:   属性名
        :type attr_name:    string
        '''
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)
        js = '''
            var node = qt4w_driver_lib.selectNode('%s');
            node.getAttribute('%s');
        ''' % (elem_xpath, attr_name)
        result = self.eval_script(frame_xpaths, js)
        if result == 'undefined': result = None
        return result
    
    def set_attribute(self, elem_xpaths, attr_name, value):
        '''设置元素属性
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param attr_name:   属性名
        :type attr_name:    string
        :param value:       新的值
        :type value:        string
        '''
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)

        if type(value) == str:
            value = self._my_encode(value)
            value = '\'' + value + '\''
        js = '''
            qt4w_driver_lib.node = qt4w_driver_lib.selectNodes('%s')[0];
            if(qt4w_driver_lib.node == undefined) throw('find %s failed');
            qt4w_driver_lib.result = qt4w_driver_lib.node.setAttribute('%s', %s);
        ''' % (elem_xpath, elem_xpath, attr_name, value)
        return self.eval_script(frame_xpaths, js)
        
    def get_elem_rect(self, elem_xpaths, rav=True):
        '''获取元素在页面中的坐标
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param rav:         是否是相对于当前frame
        :type rav:          bool
        '''
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)
        
        result = self._get_elem_rect(frame_xpaths, elem_xpath)
        if not rav and frame_xpaths:
            while frame_xpaths:
                result1 = self._get_elem_rect(frame_xpaths[:-1], frame_xpaths[-1])
                for i in range(2):
                    result[i] += result1[i]
                frame_xpaths = frame_xpaths[:-1]
        return result
    
    def _get_elem_rect(self, frame_xpaths, elem_xpath):
        '''获取元素在当前frame中的相对坐标
        '''
        js = '''
            qt4w_driver_lib.result = qt4w_driver_lib.getElemRect('%s');
        ''' % elem_xpath  
        result = self.eval_script(frame_xpaths, js)
        result = result.replace('"', '')
        result = result.split(',')
        for i in range(len(result)):
            result[i] = float(result[i])
        return result
    
    def get_property(self, elem_xpaths, prop_name):
        '''获取元素的特定值，例如：node.innerHTML
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param prop_name:   property名
        :type prop_name:    string
        '''
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)

        js = '''
            var node = qt4w_driver_lib.selectNode('%s');
            node.%s;
        ''' % (elem_xpath, prop_name)
        return self.eval_script(frame_xpaths, js)
    
    def set_property(self, elem_xpaths, prop_name, value):
        '''设置元素的特定值，例如：node.innerHTML
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param prop_name:   property名
        :type prop_name:    string
        :param value:       新的值
        :type value:        string
        '''
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)

        if value is None:
            value = ''
        if type(value) == str:
            value = self._my_encode(value)
            value = '\'' + value + '\''
        js = '''
            var node = qt4w_driver_lib.selectNode('%s');
            node.%s = %s;
        ''' % (elem_xpath, prop_name, value)
        return self.eval_script(frame_xpaths, js)
    
    def get_style(self, elem_xpaths, style_name):
        '''获取元素的某一样式值
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param style_name:  样式名称
        :type style_name:   string
        '''
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)

        js = r'''
            var node = qt4w_driver_lib.selectNode('%s');
            window.getComputedStyle(node, null).getPropertyValue('%s');
        ''' % (elem_xpath, style_name)
        return self.eval_script(frame_xpaths, js)
    
    def is_elem_focused(self, elem_xpaths):
        '''是否是当前有焦点元素
        
        :param elem_xpaths:
        :type elem_xpaths:
        '''
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)
        js = r'''
            var node = qt4w_driver_lib.selectNode('%s');
            document.activeElement == node;
        ''' % (elem_xpath)
        return 'true' in self.eval_script(frame_xpaths, js)
    
    def scroll_to_visible(self, elem_xpaths):
        '''将元素滚动到可见区域
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        '''
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)
        js = r'''qt4w_driver_lib.scrollToVisible(qt4w_driver_lib.selectNode('%s'));''' % elem_xpath
        self.eval_script(frame_xpaths, js)
    
    def highlight(self, elem_xpaths):
        '''使元素高亮
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        '''
        self.scroll_to_visible(elem_xpaths)
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)
        
        js = '''qt4w_driver_lib.highlight(qt4w_driver_lib.selectNode('%s'));''' % elem_xpath
        self.eval_script(frame_xpaths, js)
        return True
    
    def drag_element(self, elem_xpaths, from_x, from_y, to_x, to_y):
        '''拖拽元素
        
        :param elem_xpaths: 元素的XPATH路径
        :type elem_xpaths:  list
        :param from_x:      起点横坐标，相对于WebView左上角
        :type from_x:       int/float
        :param from_y:      起点纵坐标，相对于WebView左上角
        :type from_y:       int/float
        :param to_x:        终点横坐标，相对于WebView左上角
        :type to_x:         int/float
        :param to_y:        终点纵坐标，相对于WebView左上角
        :type to_y:         int/float
        '''
        self.scroll_to_visible(elem_xpaths)
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)
        
        js = '''
window['qt4w_driver_lib']['createTouch'] = function(element, point, id) {
    if (document.createTouch)
        return document.createTouch(window, element, id, point.x, point.y, point.x, point.y);

    return {
        view: window,
        target: element,
        identifier: id || 0,
        pageX: point.x,
        pageY: point.y,
        clientX: point.x,
        clientY: point.y
    };
};

window['qt4w_driver_lib']['createTouchList'] = function(touches) {
    if (document.createTouchList)
        return document.createTouchList(touches);

    if (Array.isArray(touches))
        return touches;

    return [touches];
};

window['qt4w_driver_lib']['fireTouchStartEvent'] = function(element, x, y){
    var startEvent = document.createEvent("Event");
    startEvent.initEvent('touchstart', true, true);
    startEvent.touches = this.createTouchList(this.createTouch(element, { x: x, y: y}, 1));
    startEvent.changedTouches = startEvent.touches;
    element.dispatchEvent(startEvent);
};

window['qt4w_driver_lib']['fireTouchMoveEvent'] = function(element, x, y){
    var moveEvent = document.createEvent("Event");
    moveEvent.initEvent('touchmove', true, true);
    moveEvent.touches = this.createTouchList(this.createTouch(element, { x: x, y: y}, 1));
    moveEvent.changedTouches = moveEvent.touches;
    element.dispatchEvent(moveEvent);
};

window['qt4w_driver_lib']['fireTouchEndEvent'] = function(element, x, y){
    var endEvent = document.createEvent("Event");
    endEvent.initEvent('touchend', true, true);
    endEvent.touches = this.createTouchList(this.createTouch(element, { x: x, y: y}, 1));
    endEvent.changedTouches = endEvent.touches;
    element.dispatchEvent(endEvent);
};

window['qt4w_driver_lib']['fireDragEvent'] = function(element, x1, y1, x2, y2){
    this.fireTouchStartEvent(element, x1, y1);
    var self = this;
    setTimeout(function(){self.fireTouchMoveEvent(element, (x1+x2)/2, (y1+y2)/2);}, 200);
    setTimeout(function(){self.fireTouchEndEvent(element, x2, y2);}, 400);
};

qt4w_driver_lib.fireDragEvent(qt4w_driver_lib.selectNode('%s'), %s, %s, %s, %s);
        ''' % (elem_xpath, from_x, from_y, to_x, to_y)
        self.eval_script(frame_xpaths, js)
    
    def fire_event(self, elem_xpaths, type):
        '''触发事件
        
        :param elem_xpaths: 要触发事件的元素XPATH路径
        :type  elem_xpaths: list
        :param type:        事件类型
        :type  type:        string
        '''
        frame_xpaths, elem_xpath = self._break_xpaths(elem_xpaths)
        
        js = '''
var node = qt4w_driver_lib.selectNode('%s');
var evt = document.createEvent("Events");
evt.initEvent('%s', true, false);
node.dispatchEvent(evt);
        ''' % (elem_xpath, type)
        self.eval_script(frame_xpaths, js)
    
    def read_console_log(self, frame_xpaths):
        '''读取指定条数的日志
        
        :param frame_xpaths: 当前页面的XPATH路径
        :type  frame_xpaths: list
        :return:             读取到的一条日志
        '''
        js = '''qt4w_driver_lib.readLogData();'''
        return self.eval_script(frame_xpaths, js)
        
if __name__ == '__main__':
    pass
    
