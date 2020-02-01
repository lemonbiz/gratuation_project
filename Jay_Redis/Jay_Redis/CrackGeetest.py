# -*- coding: utf-8 -*-
# Author : Jay
# WritedTime : 2019/12/22 intern ing!
"""
*******************************************************
*   破解geetest滑块验证码3.0                           *
*   调用crack_bili_login_slider_geetest()返回cookie    *
*   使用cookie登陆即可                                 *
*******************************************************
"""
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import base64
ACCOUNT = '17748495720'
PASSWORD = '919169807'
chrome_options = Options()
# chrome_options.add_argument('--headless')  # 无头
# chrome_options.add_argument('--disable-gpu')  # 不加载gpu，规避bug
# chrome_options.add_argument('proxy-server=http://111.11.11.11:1234')  # proxy
chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
# chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
# chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度


class CrackGeetest():
    """
    破解极验滑块3.0，传入出现滑块验证码的网页，返回cookie值
    """
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.ACCOUNT = ACCOUNT
        self.PASSWORD = PASSWORD

    def get_captcha(self):
        """
        获取残缺、完整的验证码
        :return: 返回验证码图片
        """
        time.sleep(1)
        brokeimg = self.browser.execute_script('return document.getElementsByClassName("geetest_canvas_bg geetest_abso'
                                               'lute")[0].toDataURL("image/png")')[22:]
        fullimg = self.browser.execute_script('return document.getElementsByClassName("geetest_canvas_fullbg geetest_f'
                                              'ade geetest_absolute")[0].toDataURL("image/png")')[22:]
        return brokeimg, fullimg

    def get_decode_image(self, image):
        """
        解码图片
        :param image: 未解码的图片
        :return: 解码后的图片
        """
        image = base64.decodebytes(image.encode())
        new_image = Image.open(BytesIO(image))
        return new_image

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 是否相同
        """
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0]-pixel2[0]) < threshold and abs(pixel1[1]-pixel2[1]) < threshold and \
                abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def compute_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口的图片
        :param image2: 带缺口的图片
        :return: 偏移量
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值 0.5
        mid = distance*4/5
        # 计算间隔 0.7
        t = 0.2
        # 初速度 10
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正3
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度为v = v0+at
            v = v0 + a*t
            # 移动距离 x = v0t + 1/2*a*t^2
            move = v0*t + 1/2*a*t*t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        print('滑动轨迹为: %s' % track)
        return track

    def move_to_gap(self, track):
        slider = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
            '''
            不同的电脑会在这里遇到问题，如果遇到拖动速度卡顿的问题
            请在环境里的selenium/webdriver/common/actions/pointer_input里修改
            DEFAULT_MOVE_DURATION = 150 自己调试着改 我的电脑要改到2才能测试通过
            整了一个月都不明白的问题，被一个大佬解决了
            '''
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def crack_bili_login_slider_geetest(self):
        try:
            self.browser.get("https://passport.bilibili.com/login")
            Input = self.browser.find_element_by_id('login-username')
            Input.send_keys(self.ACCOUNT)
            Input = self.browser.find_element_by_id('login-passwd')
            Input.send_keys(self.PASSWORD)
            Input.send_keys(Keys.ENTER)
            image1, image2 = self.get_captcha()
            image1 = self.get_decode_image(image1)  # 残缺图片
            image2 = self.get_decode_image(image2)  # 完整图片
            gap = self.compute_gap(image2, image1)
            track = self.get_track(gap-8)
            self.move_to_gap(track)
            time.sleep(200)
            '''
            此处编写获取cookie并返回
            '''
        except Exception as e:
            print(e)
        finally:
            self.browser.close()


# aa = CrackGeetest()
# aa.crack_bili_login_slider_geetest()

