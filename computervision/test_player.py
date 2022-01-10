import math
import os
import sys
import cv2

import numpy as np

from tensorflow.keras.models import load_model
from tensorflow import keras

from GameAI import TTT_Minimax
from computervision.pre_processes import matrix_transformations
from computervision.pre_processes import PreProccesing
from computervision.gameboard import Tic, get_enemy

"""
Detect the coordinates of the sheet, first point is center so hit ignore since we only want the corners.  

"""

MIN_GRID_SIZE = 500
grid = []


def detect_Corners_paper(frame, thresh, add_margin=True):
    pre_Corners = PreProccesing.Detect_Corners(thresh)

    corners = pre_Corners[1:, :2]
    # corners = matrix_transformations.FPT_HELPER_(corners)
    # print(corners)
    # paper = matrix_transformations.FPT_BIRDVIEW(frame, corners)
    paper = frame
    if add_margin:
        paper = paper[10:-10, 10:-10]
    return paper, corners


def detect_SYMBOL(box):
    """detects the symbol in one box of the grid """

    mapper = {0: None, 1: 'X', 2: 'O'}
    box = PreProccesing.Frame_PRE_proccsing(box)
    idx = np.argmax(model.predict(box))
    print("mapper found", idx, "which is symbol :", mapper[idx])
    return mapper[idx]


def get_3X3_GRID(threshold_img):
    """Returns 3 x 3 grid,
     Find grid's center cell, and based on it fetch the other eight cells
    """

    global grid

    middle_center = PreProccesing.return_contourdbox(threshold_img)
    center_x, center_y, width, height = list(middle_center)

    # Useful coordinates
    left = center_x - width
    right = center_x + width
    top = center_y - height
    bottom = center_y + height

    # Middle row

    middle_left = [left, center_y, width, height]
    middle_right = [right, center_y, width, height]

    # Top row

    top_left = [left, top, width, height]
    top_center = [center_x, top, width, height]
    top_right = [right, top, width, height]

    # Bottom row
    bottom_left = [left, bottom, width, height]
    bottom_center = [center_x, bottom, width, height]
    bottom_right = [right, bottom, width, height]

    # Grid's coordinates
    # print(height,"height")
    # print(width,"width")
    # print(top_left,"TL")
    # print((bottom_left,'BL'))
    # width_rectangle = (top_right-top_left)
    # height_rectangle =  (bottom_left-top_left)

    if (width * height > MIN_GRID_SIZE):
        grid = [top_left, top_center, top_right,
                middle_left, middle_center, middle_right,
                bottom_left, bottom_center, bottom_right]
        return grid


def getMiddleCoord(cellNr):
    global grid
    # grid = [top_left, top_center, top_right,
    # middle_left, middle_center, middle_right,
    # bottom_left, bottom_center, bottom_right]

    print('grid:', grid)
    grid = scaleGrid()
    print('scaled grid:', grid)

    x = 0
    y = 0
    z = 21.1  # default value
    power = 69  # default value

    if cellNr == 1:
        x = abs(grid[0][0] - grid[2][0]) / 6
        y = abs(grid[0][1] - grid[6][1]) / 6
    elif cellNr == 2:
        x = 3 * (abs(grid[0][0] - grid[2][0]) / 6)
        y = abs(grid[0][1] - grid[6][1]) / 6
    elif cellNr == 3:
        x = 5 * (abs(grid[0][0] - grid[2][0]) / 6)
        y = abs(grid[0][1] - grid[6][1]) / 6
    elif cellNr == 4:
        x = abs(grid[3][0] - grid[5][0]) / 6
        y = 3 * (abs(grid[0][1] - grid[6][1]) / 6)
    elif cellNr == 5:
        x = 3 * (abs(grid[3][0] - grid[5][0]) / 6)
        y = 3 * (abs(grid[0][1] - grid[6][1]) / 6)
    elif cellNr == 6:
        x = 5 * (abs(grid[3][0] - grid[5][0]) / 6)
        y = 3 * (abs(grid[0][1] - grid[6][1]) / 6)
    elif cellNr == 7:
        x = abs((grid[6][0] - grid[8][0]) / 6)
        y = 5 * (abs(grid[0][1] - grid[6][1]) / 6)
    elif cellNr == 8:
        x = 3 * (abs(grid[6][0] - grid[8][0]) / 6)
        y = 5 * (abs(grid[0][1] - grid[6][1]) / 6)
    elif cellNr == 9:
        x = 5 * (abs(grid[6][0] - grid[8][0]) / 6)
        y = 5 * (abs(grid[0][1] - grid[6][1]) / 6)

    middleCoord = (grid[0][0] + x, grid[0][1] + y, z, power)
    return middleCoord


