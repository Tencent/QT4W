
## QT4W

QT4W (Quick Test for Web) is a QTA test automation driver for Web.

### Features
* Android platform: support web automated testing based on webkit, X5 (used with QT4A), please refer to [QT4A][1]. 
* IOS platform: Support Web automation testing for embedded pages of IOS applications and browser applications (used with QT4I),Please refer to [QT4I][2].
* Windows platform: Supports web automation based on Chrome, IE kernel (used with QT4C), 
Now QT4C is in the open source process.

QT4W consists of three modules: WebView, webDriver, and WebControl module.

### WebView
WebView is an abstraction of the browser window, which is a re-encapsulation of the native control. QT4W only defines the relevant interface of WebView, but does not give a concrete implementation. QT4X provides some implementations of WebView on each side. For example, QT4C provides implementations such as IeWebView and ChromeWebView.

### WebDriver
WebDriver is the driver layer of web automation. This module is mainly used to handle Dom structure related operations, such as finding web elements. Driver implementations based on Webkit and Chrome kernel are available in QT4W.

### WebControl
The WebControl module defines the WebElement and WebPage interfaces and provides implementations. In addition, QT4W also encapsulates other common web elements that are used to encapsulate pages for web automation.Webelement and WebPage usage refer to usage documentation。

### link
* Usage Document
* Design Document
------------------------------
 QT4W(Quick Test for Web)是QTA测试体系中的一环，主要用于Web自动化测试。
### 支持多种平台的Web自动化
* Android平台：支持基于webkit，X5等内核Web自动化测试（和QT4A一起使用）请参考QT4A相关文档
* IOS平台：支持IOS应用的内嵌页面及浏览器应用的Web自动化测试（和QT4I一起使用）请参考QT4I相关文档
* Windows平台：支持基于Chrome，IE内核的Web自动化测试（和QT4C一起使用），目前QT4C正在开源流程中。

QT4W是QTA测试体系中Web自动化测试的基础， 包含三个模块：WebView、webDriver以及WebControl模块。 

### WebView
WebView是对浏览器窗口的抽象，是对原生控件的再次封装。QT4W只是定义了WebView的相关接口，并未给出具体实现。QT4X各端提供了部分WebView的实现，例如QT4C中提供IeWebView、ChromeWebView等实现.关于如何封装自己的webView，请参考[WebView封装文档][3]。


### WebDriver
WebDriver是web自动化中驱动层的封装，该模块主要用来处理Dom结构相关操作，例如查找web元素等。QT4W中提供了基于Webkit和Chrome内核的WebDriver封装。如何封装其他内核的WebDriver请参考[WebDriver封装文档][4]。


### WebControl
WebControl模块定义WebElement以及WebPage的接口，并且给出了相关实现。此外，QT4W还封装了其他的常用Web元素，使用该模块来封装Web自动化时的页面。Webelement及WebPage的使用参考[使用文档][5]。

### 链接

* [使用文档](http://file.sng.com/browse/qta/htdocs/qt4w/lastest/index.html)
* [设计文档](https://git.code.oa.com/QT4W/QT4W/blob/master/design.md)


  [1]: https://github.com/Tencent/QT4A
  [2]: https://github.com/Tencent/QT4i
  [3]: http://file.sng.com/browse/qta/htdocs/qt4w/testdoc/webview.html
  [4]: http://file.sng.com/browse/qta/htdocs/qt4w/testdoc/WebDriver.html
  [5]: http://file.sng.com/browse/qta/htdocs/qt4w/testdoc/usage.html