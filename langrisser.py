#coding=utf-8
import math
import win32gui
import win32ui
import win32con
import win32api
import time
import random
import os
import sys
import platform
import ctypes
import subprocess

# diy  
import bmp

keyword = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 0, win32con.KEY_READ)
dir_local_appdata = win32api.RegQueryValueEx(keyword, 'Local AppData')[0]
dir_tmp_pic = dir_local_appdata + '\\Langrissers\\'
dir_harvest = dir_tmp_pic+'\\harvest\\'
if 'Langrissers' not in os.listdir(dir_local_appdata):
    os.makedirs(dir_tmp_pic)
if 'harvest' not in os.listdir(dir_tmp_pic):
    os.makedirs(dir_harvest)

dir_solid_pic = 'pics\\'
global num_create
global n_error
n_error = 0
num_create = 0

x_init = 0
y_init = 1  # win7 has a 21 pixel height title bar, but win10 has 22 pixel.
x_final = 1024
y_final = 767
global win10
win10 = 0
windows_version = platform.version()
build_number = int(windows_version.split(r'.')[0])
if build_number == 10:
    win10 = 1
    y_init = 0
    y_final = 768


print('dir_solid_pic: ', dir_solid_pic)
def wait_rand(tt):
    time.sleep(tt * (0.95 + 0.1 * random.random()))


def move_resize_window(x0=x_init, y0=y_init, xx=x_final, yy=y_final):
    wait_rand(0.4)
    hld = win32gui.FindWindow(None, '梦幻模拟战')
    if hld == 0:
        print('Cannot find Langrisser App')

    win32gui.SetWindowPos(hld, win32con.HWND_TOPMOST, x0, y0, xx, yy, win32con.SWP_SHOWWINDOW)
    wait_rand(0.4)


def cancel_top_most(x0=x_init, y0=y_init, xx=x_final, yy=y_final):
    hld = win32gui.FindWindow(None, '梦幻模拟战')
    if hld == 0:
        print('Cannot find Langrisser App')

    win32gui.SetWindowPos(hld, win32con.HWND_NOTOPMOST, x0, y0, xx, yy, win32con.SWP_SHOWWINDOW)


def window_capture(filename, wmin, hmin, wmax, hmax, scaling_factor = 1.0):
    move_resize_window()
    num_fail = 0
    global num_create
    # num_create += 1
    # print('num_create: ', num_create)
    wmax = int(wmax * scaling_factor)
    wmin = int(wmin * scaling_factor)
    hmax = int(hmax * scaling_factor)
    hmin = int(hmin * scaling_factor)
    
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    BitMap = win32ui.CreateBitmap()
    # MoniterDev = win32api.EnumDisplayMonitors(None, None)
    BitMap.CreateCompatibleBitmap(mfcDC, wmax-wmin, hmax-hmin)
    saveDC.SelectObject(BitMap)
    saveDC.BitBlt((0, 0), (wmax, hmax), mfcDC, (wmin, hmin), win32con.SRCCOPY)
    BitMap.SaveBitmapFile(saveDC, filename)

    win32gui.DeleteObject(BitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    cancel_top_most()


def wtt(filename, wmin, hmin, wmax, hmax, scaling_factor = 1.0):
    wmax = int(wmax * scaling_factor)
    wmin = int(wmin * scaling_factor)
    hmax = int(hmax * scaling_factor)
    hmin = int(hmin * scaling_factor)
    
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    BitMap = win32ui.CreateBitmap()
    # MoniterDev = win32api.EnumDisplayMonitors(None, None)
    BitMap.CreateCompatibleBitmap(mfcDC, wmax-wmin, hmax-hmin)
    saveDC.SelectObject(BitMap)
    saveDC.BitBlt((0, 0), (wmax, hmax), mfcDC, (wmin, hmin), win32con.SRCCOPY)
    BitMap.SaveBitmapFile(saveDC, filename)

    win32gui.DeleteObject(BitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    cancel_top_most()


def rms_difference(p1, p2):# p1 and p2 are two filenames of picture
    img1 = bmp.bmp(p1)
    img2 = bmp.bmp(p2)

    d1 = img1.reverse_data
    d2 = img2.reverse_data
    n1 = img1.bi_width
    m1 = img1.bi_height
    n2 = img2.bi_width
    m2 = img2.bi_height
    if m1 != m2 or n1 != n2:
        print('sizes of pic1 and pic2 are different')
    m = min(m1, m2)
    n = min(n1, n2)
    diff = 0
    for i in range(m):
        for j in range(n):
            diff += abs(d1[i][j][0] - d2[i][j][0]) ** 2
            diff += abs(d1[i][j][1] - d2[i][j][1]) ** 2
            diff += abs(d1[i][j][2] - d2[i][j][2]) ** 2
            

    rms = (diff / float(m*n)) ** 0.5
    return rms


def click(x, y):
    x11 = x - 2 + int(4 * random.random())
    y11 = y - 2 + int(4 * random.random())
    win32api.SetCursorPos((x11, y11))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x11, y11, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x11, y11, 0, 0)


def back_click():
    click(80, 58)


def auto_team():
    click(626,708)


def drag(input_x0, input_y0, input_x1, input_y1):
    x0 = input_x0
    y0 = input_y0
    x1 = input_x1
    y1 = input_y1
    move_resize_window()
    win32api.SetCursorPos((x0,y0))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x0, y0, 0, 0)
    dx = (x1 - x0) / 10
    dy = (y1 - y0) / 10
    for i in range(10):
        xx = x0 + int(dx * i)
        yy = y0 + int(dy * i)
        wait_rand(0.05)
        win32api.SetCursorPos((xx, yy))

    win32api.SetCursorPos((x1, y1))
    wait_rand(1.0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x1, y1, 0, 0)
    cancel_top_most()


