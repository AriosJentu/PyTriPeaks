import curses

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

#Drawing deck function
def draw_desk(level=-1, desk_pos=0, menu_pos=0):

	#Clear game screen
	game_screen.clear()

	#Draw game desk
	for i in cards_positions:
		for j in i[1:]:

			game_screen.addstr(i[0], j, "###", 
				curses.color_pair(CARD_DEFAULT_COLOR) | curses.A_BOLD
			)

	#Current Card
	game_screen.addstr(*deck_card_pos, "###", 
		curses.color_pair(CARD_DEFAULT_COLOR) | curses.A_BOLD
	)

	#Draw Deck Cards Count
	game_screen.addstr(*deck_side_pos, "#"*23, 
		curses.color_pair(CARD_DEFAULT_COLOR) | curses.A_BOLD
	)

	#Colorization cursor
	#Levels - vertical cursor position, Positions - horizontal cursor positions
	#Level 0 - Choosing card with curses's cursor
	#Level 1 - Get card from deck
	#Level 2 - Menu

	if level == 0:
		pass

	elif level == 1:
		
		#Update current card color to selected
		game_screen.addstr(*deck_card_pos, "###", 
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
	while key != ord('q'):

		key = game_screen.getch()

		if key == curses.KEY_UP:
			cursor_level = max(0, cursor_level-1)

		elif key == curses.KEY_DOWN:
			cursor_level = min(2, cursor_level+1)


		draw_desk(cursor_level, desk_pos, menu_pos)


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

	draw_desk()
	key_search()

finally:
	
	curses.nocbreak()
	curses.echo()
	curses.curs_set(True)
	game_screen.keypad(False)

	curses.endwin()

