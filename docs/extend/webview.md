## WebView实现

　　WebView是所有WebControl的底层容器，WebView也是进行Web自动化的底层窗口基础，所有的Web控件操作最终都会体现在WebView的操作上，此外，WebView的封装还会用到底层的系统窗口的一些属性。WebView的封装都需要继承QT4W中定义的IWebView基类，在该基类中定义了一些列WebView需要实现的操作：</br>
1.WebView的窗口属性;</br>
2.常见操作：点击、拖拽、鼠标hover、滑动等。</br>
3.辅助接口：Js执行、截屏、文件上传等。</br>
IWebView中具体的接口定义详见*[API文档][1]*。

### WebView示例

　　下面就以PC端Windows上的WebView封装为例来说明整个WebView封装的流程。首先，这里需要明确的是WebView本质上也是系统上的一个窗口，对于Windows系统来说，webView的底层实现是基于window窗口，所以实现webView需要封装windows的窗口及其他的系统操作。

#### 封装系统窗口

　　在封装WebView前，需要封装好系统的控件实现，提供基本的能力支持，QT4X已经实现了系统原生窗口封装、鼠标操作及键盘输入输入等。QT4C提供了Windows原声控件的封装；QT4A提供Android系统原生控件操作；QT4I提供IOS控件操作。此处的具体实现可以参考QT4X的接口文档：</br>
QT4C: *接口文档链接（暂未开源，开源后更新）*;</br>
QT4A: [接口文档链接][2];</br>
QT4I: [接口文档链接][3];</br>

#### 实现WebView功能

整个WebView功能大致可以分为三个部分：</br>
其一：WebView的属性及基本能力提供，这一部分提供的能力主要用于实现WebView自身的操控，包括获取自身的Rect属性、一些列点击操作以及输入操作.这部分实现和操作系统的窗口系统有着十分紧密的联系，故此处会用到操作系统的窗口操作API。下面给出QT4C端的windows系统上的这部分实现。
　　
```python
    @property
    def rect(self):
        '''当前可见窗口的坐标信息
        '''
        return win32gui.GetClientRect(self._window.HWnd)
    def activate(self, is_true=True):
        '''激活当前窗口
        
        :param is_true: 是否激活，默认为True
        :type  is_true: bool
        '''
        self._window.TopLevelWindow.bringForeground()
        win32gui.BringWindowToTop(self._window.TopLevelWindow.HWnd)
    def _inner_click(self, flag, click_type, x_offset, y_offset,):
        self.activate()
        new_x, new_y = win32gui.ClientToScreen(self._window.HWnd, (int(x_offset), int(y_offset)))
        if self._offscreen_win:
            new_x += self._window.BoundingRect.Left - self._offscreen_win.BoundingRect.Left
            new_y += self._window.BoundingRect.Top - self._offscreen_win.BoundingRect.Top
        Mouse.click(new_x, new_y, flag, click_type)
        
    def click(self, x_offset, y_offset):        
        self._inner_click(MouseFlag.LeftButton, MouseClickType.SingleClick, x_offset, y_offset)
        
    def double_click(self, x_offset, y_offset):
        self._inner_click(MouseFlag.LeftButton, MouseClickType.DoubleClick, x_offset, y_offset)
    
    def right_click(self, x_offset, y_offset):
        self._inner_click(MouseFlag.RightButton, MouseClickType.SingleClick, x_offset, y_offset)
    
    def long_click(self, x_offset, y_offset, duration=1):
        raise NotImplementedError
        
    def hover(self, x_offset, y_offset):
        self.activate()
        new_x, new_y = win32gui.ClientToScreen(self._window.HWnd, (int(x_offset), int(y_offset)))
        if self._offscreen_win:
            new_x += self._window.BoundingRect.Left - self._offscreen_win.BoundingRect.Left
            new_y += self._window.BoundingRect.Top - self._offscreen_win.BoundingRect.Top
        Mouse.move(new_x, new_y)
    
    def scroll(self, backward=True):
        self._window.scroll(backward)
        
    def send_keys(self, keys):
        self._window.sendKeys(keys)     
```
说明：这里使用了经过Python封装的WIN32API来获取Windows窗口操作能力，WebView在WindowsPC上本质就是一个Window,在WebView初始化时会传入，一直指代其自身的窗口句柄self._window。这部分的接口实现就是使用经过Python封装的windowsAPI来对这个窗口进行一些列操作。此处封装较为简单，主要就是对系统API在封装。对于PC端来说，没有长按这个操作，故long_click()可以不用实现，此处可以不重写，但是如果重写该方法，就需要raise NotImplmentError，以便告知用户该功能未实现。</br>
　　
其二：实现eval_script()接口，提供注入JS脚本的能力，此处具体实现在不同的浏览器上有所差异，执行JS代码是浏览器内核所具备的能力，因此此处需要实现浏览器驱动来执行JS脚本。因此这里需要对不同浏览器内核通信方案比较熟悉，才能很好地实现该方法。下面给出一个封装IE浏览器内核驱动的示例，windows上是通过windows消息机制来建立和浏览器的通信机制，根据提frameID来获取指定的HTMLWindow，具体实现如下：</br>

