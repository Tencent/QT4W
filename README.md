
## QT4W

[![Build Status](https://travis-ci.org/Tencent/QT4W.svg?branch=master)](https://travis-ci.org/Tencent/QT4W)
[![Documentation Status](https://readthedocs.org/projects/qt4w/badge/?version=latest)](https://qt4w.readthedocs.io/zh_CN/latest/?badge=latest)
[![PyPi version](https://img.shields.io/pypi/v/qt4w.svg)](https://pypi.python.org/pypi/qt4w/) 
[![GitHub tag](https://img.shields.io/github/tag/qtacore/qt4w.svg)](https://GitHub.com/qtacore/qt4w/tags/)

QT4W (Quick Test for Web) is a QTA test automation driver for Web.

### Features
* Android platform: support web automated testing based on webkit, X5 (used with [QT4A][1]). 
* IOS platform: Support Web automation testing for embedded pages of IOS applications and browser applications (used with [QT4I][2]).
* Windows platform: Supports web automation based on Chrome, IE kernel (used with QT4C), 
Now QT4C is in the open source process.

QT4W consists of three modules: WebView, webDriver, and WebControl module.

### WebView
WebView is an abstraction of the browser window, which is a re-encapsulation of the native control. QT4W only defines the relevant interface of WebView, but does not give a concrete implementation. QT4X provides some implementations of WebView on each side. For example, QT4C provides implementations such as IeWebView and ChromeWebView.

### WebDriver
WebDriver is the driver layer of web automation. This module is mainly used to handle Dom structure related operations, such as finding web elements. Driver implementations based on Webkit and Chrome kernel are available in QT4W.

### WebControl
The WebControl module defines the WebElement and WebPage interfaces and provides implementations. In addition, QT4W also encapsulates other common web elements that are used to encapsulate pages for web automation.Webelement and WebPage usage refer to usage documentation。

### Usage scenarios and installation
QT4W can be used for web applications or embedded page automation, which cannot be used independently and needs to be used in conjunction with other native layer automation frameworks:
* Android:  use and installation, please refer to [QT4A Document](https://qt4a.readthedocs.io/zh_CN/latest/web_test.html).
* iOS: use and install, please refer to [QT4i document](https://qt4i.readthedocs.io/zh_CN/latest/advance/webview.html).
* Windows: use and install, please refer to QT4C document
### links
* [Usage Document](https://qt4w.readthedocs.io/zh_CN/latest/index.html)
* [Design Document](https://github.com/qtacore/QT4W/blob/master/design.md)
------------------------------
 QT4W(Quick Test for Web)是QTA测试体系中的一环，主要用于Web自动化测试。
### 支持多种平台的Web自动化
* Android平台：支持基于webkit，X5等内核Web自动化测试（和[QT4A][1]一起使用)。
* IOS平台：支持IOS应用的内嵌页面及浏览器应用的Web自动化测试（和[QT4I][2]一起使用)。
* Windows平台：支持基于Chrome，IE内核的Web自动化测试（和QT4C一起使用），目前QT4C正在开源流程中。

QT4W是QTA测试体系中Web自动化测试的基础， 包含三个模块：WebView、webDriver以及WebControl模块。 

### WebView
WebView是对浏览器窗口的抽象，是对原生控件的再次封装。QT4W只是定义了WebView的相关接口，并未给出具体实现。QT4X各端提供了部分WebView的实现，例如QT4C中提供IeWebView、ChromeWebView等实现。

### WebDriver
WebDriver是web自动化中驱动层的封装，该模块主要用来处理Dom结构相关操作，例如查找web元素等。QT4W中提供了基于Webkit和Chrome内核的WebDriver封装E。


### WebControl
WebControl模块定义WebElement以及WebPage的接口，并且给出了相关实现。此外，QT4W还封装了其他的常用Web元素，使用该模块来封装Web自动化时的页面。

### 使用场景及安装
QT4W可用于各个端上的Web应用或者Native应用内嵌Web页面的自动化，其不能独立使用，需要结合其他Native层的自动化框架一起使用：
* Android端的使用及安装，请参考[QT4A文档](https://qt4a.readthedocs.io/zh_CN/latest/web_test.html)。
* iOS端的使用及安装，请参考[QT4i文档](https://qt4i.readthedocs.io/zh_CN/latest/advance/webview.html)。
* Windows端的使用及安装，请参考QT4C文档

### 链接

* [使用文档](https://qt4w.readthedocs.io/zh_CN/latest/index.html)
* [设计文档](https://github.com/qtacore/QT4W/blob/master/design.md)


  [1]: https://github.com/Tencent/QT4A
  [2]: https://github.com/Tencent/QT4i
  
 ------------------------------

欢迎加入QQ群（432699528）交流使用和反馈

