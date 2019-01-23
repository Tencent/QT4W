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
'''WebPage、WebElement接口类
'''


from __future__ import absolute_import,division
import copy
import re
import time
from qt4w.util import Deprecated, TimeoutError, lazy_init, encode_wrap
from qt4w import XPath
from six.moves import xrange
import six

class IWebPage(object):
    '''WebPage接口定义
    '''
    
    @property
    def browser_type(self):
        '''浏览器类型
        '''
        raise NotImplementedError
    
    @property
    def url(self):
        '''页面url
        '''
        raise NotImplementedError
    
    @Deprecated('url')
    @property
    def Url(self):
        '''页面url
        '''
        raise NotImplementedError
    
    @property
    def title(self):
        '''页面标题
        '''
        raise NotImplementedError
    
    @Deprecated('title')
    @property
    def Title(self):
        '''页面标题
        '''
        raise NotImplementedError
    
    @property
    def cookie(self):
        '''页面cookie
        '''
        raise NotImplementedError
    
    @property
    def ready_state(self):
        '''页面状态
        '''
        raise NotImplementedError
    
    @Deprecated('ready_state')
    @property
    def ReadyState(self):
        '''页面状态
        '''
        raise NotImplementedError
    
    @property
    def accessible_object(self):
        '''accessible对象
        '''
        raise NotImplementedError
    
    def activate(self):
        '''激活承载页面的窗口
        '''
        raise NotImplementedError
    
    def close(self):
        '''关闭承载页面的窗口
        '''
        raise NotImplementedError
    
    def release(self):
        '''释放占用的资源
        '''
        raise NotImplementedError
    
    def wait_for_ready(self, timeout=60):
        '''等待页面状态变为ready
        
        :param timeout: 超时时间
        :type timeout:  int
        '''
        raise NotImplementedError
    
    @Deprecated('wait_for_ready')
    def waitForReady(self, timeout=60):
        '''等待页面状态变为ready
        
        :param timeout: 超时时间
        :type timeout:  int
        '''
        raise NotImplementedError
    
    def scroll(self, x, y):
        '''滚动
        
        :param x: 横向滚动的偏移，负值向左，正值向右
        :type x:  int
        :param y: 纵向滚动的偏移，负值向上，正值向下
        :type y:  int
        '''
        raise NotImplementedError
    
    def exec_script(self, script):
        '''在页面中执行JavaScript代码，并返回直接结果
        
        :param script: 要执行的代码
        :type script:  string
        '''
        raise NotImplementedError
    
    @Deprecated('exec_script')
    def execScript(self, script):
        '''在页面中执行JavaScript代码，并返回直接结果
        
        :param script: 要执行的代码
        :type script:  string
        '''
        raise NotImplementedError
    
    def get_element(self, locator):
        '''在页面中查找元素，返回第一个匹配的元素
        
        :param locator: 元素的xpath路径
        :type locator:  string或XPath
        '''
        raise NotImplementedError
    
    @Deprecated('get_element')
    def getElement(self, locator):
        '''在页面中查找元素，返回第一个匹配的元素
        
        :param locator: 元素的xpath路径
        :type locator:  string或XPath
        '''
        raise NotImplementedError
    
    def get_elements(self, locator):
        '''在页面中查找元素，返回包含所有匹配的元素的列表
        
        :param locator: 元素的xpath路径
        :type locator:  string或XPath
        '''
        raise NotImplementedError
    
    @Deprecated('get_elements')
    def getElements(self, locator):
        '''在页面中查找元素，返回包含所有匹配的元素的列表
        
        :param locator: 元素的xpath路径
        :type locator:  string或XPath
        '''
        raise NotImplementedError
    
    def pull_down_refresh(self):
        '''下拉刷新
        '''
        raise NotImplementedError
    
    
    def pull_up_refresh(self):
        '''上拉刷新
        '''
        raise NotImplementedError
    
    def upload_file(self, file_path):
        '''上传文件
        
        :param file_path: 文件路径
        :type  file_path: str
        '''
        raise NotImplementedError
    
    def read_console_log(self, timeout=None):
        '''读取一条console.log输出的日志
        
        :param timeout: 读取日志的超时时间，为None表示不会超时
        :type  timeout: int
        '''
        raise NotImplementedError
        
