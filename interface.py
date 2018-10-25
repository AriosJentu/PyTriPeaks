import curses
import cards
import desk

cards_positions = [
	[1, 	       7,             19,            31       ],
	[3, 	     5,   9,        17,  21,       29,  33    ],
	[5, 	  3,   7,   11,  15,  19,  23,  27,  31,  35  ],
	[7, 	1,   5,   9,  13,  17,  21,  25,  29,  33,  37]	
]

#Decl Cards Positions: for current card, and for deck list
deck_card_pos = [10, 6]
deck_side_pos = [10, 12]

#Color definition
CARD_DEFAULT_COLOR = 1
CARD_SELECTED_COLOR = 2
CARD_RED_COLOR = 3
CARD_BLACK_COLOR = 4

#Current desk
current_desk = desk.CardDesk(cards.Deck(True))

#Function to get card coords from desk by index, real is for pop function
def get_card_coords_by_desk_index(desk=current_desk, index=0, real=False):

	try:
		cards_indexes = desk.get_available_cards_coordinates()
		y, x = cards_indexes[index] 

		if real:
			y, x = len(cards_positions)-y, x+1

		return (y, x)

	except:

		return (-1, -1)


#Drawing deck function
def draw_desk(carddesk=current_desk, level=0, desk_pos=0, menu_pos=0):

	#Clear game screen
	game_screen.clear()

	deskfield = carddesk.get_desk()
	#Draw game desk
	for i, v in enumerate(cards_positions):
		for j, u in enumerate(deskfield[i]):
			if u != 0:
	
				card_str = str(u)
				card_col = CARD_RED_COLOR

				if u.is_hidden():
					card_str = "###"
					card_col = CARD_DEFAULT_COLOR
				else:
					if u.get_suit().get_color() == "Black":
						card_col = CARD_BLACK_COLOR


				game_screen.addstr(v[0], v[j+1], card_str, 
					curses.color_pair(card_col) | curses.A_BOLD
				)

	#Current Card
	cur_card = carddesk.get_current_card()
	cur_card_col = CARD_RED_COLOR

	if cur_card.get_suit().get_color() == "Black":
		cur_card_col = CARD_BLACK_COLOR

	#Draw Current Card
	game_screen.addstr(*deck_card_pos, str(cur_card), 
		curses.color_pair(cur_card_col) | curses.A_BOLD
	)

	#Draw Deck Cards Count
	game_screen.addstr(*deck_side_pos, "#"*carddesk.get_deck_size(), 
		curses.color_pair(CARD_DEFAULT_COLOR) | curses.A_BOLD
	)

	#Colorization cursor
	#Levels - vertical cursor position, Positions - horizontal cursor positions
	#Level 0 - Choosing card with curses's cursor
	#Level 1 - Get card from deck
	#Level 2 - Menu

	#Level of field of selecting cards 
	if level == 0:
		
		#Get selected card indexes
		index_y, index_x = get_card_coords_by_desk_index(carddesk, desk_pos)
		if index_y == -1:
			level = 2
			return None
		
		#Calculate cursor position using array
		cursor_position = (
			cards_positions[index_y][0],
			cards_positions[index_y][index_x+1]
		)

		#Get selected card from desk, and get it's color
		selected_card = carddesk.get_desk()[index_y][index_x]
		selected_card_col = CARD_RED_COLOR

		if selected_card.get_suit().get_color() == "Black":
			selected_card_col = CARD_BLACK_COLOR

		#Draw Selected card
		game_screen.addstr(*cursor_position, "  "+str(selected_card)[-1:], 
			curses.color_pair(selected_card_col) | curses.A_BOLD
		)

		game_screen.addstr(*cursor_position, str(selected_card)[:-1], 
			curses.color_pair(CARD_SELECTED_COLOR) | curses.A_BOLD
		)

	#Level of current card
	elif level == 1:
		
		#Update current card color to selected
		#First 2 chars are colored to selected color
		#Last char (suit char) colored by suit color
		game_screen.addstr(*deck_card_pos, "  "+str(cur_card)[-1:], 
			curses.color_pair(cur_card_col) | curses.A_BOLD
		)

		game_screen.addstr(*deck_card_pos, str(cur_card)[:-1], 
			curses.color_pair(CARD_SELECTED_COLOR) | curses.A_BOLD
		)


	elif level == 2:
		pass


def key_search():

	#Pressed key
	key = 0	
	
	#Cursor level and position information
	cursor_level = 0
	desk_pos = 0
	menu_pos = 0

	#Infinity key calculation, while not exit
	available_count = current_desk.get_available_cards_count()
	while key != ord('q'):

		#Get pressed key
		key = game_screen.getch()

		#Undo move
		if key == ord('z'):
			try:
				current_desk.undo_move()
			except:
				pass

		#Generate new Field
		elif key == ord('n'):
			current_desk.generate(cards.Deck(True))

		#Regenerate current Field
		elif key == ord('m'):
			current_desk.regenerate()

		#Change Levels
		elif key == curses.KEY_UP:
			cursor_level = max(0, cursor_level-1)

		elif key == curses.KEY_DOWN:
			cursor_level = min(2, cursor_level+1)

		#Change positions of level
		elif key == curses.KEY_LEFT:
			
			if cursor_level == 0:
				desk_pos = max(0, desk_pos-1)

		elif key == curses.KEY_RIGHT:
			
			if cursor_level == 0:
				desk_pos += 1

		#Accept key
		elif (key == curses.KEY_ENTER or 
				key == 10 or 
				key == 13 or
				key == ord('f') or
				key == ord('e') or 
				key == ord(' ')
		):

			#For level 0 - pop selected card from desk
			if cursor_level == 0:

				coords = get_card_coords_by_desk_index(current_desk, desk_pos, 
						True
				)

				try:
					current_desk.pop_card_from_desk(*coords)
				except:
					pass

			#For level 1 - pop card from deck
			elif cursor_level == 1:
				try:
					current_desk.pop_card_from_deck()
				except:
					pass

		#Update counts
		available_count = current_desk.get_available_cards_count()
		desk_pos = min(desk_pos, available_count-1)
		
		draw_desk(current_desk, cursor_level, desk_pos, menu_pos)


try:

	game_screen = curses.initscr()

	curses.start_color()
	curses.use_default_colors()
	
	curses.init_pair(CARD_DEFAULT_COLOR, curses.COLOR_WHITE, -1)
	curses.init_pair(CARD_SELECTED_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(CARD_RED_COLOR, curses.COLOR_WHITE, curses.COLOR_RED)
	curses.init_pair(CARD_BLACK_COLOR, curses.COLOR_WHITE, curses.COLOR_BLUE)

	curses.cbreak()
	curses.noecho()
	curses.curs_set(False)
	game_screen.keypad(True)

	draw_desk(current_desk)
	key_search()

finally:
	
	curses.nocbreak()
	curses.echo()
	curses.curs_set(True)
	game_screen.keypad(False)

	curses.endwin()

