from datetime import datetime

class Article():
	
	def __init__(self, id, date, title, newspaper):
		self.newspaper = newspaper
		self.date = datetime.strptime(date, '%Y/%m/%d')
		self.title = title
		self.id = id
		