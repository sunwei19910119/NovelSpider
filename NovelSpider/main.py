from scrapy.cmdline import execute
import sys
import os

#将系统当前目录设置为项目根目录
#os.path.abspath(__file__)为当前文件所在的绝对路径
#os.path.dirname为文件所在目录  
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#执行命令相当于在控制台输入改名了
execute(["scrapy","crawl","zxcs"])
