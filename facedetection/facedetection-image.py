#Note: 1)The detection works only on grayscale images. So it is important to convert the color image to grayscale.
# 2) detectMultiScale function is used to detect the faces.
# It takes 3 arguments — the input image, scaleFactor and minNeighbours. scaleFactor specifies how much the image size is reduced with each scale.
# minNeighbours specifies how many neighbors each candidate rectangle should have to retain it.
# 3) faces contains a list of coordinates for the rectangular regions where faces were found.

import numpy as np
import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Read the input image
img = cv2.imread('images/img.jpg')

# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Convert into hsvscale
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#faces = face_cascade.detectMultiScale(gray)

# Draw rectangle around the faces
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    #detect eyes and draw rectangle around it
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    #save the cropped faces
    crop_face = img[y:y + h, x:x + w]
    cv2.imwrite(str(w) + str(h) + '_faces.jpg', crop_face)

# Display the output
cv2.imshow('Original', img)
cv2.imshow('Detected Gray', gray)
cv2.imshow('Detected HSV', hsv)

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('detected_image.jpg',img)
    cv2.destroyAllWindows()
