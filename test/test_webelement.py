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

''' Webelement模块单元测试
'''

from __future__ import absolute_import
import unittest
import mock
from qt4w.webview.webview  import IWebView
from qt4w.webcontrols import WebElement ,ui_list,UIListBase
from test.util import TestPage,TestElement
from past.builtins import cmp


class TestWebElement(unittest.TestCase):
    def get_control(self):
        test = TestPage()
        return test.control("test")

    def test_page(self):
        element= self.get_control()
        self.assertTrue(isinstance(element.page,TestPage))
        self.assertEqual("testbrowser",element.page.browser_type)

    def test_controls(self):
        test = TestPage()
        element=test.control("test")
        self.assertTrue(isinstance(element,WebElement))
        self.assertEqual("//div[@id='test']",element._locators[0])
        close = test.control("test.close")
        self.assertTrue(isinstance(close, WebElement))
        self.assertEqual( "//div[@id='test']//div[@class='close']",close._locators[0])


    def test_rect(self):
        element = self.get_control()
        self.assertEqual(0,cmp(element.rect,[0,1,2,3]))

    def test_Boundrect(self):
        element = self.get_control()
        self.assertEqual(0, element.BoundingRect.left )
        self.assertEqual(1, element.BoundingRect.top)
        self.assertEqual(2, element.BoundingRect.width)
        self.assertEqual(3, element.BoundingRect.height)

    def test_dispaly(self):
        test = TestPage()
        element = test.control("test")
        #验证display为None
        style={"display":"none"}
        test.get_webview().set_attr_dict(style)
        self.assertFalse(element.displayed)
        # 验证display不为None
        style = {"display": "True","visibility":"display"}
        test.get_webview().set_attr_dict(style)
        self.assertTrue(element.displayed)
        # 验证visibility为hidden
        style = {"display": "True", "visibility": "hidden"}
        test.get_webview().set_attr_dict(style)
        self.assertFalse(element.displayed)
        # 验证width或者heigth为0
        test.get_webview().set_rect([0,0,0,1])
        self.assertFalse(element.displayed)
        test.get_webview().set_rect([0, 0, 1, 0])
        self.assertFalse(element.displayed)

    def test_visible(self):
        test = TestPage()
        #diaplay 不显示
        style = {"display": "none"}
        test.get_webview().set_attr_dict(style)
        element = test.control("test")
        self.assertFalse(element.visible)
        # 控件正常显示
        style = {"display": "true","visibility":"display"}
        test.get_webview().set_attr_dict(style)
        self.assertTrue(element.visible)
        #控件显示不全
        test.get_webview().set_rect([0,1,2,5])
        self.assertFalse(element.visible)

    def test_innertext(self):
        test = TestPage()
        attr = {"innerText": "innerTextTest"}
        test.get_webview().set_attr_dict(attr)
        element = test.control("test")
        self.assertEqual("innerTextTest",element.inner_text)

    def test_set_innertext(self):
        test = TestPage()
        attr = {"innerText": "innerTextTest"}
        test.get_webview().set_attr_dict(attr)
        element = test.control("test")
        element.inner_text= "setInnertexttest"
        self.assertEqual("setInnertexttest",element.inner_text)

    def test_innerhtml(self):
        test = TestPage()
        attr = {"innerHTML": "innerhtmlTest"}
        test.get_webview().set_attr_dict(attr)
        element = test.control("test")
        self.assertEqual("innerhtmlTest",element.inner_html)

    def test_set_innerhtml(self):
        test = TestPage()
        attr = {"innerHTML": "innerHtmlTest"}
        test.get_webview().set_attr_dict(attr)
        element = test.control("test")
        element.inner_html= "setInnerhtmltest"
        self.assertEqual("setInnerhtmltest",element.inner_html)

    def test_exist(self):
        element=self.get_control()
        self.assertTrue(element.exist())

    def test_pre_click(self):
        test = TestPage()
        style = {"display": "true", "visibility": "display"}
        test.get_webview().set_attr_dict(style)
        element = test.control("test")
        xoff,yoff=element._pre_click()
        self.assertEqual(1,xoff)
        self.assertEqual(2.5,yoff)
        xoff, yoff = element._pre_click(x_offset=1, y_offset=1)
        self.assertEqual(1, xoff)
        self.assertEqual(2, yoff)

class TestUIListBase(unittest.TestCase):
    def get_uilist(self):
        test=TestElement()
        return ui_list(TestElement)(test,"//div[id@='test']")

    def test_len(self):
        uilist=self.get_uilist()
        self.assertEqual(3, len(uilist))

    def test_getelements(self):
        uilist = self.get_uilist()
        self.assertTrue(isinstance(uilist._get_elements()[0],TestElement))
        self.assertEqual(3, len(uilist._get_elements()))

    def test_fikter_condition_null(self):
        uilist = self.get_uilist()
        self.assertRaises( RuntimeError,uilist.filter,'')

    def test_filter_attrbute_null(self):
        uilist = self.get_uilist()
        self.assertRaises(RuntimeError,uilist.filter,{"test.value":"test"})

    def test_filter_atrr(self):
        uilist = self.get_uilist()
        self.assertRaises(RuntimeError,uilist.filter, {"test.attributes['value']":"value"})
        self.assertTrue(isinstance(uilist.filter({"test.attributes['value']": "test"}),TestElement))

if __name__ == '__main__':
    unittest.main()