import time
import re 
import pandas as pd
from bs4 import BeautifulSoup as b4
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import date
import requests
import os 
import sys
import random


def sendmsg(cc,data,words,email,name):
    urls = data['businessUrl']
    for x in range(len(urls)):
        print(urls[x])
        cz = True
        et = True
        btx = True
        while (et or cz) and btx:
            btx = False
            cc.get('https://www.yelp.com'+str(urls[x]))
            try:
                ht = cc.page_source
                bt = re.findall("Error",ht)
                cw = re.findall("Confirmation",ht)
                bn = cc.find_element(By.CLASS_NAME,"css-35w7iu")
                btx = bn is not None
                print("msg button field")
                bn.click()
                # data.loc[:('renderAdInfo',x)] = True
                # data['isAd'][x]=True
                w = cc.find_element(By.XPATH,"/html/body/yelp-react-root/div[3]/div[2]/div/div/div/div[2]/div/form/div[2]/div[2]/div/textarea")
                print("text field")
                btx = w is not None
                e = cc.find_element(By.XPATH,"/html/body/yelp-react-root/div[3]/div[2]/div/div/div/div[2]/div/form/div[3]/div[2]/div/div[1]/div/label/input")
                print("email field")
                btx = e is not None
                n = cc.find_element(By.XPATH,"/html/body/yelp-react-root/div[3]/div[2]/div/div/div/div[2]/div/form/div[3]/div[2]/div/div[2]/div/label/input")
                print("name field")
                btx = n is not None
                s = cc.find_element(By.XPATH,"/html/body/yelp-react-root/div[3]/div[2]/div/div/div/div[2]/div/form/div[4]/div[1]/button/span")
                print("submit button")
                btx = s is not None
                w.send_keys(words)
                e.send_keys(email)
                n.send_keys(name)
                s.click()
                time.sleep(1)
                ht = cc.page_source
                bz = re.findall("Error",ht)
                et = len(bt)<len(bz)
                cy = re.findall("Confirmation",ht)
                cz = len(cy) <= len(cw)
                if cz==True:
                    data['isAd'][x]=True
                if et == True:
                    cv()
            # data.loc[:('isAd',x)] = True
            except:
                data['isAd'][x]=False
                # data.loc[:('isAd',x)] = False
                # pass
            print(et,cz,btx)
                
    return data

def sendmsg1(cc,url,words,email,name):
    cc.get(url)
    bn = cc.find_element_by_class_name("css-35w7iu")
    print("msg button field")
    bn.click()
    w = cc.find_element_by_xpath("/html/body/yelp-react-root/div[3]/div[2]/div/div/div/div[2]/div/form/div[2]/div[2]/div/textarea")
    print("text field")
    e = cc.find_element_by_xpath("/html/body/yelp-react-root/div[3]/div[2]/div/div/div/div[2]/div/form/div[3]/div[2]/div/div[1]/div/label/input")
    print("email field")
    n = cc.find_element_by_xpath("/html/body/yelp-react-root/div[3]/div[2]/div/div/div/div[2]/div/form/div[3]/div[2]/div/div[2]/div/label/input")
    print("name field")
    s = cc.find_element_by_xpath("/html/body/yelp-react-root/div[3]/div[2]/div/div/div/div[2]/div/form/div[4]/div[1]/button/span")
    print("submit button")
    w.send_keys(words)
    e.send_keys(email)
    n.send_keys(name)
    # s.click()
        # data['isAd'][x]=True
        # data.loc[:('isAd',x)] = True
        # data.loc[:('isAd',x)] = False
    # return data