def getCoordsToSketchCross(middleCoord):
    print(middleCoord)
    height_dist = 2  # TODO test which value is best
    width_dist = 2  # TODO test which value is best

    x = middleCoord[0]
    y = middleCoord[1]
    z = middleCoord[2]
    power = middleCoord[3]

    coords = []
    coord0 = (x - width_dist, y + height_dist, z, power)  # top left coord of cross
    coord1 = middleCoord
    coord2 = (x + width_dist, y - height_dist, z, power)  # bottom right coord of cross
    coord3 = (x + width_dist, y - height_dist, z + 3, power)  # position in the air before sketching second line
    coord4 = (x + width_dist, y + height_dist, z, power)  # top right coord of cross
    coord5 = middleCoord
    coord6 = (x - width_dist, y - height_dist, z, power)  # bottom left coord of cross

    coords.append(coord0)
    coords.append(coord1)
    coords.append(coord2)
    coords.append(coord3)
    coords.append(coord4)
    coords.append(coord5)
    coords.append(coord6)

    print(coords)

    return coords


def getCoordsToSketchCircle(middleCoord):
    ray = 2
    nrOfDots = 20
    angle = 360 / nrOfDots

    coords = []

    x = middleCoord[0]
    y = middleCoord[1]
    z = middleCoord[2]
    power = middleCoord[3]

    for i in range(nrOfDots):
        currentAngle = 0 + (i * angle)
        cos = round(math.cos(currentAngle), 2)
        sin = round(math.cos(currentAngle), 2)
        c = (x + cos * ray, y + sin * ray, z, power)
        coords.append(c)

    return coords


def scaleGrid():
    global grid

    longSideBoard = (-21.25, 21.25)  # y
    lengthBoard = 42.5
    shortSideBoard = (10, 40.5)  # x
    widthBoard = 30.5

    longSideCV = (125, 857)
    lengthCV = 732
    shortSideCV = (88, 628)
    widthCV = 540

    z = 21.1  # default value
    power = 69  # default value

    scaledGrid = [[round(longSideBoard[0] + (grid[0][1] / widthCV * lengthBoard), 1),
                   round(shortSideBoard[1] - (grid[0][0] / lengthCV * widthBoard), 1), z, power],
                  [round(longSideBoard[0] + (grid[1][1] / widthCV * lengthBoard), 1),
                   round(shortSideBoard[1] - (grid[1][0] / lengthCV * widthBoard), 1), z, power],
                  [round(longSideBoard[0] + (grid[2][1] / widthCV * lengthBoard), 1),
                   round(shortSideBoard[1] - (grid[2][0] / lengthCV * widthBoard), 1), z, power],
                  [round(longSideBoard[0] + (grid[3][1] / widthCV * lengthBoard), 1),
                   round(shortSideBoard[1] - (grid[3][0] / lengthCV * widthBoard), 1), z, power],
                  [round(longSideBoard[0] + (grid[4][1] / widthCV * lengthBoard), 1),
                   round(shortSideBoard[1] - (grid[4][0] / lengthCV * widthBoard), 1), z, power],
                  [round(longSideBoard[0] + (grid[5][1] / widthCV * lengthBoard), 1),
                   round(shortSideBoard[1] - (grid[5][0] / lengthCV * widthBoard), 1), z, power],
                  [round(longSideBoard[0] + (grid[6][1] / widthCV * lengthBoard), 1),
                   round(shortSideBoard[1] - (grid[6][0] / lengthCV * widthBoard), 1), z, power],
                  [round(longSideBoard[0] + (grid[7][1] / widthCV * lengthBoard), 1),
                   round(shortSideBoard[1] - (grid[7][0] / lengthCV * widthBoard), 1), z, power],
                  [round(longSideBoard[0] + (grid[8][1] / widthCV * lengthBoard), 1),
                   round(shortSideBoard[1] - (grid[8][0] / lengthCV * widthBoard), 1), z, power]
                  ]

    return scaledGrid


