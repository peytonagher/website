import cards
import random
random.seed(100)

MENU = '''     
Input options:
    MTT s d: Move card from end of Tableau column s to end of column d.
    MTC s d: Move card from end of Tableau column s to Cells d.
    MCT s d: Move card from Cells s to end of Tableau column d.
    MTF s d: Move card from end of Tableau column s to Foundation d.
    MCF s d: Move card from end of Cell s to Foundation d.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game       \n'''


    '''Creates and initializes the tableau, foundation, and cells
    returning them as a tuple'''

def initialize():
    foundation = [[],[],[],[]]
    tableau = [[],[],[],[],[],[],[],[],[],[]]
    cells = []
    deck = cards.Deck()
    deck.shuffle() # shuffles the deck each time the game is initalized
    for element in range(5):
        for i in range(10):
            card = deck.deal()
            tableau[i].append(card)
    for i in range(4):
        if i == 0:
            cells.append(None)
        else:
            card = deck.deal()
            cells.append(card)
    return (tableau, foundation, cells)


    '''Display the cell and foundation at the top.
    Display the tableau below.'''

def display(tableau, foundation, cells):
    print("\n{:<11s}{:^16s}{:>10s}".format( "foundation","cell", "foundation"))
    print("{:>14s}{:>4s}{:>4s}{:>4s}".format( "1","2","3","4"))
    for i,f in enumerate(foundation):
        if f and (i == 0 or i == 1):
            print(f[-1],end=' ')  # Print first card in stack(list)
        elif i == 0 or i == 1:    # on foundation.
            print("{:4s}".format( " "),end='') # Fill space where card would be 
    print("{:3s}".format(' '),end='')          # so foundation gets printed in 
    for c in cells:                            # the right place.
        if c:
            print(c,end=' ')  # Print first card in stack(list) on foundation.
        else:
            print("[  ]",end='') # Fill space where card would be so foundation 
    print("{:3s}".format(' '),end='') # gets printed in the right place.
    for i,f in enumerate(foundation):
        if f and (i == 2 or i == 3):
            print(f[-1],end=' ')  # Print first card in stack(list) on 
        elif i == 2 or i == 3:    # foundation.
            print("{}{}".format( " ", " "),end='') # Fill space where card would
    print()                                        # be so foundation gets 
    print("\ntableau")                             # printed in the right place.
    print("   ",end=' ')
    for i in range(1,11):
        print("{:>2d} ".format(i),end=' ')
    print()
    # determine the number of rows in the longest column        
    max_col = max([len(i) for i in tableau])
    for row in range(max_col):
        print("{:>2d}".format(row+1),end=' ')
        for col in range(10):
            # check that a card exists before trying to print it
            if row < len(tableau[col]):
                print(tableau[col][row],end=' ')
            else:
                print("   ",end=' ')
        print()  # carriage return at the end of each row
    print()  # carriage return after printing the whole tableau


    '''Determines if the player can move a card within their tableau'''

def validate_move_within_tableau(tableau,source_index,destination_index):
    if len(tableau[destination_index]) == 0:
        if tableau[source_index][-1].rank() == 13: # 13 cards per suit
            return True
        else:
            return False
    else:
        if len(tableau[source_index]) > 0:
            if (tableau[source_index][-1].rank()) == \
                (tableau[destination_index][-1].rank() - 1):
                if (tableau[source_index][-1].suit()) == \
                    (tableau[destination_index][-1].suit()):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


    '''Determines if the player can move a card from a cell to the tableau'''

def validate_move_cell_to_tableau(tableau,cells,cell_no,destination_index):
    if (cells[cell_no]) == None:
        return False
    if len(tableau[destination_index]) == 0:
        if (cells[cell_no].rank()) == 13: # checks to see if card is a king
            return True
        else:
            return False
    else:
        if (cells[cell_no].rank()) == (tableau[destination_index][-1].rank()\
            - 1):
            if (cells[cell_no].suit()) == (tableau[destination_index]\
                [-1].suit()):
                return True
            else:
                return False
        else:
            return False


    '''Determines if the player can move a card from the tableau to a cell'''