def simple_drag(xx=1, yy=1):
    tx = 200
    ty = 200
    drag(512+tx*xx, 384-ty*yy, 512-tx*xx, 384+ty*yy)



def mouse_wheel(up_down=-1):
    win32api.SetCursorPos((1000,57))
    click(1000,57)
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, up_down)
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, up_down)
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, up_down)


def cdll_determine_stage():
    move_resize_window()
    print('dd_stage.exe 0')
    p = subprocess.Popen('dd_stage.exe 0')
    p.wait()
    stage = p.returncode
    print('subprocess_stage: ', stage)
    return stage
     
#def cdll_determine_stage():
#    #dllcv = ctypes.WinDLL('opencv_world345.dll')
#    dll = ctypes.WinDLL('determine_stage.dll')
#    #dll.determine_stage.restype = ctypes.c_int
#    stage = dll.determine_stage()
#    print('subprocess_stage: ', stage)
#    #win32api.FreeLibrary(dllcv._handle)
#    win32api.FreeLibrary(dll._handle)
#    return stage
#

def is_imfull():
    window_capture(dir_tmp_pic+'tmp_full.bmp', 330, 330, 700, 480)
    dd1 = rms_difference(dir_tmp_pic+'tmp_full.bmp', dir_solid_pic+'Imfull.bmp')
    if dd1 < 20:
        return 1
    return 0


def is_hamberger():
    window_capture(dir_tmp_pic+'3_tt.bmp', 316, 272, 715, 393)
    dd1 = rms_difference(dir_tmp_pic+'3_tt.bmp', dir_solid_pic+'3_hamberger.bmp')
    if dd1 < 20:
        return 1
    return 0


def is_40_crystal_buy():
    window_capture(dir_tmp_pic+'40_tmp.bmp', 620, 400, 660, 480)
    dd1 = rms_difference(dir_tmp_pic+'40_tmp.bmp', dir_solid_pic+'40_crystal_buy_stamina.bmp')
    print("40_crystal, dd: %f" % dd1)
    if dd1 < 20:
        return 1
    return 0


def is_60_crystal_buy():
    window_capture(dir_tmp_pic+'60_tmp.bmp', 620, 400, 660, 480)
    dd1 = rms_difference(dir_tmp_pic+'60_tmp.bmp', dir_solid_pic+'60_crystal_buy_stamina.bmp')
    print("60_crystal, dd: %f" % dd1)
    if dd1 < 20:
        return 1
    return 0


