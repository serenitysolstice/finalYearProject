from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField
import tables
import re

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://tab23:Wormwaterfallwheel2@localhost/scientistsinwales"
app.config["SECRET_KEY"] = "b'\xcb/\xa2~w^G\x02;^\xa2\x04'"
db = SQLAlchemy(app)

class Scientist(db.Model):
	__tablename__ = "scientists"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), unique=False, nullable=False)
	field = db.Column(db.String(30), unique=False, nullable=False)
	articleID = db.Column(db.String(128), unique=True, nullable=False)
	url = None
	
	articlesR = db.relationship("Articles", backref="articleID")
	
	def __str__(self):
		return self.name
	
class Articles(db.Model):
	__tablename__ = "articles"
	id = db.Column(db.String(128), db.ForeignKey(Scientist.articleID), primary_key=True)
	articleTitle = db.Column(db.String(500), unique=False, nullable=False)
	articleDate = db.Column(db.DateTime, unique=False, nullable=False)
	newsTitle = db.Column(db.String(255), unique=False, nullable=False)
	url = None
	
	scientistsR = db.relationship("Scientist", backref="Articles.id")
	
	def __str__(self):
		return self.id

class searchForm(FlaskForm):
	choices = [("name", "Name"), ("field", "Field"), 
				("articleTitle", "Article Title")]
	select = SelectField("Search for data:", choices=choices)
	search = StringField("")
	
@app.route("/", methods=["GET", "POST"])
def index():
	search = searchForm(request.form)
	if request.method == "POST":
		flash("This is a test message")
		return search_results(search)
	return render_template("home.html", form=search)
 
def returnLinks(resultsList, type):
	if type == 1:
		urls = dict()
		for result in resultsList:
			urlParts = re.split("-", result.articleID)
			url = '/'.join((urlParts[0], urlParts[2], urlParts[3]))
			urls[result.articleID] = url
	elif type == 2:
		urls = dict()
		for result in resultsList:
			urlParts = re.split("-", result.id)
			url = '/'.join((urlParts[0], urlParts[2], urlParts[3]))
			urls[result.id] = url
	return urls

@app.route("/results", methods=["GET", "POST"])
def search_results(search):
		results = []
		urls = []
		search_string = search.data["search"]
		
		if search_string:
			#If there is a search string:
			#Determine the type of the search
			if search.data['select'] == 'name':
				#Search the database for scientist data
				qry = db.session.query(Scientist).filter(Scientist.name.contains(search_string))
				results = [item for item in qry.all()]
				urls = returnLinks(results, 1) #gets the url suffix for all results
			elif search.data['select'] == 'articleTitle':
				#Search the database for articles
				qry = db.session.query(Articles).filter(Articles.articleTitle.contains(search_string))
				results = [item for item in qry.all()]
				urls = returnLinks(results, 2)
			elif search.data['select'] == 'field':
				#Search the database for a field of study
				qry = db.session.query(Scientist).filter(Scientist.field.contains(search_string))
				results = [item for item in qry.all()]
				urls = returnLinks(results, 1)
				
		else:
			#Else an empty search.
			error = "Empty String"
			return redirect('/')
			
		if not results:
			error = "No results found"
			return redirect('/')
			
		elif not search.data['select'] == 'articleTitle':
			for u in urls:
				parts = re.split("/", u)
				for r in results:
					artIDParts = re.split("-", r.articleID)
					if artIDParts[0] == parts[0]:
						r.url = '/'.join(("https://newspapers.library.wales/view", u))
			table = tables.ScientistResults(results)
			table.border = True
			return render_template("results.html", table=table)
		else:
			for u in urls:
				parts = re.split("/", u)
				for r in results:
					artIDParts = re.split("-", r.id)
					if artIDParts[0] == parts[0]:
						r.url = '/'.join(("https://newspapers.library.wales/view", u))
			table = tables.ArticleResults(results)
			table.border = True
			
			return render_template("results.html", table=table, search=search)
			
@app.route("/redirect", methods=["GET", "POST"])
def linkClicked():
	
	return redirect("/")
		
if __name__ == "__main__":
	app.run(debug=True)