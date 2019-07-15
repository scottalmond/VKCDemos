import sys
import cv2
import numpy as np

#import queue
from multiprocessing import Queue

import pprint

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    
    rows = gray.shape[0]

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=30,
                               minRadius=1, maxRadius=30)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(frame, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv2.circle(frame, center, radius, (255, 0, 255), 3)
    return frame

def main(argv):
    display = 'imshow'

    if display == 'imshow':
        cap = cv2.VideoCapture(0)
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if ret:
                frame = process_frame(frame) 
                # Display the resulting frame
                cv2.imshow('rpicam',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()
    
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])

