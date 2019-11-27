import time
import numpy as np
import cv2
import asyncio
import firebase_admin
from firebase_admin import credentials,firestore,storage
from os import listdir
from os.path import isfile, join
from random import seed
from random import random
from playsound import playsound

seed(1)

cred = credentials.Certificate("./servicekey.json")
firebase_admin.initialize_app(cred)
# {
#     'storageBucket':'gs://sentryhome-c84fb.appspot.com'
# })
db=firestore.client()
ref=db.collection("Options").document("isArmed")
doc=None
face_no=0
# from pykeyboard import PyKeyboard
faceCascade = cv2.CascadeClassifier("haarcascade_default.xml")

def fire_and_forget(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)

    return wrapped

@fire_and_forget
def get_data():
    global doc
    try:
        doc=ref.get()
        # print(doc.to_dict())
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
        screams.append(onlyfiles[val])
        print("./Scream/"+onlyfiles[val])
        playsound("./Scream/"+onlyfiles[val])



def face_detect(orig):
    global face_no
    # normalized=cv2.normalize(orig,normalized,1,255,cv2.NORM_MINMAX)
    gray=cv2.cvtColor(orig,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(20, 20),
        # flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    # face_no=0
    # print(len(faces))
    if len(faces)>0:
        # play_scream(len(faces))
        if not len(faces) == face_no:
            face_no=len(faces)
            asyncio.ensure_future(play_scream(len(faces)))
        for (x, y, w, h) in faces:
            cv2.rectangle(orig, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # cv2.imshow("face "+str(i),orig[y:y+h,x:x+h])
            # cv2.destroyWindow("face "+str(i+1))
    return orig

def show_fb():
    cam=cv2.VideoCapture(0)
    # doc=None
    global doc
    try:
        doc=ref.get()
        print(doc.to_dict())
    except:
        print("not found")
    while True:
        ret, frame=cam.read()
        # print(doc.to_dict()["check"])
        if(doc.to_dict()["check"]):
            cv2.imshow("FrameBuffer2", face_detect(frame))
        else:
            cv2.imshow("FrameBuffer2",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # if("ALL COMPLETED"==asyncio.ALL_COMPLETED):
        asyncio.ensure_future(get_data())
        # print(asyncio.ALL_COMPLETED)
        #     get_data(doc=doc)
    cam.release()
    # cv2.waitKey(0)


def main():
    show_fb()


if __name__ == '__main__':
    main()