def is_100_crystal_buy():
    window_capture(dir_tmp_pic+'100_tmp.bmp', 560, 450, 660, 480)
    dd1 = rms_difference(dir_tmp_pic+'100_tmp.bmp', dir_solid_pic+'100_crystal_buy_stamina.bmp')
    print("100_crystal, dd: %f" % dd1)
    if dd1 < 20:
        return 1
    return 0


def is_alchemy():
    window_capture(dir_tmp_pic+'26_tmp.bmp', 902, 30, 1000, 100)
    dd1 = rms_difference(dir_tmp_pic+'26_tmp.bmp', dir_solid_pic+'26_alchemy.bmp')
    print('alchemy dd1: ' + str(dd1))
    if dd1 < 20:
        return 1
    return 0


def is_drill():
    window_capture(dir_tmp_pic+'24_tmp.bmp', 902, 30, 1000, 100)
    dd1 = rms_difference(dir_tmp_pic+'24_tmp.bmp', dir_solid_pic+'24_drill.bmp')
    print('drill dd1: ' + str(dd1))
    if dd1 < 20:
        return 1
    return 0


def is_store():
    window_capture(dir_tmp_pic+'22_tmp.bmp', 902, 30, 1000, 100)
    dd1 = rms_difference(dir_tmp_pic+'22_tmp.bmp', dir_solid_pic+'22_store.bmp')
    #('is_in_store, dd:', dd1)
    if dd1 < 20:
        return 1
    return 0
    
    
def is_cancel_team():
    window_capture(dir_tmp_pic+'16_tmp.bmp', 300, 300, 700, 500)
    dd1 = rms_difference(dir_tmp_pic+'16_tmp.bmp', dir_solid_pic+'16_cancel_team.bmp')
    #('is_cancel_team, dd:', dd1)
    if dd1 < 20:
        return 1
    return 0


def is_re_invite():
    window_capture(dir_tmp_pic+'17_tmp.bmp', 400, 300, 600, 500)
    dd1 = rms_difference(dir_tmp_pic+'17_tmp.bmp', dir_solid_pic+'17_re_invite.bmp')
    #('is_re_invite, dd:', dd1)
    if dd1 < 20:
        return 1
    return 0


def is_captain():
    window_capture(dir_tmp_pic+'18_tmp.bmp', 772, 568, 890, 600)
    window_capture(dir_tmp_pic+'20_tmp.bmp', 772, 568, 890, 600)
    dd1 = rms_difference(dir_tmp_pic+'18_tmp.bmp', dir_solid_pic+'18_start_captain.bmp')
    dd2 = rms_difference(dir_tmp_pic+'20_tmp.bmp', dir_solid_pic+'20_gray_captain.bmp')
    #('is_re_invite, dd:', dd1, dd2)
    if dd1 < 20 or dd2 < 20:
        return 1
    return 0


def is_summon():
    window_capture(dir_tmp_pic+'tmp_summon.bmp', 800, 33, 1000, 93)
    dd1 = rms_difference(dir_tmp_pic+'tmp_summon.bmp', dir_solid_pic+'41_summon.bmp')
    if dd1 < 20:
        print('yes summon')
        return 1
    return 0


def is_friend():
    window_capture(dir_tmp_pic+'tmp_friend.bmp', 200, 650, 400, 700)
    dd1 = rms_difference(dir_tmp_pic+'tmp_friend.bmp', dir_solid_pic+'42_friend.bmp')
    if dd1 < 20:
        return 1
    return 0


def is_hero():
    window_capture(dir_tmp_pic+'tmp.bmp', 230, 100, 310, 130)
    dd1 = rms_difference(dir_tmp_pic+'tmp.bmp', dir_solid_pic+'44_hero.bmp')
    if dd1 < 20:
        return 1
    return 0


def is_full_level():
    window_capture(dir_tmp_pic+'tmp.bmp', 310, 360, 690, 535)
    dd1 = rms_difference(dir_tmp_pic+'tmp.bmp', dir_solid_pic+'45_full_level.bmp')
    if dd1 < 20:
        return 1
    return 0


