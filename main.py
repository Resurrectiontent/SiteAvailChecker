import time
import atexit
from logging import warning, error

from threading import Thread
from Condition import Condition
from SiteChecker import SiteChecker

URL = r'http://v.dltc.spbu.ru:5000/user/sign-in'
PERIOD = 300  # Seconds


def init_int_threads():
    """Initializes threads which safely interrupt work of application"""
    alarm_delegates = [SiteChecker.onclose, cond.interrupt]
    return [Thread(target=x) for x in alarm_delegates]


def alarm_stop():
    """Safely stops application"""
    for breaker in interrupting_threads:
        breaker.start()


if __name__ == '__main__':
    cond = Condition()
    atexit.register(alarm_stop)
    interrupting_threads = init_int_threads()

    # Infinite site checking
    while True:
        response = SiteChecker.check_site(URL)
        if response['value']:
            cond.risen()

        elif response['cause'].lower().startswith('server'):
            warning(response['cause'])
            cond.crashed()

        elif response['cause'].lower().startswith('internet'):
            current_time = time.localtime()
            error('{0}\n \t{1}:{2}:{3}'.format(response['cause'],
                                               current_time.tm_hour,
                                               current_time.tm_min,
                                               current_time.tm_sec))

        time.sleep(PERIOD)
