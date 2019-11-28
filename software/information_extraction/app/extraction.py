from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk import ne_chunk, pos_tag, chunk, Tree
import json
from informationExtraction import spell_corrector
from informationExtraction import article
import ast, os, sys
import mysql.connector
from mysql.connector import Error
from nameparser import HumanName
from informationExtraction import person
import python_mysql_dbconfig

stopWords = set(stopwords.words('english'))
#for some reason, adding these characters to the stopwords set stops them from being 'corrected' into the character 's'
stopWords.update("""'.,(){}//"!%&^""")
article_list = []
final_articles = []
fieldOfStudy = ["astronomy", "biology", "chemistry", "mathematics", "physics"]#List of potential study fields. 
listOfPerson = []

def filterWords():
	'''
	Removes the stop words from an article. No longer in use, kept around just 
	in case it comes in handy.
	'''
	filteredWords = []
	for w in words:
		if w not in stopWords:
			filteredWords.append(w)
	return filteredWords
	
def lowerCase(words):
	'''
	Turns a list of words into a list where all words are lower case
	NOT TO BE USED until feeding text into the database: removing capital letters
	makes it incredibly hard to extract meaning using the NLTK.
	'''
	lower_case = [w.lower() for w in words]
	return lower_case

def tag(list):
	'''
	Takes a list of words, turns the list into a list of tuples
	Each tuple is (<word>, <part of speech tag>).
	Returns the tuple list
	'''
	tagged = pos_tag(list)
	return tagged

def entities(list):
	'''
	Creates a Tree object from a list of tuples. 
	All leaves are tuples of words and their part of speech
	Any subtrees are entities of type subtree.label().
	'''
	e = ne_chunk(list)
	return e

#Original code from here
#https://stackoverflow.com/questions/40188226/nltks-spell-checker-is-not-working-correctly
#This essentially just determines whether or not a word is spelled correctly
#Returns true if it is, false if it is not. 
def checkSpelling(word):
		if not wordnet.synsets(word):
			if word in stopWords:
				#print("good word")
				return True
			else:
				#print("bad word")
				return False
		else:
			#print("good word")
			return True

def correctSpelling(words):
	'''
	Checks to determine whether or not a word needs to be corrected
	Corrects it if so
	Parameter is a list of words
	Returns the same list, with words spelled correctly
	NOTE: not perfect, but good enough. 
	'''
	checked = []
	for w in words:
		if not checkSpelling(w):
			#print("Word needs correcting")
			w = spell_corrector.correction(w)
			#print("word corrected")
			checked.append(w)
		else: 
			#print("No correction needed")
			checked.append(w)
	return checked

def isKeywords(word, list):
	for w in list:
		if word is w:
			return True
	
	return False

def findText(d):
	'''
	Looks for the full text of the article, and returns it as a strings that is added to a list
	Also finds the metadata for that specific article, creates an article object and attaches the 
		metadata to that object. Adds the article to a global list of articles
	Parameter is a dictionary of article data and metadata
	'''
	text_list = []
	counter = 0
	for doc in d['response']['docs']:
		''' Comment out the below lines for actual running of code '''
		print("Finding for article" + str(counter))
		counter = counter + 1
		''''''
		text_done = False #stops the same article being written over and over again
		text_list.append(doc['full_text'])
		if doc['date_day'] < 10:
			day = '0' + str(doc['date_day'])
		else :
			day = str(doc['date_day'])
		if doc['date_month'] < 10:
			month = '0' + str(doc['date_month'])
		else:
			month = str(doc['date_month'])
		date = (str(doc['date_year']) + "/" + month + "/" + day)
		art = article.Article(doc['id'], date, doc['title_en'], doc['collection_title'])#create article using current article metadata
		article_list.append(art)
		text_done = True
		if text_done == True:
			continue

	return text_list

def convertToDict(text):
	'''
	Takes in a string, and converts it to a dictionary
	'''
	text = ast.literal_eval(text)
	return text
		
