# USAGE
# python problem1.py
# python problem1.py --image image/1.jpg

# import the necessary packages
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())



#-------------------------------------------------------------
#Loading a color (RGB) image
img = cv2.imread(args["image"])

#Disply it
cv2.imshow("Problem 1", img)

#Wait for key press
cv2.waitKey(0)


#-------------------------------------------------------------
#Display the histograms of all three color channels

#Pre alocate memory
h = np.zeros((300,256,3))
bins = np.arange(256).reshape(256,1)
color = [ (255,0,0),(0,255,0),(0,0,255) ]


#for each  color channel
for ch, col in enumerate(color):
	#get the histogram
	hist_item = cv2.calcHist([img],[ch],None,[256],[0,255])
	#normalize it
	cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
	#convert to int32
	hist=np.int32(np.around(hist_item))
	#stack the matrixes (axis of the graphs+ histogram values)
	pts = np.column_stack((bins,hist))
	#plot the graphs
	cv2.polylines(h,[pts],False,col)


#For some weird reason opencv uses BGR instead of RGB
#Need to take that into account

#Show the blue histogram
#cv2.imshow('Histogram - Blue',h[:,:,0])

#Show the Green histogram
#cv2.imshow('Histogram - Green',h[:,:,1])

#Show the Red histogram
#cv2.imshow('Histogram - Red',h[:,:,2])

#Show all of them combined histogram
cv2.imshow('Histogram - All',h)

#wait for input
cv2.waitKey(0)

#destroy all windows
cv2.destroyAllWindows()

#-------------------------------------------------------------

#pre alocate memory
squareWindow = np.zeros((11,11,3))
aux = np.zeros((140,500,3), np.uint8)

#define font foir some writing
font = cv2.FONT_HERSHEY_SIMPLEX

# mouse callback function
def on_mouse_move(event,x,y,flags,param):
	

	#if we have mouse movement
	if event == cv2.EVENT_MOUSEMOVE:
		#compute the window of interest around the mouse
		squareWindow = img[(y-5):(y+5), (x-5):(x+5)]		
		
		#prepare some kind of canvas to display the data
		#take speciial care to use the uint8 type
		#or else opencv will be unpredictable
		aux = np.zeros((140,500,3), np.uint8)
		
		#place the window of interest on the canvas
		aux[5:15, 5:15] = img[(y-5):(y+5), (x-5):(x+5)]
		#print some explanatory text on the canvas
		cv2.putText(aux,' <--- 11x11 window:',(10,13), font, 0.5,(255,255,255),1)
		cv2.putText(aux,'The current pointer position is:',(0,35), font, 0.5,(255,255,255),1)
		cv2.putText(aux,'( ' + str(x) + ' , ' + str(y) + ')',(0,55), font, 0.5,(255,255,255),1)
		cv2.putText(aux,'RGB = ' + str(np.flipud(img[y][x])),(0,75), font, 0.5,(255,255,255),1)
		cv2.putText(aux,'Intensity = ' + str(np.average(img[y][x])),(0,95), font, 0.5,(255,255,255),1)
		#get the mean and std deviation in one scan
		mean, stdDev = cv2.meanStdDev(squareWindow)
		#Make it nicer to print on the screen
		mean = [m[0] for m in mean]
		stdDev = [s[0] for s in stdDev]
		#print more explanatory text
		cv2.putText(aux,'Window Mean = ' + str(np.flipud(np.around(mean,2))),(0,115), font, 0.5,(255,255,255),1)
		cv2.putText(aux,'Window StdDvt = ' + str(np.flipud(np.around(stdDev,2))),(0,135), font, 0.5,(255,255,255),1)
		#show the canvas
		cv2.imshow('Stats',aux)

#define the main windows
cv2.namedWindow('Image')
#attach it to the mouse event
cv2.setMouseCallback('Image',on_mouse_move)

#open the canvas even if there is no mouse movement
cv2.imshow('Stats',aux)

#keep processing while no input
while(1):
	cv2.imshow('Image',img)
	k = cv2.waitKey(0)
	if k:
		break

#destroy all windows
cv2.destroyAllWindows()