def validate_move_tableau_to_cell(tableau,cells,source_index,cell_no):
    if not len(tableau[source_index]) == 0:
        if ((source_index < 10) and (source_index > -10)) or \
            ((cell_no < 4) and (cell_no > 0)):
            if cells[cell_no] == None: # makes sure that there isnt a card
                return True            # in the cell already
            else:
                return False
        else:
            return False
    else:
        return False


    '''Determines if the player can move a card from the tableau to one of
    the foundation piles'''

def validate_move_tableau_to_foundation(tableau,foundation,source_index,found_no):
    if ((source_index < 10) and (source_index > 0)) or \
        ((found_no < 10) and (found_no > 0)):
        if len(foundation[found_no]) == 0:
            if len(tableau[source_index]) != 0:
                if tableau[source_index][-1].rank() == 1: # Place Ace first
                    return True
                else:
                    return False
            else:
                return False
        else:
            if (tableau[source_index][-1].rank()) == \
                (foundation[found_no][-1].rank() + 1):
                if (foundation[found_no][-1].suit()) == \
                    (tableau[source_index][-1].suit()):
                    return True  # above code compares ranks and suits of both
                else:            # cards
                    return False
            else:
                return False
    else:
        return False


    '''Determines if the player can move a card from a cell to one of the 
    foundation piles'''

def validate_move_cell_to_foundation(cells,foundation,cell_no,found_no):
    if ((cell_no < 5) and (cell_no > 0)) or ((found_no < 10) and \
        (found_no > 0)):
        if cells[cell_no] != None:
            if len(foundation[found_no]) == 0:
                if cells[cell_no].rank() == 1: # Place Ace first
                    return True
                else:
                    return False
            else:
                if (cells[cell_no].rank()) == (foundation[found_no][-1].rank()\
                    + 1):
                    if (cells[cell_no].suit()) == \
                        (foundation[found_no][-1].suit()):
                        return True # above code compares ranks and suits of
                    else:           # both cards
                        return False
                else:
                    return False
        else:
            return False
    else:
        return False


    '''Moves a card from one tableau column to another tableau column'''

def move_within_tableau(tableau,source_index,destination_index):
    if validate_move_within_tableau(tableau,source_index,destination_index)\
        == True:
        card = tableau[source_index].pop(-1) # pops the bottom card
        tableau[destination_index].append(card)
        return True
    else:
        return False


    '''Moves a card from one tableau column to a cell'''

def move_tableau_to_cell(tableau,cells,source_index,cell_no):
    if validate_move_tableau_to_cell(tableau,cells,source_index,cell_no)\
        == True:
        card = tableau[source_index].pop(-1) # pops the bottom card
        cells[cell_no] = card # puts card in the specific cell
        return True
    else:
        return False


    '''Moves a card from one cell to a tableau column'''

def move_cell_to_tableau(tableau,cells,cell_no,destination_index):
    if validate_move_cell_to_tableau(tableau,cells,cell_no,destination_index)\
        == True:
        card = cells[cell_no] # takes card from cell
        cells[cell_no] = None # replaces cell with None value
        tableau[destination_index].append(card)
        return True
    else:
        return False


    '''Moves a card from one tableau column to one of the foundation
    piles'''

def move_tableau_to_foundation(tableau,foundation,source_index,found_no):
    if validate_move_tableau_to_foundation(tableau,foundation,source_index,\
        found_no) == True:
        card = tableau[source_index].pop(-1) # pops the bottom card
        foundation[found_no].append(card)
        return True
    else:
        return False


    '''Moves a card from one cell to one of the foundation piles'''

def move_cell_to_foundation(cells,foundation,cell_no,found_no):
    if validate_move_cell_to_foundation(cells,foundation,cell_no,found_no)\
        == True:
        card = cells[cell_no] # card is pulled from the specific cell
        cells[cell_no] = None # replaces the specific cell with a None value
        foundation[found_no].append(card)
        return True
    else:
        return False


    '''Checks the foundation piles to see if all four foundations total to 52'''

def check_for_win(foundation):
    result = False
    for fnd in foundation:
        if len(fnd) == 13: # each foundation has to total 13, 52/4 suits = 13
            result = True
        elif len(fnd) != 13:
            return False
            break
    return result


    '''Prompt the user for an option and check that the input has the 
    form requested in the menu, printing an error message, if not.
    Return:
    MTT s d: Move card from end of Tableau column s to end of column d.
    MTC s d: Move card from end of Tableau column s to Cells d.
    MCT s d: Move card from Cells s to end of Tableau column d.
    MTF s d: Move card from end of Tableau column s to Foundation d.
    MCF s d: Move card from Cells s to Foundation d.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game        
    '''

