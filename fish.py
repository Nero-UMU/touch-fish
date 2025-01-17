import os
import datetime
import webbrowser
import csv
from record_fish import record_fish
# 读取配置文件
config = {}
if os.path.exists("config.cfg"):
    with open("config.cfg", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=")
                config[key.strip()] = value.strip()

# 检查是否为星期五
day = datetime.datetime.now().weekday()

# 根据配置打开网页
if config.get("v2ex") == "True":
    webbrowser.open("https://www.v2ex.com/")
if config.get("linux_do") == "True":
    webbrowser.open("https://linux.do/")
if config.get("github_trending") == "True":
    webbrowser.open("https://github.com/trending/")
if config.get("medium") == "True":
    webbrowser.open("https://medium.com/")

if day == 4:
    if config.get("ruanyifeng") == "True":
        webbrowser.open("https://www.ruanyifeng.com/blog/")

if config.get("tieba") == "True":
    webbrowser.open("https://tieba.baidu.com/")
if config.get("hackernoon") == "True":
    webbrowser.open("https://hackernoon.com/")
if config.get("hacker_news") == "True":
    webbrowser.open("https://news.ycombinator.com/")
if config.get("xiaoheihe") == "True":
    webbrowser.open("https://www.xiaoheihe.cn/app/bbs/home")
if config.get("arch_linux_bbs") == "True":
    webbrowser.open("https://bbs.archlinuxcn.org/")
if config.get("reddit") == "True":
    webbrowser.open("https://www.reddit.com/")
if config.get("twitter") == "True":
    webbrowser.open("https://x.com/")
if config.get("pixiv") == "True":
    webbrowser.open("https://www.pixiv.net/")
if config.get("buzzing") == "True":
    webbrowser.open("https://www.buzzing.cc/")
if config.get("steam") == "True":
    webbrowser.open("https://steamcommunity.com/")
if config.get("iflow") == "True":
    webbrowser.open("https://www.iflow  .work/")


record_fish(config.get("record_fish"),config.get("generate_fish_record"))