class IWebElement(object):
    '''WebElement接口定义
    '''
    @property
    def page(self):
        '''元素所在WebPage
        '''
        raise NotImplementedError
    
    @property
    def attributes(self):
        '''元素的属性集合
        '''
        raise NotImplementedError
    
    @Deprecated('attributes')
    @property
    def Attributes(self):
        '''元素的属性集合
        '''
        raise NotImplementedError
    
    @property
    def styles(self):
        '''元素的样式集合
        '''
        raise NotImplementedError
    
    @property
    def rect(self):
        '''元素位置信息
        '''
        raise NotImplementedError
    
    @property
    def BoundingRect(self):
        '''元素位置信息
        '''
        raise NotImplementedError
    
    @property
    def displayed(self):
        '''元素是否显示
        '''
        raise NotImplementedError
    
    @Deprecated('displayed')
    @property
    def Displayed(self):
        '''元素是否显示
        '''
        raise NotImplementedError
    
    @property
    def visible(self):
        '''元素是否视觉可见
        '''
        raise NotImplementedError
    
    @property
    def focused(self):
        '''元素是否有焦点
        '''
        raise NotImplementedError
    
    @property
    def inner_text(self):
        '''元素所包含的文本
        '''
        raise NotImplementedError
    
    @Deprecated('inner_text')
    @property
    def InnerText(self):
        '''元素所包含的文本
        '''
        raise NotImplementedError
    
    @property
    def inner_html(self):
        '''元素所包含的HTML代码
        '''
        raise NotImplementedError
    
    @Deprecated('inner_html')
    @property
    def InnerHtml(self):
        '''元素所包含的HTML代码
        '''
        raise NotImplementedError
    
    def exist(self):
        '''元素是否存在
        '''
        raise NotImplementedError
    
    def scroll(self, x, y):
        '''滚动元素
        
        :param x: 横向滚动的偏移，负值向左，正值向右
        :type x:  int
        :param y: 纵向滚动的偏移，负值向上，正值向下
        :type y:  int
        '''
        raise NotImplementedError
    
    def get_element(self, locator):
        '''在当前元素的子孙元素中查找元素，返回第一个匹配的元素
        
        :param locator: 元素的xpath路径
        :type locator:  string或XPath
        '''
        raise NotImplementedError
    
    @Deprecated('get_element')
    def getElement(self, locator):
        '''在当前元素的子孙元素中查找元素，返回第一个匹配的元素
        
        :param locator: 元素的xpath路径
        :type locator:  string或XPath
        '''
        raise NotImplementedError
    
    def get_elements(self, locator):
        '''在当前元素的子孙元素中查找元素，返回包含所有匹配的元素的列表
        
        :param locator: 元素的xpath路径
        :type locator:  string或XPath
        '''
        raise NotImplementedError
    
    @Deprecated('get_elements')
    def getElements(self, locator):
        '''在当前元素的子孙元素中查找元素，返回包含所有匹配的元素的列表
        
        :param locator: 元素的xpath路径
        :type locator:  string或XPath
        '''
        raise NotImplementedError
    
    def wait_for_visible(self, timeout=10, interval=0.5):
        '''等待控件可见
        
        :param timeout: 超时时间
        :type timeout:  float
        :param interval:查询间隔时间
        :type interval: float
        '''
        raise NotImplementedError
    
    def wait_for_attribute(self, name, value, timeout=10, interval=0.5):
        '''暂停程序执行，直到当前元素的指定属性变为特定值
        
        :param name:   要等待的属性名
        :type name:    string
        :param value:  要等待的属性值
        :type value:   string
        :param timeout:超时时间
        :type timeout: int或float
        :param interval:重试间隔时间
        :type interval:int或float
        '''
        raise NotImplementedError
    
    def wait_for_style(self, name, value, timeout=10, interval=0.5):
        '''暂停程序执行，直到当前元素的指定样式变为特定值
        
        :param name:   要等待的样式名
        :type name:    string
        :param value:  要等待的样式值
        :type value:   string
        :param timeout:超时时间
        :type timeout: int或float
        :param interval:重试间隔时间
        :type interval:int或float
        '''
        raise NotImplementedError
    
    def wait_for_text(self, value, timeout=10, interval=0.5):
        '''暂停程序执行，直到当前元素的InnerText变为特定值
        
        :param value:   要等待的特定值
        :type value:    string
        :param timeout: 超时时间
        :type timeout:  int或float
        :param interval:重试间隔时间
        :type interval: int或float
        '''
        raise NotImplementedError
    
    def click(self, x_offset=None, y_offset=None):
        '''点击元素，默认点击元素中点
        
        :param x_offset: 距离控件区域左上角的横向偏移。
        :type x_offset:  int或float
        :param y_offset: 距离控件区域左上角的纵向偏移。
        :type y_offset:  int或float
        '''
        raise NotImplementedError
    
    def long_click(self, x_offset=None, y_offset=None, duration=1):
        '''长按元素
        
        :param x_offset: 距离控件区域左上角的横向偏移
        :type x_offset:  int/float
        :param y_offset: 距离控件区域左上角的纵向偏移
        :type y_offset:  int/float
        :param duration: 按住的持续时间
        :type duration:  int/float
        '''
        raise NotImplementedError
    
    def double_click(self, x_offset=None, y_offset=None):
        '''双击元素，默认双击元素中点
        
        :param x_offset: 距离控件区域左上角的横向偏移。
        :type x_offset:  int或float
        :param y_offset: 距离控件区域左上角的纵向偏移。
        :type y_offset:  int或float
        '''
        raise NotImplementedError
    
    def right_click(self, x_offset=None, y_offset=None):
        '''右击元素，默认右击元素中点
        
        :param x_offset: 距离控件区域左上角的横向偏移。
        :type x_offset:  int或float
        :param y_offset: 距离控件区域左上角的纵向偏移。
        :type y_offset:  int或float
        '''
        raise NotImplementedError
    
    def hover(self, x_offset=None, y_offset=None):
        '''鼠标悬停
        
        :param x_offset: 距离控件区域左上角的横向偏移。
        :type x_offset:  int或float
        :param y_offset: 距离控件区域左上角的纵向偏移。
        :type y_offset:  int或float
        '''
        raise NotImplementedError
    
    def drag(self, x, y):
        '''拖放元素到指定位置
        
        :param x: 拖放终点距离起点的横向偏移。
        :type x:  int或float
        :param y: 放终点距离起点的纵向偏移。
        :type y:  int或float
        '''
        raise NotImplementedError
    
    def send_keys(self, keys):
        '''发送按键
        
        :param keys: 发送的按键
        :type keys:  string
        '''
        raise NotImplementedError
    
    @Deprecated('send_keys')
    def sendKeys(self, keys):
        '''发送按键
        
        :param keys: 发送的按键
        :type keys:  string
        '''
        raise NotImplementedError
    
    def set_focus(self):
        '''设为焦点
        '''
        raise NotImplementedError

