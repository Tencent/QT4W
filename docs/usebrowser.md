## 跨端跨平台测试
### QT4W的Browser抽象
  QT4W将浏览器抽象为一个IBrowser对象，在该对象中定义了两个操作：
* 打开一个URL指定的页面open_url()
* 在打开的页面中查找和指定url匹配的页面。

在实现自己的IBrowser对象后，就可以通过该对象来操作浏览器。关于如何封装IBrowser接口参见[Browser实现][1]。
为了进一步消除，不同浏览器调用时的差异，QT4W提供了Browser类，该类继承自IBrowser。该类能够根据注册的浏览器名，获取到对应的实现实例。在QT4W中一般都通过，该类来调用具体的IBrowser实现。该类的实现，如下所示：
```python
class Browser(IBrowser):
    '''对外的浏览器类
    '''
    browser_dict = {}  # 存储浏览器类型与浏览器类的对应关系
    def __init__(self, browser_name=None):
        '''创建具体的Browser实例
        :param browser_name: 要创建的浏览器类型
        :type browser_name:
        '''
        self._browser_name = browser_name
        self._browser = self._get_browser_cls()
    
    def _get_browser_cls(self):
        '''获取浏览器类
        '''
        if not self._browser_name:
            # 随机选择浏览器
            self._browser_name = random.choice(self.browser_dict.keys())
        browser_cls_path = self.browser_dict.get(self._browser_name)
        if not browser_cls_path:
            raise TypeError('Browser %s is not registered' % self._browser_name)
        logger.info('[Browser] Current browser type is %s' % self._browser_name)
        module = __import__('.'.join(browser_cls_path.split('.')[:-1]))
        for item in browser_cls_path.split('.')[1:]:
            module = getattr(module, item)
        return module()
    
    @staticmethod
    def register_browser(browser_name, browser_cls_path):
        '''注册浏览器
        
        :param browser_name:     浏览器名称
        :type browser_name:      string
        :param browser_cls_path: 浏览器类路径
        :type browser_cls_path:  string
        '''
        Browser.browser_dict[browser_name] = browser_cls_path
        
    def open_url(self, url, page_cls=None):
        '''打开一个url，返回page_cls类的实例
        :param url: 要打开页面的url
        :type url:  string
        :param page_cls: 要返回的具体WebPage类,为None表示返回WebPage实例
        :type page_cls: Class
        '''
        return self._browser.open_url(url, page_cls)
    
    def find_by_url(self, url, page_cls=None, timeout=10):
        '''在当前打开的页面中查找指定url,返回WebPage实例，如果未找到，返回None
        :param url: 要查找的页面url
        :type url:  string
        :param page_cls: 要返回的具体WebPage类,为None表示返回WebPage实例
        :type page_cls: Class
        :param timeout: 查找超时时间，单位：秒
        :type timeout: int/float
        '''
        page = self._browser.find_by_url(url, page_cls, timeout)
        if page == None: raise RuntimeError('Can\'t find page %s in browser %s' % (url, self._browser_name))
        return page
```
register_browser方法实现了浏览器名和浏览器封装实现的对应关系，并将该对应关系以字典的形式存储在类变量browser_dict中；_get_browser_cls方法会根据browser_dict变量中的信息来返回浏览器名的对应浏览器实现的Object对象。如果初始化的时候未传入浏览器名，会随机选择一个已注册的浏览器实现。如果未注册任何浏览器则会报错。这里的隐式的要求，在实现自己的IBrowser封装时，初始化时没有必传的参数。在QT4W自动化中，推荐使用该类的实例来打开或者查找页面。
#### Browser用法示例
在获取Browser类的实例前，先需要使用Browser.register_browser注册浏览器，在注册时，传入了两个参数：浏览器名和XXBrowser类的路径。然后再初始化Browser对象时传入注册的浏览器名，获取指定的浏览器对象，使用方法如下所示：
　　
```python
#注册浏览器并获取浏览器实例
 Browser.register_browser('TestBrowser', 'BrowserPath')
 browser=Browser('TestBrowser')
 
 #打开URL
 browser.open_url(https://qtacore.github.io/qt4w/demo.html，PageClass)
```
说明: 此处注册时传入的第二个参数指示浏览器实现所在的class，此处传入的TestBrowser给出的是TestBrowser浏览器封装的实现。

