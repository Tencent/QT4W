# -*- coding: UTF-8 -*-
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

''' browser模块单元测试
'''


import unittest
import mock
from qt4w.browser.browser import Browser

class TestBrowser(unittest.TestCase):


    def test_register_browser(self):
        Browser.register_browser("testBrowser","test.util.FakeBrowser")
        self.assertEqual(Browser.browser_dict["testBrowser"],"test.util.FakeBrowser")

    def test_openurl(self):
        Browser.register_browser("testBrowser", "test.util.FakeBrowser")
        self.assertEqual("http://www.test.com", Browser("testBrowser").open_url("http://www.test.com"))



if __name__ == '__main__':
    unittest.main()