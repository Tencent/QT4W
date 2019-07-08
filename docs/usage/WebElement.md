
## Web控件标识

　　Web控件是Web页面的基础,QT4W在WebElement类中封装常见的控件操作，一般情况下，我们可以使用Webelement来表示绝大部分的Web控件。对于一些比较特殊的控件，可以在WebElement的基础上在进行封装。QT4W还提供了FrameElement、inputElement以及SelectElement的实现。FrameElement对应Frame控件；InputElement用于输入控件，selectElement用于选择类型的控件。

###  基础控件标识
下面详细说明如何在Web自动化中使用WebElement来封装Web控件，下面以一个实例来说明如何对Web控件进行封装。
```python
'controlname':{'type': WebElement,
              'locator': XPath('//div[@id="controlid"]'),
              }
```
封装一个Web控件首先需要定义一个控件名，此控件名会作为控件的唯一标志，后续使用到该控件时会通过该控件名来调用该控件。在封装控件时，一般会传入两个参数type和locator,type用来指示控件的类型，locator用于传递控件的Xpath，此处的Xpath采用标准的xpath写法，具体xpath标准参考*[xpath标准][2]*。</br>
关于如何查找控件的Xpath路径，各个端有不同的方法，PC端可以直接在浏览器进入调试模式，查找控件xpath;在移动端，这里我们推荐使用QT4X提供的UISPY定位控件XPath。关于控件xpath，建议尽可能使用id来进行定位，在没有id的情况下，尽量使用具有唯一性的属性来定位控件，尽量不要使用[index]下标来定位控件。此外这里Xpath应该能保证能够定位到唯一的控件，否则会报ControlAmbiguousError；在Xpath无法定位控件时，报ControlNotFoundError错误。</br>
 在默认情况下，可以不用指定type类型，默认的type类型为WebElement，此时控件可以直接如此封装：
```python
'controlname':'locator': XPath('//div[@id="controlid"]')
```
### 容器类控件标识
　　所谓容器类控件是指该控件本身还包含一些子控件，常见的容器控件有列表型控件等，下面以右键菜单为例来说明如何封装容器类控件：
```python
'右键菜单':{'type': WebElement,
            'locator': XPath('//div[@class="table-menu"]'),
            'ui_map': {'剪切':{'type': WebElement,
                                'locator': XPath('//div[@id="cut"]'),
                                },
                       '复制':{'type': WebElement,
                                'locator': XPath('//div[@id="copy"]'),
                               },
                       '粘贴':{'type': WebElement,
                                'locator': XPath('//div[@id="paste"]'),
                               },
                                  
                        }
            }
```
　　容器类型的控件时，和普通控件相比就是多了一个ui_map属性，在该属性中封装子控件，子控件的封装和基础控件类似，只是此时需要注意的是子控件的locator中的Xpath应该是以父控件为基础的，也就是说子控件的locator实际上应该是父控件的locator加上自身的locator。

### ui_list封装控件
　　在某些时候，有些控件的子控件是非常相似的，XPath路径业极其相似，如果直接使用容器进行封装会导致控件的ui_map中子控件的封装类似，而且容易出错。常见的这类型控件有：颜色选择器，字号设置等等控件。对于此类控件，推荐直接使用ui_list进行封装：
　　
```python
from qt4w.webcontrols import  ui_list
'colorpick':{'type':ui_list(WebElement),          
             'locator': ('//div[@class="colorPicker-swatch"]'),
             },
```
　　在使用ui_list封装控件时，需要直接在控件的type字段直接指定为ui_list(CalssType),在使用前需要从qt4w.webcontrols中引入该方法。ui_list会返回一个ClassTypeUIList的迭代器类，如上会生成WebElementUIList类，该类继承自UIListBase。此处的locator应该是可以定位到多个控件的。

### Frame内部控件封装 
在某些情况下，页面中可能有内嵌frame，直接按照上面的写法来写Frame/Iframe内部的控件，可能会报“ControlNotFoundError”错误。QT4W的实现中frame和控件是分开查找的，在一般搜索控件时，我们会直接在默认的页面下查找，不会查找内嵌Frame里的控件。因此对于frame的内部控件描述，可以参考以下实现：
```python
from qt4w.webcontrols import FrameElement
'framename':{
              'type': FrameElement, 'locator':XPath('//iframe[@id="frameid"]'),
              'ui_map':{
                  '帐号': XPath('//input[@class="inputstyle" and @type="text"]'),
                  '密码': XPath('//input[@class="inputstyle password" and @type="password"]'),)
               }
            }
```
封装Frame内部控件时，需要先描述frame控件，然后再Frame控件的ui_map里描述其内部控件。


### 获取Web控件对象

　　一般情况下控件都是在WebPage页面类进行封装，如果想操作该控件可以使用control方法来获取控件对象，示例如下：
```python
webpage.control('controlname')
```
　　如果想要获取容器类的子控件需要用父控件的名字加上子控件的名字，中间用"."进行连接，示例如下：
```python
webpage.control("右键菜单.剪切")
```
　　对于使用ui_list封装的控件，因为返回的是一个迭代器，需要通过循环来获取满足指定条件的子控件，示例如下：
```python
for item in self.control("colorpick"):
    if iscondition(item):
        return item
    return None
```
获取到控件对象后，就可以对该控件进行一些系列操作，具体的操作接口参见*[WebElement接口文档][1]*。</br>



  [1]: ../api/qt4w.html#module-qt4w.webcontrols
  [2]: https://www.w3schools.com/xml/xpath_intro.asp