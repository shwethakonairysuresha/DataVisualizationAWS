import os, re, time, memcache
from flask import Flask, render_template, request, redirect, session
from random import randint
from datetime import datetime
import sys, csv
import pymysql
from werkzeug.utils import secure_filename

ACCESS_KEY_ID = '********'
ACCESS_SECRET_KEY = '********'
BUCKET_NAME = '********'

hostname = '********'
username = '********'
password = '********'
database = '********'
Conn = pymysql.connect( host=hostname, user=username, passwd=password, db=database, autocommit = True, cursorclass=pymysql.cursors.DictCursor, local_infile=True)

print "Database Connected"

application = Flask(__name__)
app = application
app.secret_key = 'pass'

def memcache_connect():
    #Connecting to the memcache
	memc = memcache.Client(['shwethacache.5qit6s.cfg.use2.cache.amazonaws.com:11211'], debug = 1)
	print "Memcache connected"
	return memc

UPLOAD_FOLDER = '/home/ubuntu/flaskapp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
query= "select * from Education limit"

@app.route("/")
def hello():#For displaying the first page
    return render_template("filehandle.html")

@app.route("/csv_file_upload", methods = ['POST'])
def csv_file_upload():#For uploading the file
	file = request.files['file_upload']	
	filename=file.filename
	session['file_name']=filename
	print "file recieved"
	filename = secure_filename(file.filename)
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	dropquery="drop table IF EXISTS "+ filename[:-4]
	with Conn.cursor() as curs:
		curs.execute(dropquery)
		Conn.commit()
	print "dropped"
	columnname="("
	abs_filename=UPLOAD_FOLDER+filename
	with open(abs_filename, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			line=row
			break
	for i in line:
		columnname+=i+" VARCHAR(50),"
	query="Create table if not exists " + filename[:-4]+columnname+" sr_no INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(sr_no));"
	print query
	with Conn.cursor() as curs:
		curs.execute(query)
		Conn.commit()
	curs.close()
	print "successfully created"
	
	insert_data="""LOAD DATA LOCAL INFILE '"""+absfilename+ """'INTO TABLE """+ filename[:-4] +""" FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"""
	print (insert_data)
	with Conn.cursor() as curs:
		curs.execute(insert_data)
		Conn.commit()
	print "successfully loaded"
	return render_template("filehandle.html")

@app.route('/plotbarchart', methods=['POST'])
def plotbarchart():
    	maxnum = request.form['limit']

    	query1 = "select count(distinct county),state from USZipcodes group by state having count( distinct county) <"+str(5)

    	result1 = []
	with Conn.cursor() as curs:
    		curs.execute(query1)
    		for row in curs:
        		result1.append(row)
    	x1 = [x['count(distinct county)'] for x in result1]
    	x2 = [x['state'] for x in result1]
    	result2 = []
    	print x1
    	print x2
    	print result2
    	for p in x2:
        	result2.append(p)
    	print(result2)
    	return render_template("index.html",zipped_data= x1,x2=result2)



