import cv2
import numpy as np
RED = 2
GREEN = 1
BLUE = 0

def nothing(x):
    pass

# Create a black image, a window
# img = cv2.imread('1.jpg',1)
# cv2.namedWindow('image', cv2.WINDOW_NORMAL);
cap = cv2.VideoCapture(0)
cv2.namedWindow('image', cv2.WINDOW_NORMAL);

# create trackbars for color change
cv2.createTrackbar('<R','image',--5,255,nothing)
cv2.createTrackbar('R>','image',-255,255,nothing)
cv2.createTrackbar('<G','image',-255,255,nothing)
cv2.createTrackbar('G>','image',-255,255,nothing)
cv2.createTrackbar('<B','image',-255,255,nothing)
cv2.createTrackbar('B>','image',-255,255,nothing)
# frame = img
while(1):
    ret, img = cap.read()
    # img = cv2.imread('sfa_database/original/img (3).jpg',1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    b_r = cv2.getTrackbarPos('<R','image')
    u_r = cv2.getTrackbarPos('R>','image')
    b_g = cv2.getTrackbarPos('<G','image')
    u_g = cv2.getTrackbarPos('G>','image')
    b_b = cv2.getTrackbarPos('<B','image')
    u_b = cv2.getTrackbarPos('B>','image')

    lower_b = np.array([b_b,b_g,b_r])
    upper_b = np.array([u_b,u_g,u_r])
    frame = img
    height, width, channels = frame.shape


    mask_skin = cv2.inRange(img, lower_b, upper_b)
    frame = cv2.bitwise_and(img, img, mask=mask_skin)
    cv2.imshow('image',frame)

cv2.destroyAllWindows()