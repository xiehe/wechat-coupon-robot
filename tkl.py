#!/usr/bin/env python
# coding: utf-8

import requests
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

"""
淘口令生成器
"""
class Tkl:
    def __init__(self):
        self.tkl_url = {
            'one': 'http://www.tuidian.net/?a=tpwd',
            'two': 'http://tool.chaozhi.hk/api/tb/GetTkl.php',
        }
        # 次数限制
        self.tkl_limit = {
            'one': -1,  # 不限制
            'two': 100,
        }
        # 当前使用的
        self.current = 'one'
        date = time.strftime('%Y-%m-%d', time.localtime())
        try:
            line = self.get_data()
            self.current = line[0]
            # 如果不是当前则重置
            if line[1] != date:
                self.write_date('one')
        except IOError, e:
            self.write_date('one')

    def get_code(self, url):
        # return method_one(url)
        ret = getattr(self, 'method_'+self.current)(url)
        if ret == '' and self.current == 'one':
            self.write_date('two')
            self.current = 'two'
            ret = getattr(self, 'method_'+self.current)(url)

        # 是否次数用完
        if self.tkl_limit['two'] == 0 and self.current == 'two':
            print '[ERROR] 次数全部用完'

        return ret

    def method_one(self, url):
        """调用方式一"""
        payload = {'url': url}
        headers = {
            'X-Requested-With':'XMLHttpRequest',
            'User-Agent':"""Mozilla/5.0 (Windows NT 10.0; WOW64) 
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36""",
            'Referer':'http://www.tuidian.net/'
        }
        r = requests.post(self.tkl_url['one'], data=payload, headers=headers)
        json = r.json()
        if json['error'] == 1:
            return json['info']
        else:
            return ''

    def method_two(self, url):
        payload = {
            'url': url,
            'text': '粉丝福利购',
            'logo':'',
            'action':'refresh'
        }
        headers = {
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://tool.chaozhi.hk/tkl/',
            'X-Requested-With':'XMLHttpRequest'
        }
        r = requests.post(self.tkl_url['two'], data=payload, headers=headers)
        json = r.json()
        if json['model'] != '':
            # 剩余次数
            self.tkl_limit['two'] = int(json['refresh'])
            return '复制这条信息，打开 [手机淘宝] 即可查看' + json['model']
        else:
            return ''

    def get_data(self):
        f = open('tkl.data', 'r')
        line = f.read().split('|')
        f.close()
        return line

    def write_date(self, current):
        date = time.strftime('%Y-%m-%d', time.localtime())
        f = open('tkl.data', 'w')
        f.write(current+'|'+date)
        f.close()