def get_empty():
    window_capture(dir_tmp_pic+'23_4_tmp.bmp',731, 267, 840, 300)
    window_capture(dir_tmp_pic+'23_5_tmp.bmp',731, 424, 840, 451)
    window_capture(dir_tmp_pic+'23_6_tmp.bmp',731, 575, 840, 604)
    dd1 = rms_difference(dir_tmp_pic+'23_4_tmp.bmp', dir_solid_pic+'23_4_empty.bmp')
    dd2 = rms_difference(dir_tmp_pic+'23_5_tmp.bmp', dir_solid_pic+'23_5_empty.bmp')
    dd3 = rms_difference(dir_tmp_pic+'23_6_tmp.bmp', dir_solid_pic+'23_6_empty.bmp')
    print('get empty: ', dd1, dd2, dd3)
    num_empty = 0
    if dd1 < 20:
        num_empty +=1
    if dd2 < 20:
        num_empty +=1
    if dd3 < 20:
        num_empty +=1
    return num_empty


def get_complete():
    window_capture(dir_tmp_pic+'23_1_tmp.bmp',731, 267, 840, 300)
    window_capture(dir_tmp_pic+'23_2_tmp.bmp',731, 424, 840, 451)
    window_capture(dir_tmp_pic+'23_3_tmp.bmp',731, 575, 840, 604)
    dd1 = rms_difference(dir_tmp_pic+'23_1_tmp.bmp', dir_solid_pic+'23_1_complete.bmp')
    dd2 = rms_difference(dir_tmp_pic+'23_2_tmp.bmp', dir_solid_pic+'23_2_complete.bmp')
    dd3 = rms_difference(dir_tmp_pic+'23_3_tmp.bmp', dir_solid_pic+'23_3_complete.bmp')
    print('get complete: ', dd1, dd2, dd3)
    num_complete = 0
    if dd1 < 20:
        num_complete +=1
    if dd2 < 20:
        num_complete +=1
    if dd3 < 20:
        num_complete +=1
    return num_complete


def training(index_project=0, index_lv=0):
    # 全部,  女神，第一个训练，第二个训练
    #y1 = [151, 210, 280, 350, 420, 490, 560, 630, 700, 750]  # max=768
    #      65,  60,  55,  50,  45,  40,  35,  30,  25,  20
    #y2 = [640, 580, 520, 470, 410, 356, 298, 245, 202 ]
    #   女神，第一个训练，第二个训练
    y1 = [210, 280, 350, 420, 490, 560, 630, 700, 750]  # max=768
    #      65,  60,  55,  50,  45,  40,  35,  30,  25,  20
    y2 = [640, 580, 520, 470, 410, 356, 298, 245, 202 ]
    click(190,y1[index_project]) 
    wait_rand(0.4)
    drag(373,592,373,378)
    wait_rand(0.8)
    click(370,y2[index_lv])

    wait_rand(0.5)
    auto_team()   # click auto team


def event_training(index_project=0, index_lv=0):
    print('event training:')
    print(index_project, index_lv)
    #   樱花
    y1 = [140, 210, 280, 350, 420, 490, 560]
    y2 = [200, 255, 310, 365, 430, 475, 535, 600]
    y3 = [640, 580, 520, 470, 410, 356, 298, 245, 202,    316, 260, 200, 146]
        
    print(370,y3[index_lv])
    click(190,y1[index_project]) 
    wait_rand(0.8)
    if index_lv > 0:
        drag(373,592,373,378)

    wait_rand(1.0)
    click(370,y3[index_lv])
    wait_rand(0.5)
    auto_team()   # click auto team


def solo_event(index_project=0, index_level=0):
    # ['0剧院', '+1协会据点', '+2日落之镇', '+3时空之门', '+4朝霞之港']
    move_resize_window()
    wait_rand(0.5)
    mouse_wheel(-1)
    wait_rand(0.5)
    mouse_wheel(-1)
    wait_rand(0.5)
    x_drag = [-1,-1,-1, 1, 1]
    y_drag = [-1, 1,-1, 1,-1]
    x1 = [790, 780, 525, 505, 489]
    y1 = [126, 561, 203, 555, 200]
    for i in range(3):
        wait_rand(0.5)
        simple_drag(x_drag[index_project], y_drag[index_project])

    wait_rand(0.5)
    click(x1[index_project],y1[index_project]) # open options

    wait_rand(2.0)

    win32api.SetCursorPos((100, 100))
    wait_rand(1.5)
    window_capture(dir_tmp_pic+'13_tmp.bmp', 457,232,575,260, scaling_factor = 1.0)
    rms_dd = rms_difference(dir_tmp_pic+'13_tmp.bmp', dir_solid_pic+'13_location_selected.bmp')
    print('rms_camp_selected:', rms_dd)
    x2 = [640, 640, 640, 640, 640]
    y2 = [355, 473, 295, 410, 527]
    cancel_top_most()
    if rms_dd < 20:
        if index_level < 0:
            drag(490,500,500,255)
            wait_rand(0.5)
            drag(490,500,500,255)
            wait_rand(0.5)
        click(x2[index_level], y2[index_level])

    return rms_dd


