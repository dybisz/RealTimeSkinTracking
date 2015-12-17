# import the necessary packages
import imutils
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
args = vars(ap.parse_args())

# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([34, 0, 0], dtype="uint8")
upper = np.array([73, 255, 134], dtype="uint8")
# if a video path was not supplied, grab the reference
# to the gray
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, load the video
else:
    camera = cv2.VideoCapture(args["video"])
# keep looping over the frames in the video
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    height, width, channels = frame.shape

    binary = np.zeros((height, width, 3), np.uint8)
    # if we are viewing a video and we did not grab a
    # frame, then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, convert it to the HSV color space,
    # and determine the HSV pixel intensities that fall into
    # the speicifed upper and lower boundaries
    frame = imutils.resize(frame, width=400)
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    skinMask = cv2.inRange(converted, lower, upper, binary)
    binary = cv2.inRange(converted, lower, upper)
    # apply a series of erosions and dilations to the mask
    # using an elliptical kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.morphologyEx(skinMask, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # blur the mask to help remove noise, then apply the
    # mask to the frame
    # binary = cv2.GaussianBlur(binary, (5, 5), 0)

    imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    skin = cv2.bitwise_and(frame, frame, mask=skinMask)
    im2, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('image2',skinMask)
    cv2.drawContours(frame, contours, -1, (0,255,0), 3)
    # show the skin in the image along with the mask
    cv2.imshow("images", np.hstack([frame, skin]))

    # if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
