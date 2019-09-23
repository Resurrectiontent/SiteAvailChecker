import time

from Condition import Condition
from SiteChecker import SiteChecker

URL = r'http://v.dltc.spbu.ru:5000'
PERIOD = 60  # Seconds

cond = Condition()
sch = SiteChecker(URL)

if __name__ == '__main__':
    while True:
        if sch.check_site():
            cond.risen()
        else:
            cond.crashed()

        time.sleep(PERIOD)
