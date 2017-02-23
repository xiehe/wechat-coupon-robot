#!/usr/bin/env python
# coding: utf-8

import time

"""
::定时器::
解决长时间sleep自动退出问题
example:
    s = Schedule(60)
    print s.is_valid_time()
"""
class Schedule:
    def __init__(self, sleep_sec):
        self.sleep_sec = sleep_sec

    def is_valid_time(self):
        """判断当前是否在有时间内"""
        last_time = self.get_last_time()
        now_time = int(time.time())
        if (last_time + self.sleep_sec) > now_time:
            return False
        elif last_time == 0:
            self.write_time()
            return True
        else:
            self.write_time()
            return True

    def get_last_time(self):
        """获取最后执行时间"""
        try:
            f = open('schedule.data', 'r')
            timestmap = f.read()
            if timestmap == '':
                return 0
        except IOError, e:
            return 0
        return int(timestmap)

    def write_time(self):
        """写入时间戳"""
        f = open('schedule.data', 'w')
        now_time = int(time.time())
        f.write(str(now_time))