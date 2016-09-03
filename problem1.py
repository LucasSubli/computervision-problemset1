# USAGE
# python skindetector.py
# python skindetector.py --video video/skin_example.mov

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

# load the image
img = cv2.imread(args["image"])

orig = img.copy()

cv2.imshow("Problem 1", img)

cv2.waitKey(0)


#-------------------------------------------------------------

h = np.zeros((300,256,3))

bins = np.arange(256).reshape(256,1)
color = [ (255,0,0),(0,255,0),(0,0,255) ]

for ch, col in enumerate(color):
    hist_item = cv2.calcHist([img],[ch],None,[256],[0,255])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    pts = np.column_stack((bins,hist))
    cv2.polylines(h,[pts],False,col)

h=np.flipud(h)

cv2.imshow('Histogram - Blue',h[:,:,0])

cv2.imshow('Histogram - Green',h[:,:,1])

cv2.imshow('Histogram - Red',h[:,:,2])

cv2.imshow('Histogram - All',h)

cv2.waitKey(0)


cv2.destroyAllWindows()

#-------------------------------------------------------------


squareWindow = np.zeros((11,11,3))
aux = np.zeros((140,500,3), np.uint8)

font = cv2.FONT_HERSHEY_SIMPLEX

# mouse callback function
def on_mouse_move(event,x,y,flags,param):
	if event == cv2.EVENT_MOUSEMOVE:
		squareWindow = img[(y-5):(y+5), (x-5):(x+5)]		
		aux = np.zeros((140,500,3), np.uint8)
		
		aux[5:15, 5:15] = img[(y-5):(y+5), (x-5):(x+5)]
		cv2.putText(aux,' <--- 11x11 window:',(10,13), font, 0.5,(255,255,255),1)
		cv2.putText(aux,'The current pointer position is:',(0,35), font, 0.5,(255,255,255),1)
		cv2.putText(aux,'( ' + str(x) + ' , ' + str(y) + ')',(0,55), font, 0.5,(255,255,255),1)
		cv2.putText(aux,'RGB = ' + str(np.flipud(img[y][x])),(0,75), font, 0.5,(255,255,255),1)
		cv2.putText(aux,'Intensity = ' + str(np.average(img[y][x])),(0,95), font, 0.5,(255,255,255),1)
		mean, stdDev = cv2.meanStdDev(squareWindow)
		mean = [m[0] for m in mean]
		stdDev = [s[0] for s in stdDev]
		cv2.putText(aux,'Window Mean = ' + str(np.flipud(np.around(mean,2))),(0,115), font, 0.5,(255,255,255),1)
		cv2.putText(aux,'Window StdDvt = ' + str(np.flipud(np.around(stdDev,2))),(0,135), font, 0.5,(255,255,255),1)

		cv2.imshow('Stats',aux)

cv2.namedWindow('Image')
cv2.setMouseCallback('Image',on_mouse_move)

cv2.imshow('Stats',aux)
cv2.imshow('Stats', squareWindow)


while(1):
	cv2.imshow('Image',img)
	k = cv2.waitKey(0)
	if k:
		break

cv2.destroyAllWindows()