def draw_SYMBOL(baseimage, symbol, placement):
    x, y, w, h = placement
    if symbol == 'O':
        centroid = (x + int(w / 2), y + int(h / 2))
        cv2.circle(baseimage, centroid, 20, (0, 0, 0), 6)
    elif symbol == 'X':
        # Draws the 'X' shape
        cv2.line(baseimage, (x + 10, y + 7), (x + w - 10, y + h - 7),
                 (0, 0, 0), 6)
        cv2.line(baseimage, (x + 10, y + h - 7), (x + w - 10, y + 7),
                 (0, 0, 0), 6)
    return baseimage


def preprocesses(frame):
    global grid

    output = []
    # Preprocesses for finding board
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurry_thresh_gray_frame = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                     cv2.THRESH_BINARY_INV, 11, 7)
    cv2.imshow("preprosses input", blurry_thresh_gray_frame)
    blurry_thresh_gray_frame = cv2.GaussianBlur(blurry_thresh_gray_frame, (7, 7), 0)
    paper, corners = detect_Corners_paper(frame, blurry_thresh_gray_frame)
    paper_cut = matrix_transformations.smart_cut(paper)
    output.append(paper_cut)

    # Thresholding to find grid
    paper_gray = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)
    paper_thresh = cv2.adaptiveThreshold(paper_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 6)
    paper_thresh_cut = matrix_transformations.smart_cut(paper_thresh)
    cv2.imshow("threshold", paper_thresh_cut)
    grid = get_3X3_GRID(paper_thresh_cut)
    output.append(grid)
    return output


