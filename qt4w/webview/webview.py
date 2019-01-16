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
'''IWebView接口
'''



class IWebView(object):
    '''IWebView接口
    '''
    
    @property
    def webdriver_class(self):
        '''WebView对应的WebDriver类
        '''
        raise NotImplementedError
        
    @property
    def rect(self):
        '''WebView控件的坐标信息
        '''
        raise NotImplementedError
    
    @property
    def visible_rect(self):
        '''WebView控件可见区域的坐标信息
        '''
        return self.rect
    
    def eval_script(self, frame_xpaths, script):
        '''在指定frame中执行JavaScript，并返回执行结果
        
        :param frame_xpaths: frame元素的XPATH路径，如果是顶层页面，则传入“[]”
        :type frame_xpaths:  list
        :param script:       要执行的JavaScript语句
        :type script:        string
        '''
        raise NotImplementedError
    
    def screenshot(self):
        '''当前WebView的截图
        :return: PIL.Image
        '''
        raise NotImplementedError
        
    def click(self, x_offset, y_offset):
        '''点击WebView中的某个坐标
        
        :param x_offset: 与WebView左上角的横向偏移量
        :type x_offset:  int/float
        :param y_offset: 与WebView左上角的纵向偏移量
        :type y_offset:  int/float
        '''
        raise NotImplementedError
    
    def send_keys(self, text):
        '''发送可见字符按键
        
        :param text: 要输入的文本
        :type  text: string
        '''
        raise NotImplementedError
        
    def long_click(self, x_offset, y_offset, duration=1):
        '''长按WebView中的某个坐标
        
        :param x_offset: 与WebView左上角的横向偏移量
        :type x_offset:  int/float
        :param y_offset: 与WebView左上角的纵向偏移量
        :type y_offset:  int/float
        :param duration: 按住的持续时间
        :type duration:  int/float
        '''
        raise NotImplementedError
    
    def right_click(self, x_offset, y_offset):
        '''右键点击WebView中的某个坐标
        
        :param x_offset: 与WebView左上角的横向偏移量
        :type x_offset:  int/float
        :param y_offset: 与WebView左上角的纵向偏移量
        :type y_offset:  int/float
        '''
        raise NotImplementedError
    
    def double_click(self, x_offset, y_offset):
        '''双击WebView中的某个坐标
        
        :param x_offset: 与WebView左上角的横向偏移量
        :type x_offset:  int/float
        :param y_offset: 与WebView左上角的纵向偏移量
        :type y_offset:  int/float
        '''
        raise NotImplementedError
    
    def drag(self, x1, y1, x2, y2):
        '''从(x1, y1)点拖动到(x2, y2)点
        
        :param x1: 起点横坐标
        :type x1:  int/float
        :param y1: 起点纵坐标
        :type y1:  int/float
        :param x2: 终点横坐标
        :type x2:  int/float
        :param y2: 终点纵坐标
        :type y2:  int/float
        '''
        raise NotImplementedError
    
    def hover(self, x_offset, y_offset):
        '''
        
        :param x_offset: 与WebView左上角的横向偏移量
        :type x_offset:  int/float
        :param y_offset: 与WebView左上角的纵向偏移量
        :type y_offset:  int/float
        '''
        raise NotImplementedError
    
    def scroll(self, backward=True):
        '''
        
        :param backward: 是否向后滚动，默认为True
        :type  backward: bool
        '''
        raise NotImplementedError
     
    def upload_file(self, file_path):
        '''上传文件
        
        :param file_path: 文件路径
        :type  file_path: str
        '''
        raise NotImplementedError
     
# class WebViewBase(IWebView):
#     '''WebView基类，实现一些公共方法
#     '''
#     
#     def _handle_result(self, result, frame_xpaths):
#         '''处理执行JavaScript的结果
#         
#         :param result: 要处理的数据
#         :type  result: string
#         :param frame_xpaths: 执行js所在frame的xpath
#         :type  frame_xpaths: list
#         '''
#         from qt4w.util import JavaScriptError
#         if result[0] == 'S': return result[1:]
#         elif result[0] == 'E':
#             raise JavaScriptError(frame_xpaths, result[1:])
#         else:
#             raise ValueError('执行JavaScript返回结果错误：%r' % result)
            