class ControlContainer(object):
    '''控件容器基类
    '''
    ui_control_type = None
    ui_map = {}
    
    def __init__(self):
        self._locator_dict = {}
        self._ui_map = {}
        self._update_ui_map()
        
    def __getitem__(self, key):
        '''获取控件
        '''
        item = copy.copy(self._locator_dict[key])
        cls = item.pop('type')
        root = item.pop('root', None)
        loc = item['locator']
        if isinstance(root, str) and root[0] == '@':
            root = self[root[1:]]
        else:
            root = self

        if issubclass(cls, WebElement):
            return cls(root, loc)
        else:
            return cls(root, key, **item)
            
    @property
    def Controls(self):
        return self
    
    def updateLocator(self, locators):
        '''更新控件定位参数
        
        :type locators: dict
        :param locators: 定位参数，格式是 {'控件名':{'type':控件类, 控件类的参数dict列表}, ...}
        '''
        self._locator_dict.update(locators)
    
    def _update_ui_map(self):
        '''从ui_map中更新控件信息
        '''
        import copy
        cls_list = []
        cls = self.__class__
        while cls != ControlContainer and cls != WebPage and cls != WebElement:
            cls_list.insert(0, cls)  # 基类在前，子类在后
            cls = cls.__base__
        last_cls = None
        for cls in cls_list:
            if cls.ui_map and (not last_cls or cls.ui_map != last_cls.ui_map):
                # 防止某个类未定义ui_map
                ui_map = copy.deepcopy(cls.ui_map)
                self._ui_map.update(ui_map)
            last_cls = cls
    
    def update_ui_map(self, ui_map):
        '''从指定的ui_map中更新控件定义
        '''
        self._ui_map.update(ui_map)
        
    def control(self, name):
        '''获取控件实例
        '''
        from qt4w import XPath
        list_pattern = re.compile(r'^(.+)\[(\d+)\]$')
        if '.' in name:
            # 多层结构方式
            name_list = name.split('.')
            obj = self
            for name in name_list:
                obj = obj.control(name)
            return obj
        
        ret = list_pattern.match(name)
        if ret != None:
            # 索引方式
            name = ret.group(1)
            index = int(ret.group(2))
            return self.control(name)[index]
        
        if not (name in self._ui_map):
            raise NameError("%s没有名为'%s'的子控件！" % (type(self), name))
        ui_control = self._ui_map[name]
        ui_type = self.ui_control_type if self.ui_control_type else WebElement
        if isinstance(ui_control, dict):
            if 'type' in ui_control: ui_type = ui_control['type']
            if not issubclass(ui_type, (WebElement, UIListBase)):
                ui_control.pop('type')
                instance = ui_type(self, name, **ui_control)
                # Not support child control currently
                return instance
        else:
            if not isinstance(ui_control, XPath):
                raise TypeError('控件：%s 类型错误(%s)' % (name, type(XPath)))
            self._ui_map[name] = {'locator': ui_control}
        instance = ui_type(self, self._ui_map[name]['locator'])
        if 'ui_map' in self._ui_map[name]:
            instance._ui_map = self._ui_map[name]['ui_map']
        return instance
    
    def get_metis_view(self):
        '''返回MetisView
        '''
        return MetisView(self)
    
