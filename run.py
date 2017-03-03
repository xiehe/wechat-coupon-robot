#!/usr/bin/env python
# coding: utf-8

from wxbot import *
from parseconf import ParseConf
from parse_excel import ParseExcel
from schedule import Schedule
import os
import requests
import re
import time
import urllib2
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MyWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)
        self.config = ParseConf()

    def handle_msg_all(self, msg):
        # 群新成员欢迎
        # msg_type_id = 3是群聊
        # msg['content']['type'] == 12是邀请
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 12:
            if msg['user']['name'] == self.config.group_name:
                m = re.findall(ur'邀请\"(.*)\"', msg['content']['data'])
                if len(m) == 1:
                    invitee = m[0] # 被要求人名
                    # 发送欢迎
                    if self.config.welcome and os.path.exists(self.config.welcome):
                        f = open(self.config.welcome, 'r')
                        welcome = f.read()
                        f.close()
                        print '[INFO] Send welcome message to %s.' % (invitee)
                        self.send_msg(self.config.group_name, u'@%s\n %s' % (invitee, welcome))
                    # 发送提醒
                    if self.config.notice and os.path.exists(self.config.notice):
                        f = open(self.config.notice, 'r')
                        notice = f.read()
                        f.close()
                        print '[INFO] Send notice message to %s.' % (invitee)
                        self.send_msg(self.config.group_name, u'@%s\n %s' % (invitee, notice))

    def schedule(self):
        # self.send_msg(u'测试', u'机器人测试')
        # dst = self.get_user_id(u'测试')
        # self.send_img_msg_by_uid('b812c8fcc3cec3fdbddb1a8cd488d43f86942765.jpg', dst)

        s = Schedule(self.config.schedule_sleep)
        if s.is_valid_time() == True:
            dst = self.get_user_id(self.config.group_name)

            xls = ParseExcel(self.config)
            data = xls.get_line_str()

            if data == '':
                print u'[INFO] 没有需要发送的数据.'
            elif data['text'] and data['image_url']:
                # 下载商品图片
                img_data = urllib2.urlopen(data['image_url']).read()
                # 保存图片
                m = hashlib.md5()
                m.update(data['image_url'])
                name = "temp/img/%s.jpg" % (m.hexdigest())
                print '[INFO] Download image as %s' % (name)
                f = open(name, 'wb')
                f.write(img_data)
                f.close()
                stat = self.send_img_msg_by_uid(name, dst)
                if stat == True:
                    print u'[INFO] 图片发送成功 %s' % (dst)
                
                # 延迟2秒,防止图片比文字慢
                time.sleep(2)

                stat = self.send_msg(self.config.group_name, data['text'])
                if stat == True:
                    print u'[INFO] 优惠信息发送成功. %s' % (dst)
            else:
                print u'[INFO] 没有图片和优惠码等信息.'

        # time.sleep(10)


def main():
    print u'version v0.3.12 By:小墨 QQ:244349067'
    bot = MyWXBot()
    # bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()

    # 淘口令测试
    # tkl = Tkl()
    # print tkl.get_code("https://uland.taobao.com/coupon/edetail?e=7EVvU0WKZAMN%2BoQUE6FNzLZT%2FCtAkW38zXEUa5tVE6YLiN%2FThfFfO7tLmdOqMMWWQMaEildNVff21CRvce78ah0HgBdG%2FDDL%2F1M%2FBw7Sf%2FfhIA3IALBf2qTj%2FKNmxZP%2Bo8BWEgW6U2HKjYLBGfMnkUrGLMmMO24%2B&pid=mm_15647003_18732119_65972202&af=1")

    # 解析excel测试
    # xls = ParseExcel(ParseConf())
    # print xls.get_line_str()

if __name__ == '__main__':
    main()
