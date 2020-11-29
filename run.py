import os
import time
t = time.localtime()
print("Bot started at {:0>2}:{:0>2}!".format(t.tm_hour, t.tm_min))
filename = "logs/logs{:0>2}{:0>2}{:0>2}{:0>2}"
while True:
    os.system("reminderbot.py")
    t = time.localtime()
    print("Bot restarted at {:0>2}:{:0>2}!".format(t.tm_hour, t.tm_min))