class WebElement(ControlContainer, IWebElement):
    '''IWebElement实现
    '''
    
    def __init__(self, root, locator):
        ControlContainer.__init__(self)
        from qt4w.__init__ import XPath
        from qt4w.util import WebElementAttributes, WebElementStyles
        if isinstance(root, WebPage):
            self._page = root
        else:
            self._page = root.page
        self._webview = self._page._webview
        self._webdriver = self._page._webdriver
        self._root = root
        if isinstance(root, WebPage):
            self._locators = XPath(locator).break_frames()
        elif isinstance(root, FrameElement):
            loc = XPath(locator).break_frames()
            self._locators = root._locators + loc
        else:
            self._locators = root._locators[:-1]
            self._locators += XPath(root._locators[-1] + locator).break_frames()
        self._attrs = WebElementAttributes(self._getattr, self._setattr, self._listattr)
        self._styles = WebElementStyles(self._getstyle)
        
    def __str__(self):
        return '<%s object at 0x%X [xpath=%s]>' % (self.__class__.__name__, id(self), ''.join(self._locators))
    
    def __getitem__(self, key):
        '''获取控件
        '''
        item = self._page._locator_dict[key]
        cls = item['type']
        root = item['root']
        loc = item['locator']
        return cls(self, loc)
    
    def post_init(self):
        '''窗口类自定义的初始化逻辑
        '''
        self._wait_for_exist()
    
    @property
    def page(self):
        '''元素所在WebPage
        '''
        return self._page
    
    @lazy_init
    def _getattr(self, name):
        if name in ["value", "checked", "innerText", "innerHTML"]:
            ret = self._webdriver.get_property(self._locators, name)
        else:
            ret = self._webdriver.get_attribute(self._locators, name)
        return ret
    
    @lazy_init
    def _setattr(self, name, value):
        self.highlight()
        if name in ["value", "checked", "innerText", "innerHTML"]:
            ret = self._webdriver.set_property(self._locators, name, value)
        else:
            ret = self._webdriver.set_attribute(self._locators, name, value)
        return ret

    def _listattr(self):
        return ['id', 'name', 'class']
    
    @lazy_init
    def _getstyle(self, name):
        ret = self._webdriver.get_style(self._locators, name.lower())
        return ret
    
    def _wait_for_exist(self, timeout=10, interval=0.5):
        '''等待元素出现
        
        :param timeout:  超时时间，单位为秒
        :type timeout:   int/float
        :param interval: 重试时间间隔，单位为秒
        :type interval:  int/float
        '''
        time0 = time.time()
        while time.time() - time0 < timeout:
            if self.exist(): return
            time.sleep(interval)
        self._webdriver.get_element(self._locators)
        
    @property
    def attributes(self):
        '''元素的属性集合
        '''
        return self._attrs
    
    @property
    def styles(self):
        '''元素的样式集合
        '''
        return self._styles
    
    @property
    @lazy_init
    def rect(self):
        '''元素相对于WebView的位置信息
        '''
        return self._webdriver.get_elem_rect(self._locators, False)
    
    @property
    def BoundingRect(self):
        '''元素位置信息
        '''
        from qt4w.util import Rect
        return Rect(self.rect)
    
    @property
    @lazy_init
    def displayed(self):
        '''元素是否显示在页面中（Web层可见，肉眼不一定可见）
        '''
        if self.styles['display'] == 'none': return False
        if self.styles['visibility'] == 'hidden': return False  # 只有为hidden的时候才认为不可见
        self_rect = self.rect
        if self_rect[2] == 0 or self_rect[3] == 0: return False
        return True
    
    @property
    def visible(self):
        '''元素是否视觉可见
        '''
        if not self.displayed: return False
        self_rect = self.rect
        root_rect = self._webview.visible_rect
        root_rect = [0, 0, root_rect[2], root_rect[3]]
        
        if self_rect[0] >= root_rect[0] and \
            self_rect[0] + self_rect[2] <= root_rect[0] + root_rect[2] and \
            self_rect[1] >= root_rect[1] and \
            self_rect[1] + self_rect[3] <= root_rect[1] + root_rect[3]:
            return True
        return False
    
    @property
    @lazy_init
    def focused(self):
        '''元素是否有焦点
        '''
        return self._webdriver.is_elem_focused(self._locators)

    @property
    @lazy_init
    @encode_wrap
    def inner_text(self):
        '''元素所包含的文本
        '''
        return self._attrs['innerText']
    
    @inner_text.setter
    @lazy_init
    def inner_text(self, text):
        '''设置元素所包含的文本
        '''
        self._attrs['innerText'] = text
    
    @property
    @encode_wrap
    def inner_html(self):
        '''元素所包含的HTML代码
        '''
        return self._attrs['innerHTML']
    
    @inner_html.setter
    def inner_html(self, html):
        '''设置html代码
        '''
        self._attrs['innerHTML'] = html
        
    def exist(self):
        '''元素是否存在
        '''
        from qt4w.util import ControlNotFoundError
        try:
            self._webdriver.get_element(self._locators)
            return True
        except ControlNotFoundError:
            return False
    
    @lazy_init
    def highlight(self):
        '''高亮
        '''
        self._webdriver.highlight(self._locators)
        time.sleep(0.5) # wait for highlight
        
    def scroll(self, x, y):
        '''滚动元素
        
        :param x: 横向滚动的偏移，负值向左，正值向右
        :type x:  int
        :param y: 纵向滚动的偏移，负值向上，正值向下
        :type y:  int
        '''
        raise NotImplementedError
    
    def get_element(self, locator, elem_cls=None):
        '''在当前元素的子孙元素中查找元素，返回第一个匹配的元素
        
        :param locator: 元素的xpath路径
        :type locator:  string或XPath
        :paran elem_cls: 返回的元素类型
        :type elem_cls:  class
        '''
        if elem_cls == None: elem_cls = WebElement
        return elem_cls(self, locator)
    
    def get_elements(self, locator, elem_cls=None):
        '''在当前元素的子孙元素中查找元素，返回包含所有匹配的元素的列表
        
        :param locator: 元素的xpath路径
        :type locator:  string或XPath
        :paran elem_cls: 返回的元素类型
        :type elem_cls:  class
        '''
        locator = self._locators[-1] + locator
        return self._page.get_elements(locator, elem_cls)
    
    def wait_for_visible(self, timeout=10, interval=0.5):
        '''等待控件可见
        
        :param timeout: 超时时间
        :type timeout:  float
        :param interval:查询间隔时间
        :type interval: float
        '''
        time0 = time.time()
        while time.time() - time0 < timeout:
            if self.visible: return
            time.sleep(interval)
        else:
            raise RuntimeError('元素：%s 在%s秒内不可见' % (''.join(self._locators), timeout))
        
        
    def wait_for_attribute(self, name, value, timeout=10, interval=0.5):
        '''暂停程序执行，直到当前元素的指定属性变为特定值
        
        :param name:   要等待的属性名
        :type name:    string
        :param value:  要等待的属性值
        :type value:   string
        :param timeout:超时时间
        :type timeout: int或float
        :param interval:重试间隔时间
        :type interval:int或float
        '''
        from util import TimeoutError
        time0 = time.time()
        while time.time() - time0 < timeout:
            real_value = self.attributes[name]
            real_value = real_value.replace('"', '')
            if real_value == value:return
            time.sleep(interval)
        raise TimeoutError('等待控件属性%s超时：期望值："%s"，当前值："%s"' % (name, value, self.inner_text))
    
    def wait_for_style(self, name, value, timeout=10, interval=0.5):
        '''暂停程序执行，直到当前元素的指定样式变为特定值
        
        :param name:   要等待的样式名
        :type name:    string
        :param value:  要等待的样式值
        :type value:   string
        :param timeout:超时时间
        :type timeout: int或float
        :param interval:重试间隔时间
        :type interval:int或float
        '''
        raise NotImplementedError
    
    def wait_for_text(self, text, timeout=10, interval=0.5):
        '''暂停程序执行，直到当前元素的InnerText变为特定值
        
        :param text:   要等待的特定值
        :type text:    string
        :param timeout: 超时时间
        :type timeout:  int或float
        :param interval:重试间隔时间
        :type interval: int或float
        '''
        from util import TimeoutError
        time0 = time.time()
        while time.time() - time0 < timeout:
            if self.inner_text == text:return
            time.sleep(interval)
        raise TimeoutError('等待控件文本超时：期望值："%s"，当前值："%s"' % (text, self.inner_text))
    
    def wait_for_value(self, value, timeout=10, interval=0.5):
        '''暂停程序执行，直到当前元素的InnerText变为特定值
        
        :param value:   要等待的特定值
        :type value:    string
        :param timeout: 超时时间
        :type timeout:  int或float
        :param interval:重试间隔时间
        :type interval: int或float
        '''
        
    
    def _pre_click(self, x_offset=None, y_offset=None, highlight=True):
        '''点击前的处理
        '''
        from qt4w.util import TimeoutError
        # 等待控件可见
        timeout = 5
        time0 = time.time()
        while time.time() - time0 < timeout:
            if self.displayed: break
            time.sleep(0.1)
        else:
            raise TimeoutError('控件：%s 在%d秒内不可见' % (self, timeout))
        
        self._webdriver.scroll_to_visible(self._locators)

        rect = self.rect
        time0 = time.time()
        while time.time() - time0 < 2:
            time.sleep(0.5)  # 等待元素位置发生变化
            new_rect = self.rect
            if new_rect != rect: break
            self._webdriver.scroll_to_visible(self._locators) # 避免某些情况下滑动失败
            
        if highlight: self.highlight()

        rect = self.rect  # 此时坐标可能发生变化，需要重新获取
        outer_rect = self._webview.visible_rect
        outer_rect = [0, 0, outer_rect[2], outer_rect[3]]  # 换算成以WebView左上角为原点的坐标
        # 计算交集，避免计算出的坐标为窗口外面
        left = max(rect[0], outer_rect[0])
        top = max(rect[1], outer_rect[1])
        right = min(rect[0] + rect[2], outer_rect[0] + outer_rect[2])
        bottom = min(rect[1] + rect[3], outer_rect[1] + outer_rect[3])
        rect = (left, top, right - left, bottom - top)

        x_offset = rect[0] + (rect[2] / 2 if not x_offset else x_offset)
        y_offset = rect[1] + (rect[3] / 2 if not y_offset else y_offset)
        return x_offset, y_offset
    
    def click(self, x_offset=None, y_offset=None, highlight=True):
        '''点击元素，默认点击元素中点
        
        :param x_offset: 距离控件区域左上角的横向偏移。
        :type x_offset:  int或float
        :param y_offset: 距离控件区域左上角的纵向偏移。
        :type y_offset:  int或float
        :param highlight: 是否高亮元素
        :type  highlight: bool
        '''
        x_offset, y_offset = self._pre_click(x_offset, y_offset, highlight)
        # print x_offset, y_offset
        self._webview.click(x_offset, y_offset)
    
    def long_click(self, x_offset=None, y_offset=None, duration=1):
        '''长按元素
        
        :param x_offset: 距离控件区域左上角的横向偏移
        :type x_offset:  int/float
        :param y_offset: 距离控件区域左上角的纵向偏移
        :type y_offset:  int/float
        :param duration: 按住的持续时间
        :type duration:  int/float
        '''
        x_offset, y_offset = self._pre_click(x_offset, y_offset)
        self._webview.long_click(x_offset, y_offset, duration)
        
    def double_click(self, x_offset=None, y_offset=None):
        '''双击元素，默认双击元素中点
        
        :param x_offset: 距离控件区域左上角的横向偏移。
        :type x_offset:  int或float
        :param y_offset: 距离控件区域左上角的纵向偏移。
        :type y_offset:  int或float
        '''
        x_offset, y_offset = self._pre_click(x_offset, y_offset)
        self._webview.double_click(x_offset, y_offset)
        
    def right_click(self, x_offset=None, y_offset=None):
        '''右击元素，默认右击元素中点
        
        :param x_offset: 距离控件区域左上角的横向偏移。
        :type x_offset:  int或float
        :param y_offset: 距离控件区域左上角的纵向偏移。
        :type y_offset:  int或float
        '''
        x_offset, y_offset = self._pre_click(x_offset, y_offset)
        self._webview.right_click(x_offset, y_offset)
    
    def hover(self, x_offset=None, y_offset=None):
        '''鼠标悬停
        
        :param x_offset: 距离控件区域左上角的横向偏移。
        :type x_offset:  int或float
        :param y_offset: 距离控件区域左上角的纵向偏移。
        :type y_offset:  int或float
        '''
        x_offset, y_offset = self._pre_click(x_offset, y_offset)
        self._webview.hover(x_offset, y_offset)
    
    def drag(self, x, y):
        '''拖放元素到指定位置
        
        :param x: 拖放终点距离起点的横向偏移。
        :type x:  int或float
        :param y: 放终点距离起点的纵向偏移。
        :type y:  int或float
        '''
        screen_size = self._webdriver.get_screen_size()
        if abs(x) > screen_size[0]: x = screen_size[0] * abs(x) / x
        if abs(y) > screen_size[1]: y = screen_size[1] * abs(y) / y
        
        rect = self.rect
        # 计算与屏幕的交集
        if rect[0] < 0: 
            rect[2] += rect[0]
            rect[0] = 0
        if rect[1] < 0: 
            rect[3] += rect[1]
            rect[1] = 0
        if rect[0] + rect[2] > screen_size[0]:
            rect[2] = screen_size[0] - rect[0]
        if rect[1] + rect[3] > screen_size[1]:
            rect[3] = screen_size[1] - rect[1]
        mid_x = rect[0] + rect[2] / 2
        mid_y = rect[1] + rect[3] / 2

        self._webdriver.drag_element(self._locators, mid_x - x / 2, mid_y - y / 2, mid_x + x / 2, mid_y + y / 2)
        time.sleep(1)  # 等待滚动完成
        
    def send_keys(self, keys):
        '''发送按键
        
        :param keys: 发送的按键
        :type keys:  string
        '''
        self.click()
        self._webview.send_keys(keys)
    
    def set_focus(self):
        '''设为焦点
        '''
        raise NotImplementedError  

