import time
import atexit

from threading import Thread
from Condition import Condition
from SiteChecker import SiteChecker

URL = r'http://v.dltc.spbu.ru:5000'
PERIOD = 60  # Seconds

cond = Condition()
sch = SiteChecker(URL)


def init_int_threads(threads: list):
    alarm_delegates = [sch.immediate_break, cond.interrupt]
    threads = [Thread(target=x) for x in alarm_delegates]


def alarm_stop():
    for breaker in interrupting_threads:
        breaker.start()


interrupting_threads = []
atexit.register(alarm_stop)


if __name__ == '__main__':
    init_int_threads(interrupting_threads)
    while True:
        if sch.check_site():
            cond.risen()
        else:
            cond.crashed()

        time.sleep(PERIOD)
