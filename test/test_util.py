# -*- coding: UTF-8 -*-
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

"""util模块单元测试
"""

from __future__ import absolute_import

import inspect
import random
import socket
import threading
import unittest
import six

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

from qt4w import util

from test.util import start_mock_http_server


class EnumKeyCodeTestCase(unittest.TestCase):
    def test_parse(self):
        result = util.EnumKeyCode.parse("123{ENTER}XXX")
        self.assertEqual(result, ["123", util.KeyCode("Enter", 13), "XXX"])
        result = util.EnumKeyCode.parse("123{YYY}XXX")
        self.assertEqual(result, "123{YYY}XXX")
        result = util.EnumKeyCode.parse("123{YYYXXX")
        self.assertEqual(result, "123{YYYXXX")
        result = util.EnumKeyCode.parse("123{x{ENTER}XXX")
        self.assertEqual(result, ["123{x", util.KeyCode("Enter", 13), "XXX"])
        result = util.EnumKeyCode.parse("123{CTRL}XXX")
        self.assertEqual(
            result, ["123", util.KeyCode("Control", 17), ("KeyX", 88), "XX"]
        )


class DeprecatedTestCase(unittest.TestCase):
    class Test(object):
        def new_func(self):
            pass

        @util.Deprecated("new_func")
        def func(self):
            pass

    def test_call(self):
        self.Test().func()


class ProxyServerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proxy_port = random.randint(10000, 65000)
        print("proxy port is %d" % cls.proxy_port)
        cls.proxy_server = util.ProxyServer(cls.proxy_port)
        cls.proxy_server.start_in_thread()
        cls.server_port = random.randint(10000, 65000)
        print("http server port is %d" % cls.server_port)
        cls.httpd = start_mock_http_server(cls.server_port, True)

    @classmethod
    def tearDownClass(cls):
        cls.proxy_server.stop()
        cls.httpd.shutdown()

    # def test_http(self):
    #     util.HostsManager().add_host('www.test.com', '127.0.0.1')
    #     proxy_addr = 'http://127.0.0.1:%d' % self.proxy_port
    #     proxy = urllib2.ProxyHandler({"http" : proxy_addr})
    #     opener = urllib2.build_opener(proxy)
    #     urllib2.install_opener(opener)
    #     url = 'http://www.test.com:%d/qt4w/?id=123' % self.server_port
    #     request = urllib2.Request(url)
    #     response = urllib2.urlopen(request)
    #     self.assertEqual(response.code, 200)
    #     body = response.read()
    #     self.assertEqual(body, b'/qt4w/?id=123')

    def test_https(self):
        util.HostsManager().add_host("www.test.com", "127.0.0.1")
        s = socket.socket()
        s.connect(("127.0.0.1", self.proxy_port))
        buffer = "CONNECT www.test.com:%d HTTP/1.1\r\nhost: www.test.com:%d\r\n\r\n" % (
            self.server_port,
            self.server_port,
        )
        if not isinstance(buffer, bytes):
            buffer = buffer.encode()
        s.send(buffer)
        buffer = s.recv(4096)
        first_line = buffer.splitlines()[0]
        status_code = int(first_line.split()[1])
        self.assertEqual(status_code, 200)
        s.send(b"GET / HTTP/1.1\r\nHost: www.test.com\r\n\r\n")
        buffer = s.recv(4096)
        first_line = buffer.splitlines()[0]
        status_code = int(first_line.split()[1])
        self.assertEqual(status_code, 200)


def test_Singleton():

    @six.add_metaclass(util.Singleton)
    class A(object):

        def __init__(self):
            if not hasattr(self, "_obj"):
                self._obj = 0
            else:
                raise RuntimeError("Duplicated init")

    a1 = A()
    a2 = A()
    assert a1 == a2
    assert isinstance(A, type)
    assert issubclass(A, object)


if __name__ == "__main__":
    unittest.main()
