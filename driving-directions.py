__author__ = 'sdouglas'
import requests, sys


def parse_address(origin, destination):
    url = 'http://maps.googleapis.com/maps/api/directions/xml?origin=' + origin + \
          '&destination=' + destination + '&units=imperial&mode=driving&sensor=false'
    return url


def make_request(input):
    s = requests.Session()
    r = s.get(input)
    return r.text


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print "Example: ./driving-directions.py 'San Diego, CA' 'Napa, CA'"
    print make_request(parse_address(sys.argv[1], sys.argv[2]))

if __name__ == '__main__':
    main()