def play(vcap, difficulty):
    """Play tic tac toe game with computer that uses the alphabeta algorithm"""

    global grid

    # Initialize opponent (computer)
    gameboard = Tic()
    gamehistory = {}
    message = True
    it = 1
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
        # Preprocesses for finding board
        # frame = PreProccesing.Frame_PRE_proccsing(frame,500)
        # frame = matrix_transformations.smart_cut(frame)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # _, blurry_thresh_gray_frame = cv2.threshold(gray_frame, 170, 255, cv2.THRESH_BINARY)
        blurry_thresh_gray_frame = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                         cv2.THRESH_BINARY_INV, 199, 7)
        cv2.imshow("preprosses input", blurry_thresh_gray_frame)
        blurry_thresh_gray_frame = cv2.GaussianBlur(blurry_thresh_gray_frame, (7, 7), 0)
        paper, corners = detect_Corners_paper(frame, blurry_thresh_gray_frame)
        paper_cut = matrix_transformations.smart_cut(paper)

        """
       four red dots  need to appear other which empty array will make the code bug
        """
        # TODO need to find a way to only anisihate when corners is not empty (I think)
        try:
            for c in corners:
                cv2.circle(frame, centre_coordinates=tuple(c), radius=2, color=(0, 0, 255), thickness=2)
        except:
            #     print("sum tyn wun ")
            pass

        # use paper to find grid
        # Thresholding to find grid
        paper_gray = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)
        # paper_thresh = cv2.threshold(  paper_gray, 170, 255, cv2.THRESH_BINARY_INV)
        paper_thresh = cv2.adaptiveThreshold(paper_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 199,
                                             6)
        paper_thresh_cut = matrix_transformations.smart_cut(paper_thresh)
        cv2.imshow("threshold", paper_thresh_cut)
        grid = get_3X3_GRID(paper_thresh_cut)

        try:
            # Draw grid wait on user
            for i, (x, y, w, h) in enumerate(grid):

                # cv2.rectangle(paper, (x, y), (x + w, y + h), (0, 0, 0), 2)
                cv2.rectangle(paper_cut, (x, y), (x + w, y + h), (0, 0, 0), 4)
                if gamehistory.get(i) is not None:
                    shape = gamehistory[i]['shape']
                    paper_cut = draw_SYMBOL(paper_cut, shape, (x, y, w, h))

        except:
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

        # iterate through cells to find player move

        available_moves = np.delete(np.arange(9), list(gamehistory.keys()))
        try:
            for i, (x, y, w, h) in enumerate(grid):
                gameboard.show()
                if i not in available_moves:
                    continue
                # Find what is inside each free cell

                cell = paper_thresh_cut[int(y): int(y + h), int(x): int(x + w)]
                shape = detect_SYMBOL(cell)

                # print(shape)
                if shape is not None:
                    gamehistory[i] = {'shape': shape, 'bbox': (x, y, w, h)}
                    gameboard.make_move(i, shape)
                    # gameboard.make_move(i, player) player overloads with false positives

                    # paper = draw_SYMBOL(paper, shape, (x, y, w, h))
                paper_cut = draw_SYMBOL(paper_cut, shape, (x, y, w, h))
                # it = it +1
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

        # it = it +1

        player = get_enemy(player)
        computer_move = TTT_Minimax.determine(gameboard.squares, player,
                                              difficulty)  # computer move is a number between 1 and 9
        print('computer_move', computer_move)

        middleCoord = getMiddleCoord(computer_move)
        crossCoords = getCoordsToSketchCross(middleCoord)
        circleCoords = getCoordsToSketchCircle(middleCoord)
        print('Cross coordinates:', crossCoords)
        print('circle coordinates:', circleCoords)

        # computer_move = CompTurn(gameboard.squares)
        # print(gameboard.squares)
        # print(computer_move, "CompTurn")
        try:
            gameboard.make_move(computer_move, player)
            gamehistory[computer_move] = {'shape': 'O', 'bbox': grid[computer_move]}
            # paper = draw_SYMBOL(paper, 'O', grid[computer_move])
            paper_cut = draw_SYMBOL(paper_cut, 'O', grid[computer_move])

            print("-----------------------Computer move-----------------------------------------------")
            gameboard.show()
            # print(it)
        except:
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
    text = 'Winner is {}!!'.format(str(winner))
    cv2.putText(frame, text, (350, height - 500),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
    cv2.imshow('finished', frame)
    cv2.waitKey(0) & 0xFF

    # Close windows
    vcap.release()
    cv2.destroyAllWindows()
    return gameboard.winner()


def main():
    # TEST:
    # TODO z should be 21.1, below is for testing purposes
    phi = 69
    # g = [(-21.2, 40.50, 21.1, phi), (0, 40.50, 21.1, phi), (21.2, 40.50, 21.1, phi),
    #     (-21.2, 25.25, 21.1, phi), (0, 25.25, 21.1, phi), (21.2, 25.25, 21.1, phi),
    #     (-21.2, 10.00, 21.1, phi), (0, 10.00, 21.1, phi), (21.2, 10.00, 21.1, phi)]
    # middleCoord = getMiddleCoord(2)
    # crossCoords = getCoordsToSketchCross(middleCoord)
    # # circleCoords = getCoordsToSketchCircle(middleCoord)
    # print('Cross coordinates:', crossCoords)
    # # print('circle coordinates:', circleCoords)
    # sketch cross using the robotic arm

    """Check if everything's okay and start game"""
    # Load model
    global model
    global grid
    os.path
    # assert os.path.exists(args.model), '{} does not exist'
    model = load_model('../data/model2.h5')
    # model = keras.models.load_model('data/model.h5')

    # Initialize webcam feed
    vcap = cv2.VideoCapture(0)
    if not vcap.isOpened():
        raise IOError('could not get feed from cam #{}'.format())

    # Announce winner!
    winner = play(vcap, 100)
    print('Winner is:', winner)

    sys.exit()

    # return crossCoords


if __name__ == '__main__':
    main()
