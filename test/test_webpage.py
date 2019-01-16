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

''' WebPage模块单元测试
'''

import unittest
from test.util import TestWebView
from qt4w.webcontrols import WebPage, WebElement
import mock

class MyElement(WebElement):
    pass

class testWebPage(unittest.TestCase):
    def _getPage(self):
        testview=TestWebView("TestBrowser")
        return WebPage(testview)

    def test_browser_tye(self):
        page=self._getPage()
        self.assertEqual(page.browser_type,"TestBrowser")

    def test_url(self):
        page=self._getPage()
        self.assertEqual(page.url,"http://www.test.com")

    def test_title(self):
        page = self._getPage()
        self.assertEqual(page.title, "testtitle")

    def test_cookie(self):
        page = self._getPage()
        cookie=page.cookie["Test"]
        self.assertEqual(cookie, "test")

    def test_ready_state(self):
        page = self._getPage()
        self.assertEqual(page.ready_state, "complete")

    def test_wait_for_ready(self):
        page = self._getPage()
        self.assertEqual(page.wait_for_ready(), None)

    def test_wait_for_ready_timeout(self):
        testview = TestWebView("TestBrowser")
        page = WebPage(testview, wait_for_ready=False)
        page._webdriver.set_dict("document.readyState","not Ready")
        self.assertRaises(RuntimeError,page.wait_for_ready, timeout=10)

    def test_upload(self):
        page = self._getPage()
        self.assertEqual(page.upload_file("/root"), "/root upload complete")

    def test_console_log(self):
        page = self._getPage()
        self.assertEqual(page.read_console_log(), "testlog")

    def test_get_element(self):
        page = self._getPage()
        ele=page.get_element("//div[@id='test']")
        self.assertTrue(isinstance(ele,WebElement))

    def test_get_myelement(self):
        page = self._getPage()
        ele = page.get_element("//div[@id='test']",MyElement)
        self.assertTrue(isinstance(ele, MyElement))

    def test_get_elements(self):
        page = self._getPage()
        ele = page.get_elements("//div[@id='test']")
        self.assertEqual(len(ele),3)
        self.assertEqual(ele[0]._locators[0], "(//div[@id='test'])[1]")

if __name__ == '__main__':
    unittest.main()