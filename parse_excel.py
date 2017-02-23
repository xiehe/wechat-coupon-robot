#!/usr/bin/env python
# coding: utf-8

from tkl import Tkl
import xlrd
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

"""
解析excel数据
"""
class ParseExcel:
    def __init__(self, conf):
        self.conf = conf

    def get_line_str(self):
        """
        根据上次行数+1，获取该行数据组合
        """
        excel = xlrd.open_workbook(self.conf.excel_file)
        table = excel.sheet_by_index(0)
        rows = table.nrows
        data = {
            "text": "",
            "image_url": "",
        }

        # 没有要执行的数据
        if rows == 0 or (rows - self.conf.start_line) == 0:
            return ''

        # 根据上次执行的行号处理
        current_line = self.get_last_time_line()

        # 上次行号后是否有新数据
        if current_line >= rows or (current_line + 1) >= rows:
            print '[INFO] No new line to execute in excel.'
            return ''
        current_line = current_line + 1
        row = table.row_values(current_line)
        
        # 优惠券是否过期
        if self.get_coupon_is_expired(row) == True:
            print '[INFO] Line %d coupon is not in the date range.' % (current_line)
        else:
            # 组装字符串
            # 标题
            data['text'] = row[self.conf.title_col] + '\n'
            # 获得使用优惠券后的价格后，组装价格一行数据
            coupon = self.get_coupon_price(row[self.conf.price_col], row[self.conf.coupon_col])
            if coupon['math'] == 1:
                data['text'] += u'在售%s元，券后%s元 \n' % (row[self.conf.price_col], coupon['coupon_price'])
            else:
                data['text'] += u'%s元起，%s \n' % (row[self.conf.price_col], row[self.conf.coupon_col])
            data['text'] += '--------- \n';
            # 店铺信息
            data['text'] += u'来自%s \n' % (row[self.conf.shop_col])
            # 淘口令信息
            tkl = Tkl()
            code = tkl.get_code(row[self.conf.coupon_campaign_col])
            if code == '':
                print '[ERROR] 生成淘口令失败'
                raw_input(u"按任意键结束...")
                exit()
            data['text'] += code
            # 主图信息
            data['image_url'] = row[self.conf.pic_col]

        # 写入当前成功执行的行数
        self.write_current_line(current_line)
        
        return data

    def get_coupon_price(slef, price, coupon_info):
        """
        获得使用优惠券后的价格
        """
        data = {
            "match": 0,             # 是否满足优惠券满减
            "coupon_price": 0.0,    # 使用优惠券后的金额
            "coupon": [0, 0]        # 满减的两个价格
        }
        m = re.findall(r'(\d+)', coupon_info)
        if len(m) == 2:
            # 满x元减x元
            data['coupon'] = [int(i) for i in m]
        elif len(m) == 1:
            data['coupon'] = [0, int(m[0])]
        else:
            print u'[ERROR] 优惠券格式不正确'

        # 如果没有达到优惠券指定金额则返回原价
        price = float(price)
        if price >= data['coupon'][0]:
            data['math'] = 1
            data['coupon_price'] = price - data['coupon'][1]
        else:
            data['math'] = 0

        return data

    def get_coupon_is_expired(self, row):
        """
        判断优惠券是否过期,或未开始
        return bool
        """
        # 是否忽略时间验证
        if self.conf.ignore_coupon_date == 1:
            return False

        # date = time.strftime('%Y-%m-%d', time.localtime())
        start = re.findall(r'\d{4}\-\d{2}\-\d{2}', row[self.conf.coupon_start_col])
        end = re.findall(r'\d{4}\-\d{2}\-\d{2}', row[self.conf.coupon_end_col])
        if len(start) == 1 and len(end) == 1:
            start = start[0]
            end = end[0]
        else:
            print u'[ERROR] 优惠券时间获取失败.'
            raw_input(u"按任意键结束...")
            exit()

        # 时间戳比较
        start_time = time.mktime(time.strptime(start, "%Y-%m-%d"))
        end_time = time.mktime(time.strptime(end, "%Y-%m-%d"))
        end_time = time.mktime(time.strptime('2016-12-04', "%Y-%m-%d"))
        cur_time = time.time()

        if start_time <= cur_time and end_time >= cur_time:
            return False
        else:
            print u'[WARNING] 优惠券过期[%s至%s].' % (row[self.conf.coupon_start_col], row[self.conf.coupon_end_col])
            return True

    def get_last_time_line(self):
        """
        获取最后一次执行成功的excel行号
        return int
        """
        try:
            f = open('excel.data', 'r')
            line = f.read()
            f.close()
            if line == '':
                line_num = 0
            else:
                line_num = int(line)
        except IOError, e:
            line_num = 0
        
        return line_num

    def write_current_line(self, line_num):
        """
        写入当前行
        """
        f = open('excel.data', 'w')
        f.write(str(line_num))
        f.close()