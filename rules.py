from cards import Card

def is_available_to_bring_card(card1, card2):
	dif = abs(card1.get_index() - card2.get_index())
	return dif == 1 or dif == 12

def refresh_desk(deskarray):

	#Cycle for lines, not included first line
	for j in range(1, 4):

		#Cycle for cards on line, not included last card
		for i in range(len(deskarray[j])-1):

			#Check for free two neighbour cards
			if deskarray[j][i] == deskarray[j][i+1] == 0:

				#On last line all correct, but for previous need to divide by triangles
				if (j == 3 or (i+1)%(j+1) != 0):

					#By default, index is current
					k = i

					#If its third and second line, calculate index with triangle part index formula
					if j == 2:
						k = i%3 + i//3 + (i+1)//3
					elif j == 1:
						k = i//2
					
					#Show card by this index
					if type(deskarray[j-1][k]) == Card:
						deskarray[j-1][k].set_hidden(False)

	return deskarray
