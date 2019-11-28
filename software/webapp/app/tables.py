from flask_table import Table, LinkCol, Col

class ScientistResults(Table):
	id = Col("ID", show=False)
	name = Col("Name")
	field = Col("Field")
	#articleID = LinkCol("articleID", "linkClicked")
	articleID = Col("articleID")

class ArticleResults(Table):
	#id = LinkCol("ID", "linkClicked")
	id = Col("ID")
	articleTitle = Col("Title")
	newsTitle = Col("Newspaper")
	