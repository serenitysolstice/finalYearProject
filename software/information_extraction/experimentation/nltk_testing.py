from nltk.tokenize import word_tokenize
from nltk import ne_chunk, pos_tag

text = ("A curious experiment. A distinguished German biologist—Dr. Weisman —is making experiments in the way of trying to show that artificial modifications made "
	"in living animals may be reproduced in succeeding genera- tions. He has taken 900 white mice, and cut off their tails with a carving knife," 
	"or some other in- strument, and he hopes in time to produce from these mice that will be born tailless. "
	"This is not under. taken because a breed of tailless white mice is urgently needed, but to establish a great fact, if it be a fact, in evolution."
	"Whatever success Dr. Weisman may attain, says a correspondent, his attempt iB much more on scientific lines than the theory recently set by an amateur naturalist,"
	"with much gravity and alleged circumstance, that the Manx or tailless cat is the product of a chance cross between the ordinary domestic tabby and the wild rabbit."
	"As the Manx cat is a perfect cat in every- thing but its tail, showing nothing of the structure or habits of the rabbit, and as the pairing of a long tailed animal"
	"with a short tailed animal would not be likely to abolish the tail altogether: as the rabbit is entirely herbivorous and the cat almost entirely carnivorous, and as "
	"the cat would be much^ more likely to eat the rabbit than to pair with it, the amateur naturalist can hardly be said to have brought to light a great scientific truth. "
	"What Dr. W eisman will do with his mice remains to be seen. ")
words = word_tokenize(text)
tagged = pos_tag(words)
ent = ne_chunk(tagged)

for e in ent:
	print(e)