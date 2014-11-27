import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

addr = ("10.1.100.63", 8000)

serv = BaseHTTPServer.HTTPServer(addr, SimpleHTTPRequestHandler)

serv.serve_forever()
