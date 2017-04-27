import requests
from bs4 import BeautifulSoup
import re
from spider import get_search_url, dingdian, info_list




# 获取页面的response然后返回
def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    html = requests.get(url,headers=headers).content

    return html

def get_allbook_url(search_name):
    info = []
    for item in info_list.find():
        if search_name in item:
            info = item[search_name]
    if info ==[]:
        info = get_search_url(search_name)
    urls = [i[0] for i in info]
    # print(urls)
    return urls


def get_allzj_title(search_name):

    urls = get_allbook_url(search_name)
    L = []
    for url in urls:
        # BeautifulSoup解析页面获取所有章节url
        soup = BeautifulSoup(get_html(url), 'lxml')
        all_td = soup.find_all('td', class_="L")
        # 定义一个存储章节url的集合
        urllist = []
        titlelist = []
        for a in all_td:
            # 这里有些小说会有作者写的一些通知，页面会和普通章节页不同，直接过滤报错
            try:
                titles = a.get_text()
                titlelist.append(titles)
            except Exception:
                pass
        L.append(titlelist)
    return L


# def get_allzj_title(search_name):
#     for each in get_allzj_url(search_name):
#         #print(each)
#         for i in each:
#             soup = BeautifulSoup(get_html(i), 'lxml')
#             # 获取章节标题
#             title = soup.title.text.split('-')[1]
#             # print(title)
#             return title
#         #all_info = soup.find('dd', id="contents")
#         # 使用正则匹配章节内容
#         #p = r'<dd id="contents">(.*?)</dd>'
#         # 处理正则在匹配错误，都是作者牢骚的内容，不影响小说内容抓取，直接过滤
#         # try:
#         #     info = re.findall(p, str(all_info), re.S)[0]
#         #     # 下载到txt文件
#         #     with open(title + '.txt', 'w', encoding='gbk', errors='ignore') as f:
#         #         f.write(info.replace('<br/>', '\n'))
#         #         print('save sucessful: %s' % title)
#         # except Exception:
#         #     print('re faild: %s' % title)
#
# search_name = "九鼎记"
# get_allzj_title(search_name)
# get_allbook_url(search_name)
# get_allzj_title(search_name)
