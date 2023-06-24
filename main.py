from utils.Clock import Clock
import time

clock = Clock(0, 59)
while True:
    print(clock.stringify(twelve_hr_format=True))
    time.sleep(0.05)
    clock.update()