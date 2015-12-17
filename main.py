import cv2
from uv_approach.skin_classifier_uv import SkinClassifierUV
import numpy as np

# import pyttsx

sc = SkinClassifierUV()
# sc.learn_from_database()
# print('SKIN HISTO')
# sc.skin_histogram.plot()
# print('NON-SKIn HISTO')
# sc.non_skin_histogram.plot()
# sc.test()

# cap = cv2.VideoCapture(0)
# cv2.namedWindow('frame', cv2.WINDOW_NORMAL);
#
# while (True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#
#     # Our operations on the frame come here
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
#     # gray = sc.mark_skin(frame)
#     # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
#     # Display the resulting frame
#
#     #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
#
#     height, width, channels = frame.shape
#
#     RED = 2
#     GREEN = 1
#     BLUE = 0
#
#     # frame = cv2.convertScaleAbs(frame)
#     # for i in range(0, width):
#     #     for j in range(0, height):
#     #
#     #         y = (frame.item(j, i, RED) + 2 * frame.item(j, i, GREEN) + frame.item(j, i, BLUE)) / 4
#     #         u = int(frame.item(j, i, RED)) - int(frame.item(j, i, GREEN))
#     #         v = int(frame.item(j, i, BLUE)) - int(frame.item(j, i, GREEN))
#     #         frame.itemset((j,i,0), v)
#     #         frame.itemset((j,i,1), u)
#     #         frame.itemset((j,i,2), y)
#
#     lower_b = np.array([-40, 10, -255])
#     upper_b = np.array([11, 74, 255])
#     mask_skin = cv2.inRange(frame, lower_b, upper_b)
#     frame = cv2.bitwise_and(frame, frame, mask=mask_skin)
#
#     cv2.imshow('frame', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()

# engine = pyttsx.init()
# engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()








RED = 2
GREEN = 1
BLUE = 0


frame = cv2.imread('sfa_database/original/img (3).jpg',1)

height, width, channels = frame.shape
frame = cv2.convertScaleAbs(frame)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
# for i in range(0, width):
#     for j in range(0, height):
#
#         y = (frame.item(j, i, RED) + 2 * frame.item(j, i, GREEN) + frame.item(j, i, BLUE)) / 4
#         u = int(frame.item(j, i, RED)) - int(frame.item(j, i, GREEN))
#         v = int(frame.item(j, i, BLUE)) - int(frame.item(j, i, GREEN))
#         frame.itemset((j,i,0), v)
#         frame.itemset((j,i,1), u)
#         frame.itemset((j,i,2), y)


lower_b = np.array([-255, 10, -40])
upper_b = np.array([255, 74, 11])
mask_skin = (cv2.inRange(frame, lower_b, upper_b))
frame = cv2.bitwise_and(frame, frame, mask=mask_skin)

cv2.imshow('image',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()