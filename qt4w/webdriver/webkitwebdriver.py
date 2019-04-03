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

'''Webkit WebDrvier实现
'''


from __future__ import absolute_import
from qt4w.webdriver.webdriver import WebDriverBase

class WebkitWebDriver(WebDriverBase):
    '''Webkit WebDrvier
    '''
    
    driver_script = WebDriverBase.driver_script + r'''
    window.Notification = undefined; // disable Notification
    window['qt4w_driver_lib']['getScale'] = function(){return window.devicePixelRatio;};
    window['qt4w_driver_lib']['getElemRect'] = function(node) {
        var result = new Array();
        var rect = node.getBoundingClientRect();
        var scale = this.getScale();
        scale *= this.getElementZoom(node);
        var left = rect.left;
        var top = rect.top;
        if (document.documentElement.scrollWidth > document.documentElement.clientWidth) {
            // 页面未适配终端
            if (window.visualViewport) {
                // above Chrome 61
                left -= window.visualViewport.offsetLeft;
                top -= window.visualViewport.offsetTop;
            } else {
                if (window.scrollX && document.documentElement.getBoundingClientRect().left == 0) {
                    // getBoundingClientRect return fix position
                    left -= window.scrollX;
                }
                if (window.scrollY && document.documentElement.getBoundingClientRect().top == 0) {
                    top -= window.scrollY;
                }
            }
        }
        
        result.push(left * scale);
        result.push(top * scale);
        result.push(rect.width * scale);
        result.push(rect.height * scale);
        return result.toString();
    }
    document.addEventListener('click', function(event){console.log('[ClickListener](' + event.clientX + ', ' + event.clientY + ')');}, true);
    '''
