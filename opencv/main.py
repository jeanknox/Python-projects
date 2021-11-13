import cv2
import imutils
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import time

user = "admin"
password = "614937"
ip = "192.168.1.191"
port = "554"
stream = "1"

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


cam_adress_rtsp ='rtsp://{DOMINIO}:{PORTA}/user={USUARIO}&password={SENHA}&channel=1&stream=0.sdp'.format(DOMINIO=ip, PORTA=port, USUARIO=user, SENHA=password)
camera = cv2.VideoCapture(cam_adress_rtsp) 
while True:
    start = time.time()
    _, image = camera.read()
    #orig = image.copy()
    image = imutils.resize(image, width=min(800, image.shape[1]))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
    for (x, y, w, h) in rects:
	    cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    for (xA, yA, xB, yB) in pick:
	    cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
    end = time.time()
    elapsed_time = 1/(end - start)
    cv2.putText(image, f"FPS:{elapsed_time:2.0f}", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
    cv2.putText(orig, f"FPS:{elapsed_time:2.0f}", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
    cv2.imshow('Frame', image)
    #cv2.imshow('Frame orig', orig)
  
    if cv2.waitKey(1) & 0xFF == ord('q'): break
    

camera.release()
cv2.destroyAllWindows()
