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

def get_desk_available_cards_coords(deskarray):

	coords = []

	################################################
	#TODO: Create method to get ordered coordinates#
	################################################

	"""
	i = 3
	j = 0
	flag = True

	while flag:

		if deskarray[i][j] != 0 and not deskarray[i][j].is_hidden():
			
			coords.append((i, j))

		elif deskarray[i][j] == 0:

			if j+1 < len(deskarray[i]) and deskarray[i][j+1] == 0:

				i -= 1
			
			pass

		j = j+1	
	"""

	"""
	#Cycle for lines, not included first line
	for j in range(1, 4):

		#Cycle for cards on line, not included last card
		for i in range(len(deskarray[j])-1):

			#Check for first card in this block
			if (type(deskarray[j][i]) != int 
					and not deskarray[j][i].is_hidden()):
				coords.append((j, i))

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
						coords.append((j-1, k))

			elif not deskarray[j][i+1].is_hidden():
				coords.append((j, i+1))
	"""

	return coords


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
