# wanfang.v2

运行：pip3 install scrapy


进入....../wanfang/spider文件夹，

screen -S spider1  创建一个任务窗口

scrapy crawl wanfang -o wanfang.csv

ctrl + a d把窗口关闭。这样本地退出终端服务器依然可以运行爬虫。

再输入screen -r spider1即可恢复任务窗口进行查看
