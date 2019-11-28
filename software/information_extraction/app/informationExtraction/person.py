
class Person():

	def __init__(self, name, field):
		self.name = name
		self.field = field
		self.action = None
		self.article = None
		
	def assignArticle(self, articleID):
		self.article = articleID
		
	def isPersonReal(self):
		'''
			Determines whether a name is actually a human name
			Returns true if so, and false if not
			Designed to remove instances where the named entity chunker fails me.
		'''
		name = self.name
		with open("C:\\Users\\user\\Documents\\major_project\\what-made-scientists-in-wales-famous-and-infamous-1804-1919\\software\\textfiles\\NAMES.txt", "r") as file:
			listOfNames = file.read()
			for names in listOfNames:
				if names[0] == name[0]:
				#if the first letter of the current name matches the first letter of the wanted name
				#makes the search through over 150000 names not take forever
					if name in listOfNames:
						isReal = True
					else:
						isReal = False
				else:
					continue
		return isReal

	
