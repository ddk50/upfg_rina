import datetime
import sqlite3
import re
from texttable import Texttable

from dateutil.parser import parse
from .msg import Msg

MAX_SLOT_NUM = 15

class Notifications:
    slots = {}
    def __init__(self):
        for i in range(MAX_SLOT_NUM):
            self.slots[i] = None
        self.angry_count = 0

    def get_all(self):
        return filter(lambda x: x != None, self.slots)

    def size(self):
        return len(self.slots)

    def put(self, start_time, msg):
        for i in range(len(self.slots)):
            h = self.slots[i]
            if h == None:
                self.slots[i] = Msg(start_time, msg)
                return self.slots[i]
        return None

    def angry(self):
        str = ""
        with open(path) as f:
            while True:
                str += f.readline()
                if not s_line:
                    break
        return str

    def get_pp(self):
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t', 't', 'i', 'i', 'i', 'i', 'i'])
        table.add_rows([["msg", "date", "24", "12", "6", "3", "1"]])
        

    def execute_notify(self, rest_msg):
        notify      = Notifications.parse_notify(rest_msg)
        msg         = notify[0]
        datetimestr = f"{notify[1]} {notify[2]}"
        start_time   = parse(datetimestr)
        
        ret = self.put(start_time, msg)
        if ret != None:
            return f"{start_time} に イベントが登録されたよ! 開始時刻の {ret.get_notification_times()} ごとに告知するよ"
        else:
            return "予約枠がいっぱい。。。もう登録できない。。。どれか消してね"
        
    def execute(self, msg):
        r = Notifications.parse(msg)
        if r == None:
            return None
        else:
            t = r.split()
            first = t[0]
            rest = ' '.join(t[1:])
            if first == 'help':
                print(f"Incoming help command")
                return '私、天王寺璃奈。どっちでも好きな方つかっていいよ//'
            elif first == 'list':
                print(f"Incoming list command")
                list = self.get_all()
                return f"予約されてる告知は: \n ${list} だよ"
            elif first == 'tong':
                return f"トングさんは{rest}。璃奈、覚えた"
            elif first == 'notify':
                print(f"Incoming notify command {rest}")
                return self.execute_notify(rest)
            else:
                self.angry_count += 1
                str = 'なにいってるのかよくわからない... /rina help で使い方が見れるよ'
                if self.angry_count >= 3:
                    self.angry_count = 0
                    str = self.angry()
                return str
            return None

    @staticmethod
    def parse_notify(cmdstr):
        m = re.search('"(.+)"\s+(\S+)\s+(\S+)', cmdstr)
        if m != None:
            r = m.groups()
            msg = r[0]
            day = r[1]
            time = r[2]
            return (msg, day, time)
        else:
            return None

    @staticmethod
    def parse(cmdstr):
        m = re.search('^(/rina)\s+(.+)', cmdstr)
        if m != None:
            r = m.groups()
            return r[1]
        else:
            return None
        
