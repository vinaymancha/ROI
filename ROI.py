import cv2
import numpy as np


image = cv2.imread('C:\\Users\\vinay\\Desktop\\ROI\\images\\image1.jpg', cv2.IMREAD_UNCHANGED)

img_2 = image
cv2.imshow('img', img_2)



#extract red channel
image = image[:,:,2]


cv2.imshow('grayscale', image)

# binary
ret, thresh = cv2.threshold(image, 225, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('threshold', thresh)

# dilation
kernel = np.ones((3, 3), np.uint8)
img_dilation = cv2.dilate(thresh, kernel, iterations=1)
img_dilation = cv2.bitwise_not(img_dilation)

#cv2.imshow('dilated', img_dilation)

# find contours
# cv2.findCountours() function changed from OpenCV3 to OpenCV4: now it have only two parameters instead of 3
cv2MajorVersion = cv2.__version__.split(".")[0]
# check for contours on thresh
if int(cv2MajorVersion) >= 4:
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
else:
    im2, ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# sort contours
sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

for i, ctr in enumerate(sorted_ctrs):
    # Get bounding box
    x, y, w, h = cv2.boundingRect(ctr)

    # Getting ROI
    roi = image[y:y + h, x:x + w]
    
    # show ROI

    cv2.rectangle(img_2, (x, y), (x + w, y + h), (0, 255, 0), 2)
  
    print((x, y), x + w, y + h)

    if w > 15 and h > 15:
        cv2.imwrite('C:\\Users\\vinay\\Desktop\\ROI\\images\\{}.jpg'.format(i), roi)


for i, ctr in enumerate(sorted_ctrs):
    # Get bounding box
    x, y, w, h = cv2.boundingRect(ctr)

    area = (w*h/16)*111   ##distance between two latitudes and longitudes is 111 km
    text = str(area) + " Sq.Km"
    if area > 6000:
        cv2.putText(img_2, text, (x,y ), cv2.FONT_HERSHEY_SIMPLEX, .3, (0, 0, 0), lineType=cv2.LINE_AA)

cv2.imshow('marked areas', img_2)
cv2.waitKey(0)
