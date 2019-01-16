## 扩展QT4W

　　QT4W作为一个中间层的框架，做了分层设计，提供了良好的扩展性。虽然QT4X提供的现成的封装已经能够满足大部分场景下的使用。但是某些特殊场景下，可能需要自己去扩展QT4W。扩展QT4W可能需要实现WebView、WebDriver或者Browser接口。例如如果需要在MAC系统上进行Chrome浏览器的自动化测试，这里就需要实现Mac上能正常运行的WebView、Browser以及WebDriver接口。下面就详细说说如何去实现这几个接口</br>
　　
+ [WebView实现][1]；   </br>
+ [WebDriver实现][2]； </br>
+ [Browser实现][3]；   </br>


  [1]: extend/webview.html
  [2]: extend/WebDriver.html
  [3]: extend/Browser.html