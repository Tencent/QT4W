
# QT4W简介

QT4W (Quick Test for Web) 是QTA自动化体系内实现支持Web自动化测试能力的支持库，是QTA的Android、iOS、Windows和Mac自动化测试中实现Web自动化测试能力的基础。

## 原生和Web控件的关系

要理解QT4W和QTA其他的针对原生控件的QT4x（x表示i/A/C/Mac等）的关系，可以先了解一下原生控件和Web控件的关系。

```
+-------------------------------+
|                               |
|  +-------------------------+  |                     +-------------------------+
|  |                         |  |                     |  +------------+         |
|  |                         |  |                     |  |            |         |
|  |                         |  |                     |  |  Element   |         |
|  |                         |  |                     |  |            |         |
|  |                         |  |                     |  +------------+         |
|  |                         |  |                     |  +------------+         |
|  |                         |  |                     |  |            |         |
|  |                         |  |                     |  |  Element   |         |
|  |                         <------------------------>  |            |         |
|  |                         |  |                     |  +------------+         |
|  |                         |  |                     |                         |
|  |                         |  |                     |                         |
|  |                         |  |                     |                         |
|  |                         |  |                     |                         |
|  |                         |  |                     |                         |
|  |                         |  |                     |                         |
|  |                         |  |                     |                         |
|  +-------------------------+  |                     +-------------------------+
|       Web View Control        |                             Web Page
|                               |
|                               |
+-------------------------------+
         Native Window



       Layers of Native                                     Layers of Web



```

如上图所示，我们可以理解为，所有的网页（Web Page）都是在原生控件提供的一个Web View的基础上实现的。

## 统一的Web控件接口

参考原生控件和Web控件的关系，QT4W也设计了类似的Web控件使用接口：

```python
from qt4w.webcontrols import WebPage

wv = SomeNativeWebView()
page = WebPage(wx)
page.controls("XXX").click()
```

无论是哪个操作或终端的UI自动化的Web自动化部分，QTA都是统一使用以上模式的接口的，因此，QT4W提供的第一个功能，就是在QTA的自动化测试工具体系中，提供统一的Web控件识别和操作的接口，关于这块的更多内容，请参考《[Web控件识别和操作][1]》。

## Write Once Run Anywhere

在很多情况下，Web实现的页面，是保持在跨端跨平台上一致的，很多时候也是在一份相同的代码实现的，这个是Web本身的魅力之一。因此，在这种情况下，针对跨平台跨端的Web界面，测试自动化本身也是可以做到一份测试脚本，同时在不同终端和平台上执行，实现Write Once Run Anywhere，这样可以大大的降低测试自动化的维护的成本。为了达到这样的效果，除了统一的Web控件操作接口外，QT4W还提供了统一的Webview实例化框架，也就是Browser框架，更多的详情请参考《[跨端跨平台测试][2]》。

## 可扩展性

在各个QT4x的支持下，QT4W目前支持多种操作系统下，不同浏览器内核和混合客户端的Web自动化。目前支持的情况如下：

| WebView | 平台或操作系统 | 说明 | 相关实现代码 |
| -- | -- | -- |  -- |
| IE | Windows |  IE浏览器和内嵌页面使用，支持IE 7～11|  由QT4C提供 | 
| Chrome | Windows | Chrome浏览器和内嵌页面使用 |  由QT4C提供 | 
| TBS | Windows | QQ浏览器和相关内嵌页面使用 |  由QT4C提供 | 
| CEF |  Windows  | Chromium内嵌页面使用 | 由QT4C提供 | 
| Chrome | Linux |  Linux下的Headless模式的Chrome浏览器使用 | 由chrome-headless-browser提供|
| AndroidBuildin | Android  | Android系统内置浏览器和内嵌页面使用 | 由[QT4A](https://github.com/Tencent/QT4A/blob/master/qt4a/andrcontrols.py)提供| 
| X5 | Android | QQ移动浏览器和X5内核内嵌页面使用 | 由[QT4A](https://github.com/Tencent/QT4A/blob/master/qt4a/andrcontrols.py)提供| 
| XWalk | Android | XWalk内核内嵌页面使用 | 由[AndroidWXMPLib](https://github.com/qtacore/AndroidWXMPLib/blob/master/wxmplib/util.py)提供| 
| iOSBuildin | iOS | iOS系统内置浏览器和内嵌页面使用 | 由[QT4i](https://github.com/Tencent/QT4i/tree/master/qt4i/driver/web)提供| 
| 微信小程序/微信H5 | Android微信 | 微信小程序或者微信内部的H5页面使用 |  由[AndroidWXMPLib](https://github.com/qtacore/AndroidWXMPLib/)提供| 
| Chrome | MacOS | Mac OS下的Chrome浏览器和内嵌页面使用 | 由QT4Mac提供 |

QT4W也支持用户自定义扩展来支持更多的兼容性。更多信息请查阅《[扩展QT4W][3]》章节。


  [1]: usage.html
  [2]: usebrowser.html
  [3]: extend.html