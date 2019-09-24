import time
import atexit

from threading import Thread
from Condition import Condition
from SiteChecker import SiteChecker

URL = r'http://v.dltc.spbu.ru:5000'
PERIOD = 60  # Seconds

cond = Condition()


def init_int_threads():
    alarm_delegates = [SiteChecker.onclose, cond.interrupt]
    return [Thread(target=x) for x in alarm_delegates]


def alarm_stop():
    for breaker in interrupting_threads:
        breaker.start()


interrupting_threads = []
atexit.register(alarm_stop)


if __name__ == '__main__':
    interrupting_threads = init_int_threads()
    while True:
        if SiteChecker.check_site(URL):
            cond.risen()
        else:
            cond.crashed()

        time.sleep(PERIOD)
