from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
import json,os
from flask import jsonify
import datetime
import pymysql

#判断username 和 对应的password是否合法
def checkUP(db,username,passwd):
	cursor = db.cursor()
	count = cursor.execute("select user.id,passwd from user where user.name = '"+username+"'")
	result = cursor.fetchone()
	cursor.close()
	if( count != 1):
		return 'no user',-1
	if(result['passwd'] != passwd):
		return 'wrong pwd',-1
	return 'find user',result['id']

#判断数据库中是否有这个人名
def hasName(cursor,username):
	count = cursor.execute("select user.id from user where user.name = '"+username+"'")
	if(count >= 1):
		return True
	else:
		return False

#添加一名用户到数据库
def addUser(db,username,password):
	cursor = db.cursor()
	cursor.execute("insert into user(name,passwd) values('"+username+"','"+password+"')")
	cursor.close()
	db.commit()

#添加一个用户的读书记录
def addBook(db,bookName,userID):
	cursor = db.cursor()
	result = cursor.execute("insert into books(name) values('"+bookName+"')")
	#influence = result.fetchone()
	bookid = db.insert_id()
	currentDate = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	query = "insert into user_book(uid,bid,date,readpage,totalpage) values("+str(userID)+","+str(bookid)+",'"+currentDate+"',0,200)"
	cursor.execute(query)
	cursor.close()
	db.commit()
	return {'newBookid' : bookid}

#获取到一个用户的所有记录
def getAllUserBook(db,uid,keyword):
	results = {}
	#获取用户阅读了哪些书籍，但是没有这些书籍的tags
	query = "select bid,name,date,readpage,totalpage from user_book join books on  user_book.bid = books.id and user_book.uid = "+str(uid)
	searchByKeyword = " and name like '%"+keyword+"%' "
	query = query + searchByKeyword
	cursor = db.cursor()
	cursor.execute(query)
	books = cursor.fetchall()
	
	#格式化时间
	for i in range(0,len(books)):
	    books[i]['date'] = str(books[i]['date'])
	
	results['books'] = books
	
	#获取用户对书籍定义的tags
	query = "select bid,tn from user_books_tags where uid = " + str(uid)
	cursor.execute(query)
	tags = cursor.fetchall()
	results['tags'] = tags
	cursor.close()
	return results

#改变用户对书的标签的定义
def changeBookTags(db,uid,bid,added,deleted):
	cursor = db.cursor()
	#查询添加的标签是否在数据库中存在，如果不存在这个标签，就添加
	#防止有些tag在数据库中不存在
	query = "select * from tags where tags.name = "
	for i in range(0,len(added)):
		currentQuery = query + "\'" + added[i] + "\'"
		count = cursor.execute(currentQuery)
		if(count == 0):
			addQuery = "insert into tags(name) values (\""+added[i]+"\")"
			cursor.execute(addQuery)
			
	#增添关系到user_book_tag
	for i in range(0,len(added)):
		query = "INSERT INTO `booklib`.`user_books_tags` (`uid`, `bid`, `tn`) VALUES ('"+str(uid)+"', '"+str(bid)+"', '"+added[i]+"');"
		print(query)
		cursor.execute(query)
		
	#删除user_book_tag中过时的关系
	for i in range(0,len(deleted)):
		query = "delete from user_books_tags where uid = "+str(uid)+" and tn = \""+deleted[i]+"\""
		print(query)
		cursor.execute(query)
	cursor.close()
	db.commit()
	
def changePassword(db,uid,newPassword):
	cursor = db.cursor()
	sql = "update user set passwd = \""+str(newPassword)+"\" where id = " + str(uid)
	cursor.execute(sql)
	cursor.close()
	db.commit()

def updateUserLoginTime(db,uid):
	cursor = db.cursor()
	currentDate = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	sql = "update user set lastLoginTime = \"" + currentDate + "\" where id = " + str(uid)
	cursor.execute(sql)
	db.commit()

def getLastLoginTime(db,uid):
	cursor = db.cursor()
	cursor.execute("select lastLoginTime from user where id = " + str(uid))
	result = cursor.fetchone()
	time = str(result['lastLoginTime'])
	return time
	
def changeBookName(db,bid,newname):
	cursor = db.cursor()
	sql = "update books set name = \"" + newname + "\" where id = " + str(bid)
	cursor.execute(sql)
	db.commit()

def changePage(db,type,value,uid,bid):
	cursor = db.cursor()
	sql = ""
	if(type == 'read'):
		sql = "update user_book set readpage = " + str(value) + " where uid = " + str(uid) + " and bid = " + str(bid)
	elif(type == 'total'):
		sql = "update user_book set totalpage = " + str(value) + " where uid = " + str(uid) + " and bid = " + str(bid)
	cursor.execute(sql)
	db.commit()

def deleteBook(db,uid,bid):
	cursor = db.cursor()
	#删除一条Book信息包括以下步骤
	#1. 删除user_book 里面的信息
	#2. 删除user_books_tags 里面的信息
	#3. 删除books里面的信息
	
	#1. 删除user_book 里面的信息
	sql = "delete from user_book where uid = " + str(uid) + " and bid = " + str(bid)
	cursor.execute(sql)
	#2. 删除user_books_tags里面的信息
	sql = "delete from user_books_tags where uid = " + str(uid) + " and bid = " + str(bid)
	cursor.execute(sql)
	#3. 删除books里面的信息
	sql = "delete from books where id = " + str(bid)
	cursor.execute(sql)
	
	db.commit()
	
	
	