class WebPage(ControlContainer, IWebPage):
    '''IWebPage接口实现
    '''
    ui_control_type = WebElement
    WebElement.ui_control_type = WebElement  # 不能直接在WebElement中赋值
            
    def __init__(self, webview_or_webpage, locator=None, wait_for_ready=True):
        ControlContainer.__init__(self)
        if locator is None: locator = []
        if isinstance(webview_or_webpage, WebPage):
            self._webview = webview_or_webpage._webview
            self._locator = webview_or_webpage._locator
            self._webdriver = webview_or_webpage._webdriver
        else:
            self._webview = webview_or_webpage
            self._locator = locator
            try:
                self._webdriver = self._webview.webdriver_class(self._webview)
            except NotImplementedError:
                self._webdriver = self._webview  # remove later
        if wait_for_ready: self.wait_for_ready()
        
    def __str__(self):
        return '<%s object at 0x%X [title=%s url=%s]>' % (self.__class__.__name__, id(self), self.title, self.url)
    
    @property
    def browser_type(self):
        '''浏览器类型
        '''
        return self._webview.browser_type
        
    @property
    def url(self):
        '''页面url
        '''
        return self.exec_script('location.href')
    
    @url.setter
    def url(self, new_url):
        '''跳转到指定url
        
        :param new_url: 要跳转到的url
        :type  new_url: str
        '''
        self.exec_script('location.href="%s"' % new_url)
        
    @property
    def title(self):
        '''页面标题
        '''
        return self.exec_script('document.title')
    
    @property
    def cookie(self):
        '''页面cookie
        '''
        return self.exec_script('document.cookie')
    
    @property
    def ready_state(self):
        '''页面状态
        '''
        return self.exec_script('document.readyState')
    
    def activate(self):
        '''激活承载页面的窗口
        '''
        raise NotImplementedError
    
    def close(self):
        '''关闭承载页面的窗口
        '''
        self.exec_script('close()')
    
    def release(self):
        '''释放占用的资源
        '''
        raise NotImplementedError
    
    def wait_for_ready(self, timeout=60):
        '''等待页面状态变为ready
        
        :param timeout: 超时时间
        :type timeout:  int
        '''
        time0 = time.time()
        while time.time() - time0 < timeout:
            if self.ready_state == 'complete': return
            time.sleep(0.5)
        else:
            raise RuntimeError('页面未在%d秒内加载完成' % timeout)
    
    def scroll(self, x, y):
        '''滚动
        
        :param x: 横向滚动的偏移，负值向左，正值向右
        :type x:  int
        :param y: 纵向滚动的偏移，负值向上，正值向下
        :type y:  int
        '''
        self.exec_script('scrollBy(%s, %s);' % (x, y))
    
    @encode_wrap
    def exec_script(self, script):
        '''在页面中执行JavaScript代码，并返回直接结果
        
        :param script: 要执行的代码
        :type script:  string
        '''
        return self._webdriver.eval_script(self._locator, script)
    
    def get_element(self, locator, elem_cls=None):
        '''在页面中查找元素，返回第一个匹配的元素
        
        :param locator: 元素在当前页面的xpath路径
        :type locator:  string或XPath
        :paran elem_cls: 返回的元素类型
        :type elem_cls:  class
        '''
        if elem_cls == None: elem_cls = WebElement
        return elem_cls(self, locator)
    
    def get_elements(self, locator, elem_cls=None):
        '''在页面中查找元素，返回包含所有匹配的元素的列表
        
        :param locator: 元素的xpath路径
        :type locator:  string或XPath
        :paran elem_cls: 返回的元素类型
        :type elem_cls:  class
        '''
        from qt4w.util import LazyDict
        locators = self._locator[:]
        locators.append(locator)
        elem_count = self._webdriver.get_element_count(locators)
        # print elem_count
        def get_elem(index):
            loc = '(%s)[%d]' % (locator, index + 1)
            return self.get_element(loc, elem_cls)

        return LazyDict(get_elem, lister=lambda:xrange(elem_count))
    
    def pull_down_refresh(self):
        '''下拉刷新
        '''
        self.exec_script('scroll(0, 0);')  # 滑动到顶部 
        rect = self._webview.visible_rect
        x1 = x2 = rect[0] + rect[2] / 2
        y1 = rect[1] + rect[3] / 4
        y2 = rect[1] + rect[3] * 3 / 4
        self._webview.drag(x1, y1, x2, y2)  # 从纵坐标1/4处滑倒3/4处

    def pull_up_refresh(self):
        '''上拉刷新 
        '''
        self.exec_script('scroll(0,document.body.scrollHeight);')  # 滑动到底部 
        rect = self._webview.visible_rect
        x1 = x2 = rect[0] + rect[2] / 2
        y1 = rect[1] + rect[3] * 3 / 4
        y2 = rect[1] + rect[3] / 4
        self._webview.drag(x1, y1, x2, y2)  # 从纵坐标3/4处滑倒1/4处
    
    def upload_file(self, file_path):
        '''上传文件
        
        :param file_path: 文件路径
        :type  file_path: str
        '''
        return self._webview.upload_file(file_path)
    
    def read_console_log(self, timeout=None):
        '''读取一条console.log输出的日志
        
        :param timeout: 读取日志的超时时间，为None表示不会超时
        :type  timeout: int
        '''
        time0 = time.time()
        while timeout == None or time.time() - time0 < timeout:
            result = self._webdriver.read_console_log(self._locator)
            if result: return result
            time.sleep(0.1)
        else:
            raise TimeoutError('Read console log timeout')
           
        
