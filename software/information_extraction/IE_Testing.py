import unittest
from app import extraction
from nltk import word_tokenize
from nltk.tree import Tree

class TestTextProcessing(unittest.TestCase):
	"""
	Tests the nlp_practice library
	"""
	
	def test_tagging(self):
		'''
		Tests that words are tagged correctly
		'''
		list = ["A", "single", "man", "in", "possession", "of", "a", "large", "fortune", "must", "be", "in", "want", "of", "a", "wife"]
		r = extraction.tag(list)
		self.assertEqual(r, [('A', 'DT'), ('single', 'JJ'), ('man', 'NN'), ('in', 'IN'), ('possession', 'NN'), ('of', 'IN'), ('a', 'DT'), ('large', 'JJ'), ('fortune', 'NN'), ('must', 'MD'), ('be', 'VB'), ('in', 'IN'), ('want', 'NN'), ('of', 'IN'), ('a', 'DT'), ('wife', 'NN')])
		
	
	def test_entities(self):
		'''
		Tests that entities are tagged correctly
		'''
		list = [('Thompson', 'NNP')]
		e = extraction.entities(list)
		self.assertEqual(e, Tree('S', [Tree('PERSON', [('Thompson', 'NNP')])]))
		
	def testisKeywords(self):
		'''
		Tests that keywords are detected from a list
		'''
		words = ["onion", "cauliflower", "pepper", "raspberry"]
		keywords = ["tomato", "onion", "potato", "lettuce", "cucumber", "pepper", "spring onion"]
		list = []
		for word in words:
			answer = extraction.isKeywords(word, keywords)
			list.append(answer)
		self.assertEqual(list, [True, False, True, False])
		
	def testcheckSpelling(self):
		list = ["Widnows", "are", "fro", "peolpe", "with", "no", "imagnatin"]
		result = []
		for w in list:
			a = extraction.checkSpelling(w)
			result.append(a)
		self.assertEqual(result, [False, True, False, False, True, True, False])
		
	def testfindTextOne(self):
		'''
		Tests the find Text function with one attribute labelled full_text
		'''
		testDict = {
			"response": {
			"docs": [{
			"article_word_count": 27,
			"category": "News",
			"collection_title": "Llanelly Star",
			"date": "1914-01-17T00:00:00Z",
			"date_day": 17,
			"date_decade": 1910,
			"date_month": 1,
			"date_weekday": 6,
			"date_year": 1914,
			"doc_type": "Newspapers-article",
			"edition_statement": "",
			"title_en": "eleven",
			"12": "twelve",
			"full_text": "I A CHEMISTRY DIPLOMA. Mr. Tom Williams",
			"id": "4122756-modsarticle24-4122757-1",},
			]}}
		a = extraction.findText(testDict)
		self.assertEqual(a, ["I A CHEMISTRY DIPLOMA. Mr. Tom Williams"])
		
	def testfindTextTwo(self):
		'''
		Tests the find Text function with two attributes labelled full text
		'''
		testDict = {
			"response": {
			"docs": [{
				"doc_type": "Newspapers-article",
				"full_text": "I A CHEMISTRY DIPLOMA. Mr. Tom Williams",
				"date_day": 14,
				"date_month": 3,
				"date_year": 1902,
				"id": "akldfapeiwfaofjewio",
				"title_en": "Manually finding these is so dull",
				"collection_title": "And its ten to three in the morning"
				},
				{
				"full_text": "in delivering a lecture recently on this subject at Perth",
				"date_day": 14,
				"date_month": 3,
				"date_year": 1902,
				"id": "akldfapeiwfaofjewio",
				"title_en": "Manually finding these is so dull",
				"collection_title": "And its ten to three in the morning"}
				]}}
		a = extraction.findText(testDict)
		self.assertEqual(a, ["I A CHEMISTRY DIPLOMA. Mr. Tom Williams", "in delivering a lecture recently on this subject at Perth"],)
		
		
	def testconvertToDict(self):
		ex = ('{ "a": { "b": [ { "c": [ "d", "e", "f"], "g": ["h","y"], "i": ["j", "k", "l", "m"]}]}}')
		a = extraction.convertToDict(ex)
		self.assertEqual(a, { "a": { "b": [ { "c": [ "d", "e", "f"], "g": ["h", "y"], "i": ["j", "k", "l", "m"]}]}})

	def testcreateName(self):
		tuples = [("Mr.", "NNP"), ("Tom", "NNP"), ("Williams", "NNP")]
		name = extraction.createName(tuples)
		self.assertEqual(name, "Mr. Tom Williams")
		
	def testcreatePeople(self):
		p = [([('Mr.', 'NNP'), ('Tom', 'NNP'), ('Williams', 'NNP')], 0), ([('Karlsruke', 'NNP')], 0), ([('Robinson', 'NNP')], 1), 
			([('W', 'NNP'), ('D', 'NNP'), ('Brooks', 'NNP')], 0), ([('Roberts', 'NNP')], 0)]
		people = extraction.createPeople(p, 1)
		names = []
		for e in people:
			names.append(str(e.name))
		self.assertEqual(names, ["Mr. Tom Williams"])
		

if __name__ == '__main__':
	unittest.main()