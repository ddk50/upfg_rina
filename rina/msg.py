import datetime

class Msg:
    skip_threshold_secs = 30 * 60
    notify_hours = {
        24: False,
        12: False,
        6: False,
        3: False,
        1: False
    }
    start_time = 0
    msg = ""
    def __init__(self, start_time, msg):
        self.start_time = start_time
        self.msg = msg

    @staticmethod
    def by_secs(hours):
        return hours * 60 * 60

    def get_timetable(self):
        return self.notify_hours

    def get_notification_times(self):
        mapped_list = map(str, self.notify_hours.keys())
        return ', '.join(mapped_list)

    def broadcast_or_not(self, now = datetime.datetime.now()):
        delta = self.start_time - now
        for k,v in self.notify_hours.items():
            if delta.total_seconds() <= Msg.by_secs(k) and v == False:
                if Msg.by_secs(k) - delta.total_seconds() > self.skip_threshold_secs:
                    # 通知時間をあまりにも超えていた場合はBotが停止していた時間があったと考えて
                    # その時刻は通知済みFlag立てるだけにし、実際の通知は行わない
                    self.notify_hours[k] = True
                else:
                    self.notify_hours[k] = True # 放送済みにする
                    return self.msg
        return None