### 实现WORA(Write Once Run Anywhere)示例
下面以DemoPage为示例来说说明，如何使用使用Browser类实现一份QT4W测试用例，仅需做少许修改便可以在多个端上运行。
#### Android端执行DemoPage测试
在Android端，要想使用QT4W需要QT4A的支持。在Android端我们使用QT4A中封装的系统自带的浏览器来检查Demo页面是否运行正常。因此，我们实现了如下所示的测试用例：
```python
class DemoTest(AndroidTestBase):
    '''QT4W示例测试用例
    '''
    owner = "testowner"
    timeout = 5
    priority = AndroidTestBase.EnumPriority.High
    status = AndroidTestBase.EnumStatus.Ready
    
    def pre_test(self):
        Browser.register_browser('TestBrowser', 'qt4a.browser.QT4ABrowser') 
        
    def run_test(self):
        self.startStep('1.设置信息并提交')
        browser = Browser("TestBrowser")
        page = browser.open_url('https://qtacore.github.io/qt4w/demo.html', DemoPage)
        page.set_name("qta")
        page.set_female()
        page.set_age(str(20))
        page.set_company("tencent")
        page.submit()
```
这里在pre_test中，将TestBrowser注册为QT4A中的QT4ABrowser。在具体的测试用例中，使用Browser("TestBrowser")获取到对应的浏览器实例类似执行DemoPage测试。
#### IOS端执行DemoPage测试
在IOS端，可以直接复制上述代码，然后修改一下浏览器注册部分的内容，将测试的基类改成使用IOS的测试基类即可运行。修改后如下所示：
```python
class DemoTest(iTestCase):
    '''IOS QT4W示例测试用例
    '''
    owner = "testowner"
    timeout = 5
    priority = iTestCase.EnumPriority.High
    status = iTestCase.EnumStatus.Ready
    
    def pre_test(self):
        Browser.register_browser('TestBrowser', 'qt4i.app.Safari') 
        
    def run_test(self):
        self.startStep('1.设置信息并提交')
        browser = Browser("TestBrowser")
        page = browser.open_url('https://qtacore.github.io/qt4w/demo.html', DemoPage)
        print page.url
        page.set_name("qta")
        page.set_age(str(20))
        page.set_company("tencent")
        page.set_female()
        page.submit()
```
这里仅仅是将TestBrowser重新注册为了qt4i.app.Safari,同时为了用例能够在IOS平台上顺利执行，需要将DemoTest的测试基类改为继承QT4I提供的iTestCase。即可在IOS上顺利执行。
#### 高级用法
更加方便的用法是在各端分别封装一个测试基类，并在测试基类中注册对应的浏览器。例如Android端可以封装如下测试基类，继承自Android自动化的测试基类AndroidTestBase：
```python
class BrowserTestCase(AndroidTestBase):
    '''Browser测试用例基类
    '''
    def pre_test(self):
        super(BrowserTestCases, self).pre_test()
        # 注册Android浏览器类路径
        Browser.register_browser('TestBrowser', 'qt4a.browser.QT4ABrowser')
```
IOS端同样也封装一个BrowserTestCase，继承IOS自动化的测试基类iTestCase，如下：
```python
class BrowserTestCase(iTestCase):
    '''Browser测试用例基类
    '''
    def pre_test(self):
        super(BrowserTestCases, self).pre_test()
        # 注册IOS浏览器类路径
        Browser.register_browser('TestBrowser', 'qt4i.app.Safari') 
```
经过如此封装后，Android和IOS两端的DemoPage自动化便可统一使用下面的测试用例：
```python
class DemoTest(BrowserTestCase):
    '''QT4W示例测试用例
    '''
    owner = "testowner"
    timeout = 5
    priority = BrowserTestCase.EnumPriority.High
    status = BrowserTestCase.EnumStatus.Ready
    
    def run_test(self):
        self.startStep('1.设置信息并提交')
        browser = Browser("TestBrowser")
        page = browser.open_url('https://qtacore.github.io/qt4w/demo.html', DemoPage)
        page.set_name("qta")
        page.set_female()
        page.set_age(str(20))
        page.set_company("tencent")
        page.submit()
```
在上面的示例中，在不同端上，需要手动的去修改所引入的BrowserTestCase，Android端引入Android端封装的BrowserTestCase,IOS端运行时，需要修改为IOS端的BrowserTestCase封装。如果不想所动修改的话，可以在测试用例前使用__import__方法动态引入,package.moudle指代BrowserTestCase的路径，如果两端的实现，在同一路径下，便不需做任何更改。
```python
BrowserTestCase=__import__(package.moudle)
```
跨终端的具体用例写法可以参考[QT4WDemo项目](https://github.com/qtacore/QT4WDemoProj)
### 内嵌页面如何实现WORA
内嵌页面，实际上也是一个隐形的浏览器，内嵌页面实现WORA，同样必须为内嵌页面封装IBrowser类，然后使用Browser.register_browser(),方法注册该内嵌页面的浏览器封装即可。使用方式和上面相同。如何实现IBrowser封装，Android端可以参考[QT4ABrowser][2]的实现，IOS端可以参考[Safari][3]的实现。


  [1]: extend/Browser.html
  [2]: https://github.com/Tencent/QT4A/blob/master/qt4a/browser.py
  [3]: https://github.com/Tencent/QT4i/blob/master/qt4i/app.py