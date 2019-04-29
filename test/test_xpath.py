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
import mock
from qt4w import XPath

class TestXPath(unittest.TestCase):

    def test_node(self):
        xp=XPath('//div[@id="google_shimpl"]')
        self.assertEqual("div", xp.Nodetest);
        xp = XPath('//div[@id="google_shimpl"]//div[text()="test"]')
        self.assertEqual("div", xp.Nodetest);


    def test_break_step(self):
        xp = XPath('//div[@id="google_shimpl"]//div[text()="test"]')
        steps=xp.break_steps()
        self.assertEqual('//div[@id="google_shimpl"]', steps[0]);
        self.assertEqual('//div[text()="test"]', steps[1]);

    def test_break_frame(self):
         xp = XPath('//div[@id="google_shimpl"]//div[text()="test"]')
         steps = xp.break_frames()
         self.assertEqual('//div[@id="google_shimpl"]//div[text()="test"]', steps[0]);
         xp = XPath('//iframe[@id="google_shimpl"]//div[text()="test"]')
         steps = xp.break_frames()
         self.assertEqual('//iframe[@id="google_shimpl"]', steps[0]);
         xp = XPath('(//iframe[@id="google_shimpl"])//div[text()="test"]')
         steps = xp.break_frames()
         self.assertEqual('(//iframe[@id="google_shimpl"])', steps[0]);
         xp = XPath('//frame[@id="main"]//iframe[@id="mainwindow"]//I[@class="spr nav1"]')
         steps = xp.break_frames()
         self.assertEqual('//frame[@id="main"]', steps[0]);

if __name__ == '__main__':
    unittest.main()