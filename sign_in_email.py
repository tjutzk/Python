#-*- coding:utf-8 -*-
from selenium import webdriver
from PIL import Image
from PIL import ImageEnhance
import time
import random
import pytesseract
import unittest

url = "http://reg.email.163.com/unireg/call.do?cmd=register.entrance&from=126mail"
email_address_head_range = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ"
email_address_body_range = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ0123456789_"

def generate_eamil():
    email_address_length = random.randint(6,18)
    email_address_head = random.choice(email_address_head_range)
    email_address_body = ''.join(random.choice(email_address_body_range) for i in range(email_address_length-1))
    email_address = email_address_head + email_address_body
    return email_address

def input_email_account(driver):
    email_address = generate_eamil()
    driver.find_element_by_id("nameIpt").send_keys(email_address)

def input_email_passwd(driver):
    passwd = "abc123"
    driver.find_element_by_id("mainPwdIpt").send_keys(passwd)
    driver.find_element_by_id("mainCfmPwdIpt").send_keys(passwd)

def get_picture_captcha(driver):
    driver.save_screenshot('screenshot.png') #截屏
    picture_captcha = driver.find_element_by_id('vcodeImg')
    location = picture_captcha.location #获取验证码图片坐标位置
    size = picture_captcha.size #获取验证码图片大小
    rangle = (int(location['x']),
          int(location['y']),
          int(location['x']) + size['width'],
          int(location['y']) + size['height'],) 
    picture = Image.open('screenshot.png')
    captcha = picture.crop(rangle) #获取验证码图片
    captcha.save('captcha.png')

def recognition_captcha():
    i1 = Image.open("captcha.png")
    imgry = i1.convert('L') #图像加强 二值化 灰度
    i2 = ImageEnhance.Contrast(imgry) #对比度增强
    i3 = i2.enhance(3.0) #图像饱和度
    i3.save("deal_image.png")
    i4 = Image.open("deal_image.png")
    text = pytesseract.image_to_string(i4).strip()
    print 111
    if text == '':
        print "text is null"
    print text
    return text

def input_captcha(driver,captcha_num):
    print 222
    driver.find_element_by_id("vcodeIpt").send_keys(captcha_num)


if __name__ == "__main__":
    #打开126邮箱地址
    driver = webdriver.Firefox()
    driver.maximize_window()
    time.sleep(2)
    driver.get(url)
    time.sleep(5)
    #输入用户名
    input_email_account(driver)
    time.sleep(1)
    #输入密码
    input_email_passwd(driver)
    time.sleep(1)
    #验证码识别
    get_picture_captcha(driver)
    captcha_num = recognition_captcha()
    input_captcha(driver,captcha_num)