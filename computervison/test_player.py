

import os
import sys
import cv2

import numpy as np

from tensorflow.keras.models import load_model
from tensorflow import keras

from pre_processes import matrix_transformations
from pre_processes import PreProccesing
from alphabeta import Tic, get_enemy, determine
from Minimax import *

"""
Detect the coords of the sheet, first point is center so hit ignore since we only want the corners.  

also computes birds eye view (if use)
"""


MIN_GRID_SIZE = 8000
def detect_Corners_paper(frame, thresh, add_margin=True):

    pre_Corners = PreProccesing.Detect_Corners(thresh)

    corners = pre_Corners[1:, :2]
    #corners = matrix_transformations.FPT_HELPER_(corners)
   # print(corners)
   #paper = matrix_transformations.FPT_BIRDVIEW(frame, corners)
    paper = frame
    if add_margin:
        paper = paper[10:-10, 10:-10]
    return paper, corners


"""decects the symbol in one box of the grid """
def detect_SYMBOL(box):

    mapper = {0: None, 1: 'X', 2: 'O'}
    box = PreProccesing.Frame_PRE_proccsing(box)
    idx = np.argmax(model.predict(box))
    print("mapper found",idx, "which is symbol :" , mapper[idx])
    return mapper[idx]

    """Returns 3 x 3 grid, 
     Find grid's center cell, and based on it fetch
     the other eight cells
    """
def get_3X3_GRID(threshhold_img):

    middle_center = PreProccesing.return_contourdbox(threshhold_img)
    center_x, center_y, width, height = middle_center


    # Useful coords
    left = center_x - width
    right = center_x + width
    top = center_y - height
    bottom = center_y + height

    # Middle row

    middle_left = (left, center_y, width, height)
    middle_right = (right, center_y, width, height)

    # Top row

    top_left = (left, top, width, height)
    top_center = (center_x, top, width, height)
    top_right = (right, top, width, height)

    # Bottom row
    bottom_left = (left, bottom, width, height)
    bottom_center = (center_x, bottom, width, height)
    bottom_right = (right, bottom, width, height)

    # Grid's coordinates
    #print(height,"height")
    #print(width,"widht")
    #print(top_left,"TL")
    #print((bottom_left,'BL'))
    #width_retangle = (top_right-top_left)
    #height_retangel =  (bottom_left-top_left)
    if (width*height> MIN_GRID_SIZE):

     Grids=[top_left, top_center, top_right,
            middle_left, middle_center, middle_right,
            bottom_left, bottom_center, bottom_right]
     return Grids


def draw_SYMBOL(baseimage, symbol, placement):

    x, y, w, h = placement
    if symbol == 'O':
        centroid = (x + int(w / 2), y + int(h / 2))
        cv2.circle(baseimage, centroid, 10, (0, 0, 0), 2)
    elif symbol == 'X':
        # Draws the 'X' shape
        cv2.line(baseimage, (x + 10, y + 7), (x + w - 10, y + h - 7),
                 (0, 0, 0), 2)
        cv2.line(baseimage, (x + 10, y + h - 7), (x + w - 10, y + 7),
                 (0, 0, 0), 2)
    return baseimage


