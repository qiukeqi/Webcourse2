#coding=utf-8
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_script import Shell,Manager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/booklib'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
migrate = Migrate(app,db) 

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class user(db.Model):
	id = db.Column(db.Integer,autoincrement=True, primary_key=True)
	name = db.Column(db.String(128),unique = True)
	passwd = db.Column(db.String(32))
	lastLoginTime = db.Column(db.DateTime)

class books(db.Model):
    id = db.Column(db.Integer, autoincrement = True,primary_key=True)
    name = db.Column(db.String(64))
 
class user_book(db.Model):
	uid = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
	bid = db.Column(db.Integer,db.ForeignKey('books.id'),primary_key=True)
	date = db.Column(db.DateTime)
	readpage = db.Column(db.Integer)
	totalpage = db.Column(db.Integer)

class tags(db.Model):
	name = db.Column(db.String(64),primary_key = True)
	
class user_books_tags(db.Model):
	uid = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
	bid = db.Column(db.Integer,db.ForeignKey('books.id'),primary_key=True)
	tn = db.Column(db.String(64),db.ForeignKey('tags.name'),primary_key=True)

if __name__ == '__main__':
    manager.run()