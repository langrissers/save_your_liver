import win32api, win32con, win32gui
import time

while True:
    a = win32api.GetCursorPos()
    print(a)
    time.sleep(1)