class FrameElement(WebElement):
    '''frame/iframe元素
    '''
    def __init__(self, root, locator):
        loc = XPath(locator).break_frames()[-1]
        if not ('/iframe' in loc or '/frame' in loc):
            raise ValueError("Not a Frame nor IFrame: '%s'" % locator)
        super(FrameElement, self).__init__(root, locator)
        self._frame_page = None
    
    def __str__(self):
        return '<%s object at 0x%X [locator=%s]>' % (self.__class__.__name__, id(self), ''.join(self._locators))
    
    @property
    def framepage(self):
        '''frame中包含的WebPage
        '''
        if self._frame_page is None:
            webview = self._webview
            self._frame_page = WebPage(webview, self._locators)
            self._frame_page.updateLocator(self._page._locator_dict)
        return self._frame_page
    
    @property
    def FramePage(self):
        '''
        '''
        return self.framepage

class InputElement(WebElement):
    '''input元素
    '''
    @property
    def value(self):
        '''当前的value
        '''
        return self._webdriver.get_property(self._locators, 'value')
    
    @value.setter
    def value(self, val):
        '''设置新的value
        
        :param val: 新设置的value
        :type  val: string
        '''
        self._webdriver.set_property(self._locators, 'value', str(val))
        self._webdriver.fire_event(self._locators, 'input')
        self._webdriver.fire_event(self._locators, 'change')
        
