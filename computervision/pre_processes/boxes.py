
import cv2
import numpy as np
from GameAI import DotsNBoxes
   #TODO fix loop problem TypeError: 'int' object is not callable  image path
# Read image
im = cv2.imread("image path", cv2.IMREAD_GRAYSCALE)

# Set up the detector with default parameters.
#detector = cv2.SimpleBlobDetector()
# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200

# Filter by Area.1
params.filterByArea = True
params.minArea = 1

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01


detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.

keypoints = detector.detect(im)
print(len(keypoints))
range = len(keypoints)
board=[]
pts = cv2.KeyPoint_convert(keypoints )
width = 0


cols = pts[:,0]
rows = pts[:,1]

 ## lol cant make loops work for some reason
if(rows[0] == rows [1]):
	count=2
	if(rows[1]== rows[2]):
		count = count +1
		if (rows[2] == rows[3]):
			count = count + 1
			if (rows[3] == rows[4]):
				count = count + 1
				if (rows[4] == rows[5]):
					count = count + 1
					if (rows[5] == rows[6]):
						count = count + 1
						if (rows[6] == rows[7]):
							count = count + 1
							if (rows[7] == rows[8]):
								count = count + 1
								if (rows[8] == rows[9]):
									count = count + 1
									if (rows[9] == rows[10]):
										count = count + 1
print(count)
width = float(count)
print(width,"width")
height = range/count
print(height,"height")

def getwidth(width):
	return width
def getheight(height):
	return height

def main():
	while True:

		print("\t\t!! Welcome to the game of Dots and Boxes !!\n\n Be prepared to be crushed by the power of Artificial Intelligence ... !!\n\n\
                Kidding! You totally can beat it!\n\n\n")

		x = input("Press 1 to start the game or press 2 to escape from the inevitable doom!!\n\n")
		if x == "1":

			#Board_Xdim = int(input("\nPlease enter the number of rows for the board: \n")) * 2 + 1
			Board_Xdim = getwidth(count)
			if Board_Xdim < 5:
				print("\nthe number of rows should at least be 2\n")
				exit()

			#Board_Ydim = int(input("\nPlease enter the number of columns for the board: \n")) * 2 + 1
			Board_Ydim = getheight(height)
			if Board_Ydim < 5:
				print("\nthe number of columns should at least be 2\n")
				exit()

			Ply_num = int(input("\nPlease enter the number of plies used by the AI: \n"))

			if Ply_num < 2:
				print("\nThe number of plies should be higher than 1\n")
				exit()

			Match = DotsNBoxes(Board_Xdim, Board_Ydim, Ply_num)
			Match.start()
		else:
			print("\n\nEscape it is!")
			exit()


if __name__ == "__main__":
	main()




