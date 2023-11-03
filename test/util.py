# -*- coding: utf-8 -*-
#
# Tencent is pleased to support the open source community by making QT4W available.
# Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the BSD 3-Clause License (the "License");you may not use this
# file except in compliance with the License. You may obtain a copy of the License at
#
# https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
#

"""QT4W单元测试 使用项
"""
from __future__ import absolute_import

import threading

try:
    import BaseHTTPServer as httpserver
except ImportError:
    import http.server as httpserver

from qt4w.webview.webview import IWebView
from qt4w.webdriver.webdriver import IWebDriver
from qt4w.webcontrols import WebPage, WebElement
from qt4w.browser.browser import IBrowser
from qt4w import XPath


class MockWebDriver(IWebDriver):
    """Mock WebDriver"""

    attr_dict = {}
    js_dict = {
        "location.href": "http://www.test.com",
        "document.title": "testtitle",
        "document.cookie": {"Test": "test"},
        "document.readyState": "complete",
        "close()": "closePage",
    }
    rect = [0, 1, 2, 3]

    def __init__(self, webview):
        self._webview = webview

    def set_attr_dict(self, dict):
        """替换属性字典

        :param dict:
        :return:
        """
        self.attr_dict = {}
        self.attr_dict.update(dict)

    def set_dict(self, key, value):
        self.js_dict[key] = value

    def get_attribute(self, elem_xpaths, attr_name):
        return self.attr_dict[attr_name]

    def get_property(self, elem_xpaths, prop_name):
        return self.attr_dict[prop_name]

    def get_style(self, elem_xpaths, style_name):
        return self.attr_dict[style_name]

    def set_attribute(self, locator, name, value):
        self.attr_dict[name] = value

    def set_property(self, locator, name, value):
        self.attr_dict[name] = value

    def highlight(self, elem_xpaths):
        return elem_xpaths

    def drag_element(self, x1, y1, x2, y2):
        rect = []
        rect.append(x1)
        rect.append(y1)
        rect.append(x2)
        rect.append(y2)
        return rect

    def eval_script(self, frame_xpaths, script):
        """模拟JS执行方法"""
        if script in self.js_dict.keys():
            return self.js_dict[script]

    def get_element(self, locator):
        return locator

    def set_rect(self, list):
        self.rect = []
        self.rect.extend(list)

    def get_elem_rect(self, locator, recv=True):
        return self.rect

    def scroll_to_visible(self, locators):
        return True

    def read_console_log(self, timeout=10):
        return "testlog"

    def get_element_count(self, locators):
        return 3


class TestWebView(IWebView):
    """Mock WebView"""

    visible_rectelem_count = [0, 0, 4, 4]
    visible_rect = [0, 0, 4, 4]

    def __init__(self, typename):
        self._browser_type = typename

    @property
    def webdriver_class(self):
        return MockWebDriver

    def send_keys(self, text):
        return text

    def click(self, x_offset, y_offset):
        return True

    @property
    def browser_type(self):
        return self._browser_type

    @browser_type.setter
    def browser_type(self, type_name):
        self._browser_type = type_name

    def upload_file(self, file_path):
        return str(file_path) + " upload complete"


class TestPage(WebPage):
    def __init__(self):
        ui_map = {
            "test": {
                "type": WebElement,
                "locator": XPath("//div[@id='test']"),
                "ui_map": {
                    "close": {
                        "type": WebElement,
                        "locator": XPath("//div[@class='close']"),
                    },
                },
            }
        }
        self.view = TestWebView("testbrowser")
        super(TestPage, self).__init__(self.view, wait_for_ready=False)
        self.update_ui_map(ui_map)

    def get_webdriver(self):
        return self._webdriver

    def get_webview(self):
        return self.get_webdriver()  # TODO: remove this method


class TestElement(WebElement):
    def __init__(self, root="", locator=None):
        if locator is None:
            locator = []
        ui_map = {
            "test": {
                "type": type(self),
                "locator": XPath("//div[@id='test']"),
            }
        }
        self.view = TestWebView("testbrowser")
        self.test = TestPage()
        super(TestElement, self).__init__(self.test, "//div[@id='test']")
        self.test.get_webview().set_attribute("", "value", "test")
        self.update_ui_map(ui_map)

    def get_elements(self, locator, elem_cls=None):
        elelist = []
        for i in range(3):
            elelist.append(TestElement())
        return elelist


class FakeBrowser(IBrowser):
    def __init__(self):
        pass

    def open_url(self, url, page_cls=None, extra_params=None):
        return url

    def find_by_url(self, url, page_cls=None):
        return url


class MockHTTPRequestHandler(httpserver.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.headers["Host"] != "www.test.com":
            self.send_response(400)
            return
        content = self.path
        if not isinstance(content, bytes):
            content = content.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=UTF-8")
        self.send_header("Content-Length", len(content))
        self.end_headers()

        self.wfile.write(content)


def start_mock_http_server(port, in_thread=False):
    httpd = httpserver.HTTPServer(("127.0.0.1", port), MockHTTPRequestHandler)
    if in_thread:
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()
    else:
        httpd.serve_forever()
    return httpd
