#Simple program to detect eye center at close distance

import cv2
import numpy as np
import time

#select video.
cap = cv2.VideoCapture(0)


mean_time = [] 
while(True):
    
    start_time = time.time()
    #read frame
    ret,frame = cap.read()
    
    #is open?
    if ret is None:
        break
    
    #extract gray roi
#     roi = frame[100:-100, 100, -100]
    roi = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_AREA)
    rows, cols, _ = roi.shape
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (7,7),0)

    #extract biggest contour (in area) ~pupil
    _, threshold = cv2.threshold(gray_roi, 30, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse = True)

    #draw contours and centers
    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        #cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.line(roi, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
        cv2.line(roi, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)
        break

#     cv2.imshow("Threshold", threshold)
#     cv2.imshow("gray roi", gray_roi)
    cv2.imshow("Roi", roi)

    #if 'q' pressed quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #Store elapsed time
    mean_time.append(time.time() - start_time)


cv2.destroyAllWindows()
cap.release()
cv2.destroyAllWindows()
mean_time = np.mean(mean_time)
print("Execution Time (s) : "+ str(mean_time) + " (normal ~0.21s)")
print("Executions per second: " + str(1/mean_time))