def parsemenu(soup):
    # print(soup)
    # re.find()
    # data = soup.find_all('script',attrs={ "data-hypernova-key" :"yelpfrontend__5520__yelpfrontend__GondolaSearch__dynamic" })
    dnam =  str(date.today())
    data = soup.find_all('script')
    datastr = ""
    for daa in data: 
        if len(daa.text)>len(datastr):
            datastr = daa.text
    f = open("{}.txt".format(dnam),"a")
    f.write(datastr)
    f.close()
    # print(data)
    # datastr = data[0].getText()[4:-4]
    arridx=[m.start() for m in re.finditer('{"ranking":', datastr)]
    arridy=[m.start() for m in re.finditer(',"scrollablePhotos":', datastr)]
    loaded = []
    for z in range(len(arridx)):
        loaded.append(json.loads(datastr[arridx[z]:arridy[z]]))
    df1 = pd.DataFrame(loaded)

    datastr = soup.prettify()
    arridx=[m.start() for m in re.finditer('"addressLines"', datastr)]
    arridy=[m.start() for m in re.finditer('],"neighborhood', datastr)]
    loaded = []
    for z in range(len(arridx)):
        # print("{"+datastr[arridx[z]:arridy[z]+1]+"}")
        loaded.append(json.loads("{"+datastr[arridx[z]:arridy[z]+1]+"}"))
    df = pd.DataFrame(loaded)
    try:
        drame = [df,df1]
        dd = pd.concat(drame,axis=1)
        dd = dd[dd.isAd != True]
        ddd=dd.reset_index()
        ddd=ddd.drop(columns="index")
        # print(ddd)
        return ddd
    except:
        pass
def c(cc,url):
    cc.get(url)
    html = cc.page_source
    print(len(html))
    while (len(html)<7000):
        cc.close()
        # options = Options()
        # options.add_argument("--headless=new")
        # cc = webdriver.Chrome(options=options)
        cv()
        cc = webdriver.Chrome()        
        # time.sleep(30)
        cc.get(url)
        html = cc.page_source
    return html, cc
def cv():
    vx = ["us-orl.prod.surfshark.com_udp.ovpn","us-phx.prod.surfshark.com_tcp.ovpn","us-phx.prod.surfshark.com_udp.ovpn","us-sea.prod.surfshark.com_tcp.ovpn","us-sea.prod.surfshark.com_udp.ovpn","us-sfo.prod.surfshark.com_tcp.ovpn","us-sfo.prod.surfshark.com_udp.ovpn","us-sjc.prod.surfshark.com_tcp.ovpn","us-sjc.prod.surfshark.com_udp.ovpn","us-slc.prod.surfshark.com_tcp.ovpn","us-slc.prod.surfshark.com_udp.ovpn","us-stl.prod.surfshark.com_tcp.ovpn","us-stl.prod.surfshark.com_udp.ovpn","us-tpa.prod.surfshark.com_tcp.ovpn","us-tpa.prod.surfshark.com_udp.ovpn"]
    rnd = random.randint(0,len(vx)-1)
    os.system("rm -r /tmp/.org.chromium*")
    os.system('/bin/bash -c "echo kali| sudo -S pkill openvpn &"')
    time.sleep(2)
    os.system('/bin/bash -c "echo kali| sudo -S openvpn {} &"'.format(vx[rnd]))
    time.sleep(30)

def main(baseurl):
    print(baseurl)
    lat = 1
    lon = 2
    lat1 = 1
    lon2 = 2
    # os.system("rm -r /tmp/.org.chromium*")
    # os.chdir("b")
    f = open("word.txt")
    wo = f.read()
    f.close()
    email = 'elenee.space@gmail.com'
    name = 'Douglas'
    # baseurl = sys.argv[1] #&
    rt = True
    count = 0
    # options = Options()
    # options.add_argument("--headless=new")
    # cr = webdriver.Chrome(options=options)
    cr = webdriver.Chrome()
    while rt:
        url = baseurl+'&start='+str(count*10)
        html, cr = c(cr,url)
        soup = b4(html,'html')
        df = parsemenu(soup)
        df = sendmsg(cr,df,wo,email,name)
        df.to_csv("log.csv",mode="a")
        if len(df)<10 or count>=23:
            rt = False
        count = count + 1


cv()
#xz = input('input city:')
#input("input yelp search such as cafe:")
#input("input yelp email to input:")
#input("input yelp name to input:")
# xz = sys.argv[1]
xy = int(sys.argv[1])
xzz = [40,80,120,160,200,240,280,320,340,380,420]+xy
for xz in xzz:
  f = open(str(xz)+'.txt',"r")
  cities = f.read().split('\n')
  f.close()
  #cities = xz.split("\n")
  xrl = "https://www.yelp.com/search?find_desc=cafe&find_loc="
  #input("  =======================================================")
  for xc in cities:
      try:
          main(xrl+xc)
          # print(xrl+xc)
      except:
          f = open("e{}.txt".format(xz),"a")
          f.write(xc+'\n')
          f.close()
          print(xc)
          cv()
  print("finish")
  
