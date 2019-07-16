## 扩展QT4W

　　QT4W作为一个中间层的框架，做了分层设计，提供了良好的扩展性。虽然QT4X提供的现成的封装已经能够满足大部分场景下的使用。但是某些特殊场景下，可能需要自己去扩展QT4W。
目前QT4W支持的WebView有：

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
| 微信小程序 | Android微信 | 微信小程序使用 |  由[AndroidWXMPLib](https://github.com/qtacore/AndroidWXMPLib/)提供| 
| Chrome | MacOS | Mac OS下的Chrome浏览器和内嵌页面使用 | 由QT4Mac提供 |

　　扩展QT4W可能需要实现WebView、WebDriver或者Browser接口。例如如果需要在MAC系统上进行Chrome浏览器的自动化测试，这里就需要实现Mac上能正常运行的WebView、Browser以及WebDriver接口。下面就详细说说如何去实现这几个接口</br>
　　
+ [WebView实现][1]；   </br>
+ [WebDriver实现][2]； </br>
+ [Browser实现][3]；   </br>


  [1]: extend/webview.html
  [2]: extend/WebDriver.html
  [3]: extend/Browser.html