def friend_summon():
    stage = cdll_determine_stage()
    if stage != 1:
        back_click()
        wait_rand(0.5)
        back_click()
        wait_rand(0.5)
        back_click()
        wait_rand(0.5)
        back_click()
        wait_rand(0.5)

    click(373,715) # summon
    wait_rand(1.0)
    click(373,715) # summon
            
    if is_summon() == 0:
        return 2
    elif is_summon() == 1:
        drag(918,530,918,200)
        wait_rand(0.3)
        drag(918,530,918,200)
        wait_rand(0.3)
        click(914,332)
        wait_rand(0.2)
        click(914,435)
        wait_rand(0.3)
        click(914,525)
        wait_rand(0.2)
        click(914,634)
        wait_rand(0.3)
        click(914,734)
        wait_rand(0.3)
        if is_friend() == 0:
            return 3
        elif is_friend() == 1:
            click(300,672)
            wait_rand(4.0)
            drag(500, 200, 550, 600)
            wait_rand(0.2)
            drag(500, 200, 550, 600)
            wait_rand(4.0)
            for i in range(5):
                click(970, 60)
                wait_rand(0.8)
            
            click(358,592) 
            wait_rand(2.0)
            back_click()
            return 0


def exp_magic():
    stage = cdll_determine_stage()
    if stage != 1:
        back_click()
        wait_rand(0.5)
        back_click()
        wait_rand(0.5)
        back_click()
        wait_rand(0.5)
        back_click()
        wait_rand(0.5)
    click(187,715) # click hero
    wait_rand(1.0)
    click(187,715) # click hero

    ah = is_hero()
    if ah == 0:
        return 2
    elif ah == 1:
        drag(100,600,100,200)
        wait_rand(0.3)
        drag(100,600,100,200)
        wait_rand(0.3)
        drag(100,600,100,200)
        wait_rand(0.3)
        drag(100,600,100,200)
        wait_rand(0.3)
        drag(100,600,100,200)
        wait_rand(1.0)

        click(85,287)
        wait_rand(0.4)
        click(90,287)
        wait_rand(0.4)
        click(95,287)
        wait_rand(0.4)
        click(977,498) # hero detail
        wait_rand(0.3)
        click(962,181) # information
        wait_rand(0.5)
        click(830,152) # exp +
        wait_rand(0.5)
        click(346,459) # mini exp item
        wait_rand(0.4)
        a = is_full_level()
        if a == 1:
            click(585,496)
            wait_rand(1.0)
            back_click()
            wait_rand(0.5)
        elif a == 0:
            back_click()
            wait_rand(0.5)

        click(963,431) # equipments
        wait_rand(1.0)
        click(769,633) # quick equipments on
        wait_rand(1.8)
        click(584,221) # weapon
        wait_rand(0.8)
        click(178,542) # forge
        wait_rand(2)
        click(955,483) # magic augmenting
        wait_rand(0.4)
        drag(100,600,100,200)
        wait_rand(0.3)
        drag(100,600,100,200)
        wait_rand(0.3)
        click(126,600) # choos a magic ticket
        wait_rand(0.5)
        click(690,630) # magic augment
        wait_rand(0.5)
        click(674,335) # stop rand
        wait_rand(0.5)
        click(674,335) # stop rand
        wait_rand(0.5)
        click(835,178) # abondon
        wait_rand(0.5)
        click(600,474)
        wait_rand(1.0)
        back_click()
        wait_rand(1.0)
        back_click()
        wait_rand(1.0)
        back_click()
        wait_rand(1.0)
        back_click()
        wait_rand(1.0)
        return 0

