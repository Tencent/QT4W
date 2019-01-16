

## Web页面标识

### 基础页面标识

　　在在QT4W中，每个页面都被表示成WebPage类，该WebPage类是实际页面的抽象。在自动化中可能被操作的元素，在该类中应该都有所标识。在封装某个页面的WebPage时，一般会直接继承QT4W的WebPage的实现，不必再关心page页面的底层接口的实现,只需关注page页面自身的操作逻辑的实现。下面以封装QT4W提供的[Demo页面][1]为例来说明如何封装自己的Webpage：
```python
class DemoPage(WebPage):
    '''Demo页面
    '''
    ui_map = {'title':{'type': WebElement,'locator': XPath('//div[@class="panel-heading"]')},
            'name':{'type': InputElement,'locator':XPath('//input[@id="name"]')},
            'female':{'type': WebElement,'locator':XPath('//input[@value="female"]')},
            'male':{'type': WebElement,'locator':XPath('//input[@value="male"]')},
            'age':{'type': SelectElement,'locator':XPath('//select[@id="age"]')},
            'company':{'type': InputElement,'locator':XPath('//input[@id="company"]')},
            'submit':{'type': WebElement,'locator':XPath('//button[@id="submit"]')},
            }
            
    #设置姓名
    def set_name(self,name):
        self.control('name').value=name
        
    #设置性别为女
    def set_female(self):
        self.control('female').click();
        
    #设置性别为男
    def set_male(self):
        self.control('male').click();
         
    #设置姓名
    def set_age(self,age):
        self.control('age').selection=age
        
    #设置公司名
    def set_company(self,company):
        self.control('company').value=company
    
    def submit(self):
        self.control("submit").click()
```
在封装WebPage主要是包括两部分内容：</br>
其一、是构建Web页面的ui_map，页面的ui_map中存放的是所有在自动化中可能操作的元素控件。至于如何封装页面控件参考*[WebElement封装][2]*，这里给出关于封装页面元素的几条建议：
1. 封装页面元素要尽可能简洁，Xpath尽可能简短。
2. 合理的使用层次结构封装，当某个控件的子控件大部分会被使用时建议层次结构封装，例如上述示例中的menu封装，即先封装父控件，在父控件的UIMap中封装子控件，这样可以减少维护成本，结构清晰。但是只用到极少的子控件时，不建议这样封装。
3. 封装控件时，除非不得已的情况下不要使用[N]来选取第N个元素。</br>
其二、封装页面相关操作，这里主要是封装一些页面内的一些简单的UI操作或者一些UI操作的集合，来完成某个常用的行为，例如这里的登录操作，搜索操作等，这里的操作只能是本页面内的。

### 内嵌页面标识

　　对于内嵌页面封装也会继承QT4W的WebPage类，同样需要封装页面ui_map的以及页面操作。只是对于内嵌页面，没有进行Browser封装，需要在WebPage初始化时传入WebView对象,因此必须要重写WebPage的__init__()方法。下面给出一个内嵌页面的封装示例：
　　
```python
class DemoEmbedPage(WebPage):
    def __init__(window):
        #获取页面的WebView对象
        webview=WebView(window)
        super(DemoEmbedPage,self).__init__(webview)
        
        ui_map={'最热':{'type':WebElement,
                        'locator':XPath('//div[@class="filter_item"]/a[@_stat="pages_index:sort_sort_最热"]')
                        },
                  }
        self.update_ui_map(ui_map)

```

### 获取WebPage对象
　　在使用浏览器打开某个页面时，可以直接返回指定的WebPage对象,如下所示：
 ```python
    #指定浏览器
    browser = Browser("Chrome")
    #打开网页，返回指定的WebPage页
    page = browser.open_url('https://qtacore.github.io/qt4w/demo.html', DemoPage)
 ```
　　这里需要指出的是，在使用Browser("browsername")获取浏览器对象时，需要先使用register_browser()注册一下，才能使用，此处注册一次即可，具体用法参见[跨端跨平台测试][3]。此外，还可以使用browser.find_by_url(url,DemoPage),用来返回指定的Page页面。对于内嵌页面的WebPage对象，和普通对象个获取方式相同，可以直接初始化出来。示例如下：
```python
page=DemoEmbedPage(window)
```
获取到Page对象后就能够对页面进行的一些列操作，这些操作大概也可以分为以下几个类型：</br>
1.基本属性的定义及操作，包括页面的URl、Title、ReadyState、cookie等;</br>
2.页面滑动操作;</br>
3.查找元素：find_element和find_elements；</br>
4.其他操作：执行JS接口（eavl_script）、激活窗口activate()以及upload_file()等。</br>
详细的操作接口参见WebPage定义*[QT4W接口文档][4]*


  [1]: https://qtacore.github.io/qt4w/demo.html
  [2]: WebElement.html
  [3]: ../usebrowser.html
  [4]: ../api/qt4w.html#module-qt4w.webcontrols