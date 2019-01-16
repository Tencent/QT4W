## WebDriver实现
　　WebDriver是QT4W定义的用于解析Dom结构的中间层，根据输入的Xpath来定位的HTML控件，并操作其属性。在WebDriver初始化的时候，需要传入一个WebView对象，并且通过该对象来实现eval_script()方法。其他获取或者设置元素属性的方法实现依赖于eval_script()方法。WebDriver的具体实现会继承IWebDriver，并实现其中定义的方法。IWebDriver定义见*[API文档][1]*。</br>

在QT4W中实现了WebDriverBase类，实现了IWebDriver的接口。正如上面所言，接口中的很多方法都是通过JS方法实现的。在WebDriverBase中，我们顶一个成员变量driver_script,该成员变量中存放的是已经写好的JS方法。通过注入执行这些JS方法，来获取Dom操作能力。具体的WebDriverBase实现可以查看*[接口文档][2]*。</br>

在实现自己的WebDriver时可以直接继承WebDriverBase类。这里需要指出的是，由于这里涉及的JS代码以及Xpath的解析工作，在不同的浏览器上此处的实现可能会有所差异，很多时候需要重写一下eval_script方法，这里就说明一下如何来实现Driver中的eval_script方法，实现如下所示：
　　
```pyhton
    def eval_script(self, frame_xpaths, script):
        '''在指定frame中执行JavaScript，并返回执行结果（该实现需要处理js基础库未注入情况的处理）
        :param frame_xpaths: frame元素的XPATH路径，如果是顶层页面，怎传入“[]”
        :type frame_xpaths:  list
        :param script:       要执行的JavaScript语句
        :type script:        string
        '''
        from qt4w.util import JavaScriptError, ControlNotFoundError, ControlAmbiguousError
        try:
            return self._webview.eval_script(frame_xpaths, script)
        except JavaScriptError, e:
            err_msg = e.message
            err_msg = err_msg.split('\n')[0]  # 错误堆栈信息可能会有影响
            
            if isinstance(err_msg, unicode): err_msg = err_msg.encode('utf8')
            if ('ReferenceError' in err_msg or 'TypeError' in err_msg) and 'qt4w_driver_lib' in err_msg:
                # ie8 TypeError ie9 ReferenceError
                # 注入js基础库
                self.eval_script(e.frame, self.driver_script)
                # 再次执行待指定的JS代码
                return self.eval_script(frame_xpaths, script)
            elif 'Find element' in err_msg and 'failed' in err_msg:
                # 未找到元素
                raise ControlNotFoundError(err_msg)
            elif 'Find' in err_msg and 'elements match' in err_msg:
                #找到多个元素
                err_msg += self._get_dom_tree(frame_xpaths)
                raise ControlAmbiguousError(err_msg)
            else:
                raise e
```
　　在此处eval_script实现中采用后置结构，首先治理直接调用WebView.eval_script()执行传入的JS代码，如果执行失败后，通过获取的Error信息，来判断错误原因。如果是因为引入qt4w_driver_lib错误，就先注入JS代码库，然后在执行需要执行的JS脚本。在重写该方法时，推荐采用类似的方法。


  [1]: ../api/qt4w.webdriver.html#module-qt4w.webdriver.webdriver
  [2]: ../api/qt4w.webdriver.html#module-qt4w.webdriver.webdriver