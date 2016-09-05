# Usage
# python problem4.py --u 230

# import the necessary packages
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--u", type = int, required = True,
	help = "Value of U between 0 and 255")
args = vars(ap.parse_args())

#-------------------------------------------------------------
#Defining some functions for later use


#calculates the counter clockwise angle between two points
def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return (ang1 - ang2) % (2 * np.pi)

#-------------------------------------------------------------
#Loading the parameter u
u = args["u"]

#assure the parameter is within bounds
if u > 255:
	u = 255
elif u < 0:
	u = 0

#Pre allocate some memory
img = np.zeros((101,101,3))
pi = np.pi
img2 = np.zeros((101,101))


#For each pixel in our image
for i in range(0,101):
	for j in range(0,101):

		#Finding the HSI values based on definition
		#All the values here will be normalized to make calculations easier in the future
		#Including the RGB

		#Find the hue as the angle between the point and predefined value
		#note that the (0,0) has been moved to the center of the image
		hue = angle_between([i-50,(j-50)*-1], [0,-1])

		#Find the normalized saturation as the norm of the point till the center
		#note that the (0,0) has been moved to the center of the image
		saturation = np.linalg.norm([i-50,(j-50)*-1])/50

		#Fill the saturation image after denormalizing
		img2[i,j] = 255*saturation

		#The normalized intensity according to the definition
		intensity = u/255

		#Pre allocate RGB values
		r=0
		g=0
		b=0

		#If the intesity is out of bounds bound it back
		if intensity > 1:
			intensity = 1
		#If this is not a color but a grayscale
		if saturation == 0:
			r=g=b=u
		#if the saturation is out of bounds
		elif saturation > 1:
			#make it the default RGB (0,0,0)
			r=g=b=0
			#Bound the saturation back
			saturation=1
			#Apply mask to saturation image
			img2[i,j] = 0
		#If the point represents a color
		else:
			#All the credits for these formulas:
			#http://fourier.eng.hmc.edu/e161/lectures/ColorProcessing/node3.html


			#If it is within the first 120 degrees
			if hue < 2*pi/3:
				b = (1-saturation)/3;
				r = (1+(saturation*np.cos(hue)/np.cos(pi/3-hue)))/3
				g = 1-r-b;
			#If it is between 120 and 240
			elif hue < 4*pi/3:
				hue = hue - (2*pi)/3;
				r = (1-saturation)/3
				g = (1+(saturation*np.cos(hue)/np.cos(pi/3-hue)))/3
				b = 1-r-g
			#If it is between 240 and 360
			else:
				hue = hue - (4*pi)/3;
				g = (1-saturation)/3
				b = (1+(saturation*np.cos(hue)/np.cos(pi/3-hue)))/3
				r = 1-b-g

			#Denormalizze the RGB
			r = 3*intensity*r*255
			g = 3*intensity*g*255
			b = 3*intensity*b*255

			#If anything goes out of bounds clip it back
			if r > 255:
				r=255
			if g > 255:
				g=255
			if b > 255:
				b=255
		#Fill the canvas with opencv BGR pattern
		img[i,j] = (b,g,r)

#Show both images after converting the datatypes to conform with opencv standards
cv2.imshow('HSI circle',img.astype(np.uint8))
cv2.imshow('Saturation',img2.astype(np.uint8))

#wait for input
cv2.waitKey(0)

#destroy all windows
cv2.destroyAllWindows()

