from selenium import webdriver
import time

cr = webdriver.Chrome()
while True:
  cr.get("https://www.yahoo.com")
  time.sleep(10)
