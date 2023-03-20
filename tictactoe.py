from os import system
from sys import platform
from copy import deepcopy
from time import sleep
from random import randint

if platform == 'win32': clear_string = 'cls'
if platform in ('darwin', 'linux'): clear_string = 'clear'

char_dict = { # chars are 8 letters tall and 17 letters wide
        '_' : [''.join([' ' for _ in range(17)]) for _ in range(8)],
        'o' : [
        '      ____       ',
        '    /       \    ',
        '   /    _    \   ',
        '   |   | |   |   ',
        '   |   |_|   |   ',
        '   \         /   ',
        '    \_______/    ',
        '                 '],
        'x' : [
        '     _      _    ',
        '    |  \  /  |   ',
        '    \   \/   /   ',
        '     \      /    ',
        '     /      \    ',
        '    /   /\   \   ',
        '    |__/  \___|  ',
        '                 ']}

class Board:
    def __init__(self,width=3,height=3,state=None):
        self.width=width
        self.height=height
        if state is None: self.state=[['_' for _ in range(self.width)] for _ in range(self.height)] # the three states are '_' for empty, 'x' for and x, and 'o' for an o
        else: self.state=state
        
    def __repr__(self):
        return_string = ''
        for char_row_index in range((self.height * 8)-1): #char_row_index // 8 is the row index
            for column_index in range(self.width):
                return_string += char_dict[self.state[char_row_index // 8][column_index]][char_row_index % 8]
                if column_index == self.width-1: return_string += '\n'
                else: return_string += '|'
            if (char_row_index+1) % 8 == 0: return_string += ''.join([''.join(['-' for _ in range(17)]) + '+' for i in range(self.width-1)]) + ''.join(['-' for _ in range(17)]) + '\n'
        return return_string
    
    def whos_move(self):
        total = 0
        for row in self.state:
            for item in row:
                if item == '_': total += 1
        if total % 2 == 0: return -1
        return 1

    def iswin(self, value):
        wins = [self.state[0],
        self.state[1],
        self.state[2],
        [self.state[0][1],self.state[1][1],self.state[2][1]],
        [self.state[0][0],self.state[1][0],self.state[2][0]],
        [self.state[0][2],self.state[1][2],self.state[2][2]],
        [self.state[0][0],self.state[1][1],self.state[2][2]],
        [self.state[0][2],self.state[1][1],self.state[2][0]]]
        for win in wins: # this is the stupid way
            if [value, value, value] == win:
                return True
        return False

    def update(self,position, value): # returns if the given move wins continues the game, or is illegal
        current_value = self.state[position // self.width][position % self.width]
        if current_value == '_':
            self.state[position // self.width][position % self.width] = value
            if self.iswin(value): return 'win'
            return 'continue'
        return 'illegal'        
    
    def best_move(self): # returns the position it thinks is best to play
        move_map={1:'x', -1:'o'}

        class Node:
            def __init__(self,data, depth = 0,parent = None, children = None, move_from_parent=None):
                self.data = data #board state
                self.eval = None #board eval
                self.depth = depth
                self.parent = parent
                self.move_from_parent = move_from_parent # the move taken to arrive at the node from it's parent    
                if children is None: self.children = []
                else: self.children = children
    
        class Tree:
            def __init__(self, root, whosmoveroot):
                self.root = root
                self.whosmoveroot = whosmoveroot

            def make(self):
                def help(node):
                    for i in range(3):
                        for j in range(3):
                            if node.data.state[i][j] == '_':
                                newboard = Board(state=deepcopy(node.data.state))
                                newboard.state[i][j] = move_map[self.whosmoveroot * (1 - 2*(node.depth % 2))] 
                                newnode = Node(data=newboard, depth = node.depth+1, parent = node)
                                newnode.move_from_parent = (newnode.data.width * i)+j+1
                                node.children.append(newnode)

                                if newboard.iswin(move_map[self.whosmoveroot * (2*(newnode.depth % 2)-1)]): 
                                    newnode.eval = float('inf') * self.whosmoveroot * (1 - 2*(node.depth % 2))

                                else:
                                    draw = True
                                    for row in newboard.state:
                                        if '_' in row:
                                            draw = False
                                            break

                                    if draw: newnode.eval = 0
                                    else: help(newnode)

                help(self.root)

            def score(self):
                def help(node):
                    if node.eval is not None: return node.eval

                    if self.whosmoveroot*(2*(node.depth % 2)-1) == 1:
                        minscore = float('inf')
                        for child in node.children:
                            node.eval = help(child)
                            if node.eval < minscore:
                                minscore = node.eval
                        node.eval = minscore
                        return minscore
                
                    else:
                        maxscore = -float('inf')
                        for child in node.children:
                            node.eval = help(child)
                            if node.eval > maxscore:
                                maxscore = node.eval
                        node.eval = maxscore
                        return maxscore

                return help(self.root)

            def best(self):
                if self.whosmoveroot == 1:
                    best_moves = []
                    maxscore = -float('inf')
                    for child in self.root.children:
                        if child.eval > maxscore: 
                            maxscore = child.eval
                            best_moves = [child.move_from_parent]
                        elif child.eval == maxscore:
                            best_moves.append(child.move_from_parent)

                    print(best_moves, maxscore)
                    return best_moves[randint(0,len(best_moves)-1)]
                
                elif self.whosmoveroot == -1:
                    minscore = float('inf')
                    best_moves = []
                    for child in self.root.children:
                        if child.eval < minscore: 
                            minscore = child.eval
                            best_moves = [child.move_from_parent]
                        elif child.eval == minscore:
                            best_moves.append(child.move_from_parent)

                    print(best_moves, minscore)
                    return best_moves[randint(0,len(best_moves)-1)]

        board = Board(state = self.state)
        return_tree = Tree(root=Node(data=board), whosmoveroot = board.whos_move())

        return_tree.make()
        return_tree.score()
        return_val = return_tree.best()
        return return_val

def player_input(input_type, accepted, return_string):
    given = input()
    while True:
        try:
            if str(given) in ('Quit','quit','q','Q'):
                print('Game Quit.')
                break
            if input_type(given) in accepted:
                given = input_type(given)
                return given     
            else:
                given = input_type(given)
                print(return_string)
                given = input()
        except:
            if input_type == int: print('Not an integer! Please try again.')
            if input_type == str: print('Not an string! Please try again.')
            given = input()

def player_text_input(forbidden_string_lst = None): # takes users text input and returns it as long as it is not in a list of forbidden strings
    if forbidden_string_lst is None: forbidden_string_lst = []
    given = input()
    while True:
        if str(given) in ('Quit','quit','q','Q'):
                print('Game Quit.')
                break
        if given in forbidden_string_lst:
            print('You can\'t use that name! Choose another.')
            given = input()
        if len(given) > 50:
            print('The entered name is too long. Try entering a name less than 50 characters.')
            given = input()
        if len(given) == 0:
            print('The entered name is too short. Try entering a name that is atleast 1 character long.')
            given = input()
        if len(given) > 0 and len(given) <= 50 and given not in ('Quit','quit','q','Q') and given not in forbidden_string_lst:
            return given

class Player:
    def __init__(self, name, alias, computer=False):
        self.name = name
        self.alias = alias
        self.computer = computer #boolean if whether or not the player is the computer

class Game:
    def __init__(self, player1, player2):
        self.board=Board()
        self.player1 = player1 
        self.player2 = player2
        self.current_player = self.player1
        self.move_map={1:'x', 2:'o'}
        self.moves = 0

    def start(self):    
        print(self.board)
        result = 'continue'
        move_guide='1 2 3\n4 5 6\n7 8 9\n'

        while True: #gameloop
            if not self.current_player.computer:
                print('{}\'s turn'.format(self.current_player.name))
                print(move_guide)
                while True:
                    chosen_position = player_input(int, (1,2,3,4,5,6,7,8,9), 'Please enter integer 1 - 9.')
                    if chosen_position is None: return [0,0] # if user quits out here, they do not want to play again.
                    else:
                        result = self.board.update(position=chosen_position-1, value=self.move_map[self.current_player.alias])
                        if result != 'illegal': break
                        print('That position is filled. Choose another location.')
                        
            if self.current_player.computer: 
                print('Computer\'s turn')
                print(move_guide)
                quick_move=True
                for row in self.board.state:
                    if row != ['_','_','_']:
                        chosen_position = self.board.best_move() #give the computer what turn it is
                        quick_move=False
                        break
                if quick_move: 
                    chosen_position = randint(0,9) # any move is playable
                    sleep(0.8)
                
                print('Computer chooses:', chosen_position)
                result = self.board.update(position=chosen_position-1, value=self.move_map[self.current_player.alias])

            self.moves += 1
            system(clear_string)
            print(self.board)
            if result == 'win' or self.moves == 9:
                system(clear_string)
                print(self.board)
                if result == 'win':
                    print('{} wins!\n'.format(self.current_player.name))
                elif self.moves == 9:
                    print('It\'s a draw!\n')
                return_lst = [0,0]
                if result == 'win': return_lst[self.current_player.alias-1] = 2
                elif self.moves == 9: return_lst = [1,1]
                return return_lst

            if self.current_player.alias == 1: self.current_player = self.player2
            elif self.current_player.alias == 2: self.current_player = self.player1


class Session:
    def __init__(self):
        self.rivalries_dict = {}

    def start(self):
        system(clear_string)
        print('-----Welcome to Tic-Tac-Toe-----\n')
        sleep(0.5)
        
        play_again=True
        while play_again:
            
            print('Enter player names. Enter \'Computer\' for either Player 1 or Player 2 to play the computer.\n')

            sleep(0.5)

            print('What would you like Player 1\'s name to be?')
            name_1 = player_text_input()
            if name_1 is None: return False # if user quits out here, they do not want to play again.
            elif name_1 == 'Computer': self.player1 = Player(name='Computer', alias=1, computer=True)
            else: self.player1 = Player(name=name_1, alias = 1)

            print('What would you like Player 2\'s name to be?')
            name_2 = player_text_input([self.player1.name])
            if name_2 is None: return False # if user quits out here, they do not want to play again.
            elif name_2 == 'Computer': self.player2 = Player(name='Computer', alias=2, computer=True)
            else: self.player2 = Player(name=name_2, alias = 2)

            try:
                self.rivalries_dict[(name_1.lower(), name_2.lower())][0]
                self.rivalries_dict[(name_2.lower(), name_1.lower())][0]
            except KeyError:
                self.rivalries_dict[(name_1.lower(), name_2.lower())] = [0,0]
                self.rivalries_dict[(name_2.lower(), name_1.lower())] = [0,0]
            system(clear_string)

            print('Enter \'Quit\' at anytime to exit the game.\n')
            system(clear_string)
            game_result = Game(player1 = self.player1, player2 = self.player2).start()

            self.rivalries_dict[(name_1.lower(), name_2.lower())][0] += game_result[0]
            self.rivalries_dict[(name_1.lower(), name_2.lower())][1] += game_result[1]

            name1score = self.rivalries_dict[(name_1.lower(), name_2.lower())][0] + self.rivalries_dict[(name_2.lower(), name_1.lower())][1]
            name2score = self.rivalries_dict[(name_2.lower(), name_1.lower())][0] + self.rivalries_dict[(name_1.lower(), name_2.lower())][1]
            if name1score == 1: s1 = ''
            else: s1 = 's'
            if name2score == 1: s2 = ''
            else: s2 = 's'
            if name1score + name2score != 0: print('The running total is {} point{} for {} and {} point{} for {}.\n'.format(name1score,s1,name_1,name2score,s2,name_2))

            print('Would you like to play again?')
            play_again = player_input(str, ('yes', 'Yes', 'y', 'no', 'No', 'n'), 'Please enter \'Yes\' or \'No\'')
            if play_again in ('no', 'No', 'n') or play_again is None: play_again = False
            if play_again in ('yes', 'Yes', 'y'): play_again = True

if __name__ == '__main__': Session().start()
