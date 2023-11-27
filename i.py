from selenium import webdriver
import time

cr = webdriver.Chrome()
while True:
  cr.get("https://www.instagram.com/uhhnina")
  time.sleep(10)
