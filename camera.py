import cv2
import os
import tensorflow as tf

from keras.preprocessing import image


import tensorflow.keras as k
import cv2
import numpy as np
import time

model = tf.keras.models.load_model('C:/Users/adinc/Desktop/Moodify/static/vgg16.h5')
face_cascade=cv2.CascadeClassifier("C:/Users/adinc/Desktop/Moodify/static/haarcascade_frontalface_alt2.xml")
ds_factor=0.6

class VideoCamera(object):
    mask=0
    video=0;

    def __init__(self):

        print("Video open")

        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
        print("Video close")


    def get_frame(self):
        class_name = ['Happy', 'Neutral', 'Sad']
        success, pic = self.video.read()
        #pic=cv2.resize(pic,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)


        gray=cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
        #print(pic.shape)

        face_rects=face_cascade.detectMultiScale(gray,1.3,5)
        img=pic.copy()
        for (x,y,w,h) in face_rects:
            img=img[y-10:y+h+10,x-10:x+w+10]
            break
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)












        path="static\\img.png"
        resized = cv2.resize(img, (48, 48), interpolation=cv2.INTER_AREA)
        resized = resized / 255
        cv2.imwrite('static\\img.png', resized)



        #img = image.load_img(path, target_size=(48, 48))
        #print(img.shape)
        x = image.img_to_array(resized)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        classes = model.predict(images)
        print(classes[0])
        idx = np.argmax(classes[0])
        mood=class_name[idx]
        print(class_name[idx])






        #i=np.row_stack((pic,white))
        pic=pic[100:pic.shape[0]-100,100: pic.shape[1]-100]

        return (pic,mood)
