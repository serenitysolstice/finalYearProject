from informationExtraction import person
import unittest

class TestPerson(unittest.TestCase):

	def testIsPersonRealTrue(self):
		p = person.Person("Angela", "Medicine")
		b = person.Person.isPersonReal(p)
		self.assertEqual(b, True)

	def testIsPersonRealFalse(self):
		p = person.Person("Tracer", "Chronology")
		b = person.Person.isPersonReal(p)
		self.assertEqual(b, False)
		
if __name__ == "__main__":
		unittest.main()