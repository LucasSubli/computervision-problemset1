# USAGE
# python problem4.py

# import the necessary packages
import numpy as np
from matplotlib import pyplot as plt
import cv2


#-------------------------------------------------------------
#Loading two same size images
img1 = cv2.imread('images/400by400n1.png', 0)
img2 = cv2.imread('images/400by400n2.png', 0)

#First channel -> real part. Second channel -> imaginary part 
dft1 = cv2.dft(np.float32(img1),flags = cv2.DFT_COMPLEX_OUTPUT)
dft2 = cv2.dft(np.float32(img2),flags = cv2.DFT_COMPLEX_OUTPUT)

#pre allocate some memory
amp1Phase2 = np.zeros((400,400,2))
amp2Phase1 = np.zeros((400,400,2))
polar1 = np.zeros((400,400,2))
polar2 = np.zeros((400,400,2))


#this is for changing the quadrants (not necessary, just documenting for debug)
#dft_shift = np.fft.fftshift(dft)


# Calculates the magnitute and angle
polar1[:,:,0], polar1[:,:,1] = cv2.cartToPolar(dft1[:,:,0], dft1[:,:,1])
polar2[:,:,0], polar2[:,:,1] = cv2.cartToPolar(dft2[:,:,0], dft1[:,:,1])

#take it back to cartesian coordinates but swap out the phase and amp
amp1Phase2[:,:,0], amp1Phase2[:,:,1] = cv2.polarToCart(polar1[:,:,0], polar2[:,:,1])
amp2Phase1[:,:,0], amp2Phase1[:,:,1] = cv2.polarToCart(polar2[:,:,0], polar1[:,:,1])

#take the image back to the spatial domain
img_back1 = cv2.idft(amp1Phase2)
img_back1 = cv2.magnitude(img_back1[:,:,0],img_back1[:,:,1])

img_back2 = cv2.idft(amp2Phase1)
img_back2 = cv2.magnitude(img_back2[:,:,0],img_back2[:,:,1])


#Plot all of those side by side for better comparison
plt.subplot(221),plt.imshow(img1, cmap = 'gray')
plt.title('Input Image 1'), plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(img2, cmap = 'gray')
plt.title('Input Image 2'), plt.xticks([]), plt.yticks([])
plt.subplot(223),plt.imshow(img_back1, cmap = 'gray')
plt.title('Amp from 1 Phase from 2'), plt.xticks([]), plt.yticks([])
plt.subplot(224),plt.imshow(img_back2, cmap = 'gray')
plt.title('Amp from 2 Phase from 1'), plt.xticks([]), plt.yticks([])
plt.show()




#-------------------------------------------------------------
#Loading a uniform texture / human face
img = cv2.imread('images/texture1.png', 0)

#First channel -> real part. Second channel -> imaginary part 
dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
ampModified = np.zeros((400,400,2))
phaseModified = np.zeros((400,400,2))
polar = np.zeros((400,400,2))


# Calculates the magnitute and angle
polar[:,:,0], polar[:,:,1] = cv2.cartToPolar(dft[:,:,0], dft[:,:,1])

#take it back to cartesian coordinates but transform them before doing it
ampModified[:,:,0], ampModified[:,:,1] = cv2.polarToCart(np.log(polar[:,:,0]), polar[:,:,1])
phaseModified[:,:,0], phaseModified[:,:,1] = cv2.polarToCart(polar[:,:,0], polar[:,:,1]*1.1)

#take the image back to the spatial domain
img_back3 = cv2.idft(ampModified)
img_back3 = cv2.magnitude(img_back3[:,:,0],img_back3[:,:,1])

img_back4 = cv2.idft(phaseModified)
img_back4 = cv2.magnitude(img_back4[:,:,0],img_back4[:,:,1])


#plot side by side
plt.subplot(131),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(img_back3, cmap = 'gray')
plt.title('Amp  modified'), plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(img_back4, cmap = 'gray')
plt.title('Phase modified'), plt.xticks([]), plt.yticks([])
plt.show()
