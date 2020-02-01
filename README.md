# gratuation_project
豆瓣电影的主从scrapy_redis爬虫，django网页展示数据，mongo存储数据，数据量不大，**学习为主**，顺便完成毕业设计，
不涉及很大的爬取量

Jay_Redis Jay_Redis_slave 分别是master端和slave端的爬虫，基本已经编写完毕了，就差Django的网页了
曾经试过在云主机上放一个爬取代理IP池拿来自己用，结果发现如果有badproxy的话会导致出现很多同样的网站待爬
而且发现豆瓣还是很友好的，你不过分基本不会涉及封ip，所以就放弃了使用代理池

可视化工具用了Navicat premium， anoter redis desktop manager

一个比较有意思的库 fake_useragent 自动生成useragent， 麻麻再也不用担心我去到处收集useragent来轮换了


# timeline
#### 2020/2/1 
把年前写好的爬虫提交了上去，说好的过年写完django，结果因为冠状病毒（在家发呆），回学校前一定写完