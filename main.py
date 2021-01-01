from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import make_response
import json,os
from flask import jsonify
import datetime
import pymysql
from sql import *
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__,static_folder='',static_url_path='')

config = {
        'host':'localhost',
        'port':3306,
        'user':'root',
        'password':'',
        'db':'booklib',
        'charset':'utf8',
        'cursorclass':pymysql.cursors.DictCursor
        }

db = pymysql.connect(**config)

@app.route('/')
def homePage():
    return render_template('login.html',state = 'success')

@app.route('/checkValidation')
def checkValidation():
	username = request.args.get('username')
	password = request.args.get('password')
	result = checkUP(db,username, password)
	if(result[0] == 'find user'):
		res = make_response(render_template('login.html',state = 'success'))
		res.set_cookie('username',username)
		temp = '%d' %result[1]
		res.set_cookie('user_id',temp)
		return res
	elif(result[0] == 'wrong pwd'):
		return render_template('login.html',state = 'wrong pwd')
	elif(result[0] == 'no user'):
		return render_template('login.html',state = 'no user')
	return result[0]

@app.route('/register')
def register():
	username = request.args.get('username')
	password = request.args.get('password')
	nameIsExisted = hasName(db.cursor(),username)
	if(nameIsExisted):
		return render_template('login.html',state = 'invalid register name')
	else:
		addUser(db,username,password)
		return render_template('login.html',state = 'register success')
		
		
@app.route('/login')
def login():
	return enterWeb(request)

@app.route('/index')
def index():
	return enterWeb(request)

def enterWeb(request):
	userid = request.cookies.get("user_id")
	if(userid is None):
		return render_template('login.html',state = 'no cookie')
	return render_template('index.html')

@app.route('/logout')
def logout():
	res = make_response(render_template('login.html',state = 'success'))
	res.delete_cookie('user_id')
	res.delete_cookie('username')
	uid = getUidFromCookie(request)
	updateUserLoginTime(db,uid)
	return res

@app.route('/user')
def user():
	if(not hasRights(request)):
		return "have no rights to access this page"
	uid = getUidFromCookie(request)
	name = request.cookies.get("username")
	time = getLastLoginTime(db,uid)
	res = make_response(render_template('user.html',
						username = name,
						ltime = time,
						uid = uid))
	return res

@app.route('/addBook', methods=['GET', 'POST'])
def addBookRoute():
	if(not hasRights(request)):
		return "have no rights"
	request_data = json.loads(request.get_data(as_text=True))
	print(request_data)
	userID = request.cookies.get("user_id")
	results = addBook(db,request_data['bookName'],userID)
	return jsonify(results),"200 OK"
	
@app.route('/getAll',methods=['GET', 'POST'])
def getAll():
	if(not hasRights(request)):
		return "has no rights"
	request_data = json.loads(request.get_data(as_text=True))
	keyword = request_data['keyword']
	
	if(keyword is None):
		return jsonify({}),"200,OK"
	uid = request.cookies.get("user_id")
	dic = getAllUserBook(db,uid,keyword)
	return jsonify(dic),"200 OK"
	
@app.route('/changeBookTags',methods=['GET', 'POST'])
def changeBookTagsRoute():
	if(not hasRights(request)):
		return "have no rights"
	request_data = json.loads(request.get_data(as_text=True))
	print(request_data)
	uid = request.cookies.get("user_id")
	bid = request_data['bid']
	added = request_data['added']
	deleted = request_data['deleted']
	changeBookTags(db,uid,bid,added,deleted);
	print(request_data)
	return jsonify({}),"200 OK"

@app.route('/changePassword',methods = ['POST','GET'])
def changePasswordRoute():
	if(not hasRights(request)):
		return "have no rights"
	uid = request.cookies.get("user_id")
	request_data = json.loads(request.get_data(as_text=True))
	newPassword = request_data['newPassword']
	if(newPassword is None):
		return "no new password"
	changePassword(db,uid,newPassword)
	return jsonify({}),'200 OK'

@app.route('/changeBookName',methods = ['POST','GET'])
def changeBookNameRoute():
	if(not hasRights(request)):
		return "have no rights"
	request_data = json.loads(request.get_data(as_text=True))
	changeBookName(db,request_data['bid'],request_data['newname'])
	return jsonify({}),"200 OK"
	
@app.route('/changePage',methods = ['POST','GET'])
def changePageRoute():
	if(not hasRights(request)):
		return "have no rights"
	request_data = json.loads(request.get_data(as_text=True))
	uid = getUidFromCookie(request)
	type = request_data['type']
	bid = request_data['bid']
	value = request_data['value']
	if(type is None or type not in ['read','total'] or bid is None):
		return "invalid change page"
	changePage(db,type,value,uid,bid)
	return "200 OK"

@app.route('/delete',methods = ['POST','GET'])
def deleteRoute():
	if(not hasRights(request)):
		return "have no rights"
	request_data = json.loads(request.get_data(as_text=True))
	uid = getUidFromCookie(request)
	bid = request_data['bid']
	if(bid is None):
		return "not perrmited to delete"
	deleteBook(db,uid,bid)
	return jsonify({}),"200 OK"

@app.route('/upload_file',methods = ['GET','POST'])
def upload_file():
	if(not hasRights(request)):
		return "have no rights"
	uid = getUidFromCookie(request)
	
	base = os.getcwd()
    
	#target_dir= base + "\\file\\" + file_id
	target_path = base + "\\static\\images\\head_portrait\\" + str(uid)
	
	#os.mkdir(target_dir)
	fp = open(target_path,'wb')
	fp.write(request.get_data())
	fp.close()
    #结束文件的上传工作
	return jsonify({}),"200 OK" 

def hasRights(request):
	userID = request.cookies.get("user_id")
	if(userID is None):
		return False
	else:
		return True
def getUidFromCookie(request):
	return request.cookies.get("user_id")


		
	