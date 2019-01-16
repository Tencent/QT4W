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
'''Web自动化测试基础库
'''



class XPath(str):
    '''表示XPath'''
    # 2012-02-14    beyondli    创建
    def __init__(self, obj):
        str.__init__(self)
        self._obj = obj
        self._censored = None

    def __str__(self):
        if not self._obj:
            return ""
        obj = self._obj
        if not obj.strip("(").startswith("/"):
            if "#" in obj:
                pos = obj.find("#")
                nodename = obj[:pos] or "*"
                nodeid = obj[pos + 1:]
                t = nodename + nodeid
                if not nodeid or '"' in t or "'" in t:
                    obj = "/" + obj
                else:
                    obj = "//%s[@id='%s']" % (nodename, nodeid)
            else:
                obj = "/" + obj
            self._obj = obj

        return str(obj)

    def __repr__(self):
        return repr(str(self))

    @property
    def Axis(self):
        axis = None
        pos = self._censor().strip("/").find("::")
        if pos > 0:
            axis = self.strip("/")[:pos]
        return axis

    @property
    def Nodetest(self):
        p1 = self._censor().strip("/").rfind("::")
        if p1 < 0:
            p1 = self._censor().strip("/").rfind("/")
        if p1 < 0:
            p1 = 0
        p2 = self._censor().strip("/").find("[", p1)
        if p2 < 0:
            p2 = len(self._censor().strip("/"))
        nodetest = self._censor().strip("/")[p1 + 1:p2]
        # print nodetest
        return nodetest

    def break_steps(self):
        ret = []
        p1 = 0
        p2 = 0
        p3 = 0
        s = str(self)
        t = self._censor()
        while True:
            if s[p1] == "(":
                p2 = p1
                while p2 >= 0:
                    p2 = t.find(")", p2 + 1)
                    if t.count("(", p1 + 1, p2) == t.count(")", p1 + 1, p2):
                        break
            else:
                p2 = p1 + 2
            p3 = t.find("/", p2)
            if p3 < 0:
                break
            if s[p3 - 1] == "(":
                p3 = p3 - 1
            ret.append(XPath(s[p1:p3]))
            p1 = p3
        ret.append(XPath(s[p1:]))
        return ret

    def break_frames(self):
        steps = self.break_steps()
        ret = []
        frame = ""
        for step in steps:
            frame += step
            if step.Nodetest.lower() in ["iframe", "frame"]:
                ret.append(XPath(frame))
                frame = ""
        if frame:
            ret.append(XPath(frame))
        return ret
    
    def _censor(self):
        if self._censored is not None:
            return self._censored
        ret = str(self)
        p3 = 0
        while p3 >= 0:
            p1 = ret.find("'", p3 + 1)
            p2 = ret.find('"', p3 + 1)
            if p1 < 0 and p2 < 0:
                break
            if p2 < 0 or 0 <= p1 < p2:
                p3 = ret.find("'", p1 + 1)
                if p3 < 0:
                    break
                ret = ret[:p1 + 1] + '"' * (p3 - p1 - 1) + ret[p3:]
            elif p1 < 0 or 0 <= p2 < p1:
                p3 = ret.find('"', p2 + 1)
                if p3 < 0:
                    break
                ret = ret[:p2 + 1] + "'" * (p3 - p2 - 1) + ret[p3:]
        self._censored = ret
        return ret

def set_logger(logger):
    '''set qt4w default logger
    '''
    import qt4w.util
    util.logger = logger