

#! env/bin/python3
# -*- encoding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
url = "http://www.weibo.com/login.php"
url2='https://www.zhihu.com/#signin'
driver = webdriver.Chrome()
driver.get(url2)
username = driver.find_element_by_name('account')
username.clear()
username.send_keys("liujiawei0524@163.com")
password = driver.find_element_by_name('password')
password.clear()
password.send_keys('ljw1107779806')
driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()