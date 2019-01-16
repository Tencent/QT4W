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
    document.addEventListener('click', function(event){console.log('[ClickListener](' + event.clientX + ', ' + event.clientY + ')');}, true);
    '''
