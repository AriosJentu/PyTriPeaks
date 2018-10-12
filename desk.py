from cards import Deck
import rules

#Class Of Desk with Cards
class CardDesk:

	#List of lists - how looks like desk
	__desktype = [
		[      0,          0,          0      ],
		[    0,  0,      0,  0,      0,  0    ],
		[  0,  0,  0,  0,  0,  0,  0,  0,  0  ],
		[0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
	]

	#Initialization desk with deck of cards
	def __init__(self, deck=Deck(True)):

		#Copy desk list
		carddesk = [i.copy() for i in CardDesk.__desktype]

		#Push cards from deck to desk
		for i, v in enumerate(carddesk):
			for j, _ in enumerate(v):
				carddesk[i][j] = deck.pop_card()

		#Show front available cards
		for k in carddesk[-1]:
			k.set_hidden(False)

		#Desk Properties
		self.__current_card = deck.pop_card()
		self.__deck = deck
		self.__desk = carddesk

		self.__current_card.set_hidden(False)


	#Bring card to current
	def bring(self, card):
		if not card.is_hidden() and rules.is_available_to_bring_card(self.__current_card, card):
			self.__current_card = card
		else:
			raise Exception("Unable to bring this card by game rules")


	#Getters
	def get_current_card(self):
		return self.__current_card

	def get_deck(self):
		return self.__deck.get_deck()

	def get_desk(self):
		return self.__desk


	def pop_card_from_deck(self):
		self.__current_card = self.__deck.pop_card()

	#Pop card from current desk, notice - line and position starts from 1, line from bottom to top
	def pop_card_from_desk(self, line, position):

		#Count of lines
		lines_count = len(CardDesk.__desktype)

		#Check position for correctness
		if not (0 <= lines_count-line < lines_count and 0 <= position-1 < len(CardDesk.__desktype[lines_count-line])):
			raise Exception("Desk Card Position wrong")

		#Check for availablety of current position
		if self.__desk[lines_count - line][position-1] == 0 or self.__desk[lines_count - line][position-1].is_hidden():
			raise Exception("This position is unable")

		#Update current card and desk
		self.bring(self.__desk[lines_count - line][position-1])
		self.__desk[lines_count - line][position-1] = 0
		self.__desk = rules.refresh_desk_by_position(self.__desk, lines_count - line, position - 1)


	#Function to check - is desk empty
	def is_desk_empty(self):

		is_empty = True
		for i in self.__desk[0]:
			if i != 0:
				is_empty = False

		return is_empty
