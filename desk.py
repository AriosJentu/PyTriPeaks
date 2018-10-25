import cards
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
	def __init__(self, deck=cards.Deck(True)):

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
		self.__states = []

		self.__current_card.set_hidden(False)


	#Bring card to current
	def bring(self, card, from_deck=False):

		if (not card.is_hidden() and 
				(rules.is_available_to_bring_card(self.__current_card, card)
				or from_deck)
		):

			self.__current_card = card

		else:
			print("WRONG")
			raise Exception("Unable to bring this card by game rules")


	#Getters
	def get_current_card(self):
		return self.__current_card

	def get_deck(self):
		return self.__deck.get_deck()

	def get_deck_size(self):
		return self.__deck.get_deck_size()

	def get_desk(self):
		return self.__desk

	def get_available_cards_coordinates(self):
		return rules.get_desk_available_cards_coords(self.__desk)

	def get_available_cards_count(self):
		
		cnt = 0

		for i in self.__desk:
			for j in i:
				if j != 0 and not j.is_hidden():
					cnt += 1

		return cnt


	def pop_card_from_deck(self):

		prev_card = self.__current_card
		
		card = self.__deck.pop_card()
		card.set_hidden(False)

		self.bring(card, True)

		#Save state of card to be abled to undo move
		self.__states.append([
			self.__current_card, 
			prev_card,
			-1 						#Means thats card is from deck
		])


	#Pop card from current desk, notice - line and position starts from 1,
	# line from bottom to top
	def pop_card_from_desk(self, line, position, callback=cards.empty_func):

		#Count of lines
		lines_count = len(CardDesk.__desktype)

		#Check position for correctness
		if not (0 <= lines_count-line < lines_count and 
				0 <= position-1 < len(CardDesk.__desktype[lines_count-line])
		):

			raise Exception("Desk Card Position wrong")


		#Check for availablety of current position
		if (self.__desk[lines_count - line][position-1] == 0 or 
				self.__desk[lines_count - line][position-1].is_hidden()
		):

			raise Exception("This position is unable")


		#Update current card and desk
		prev_card = self.__current_card
		self.bring(self.__desk[lines_count - line][position-1])
		self.__desk[lines_count - line][position-1] = 0

		#Save state of card to be abled to undo move
		self.__states.append([
			self.__current_card, 
			prev_card,
			line, 			#Coordinates in array
			position
		])

		#Refresh desk by popt card
		self.__desk = rules.refresh_desk_by_position(
			self.__desk, 
			lines_count - line, 
			position - 1,
			callback
		)

	def _push_card_to_desk(self, card, line, position, cbf=cards.empty_func):

		#Count of lines
		lines_count = len(CardDesk.__desktype)

		#Check position for correctness
		if not (0 <= lines_count-line < lines_count and 
				0 <= position-1 < len(CardDesk.__desktype[lines_count-line])
		):

			raise Exception("Desk Card Position wrong")


		#Check for availablety of current position
		if (self.__desk[lines_count - line][position-1] != 0):

			raise Exception("This position already taken: "+
				str(lines_count - line)+" "+
				str(position-1)
			)

		self.__desk[lines_count - line][position-1] = card

		#Refresh desk by popt card
		self.__desk = rules.refresh_desk_by_position(
			self.__desk, 
			lines_count - line, 
			position - 1,
			cbf,
			True
		)

	#Function to check - is desk empty
	def is_desk_empty(self):

		is_empty = True
		for i in self.__desk[0]:
			if i != 0:
				is_empty = False

		return is_empty


	#function to undo last move
	def undo_move(self):

		#If nothing to undo
		if len(self.__states) == 0:
			raise Exception("Nothing to undo")

		card_values = self.__states.pop()

		#If card from deck
		if card_values[2] == -1:

			#push it back to deck
			self.__deck._push_card_to_deck(card_values[0])

		else:

			#to desk
			self._push_card_to_desk(
				card_values[0], 
				card_values[2], 
				card_values[3]
			)

		self.__current_card = card_values[1]