```python
class IEDriver(object):
    '''window['qt4w_driver_lib']
    '''
    def __init__(self, ie_server_hwnd):
        self._hwnd = ie_server_hwnd
        self._init_com_obj()
        
    def _init_com_obj(self):
        '''初始化com对象
        '''
        if hasattr(self, '_doc'): logging.debug('[IEDriver] re_init com_obj')
        else: time.sleep(2)  # 部分IE10上发现打开页面时不sleep会导致拒绝访问错误
        msg = win32gui.RegisterWindowMessage('WM_HTML_GETOBJECT')
        for _ in range(3):
            try:
                ret, result = win32gui.SendMessageTimeout(self._hwnd, msg, 0, 0, win32con.SMTO_ABORTIFHUNG, 2000)
                ob = pythoncom.ObjectFromLresult(result, pythoncom.IID_IDispatch, 0)
                self._doc = win32com.client.dynamic.Dispatch(ob)
                self._win = self._doc.parentWindow
                break
            except AttributeError, e:
                # 页面跳转时易发生此问题
                logging.debug(str(e))
                time.sleep(0.5)
        else:
            raise RuntimeError('初始化COM对象失败')
       
    def _check_valid(self):
        '''检查com对象的有效性
        '''
        try:
            self._doc._oleobj_.GetIDsOfNames('readyState')
            return True
        except pywintypes.com_error, e:
            if (e.args[0] % 0x100000000) == 0x80070005:
                self._init_com_obj()  # 重新初始化
                return False
            raise e
     
    def eval_script(self, frame_win, script, use_eval=True):
        '''
        IE10以上异常对象才有stack属性
        '''
        logging.debug('[IEDriver] eval script: %s' % script[:200].strip())
        if not isinstance(script, unicode):
            script = script.decode('utf8')  # 必须使用unicode编码
            
        if use_eval:
            script = script.replace('\\', r'\\')
            script = script.replace('"', r'\"')
            script = script.replace('\r', r'\r')
            script = script.replace('\n', r'\n')
            script = r'''document.script_result = (function(){
                try{
                    var result = eval("%s");
                    if(result != undefined){
                        return 'S'+result.toString();
                    }else{
                        return 'Sundefined';
                    }
                }catch(e){
                    var retVal = 'E['+e.name + ']' + e.message;//toString()
                    if(e.stack) retVal += '\n' + e.stack;
                    else{
                        var f = arguments.callee.caller;
                        while (f) {
                            retVal += f.name;
                            f = f.caller;
                        }
                    }
                    return retVal;
                }
            })();''' % script  
        self._check_valid()
        
        if frame_win == None:
            frame_win = self._win
            frame_doc = self._doc
        else:
            frame_doc = frame_win.document
        self._retry_for_access_denied(lambda: frame_win.execScript(script))
        if not use_eval: return
        if not self._check_valid(): return  # 一般是页面发生跳转，此时无法获取到直接结果
        name_id = frame_doc._oleobj_.GetIDsOfNames('script_result')
        result = frame_doc._oleobj_.Invoke(name_id, 0, pythoncom.DISPATCH_PROPERTYGET, True)
        if result == '': raise IEDriverError('JavaScript返回为空')
        if isinstance(result, unicode):
            result = result.encode('utf8')
        logging.debug('[IEDriver] result: %s' % result[:200].strip())
        return result
```
说明：IEDriver初始化时通过调用_init_com_obj函数获取到IHTMLDocument2的com对象，然后通过获取该对象的ParentWindow,调用IE浏览器的Window.exceScript()来执行JS脚本，并直返回JS代码的执行结果。各个浏览器的执行JS方法实现有所差别，因此这里应该根据浏览器的实现原理采用不同实现。</br>

