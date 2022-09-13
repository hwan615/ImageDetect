import cv2
import math
import numpy as np

## Params
img = cv2.imread('./static/leo.jpg')
mask_template = np.zeros([826, 550, 3])
mask_img = cv2.imwrite('mask_img.jpg', mask_template)
DETECT_LINE_COLOR = (0, 0, 255)
DETECT_POINT_COLOR = (255, 0 , 0)
COLLECTED_POINTS = []

def detectPoint(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.line(img, (x,y), (x,y), DETECT_POINT_COLOR, 5)
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        COLLECTED_POINTS.append([x,y])
        connectPoints()
        cv2.imshow('image', img)

## 어떤 기준으로 점과 점 사이를 이을까?
## 기존에 있던 점들 중 가장 가까운 거리의 2개를 이으면 
## 점이 많아질 수록 정확한 이미지 contour 를 갖을 수 있을 것 같다.
## make connection to the nearest two points
def connectPoints():
    if COLLECTED_POINTS.__len__() == 1:
        return 
    elif COLLECTED_POINTS.__len__() == 2:
        POINT1 = COLLECTED_POINTS[0]
        POINT2 = COLLECTED_POINTS[1]
        cv2.line(img, POINT1, POINT2, DETECT_LINE_COLOR, 3)
    else:
        INDEX_OF_POINT_TO_CONNECT = getDistance().astype(int)
        print("index", INDEX_OF_POINT_TO_CONNECT)
        POINT1 = COLLECTED_POINTS[INDEX_OF_POINT_TO_CONNECT[0]]
        POINT2 = COLLECTED_POINTS[INDEX_OF_POINT_TO_CONNECT[1]]
        connectTwoPoints()

def connectTwoPoints(originPoint, point1, point2):
    cv2.line(img, originPoint, point1, DETECT_LINE_COLOR, 3)
    cv2.line(img, originPoint, point2, DETECT_LINE_COLOR, 3)
    cv2.line(mask_template, originPoint, point1, DETECT_LINE_COLOR, 3)
    cv2.line(mask_template, originPoint, point2, DETECT_LINE_COLOR, 3)
    cv2.imshow("mask image", mask_template)

## 새로 들어오는 점과 기존에 있던 점들과의 거리만 계산해서
## 가장 짧은 거리 두개를 그으면 될 줄 알았는데
## 기존의 선들도 새로 그어야한다...새로운 계산법이 필요할 것 같다
def getDistance():
    POINT_DISTANCE = np.zeros((COLLECTED_POINTS.__len__(), 2))
    for idx, point in enumerate(COLLECTED_POINTS):
        POINT_DISTANCE[idx] = [math.dist(point, COLLECTED_POINTS[-1]), idx]
    POINT_DISTANCE = POINT_DISTANCE[POINT_DISTANCE[:, 0].argsort()]
    print(POINT_DISTANCE)
    RESULT_POINT_INDEX = np.array([POINT_DISTANCE[-1][1], POINT_DISTANCE[-2][1]])
    return RESULT_POINT_INDEX

if __name__=="__main__":
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', detectPoint)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
