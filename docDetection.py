import cv2

## param
img = cv2.imread('./static/leo.jpg')
cap = cv2.VideoCapture(0)
imgW = 640
imgH = 480
cap.set(3, imgW)
cap.set(4, imgH)
cap.set(10,150)

def imgPreprocessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(img, (7,7), 0)
    imgCanny = cv2.Canny(imgBlur, 50, 200)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    imgEro = cv2.erode(imgCanny, kernel, iterations=1)
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    return imgCanny, imgDil

def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    return biggest


# while True:
#     success, img = cap.read()
#     cv2.imshow('video', img)
#     imgBlur = imgPreprocessing(img)
#     if cv2.waitKey(1) & 0xFF == ord('x'):
#         break

