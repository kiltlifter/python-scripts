#!/usr/bin/python
__author__ = 'sdouglas'


import urllib2
import re
import json


def get_movie_info(title):
    spaces = re.compile("\s")
    url_safe_title = spaces.sub("+", title[0])
    request_string = "http://www.omdbapi.com/?t=%s&y=%s&plot=short&r=json" % (url_safe_title, title[1])
    request_obj = urllib2.Request(
        url=request_string,
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)" +
            "Chrome/39.0.2171.95 Safari/537.36"}
    )
    data = urllib2.urlopen(request_obj)
    return data.read()


def format_title(full_title):
    year = re.findall("\((\d{4})\)", full_title)[0]
    title = re.findall("^-(.*)\s", full_title)[0]
    return [title, year]


def parse_json(movie_data):
    movie_dict = json.loads(movie_data)
    print movie_dict["Title"]
    print movie_dict["Year"]
    print movie_dict["Rated"]
    print movie_dict["Runtime"]
    print movie_dict["Genre"]
    print movie_dict["Poster"]
    print movie_dict["Plot"]
    print movie_dict["imdbRating"]
    print "http://imdb.com/title/" + movie_dict["imdbID"]


def main():
    title = "-A Walk Among the Tombstones (2014)"
    formated_title = format_title(title)
    movie_data = get_movie_info(formated_title)
    parse_json(movie_data)

if __name__ == '__main__':
    main()
