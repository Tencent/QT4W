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

'''util模块单元测试
'''

import unittest

from qt4w import util


class EnumKeyCodeTestCase(unittest.TestCase):

    def test_parse(self):
        result = util.EnumKeyCode.parse('123{ENTER}XXX')
        self.assertEqual(result, ['123', util.KeyCode('Enter', 13), 'XXX'])
        result = util.EnumKeyCode.parse('123{YYY}XXX')
        self.assertEqual(result, '123{YYY}XXX')
        result = util.EnumKeyCode.parse('123{YYYXXX')
        self.assertEqual(result, '123{YYYXXX')
        result = util.EnumKeyCode.parse('123{x{ENTER}XXX')
        self.assertEqual(result, ['123{x', util.KeyCode('Enter', 13), 'XXX'])
        result = util.EnumKeyCode.parse('123{CTRL}XXX')
        self.assertEqual(result, ['123', util.KeyCode('Control', 17), ('KeyX', 88), 'XX'])


class DeprecatedTestCase(unittest.TestCase):

    class Test(object):
        def new_func(self):
            pass

        @util.Deprecated('new_func')
        def func(self):
            pass

    def test_call(self):
        self.Test().func()


if __name__ == '__main__':
    unittest.main()
