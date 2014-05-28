#-*- coding: utf8 -*-

import time
import BaseHTTPServer
import os
import mimetypes

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 8080

DEFAULT_PATH = os.path.join("g:\\", "web", "www", "geckhosting_ori")

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        print s.path
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        
    def do_GET(s):
        # actions spécifiques
        if (s.path == "/pok"):
          s.pok()
        else: # mode normal
            path = os.path.join(DEFAULT_PATH, s.path[1:])
            if (os.path.isdir(path)): # La ressource est un dossier
                s.view_folder(path)
            else: #la ressource est un fichier
                s.view_file(path)
           
    def pok(s):
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()      
        s.wfile.write("pok ?")
        
    def view_folder(s, path):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        
        s.wfile.write("<html><head><title>killruana web server</title></head>")
        s.wfile.write("<body><p>http file explorer.</p>")
        s.wfile.write("<p>You accessed path: %s (<a href=\"..\">parent</a>)</p>" % s.path)
        
        s.wfile.write("<ul>")
        for element in os.listdir(path):
            sep = ""
            if (os.path.isdir(os.path.join(path, element))):
                sep = "/"
            s.wfile.write("<li><a href=\"http://%s:%i%s%s%s\">%s</a></li>" % (HOST_NAME, PORT_NUMBER, s.path, element, sep, element))
        s.wfile.write("</ul>")
          
        s.wfile.write("</body></html>")
        
    def view_file(s, path):        
        s.send_response(200)
        s.send_header("Content-type", mimetypes.guess_type(path)[0])
        s.end_headers()
        
        f = open(path, "rb")
        s.wfile.write(f.read())
        f.close()

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
