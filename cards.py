from random import shuffle

def empty_func(*a):
	pass

#Class of Suit of card
class Suit: 

	#Dict with information of suits 
	#Styles like Suits[char_index] containing Full Name and Color
	__suits = {
		"c":["Clubs", 		"Black",	"♣"],
		"s":["Spades", 		"Black",	"♠"],
		"d":["Diamonds", 	"Red",		"♦"], 
		"h":["Hearts", 		"Red",		"♥"]
	}

	#initialization with char index of suit
	def __init__(self, suitstr):

		#Checking for correctness char_index
		if suitstr not in self.__suits.keys():
			raise Exception("Suit index is incorrect")

		#Object Private Fields
		self.__index = suitstr
		self.__name = self.__suits[suitstr][0]
		self.__color = self.__suits[suitstr][1]
		self.__char = self.__suits[suitstr][2]

	#Converting Class Object to string with basic information 
	def __str__(self):
		return "Suit - "+self.__name+" "+self.__color+";"


	#Getters
	def get_name(self):
		return self.__name

	def get_color(self):
		return self.__color

	def get_index(self):
		return self.__index

	def get_char(self):
		return self.__char

	#Static method for getting Suit dictionary
	@staticmethod
	def get_suits():
		return Suit.__suits

#Class of Cards
class Card:

	#Initialization with card index (number) and suit with Suit class
	def __init__(self, index, suit):

		#Checking for correctness Card Index
		if index not in ["J", "Q", "K", "A"] and not (1 <= int(index) <= 13):

			raise Exception(
				"Index should be between 1 and 13 or can be J, K, Q or A"
			)


		#Checking for correctness Suit
		if type(suit) != Suit:
			raise Exception("Suit is incorrect")

		#Card Name
		name = str(index)

		if name in ["1", "11", "12", "13"]:
			name = {"11":"J", "12":"Q", "13":"K", "1":"A"}[name]

		if index in ["J", "Q", "K", "A"]:
			index = {"J":11, "Q":12, "K":13, "A":1}[index]


		#Object Private Fields
		self.__index = int(index)
		self.__suit = suit
		self.__name = name
		self.__hidden = True


	#Converting Class Object to string with basic information 
	def str(self):
		return "Card - "+str(self.__name)+"; "+str(self.__suit)

	def __str__(self):
		return "%2s"%self.__name+self.__suit.get_char()


	#Setters
	def set_hidden(self, boolean):
		self.__hidden = bool(boolean)


	#Getters
	def is_hidden(self):
		return self.__hidden

	def get_name(self):
		return self.__name

	def get_suit(self):
		return self.__suit

	def get_index(self):
		return self.__index


#Class of deck
class Deck:

	
	#Generating list of suits and cards
	__suits = [Suit(i) for i in Suit.get_suits().keys()]
	
	#Initialization
	def __init__(self, shuff=False):

		#Generating list with cards
		cards = [Card(i, j) for i in range(1, 14) for j in Deck.__suits]

		#Default Object Properties
		self.__cards = cards
		self.__cards_count = len(cards)

		#If flag shuffling, shuffle cards
		if shuff:
			self.shuffle()


	#Shuffling deck
	def shuffle(self):
		shuffle(self.__cards)


	#Getters

	#Getting last card from deck
	def pop_card(self):
		
		if self.__cards_count == 0:
			raise Exception("Deck is empty")

		self.__cards_count -= 1
		return self.__cards.pop()


	def get_deck(self):
		return self.__cards

	def get_deck_size(self):
		return self.__cards_count


	def _push_card_to_deck(self, card):
		
		if type(card) != Card:
			raise Exception("Trying to push non-card object to deck")

		card.set_hidden(True)
		self.__cards.append(card)
		self.__cards_count += 1