def createName(tuples):
	'''
	Iterate over a list of tuples, remove the second element and save to 
	a temporary list
	Take that list, and turn it into a string, then turn that string in to 
	a name.
	Return the name
	'''
	name_parts = []
	for tup in tuples:
		name_parts.append(tup[0])
		name = HumanName(' '.join(name_parts))
	return name
	
def isPersonReal(name):
		'''
		Determines whether a name is actually a human name
		Returns true if so, and false if not
		Designed to remove instances where the named entity chunker fails me.
		'''
		isReal = False
		with open("C:\\Users\\user\\Documents\\major_project\\A collection of scientists in Wales between 1804 and 1919 built using Natural Language Processing techniques\\software\\textfiles\\NAMES.txt", "r") as file:
			with open("C:\\Users\\user\\Documents\\major_project\\A collection of scientists in Wales between 1804 and 1919 built using Natural Language Processing techniques\\software\\textfiles\\SURNAMES.txt", "r") as f:
				listOfNames = file.read()
				listOfSurnames = f.read()
				for names in listOfNames:
					if names[0] == name[0]:
					#if the first letter of the current name matches the first letter of the wanted name
					#makes the search through over 150000 names not take forever
						if name in listOfNames or name in listOfSurnames:
							isReal = True
						else:
							isReal = False
					else:
						continue
		return isReal
		
def createPeople(listOfPeople, fieldInt):
	lPeople = []
	for p in listOfPeople:
		names = p[0]
		aNumber = p[1]
		n = createName(names)
		if not str(n.first) == "" and not str(n.last) == "": #occassionally, a person had no first name. Index out of bounds error if not checked for.
			if isPersonReal(n.first) and isPersonReal(n.last) and not str(n.title) == "": 
				#if both names of the person are real names, and the person has a title
				study = fieldOfStudy[fieldInt] #fieldInt increased in the file for loop
				human = person.Person(n, study)
				#comment out the below line for testing purposes - Nothing in article_list
				human.assignArticle(article_list[aNumber].id)
				lPeople.append(human)
		
	return lPeople
	
'''def determineActions(articleTexts){

}'''
def connectDB():
	dbConfig = python_mysql_dbconfig.read_db_config()
	try:
		database = mysql.connector.connect(**dbConfig)
		if database.is_connected():
			print("Connected to database")
	except Error as e:
		print(e)
		database.close()
	return database

def populateScientists():
	db = connectDB()
	if db.is_connected():
		cursor = db.cursor(buffered=True)
		for p in people:
			addScientist = """ INSERT INTO scientists (name, field, articleID) 
					VALUES (%s, %s, %s);"""
			try:
				print("Scientist " + str(p.name) + " is being added")
				cursor.execute(addScientist, (str(p.name), p.field, p.article))
				db.commit()
			except Error as error:
				print(error)
				cursor.close()
				db.close()
		cur = db.cursor(buffered=True)
		query = """ SELECT * FROM scientists; """
		cur.execute(query)
		print(cur.fetchall())
		cursor.close()
		cur.close()
		db.close()
	else:
		print("Database connection Error")
	
def populateArticles():
	'''
		Adds articles to database
		Need to introduce a check for whether or not an article-id is already in the database.
		Articles can show up for multiple keywords.
	'''
	db = connectDB()
	if db.is_connected():
		cursor = db.cursor(buffered = True)
		query = """ SELECT articleID FROM articles;"""
		cursor.execute(query)
		list_articles = cursor.fetchall()
		print(list_articles)
		for a in final_articles:
			c = db.cursor(buffered = True)
			articleIDTup = (a.id,)
			print(articleIDTup)
			if not list_articles == []:
				#if the database is not empty
				if not articleIDTup in list_articles:
					#check to make sure an article has not already been added
					print("Articles not the same")
					addArticle = """ INSERT INTO articles (articleID, articleTitle, articleDate, newsTitle)
						VALUES (%s, %s, %s, %s);"""
					try:
						print("Article " + a.id + " is being added")
						c.execute(addArticle, (a.id, a.title, a.date, a.newspaper))
						db.commit()
					except Error as error:
						print(error)
						c.close()
						db.close()
			else:
				addArticle = """ INSERT INTO articles (articleID, articleTitle, articleDate, newsTitle)
					VALUES (%s, %s, %s, %s);"""
				try:
					print("Article " + a.id + " is being added")
					c.execute(addArticle, (a.id, a.title, a.date, a.newspaper))
					db.commit()
				except Error as error:
					print(error)
					c.close()
					db.close()
						
		cursor = db.cursor(buffered = True)
		query = """ SELECT articleID FROM articles;"""
		cursor.execute(query)
		print(cursor.fetchall())
		cursor.close()
		db.close()
	else:
		print("Database connection error")
		
