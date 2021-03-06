from classify_image import *
from flask import *
import os
from dbconnection import *
import json
from gpscoordinates import *
from random import randint,uniform
from wikipediaApi import *


# INIT
app = Flask(__name__)
PORT = int(os.environ.get("PORT",5000))
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Get everything/filtered in databse
@app.route('/getMethod')
def getMethodHandler():
	rows = selectByLable("")
	print(rows)
	return json.dumps(rows)

# Get file for icons
@app.route('/img/<filename>')
def get_icon_file(filename):
	return send_from_directory('img', filename)

# Get the uploaded file
# filename is in path
@app.route('/uploads/<filename>')
def send_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# REQUEST BODY - none
# Form action - upload image
# Response - TBD
@app.route("/upload", methods=['GET'])
def uploadPageHandler():
	print "Request for upload form"
	return render_template('upload.html')

# REQUEST BODY - multipart upload
# Keep the file on server
# Response - google map
@app.route("/upload", methods=['POST'])
def uploadFileHandler():
	print "Request for upload file"
	f = request.files['image_file']
	#secureFilename = secure_filename(f.filename) # Requires werkzeug.utils
	secureFilename = f.filename # not really secure...
	print "got %s" % (secureFilename)
	fullPathToUploadedFile = os.path.join(app.config['UPLOAD_FOLDER'], secureFilename)
	f.save(fullPathToUploadedFile)
	print "saved %s" % (secureFilename)
	labels = classify(fullPathToUploadedFile)
	print "classified as %s" % (labels)

	tmp = read_gps_data(fullPathToUploadedFile)
	if tmp != None:
		lat, lng = tmp
	else:
		lat, lng = uniform(40,60), uniform(0,40)
		print "random lat %f %f" % (lat, lng)
	date = read_date(fullPathToUploadedFile)
	if date == None:
		date = '%d Sep 2016, %d:%d' % (randint(1,29)+1, randint(1,12)+8, randint (1,50)+1)
	try:
		status = getEndangeredStatus(labels)
	except Exception as e:
		status = -1

	insertLine(secureFilename, lat,lng,labels, date,status)
	print "saved %s" % (secureFilename)
	if PORT==5000:
		print "WORKING LOCALLY"
	else:
		print "WORKING ON HEROKU"
	#return "Uploaded %s, <img src='uploads/%s'>" % (secureFilename, secureFilename)
	tmp = selectByLable("")
	print tmp
	print json.dumps(tmp)
	# redirect to homepage
	return redirect("/", 302)
	#return json.dumps(tmp)


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

@app.route("/initdb/", methods=['GET'])
def initDbHandler():
	print "init db"
	initDB()
	return 'db is init'


# THIS IS OUR HOMEPAGE!
@app.route("/")
def hello():
	return render_template('maptest.html')


# RUNNING THE APP
#print "serving at port", PORT
#app.run(host='0.0.0.0', port=PORT)
