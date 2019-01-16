
## Browser实现

　　对于Web自动化而言第一步就是使用浏览器打开某个指定的URL，进入特定页面。Web自动化的第一步就是如何封装好一个Bowser。进行Browser封装一般以QT4W的IBrowser作为父类去继承，QT4W的IBrowser定义如下所示：</br>
``` python
class IBrowser(object):
    '''浏览器接口类
    '''   
    def open_url(self, url, page_cls=None):
        '''打开一个url，返回page_cls类的实例
        
        :param url: 要打开页面的url
        :type url:  string
        :param page_cls: 要返回的具体WebPage类,为None表示返回WebPage实例
        :type page_cls: Class
        '''
        raise NotImplementedError
    
    def find_by_url(self, url, page_cls=None):
        '''在当前打开的页面中查找指定url,返回page_cls类的实例，如果未找到，返回None
        
        :param url: 要查找的页面url
        :type url:  string
        :param page_cls: 要返回的具体WebPage类,为None表示返回WebPage实例
        :type page_cls: Class
        '''
        raise NotImplementedError
```
在IBrowser类中主要是定义了两个接口，一个是通过URL直接打开page页面的接口：open_url();另外一个在当前打开页面页面中查找指定URL对应的页面。在封装Browser是最重要的就是实现这两个方法。**此外值得注意的是内嵌页面可以不封装IBrowser接口**

###  示例

IBrowser封装就是在系统中驱动指定的浏览器来打开指定的页面以及在所有打开的页面中通过对比URL来查找指定的页面。这部分操作的实现和系统以及浏览器的类型是高度相关的，也就是说在不同平台的不同浏览器上有不同的实现。实现浏览器封装的前提是已经封装好了系统原声控件的操作，这部分能力由QT4X提供。下面以在windows系统上封装ChromeBrowser为例来说明如何实现自己的Browser。

#### 实现open_url方法

　　根据url打开浏览器，实现大致可以分为的三个部分：</br>
　　1.启动浏览器，并传入指定的URL并打开；</br>
　　2.根据打开的网页窗口初始化一个WebView对象；</br>
　　3.将WebView对象转换为指定类型。</br>
　　当然在不同的平台上，打开浏览器的方式有所不同，在Windows上就是用win32processAPI创建一个浏览器进程，并且将URL当做参数传入。在Windows上子进程创建成功后，会返回PId，然后需要根据PID获取窗口句柄，并且使用该句柄来WebView对象。具体实现如下所示：

```python
class ChromeBrowser(IBrowser):
    '''Chrome浏览器
    '''
    def open_url(self, url, page_cls=None):
        import win32process, win32con
        while is_port_occupied(self._port):  # 如果端口被占用，则查找下一个可用端口
            self._port += 1
        if not self._port in self._port_list:
            self._port_list.append(self._port)
        temp_dir = self._temp_dir % self._port
        #获取可执行文件位置
        exe_path = ChromeBrowser.get_browser_path()
        
        #启动浏览器参数
        params = "--remote-debugging-port=%d --disable-session-crashed-bubble --disable-translate --disable-breakpad --no-first-run --new-window --disable-desktop-notifications --user-data-dir=%s" % (self._port, temp_dir)
        cmd = ' '.join([exe_path, params, url])
        logging.debug('chrome: %s' % cmd)
        _, _, pid, _ = win32process.CreateProcess(None, cmd, None, None, 0, 0, None, None, win32process.STARTUPINFO())
        handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
        win32event.WaitForInputIdle(handle, 10000)
        self._pid = pid
        logging.info('chrome进程为%d' % pid)  # 加上此句话查看chrome是否成功打开了
        
        timeout = 10
        time0 = time.time()
        while time.time() - time0 < timeout:
            #获取指定进程的窗口句柄
            win_list = self.get_chrome_window_list(pid)
            if len(win_list) > 0: break
            time.sleep(1)
        else:
            raise RuntimeError('find chrome browser window failed')
        assert(len(win_list) == 1)
        page_wnd = win_list[0]
        #通过窗口句柄初始化WebView对象
        self._webview = ChromeWebView(page_wnd, url, self._pid, self._port)
        return self.get_page_cls(self._webview, page_cls) 
```
　　为了返回指定的page类型，需要实现一个get_page_cls，该函数的主要功能就是实现类型转换,在封装其他的Browser时，可以直接复用该方法。
```pyhton
def get_page_cls(self, webview, page_cls=None):
    if page_cls:
       return page_cls(webview)
    return webview
```
#### 实现find_by_url方法
　　find_by_url实现方法与此类似，需要搜索所有的已经打开的chrome页面，获取各个页面的URL和给定的URL进行对比，具体实现如下所示：

```python
 def find_by_url(self, url, page_cls=None, timeout=10):
        '''在当前打开的页面中查找指定url,返回WebPage实例，如果未找到，则抛出异常
        '''
        time0 = time.time()
        while time.time() - time0 < timeout:
            try:
                #搜索所有WebView
                webview = self.search_chrome_webview(url)
                break
            except RuntimeError, e:
                logging.warn('[ChromeBrowser] search chrome window failed: %s' % e)
                time.sleep(0.5)
        else:
            raise
        return self.get_page_cls(webview, page_cls)   
        
    def search_chrome_webview(self, url):
        '''根据url查找chrome对应的webview类
        returns ChromeWebView: ChromeWebView类
        '''
        import win32com.client
        from qt4c.webview.chromewebview.chromedriver import ChromeDriver
        #获取chrome可执行文件路径
        chrome_path = self.get_browser_path()
        #获取打开page列表，找到指定的url及title并进行整理
        for port in self._port_list:
            chrome_driver = ChromeDriver(port)
            title = ''
            for it in chrome_driver.get_page_list():
                if it['url'] == url or re.match(url, it['url']):
                    title = self._handle_title(it['title'])
                    url = it['url']
                    if isinstance(title, unicode): title = title.encode('utf8')
                    break
            	else: continue
            break
        else:
            raise RuntimeError('获取页面：%s 标题失败' % url)
        #获取所有windows窗口
        wmi = win32com.client.GetObject('winmgmts:')
        
        #搜索Chrome窗口
        for p in wmi.InstancesOf('win32_process'):
            if not p.CommandLine:
                continue
            if p.CommandLine.startswith(chrome_path) or p.CommandLine.startswith('"%s"' % chrome_path):
                items = p.CommandLine[len(chrome_path):].split()
                if not items or items[0].startswith('--type='): continue  # 都不是Browser进程
                chrome_window_list = self.get_chrome_window_list(p.ProcessId)
                for chrome_window in chrome_window_list:
                    win_title = chrome_window.Parent.Text
                    if win_title.endswith(' - Google Chrome'): win_title = win_title[:-16]
		            #比较页面title，返回WebView对象
                    if win_title == title:
                        win32gui.SetForegroundWindow(chrome_window.TopLevelWindow.HWnd)
                        self._webview = ChromeWebView(chrome_window, url, p.ProcessId)
                        return self._webview
                raise RuntimeError('当前标签页不在窗口最前端！')
        else:
            raise RuntimeError('%s对应的chrome进程不存在' % url)
```
　