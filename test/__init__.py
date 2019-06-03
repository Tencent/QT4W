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

'''QT4W单元测试
'''

import unittest
import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(test_dir))
def main():
    runner = unittest.TextTestRunner(verbosity=10 + sys.argv.count('-v'))
    suite = unittest.TestLoader().discover(test_dir,  pattern='test_*.py')
    raise SystemExit(not runner.run(suite).wasSuccessful())


if __name__ == '__main__':
    main()
# if __name__ == '__main__':
#     test=TestElement()
#     print test.control("test").attributes["value"]
# test=TestWebView("TestWebview")
#     print testvisible_rect
#     print test.browser_type
#     print test.upload_file("/root/test.py")
#     print test.read_console_log()
#     print test.eval_script('//dic[@id="test"]',"location.href")
#     test=TestPage()
#     print test.control("test.close")._locators[0]
