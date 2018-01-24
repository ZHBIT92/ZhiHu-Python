from scrapy.cmdline import execute

import sys
import os

# 获取项目当前位置

address = sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(address)
# 用execute调用命令打开爬虫，cmd中命令为`scrapy crawl jobbole`
execute(["scrapy", "crawl", "jobbole"])