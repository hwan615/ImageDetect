import cv2
import numpy as np

DETECTED_POINT = []
width = 300
height = 400

def detect_point(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
        cv2.line(img, (x,y), (x,y), (255, 0, 0), 3)
        DETECTED_POINT.append([x,y])

    if DETECTED_POINT.__len__() == 4:
        point1 = np.float32(DETECTED_POINT)
        point2 = np.float32([[0,0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(point1, point2)
        output = cv2.warpPerspective(img, matrix, (width, height))
        cv2.imshow("imgOutput", output)
    cv2.imshow('img', img)

img = cv2.imread('./static/tile.jpg')
cv2.imshow('img', img)
cv2.setMouseCallback('img', detect_point)
cv2.waitKey(0)
cv2.destroyAllWindows()
