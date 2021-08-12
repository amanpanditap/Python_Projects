#Note: 1)The detection works only on grayscale images. So it is important to convert the color image to grayscale.
# 2) detectMultiScale function is used to detect the faces.
# It takes 3 arguments — the input image, scaleFactor and minNeighbours. scaleFactor specifies how much the image size is reduced with each scale.
# minNeighbours specifies how many neighbors each candidate rectangle should have to retain it.
# 3) faces contains a list of coordinates for the rectangular regions where faces were found.
# 4) Saving the video will not work while using video file as input

import numpy as np
import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

font = cv2.FONT_HERSHEY_SIMPLEX

# To capture video from webcam.
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# To use a video file as input
# cap = cv2.VideoCapture('videos/input/vid.mp4')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('videos/output/detected-video.avi',fourcc, 20.0, (640,480))

while True:
    # Capture frame-by-frame
    ret, img = cap.read()

    if ret == True:
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #Convert to hsvscale
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #store the detected video from camera
        out.write(img)

        # Detect faces
        # faces = face_cascade.detectMultiScale(
        #         gray,
        #         scaleFactor=1.1,
        #         minNeighbors=5,
        #         minSize=(200, 200),
        #         flags=cv2.CASCADE_SCALE_IMAGE
        #     )
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        #most common parameters of the detectMultiScale function
        # scaleFactor : Parameter specifying how much the image size is reduced at each image scale.
        # minNeighbors : Parameter specifying how many neighbors each candidate rectangle should have to retain it.
        # minSize : Minimum possible object size. Objects smaller than that are ignored.
        # maxSize : Maximum possible object size. Objects larger than that are ignored.

        # Draw rectangle around the faces
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0), 3)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            cv2.putText(img,'Face',(x, y), font, 1,(255,0,0),2)

            #eyes
            eyes = eye_cascade.detectMultiScale(roi_gray)
            #detect eyes and draw rectangle around it
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                cv2.putText(img,'Eye',(x + ex,y + ey), 1, 1, (0, 255, 0), 1)

            #smile
            smile = smile_cascade.detectMultiScale(
                roi_gray,
                scaleFactor= 1.16,
                minNeighbors=35,
                minSize=(25, 25),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            #detect smile and draw rectangle around it
            for (sx, sy, sw, sh) in smile:
                cv2.rectangle(roi_color, (sh, sy), (sx+sw, sy+sh), (255, 0, 0), 2)
                cv2.putText(img,'Smile',(x + sx,y + sy), 1, 1, (0, 255, 0), 1)

            #Display Number of Faces
            cv2.putText(img,'Number of Faces : ' + str(len(faces)),(40, 40), font, 1,(255,0,0),2)

            #save the cropped faces
            crop_face = img[y:y + h, x:x + w]
            cv2.imwrite('videos/output/' + str(w) + str(h) + '_faces_video.jpg', crop_face)
            # cv2.imwrite('videos/output/' +  str(w) + str(h) + '_faces_filevideo.jpg', crop_face)     #for using file from video for identification
        # Display
        cv2.imshow('Original', img)
        cv2.imshow('Detected Gray', gray)
        cv2.imshow('Detected HSV', hsv)

        # Stop if escape key is pressed
        k = cv2.waitKey(1) & 0xff
        if k==27:
            break
    else:
        break
# Release the VideoCapture object
cap.release()
out.release()
cv2.destroyAllWindows()
