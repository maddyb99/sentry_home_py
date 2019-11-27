import asyncio
from picamera import PiCamera
import time
import numpy as np
import cv2
import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials,firestore,storage
from os import listdir
from os.path import isfile, join
from random import seed
from random import random
from pydub import AudioSegment
from pydub.playback import play

seed(1)

cred = credentials.Certificate("./servicekey.json")
firebase_admin.initialize_app(cred)
db=firestore.client()
ref=db.collection("Options").document("isArmed")
doc=None
face_no=0
faceCascade = cv2.CascadeClassifier("haarcascade_default.xml")

servoPIN = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0) # Initialization


def doDutyCycle(ip, t=1.0):
    GPIO.output(servoPIN, True)
    #print(ip)
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

@fire_and_forget
def get_data():
    global doc
    try:
        doc=ref.get()
        #print(doc.to_dict())
        # return await True
    except:
        print("not found")


@fire_and_forget
def play_scream(number):
    onlyfiles = [f for f in listdir("./Scream") if isfile(join("./Scream", f))]
    # print(onlyfiles)
    screams=[]
    for i in range(number):
        val=1+int(random()*number)
        # print(val)
        song=AudioSegment.from_mp3("./Scream/"+onlyfiles[val])
        screams.append(onlyfiles[val])
        print("./Scream/"+onlyfiles[val])
        # playsound("./Scream/"+onlyfiles[val])
        play(song)

def face_detect(orig):
    global face_no
    # normalized=cv2.normalize(orig,normalized,1,255,cv2.NORM_MINMAX)
    gray=cv2.cvtColor(orig,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        # flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    if len(faces)>0:
        # play_scream(len(faces))
        if not len(faces) == face_no:
            face_no=len(faces)
            asyncio.ensure_future(play_scream(len(faces)))
        for (x, y, w, h) in faces:
            cv2.rectangle(orig, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # cv2.imshow("face "+str(i),orig[y:y+h,x:x+h])
            # cv2.destroyWindow("face "+str(i+1))
    else:
        face_no=0
    return orig

def show_fb():
    print("here")
    global doc
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate=24
    frame = np.empty((480 * 640 * 3,), dtype=np.uint8)
    # camera.start_preview()
    # cam=cv2.VideoCapture(0)global doc
    try:
        doc=ref.get()
        print(doc.to_dict())
    except:
        print('Not found!')

    #get_data()
    #print(doc.to_dict())
    while True:
        # ret, frame=cam.read()
        camera.capture(frame, 'bgr')
        frame=frame.reshape((480,640,3))
        print(doc.to_dict())
        if(doc.to_dict()["check"]):
            cv2.imshow("FrameBuffer2", face_detect(frame))
        else:
            cv2.imshow("FrameBuffer2",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # if("ALL COMPLETED"==asyncio.ALL_COMPLETED):
        asyncio.ensure_future(get_data())
    cam.release()
    # cv2.waitKey(0)


def main():
    asyncio.ensure_future(rot_cam())
    show_fb()


if __name__ == '__main__':
    main()
