import json
import re
import time
from datetime import datetime

import requests as requests
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from App import db, app

class CrawlData:
    def __init__(self):
        self.ua = UserAgent()
        self.urls={
            'V3EX':'https://www.v2ex.com/?tab=hot',
            'Github':'https://github.com/trending',
            'WeiBo':'https://s.weibo.com/top/summary',
            'ZhiHu':'https://www.zhihu.com/hot',
        }
        self.headers={
            'User-Agent': self.ua.random,
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }


    # 抖音 热搜榜
    def douyin(self):
        headers = {
            'Referer': 'https://www.douyin.com',
            'User-Agent': self.ua.random
        }
        response = requests.get('https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/', headers=headers)
        if response.status_code == 200:
            json_res = response.json()
            temp_arr = []
            for k, v in enumerate(json_res['word_list']):
                temp_arr.append({
                    'index': k + 1,
                    'title': v['word'],
                    'hot': f"{round(v['hot_value'] / 10000, 1)}万",
                    'url': f'https://www.douyin.com/search/{v["word"]}',
                    'mobilUrl': f'https://www.douyin.com/search/{v["word"]}'
                })
            return {
                'success': True,
                'title': '抖音',
                'subtitle': '热搜榜',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data': temp_arr
            }
        else:
            return {'success': False, 'message': '请求失败'}


    # 知乎热榜  热度
    def zhihu_hot(self):
        headers = {
            'Referer': 'https://www.zhihu.com',
            'User-Agent': self.ua.random
        }
        response = requests.get('https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true',
                                headers=headers)
        if response.status_code == 200:
            json_res = response.json()
            temp_arr = []
            for k, v in enumerate(json_res['data']):
                hot = re.search(r'\d+', v['detail_text']).group()
                temp_arr.append({
                    'index': k + 1,
                    'title': v['target']['title'],
                    'hot': f"{hot}万",
                    'url': f'https://www.zhihu.com/question/{v["target"]["id"]}',
                    'mobilUrl': f'https://www.zhihu.com/question/{v["target"]["id"]}'
                })
            return {
                'success': True,
                'title': '知乎热榜',
                'subtitle': '热度',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data': temp_arr
            }
        else:
            return {'success': False, 'message': '请求失败'}


    # 微博 热搜榜
    def wbresou(self):
        md5 = str(int(time.time()))  # 获取当前时间的时间戳并转换为字符串
        cookie = f"Cookie: {md5}:FG=1"
        headers = {
            'Cookie': cookie,
            'Referer': 'https://s.weibo.com',
            'User-Agent': self.ua.random
        }
        response = requests.get('https://weibo.com/ajax/side/hotSearch', headers=headers)
        if response.status_code == 200:
            json_res = response.json()
            temp_arr = []
            for k, v in enumerate(json_res['data']['realtime']):
                temp_arr.append({
                    'index': k + 1,
                    'title': v['note'],
                    'hot': f"{round(v['num'] / 10000, 1)}万",
                    'url': f"https://s.weibo.com/weibo?q={v['note']}&Refer=index",
                    'mobilUrl': f"https://s.weibo.com/weibo?q={v['note']}&Refer=index"
                })
            return {
                'success': True,
                'title': '微博',
                'subtitle': '热搜榜',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data': temp_arr
            }
        else:
            return {'success': False, 'message': '请求失败'}

    # 少数派 热榜
    def sspai(self):
        headers = {
            'Referer': 'https://sspai.com',
            'User-Agent': self.ua.random
        }
        response = requests.get(
            'https://sspai.com/api/v1/article/tag/page/get?limit=100000&tag=%E7%83%AD%E9%97%A8%E6%96%87%E7%AB%A0',
            headers=headers)
        if response.status_code == 200:
            json_res = response.json()
            temp_arr = []
            for k, v in enumerate(json_res['data']):
                temp_arr.append({
                    'index': k + 1,
                    'title': v['title'],
                    'createdAt': datetime.utcfromtimestamp(v['released_time']).strftime('%Y-%m-%d'),
                    'other': v['author']['nickname'],
                    'like_count': v['like_count'],
                    'comment_count': v['comment_count'],
                    'url': f'https://sspai.com/post/{v["id"]}',
                    'mobilUrl': f'https://sspai.com/post/{v["id"]}'
                })
            return {
                'success': True,
                'title': '少数派',
                'subtitle': '热榜',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data': temp_arr
            }
        else:
            return {'success': False, 'message': '请求失败'}


    def csdn(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
            'Referer': 'https://www.csdn.net'
        }
        response = requests.get('https://www.csdn.net', headers=headers)
        if response.status_code == 200:
            res_html = response.text
            res_html_arr = re.search(r'window.__INITIAL_STATE__=(.*?);<\/script>', res_html)
            if res_html_arr:
                json_res = json.loads(res_html_arr.group(1))
                temp_arr = []
                # 头条
                for k, v in enumerate(json_res['pageData']['data']['www-headhot']):
                    temp_arr.append({
                        'index': k + 1,
                        'title': v['title'],
                        'url': v['url'],
                        'mobilUrl': v['url']
                    })
                # 头条1
                for k, v in enumerate(json_res['pageData']['data']['www-Headlines']):
                    temp_arr.append({
                        'index': k + 17,
                        'title': v['title'],
                        'url': v['url'],
                        'mobilUrl': v['url']
                    })
                # 头条2
                for k, v in enumerate(json_res['pageData']['data']['www-headhot']):
                    temp_arr.append({
                        'index': k + 48,
                        'title': v['title'],
                        'url': v['url'],
                        'mobilUrl': v['url']
                    })
                return {
                    'success': True,
                    'title': 'CSDN',
                    'subtitle': '头条榜',
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'data': temp_arr
                }
            else:
                return {'success': False, 'message': '未能解析到数据'}
        else:
            return {'success': False, 'message': '请求失败'}

    def baike_history(self):
        month = datetime.now().strftime('%m')
        day = datetime.now().strftime('%d')
        today = datetime.now().strftime('%Y年%m月%d日')
        headers = {
            'Referer': 'https://baike.baidu.com',
            'User-Agent': self.ua.random
        }
        response = requests.get(f'https://baike.baidu.com/cms/home/eventsOnHistory/{month}.json', headers=headers)
        if response.status_code == 200:
            json_res = response.json()
            temp_arr = []
            countnum = len(json_res[month][month + day]) - 1
            for k, v in enumerate(json_res[month][month + day]):
                temp_arr.append({
                    'index': k + 1,
                    'title': f"{v['year']}年-{v['title']}",
                    'url': f'https://www.douyin.com/search/{v["title"]}',
                    'mobilUrl': f'https://www.douyin.com/search/{v["title"]}'
                })
            return {
                'success': True,
                'title': '百度百科',
                'subtitle': '历史上的今天',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data': temp_arr
            }
        else:
            return {'success': False, 'message': '请求失败'}

    # // 哔哩哔哩 全站日榜
    def bilibili_rankall(self):
        headers = {
            'Referer': 'https://www.bilibili.com',
            'User-Agent': self.ua.random
        }
        response = requests.get('https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all', headers=headers)
        if response.status_code == 200:
            json_res = response.json()
            temp_arr = []
            for k, v in enumerate(json_res['data']['list']):
                temp_arr.append({
                    'index': k + 1,
                    'title': v['title'],
                    'pic': v['pic'],
                    'desc': v['desc'],
                    'hot': f"{round(v['stat']['view'] / 10000, 1)}万",
                    'url': v['short_link_v2'],
                    'mobilUrl': v['short_link_v2']
                })
            return {
                'success': True,
                'title': '哔哩哔哩',
                'subtitle': '全站日榜',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data': temp_arr
            }
        else:
            return {'success': False, 'message': '请求失败'}

    # B站 热搜榜
    def bilibili_hot(self):
        headers = {
            'Referer': 'https://www.bilibili.com',
            'User-Agent': self.ua.random
        }
        response = requests.get('https://app.bilibili.com/x/v2/search/trending/ranking', headers=headers)
        if response.status_code == 200:
            json_res = response.json()
            temp_arr = []
            for v in json_res['data']['list']:
                temp_arr.append({
                    'index': v['position'],
                    'title': v['keyword'],
                    'url': f'https://search.bilibili.com/all?keyword={v["keyword"]}&order=click',
                    'mobilUrl': f'https://search.bilibili.com/all?keyword={v["keyword"]}&order=click'
                })
            return {
                'success': True,
                'title': '哔哩哔哩',
                'subtitle': '热搜榜',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data': temp_arr
            }
        else:
            return {'success': False, 'message': '请求失败'}


    # 百度热点
    def baiduredian(self):
        headers = {
            'User-Agent': self.ua.random
        }
        response = requests.get('https://top.baidu.com/board?tab=realtime', headers=headers)
        if response.status_code == 200:
            res_html = response.text.replace("\n", "").replace("\r", "").replace(" ", "")
            res_html_arr = re.search(r'<!--s-data:(.*?)-->', res_html)
            if res_html_arr:
                json_res = json.loads(res_html_arr.group(1))
                temp_arr = []
                for v in json_res['data']['cards']:
                    for k, _v in enumerate(v['content']):
                        temp_arr.append({
                            'index': k + 1,
                            'title': _v['word'],
                            'desc': _v['desc'],
                            'pic': _v['img'],
                            'url': _v['url'],
                            'hot': f"{round(int(_v['hotScore']) / 10000, 1)}万",
                            'mobilUrl': _v['appUrl']
                        })
                return {
                    'success': True,
                    'title': '百度热点',
                    'subtitle': '指数',
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'data': temp_arr
                }
            else:
                return {'success': False, 'message': '未能解析到数据'}
        else:
            return {'success': False, 'message': '请求失败'}


if __name__ == '__main__':
    method_list = ['douyin', 'zhihu_hot', 'wbresou', 'sspai', 'csdn', 'baike_history', 'bilibili_rankall', 'bilibili_hot', 'baiduredian']
    with app.app_context():
        cd = CrawlData()
        for method_name in method_list:
            method = getattr(cd, method_name, None)
            if method:
                data = method()
                print("======================")
                print(data)
        # data = cd.douyin()
        # data = cd.zhihu_hot()
        # data = cd.wbresou()
        # data = cd.sspai()
        # data = cd.csdn()
        # data = cd.baike_history()
        # data = cd.bilibili_rankall()
        # data = cd.bilibili_hot()
        # data = cd.baiduredian()

