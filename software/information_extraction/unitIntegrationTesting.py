import unittest
from app import extraction
import json
from nltk import word_tokenize, pos_tag, ne_chunk, Tree

class TestInformationExtraction(unittest.TestCase):
	
	'''
		Test that text is found, tokenized and spellchecked
		correctly.
		Test that the parts of speech create the correct entities
		and those entities create people.
		Test that these people are removed when they appear more 
		than once in an article.
	'''
	def testTextCollection(self):
		'''
			Tests that the text of articles is extracted properly, that articles are broken
			down into words, and these words are spelled correctly. 
			The assertion list of words was generated using each method called here seperately,
			manually checked for expected output, and used here to check that all three methods
			work as intended when combined.
		'''
		wordList = []
		with open(".//jsonTestData//astronomyTest.json") as file:
			data = json.load(file)
			text = extraction.findText(data)
			for art in text:
				words = word_tokenize(art)
				words = extraction.correctSpelling(words)
				for word in words:
					wordList.append(word)
			self.assertEqual(wordList, ['PORTMADOO', '.', 'ASTRONOMY', 'AND', 'NAVIGATION.—', 'Mr', 'hugh', 'Hughes', ',', 'headmaster', 
			'of', 'the', 'centre', "'", 're', 'felon', 'Board', 'School', ',', 'has', 'won', 'certificates', 'of', 'competency', 'in', 
			'advanced', 'nautical', 'astronomy', 'and', 'advanced', 'navigation', '.', 'DENBIGH', 'AND', 'DISTRICT', '.', 'As.ramo', ')', 
			'.', 'LitcrtriiBi.—Professor', 'J', 'will', 'resting', 'W', '104ang', 'oo', 'Astronomy', ',', 'of', 'tbeCoouty', '8', 'this', 
			'craft', '(', 'Rrfiay', ')', ',', 'at', '8', 'aloe', '.', 'to', 'liitnrn', 'by', ',', 'UsisplltMll^', 'Llysfaen', '.', 'ah', 
			'the', "'", 'A', 'LECTURE.—In', 'connection', 'imparted', 'Mutual', 'Improvement', 'Society', 'recently', 's', 'de', 'in', 
			'Llysfaen', ',', 'Mr', 'of', 'Brython', 'Hughes', 'y', 'liver', 'a', 'lecture', 'on', 'of', 'Astronomy', ',', 'of', 'or', 
			'evening', '.', 'ASTRONOMY', '.', 'Archdeacon', 'Bruce', 'has', 'presented', 'the', 'Astro-', 'nominal', 'Society', 'of', 
			'Wales', 'with', 'a', 'valuable', 'cold', 'election', 'of', 'astronomical', 'works', ',', 'to', 'be', 'housed', 'in', 'the', 
			'Free', 'Library', '.'])
				
	def testTagging(self):
		'''
			Tests that part of speech tagging leads to correct named entity recognition,
			which leads to the creation of people. As above, each method used here was 
			called individually on the test file before this test was ran. 
		'''
		text = ("\"Mr Grayson's Disloyalty I REFERENCE TO THE j !N8ULT!NG REFERENCE TO THE KING Speaking "
		"at a densely crowded meeting under the auspices of the Social Democratic Federation at Lincoln on Friday "
		"evening, Mr. Victor Grayson said in the last week or so the country had been seething. A tumult had been going "
		"on because of a certain breach of law and order. His reply was that the first breach of law and order was committed "
		"when the upper and middle classes filched from the workers the means to live. All other questions must be put on "
		"the shelf inexorably till that of unemployment was settled. The Socialist was not \"*U extraordinary person. He "
		"was merely an obeservant animal, who saw an object in the streets and did not content himself with seeing the object, "
		"but saw through it and philosophised on it. Some time ago Parliment were asied to consider the question of feeding "
		"the school-children. They said, \"We have no time. We have an overlapping programme. We have legislative indigestion, and "
		"we cannot spare a half-day to devote to the feeding of ohildren.\" (\"Shame.\") It was not a week after that that the House "
		"of Commons was wasting a couple of hours congratulating the Prince j of Wales on the birth of a child. (\"Shame.\") Starving "
		"Dog Parallel Mr. Grayson continued: The Premier, John Barns, and Winston Churchill all said there will be no legislation "
		"for unemployment this year. Oh, get a poor starving dog and starve him until you have starved him almost to a skeleton, "
		"and when the dog makes a bound for you, determined to have food, you say to that dog: \"There will be no food this year; we "
		"have an overcrowded programme.\" The dog will remind you of its undercrowded stomach. Then when the dog bites, you shout, "
		"\"Order, order!\" I would break the most sacred law on God's earth if that law stood between a human being and a meal. I "
		"believe that to die of starvation in the land of plenty would disgrace the most Primitive people who ever lived. We do not "
		"want to feed the loafer when the loafer has a chance to work apid on medical inspection is found fit and only mentally "
		"indisposed. I would commit him to the lethal chamber with as little compunction as I would kil a rat. I do not love a "
		"loafer, but I tell you that when they counted the dead bodies afterwards there would be more aristocrats amongst them "
		"than people of the lower classes. (Cheers, groans, ami prolonged interruptions.) They (the Socialists), continued Mr. "
		"Grayson, told the Government they believed they knew how this problem of unemployment could be solved. They might not be "
		"right. He merely stated they had worried out a way of solving the problem. They thought it was right. They were willing to "
		"give their lives for it, and they asked for a trial to find out how to solve unemployment. They would no longer conduct "
		"themselves decorously to society if society refused them the last chance of feeding the hungry population. If one "
		"man starved they all felt branded with the brand of murder. A Parasite.\" Questions were invited at the close, and promptly "
		"mm-c the query, What did you call the King the other day?\" Mr. Grayson answered: \"I think the term I used was a term well "
		"known in biology-a, parasite. (Prolonged hooting.) A parasite is an organism that draws its sustenance from another organism. "
		"I have not the slightest objection to the King. I might be in favour of some decorative symbol under Socialism of a "
		"similar kind. All capitalists are parasites. The King draws rent, interest, and profits out of investments in land and "
		"companies. Rent and profits are exclusively produced by labour, and the person who takes them to live on while others "
		"create them is known in biology ae a parasite, and I have applied it to sociology. The Insults of Ananias.\" Mr. \"Jack\" "
		"Williams, speaking on Friday at a demonstration of the unemployed on Tower Hill, said time after time on the floor of "
		"the House of Commons the working class had been insulted, and even while Labour members sat and listened, raising no protest "
		"whatever. John Burns had called them a drunken lot. After telling them that they spent seven bob a week on beer, he went "
		"further, and said that the unemployed of England were more drunken than the unemployed of America. They were asked to "
		"put up with the insults of Ananias, and not 1100 any strong language. I l H")
		listOfPerson = []
		names = []
		art_number = 1
		fieldInt = 1
		words = word_tokenize(text)
		tagged = extraction.tag(words)
		ents = extraction.entities(tagged)
		for e in ents:
			if type(e) == Tree:
				tempPerson = (e.leaves(), art_number)
				listOfPerson.append(tempPerson)
		tempPeople = extraction.createPeople(listOfPerson, fieldInt) #create people from the person list
		for p in tempPeople:
			names.append(str(p.name)) #Turns the name into a string so that it's easier to compare
		self.assertEqual(names, ["Mr. Victor Grayson"])
		
	def testDuplicity(self):
		finalPeople = []
		names = []
		listOfPeople = [([("Mr", "NNP"), ("Thomas", "NNP"), ("Cook", "NNP")], 1), ([("Miss", "NNP"), ("Jane", "NNP"), ("French", "NNP")], 2), ([("Mr", "NNP"), ("Thomas", "NNP"), ("Cook", "NNP")], 1)]
		people = extraction.createPeople(listOfPeople, 1)
		for p in people:
			peopleCount = 0
			for q in people:
				#Removes a person from the list of people if they are in there
				#multiple times
				if extraction.comparePeople(p, q): 
					peopleCount = peopleCount + 1
					if peopleCount > 1:
						people.remove(q)
					else:
						finalPeople.append(p)
				else:
					continue
		for i in finalPeople:
			names.append(str(i.name))
		self.assertEqual(names, ["Mr Thomas Cook", "Miss Jane French"])
		
if __name__ == '__main__':
	unittest.main()