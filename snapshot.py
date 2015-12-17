import cv2


cap = cv2.VideoCapture(0)


# Set video to 320x240
cap.set(3, 320)
cap.set(4, 240)

take_picture = False;
t0, filenum = 0, 1

while True:
  val, frame = cap.read()
  cv2.imshow("video", frame)

  key = cv2.waitKey(30)

  if key == ord(' '):
    t0 = cv2.getTickCount()
    take_picture = True
  elif key == ord('q'):
    break

  if take_picture and ((cv2.getTickCount()-t0) / cv2.getTickFrequency()) > 2:
    cv2.imwrite(str(filenum) + ".jpg", frame)
    filenum += 1
    take_picture = False

cap.release()
cv2.destroyAllWindows()

