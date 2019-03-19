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
'''QT4W公共库
'''

from __future__ import absolute_import, print_function
import sys, os
import logging as logger
import six

class QT4WRuntimeError(RuntimeError):
    '''QT4W运行时错误
    '''
    
    @property
    def message(self):
        '''解决python3上没有message属性的问题
        '''
        return self.args[0]
    
class JavaScriptError(RuntimeError):
    '''执行JavaScript报错
    '''
    def __init__(self, frame, err_msg):
        super(JavaScriptError, self).__init__(err_msg)
        self._frame = frame
        self._err_msg = err_msg
        
    @property
    def frame(self):
        '''发生JS异常的frame
        '''
        return self._frame
    
    @property
    def message(self):
        return self._err_msg
    
    def __str__(self):
        return '%s%s' % (self.frame, self._err_msg)

class ControlNotFoundError(QT4WRuntimeError):
    '''Web元素未找到
    '''
    pass
    

class ControlAmbiguousError(QT4WRuntimeError):
    '''找到多个控件
    '''
    pass

class TimeoutError(QT4WRuntimeError):
    '''超时错误
    '''
    pass
    
class LazyDict(object):
    '''类字典容器，本身不存储数据，只在需要时调用相应函数实现读写操作'''
    def __init__(self, getter, setter=None, lister=None):
        self._getter = getter
        self._setter = setter
        self._lister = lister

    def __getitem__(self, key):
        return self._getter(key)

    def __setitem__(self, key, value):
        if not self._setter:
            raise Exception("Item cannot be set.")
        return self._setter(key, value)

    def __delitem__(self):
        raise Exception("Item cannot be deleted.")

    def __iter__(self):
        if not self._lister:
            raise Exception("Items cannot be listed.")
        keys = self._lister()
        for key in keys:
            yield self.__getitem__(key)        

    def __len__(self):
        return len(self._lister())

    def __str__(self):
        keys = self._lister()
        ret = "{"
        for key in keys:
            ret += "%s: %s, " % (repr(key), repr(self[key]))
        return ret[:-2] + "}"

class WebElementAttributes(LazyDict):
    '''供WebElement的Attributes属性使用的类字典容器'''
    def __delitem__(self):
        raise Exception("Attribute cannot be deleted.")

class WebElementStyles(LazyDict):
    '''供WebElement的Styles属性使用的类字典容器'''
    def __setitem__(self, key, value):
        raise Exception("Style cannot be set.")

    def __delitem__(self):
        raise Exception("Style cannot be deleted.")

def general_encode(s):
    '''字符串通用编码处理
    python2 => utf8
    python3 => unicode
    '''
    if six.PY2 and isinstance(s, (unicode, )):
        s = s.encode('utf8')
    elif six.PY3 and isinstance(s, (bytes,)):
        s = s.decode('utf8')
    return s

def unicode_decode(s):
    '''将字符串解码为unicode编码
    '''
    if six.PY2 or isinstance(s, (bytes,)):
        s = s.decode('utf8')
    return s
    
def encode_wrap(func):
    '''处理函数返回值编码
    '''
    def wrap_func(*args, **kwargs):
        ret = func(*args, **kwargs)
        return general_encode(ret)
    return wrap_func

class Deprecated(object):
    '''废弃函数包装
    '''
    def __init__(self, new_func):
        self._new_func = new_func
    
    def __call__(self, func):
        def wrap_func(this, *args, **kwargs):
            # print 'call', func
            frame = sys._getframe(1)
            code = frame.f_code
            file_name = os.path.split(code.co_filename)[-1]
            print >> sys.stderr, '[Warning] method [%s] is deprecated, called in [%s:%s], pls use [%s] instead' % (func.__name__, file_name, code.co_name, self._new_func)
            return getattr(this, self._new_func)(*args, **kwargs)
        
        if func.__class__.__name__ == 'function': 
            return wrap_func
        elif isinstance(func, property): 
            def prop_fget(fget):
                def _wrap_fget(this):
                    frame = sys._getframe(1)
                    code = frame.f_code
                    file_name = os.path.split(code.co_filename)[-1]
                    print >> sys.stderr, '[Warning] property [%s] is deprecated, called in [%s:%s], pls use [%s] instead' % (fget.__name__, file_name, code.co_name, self._new_func)
                    return getattr(this, self._new_func)
                return _wrap_fget
            return property(prop_fget(func.fget), func.fset, func.fdel)
        else:
            raise NotImplementedError(func.__class__.__name__)

def lazy_init(func):
    '''懒初始化
    '''
    def _wrap_func(self, *args, **kwargs):
        if not hasattr(self, '__inited') or self.__inited != True:
            self.post_init()
            self.__inited = True
        return func(self, *args, **kwargs)
    return _wrap_func

class Rect(object):
    '''控件坐标区域
    '''
    def __init__(self, rect):
        self._rect = rect  # [left, top, width, height]
    
    def __getitem__(self, index):
        if not isinstance(index, (int, six.integer_types)):
            raise IndexError('index must be integer')
        if index >= 0 and index < 4:
            return self._rect[index]
        else:
            raise IndexError('index %d out of range' % index)
    
    @property
    def left(self):
        '''左上角横坐标
        '''
        return self._rect[0]
    
    @Deprecated('left')
    @property
    def Left(self):
        '''左上角横坐标
        '''
        raise NotImplementedError
    
    @property
    def top(self):
        '''左上角纵坐标
        '''
        return self._rect[1]
    
    @Deprecated('top')
    @property
    def Top(self):
        '''左上角纵坐标
        '''
        raise NotImplementedError
    
    @property
    def width(self):
        '''宽度
        '''
        return self._rect[2]
    
    @Deprecated('width')
    @property
    def Width(self):
        '''宽度
        '''
        raise NotImplementedError
    
    @property
    def height(self):
        '''高度
        '''
        return self._rect[3]
    
    @Deprecated('height')
    @property
    def Height(self):
        '''高度
        '''
        raise NotImplementedError

class Frame(object):
    '''frame element
    '''
    
    def __init__(self, _id, name, url):
        self._id = _id
        self._name = name
        self._url = url
        self._children = []
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def url(self):
        return self._url
    
    def add_child(self, frame):
        '''添加子frame
        '''
        self._children.append(frame)
    
    def find_child_frame(self, name, url):
        '''查找子frame
        '''
        for child in self._children:
            if (name and name == child.name) or (url and url == child.url):
                return child
        return None
    
class FrameSelector(object):
    '''Frame定位
    '''
    
    def __init__(self, webdriver, root_frame):
        '''
        :param webdriver: WebDriver实例
        :param root_frame: 顶层Frame对象
        '''
        self._webdriver = webdriver
        self._root_frame = root_frame
        
    def get_frame_by_xpath(self, frame_xpaths):
        '''根据XPath对象查找frame
        
        :param frame_xpaths: frame的xpath数组
        :type frame_xpaths: list
        :return: Frame object
        '''
        if not frame_xpaths: return self._root_frame
        frame = self._root_frame
        for i in range(len(frame_xpaths)):
            name, url = self._webdriver._get_frame_info(frame_xpaths[:i + 1])
            frame = frame.find_child_frame(name, url)
            if frame == None:
                # frame not found
                return None
        return frame

if __name__ == '__main__':
    pass
