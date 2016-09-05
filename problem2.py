# USAGE
# python problem2.py
# python problem2.py --video images/SampleVideo.mov

# import the necessary packages
from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required = True,
	help = "path to the (optional) video file")
args = vars(ap.parse_args())

video = cv2.VideoCapture(args["video"])


length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

d1 = np.zeros((length + 1, 3))
d2 = np.zeros((length + 1, 3))
d3 = np.zeros((length + 1, 3))

frameCount = 0;
# keep looping over the frames in the video
while True:
	# grab the current frame
	(grabbed, frame) = video.read()

	#get the aproximate frame duration in ms
	framePeriod = int(1000 * 1.0/video.get(cv2.CAP_PROP_FPS));

	# if we are viewing a video and we did not grab a
	# frame, then we have reached the end of the video
	if args.get("video") and not grabbed:
		break


	#get the mean and std deviation in one scan
	mean, stdDev = cv2.meanStdDev(frame)

	#d1[frameCount] = mean
	#d2[frameCount] = stdDev

	#Get the average color of the image
	median_color_per_row = np.median(frame, axis=0)
	median_color = np.median(median_color_per_row, axis=0)
	
	d1[frameCount, :] = [m[0] for m in mean]
	d2[frameCount, :] = [s[0] for s in stdDev]
	d3[frameCount, :] = median_color

	# show the skin in the image along with the mask
	cv2.imshow("images", frame)


	frameCount = frameCount + 1
	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(framePeriod) & 0xFF == ord("q"):
		break


#Get the mean and std dev of all the metrics
std1 = np.std(d1)
std2 = np.std(d2)
std3 = np.std(d3)

mean1 = np.mean(d1)
mean2 = np.mean(d2)
mean3 = np.mean(d3)


#Normalize them by using the slides formula
alpha1 = (std2/std1*mean1) - mean2
beta1 = std1/std2

alpha2 = (std3/std1*mean1) - mean3
beta2 = std1/std3

newD2 = np.multiply(beta1, d2+alpha1)
newD3 = np.multiply(beta2, d3+alpha2)

#print the results
print("D1 mean: " + str(mean1) + " std: " + str(std1))
print("D2 mean: " + str(mean2) + " std: " + str(std2))
print("D3 mean: " + str(mean3) + " std: " + str(std3))
print("D2* mean: " + str(np.mean(newD2)) + " std: " + str(np.std(newD2)))
print("D3* mean: " + str(np.mean(newD3)) + " std: " + str(np.std(newD3)))

#preallocate some memory
aux1 = np.zeros((frameCount, 3))
aux2 = np.zeros((frameCount, 3))


#for each time
for i in range(0, frameCount):
	aux1[i, :] = d1[i] - d2[i]
	aux2[i, :] = d1[i] - d3[i]

#Compare the functions using the L1 metric
distance1 = 1/frameCount*(np.sum(aux1))
distance2 = 1/frameCount*(np.sum(aux2))

print("L1-metric D1 and D2*: " + str(distance1))
print("L1-metric D1 and D3*: " + str(distance2))

# cleanup the video and close any open windows
video.release()
cv2.destroyAllWindows()