其三：获取页面内的属性及dom结构的操作能力的封装，在QT4W中这部分能力由WebDriver进行实现，但是在WebView中定义一个__getattr__方法来获取WebDriver的能力。WebDriver的具体能力详情见*[WEbDriver封装][4]*。</br>
```python
 def __getattr__(self, attr):
        '''转发给WebDriver实现
        '''
        return getattr(self._webdriver, attr)
```
此外，在WebView进行初始化会传递一些参数，下面看一个具体的WebView初始化实例：
```python
class IEWebView(WebViewBase):
    '''IE WebView实现
    '''
    def __init__(self, ie_window_or_hwnd):
        '''初始化
        
        :params ie_window_or_hwnd: ie窗口或句柄
        :type ie_window_or_hwnd: Control or int
        '''
        if isinstance(ie_window_or_hwnd, int):  # 句柄需要转化为对应的窗口，句柄是IEFrame的句柄
            process_id = win32process.GetWindowThreadProcessId(ie_window_or_hwnd)[1]
            from browser.ie import IEWindow_QT4W
            ie_window = IEWindow_QT4W(process_id).ie_window
        else:
            ie_window = ie_window_or_hwnd
            
        from qt4w.webdriver import iewebdriver
        self._webdriver = iewebdriver.IEWebDriver(self)
        self._browser_type = 'ie'
        self._ie_window = ie_window
        self._driver = IEDriver(self._ie_window.HWnd)
        super(IEWebView, self).__init__(ie_window, self._webdriver)
       

 class WebViewBase(IWebView):
    '''PC端WebView基类
    '''
    def __init__(self, window, webdriver, offscreen_win=None):
        self._window = window
        self._offscreen_win = offscreen_win
        self._webdriver = webdriver
        self._parent_wnd = win32gui.GetParent(self._window.HWnd)
        # 如果获取的父窗口是空
        if self._parent_wnd == 0:
            self._parent_wnd = self._window.HWnd
        self._browser_type = 'not defined'
```
 　　这里需要着重理解的就是self._driver和Self._webDriver这两者之间的区别，self._driver可以看成是浏览器执行JS内核的一个代理，负责执行传入的JS代码及返回结果，其具体实现和浏览器高度相关。self._webdriver是QT4W定义的负责解析dom结构的功能集合。此外，这里建议根据系统类型来实现对应的WebViewBase来封装窗口相关操作，然后再根据不同浏览器封装XX(browsername)WebView实现执行JS能力。


  [1]: ../api/qt4w.webview.html#module-qt4w.webview.webview
  [2]: https://qt4a.readthedocs.io/zh_CN/latest/apiref.html
  [3]: https://qt4i.readthedocs.io/zh_CN/latest/apiref.html
  [4]: WebDriver.html