# -*- encoding:utf8-*-
from selenium import webdriver  
from selenium.common.exceptions import TimeoutException  
from selenium.webdriver.support.ui import WebDriverWait 
import time  
driver = webdriver.Chrome()  ##可以替换为IE(), FireFox()  
driver.get("http://www.google.com")  
inputElement = driver.find_element_by_name("q")  
inputElement.send_keys("Cheese!")  
try:  
    WebDriverWait(driver, 10).until(lambda driver : driver.title.lower().startswith("cheese!"))  
    print driver.title  
finally:  
    driver.quit()  
