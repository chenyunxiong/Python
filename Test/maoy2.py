#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import cv2
from PIL import Image
from selenium import webdriver
import pyautogui
from numpy import random
import time


class SliderVerificationCode:

    def __init__(self):
        url = 'https://tfz.maoyan.com/yamaha/verify?requestCode=9683559bbfb347bda5382e9260e5afc7i3fmn&redirectURL=https%3A%2F%2Fwww.maoyan.com%2Fboard%2F4%3FtimeStamp%3D1662022844255%26sVersion%3D1%26offset%3D0%26index%3D9%26webdriver%3Dfalse%26signKey%3D6a9e8cc863681336b95ea0d8c24d3875%26channelId%3D40011#/'
        self.driver = self.get_url(url, '11111', '222222')

    def get_url(self, url, user, password):
        browser = webdriver.Chrome(executable_path=r'C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\MicrosoftEdge.exe')
        browser.get(url)
        browser.maximize_window()
        time.sleep(3)
        user_input = browser.find_element_by_xpath('//*[@id="username"]')
        pwd_input = browser.find_element_by_xpath('//*[@id="password"]')
        btn = browser.find_element_by_xpath('//*[@id="formLogin"]/div[4]/div/div/span/button')
        user_input.send_keys(user)
        pwd_input.send_keys(password)
        btn.click()
        time.sleep(0.5)
        return browser

    def get_image(self):
        time.sleep(3)
        print('frame location:', self.driver.find_element_by_id('tcaptcha_iframe').location)
        self.driver.switch_to.frame('tcaptcha_iframe')
        self.target = self.driver.find_element_by_xpath('//*[@id="slideBg"]')
        self.template = self.driver.find_element_by_xpath('//*[@id="slideBlock"]')
        self.download_img(self.target.get_attribute('src'), 'target.png')
        self.download_img(self.template.get_attribute('src'), 'temlate.png')

        # 下载下来的原图网页的css有调整尺寸，这样就需要按照网页的尺寸来计算偏移
        self.resize_image('target.png', 'target.png', 341, 195, 'png')
        self.resize_image('temlate.png', 'temlate.png', 68, 68, 'png')

    def resize_image(self, filein, fileout, width, height, type):
        img = Image.open(filein)
        out = img.resize((width, height), Image.ANTIALIAS)
        # resize image with high-quality
        out.save(fileout, type)

    def download_img(self, img_url, save_name):
        host_referer = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        print('download:' + img_url)
        html = requests.get(img_url, headers=host_referer)
        # 图片不是文本文件，以二进制格式写入，所以是html.content
        f = open(save_name, 'wb')
        f.write(html.content)
        f.close()

    def find_pic(self, target='target.png', template='temlate.png'):
        target_rgb = cv2.imread(target)
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_RGB2GRAY)
        template_rgb = cv2.imread(template, 0)
        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(res)
        # print(value)
        return value[2][0]

    def size(self):
        x = self.find_pic()
        img = cv2.imread('target.png')
        w1 = img.shape[1]
        w2 = self.target.size['width']
        self.offset = int(x * w2 / w1 + 25)  # 这个25没搞清楚为什么是25...
        print(self.offset)

    def drag(self):
        time.sleep(3)
        The_slider = self.driver.find_element_by_xpath('//*[@id="tcaptcha_drag_button"]')
        # 780：是验证码弹窗距离浏览器最左边的x轴距离（因为在整个验证码弹窗是个iframe，所以这个元素的x定位是以iframe的来计算的）
        # 284：是y轴的
        x = The_slider.location.get('x') + 780  # 滑块的初始x位置
        y = The_slider.location.get('y') + 284
        print(The_slider.location, ',kw_x = ', x, ',kw_y = ', y)
        xx = self.offset + 780 - 11  # offset=缺口到iframe边框的距离

        pyautogui.moveTo(x, y + 127, duration=0.1)

        pyautogui.mouseDown()

        y += random.randint(9, 19)
        pyautogui.moveTo(x + int(self.offset * random.randint(15, 23) / 20), y, duration=0.28)

        y += random.randint(-9, 0)
        pyautogui.moveTo(x + int(self.offset * random.randint(17, 21) / 20), y, duration=(random.randint(20, 31)) / 100)

        y += random.randint(0, 8)
        pyautogui.moveTo(xx, y, duration=0.3)

        # self.driver.save_screenshot('fullscreen.png')
        print('finally x:{},y:{}'.format(xx, y))

        pyautogui.mouseUp()


if __name__ == '__main__':
    p = SliderVerificationCode()
    p.get_image()
    p.find_pic()
    p.size()
    p.drag()
    print('end')