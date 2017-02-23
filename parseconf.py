#!/usr/bin/env python
# coding: utf-8

import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class ParseConf:
    def __init__(self):
        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')

            # 群名
            self.group_name = cf.get('robot', 'group_name')

            # 定时发送优惠商品间隔(秒数)
            self.schedule_sleep = int(cf.get('robot', 'schedule_sleep'))

            # 欢迎
            self.welcome = cf.get('robot', 'welcome')

            # 新人提醒
            self.notice = cf.get('robot', 'notice')

            # excel文件
            self.excel_file = cf.get('excel_parse', 'excel_file')

            # excel主要内容 开始行数
            self.start_line = int(cf.get('excel_parse', 'start_line'))

            # 优惠券时间验证可选
            self.ignore_coupon_date = int(cf.get('excel_parse', 'ignore_coupon_date'))

            # 列配置
            # 标题
            self.title_col = int(cf.get('excel_parse', 'title_col'))
            # 主图
            self.pic_col = int(cf.get('excel_parse', 'pic_col'))
            # 详情url
            self.detail_url_col = int(cf.get('excel_parse', 'detail_url_col'))
            # 商品价格
            self.price_col = int(cf.get('excel_parse', 'price_col'))
            # 店铺名称
            self.shop_col = int(cf.get('excel_parse', 'shop_col'))
            # 优惠券
            self.coupon_col = int(cf.get('excel_parse', 'coupon_col'))
            # 优惠券开始
            self.coupon_start_col = int(cf.get('excel_parse', 'coupon_start_col'))
            # 优惠券结束
            self.coupon_end_col = int(cf.get('excel_parse', 'coupon_end_col'))
            # 商品优惠券推广地址
            self.coupon_campaign_col = int(cf.get('excel_parse', 'coupon_campaign_col'))
        except Exception, e:
            print '[ERROR] File conf.ini is not exist.'
            raise e