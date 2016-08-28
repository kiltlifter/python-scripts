import requests
import re
import sys
from bs4 import BeautifulSoup as bs

API_KEY = ""

# Scrape meh.com and get the current deal and price
class Scrape:
    def __init__(self):
        self.url = "https://meh.com"
        self.soup = self.create_soup()

    def make_request(self, altUrl=None):
        if altUrl:
            r = requests.get(altUrl)
        else:
            r = requests.get(self.url)
        return r

    def create_soup(self):
        response = self.make_request()
        if response.status_code == 200:
            soup = bs(response.text, "lxml")
            return soup
        else:
            print "Error retrieving %s" % self.url
            sys.exit(0)

# Use the pushbullet api to send today's deal to all my devices
class Push:
    def __init__(self):
        self.api_url = "https://api.pushbullet.com/v2/pushes"
        self.api_key = API_KEY

    def make_request(self, title, body, url=None):
        headers = {'Access-Token': self.api_key, 'Content-Type': 'application/json'}
        if url:
            data = {'title': title, 'body': body, 'type': 'link', 'url': url}
        else:
            data = {'title': title, 'body': body, 'type': 'note'}
        r = requests.post(self.api_url, headers=headers, json=data)
        return r


def get_title(html_soup):
    title = re.sub("\r\n\s{5,}|\s{5,}", "", html_soup.body.div.article.div.find("h2").string.encode("utf8"))
    return title


def get_price(html_soup):
    price = re.match("^\r\n\s{5,}(.*)\r\n\s{5,}Buy it\n$",
                     html_soup.body.div.article.div.find("button").get_text().encode("utf8")).groups()
    price = "".join(price)
    return price


def main():
    s = Scrape()
    result = s.create_soup()
    title = get_title(result)
    price = get_price(result)

    p = Push()
    p.make_request(title, price, "https://meh.com/")


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.stderr.write('interrupted\n')
        sys.exit(1)
