from bs4 import BeautifulSoup
import requests
import os

url = "http://xkcd.com"
url2 = "http://www.dilbert.com"
home = requests.get(url)
home2 = requests.get(url2)
soup = BeautifulSoup(home.content)
soup2 = BeautifulSoup(home2.content)
#XKCD
comic_div = soup.find(id="comic")
file_url = comic_div.img["src"]
mouseover_text = comic_div.img["title"].encode("ascii", "ignore")
alt_text = comic_div.img["alt"].encode("ascii", "ignore")
#Dilbert
comic2_div = soup2.find("div", class_="STR_Image")
file2_url = url2 + comic2_div.a.img["src"]

os.popen("mkdir -p /tmp/comics/xkcd /tmp/comics/dilbert /tmp/comics/combo")
os.popen('wget -O /tmp/comics/xkcd/new.png ' + file_url)
os.popen('wget -O /tmp/comics/dilbert/new.gif ' + file2_url)
title_command = "convert -pointsize 26 -gravity north label:\"" + str(alt_text) + "\" /tmp/comics/xkcd/title.gif"
mouseover_command = "convert -pointsize 10 -gravity south -size 600x25 caption:\"" + str(mouseover_text) + "\" /tmp/comics/xkcd/mouseover.gif"
os.popen(title_command + '&&' + mouseover_command)
os.popen('convert /tmp/comics/xkcd/title.gif /tmp/comics/xkcd/new.png /tmp/comics/xkcd/mouseover.gif -gravity center -append /tmp/comics/xkcd/new.png')
os.popen('convert /tmp/comics/xkcd/new.png /tmp/comics/dilbert/new.gif -gravity center -append /tmp/comics/combo/new.png')
os.popen('nitrogen --restore')
