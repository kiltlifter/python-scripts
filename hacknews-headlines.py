from bs4 import BeautifulSoup
import requests

content = requests.get("http://news.ycombinator.com")
soup = BeautifulSoup(content.content)

title = soup.find_all(class_="title")

article = []
for item in title:
	if item.a != None and item.a.text != "More":
		field = [item.a.text, item.a['href']]
		article.append(field)

print article