class SelectElement(WebElement):
    '''select元素
    '''
    
    @property
    def options(self):
        '''返回所有选项列表
        '''
        option_list = []
        for it in self.get_elements('/option'):
            option_list.append(it.inner_text.strip())
        return option_list
    
    @property
    def selection(self):
        '''当前选择项
        '''
        return self._webdriver.get_property(self._locators, 'selectedIndex')
    
    @selection.setter
    def selection(self, option):
        '''选择某个选项
        
        :param option: 要选中的选项索引或显示的内容
        :type  option: int/string
        '''
        if isinstance(option, (str, six.text_type)):
            # change to option index
            option = self.options.index(option)

        self._webdriver.set_property(self._locators, 'selectedIndex', option)
        self._webdriver.fire_event(self._locators, 'change')
        
        
class UIListBase(object):
    '''List控件基类
    '''
    ui_control_type = None
    
    def __init__(self, root, locator):
        self._root = root
        self._locator = locator
        self._ui_map = {}
        self._elements = []
    
    def _get_elements(self):
        '''获取元素列表
        '''
        if self._elements: return self._elements
        result = []
        elements = list(self._root.get_elements(self._locator, self.ui_control_type))
        for elem in elements:
            elem._ui_map.update(self._ui_map)
            elem._parent = self._root  # elem._root是WebPage对象
            result.append(elem)
        self._elements = result
        return result
    
    def __len__(self):
        '''list长度
        '''
        return len(self._get_elements())
    
    def __iter__(self):
        '''迭代器
        '''
        for elem in self._get_elements():
            yield elem
    
    def __getitem__(self, index):
        '''索引方式访问
        '''
        if not isinstance(index, (int, six.integer_types)):
            raise TypeError('索引值必须为整数：%r' % index)
        if index < 0: index += len(self)
        if index >= len(self): raise IndexError('索引越界，数组长度为：%d，当前索引值为： %d' % (len(self), index))
        elem = self._get_elements()[index]
        return elem
    
    def filter(self, condition):
        '''根据条件过滤，找到满足条件的项即返回，如果找不到则抛出异常
        
        :param condition: 过滤条件
        :type condition:  dict
        '''
        if not condition: raise RuntimeError('过滤条件不能为空')
        pattern = re.compile(r'^(\w+)\[(.+)\]$')
        for elem in self._get_elements():
            equal_flag = True
            for key in condition:
                if not '.' in key:
                    raise ValueError('过滤条件错误：%s' % key)
                control_name, attr_name = key.split('.')
                child_elem = elem.control(control_name)
                index = ''
                ret = pattern.match(attr_name)
                if ret != None:
                    attr_name = ret.group(1)
                    index = ret.group(2)[1:-1]
                if not hasattr(child_elem, attr_name):
                    raise RuntimeError('控件：%s 没有属性：%s' % (child_elem, attr_name))
                value = getattr(child_elem, attr_name)
                if index: value = value.__getitem__(index)
                if value != condition[key]:
                    equal_flag = False
                    break
            if equal_flag: return elem
        raise RuntimeError('未找到满足条件：%s 的子控件' % condition)

