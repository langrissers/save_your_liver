#coding=utf-8
import langrisser
import time
import random
import tkinter as tk
import tkinter.ttk as ttk
import threading
import datetime
import os


__version__ = ''
dir_solid_pic = 'pics\/'
class app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.init_vars()
        self.init_ui()

    def init_vars(self):
        self.num_debug = 0
        self.stage = 0
        self.close_sign = 0
        self.run_sign = 0
        self.num_ham = 0
        self.intv_solo_var = tk.IntVar()
        self.intv_harvest_var = tk.IntVar()
        self.strv_event = tk.StringVar()
        self.strv_project = tk.StringVar()
        self.strv_level = tk.StringVar()
        self.intv_max_ham = tk.IntVar(self,0)
        self.strv_level = tk.StringVar()
        self.text_currentham = tk.StringVar()
        self.intv_num_f_voucher = tk.IntVar(self,10)
        self.intv_num_special_enhancement = tk.IntVar()
        self.strv_special_enhancement_type = tk.StringVar()
        self.task_sequence = []
        self.current_task = 0
        self.strv_seq_total = tk.StringVar(self, 0)
        self.strv_seq1_project = tk.StringVar()
        self.strv_seq2_project = tk.StringVar()
        self.strv_seq3_project = tk.StringVar()
        self.strv_seq4_project = tk.StringVar()
        self.strv_seq1_level = tk.StringVar()
        self.strv_seq2_level = tk.StringVar()
        self.strv_seq3_level = tk.StringVar()
        self.strv_seq4_level = tk.StringVar()
        self.intv_seq1_num = tk.IntVar()
        self.intv_seq2_num = tk.IntVar()
        self.intv_seq3_num = tk.IntVar()
        self.intv_seq4_num = tk.IntVar()
        self.strv_crystall_buy_stamina = tk.StringVar()
        # projects = ['trial_lucy', 'swordman', 'archer', 'piker', 'sky_water', 'rider', 'magic']
        self.levels = ['LV. 70', 'LV. 65', 'LV. 60', 'LV. 55', 'LV. 50',
                     'LV. 45', 'LV. 40', 'LV. 35', 'LV. 30']
        self.stage_list = ['None', 'event_map', 'prepare', 'hamberger', 'fighting', # index = 4
            'victory', 'before_auto', 'be_invited', 'gym', 'trial', 'team', # index = 10
             'None','None','None','None','more_reward',] # idnex = 15
        for i in range(10):
            self.stage_list.append('None')

        self.log_message = tk.StringVar(self, '忠告：')
        self.text_stage = tk.StringVar(self, '当前状态：' + self.stage_list[0])


    def init_ui(self):
        self.title('726479602这是神秘数字' + __version__)
        self.geometry('400x700+1100+100')
        self.configure(background='white')
        self.setting_frame = tk.LabelFrame(self, width=400, height=300, bg='white', text='设置')
        self.sequence_frame = tk.LabelFrame(self, width=400, height=200, bg='white', text='系列任务，先进行系列任务，然后无限循环上边的任务')
        self.state_frame = tk.LabelFrame(self, width=400, height=200, bg='white', text='数据')
        #self.log_frame = tk.LabelFrame(self, width=400, height=150, bg='white', text='日志')
        self.setting_frame.grid(row=0, column=0, sticky='wens')
        self.sequence_frame.grid(row=1, column=0, sticky='wens')
        self.state_frame.grid(row=2, column=0, sticky='wens')
        #self.log_frame.grid(row=3, column=0, sticky='wens')

        dx = 60
        dy = 25
 
        # FRAMES
        # self.setting_frame
        xx = 0
        yy = 0
        self.l_is_event = ttk.Label(self.setting_frame, text='打活动吗', background='white', width=10)
        self.l_is_event.place(x=xx, y=yy)
        xx += dx
        yy += 0
        self.c_is_event = ttk.Combobox(self.setting_frame, textvariable=self.strv_event, width=10)
        self.c_is_event.bind('<<ComboboxSelected>>', self.event_selected)
        self.c_is_event['state'] = 'readonly'
        self.c_is_event.place(x=xx, y=yy)
        self.c_is_event['values'] = ('不，我要刷兄贵', '刷活动')
        self.c_is_event.current(0)
        xx  = 0
        yy += dy
 
        self.l_project = ttk.Label(self.setting_frame, text='选个任务', background='white', width=10)
        self.l_project.place(x=xx, y=yy)
        xx += dx
        yy += 0
        self.c_project = ttk.Combobox(self.setting_frame, textvariable=self.strv_project, width=10)
        self.c_project.bind('<<ComboboxSelected>>', self.project_selected)
        self.c_project['state'] = 'readonly'
        #self.c_project.current(0)
        self.c_project.place(x=xx, y=yy)
        xx += dx*2
        yy += 0
 
        self.l_level = ttk.Label(self.setting_frame, text='选个等级', background='white', width=10)
        self.l_level.place(x=xx, y=yy)
        xx += dx
        yy += 0
        self.c_level = ttk.Combobox(self.setting_frame, textvariable=self.strv_level, width=10)
        self.c_level['state'] = 'readonly'
        self.c_level['values'] = tuple(self.levels)
        self.c_level.current(0)
        self.c_level.place(x=xx, y=yy)
        xx = 0
        yy += dy
 
        self.l_maxham = ttk.Label(self.setting_frame, text='最多汉堡', background='white', width=10)
        self.l_maxham.place(x=xx, y=yy)
        xx += dx
        yy += 0
        self.e_maxham = ttk.Entry(self.setting_frame, textvariable=self.intv_max_ham, width=10)
        self.e_maxham.place(x=xx, y=yy)
        xx += dx*2
        yy += 0
        self.cb_solo = tk.Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.intv_solo_var, text='单人作战，仅支持兄贵和龙', background='white', width=30, command=self.solo_change)
        self.cb_solo.place(x=xx, y=yy)
        
        xx  = 0
        yy += dy
        self.b_start = ttk.Button(self.setting_frame, text='开始(序列任务优先)', width=20, command=self.start)
        self.b_start.place(x=xx, y=yy)
        xx += 4*dx
        yy += 0
        self.b_stop = ttk.Button(self.setting_frame, text='停止', width=20, command=self.stop)
        self.b_stop.place(x=xx, y=yy)
        xx = 0
        yy += int(1.5*dy)

        self.cb_harvest = tk.Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.intv_harvest_var, text='记录收成?', background='white', width=10)
        self.cb_harvest.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.b_check_harvest = ttk.Button(self.setting_frame, text='检查收成', width=16, command=self.check_harvest)
        self.b_check_harvest.place(x=xx, y=yy)
        xx = 0
        yy += int(1.5*dy)

        self.c_crystal_buy_stamina = ttk.Combobox(self.setting_frame, textvariable=self.strv_crystall_buy_stamina, width=10)
        self.c_crystal_buy_stamina['values'] = tuple(['穷不吃钻石','40钻', '60钻', '100钻', '不知道多少'])
        self.c_crystal_buy_stamina['state'] = 'readonly'
        self.c_crystal_buy_stamina.current(0)
        self.c_crystal_buy_stamina.place(x=xx, y=yy)
        xx = 0
        yy += int(1.5*dy)
        self.l_stage = ttk.Label(self.setting_frame, textvariable=self.text_stage, background='white')
        self.l_stage.place(x=xx, y=yy)
        xx = 0
        yy += dy
        self.l_message = ttk.Label(self.setting_frame, textvariable=self.log_message, background='white')
        self.l_message.place(x=xx, y=yy)
        

        # self.sequence_frame
        self.wday = time.localtime().tm_wday
        self.weekday = ['一', '二', '三', '四', '五', '六', '日']
        self.items_today = [ '' for i in range(7)]
        self.items_today[0] = '火龙    剑士    弓手    羁绊    经验'
        self.items_today[1] = '冰龙    枪兵    飞水    羁绊    经验'
        self.items_today[2] = '雷龙    骑兵    魔法    羁绊    经验'
        self.items_today[3] = '火龙    剑士    弓手    羁绊    经验'
        self.items_today[4] = '冰龙    枪兵    飞水    羁绊    经验'
        self.items_today[5] = '雷龙    骑兵    魔法    羁绊    经验'
        self.items_today[6] = '暗龙    剑士    弓手    枪兵    飞水    骑兵    魔法    羁绊    经验'
        # print(self.items_today)
        self.real_items = self.items_today[self.wday].split('    ')
        self.c_project['values'] = tuple(self.real_items)
        self.c_project.current(0)
        self.show_broadcast = []
        self.show_broadcast.append('今天是星期' + self.weekday[self.wday])
        self.show_broadcast.append('今天有' + self.items_today[self.wday])
        self.l1_weekday = ttk.Label(self.sequence_frame, text=self.show_broadcast[0], background='white')
        self.l2_weekday = ttk.Label(self.sequence_frame, text=self.show_broadcast[1], background='white')
        xx = 0
        yy = 0
        self.l1_weekday.place(x=xx, y=yy)
        yy += dy
        self.l2_weekday.place(x=xx, y=yy)
        yy += dy


        # sequence setting
        xx = 0
        yy += 0
        self.c_seq1_project = ttk.Combobox(self.sequence_frame, textvariable=self.strv_seq1_project, width=10)
        self.c_seq1_project['values'] = tuple(self.real_items)
        self.c_seq1_project['state'] = 'readonly'
        self.c_seq1_project.current(0)
        self.c_seq1_project.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.c_seq1_level = ttk.Combobox(self.sequence_frame, textvariable=self.strv_seq1_level, width=10)
        self.c_seq1_level['state'] = 'readonly'
        self.c_seq1_level['values'] = tuple(['LV. 65(70龙)', 'LV. 60(65龙)', 'LV. 55', 'LV. 50', 'LV.45', 'LV.40', 'LV.35'])
        self.c_seq1_level.current(0)
        self.c_seq1_level.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.c_seq1_num = ttk.Entry(self.sequence_frame, textvariable=self.intv_seq1_num, background='white')
        self.c_seq1_num.place(x=xx, y=yy)
        xx = 0
        yy += dy

        self.c_seq2_project = ttk.Combobox(self.sequence_frame, textvariable=self.strv_seq2_project, width=10)
        self.c_seq2_project['values'] = tuple(self.real_items)
        self.c_seq2_project['state'] = 'readonly'
        self.c_seq2_project.current(0)
        self.c_seq2_project.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.c_seq2_level = ttk.Combobox(self.sequence_frame, textvariable=self.strv_seq2_level, width=10)
        self.c_seq2_level['state'] = 'readonly'
        self.c_seq2_level['values'] = tuple(['LV. 65(70龙)', 'LV. 60(65龙)', 'LV. 55', 'LV. 50', 'LV.45', 'LV.40', 'LV.35'])
        self.c_seq2_level.current(0)
        self.c_seq2_level.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.c_seq2_num = ttk.Entry(self.sequence_frame, textvariable=self.intv_seq2_num, background='white')
        self.c_seq2_num.place(x=xx, y=yy)
        xx = 0
        yy += dy

        self.c_seq3_project = ttk.Combobox(self.sequence_frame, textvariable=self.strv_seq3_project, width=10)
        self.c_seq3_project['values'] = tuple(self.real_items)
        self.c_seq3_project['state'] = 'readonly'
        self.c_seq3_project.current(0)
        self.c_seq3_project.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.c_seq3_level = ttk.Combobox(self.sequence_frame, textvariable=self.strv_seq3_level, width=10)
        self.c_seq3_level['state'] = 'readonly'
        self.c_seq3_level['values'] = tuple(['LV. 65(70龙)', 'LV. 60(65龙)', 'LV. 55', 'LV. 50', 'LV.45', 'LV.40', 'LV.35'])
        self.c_seq3_level.current(0)
        self.c_seq3_level.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.c_seq3_num = ttk.Entry(self.sequence_frame, textvariable=self.intv_seq3_num, background='white')
        self.c_seq3_num.place(x=xx, y=yy)
        xx = 0
        yy += dy

        self.c_seq4_project = ttk.Combobox(self.sequence_frame, textvariable=self.strv_seq4_project, width=10)
        self.c_seq4_project['values'] = tuple(self.real_items)
        self.c_seq4_project['state'] = 'readonly'
        self.c_seq4_project.current(0)
        self.c_seq4_project.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.c_seq4_level = ttk.Combobox(self.sequence_frame, textvariable=self.strv_seq4_level, width=10)
        self.c_seq4_level['state'] = 'readonly'
        self.c_seq4_level['values'] = tuple(['LV. 65(70龙)', 'LV. 60(65龙)', 'LV. 55', 'LV. 50', 'LV.45', 'LV.40', 'LV.35'])
        self.c_seq4_level.current(0)
        self.c_seq4_level.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.c_seq4_num = ttk.Entry(self.sequence_frame, textvariable=self.intv_seq4_num, background='white')
        self.c_seq4_num.place(x=xx, y=yy)
        xx = 0
        yy += dy


        self.l_seq_total = ttk.Label(self.sequence_frame, textvariable=self.strv_seq_total, background='white')
        self.l_seq_total.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.b_add_sequence = ttk.Button(self.sequence_frame, text='加入计划', command=self.add1_sequence)
        self.b_add_sequence.place(x=xx, y=yy)

        xx += 2*dx
        yy += 0
        self.b_clear_sequence = ttk.Button(self.sequence_frame, text='清空', command=self.clear1_sequence)
        self.b_clear_sequence.place(x=xx, y=yy)

        # end sequence
        
        # self.state_frame
        xx = 0
        yy = 0
        self.text_currentham = tk.StringVar(self, '汉堡数目，当前/目标总数：' + str(self.num_ham) + '/' + str(self.intv_max_ham.get()))
        self.l_currentham = ttk.Label(self.state_frame, textvariable=self.text_currentham, background='white')
        self.l_currentham.place(x=xx, y=yy)
        xx += 0
        yy += dy
        self.b_click_50 = ttk.Button(self.state_frame, text='点击右上角五十次', command=self.start_click_50)
        self.b_click_50.place(x=xx, y=yy)
        xx  = dx*2
        yy += 0
        self.b_cap_event = ttk.Button(self.state_frame, text='活动截图', command=self.cap_event)
        self.b_cap_event.place(x=xx, y=yy)
        xx += dx*2
        yy += 0
        self.b_summon_exp_magic = ttk.Button(self.state_frame, text='友情经验附魔三件套', command=self.start_summon_exp_magic)
        self.b_summon_exp_magic.place(x=xx, y=yy)
        xx  = 0
        yy += dy


        self.b_drill = ttk.Button(self.state_frame, text='练兵委托训练', command=self.start_drill)
        self.b_drill.place(x=xx, y=yy)
        xx  = 0
        yy += dy
        self.b_alchemy = ttk.Button(self.state_frame, text='辅助炼金', command=self.start_alchemy)
        self.b_alchemy.place(x=xx, y=yy)
        xx  = 0
        yy += dy
        self.b_buy_f_voucher = ttk.Button(self.state_frame, text='购买友情券', command=self.start_buy_voucher)
        self.b_buy_f_voucher.place(x=xx, y=yy)
        xx  = 0
        yy += dy
        self.l_num_f_voucher = ttk.Label(self.state_frame, text='友情券/附魔券数量: ', background='white')
        self.l_num_f_voucher.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.e_num_f_voucher = ttk.Entry(self.state_frame, textvariable=self.intv_num_f_voucher, background='white')
        self.e_num_f_voucher.place(x=xx, y=yy)
        xx  = 0
        yy += dy
        self.b_buy_middle = ttk.Button(self.state_frame, text='购买中级附魔', command=self.start_buy_middle)
        self.b_buy_middle.place(x=xx, y=yy)
        xx += 2*dx
        yy += 0
        self.c_special_enhancement_type = ttk.Combobox(self.state_frame, textvariable=self.strv_special_enhancement_type, width=10)
        self.c_special_enhancement_type['state'] = 'readonly'
        self.c_special_enhancement_type.place(x=xx, y=yy)
        self.c_special_enhancement_type['values'] = ('时钟', '魔术', '满月', '怒涛', '轻风', '烈日', '流星', '钢铁', '荆棘', '大树', '顽石', '寒冰', '水晶')
        self.c_special_enhancement_type.current(0)
        # end init_ui


    # call back functions
    def summon_exp_magic(self):
        self.log_message.set('summoning')

        a = langrisser.friend_summon()
        if a == 0:
            self.log_message.set('summon successed')
        else:
            self.log_message.set('summon failed')

        b = langrisser.exp_magic()
        if b == 0:
            self.log_message.set('exp magic successed')
        elif b == 2:
            self.log_message.set('exp magic failed 2')

        self.b_summon_exp_magic.config(state=tk.NORMAL)


    def start_summon_exp_magic(self):
        self.thread = threading.Thread(target=self.summon_exp_magic)
        self.thread.daemon = True
        self.thread.start()
        self.b_summon_exp_magic.config(state=tk.DISABLED)


    def check_harvest(self):
        os.startfile(langrisser.dir_harvest)

        
    def add1_sequence(self):
        for i in range(self.intv_seq1_num.get()):
            self.task_sequence.append([self.c_seq1_project.current(), self.c_seq1_level.current()])
        for i in range(self.intv_seq2_num.get()):
            self.task_sequence.append([self.c_seq2_project.current(), self.c_seq2_level.current()])
        for i in range(self.intv_seq3_num.get()):
            self.task_sequence.append([self.c_seq3_project.current(), self.c_seq3_level.current()])
        for i in range(self.intv_seq4_num.get()):
            self.task_sequence.append([self.c_seq4_project.current(), self.c_seq4_level.current()])

        self.strv_seq_total.set(str(len(self.task_sequence)))
        print(len(self.task_sequence))


    def clear1_sequence(self):
        self.task_sequence = []
        self.strv_seq_total.set(str(len(self.task_sequence)))


    def solo_change(self):
        if self.c_is_event.current() == 1:
            if self.intv_solo_var.get() == 0:
                self.c_level['values'] = tuple(self.event_team_levels)
            if self.intv_solo_var.get() == 1:
                self.c_level['values'] = tuple(self.event_solo_levels)
                self.c_level.current(2)


    def start_buy_middle(self):
        print('buy_middle button pressed')
        self.log_message.set('购买附魔')
        self.thread = threading.Thread(target=self.buy_middle)
        self.thread.daemon = True
        self.thread.start()
        self.b_buy_middle.config(state=tk.DISABLED)


    def buy_middle(self):
        if langrisser.is_store() == 1:
            langrisser.click(640,130)
            x_middle = [280, 395, 510, 625, 740]
            y_middle = [330, 440, 550]
            xxm1 = x_middle[self.c_special_enhancement_type.current() % 5]
            yym1 = y_middle[int(self.c_special_enhancement_type.current() / 5)]
            
            for i in range(self.intv_num_f_voucher.get()):
                langrisser.wait_rand(1.0)
                langrisser.click(765,240)
                langrisser.wait_rand(1.0)
                langrisser.click(xxm1,yym1)
                langrisser.wait_rand(1.0)
                langrisser.click(515,480)
                langrisser.wait_rand(1.0)
                langrisser.click(750,250)

        self.b_buy_middle.config(state=tk.NORMAL)


    def start_buy_voucher(self):
        print('buy voucher button pressed: ', self.intv_num_f_voucher.get())
        self.log_message.set('购买友情券: ' + str(self.intv_num_f_voucher.get()))
        self.thread = threading.Thread(target=self.buy_voucher)
        self.thread.daemon = True
        self.thread.start()
        self.b_buy_f_voucher.config(state=tk.DISABLED)
        

    def buy_voucher(self):
        if langrisser.is_store() == 1:
            langrisser.click(500,130)
            for i in range(self.intv_num_f_voucher.get()):
                langrisser.wait_rand(1.0)
                langrisser.click(200,250)
                langrisser.wait_rand(1.0)
                langrisser.click(479,492)
                langrisser.wait_rand(1.0)
                langrisser.click(500,700)

        self.b_buy_f_voucher.config(state=tk.NORMAL)
        
            
    def start_alchemy(self):
        print('alchemy button pressed')
        self.log_message.set('辅助炼金')
        self.thread = threading.Thread(target=self.alchemy)
        self.thread.daemon = True
        self.thread.start()
        self.b_alchemy.config(state=tk.DISABLED)


    def alchemy(self):
        if langrisser.is_alchemy() == 1:
            print('in alchemy')
            for n5 in range(5):
                for i in range(5):
                    for j in range(4):
                        langrisser.click(520+j*90, 240+i*90)
                        langrisser.wait_rand(0.2)
 
                langrisser.drag(520,600,520,340)
                langrisser.drag(520,600,520,340)
                langrisser.wait_rand(1.0)

        self.b_alchemy.config(state=tk.NORMAL)


    def cap_event(self):
        self.log_message.set('活动截图')
        langrisser.window_capture(dir_solid_pic+'1_event.bmp', 830, 43, 1000, 66)


    def start_click_50(self):
        self.log_message.set('乱点')
        self.thread = threading.Thread(target=self.click_50)
        self.thread.daemon = True
        self.thread.start()
        self.b_click_50.config(state=tk.DISABLED)


    def start_drill(self):
        print('drill button pressed')
        self.log_message.set('练兵')
        self.thread = threading.Thread(target=self.drill)
        self.thread.daemon = True
        self.thread.start()
        self.b_drill.config(state=tk.DISABLED)


    def drill(self):
        if langrisser.is_drill() == 1:
            print('in drill')

            if langrisser.get_complete() == 3:
                langrisser.click(781,281) # get 1st
                langrisser.wait_rand(2.0)
                langrisser.click(700,700)
                langrisser.wait_rand(1.5)
                langrisser.click(781,437) # get 2nd
                langrisser.wait_rand(2.0)
                langrisser.click(700,700)
                langrisser.wait_rand(1.5)
                langrisser.click(781,590) # get 3rd
                langrisser.wait_rand(2.0)
                langrisser.click(700,700)
                langrisser.wait_rand(1.5)
                langrisser.wait_rand(1.5)
                
            if langrisser.get_empty() == 3:
                print('empty and then drill')
                langrisser.click(781,281) # entrust 1st
                langrisser.wait_rand(1.4)
                langrisser.click(833,511) # 8 hour
                langrisser.wait_rand(0.8)
                langrisser.click(316,244) # click +
                langrisser.wait_rand(0.8)
                langrisser.click(363,263) # click 1
                langrisser.wait_rand(0.8)
                langrisser.click(668,416) # click 8
                langrisser.wait_rand(0.8)
                langrisser.click(363,548) # click 9
                langrisser.wait_rand(0.8)
                langrisser.click(633,629) # click ok
                langrisser.wait_rand(0.8)
                langrisser.click(665,615) # click ok
                langrisser.wait_rand(3.0)
                # 2
                langrisser.click(781,437) # entrust 2nd
                langrisser.wait_rand(0.8)
                langrisser.click(833,511) # 8 hour
                langrisser.wait_rand(0.8)
                langrisser.click(316,244) # click +
                langrisser.wait_rand(0.8)
                langrisser.click(465,263) # click 1
                langrisser.wait_rand(0.8)
                langrisser.click(460,412) # click 6
                langrisser.wait_rand(0.8)
                langrisser.click(559,416) # click 7
                langrisser.wait_rand(0.8)
                langrisser.click(633,629) # click ok
                langrisser.wait_rand(0.8)
                langrisser.click(665,615) # click ok
                langrisser.wait_rand(3.0)
                # 3
                langrisser.click(781,590) # entrust 3rd
                langrisser.wait_rand(0.8)
                langrisser.click(833,511) # 8 hour
                langrisser.wait_rand(0.8)
                langrisser.click(316,244) # click +
                langrisser.wait_rand(0.8)
                langrisser.click(560,263) # click 3
                langrisser.wait_rand(0.8)
                langrisser.click(659,263) # click 4
                langrisser.wait_rand(0.8)
                langrisser.click(367,412) # click 5
                langrisser.wait_rand(0.8)
                langrisser.click(633,629) # click ok
                langrisser.wait_rand(0.8)
                langrisser.click(665,615) # click ok
                langrisser.wait_rand(3.0)
        self.b_drill.config(state=tk.NORMAL)
        

    def click_50(self):
        for i in range(50):
            langrisser.click(1000, 57)
            langrisser.wait_rand(0.6)

        self.b_click_50.config(state=tk.NORMAL)

    def event_selected(self, event=None):
        if self.c_is_event.current() == 1:
            self.event_team_levels = ['0', '+1', '+2', '+3', '+4', '-4', '-3', '-2', '-1']
            self.event_solo_levels = ['+1', '+2', '-3', '-2', '-1']

            self.c_project['values'] = tuple(['0剧院', '+1协会据点', '+2日落之镇', '+3时空之门', '+4朝霞之港'])
            self.c_project.current(1)
            if self.intv_solo_var.get() == 1:
                self.c_level['values'] = tuple(self.event_solo_levels)
                self.c_level.current(2)
            elif self.intv_solo_var.get() == 0:
                self.c_level['values'] = tuple(self.event_team_levels)
                self.c_level.current(2)
        elif self.c_is_event.current() == 0:
            self.c_project['values'] = tuple(self.real_items)
            self.c_project.current(0)
            self.c_project.config(state=tk.NORMAL)
            self.c_level['values'] = tuple(['+1', '+2', '+3', '+4', '-4', '-3', '-2', '-1'])


    def project_selected(self, event=None):
        if self.c_is_event.current() == 1:  # event
            if self.c_project.current() == 0: 
                self.c_level['values'] = tuple(self.event_solo_levels)
                self.c_level.current(0)
            elif self.c_project.current() == 1:
                self.c_level['values'] = tuple(self.event_solo_levels)
                self.c_level.current(0)
            elif self.c_project.current() == 2:
                self.c_level['values'] = tuple(self.event_solo_levels)
                self.c_level.current(0)
            elif self.c_project.current() == 3:
                self.c_level['values'] = tuple(self.event_solo_levels)
                self.c_level.current(0)
            elif self.c_project.current() == 4:
                self.c_level['values'] = tuple(self.event_solo_levels)
                self.c_level.current(0)

        elif self.c_is_event.current() == 0:
            if self.c_project.current() == 0:
                # self.c_level['values'] = tuple(['+1', '+2', '+3', '+4', '-4', '-3', '-2', '-1'])
                self.c_level['values'] = tuple(self.levels)
                self.c_level.current(0)
            else:
                self.levels = ['LV. 65', 'LV. 60', 'LV. 55', 'LV. 50',
                            'LV. 45', 'LV. 40', 'LV. 35', 'LV. 30']
                self.c_level['values'] = tuple(self.levels)
                self.c_level.current(0)

            
    def start(self):
        print('cb: %d' % self.intv_solo_var.get())
        self.close_sign = 0
        print('start button pressed: ', self.intv_max_ham.get())
        self.text_currentham.set('汉堡数目，当前/目标总数：' + str(self.num_ham) + '/' + str(self.intv_max_ham.get()))
        self.thread = threading.Thread(target=self.run_loop)
        self.thread.daemon = True
        self.thread.start()
        self.b_start.config(state=tk.DISABLED)


    def stop(self):
        self.close_sign = 1
        langrisser.cancel_top_most()


    def run_loop(self):
        self.log_message.set('忠告：开始')

        while True:    # sequence loop
            if len(self.task_sequence) < 1:
                break

            self.log_message.set('忠告：正在进行系列任务')
            task_in_seq = self.task_sequence[0][0]
            level_in_seq = self.task_sequence[0][1]
            while True: # after one job done break and do another job
                main_return_code = self.main_loop(task_in_seq, level_in_seq)
                langrisser.cancel_top_most()
                if main_return_code == 5:
                    break
                elif main_return_code == -1:
                    return -1
                elif main_return_code == 3:
                    return 3

            self.task_sequence.pop(0)
            self.strv_seq_total.set(str(len(self.task_sequence)))

        # the main loop for 乌勒尔之弓
        while True:
            main_return_code = 0
            if self.c_is_event.current() == 0:
                self.log_message.set('忠告：正在进行活动任务')
                main_return_code = self.main_loop(self.c_project.current(), self.c_level.current())
            elif self.c_is_event.current() == 1:
                self.log_message.set('忠告：正在进行循环任务')
                main_return_code = self.main_loop(self.c_project.current(), self.c_level.current())

            if main_return_code == -1:
                langrisser.cancel_top_most()
                return -1
            elif main_return_code == 3:
                return 3
            

        return 0


    def main_loop(self, task_in_mainloop, level_in_mainloop):
            time.sleep(1)
            print('while begin')
            self.run_sign = 1
            if self.close_sign == 1:
                self.log_message.set('忠告：你点击了停止按钮, 这波分析完就停')
                print('stop button pressed, stop')
                self.run_sign = 0
                self.b_start.config(state=tk.NORMAL)
                langrisser.cancel_top_most()
                return -1

            t1 = time.time()
            self.stage = langrisser.cdll_determine_stage()
            t2 = time.time()
            print('time determine: ', t2-t1)

            self.text_stage.set('当前状态：' + str(self.stage))
            self.text_currentham.set('汉堡数目，当前/目标总数：' + str(self.num_ham) + '/' + str(self.intv_max_ham.get()))

            if self.stage == 100:
                langrisser.click(970, 286)

            elif self.stage in [351, 352, 353, 451, 452, 453, 551, 552, 553]:
                langrisser.click(645,355)

            elif self.stage == 1:
                print('event map')
                if self.intv_solo_var.get() == 1:
                    # langrisser.solo_event(self.c_project.current(), self.c_level.current())
                    langrisser.solo_event(self.c_project.current(), int(self.strv_level.get()))
                    
                elif self.intv_solo_var.get() == 0:
                    langrisser.click(965,715) # enter team play

            elif self.stage == 91 or self.stage == 92 or self.stage == 93 or self.stage == 95:
                if self.c_is_event.current() == 1:
                    langrisser.click(965,715) # enter team play
                else:
                    gym_all = ['剑士', '弓手', '枪兵', '飞水', '骑兵', '魔法']
                    if self.intv_solo_var.get() == 1:
                        y_gym = [220, 300, 380, 460, 540, 620]
                        langrisser.click(200, y_gym[gym_all.index(self.strv_project.get())])
                        langrisser.drag(440, 660, 440, 300)
                        langrisser.wait_rand(0.5)
                        langrisser.drag(440, 660, 440, 300)
                        langrisser.wait_rand(0.5)
                        x_solo = 850
                        y_solo = [680, 540, 400, 260, 120]
                        langrisser.click(x_solo,y_solo[self.c_level.current()])
                    else:
                        langrisser.click(965,715) # enter team play
            elif self.stage == 94: # 宝藏
                langrisser.click(966,670)
                langrisser.wait_rand(0.5)

            elif self.stage == 90:  # 组队
                print('index project, level:', self.c_project.current(), self.c_level.current())
                if self.c_is_event.current() == 1:
                    langrisser.event_training(task_in_mainloop, int(self.strv_level.get()))
                if self.c_is_event.current() == 0:
                    langrisser.training(task_in_mainloop, level_in_mainloop)
                self.current_task = [self.c_project.current(), self.c_level.current()]
                langrisser.wait_rand(4)
            elif self.stage == 2:  # press "出击"
                langrisser.click(955, 705)
                langrisser.wait_rand(1)
            elif self.stage == 3:
                print('stage3, checking c_crystal_buy_stamina.current: %d' % self.c_crystal_buy_stamina.current())
                if self.c_crystal_buy_stamina.current() >= 1:
                    if langrisser.is_40_crystal_buy() == 1:
                        langrisser.click(608,466)
                        return 0
                if self.c_crystal_buy_stamina.current() >= 2:
                    if langrisser.is_60_crystal_buy() == 1:
                        langrisser.click(608,466)
                        return 0
                if self.c_crystal_buy_stamina.current() >= 3:
                    if langrisser.is_100_crystal_buy() == 1:
                        langrisser.click(608,466)
                        return 0

                if self.num_ham >= self.intv_max_ham.get():
                    self.log_message.set('忠告：'+'够数啦，停了')
                    self.b_start.config(state=tk.NORMAL)
                    return 3

                langrisser.click(418, 462) # eat a hamberger
                langrisser.wait_rand(1)
                if langrisser.is_imfull() == 1:
                    langrisser.click(889, 312) # click to close the "full" stage
                    langrisser.wait_rand(2.2)
                    self.num_ham += 1
                    langrisser.auto_team() # click auto team
                    langrisser.wait_rand(3)
            elif self.stage == 4:  # fighting
                langrisser.wait_rand(10)
            elif self.stage == 5:  # victory
                langrisser.click(1000,57)
                langrisser.wait_rand(1)
                langrisser.window_capture(langrisser.dir_tmp_pic+'43_tmp.bmp', 31, 567, 144, 608)
                rms_dd = langrisser.rms_difference(langrisser.dir_tmp_pic+'43_tmp.bmp', langrisser.dir_solid_pic+'43_redo.bmp')
                if rms_dd < 20:
                    tt_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                    langrisser.window_capture(langrisser.dir_harvest+tt_str+r'.bmp', 0, 0, 1024, 768)
                    langrisser.wait_rand(1)
                    langrisser.click(90,586)
                    return 0

                langrisser.click(1000,57)
                langrisser.wait_rand(2)
                tt_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                langrisser.window_capture(langrisser.dir_harvest+tt_str+r'.bmp', 0, 0, 1024, 768)
                langrisser.wait_rand(1)
                for i in range(4):
                    langrisser.click(1000,57)
                    langrisser.wait_rand(2)
                return 5

            elif self.stage == 6:
                for i in range(3 + int(random.random()*5)):
                    langrisser.click(967,233)
                    langrisser.wait_rand(1)
            elif self.stage == 7:
                langrisser.click(140,300)
            elif self.stage == 11:
                langrisser.click(500,150)
            elif self.stage == 12:
                langrisser.wait_rand(3)
            elif self.stage == 15:
                for i in range(7):
                    langrisser.wait_rand(2)
                    langrisser.click(1000,407)
            elif self.stage == 17:
                langrisser.click(430, 471)
            elif self.stage == 18:
                langrisser.click(174, 584)
                
            if self.stage == 0:
                self.num_debug += 1
                if self.num_debug > 20:
                    self.num_debug = 0
                    langrisser.wait_rand(1)
                    langrisser.click(1000,407)

            if langrisser.is_cancel_team() == 1:
                langrisser.click(429,470)
                    
            langrisser.wait_rand(1)
            return 0
            # end main loop
                
            
a=app()
a.mainloop()
