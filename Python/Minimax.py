#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import random
import platform
import time
from os import system

"""
An implementation of Minimax AI Algorithm in Tic Tac Toe,
using Python.
This software is available under GPL license.
Author: Clederson Cruz
Year: 2017
License: GNU GENERAL PUBLIC LICENSE (GPL)
"""

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    This function tests if a specific player wins. Possibilities:
    * Three rows    [X X X] or [O O O]
    * Three cols    [X X X] or [O O O]
    * Two diagonals [X X X] or [O O O]
    :param state: the state of the current board
    :param player: a human or a computer
    :return: True if the player wins
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    A move is valid if the chosen cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the board[x][y] is empty
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    Print the board on console
    :param state: current state of the board
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice, level):
    """
    It calls the minimax function if the depth < 9,
    else it choices a random coordinate.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]
        # TODO make robot sketch an X (or O) at coordinate x,y

    random_or_not = random.randint(0, 100)
    if random_or_not <= level:
        print('move set by computer ', x, y)
        set_move(x, y, COMP)
    else:
        # play random move, that is valid and not the best move
        possible_coords = empty_cells(board)
        x_rand, y_rand = x, y
        while x_rand == x and y_rand == y and len(possible_coords) > 1:
            x_rand, y_rand = random.choice(possible_coords)[0], random.choice(possible_coords)[1]
        print('random move set by computer ', x_rand, y_rand)
        set_move(x_rand, y_rand, COMP)

    time.sleep(1)


def human_turn(c_choice, h_choice):
    """
    The Human plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    # clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    # TEST
    # if depth == 9:
    #     x = choice([0, 1, 2])
    #     y = choice([0, 1, 2])
    # else:
    #     move = minimax(board, depth, HUMAN)
    #     x, y = move[0], move[1]
    #
    # random_or_not = random.randint(0, 100)
    # level = 40
    # if random_or_not <= level:
    #     set_move(x, y, HUMAN)
    # else:
    #     # play random move, that is valid and not the best move
    #     possible_coords = empty_cells(board)
    #     x_rand, y_rand = x, y
    #     while x_rand == x and y_rand == y and len(possible_coords) > 1:
    #         x_rand, y_rand = random.choice(possible_coords)[0], random.choice(possible_coords)[1]
    #     set_move(x_rand, y_rand, HUMAN)

    while move < 1 or move > 9:
        try:
            # TODO Instead of numpad input, retrieve board's state with camera and return current board

            # move = int(input('Use numpad (1..9): '))
            move = random.randint(1, 9)
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    """
    Main function that calls all functions
    """
    global board
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first
    level = -1

    # for test
    # h_choice = 'X'

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # for test
    # level = 100

    # Choose level of difficulty
    while level > 100 or level < 0:
        try:
            level = int(input('Choose the level of difficulty [0..100]: '))
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # for test
    # first = 'Y'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # TEST
    # count_Hwin = 0
    # count_Rwin = 0
    # count_draw = 0
    # for i in range(20):
    #     print('i:', i, ', current board:', board)

    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice, level)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice, level)

    # Game over message
    if wins(board, HUMAN):
        # clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
        # count_Hwin += 1
    elif wins(board, COMP):
        # clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
        #count_Rwin += 1
    else:
        # clean()
        render(board, c_choice, h_choice)
        print('DRAW!')
        # count_draw += 1

    # board = [
    #     [0, 0, 0],
    #     [0, 0, 0],
    #     [0, 0, 0],
    # ]

    # print('draw:', count_draw)
    # print('human win:', count_Hwin)
    # print('robot win:', count_Rwin)
    exit()


def convertBoard(currentBoard):
    boardConverted = []
    intBoard = []

    for i in range(len(currentBoard)):
        if currentBoard[i] == 'X':
            intBoard.append(HUMAN)
        elif currentBoard[i] == 'O':
            intBoard.append(COMP)
        else:
            intBoard.append(0)

    row1 = [intBoard[0], intBoard[1], intBoard[2]]
    row2 = [intBoard[3], intBoard[4], intBoard[5]]
    row3 = [intBoard[6], intBoard[7], intBoard[8]]
    boardConverted.append(row1)
    boardConverted.append(row2)
    boardConverted.append(row3)

    return boardConverted


def convertPosition(x, y):
    if x == 0 and y == 0:
        computer_move = 0
    elif x == 0 and y == 1:
        computer_move = 1
    elif x == 0 and y == 2:
        computer_move = 2
    elif x == 1 and y == 0:
        computer_move = 3
    elif x == 1 and y == 1:
        computer_move = 4
    elif x == 1 and y == 2:
        computer_move = 5
    elif x == 2 and y == 0:
        computer_move = 6
    elif x == 2 and y == 1:
        computer_move = 7
    elif x == 2 and y == 2:
        computer_move = 8

    return computer_move


def determine(currentBoard, currentPlayer, level):
    """
    currentBoard is an array of strings, for example ['O', None, None, None, 'X', 'X', 'O', None, None]
    currentPlayer is 'O' or 'X'
    level is the level fo difficulty (from 0 to 100)
    """
    # print('level: ', level)
    # print(currentBoard)
    board = convertBoard(currentBoard)
    # print(board)

    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    random_or_not = random.randint(0, 100)
    if random_or_not <= level:
        computer_move = convertPosition(x, y)
        # print('current computer move is ', computer_move)
        return computer_move
    else:
        # play random move, that is valid and not the best move
        possible_coords = empty_cells(board)
        x_rand, y_rand = x, y
        while x_rand == x and y_rand == y and len(possible_coords) > 1:
            x_rand, y_rand = random.choice(possible_coords)[0], random.choice(possible_coords)[1]
        computer_move = convertPosition(x_rand, y_rand)
        print('current computer move is ', computer_move)
        return computer_move


if __name__ == '__main__':
    main()