def setFieldStudy(fileName):
	if fileName == "astronomy.json" or fileName == "astronomyTest.json":
		field = 0
	elif fileName == "biology.json"or fileName == "biologyTest.json":
		field = 1
	elif fileName == "chemistry.json" or fileName == "chemistryTest.json":
		field = 2
	elif fileName == "mathematics.json"or fileName == "mathematicsTest.json":
		field = 3
	elif fileName == "physics.json"or fileName == "physicsTest.json":
		field = 4
	else:
		print("File not found")
		sys.exit()
	return field
	
def comparePeople(p1, p2):
	"""
		Compares whether two people objects are the same or not. 
		Returns true if they are, and false if they are not.
		Compares based on their names, then their field of study, and finally by the article
		they appear in.
	"""
	if str(p1.name) == str(p2.name) and p1.field == p2.field and p1.article == p2.article:
		return True
	else:
		return False
	
def compareArticles(a1, a2):
	"""
		Compares whether two article objects are the same or not
		Returns true if they are and false if they are not
		Compares based on the article ids of the article
		
	"""
	if a1.id == a2.id:
		return True
	else:
		return False
	
'''Running on a test set of data, because running on the full dataset takes literal hours.'''
if __name__ == '__main__':
	people = []

	#c = 0 #counter for files. Should be no more than six
	with open("keywords.txt", "r") as f:
		#for folders in os.walk(".\\jsonData"):
			#fileList = folders[2] #the element of the folders tuple that  pertains to files
			#for fl in fileList:
			fl = input("Enter filename: ")
			fieldInt = setFieldStudy(fl)
			filePath = os.path.join("..\\data\\jsonTestData", fl) #two relevent directories are jsonTestData and jsonData
			with open(filePath, "r") as file:
				keywords = f.read()
				data = json.load(file) #load json file into dictionary
				text = findText(data) #find the article text within each article
				print("Text found")
				art_number = 0
				print("File path is:" + str(filePath)) #print the current file path - useful for checking which file currently being read
				for art in text:
					print("Article number is: " + str(art_number))
					#first normalize the text
					words = word_tokenize(art)
					words = correctSpelling(words)
					#part-of-speech tagging
					tagged = tag(words)
					''''''
					print(tagged)
					''''''
					#Tag named entities; turn text into a tree
					ent = entities(tagged)
					''''''
					print(ent)
					''''''
					#for each object in the tree
					for w in ent:
						if type(w) is Tree:
							#if the child is a tree, that makes its leaves entities.
							if w.label() == "PERSON":	#if the child is labelled as 'person', it has found a person.
								tempPerson = (w.leaves(), art_number)
								listOfPerson.append(tempPerson)
					art_number = art_number + 1
				tempPeople = createPeople(listOfPerson, fieldInt) #create people from the person list
				for p in tempPeople:
					''''''
					print(str(p.name))
					''''''
					peopleCount = 0
					for q in tempPeople:
						#Removes a person from the list of people if they are in there
						#multiple times
						if comparePeople(p, q): 
							peopleCount = peopleCount + 1
							if peopleCount > 1:
								tempPeople.remove(q)
							else:
								people.append(p)
						else:
							continue
				for a in article_list:
					''''''
					print(a.title)
					''''''
					articleCount = 0
					for b in article_list:
						if compareArticles(a, b):
							articleCount = articleCount + 1
							if articleCount > 1:
								article_list.remove(b)
								print("Article " + b.id + " has been removed")
							else: 
								final_articles.append(a)
								print("Article " + a.id + " has been added")
						else:
							continue
				#populateScientists()
				#populateArticles()

