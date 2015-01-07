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


def create_html(movie_dict):
    movie_tables = ""
    for movie in movie_dict:
        html_table = '<table border="1">' \
                     '<tr>' \
                     '  <td>' \
                     '      <p>%s</p>' % movie["Title"] + \
                     '      <p>%s</p>' % movie["Year"] + \
                     '      <p>%s</p>' % movie["Runtime"] + \
                     '      <p>%s</p>' % movie["Genre"] + \
                     '      <img src="%s">' % movie["Poster"] + \
                     '      <p>%s</p>' % movie["Plot"] + \
                     '      <p>%s</p>' % movie["imdbRating"] + \
                     '      <a href="http://imdb.com/title/%s">IMDB Link</a>' % movie["imdbID"] + \
                     '  </td>' \
                     '</tr>' \
                     '</table>' \
                     '<br><br>'
        movie_tables += html_table
    css_style = """
    * {
        margin: 0;
        padding: 0;
        font-family: "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;
        font-size: 100%;
        line-height: 1.6;
    }

    img {
        max-width: 100%;
    }

    body {
        -webkit-font-smoothing: antialiased;
        -webkit-text-size-adjust: none;
        width: 100%!important;
        height: 100%;
    }


    /* -------------------------------------
            ELEMENTS
    ------------------------------------- */
    a {
        color: #348eda;
    }

    .btn-primary {
        text-decoration: none;
        color: #FFF;
        background-color: #348eda;
        border: solid #348eda;
        border-width: 10px 20px;
        line-height: 2;
        font-weight: bold;
        margin-right: 10px;
        text-align: center;
        cursor: pointer;
        display: inline-block;
        border-radius: 25px;
    }

    .btn-secondary {
        text-decoration: none;
        color: #FFF;
        background-color: #aaa;
        border: solid #aaa;
        border-width: 10px 20px;
        line-height: 2;
        font-weight: bold;
        margin-right: 10px;
        text-align: center;
        cursor: pointer;
        display: inline-block;
        border-radius: 25px;
    }

    .last {
        margin-bottom: 0;
    }

    .first {
        margin-top: 0;
    }

    .padding {
        padding: 10px 0;
    }


    /* -------------------------------------
            BODY
    ------------------------------------- */
    table.body-wrap {
        width: 100%;
        padding: 20px;
    }

    table.body-wrap .container {
        border: 1px solid #f0f0f0;
    }


    /* -------------------------------------
            FOOTER
    ------------------------------------- */
    table.footer-wrap {
        width: 100%;
        clear: both!important;
    }

    .footer-wrap .container p {
        font-size: 12px;
        color: #666;

    }

    table.footer-wrap a {
        color: #999;
    }


    /* -------------------------------------
            TYPOGRAPHY
    ------------------------------------- */
    h1, h2, h3 {
        font-family: "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
        line-height: 1.1;
        margin-bottom: 15px;
        color: #000;
        margin: 40px 0 10px;
        line-height: 1.2;
        font-weight: 200;
    }

    h1 {
        font-size: 36px;
    }
    h2 {
        font-size: 28px;
    }
    h3 {
        font-size: 22px;
    }

    p, ul, ol {
        margin-bottom: 10px;
        font-weight: normal;
        font-size: 14px;
    }

    ul li, ol li {
        margin-left: 5px;
        list-style-position: inside;
    }

    /* ---------------------------------------------------
            RESPONSIVENESS
            Nuke it from orbit. It's the only way to be sure.
    ------------------------------------------------------ */

    /* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
    .container {
        display: block!important;
        max-width: 600px!important;
        margin: 0 auto!important; /* makes it centered */
        clear: both!important;
    }

    /* Set the padding on the td rather than the div for Outlook compatibility */
    .body-wrap .container {
        padding: 20px;
    }

    /* This should also be a block element, so that it will fill 100% of the .container */
    .content {
        max-width: 600px;
        margin: 0 auto;
        display: block;
    }

    /* Let's make sure tables in the content area are 100% wide */
    .content table {
        width: 100%;
    }
    """
    boilerplate_html = \
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">' \
        '<html xmlns="http://www.w3.org/1999/xhtml">' \
        '<head>' \
        '<meta name="viewport" content="width=device-width" />' \
        '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />' \
        '<title>This Week\'s movies</title>' \
        '<style>' \
        '%s' % css_style + \
        '</style>' \
        '</head>' \
        '<body bgcolor="#f6f6f6">' \
        '<table class="body-wrap">' \
        '   <tr>' \
        '       <td></td>' \
        '       <td class="container" bgcolor="FFFFFF">' \
        '           <div class="content">' \
        '               %s' % movie_tables + \
        '           </div>' \
        '       </td>' \
        '   </tr>' \
        '</table>' \
        '</body>' \
        '</html>'
    print boilerplate_html


def actions(movie_list):
    try:
        movie_items = []
        with open(movie_list, "r") as f:
            for line in f:
                title = line.rstrip("\n\r")
                formated_title = format_title(title)
                movie_data = get_movie_info(formated_title)
                if movie_data:
                    movie_items.append(json.loads(movie_data))
                #parse_json(movie_data)
        create_html(movie_items)
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
