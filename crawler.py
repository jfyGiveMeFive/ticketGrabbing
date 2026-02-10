#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
12306 火车票自动抢票工具
Python 3 现代化版本 - 使用 undetected-chromedriver
"""
import sys
import pdb
import time
import pygame
import sys
from configparser import ConfigParser
import argparse
#from splinter.browser import Browser
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from datetime import datetime, timedelta

import codecs # 解决 gbk 编码问题

class Ticket(object):
    def __init__(self, config_file):
        ## config parser setting
        self.config_file = config_file
        # 禁用插值以支持包含 % 符号的 cookie 值
        self.settings = ConfigParser(interpolation=None)
        # self.settings._interpolation = configparser.ExtendedInterpolation()
        # self.settings.read(self.config_file)
        # 解决 gbk 编码问题
        self.settings.read_file(codecs.open(self.config_file, "r", "utf-8-sig"))
        ## environment setting
        self.brower='chrome'
        self.b = None  # 浏览器将在配置验证后初始化
        self.station={}
        self.url = "https://kyfw.12306.cn/otn/leftTicket/init"
        # 席别类型(对应列标号)
        self.ticket_index = [
                            '',
                            u'商务座',
                            u'一等座', 
                            u'二等座',
                            u'高级软卧',
                            u'软卧',
                            u'动卧',
                            u'硬卧',
                            u'软座',
                            u'硬座',
                            u'无座'
                            ]
        self.seat_type = ['A', 'B', 'C', 'D', 'E']
        self.username = ''
        self.password = ''
        self.date_format='%Y-%m-%d'
        self.tolerance = -1
        self.blacklist = {}
        self.date = []
        self.isStudent = False
        self.success = 0
        self.find_ticket = 0
        self.config_parser()
        self.playmusic = False
        self.count = 0

    def ConfigSectionMap(self,section):
            dict1 = {}
            options = self.settings.options(section)
            for option in options:
                try:
                    dict1[option] = self.settings.get(section, option)
                    if dict1[option] == -1:
                        DebugPrint("skip: %s" % option)
                except:
                        print("exception on %s!" % option)
                        dict1[option] = None
            return dict1
    def daterange(self, start_date, end_date):
        for n in range(int ((end_date - start_date).days) + 1):
            yield start_date + timedelta(n) 

    def config_parser(self):
        if self.retrieve_station_dict() == -1:
            sys.exit()
        if self.retrieve_book_options() == -1:
            sys.exit()
        # 验证配置
        if not self.validate_config():
            sys.exit(1)
        
    def retrieve_station_dict(self):
        dict_helper=self.ConfigSectionMap('STATIONCOOKIE')
        for name, value in dict_helper.items():
            self.station[name]=value

    def retrieve_book_options(self):
        login_info=self.ConfigSectionMap('GLOBAL')
        self.username = login_info['username'].strip()
        self.password = login_info['password'].strip()
        self.brower = login_info.get('browser', 'chrome').strip()
        book_settings = self.ConfigSectionMap('TICKET')
        self.fromStation = [ station.strip() for station in book_settings['from_station'].split(',')]
        self.toStation = [ station.strip() for station in book_settings['to_station'].split(',')]
        trains = [ train.strip() for train in book_settings['trains'].split(',')]
        if len(trains) == 1 and trains[0] == '':
            self.trains = []
        else:
            self.trains =  trains
        self.ticket_type =[ _type.strip() for _type in book_settings['ticket_type'].split(',')]
        rangeQuery = book_settings['range_query'].strip()
        if rangeQuery == 'Y':
            date = [ d.strip() for d in book_settings['date'].split(',')]
            if len(date) < 2:
                print("未设置正确的起至时间")
                return -1
            else:
                start_date = datetime.strptime(date[0],self.date_format)
                end_date = datetime.strptime(date[1],self.date_format)
                if end_date < start_date:
                    print("查询截止日期不可大于开始日期!")
                    return -1
                for single_date in self.daterange(start_date, end_date): 
                    self.date.append(single_date.strftime(self.date_format))
        else:
            self.date = [ d.strip() for d in book_settings['date'].split(',')]
        if book_settings['student'].strip() == 'Y':
            self.isStudent = True
        self.tolerance = int(book_settings['tolerance'])
        self.people = [ people.strip() for people in book_settings['people'].split(',') ]
        if book_settings['alarm'].strip() == 'Y':
            print('已打开音乐提醒')
            self.playmusic = True

    def validate_config(self):
        """验证配置文件的正确性"""
        errors = []

        # 验证必填字段
        if not self.username or not self.password:
            errors.append("❌ 用户名或密码未设置")

        if not self.fromStation or not self.toStation:
            errors.append("❌ 起始站或到达站未设置")

        if not self.date:
            errors.append("❌ 出发日期未设置")

        if not self.people:
            errors.append("❌ 乘车人未设置")

        # 验证车站 Cookie 是否存在
        for station in self.fromStation + self.toStation:
            if station not in self.station:
                errors.append(f"❌ 车站 '{station}' 的 Cookie 未在 [STATIONCOOKIE] 中配置")

        # 验证席别类型
        for ticket_type in self.ticket_type:
            if ticket_type not in self.ticket_index:
                errors.append(f"❌ 无效的席别类型: '{ticket_type}'")

        # 验证日期格式
        for date in self.date:
            try:
                datetime.strptime(date, self.date_format)
            except ValueError:
                errors.append(f"❌ 日期格式错误: '{date}'，应为 YYYY-MM-DD")

        if errors:
            print("\n配置文件验证失败：\n")
            for error in errors:
                print(error)
            print("\n请检查配置文件: " + self.config_file)
            return False

        print("✅ 配置文件验证通过")
        return True

    def init_browser(self):
        """初始化浏览器（在配置验证后调用）"""
        if self.b is None:
            options = uc.ChromeOptions()
            options.add_argument('--disable-blink-features=AutomationControlled')
            # 指定 Chrome 主版本号为 144，匹配已安装的 Chrome 版本
            try:
                self.b = uc.Chrome(options=options, version_main=144, use_subprocess=True)
            except Exception as e:
                print(f"无法启动 Chrome: {e}")
                print("请确保已安装 Google Chrome: brew install --cask google-chrome")
                raise

    def login(self):
        """登录方法 - 已更新以适配 2026 年的 12306 网站结构"""
        self.b.get(self.url)
        tag_name = u"登录"
        try:
            # 等待登录链接出现并点击
            print("🔍 正在查找登录链接...")
            login_link = WebDriverWait(self.b, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, tag_name))
            )
            login_link.click()
            print("✅ 已点击登录链接")

            # 等待页面加载
            time.sleep(2)

            print(f"📍 当前页面: {self.b.current_url}")

            # 使用新的元素 ID (12306 网站已更新)
            print("🔍 正在查找用户名输入框 (J-userName)...")
            username = WebDriverWait(self.b, 10).until(
                EC.presence_of_element_located((By.ID, "J-userName"))
            )
            print("✅ 找到用户名输入框")

            print("🔍 正在查找密码输入框 (J-password)...")
            password = WebDriverWait(self.b, 10).until(
                EC.presence_of_element_located((By.ID, "J-password"))
            )
            print("✅ 找到密码输入框")

            # 输入用户名和密码
            print(f"📝 正在输入用户名: {self.username}")
            username.clear()
            username.send_keys(self.username)

            print("📝 正在输入密码...")
            password.clear()
            password.send_keys(self.password)

            print("\n✅ 用户名和密码已填写")
            print("⚠️  注意：12306 现在使用滑动验证码或其他验证方式")
            print("请在浏览器中手动完成验证并登录")
            print("\n按 'c' 继续执行脚本...")

            import pdb
            pdb.set_trace()

        except TimeoutException as e:
            print(f"❌ 登录页面加载超时: {e}")
            print("可能原因：")
            print("1. 网络连接问题")
            print("2. 页面加载时间过长")
            print(f"\n当前页面 URL: {self.b.current_url}")
            print(f"当前页面标题: {self.b.title}")
            raise
        except Exception as e:
            print(f"❌ 登录过程出错: {e}")
            raise
    
    def page_has_loaded(self):
        #page_state = self.b.evaluate_script("document.readyState")
        #return page_state == 'complete'
        delay = 3
        try:
            myElem = WebDriverWait(self.b, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'bgc')))
            return True
        except TimeoutException:
            return False

    def switch_to_order_page(self):
        while 1:
            order = self.b.find_element(By.LINK_TEXT, u"车票预订")
            if isinstance(order, WebElement):
                break
        order.click()

    def checkTicket(self, date, fromStation, toStation):
        print('date: %s, from %s, to %s'%(date, fromStation, toStation))
        self.b.add_cookie({'name': '_jc_save_fromDate', 'value': date})
        self.b.add_cookie({'name': '_jc_save_fromStation', 'value': self.station[fromStation]})
        self.b.add_cookie({'name': '_jc_save_toStation', 'value': self.station[toStation]})
        #self.b.cookies.all()
        self.b.refresh()
        if self.isStudent:
            self.b.find_element(By.LINK_TEXT, u'学生').click()
        self.b.find_element(By.LINK_TEXT, u"查询").click()

        if self.page_has_loaded() == False:
            return ''
        all_trains = self.b.find_elements(By.XPATH, '//table/tbody/tr/td/a[contains(@class, "btn72")]')
        this_train = ''
        for k, train in enumerate(all_trains):
            tds = train.find_elements(By.XPATH, "../../td")
            if tds and len(tds) >= 10:
                if k + 1 < len(all_trains):
                    this_train = tds[0].text.split('\n')[0] 
                    if len(self.trains) != 0 and this_train not in self.trains:
                        continue
                    if self.tolerance != -1 and this_train in self.blacklist and self.blacklist[this_train] >= self.tolerance:
                        print(u"%s 失败 %d 次, 跳过"%(this_train, self.blacklist[this_train]))
                        continue
                for cat in self.ticket_type:
                    if cat in self.ticket_index:
                        i = self.ticket_index.index(cat)
                    else:
                        print('❌ 无效的席别信息')
                        return 0, ''
                    if tds[i].text != u'无' and tds[i].text != '--':
                        if tds[i].text != u'有':
                            print(u'%s 的 %s 有余票 %s 张!'%(this_train, cat ,tds[i].text))
                        else:
                            print(u'%s 的 %s 有余票若干张!'%(this_train, cat))
                        self.find_ticket = 1
                        tds[-1].click()
                        break
            if self.find_ticket:
                break
        return this_train

    def book(self, train):
        while self.page_has_loaded() == False:
            continue
        if len(self.people) == 0:
            print('❌ 没有选择乘车人!')
            return 1
        try:
            more = self.b.find_element(By.LINK_TEXT, u"更多")
            more.click()
        except:
            pass
        people = self.people
        assert len(people) > 0, '至少提供一个乘客信息'
        try:
            person=self.b.find_element(By.XPATH, '//ul[@id="normal_passenger_id"]/li/label[contains(text(),"%s")]'%people[0])
        except:
            print(u'❌ 没找到乘客 %s'%people[0])
        for p in people:
            self.b.find_element(By.XPATH, '//ul[@id="normal_passenger_id"]/li/label[contains(text(),"%s")]'%p).click()
            style = self.b.find_element(By.XPATH, '//div[@id="dialog_xsertcj"]').get_attribute('style')
            if not ('display' in style and 'none' in style):
                self.b.find_element(By.XPATH, '//div[@id="dialog_xsertcj"]/div/div/div/a[text()="确认"]').click()
        self.b.find_element(By.ID, 'submitOrder_id').click()
        table = self.b.find_element(By.ID, 'checkticketinfo_id')
        if train.startswith('G') or  train.startswith('C') or  train.startswith('D'):
            seats = table.find_element(By.ID, 'id-seat-sel')
            seat_list = seats.find_elements(By.CSS_SELECTOR, "div[style='display: block;']")
            for i,p in enumerate(seat_list):
                seat_id = '%d%s'%(i, self.seat_type[i % len(self.seat_type)])
                p.find_element(By.ID, seat_id).click()
        table.find_element(By.ID, 'qr_submit_id').click()
        return 1

    def ring(self):
        import pdb
        pdb.set_trace()
        pygame.mixer.pre_init(64000, -16, 2, 4096)
        pygame.init()
        pygame.display.init()
        screen=pygame.display.set_mode([300,300])
        #pygame.display.flip()
        pygame.time.delay(1000)#等待1秒让mixer完成初始化
        tracker=pygame.mixer.music.load("media/sound.ogg")
        #track = pygame.mixer.music.load("sound.ogg")
        pygame.mixer.music.play()
        # while pygame.mixer.music.get_busy():
        #pygame.time.Clock().tick(10)
        running = True
        img=pygame.image.load("media/img.jpg")
        while running:
            screen.blit(img,(0,0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running = False
        pygame.quit ()
        return 1
    def executor(self):
        self.init_browser()  # 初始化浏览器
        self.login()
        self.switch_to_order_page()
        while self.success == 0:
            self.find_ticket = 0
            while self.find_ticket == 0:
                for date in self.date:
                    try:
                        self.count += 1
                        print("Try %d times" % self.count)
                        for fromStation in self.fromStation:
                            for toStation in self.toStation:
                                this_train = self.checkTicket(date, fromStation, toStation)
                                if self.find_ticket:
                                    break
                            if self.find_ticket:
                                break
                        if self.find_ticket:
                            break
                    except KeyboardInterrupt:
                        self.b.find_element(By.LINK_TEXT, u'退出').click()
                        sys.exit()
                    except (IOError, RuntimeError, TypeError, NameError) as e:
                        print(e)
                        continue
            # book ticket for target people
            self.find_ticket = 0
            while self.find_ticket == 0:
                try:
                    self.find_ticket = self.book(this_train) 
                except KeyboardInterrupt:
                    self.b.find_element(By.LINK_TEXT, u'退出').click()
                    sys.exit()
                except:
                    continue
            if self.playmusic:
                self.ring()
            print("订票成功了吗?(Y/N)")
            input_var = ''
            while input_var == '':
                input_var= sys.stdin.read(1)
                if input_var == 'Y' or input_var == 'y':
                    self.success = 1
                elif input_var == 'N' or input_var == 'n':
                    if this_train in self.blacklist:
                        self.blacklist[this_train] += 1
                    else:
                        self.blacklist[this_train] = 1
                    print(u"%s 失败 %d 次"%(this_train, self.blacklist[this_train]))
                    self.b.get(self.url)
                    #self.b.refresh()
                else:
                    input_var = ''
                    continue
        self.b.find_element(By.LINK_TEXT, u'退出').click()

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='12306 火车票自动抢票工具（Python 3 现代化版本）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python crawler.py conf/conf.ini
  python crawler.py conf/conf.ini --date 2026-02-15
  python crawler.py conf/conf.ini --trains G123,D456 --no-alarm
        """
    )

    parser.add_argument('config', help='配置文件路径')
    parser.add_argument('--date', help='覆盖配置文件中的日期（逗号分隔）')
    parser.add_argument('--trains', help='覆盖配置文件中的车次（逗号分隔）')
    parser.add_argument('--from-station', help='覆盖起始站')
    parser.add_argument('--to-station', help='覆盖到达站')
    parser.add_argument('--people', help='覆盖乘车人（逗号分隔）')
    parser.add_argument('--no-alarm', action='store_true', help='禁用音乐提醒')
    parser.add_argument('--tolerance', type=int, help='覆盖失败容忍次数')

    args = parser.parse_args()

    # 创建 Ticket 实例
    ticket_theif = Ticket(args.config)

    # 应用命令行参数覆盖
    if args.date:
        ticket_theif.date = [d.strip() for d in args.date.split(',')]
        print(f"📅 使用命令行指定的日期: {ticket_theif.date}")

    if args.trains:
        ticket_theif.trains = [t.strip() for t in args.trains.split(',')]
        print(f"🚄 使用命令行指定的车次: {ticket_theif.trains}")

    if args.from_station:
        ticket_theif.fromStation = [args.from_station.strip()]
        print(f"🚉 使用命令行指定的起始站: {args.from_station}")

    if args.to_station:
        ticket_theif.toStation = [args.to_station.strip()]
        print(f"🏁 使用命令行指定的到达站: {args.to_station}")

    if args.people:
        ticket_theif.people = [p.strip() for p in args.people.split(',')]
        print(f"👥 使用命令行指定的乘车人: {ticket_theif.people}")

    if args.no_alarm:
        ticket_theif.playmusic = False
        print("🔇 已禁用音乐提醒")

    if args.tolerance is not None:
        ticket_theif.tolerance = args.tolerance
        print(f"⚠️  失败容忍次数设置为: {args.tolerance}")

    # 启动抢票
    try:
        ticket_theif.executor()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
        sys.exit(0)
