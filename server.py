import SimpleHTTPServer
import SocketServer
from classify_image import *

PORT = 8000

class ClassifyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_POST(self):
		print "got POST"
		length = int(self.headers.getheader('content-length'))
		image_url = self.rfile.read(length)
		result = classify(image_url)
		self.wfile.write("You wrote a post, classified as %s" % (result))



Handler = ClassifyHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
