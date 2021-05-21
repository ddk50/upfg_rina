import datetime

class Msg:
    skip_threshold_secs = 5 * 60
    notify_hours = {
        24: False,
        12: False,
        6: False,
        3: False,
        1: False
    }
    start_time = 0
    msg = ""
    def __init__(self, start_time, msg, channel_id):
        self.start_time = start_time
        self.msg = msg
        self.channel_id = channel_id

    @staticmethod
    def by_secs(hours):
        return hours * 60 * 60

    def get_timetable(self):
        return self.notify_hours

    def get_notification_times(self):
        mapped_list = map(str, self.notify_hours.keys())
        return ', '.join(mapped_list)

    def broadcast_or_not(self):
        ret = None
        now = datetime.datetime.now()
        if self.start_time >= now:
            # イベント時刻が未来であるばあい
            # これは正常
            delta = self.start_time - now
            
            for k, v in self.notify_hours.items():
                t = int(delta.total_seconds() - Msg.by_secs(k))
                print(f"{self.msg} -- {t}")
                if v == False:
                    if t < 0:
                        # deltaがマイナスの場合は通知時刻を過ぎている。
                        # ので、通知したことにして実際は通知しない
                        self.notify_hours[k] = True

                        # が、±self.skip_threshold_secsの遅れは許容して通知する
                        if abs(t) <= self.skip_threshold_secs:
                            ret = self.msg, self.channel_id
                    elif t == 0:
                        # 時刻ピッタリ、通知する
                        self.notify_hours[k] = True
                        ret = self.msg, self.channel_id                        
                    else:
                        # deltaが整数の場合はまだその時間ではない
                        ret = None
        else:
            # イベント時刻が過去の場合
            # これは異常。Botが停止してたか、入力者がとち狂って過去の時刻にイベントを行おうとしたかのいずれか
            if v == True:
                print("過去のイベントが登録されてるのでフラグだけたてて抹消")
            
        return ret
