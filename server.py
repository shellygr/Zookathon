from classify_image import *
from flask import *
import os

# INIT
app = Flask(__name__)
PORT = int(os.environ.get("PORT",5000))





# REQUEST BODY == image url
# ==>
# RESPONSE BODY == name of animal/object
@app.route("/getClassification/", methods=['POST'])
def classificationHandler():
	print "got POST for classification"
	image_url = request.data
	print "got path: %s" % (image_url)
	result = classify(image_url)
	if result:
		return result.split(',')[0]
	return "I don't know :("
	

# THIS IS OUR HOMEPAGE!
@app.route("/")
def hello():
	return "Moved to flask!"


# RUNNING THE APP
print "serving at port", PORT
app.run(host='0.0.0.0', port=PORT)
