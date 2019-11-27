import asyncio
from picamera import PiCamera
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
def fire_and_forget(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)

    return wrapped

@fire_and_forget
def rot_cam():
    i=10
    increment = -2
    while True:
        doDutyCycle(i)
        i=i+increment
        if i==2 or i==10:
            increment=increment*-1

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
    print("here")
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.framerate=24
    frame = np.empty((1024 * 768 * 3,), dtype=np.uint8)
    # camera.start_preview()
    # cam=cv2.VideoCapture(0)
    while True:
        # ret, frame=cam.read()
        camera.capture(frame, 'bgr')
        frame=frame.reshape((1024,768,3))
        #cv2.imshow("FrameBuffer2", face_detect(frame))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    # cv2.waitKey(0)


def main():
    asyncio.ensure_future(rot_cam())
    show_fb()


if __name__ == '__main__':
    main()
