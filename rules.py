import cards

def is_available_to_bring_card(card1, card2):
	dif = abs(card1.get_index() - card2.get_index())
	return dif == 1 or dif == 12

def refresh_desk(deskarray, callback=cards.empty_func):

	#Cycle for lines, not included first line
	for j in range(1, 4):

		#Cycle for cards on line, not included last card
		for i in range(len(deskarray[j])-1):

			#Check for free two neighbour cards
			if deskarray[j][i] == deskarray[j][i+1] == 0:

				#On last line all correct, but for previous need
				# to divide by triangles
				if (j == 3 or (i+1)%(j+1) != 0):

					#By default, index is current
					k = i

					#If its third and second line, calculate index with 
					# triangle part index formula
					if j == 2:
						k = i%3 + i//3 + (i+1)//3
					elif j == 1:
						k = i//2
					
					#Show card by this index
					if type(deskarray[j-1][k]) != int:
						deskarray[j-1][k].set_hidden(False)
						callback(j-1, k)

	return deskarray


#Subfunction to calculate in one iteration for 2 card positions
def refresh_subfunction(deskarray, line, pos, callback=cards.empty_func):

	if deskarray[line][pos] == deskarray[line][pos+1] == 0:

		if line == 3 or (pos+1)%(line+1) != 0:

			k = pos

			if line == 2:
				k = pos%3 + pos//3 + (pos+1)//3
			elif line == 1:
				k = pos//2
			
			if type(deskarray[line-1][k]) != int:
				
				deskarray[line-1][k].set_hidden(False)
				callback(line-1, k)
			
	return deskarray


#Function to calculate desk updates by card position
def refresh_desk_by_position(deskarray, real_line, real_pos, 
		callback=cards.empty_func):

	if (real_line <= 0 
			or real_line > 3 
			or real_pos < 0 
			or real_pos > len(deskarray[real_line])):
		return deskarray

	#With right-side element
	if real_pos+1 < len(deskarray[real_line]):

		deskarray = refresh_subfunction(deskarray, real_line, real_pos, 
			callback
		)

	#With left-side element
	if real_pos-1 >= 0:

		deskarray = refresh_subfunction(deskarray, real_line, real_pos-1, 
			callback
		)

	return deskarray


def get_desk_available_cards_coords(deskarray):

	coords = []

	#  TETRAGON (PEAKS)  #
	#   /\----/\----/\   #
	#  /\/\--/\/\--/\/\  #
	# /\/\/\/\/\/\/\/\/\ #
	#/\/\/\/\/\/\/\/\/\/\#

	#Current enabled cursor position
	i = len(deskarray)-1	#Current Line
	j = 0					#Current Position, Calculation by tetragon
	flag = True 			#For exit

	#Getting positions in cycle by peaks
	while flag:

		k = j 			#Current Position, Calculation by peak
		cond = True		#Condition of correctness of index in peaks array (desk)

		#If it second line, calculate by 2/3 parts of line
		if i == 1:

			#Formula to get coordinate from tetragon to peak
			k = j%3 + j//3 + (j+1)//3
			cond = (j%3 != 2)


		#If it first line, calculate by end of peak
		elif i == 0:
			k = j//3
			cond = (k == j/3)


		#Exit condition
		if k >= len(deskarray[i]):
			flag = False
			break

		#Searching available cards:

		#'cond' = Check, is index in array correct
		#If field is empty
		if cond and deskarray[i][k] == 0:
			i -= 1 		#Move cursor for one point to top

		#if card on field is visible
		elif (cond and deskarray[i][k] != 2 and (
				deskarray[i][k] == 1 or 
				not deskarray[i][k].is_hidden()
		)):

			coords.append((i, k)) 	#Save coordinate
			j += 1					#Go to the next position card

		#If card on this position is hidden
		else:
			i += 1	#Go down
			j += 1 	#And to the next position (cause triangle)

		#If cursor position left tetragon
		if i < 0:
			i = len(deskarray)-1 	#Get it to the last line of tetragon
			j += i 					#And move cursor to next enabled part


	#Return found coords
	return coords


"""
tab = [
	[      2,          2,          2      ],
	[    2,  2,      2,  2,      2,  2    ],
	[  2,  2,  2,  2,  2,  2,  2,  2,  2  ],
	[0,  1,  1,  1,  1,  1,  1,  1,  1,  1]
]
s = get_desk_available_cards_coords(tab)
for i in s:
	print(i)

"""