def play(vcap):
    """Play tic tac toe game with computer that uses the alphabeta algorithm"""
    # Initialize opponent (computer)
    gameboard = Tic()
    gamehistory = {}
    message = True
    it =1
    # Start playing
    while True:
        ret, frame = vcap.read()
        key = cv2.waitKey(1) & 0xFF
        if not ret:
            print('[INFO] finished video processing')
            break

        # kill switch is q
        if key == ord('q'):
            print('[INFO] stopped video processing')
            break

        # Preprocess input

         #frame = PreProccesing.Frame_PRE_proccsing(frame,500)
       # frame = matrix_transformations.smart_cut(frame)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       # _, blurry_thresh_gray_frame = cv2.threshold(gray_frame, 170, 255, cv2.THRESH_BINARY)
        blurry_thresh_gray_frame = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 7 )
        cv2.imshow("preprosses input",blurry_thresh_gray_frame)
        blurry_thresh_gray_frame = cv2.GaussianBlur(blurry_thresh_gray_frame, (7, 7), 0)
        paper, corners = detect_Corners_paper(frame, blurry_thresh_gray_frame)
        paper_cut=matrix_transformations.smart_cut(paper)


        """
       four red dots  need to appear other whiche empty array will make the code bug
       
        """#TODO need to find a way to only anisihate when corners is not empty (ithink)
        try :
         for c in corners:
            cv2.circle(frame, centre_coordinates=tuple(c), radius=2, color=(0, 0, 255),thickness= 2)
        except :
      #     print("sum tyn wun ")
            pass


        # use paper to find grid

        paper_gray = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)
        #paper_thresh = cv2.threshold(  paper_gray, 170, 255, cv2.THRESH_BINARY_INV)
        paper_thresh = cv2.adaptiveThreshold(paper_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 6)
        paper_thresh_cut = matrix_transformations.smart_cut(paper_thresh)
        cv2.imshow("threshold",paper_thresh_cut)
        grid = get_3X3_GRID(paper_thresh_cut)

        try:
        # Draw grid wait on user
         for i, (x, y, w, h) in enumerate(grid):

            #cv2.rectangle(paper, (x, y), (x + w, y + h), (0, 0, 0), 2)
            cv2.rectangle(paper_cut, (x, y), (x + w, y + h), (0, 0, 0), 2)
            if gamehistory.get(i) is not None:
                shape = gamehistory[i]['shape']
                paper_cut = draw_SYMBOL(paper_cut, shape, (x, y, w, h))

        except :
        # print("something wrong in corners list")
         pass

        # Make move
        if message:
            print('Make move, then press spacebar')
            message = False
        if not key == 32:
            cv2.imshow('original', frame)
            cv2.imshow('bird view', paper_cut)
            continue
        player = 'X'

        # itterate through cells to find player move


        available_moves = np.delete(np.arange(9), list(gamehistory.keys()))
        try:
         for i, (x, y, w, h) in enumerate(grid):
            gameboard.show()
            if i not in available_moves:
                continue
            # Find what is inside each free cell

            cell = paper_thresh_cut[int(y): int(y + h), int(x): int(x + w)]
            shape = detect_SYMBOL(cell)

            #print(shape)
            if shape is not None:
                gamehistory[i] = {'shape': shape, 'bbox': (x, y, w, h)}
                gameboard.make_move(i, shape)
                #gameboard.make_move(i, player) player overloads with false positives

                #paper = draw_SYMBOL(paper, shape, (x, y, w, h))
            paper_cut = draw_SYMBOL(paper_cut, shape, (x, y, w, h))
            #it = it +1
            print(it)

        except:
            pass
        # Check whether game has finished
        if gameboard.complete():
            print("--------------------------------game finished ----- current gameboard:----------------------")
            gameboard.show()
            print("break 1")
            break


        # Computer's time to play

        #it = it +1
        # TODO for now alphabeta implentation. switch to minimax
        player = get_enemy(player)
        computer_move = determine(gameboard, player)
        #computer_move = CompTurn(gameboard.squares)
        #print(gameboard.squares)
        #print(computer_move, "CompTurn")
        try :
         gameboard.make_move(computer_move, player)
         gamehistory[computer_move] = {'shape': 'O', 'bbox': grid[computer_move]}
        #paper = draw_SYMBOL(paper, 'O', grid[computer_move])
         paper_cut = draw_SYMBOL(paper_cut, 'O', grid[computer_move])

         print("-----------------------Computer move-----------------------------------------------")
         gameboard.show()
         #print(it)
        except :
         pass
        # Check whether game has finished
        if gameboard.complete():
            print("-------------------------game-finished --------------------------")
            break

        # Show images
        cv2.imshow('original', frame)
        # cv2.imshow('blurry_thresh_gray_frame', paper_thresh)
        cv2.imshow('bird view', paper_cut)
        message = True

    # Show winner
    winner = gameboard.winner()
    height = paper.shape[0]
    text = 'Winner is {}'.format(str(winner))
    cv2.putText(paper, text, (10, height - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.imshow('bird view', paper)
    cv2.waitKey(0) & 0xFF

    # Close windows
    vcap.release()
    cv2.destroyAllWindows()
    return gameboard.winner()


def main():
    """Check if everything's okay and start game"""
    # Load model
    global model
    os.path
    #assert os.path.exists(args.model), '{} does not exist'
    model = load_model('data/model2.h5')
    #model = keras.models.load_model('data/model.h5')

    # Initialize webcam feed
    vcap = cv2.VideoCapture(0)
    if not vcap.isOpened():
        raise IOError('could not get feed from cam #{}'.format())

    # Announce winner!
    winner = play(vcap)
    print('Winner is:', winner)
    sys.exit()


if __name__ == '__main__':
    main()
