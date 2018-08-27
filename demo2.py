from selenium import webdriver
import time
dr= webdriver.Firefox()
time.sleep(5)
print 'ok'
dr.quit()
print 'quit'
