#!/usr/bin/python
__author__ = 'sdouglas'


import urllib2
import re
import json
import optparse


def get_movie_info(title):
    try:
        spaces = re.compile("\s")
        url_safe_title = spaces.sub("+", title[0])
        request_string = "http://www.omdbapi.com/?t=%s&y=%s&plot=short&r=json" % (url_safe_title, title[1])
        request_obj = urllib2.Request(
            url=request_string,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)" +
                "Chrome/39.0.2171.95 Safari/537.36"}
        )
        data = urllib2.urlopen(request_obj)
        response_data = data.read()
        found = re.findall("Response\":\"(.*)\",", response_data)
        if found:
            print "%s: Movie not found!" % title[0]
            return None
        return response_data
    except Exception as e:
        print "Error retrieving movie info for: %s" % title
        print str(e)


def format_title(full_title):
    try:
        year = re.findall("\((\d{4})\)", full_title)[0]
        title = re.findall("^-(.*)\s\(\d{4}\)", full_title)[0]
        return [title, year]
    except Exception as e:
        print "Error formatting the title for: %s" % full_title
        print str(e)


def parse_json(movie_data):
    if movie_data is None:
        return None
    try:
        movie_dict = json.loads(movie_data)
        print movie_dict["Title"]
        print movie_dict["Year"]
        print movie_dict["Rated"]
        print movie_dict["Runtime"]
        print movie_dict["Genre"]
        print movie_dict["Poster"]
        print movie_dict["Plot"]
        print movie_dict["imdbRating"]
        print "http://imdb.com/title/" + movie_dict["imdbID"] + "\n\n"
    except Exception as e:
        print "Error parsing json response."
        print str(e)


def actions(movie_list):
    try:
        with open(movie_list, "r") as f:
            for line in f:
                title = line.rstrip("\n\r")
                formated_title = format_title(title)
                movie_data = get_movie_info(formated_title)
                parse_json(movie_data)
    except Exception as e:
        print "Error reading input file."
        print str(e)


def main():
    parser = optparse.OptionParser("MovieInfo.py -l <movie list>")
    parser.add_option("-l", dest="movieList", type="string", help="movie list")
    (options, args) = parser.parse_args()
    if options.movieList is None:
        print parser.usage
        exit()
    actions(options.movieList)


if __name__ == '__main__':
    main()