def ui_list(control_cls):
    '''列表类型
    '''
    return type('%sList' % control_cls.__name__, (UIListBase,), {'ui_control_type': control_cls})

class MetisView(object):
    '''实现IMetisView接口
    '''
    
    def __init__(self, page_or_elem):
        if isinstance(page_or_elem, WebPage):
            self._page = page_or_elem
            self._elem = None
        else:
            self._page = page_or_elem.page
            self._elem = page_or_elem
        self._webview = self._page._webview
        
    @property
    def rect(self):
        '''元素相对坐标(x, y, w, h)
        '''
        if self._elem == None:
            rect = self._webview.rect
            return (0, 0, rect[2], rect[3])
        else:
            return self._elem.rect
            
    @property
    def os_type(self):
        '''系统类型，例如"android"，"ios"，"pc"
        '''
        return 'web'

    def screenshot(self):
        '''当前容器的区域截图
        :return: PIL.image
        '''
        image = self._webview.screenshot()
        if self._elem != None:
            image = image.crop(self.rect)
        return image
    
    def _get_position(self, offset_x=None, offset_y=None):
        '''
        '''
        if offset_x == None: offset_x = 0.5
        if offset_y == None: offset_y = 0.5
        rect = self.rect
        x = rect[0] + int(rect[2] * offset_x)
        y = rect[1] + int(rect[3] * offset_y)
        return x, y
        
    def click(self, offset_x=None, offset_y=None):
        '''点击
        :param offset_x: 相对于该控件的坐标offset_x，百分比( 0 -> 1 )，不传入则默认该控件的中央
        :type offset_x: float|None
        :param offset_y: 相对于该控件的坐标offset_y，百分比( 0 -> 1 )，不传入则默认该控件的中央
        :type offset_y: float|None
        '''
        x, y = self._get_position(offset_x, offset_y)
        self._webview.click(x, y)

    def send_keys(self, text):
        '''发送可见字符按键
        
        :param text: 要输入的文本
        :type  text: string
        '''
        self._webview.send_keys(text)

    def double_click(self, offset_x=None, offset_y=None):
        '''双击
        '''
        x, y = self._get_position(offset_x, offset_y)
        self._webview.double_click(x, y)

    def long_click(self, offset_x=None, offset_y=None):
        '''长按
        '''
        x, y = self._get_position(offset_x, offset_y)
        self._webview.long_click(x, y)
            
if __name__ == '__main__':
    pass
    
