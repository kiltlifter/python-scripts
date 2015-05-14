#!/usr/bin/python
__author__ = 'Sean Douglas'

import requests
from bs4 import BeautifulSoup
import re, csv

base_url = "http://www.mbrea.net"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}


def find_full_name(h3_tag):
    name = h3_tag.contents[0]
    find_name = re.compile("\s(.*)\n")
    return find_name.findall(name)[0].encode("ascii").split()


def sort_contacts(contact_table):
    details = []
    try:
        for item in contact_table:
            heading = item.find("th")
            attribute = item.find("td")
            if heading is not None and attribute is not None:
                detail = "%s: %s" % (heading.text, attribute.text)
                details.append(detail)
    except Exception, e:
        print str(e)
    return details


def get_realtor_links():
    r = requests.get(base_url + "/members", headers=headers)
    soup = BeautifulSoup(r.text)
    realtors = soup.find_all("a", class_="list-group-item")
    realtor_links = []
    for anchor in realtors:
        realtor_links.append(base_url + anchor.get("href"))
    return realtor_links


def get_profile_info(profile_url):
    r = requests.get(profile_url, headers=headers)
    soup = BeautifulSoup(r.text)
    full_name = find_full_name(soup.find("h3"))
    website = soup.find("a", {"target": "_new"}).text
    contact = sort_contacts(soup.find("table", class_="table-striped"))
    big_list = full_name + contact
    return big_list


def main():
    realtor_links = get_realtor_links()
    with open("contact_list.csv", "wb") as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for realtor in realtor_links:
            profile_list = get_profile_info(realtor)
            csv_writer.writerow(profile_list)


if __name__ == '__main__':
    main()