def get_option():
    option = input( "\nInput an option (MTT,MTC,MCT,MTF,MCF,R,H,Q): " )
    option_list = option.strip().split()
    opt_char = option_list[0][0].upper()
    if opt_char in 'RHQ' and len(option_list) == 1:  # correct format
        return [opt_char]
    if opt_char == 'M' and len(option_list) == 3 and option_list[1].isdigit() \
        and option_list[2].isdigit():
        opt_str = option_list[0]
        if opt_str in ['MTT','MTC','MCT','MTF','MCF']:
            return [opt_str,int(option_list[1]),int(option_list[2])]
    print("Error in option:", option)
    return None   # none of the above


def main():
    print("\nWelcome to Seahaven Solitaire.\n")
    tableau, foundation, cells = initialize()
    display(tableau, foundation, cells)
    print(MENU)
    option = get_option()   # calls option function to get the specific move
    while option[0].isalpha():
        if option[0] == "MTT":
            source_index = option[1] - 1
            destination_index = option[2] - 1
            if move_within_tableau(tableau,source_index,destination_index)\
                == True:
                if check_for_win(foundation) == True:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -") 
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    option = get_option()
                else:                  # above code starts new initialized game
                    display(tableau, foundation, cells)
                    option = get_option()
                    continue
            else:
                print("Error in move: {} , {} , {}".format(option[0],\
                    str(option[1]),str(option[2])))
                option = get_option()
                continue
        if option[0] == "MTC":
            source_index = option[1] - 1
            cell_no = option[2] - 1
            if move_tableau_to_cell(tableau,cells,source_index,cell_no) == True:
                if check_for_win(foundation) == True:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    option = get_option()
                else:
                    display(tableau, foundation, cells)
                    option = get_option()
                    continue
            else:
                
                print("Error in move: {} , {} , {}".format(option[0],\
                    str(option[1]),str(option[2])))
                option = get_option()
                continue
        if option[0] == "MCT":
            cell_no = option[1] - 1
            destination_index = option[2] - 1
            if move_cell_to_tableau(tableau,cells,cell_no,destination_index)\
                == True:
                if check_for_win(foundation) == True:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    display(tableau, foundation, cells)
                    print(MENU)
                    option = get_option()
                else:
                    display(tableau, foundation, cells)
                    option = get_option()
                    continue
            else:
                
                print("Error in move: {} , {} , {}".format(option[0],\
                    str(option[1]),str(option[2])))
                option = get_option()
                continue
        if option[0] == "MTF":
            source_index = option[1] - 1
            found_no = option[2] - 1
            if move_tableau_to_foundation(tableau,foundation,source_index,\
                found_no) == True:
                if check_for_win(foundation) == True:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    option = get_option()
                else:
                    display(tableau, foundation, cells)
                    option = get_option()
                    continue
            else:
                
                print("Error in move: {} , {} , {}".format(option[0],\
                    str(option[1]),str(option[2])))
                option = get_option()
                continue
        if option[0] == "MCF":
            cell_no = option[1] - 1
            found_no = option[2] - 1
            if move_cell_to_foundation(cells,foundation,cell_no,found_no)\
                == True:
                if check_for_win(foundation) == True:
                    print("You won!")
                    display(tableau, foundation, cells)
                    print("\n- - - - New Game. - - - -")
                    tableau, foundation, cells = initialize()
                    display(tableau, foundation, cells)
                    print(MENU)
                    option = get_option()
                else:
                    display(tableau, foundation, cells)
                    option = get_option()
                    continue
            else:
                
                print("Error in move: {} , {} , {}".format(option[0],\
                    str(option[1]),str(option[2])))
                option = get_option()
                continue
        if option[0] == "R":  # restarts with a new initialized game
            tableau, foundation, cells = initialize()
            display(tableau, foundation, cells)
            print(MENU)
            option = get_option()
            continue
        if option[0] == "H":  # displays the menu with option prompt
            print(MENU)
            option = get_option()
            continue
        if option[0] == "Q":  # quits/exits the program if Q is entered as input
            print("Thank you for playing.")
            quit()
        else:
            print("Error in option:", option)
            option = get_option()
            continue


if __name__ == '__main__':
    main()