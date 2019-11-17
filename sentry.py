import time
import numpy as np
import cv2
import RPi.GPIO as GPIO

faceCascade = cv2.CascadeClassifier("haarcascade_default.xml")

servoPIN = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0) # Initialization


def doDutyCycle(ip, t=1.0):
    GPIO.output(servoPIN, True)
    print(ip)
    p.ChangeDutyCycle(ip)
    time.sleep(t)
    GPIO.output(servoPIN, False)
    p.ChangeDutyCycle(0)


def face_detect(orig):
    # normalized=cv2.normalize(orig,normalized,1,255,cv2.NORM_MINMAX)
    gray=cv2.cvtColor(orig,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30),
        # flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    i=1
    for (x, y, w, h) in faces:
        cv2.rectangle(orig, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # cv2.imshow("face "+str(i),orig[y:y+h,x:x+h])
        # cv2.destroyWindow("face "+str(i+1))
        i=i+1
    return orig

def show_fb():
    cam=cv2.VideoCapture(0)
    while True:
        doDutyCycle(10)
        doDutyCycle(8)
        doDutyCycle(6)
        doDutyCycle(4)
        doDutyCycle(3)
        doDutyCycle(4)
        doDutyCycle(6)
        doDutyCycle(8)
        doDutyCycle(10)
        ret, frame=cam.read()
        #cv2.imshow("FrameBuffer2", face_detect(frame))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cam.release()
    # cv2.waitKey(0)


def main():
    show_fb()


if __name__ == '__main__':
    main()
