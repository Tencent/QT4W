## QT4W系统架构

### QT4W分层设计
　　QT4W作为一个Web自动化框架，采用了分层设计模式。QT4W从上到下总共可以分为三层：NativeControl、WebControl以及WebDriver层。</br>

  

|分层|  描述    |    
| --- | --- | 
| NativeControl  |  原生控件层，主要用于封装承载Web页面的容器控件和窗口，一般包括Broswer模块及webview模块,这部分内容和具体的平台关联性较大。  |    
  | WebControl  | Web控件层，主要用于Web层控件封装，包括web页面和web元素，该层包括WebPage和WebElement模块，此层是Web自动化的核心层。 |
| WebDriver   |  Web驱动层，包括BrowserDriver模块（实现注入Javascript代码）以及WebDriver模块（通过注入不同的js代码到Web页面中以提供不同的功能）。  |    

　　QT4W提供了统一的WebControl层的实现，定义了NativeControl和WebDriver的接口及部分功能实现。NativeControl及WebDriver在不同的平台上实现形式有所不同，和具体平台的相关，但是所有平台的都是用WebControl层提供的WebPage和WebElement作为基础进行控件封装。
   
### 模块结构
  
　　QT4W包括5个模块：Browser模块、WebView模块、WebPage模块、WebElement模块。各个模块的基本功能划分：
 1. Browser模块：提供对于浏览器窗口及浏览器常用操作的封装。
 2. WebView模块：提供注入的javascript代码、获取、操作web元素的接口，以及点击、滑动等操作。这里不同的系统会有不同的实现。
 3. WebDriver模块：对JS代码功能的封装，提供了不同WebView注入JavaScript代码的接口。由于不同的浏览器接口存在差异，这里会针对浏览器进行划分。
 4. WebPage模块：对Web页面的封装，提供了页面URL、页面标题、查找Web元素等接口，兼容autoweb中WebPage类。
 5. WebElement模块：对Web元素的封装，提供了元素样式、可见性、文本等属性，及点击、滑动等接口，兼容autoweb中WebElement类。
各个模块间的关系如下图所示：
![模块结构图][1]



 [1]: Image/moudle.png "模块图.PNG"

