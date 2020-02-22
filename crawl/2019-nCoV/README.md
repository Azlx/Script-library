# 爬取 全国每日确诊病例数(2019-nCoV)

数据来源：[新冠病毒肺炎疫情晴雨表](http://vis.pku.edu.cn/ncov/barometer/index.html)

### 问题：该页面是用svg画出来的，网页源码不是标准的html，不能爬取，如图：
![网页源码](https://raw.githubusercontent.com/AzazelX5/Script-library/master/crawl/2019-nCoV/image/WechatIMG7.png)

### 解决方法：通过浏览器控制台获取到源码保存到文件(以chrome为例)
1. 在数据页面右键，点击检查，打开控制台
2. 点击Elements标签栏，将滚动条拉至最上方
3. 找到 **html** 标签，右键点击 **Edit as HTML**
![保存html](https://raw.githubusercontent.com/AzazelX5/Script-library/master/crawl/2019-nCoV/image/WechatIMG173.png)
4. 全选全部内容，保存到 index.html 中

### 说明
> 脚本依赖：lxml　(pip install lxml)
>
> 运行方法：pyhton crawl.py
>
> 注: 每次等页面数据更新后都需要按照上面方法重新保存一下数据页面
