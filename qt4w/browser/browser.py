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
'''IBrowser接口定义
'''

from __future__ import absolute_import
import random
from qt4w.util import logger

class IBrowser(object):
    '''浏览器接口类
    '''
    
    def open_url(self, url, page_cls=None):
        '''打开一个url，返回page_cls类的实例
        
        :param url: 要打开页面的url
        :type url:  string
        :param page_cls: 要返回的具体WebPage类,为None表示返回WebPage实例
        :type page_cls: Class
        '''
        raise NotImplementedError
    
    def find_by_url(self, url, page_cls=None):
        '''在当前打开的页面中查找指定url,返回page_cls类的实例，如果未找到，返回None
        
        :param url: 要查找的页面url
        :type url:  string
        :param page_cls: 要返回的具体WebPage类,为None表示返回WebPage实例
        :type page_cls: Class
        '''
        raise NotImplementedError
    
class Browser(IBrowser):
    '''对外的浏览器类
    '''
    browser_dict = {}  # 存储浏览器类型与浏览器类的对应关系
    
    def __init__(self, browser_name=None):
        '''创建具体的Browser实例
        
        :param browser_name: 要创建的浏览器类型
        :type browser_name:
        '''
        self._browser_name = browser_name
        self._browser = self._get_browser_cls()
    
    def _get_browser_cls(self):
        '''获取浏览器类
        '''
        if not self._browser_name:
            # 随机选择浏览器
            self._browser_name = random.choice(self.browser_dict.keys())
        browser_cls_path = self.browser_dict.get(self._browser_name)
            
        if not browser_cls_path:
            raise TypeError('Browser %s is not registered' % self._browser_name)
        logger.info('[Browser] Current browser type is %s' % self._browser_name)
        
        module = __import__('.'.join(browser_cls_path.split('.')[:-1]))
        for item in browser_cls_path.split('.')[1:]:
            module = getattr(module, item)
        return module()
    
    @staticmethod
    def register_browser(browser_name, browser_cls_path):
        '''注册浏览器
        
        :param browser_name:     浏览器名称
        :type browser_name:      string
        :param browser_cls_path: 浏览器类路径
        :type browser_cls_path:  string
        '''
        Browser.browser_dict[browser_name] = browser_cls_path
        
    def open_url(self, url, page_cls=None):
        '''打开一个url，返回page_cls类的实例
        
        :param url: 要打开页面的url
        :type url:  string
        :param page_cls: 要返回的具体WebPage类,为None表示返回WebPage实例
        :type page_cls: Class
        '''
        return self._browser.open_url(url, page_cls)
    
    def find_by_url(self, url, page_cls=None, timeout=10):
        '''在当前打开的页面中查找指定url,返回WebPage实例，如果未找到，返回None
        
        :param url: 要查找的页面url
        :type url:  string
        :param page_cls: 要返回的具体WebPage类,为None表示返回WebPage实例
        :type page_cls: Class
        :param timeout: 查找超时时间，单位：秒
        :type timeout: int/float
        '''
        page = self._browser.find_by_url(url, page_cls, timeout)
        if page == None: raise RuntimeError('Can\'t find page %s in browser %s' % (url, self._browser_name))
        return page
        
if __name__ == '__main__':
    pass
    
