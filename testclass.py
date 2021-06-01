import cv2, imutils, time
import cvlib as cv
import numpy as np
import os
import sqlite3
import random

from flask import Flask, render_template, Response, request
from fuzzywuzzy import fuzz
from load import age_model, gender_model, emotion_model
from tensorflow.keras.preprocessing.image import img_to_array

age = age_model()
gender = gender_model()
emotion = emotion_model()

app = Flask(__name__)

def connection():
    conn = sqlite3.connect('thesismovies.db')
    # conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=['GET'])
def home_page():
    return render_template('index2.html')

classes_gender = ['Female','Male']
classes_age = ['0-12','13-15','16-17','Above 18']
classes_emotion = ['Angry','Disgust','Fear','Happy','Neutral','Sad','Surprise']
# classes_emotion_label = [0,0,0,1,1,0,1]
# label_age_glob = 0
# label_gender_glob = ''
# label_emotion_glob = ''

class Model:
    def __init__(self):
        self.label_age = 0
        self.label_gender = ''
        self.label_emotion = ''
        self.cap = cv2.VideoCapture(0)

    def get_age(self):
        return self.label_age

    def get_gender(self):
        return self.label_gender

    def get_emotion(self):
        return self.label_emotion

    def set_age(self, x):
        self.label_age = x

    def set_gender(self, x):
        self.label_gender = x

    def set_emotion(self, x):
        self.label_emotion = x

    def show(self):
        while True:
            (self.ret, self.frame) = self.cap.read()
            (self.face, self.confidence) = cv.detect_face(self.frame)

            for idx,f in enumerate(self.face):
                (startX, startY) = f[0], f[1]
                (endX, endY) = f[2], f[3]
                # draw rectangle over face
                cv2.rectangle(self.frame, (startX, startY), (endX, endY), (0,255,0), 2)
                # crop the detected face region
                face_crop0 = np.copy(self.frame[startY:endY, startX:endX])

                if (face_crop0.shape[0]  ) < 10 or (face_crop0.shape[1]) < 10:
                    continue
                # preprocessing for gender detection model
                face_crop = cv2.resize(face_crop0, (224,224))
                face_crop = face_crop.astype('float')/255.0
                face_crop = img_to_array(face_crop)
                face_crop = np.expand_dims(face_crop, axis = 0)

                face_crop_age = cv2.resize(face_crop0, (150,150))
                face_crop_age = face_crop_age.astype('float')/255.0
                face_crop_age = img_to_array(face_crop_age)
                face_crop_age = np.expand_dims(face_crop_age, axis = 0)

                face_crop1 = cv2.resize(face_crop0, (197,197))
                face_crop1 = face_crop1.astype('float')/255.0
                face_crop1 = img_to_array(face_crop1)
                face_crop1 = np.expand_dims(face_crop1, axis = 0)
                # appy detection for face
                conf1 = age.predict(face_crop_age)[0]
                conf2 = gender.predict(face_crop)[0]
                conf3 = emotion.predict(face_crop1)[0]

                # get label with max accuracy
                idx1 = np.argmax(conf1)
                idx2 = np.argmax(conf2)
                idx3 = np.argmax(conf3)

                tmp_label_age = classes_age[idx1]
                tmp_label_gender = classes_gender[idx2]
                tmp_label_emotion = classes_emotion[idx3]

                self.label_age = self.set_age(tmp_label_age)
                self.label_gender = self.set_gender(tmp_label_gender)
                self.label_emotion = self.set_emotion(tmp_label_emotion)
                # label_age_glob = label_age

                label = "{},{},{}".format(tmp_label_gender, tmp_label_age, tmp_label_emotion)


                Y = startY - 10 if startY - 10 > 10 else startY + 10

                cv2.putText(self.frame, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                # break
                self.cap.release()
                cv2.destroyAllWindows()
                exit(1)

            (self.ret, self.buffer) = cv2.imencode('.jpg',self.frame)
            self.frame = self.buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n')


    # def open_webcam(self):
    #     fpsLimit = 1
    #     startTime = time.time()
    #     cap = cv2.VideoCapture(0)
    #     cap.set(cv2.CAP_PROP_FPS,60)
    #     size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #     fps = cap.get(cv2.CAP_PROP_FPS)
    #
    #     while True:
    #         ret,frame = cap.read()
    #
    #         face, confidence = cv.detect_face(frame)
    #
    #         for idx, f in enumerate(face):
    #             # get corner points of face rectangle
    #             (startX, startY) = f[0], f[1]
    #             (endX, endY) = f[2], f[3]
    #             # draw rectangle over face
    #             cv2.rectangle(frame, (startX, startY), (endX, endY), (0,255,0), 2)
    #             # crop the detected face region
    #             face_crop = np.copy(frame[startY:endY, startX:endX])
    #             face_crop_age = np.copy(frame[startY:endY, startX:endX])
    #             face_crop1 = np.copy(frame[startY:endY, startX:endX])
    #
    #             if (face_crop.shape[0]  ) < 10 or (face_crop.shape[1]) < 10:
    #                 continue
    #             # preprocessing for gender detection model
    #             face_crop = cv2.resize(face_crop, (224,224))
    #             face_crop = face_crop.astype('float')/255.0
    #             face_crop = img_to_array(face_crop)
    #             face_crop = np.expand_dims(face_crop, axis = 0)
    #
    #             face_crop_age = cv2.resize(face_crop_age, (150,150))
    #             face_crop_age = face_crop_age.astype('float')/255.0
    #             face_crop_age = img_to_array(face_crop_age)
    #             face_crop_age = np.expand_dims(face_crop_age, axis = 0)
    #
    #             face_crop1 = cv2.resize(face_crop1, (197,197))
    #             face_crop1 = face_crop1.astype('float')/255.0
    #             face_crop1 = img_to_array(face_crop1)
    #             face_crop1 = np.expand_dims(face_crop1, axis = 0)
    #             # appy detection for face
    #             conf1 = age.predict(face_crop_age)[0]
    #             conf2 = gender.predict(face_crop)[0]
    #             conf3 = emotion.predict(face_crop1)[0]
    #
    #             # get label with max accuracy
    #             idx1 = np.argmax(conf1)
    #             idx2 = np.argmax(conf2)
    #             idx3 = np.argmax(conf3)
    #
    #             tmp_label_age = classes_age[idx1]
    #             tmp_label_gender = classes_gender[idx2]
    #             tmp_label_emotion = classes_emotion[idx3]
    #
    #             self.label_age = self.set_age(tmp_label_age)
    #             self.label_gender = self.set_gender(tmp_label_gender)
    #             self.label_emotion = self.set_emotion(tmp_label_emotion)
    #             # label_age_glob = label_age
    #
    #             label = "{},{},{}".format(tmp_label_gender, tmp_label_age, tmp_label_emotion)
    #
    #
    #             Y = startY - 10 if startY - 10 > 10 else startY + 10
    #
    #             cv2.putText(frame, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    #
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #
    #         ret, buffer = cv2.imencode('.jpg',frame)
    #         frame = buffer.tobytes()
    #
    #         yield (b'--frame\r\n'
    #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    #
    #     cap.release()
    #     cv2.destroyAllWindows()

m = Model()

@app.route('/video_feed')
def video_feed():
    return Response(m.show(), mimetype='multipart/x-mixed-replace; boundary=frame')

def pyshine_process():
    while True:
        # print("Age1: ",m.get_age())
        # m.open_webcam()
        print("Age1: ",m.get_age())

        list_movies = []
        c =connection()
        cursor = c.cursor()
        cursor.execute('select ads_path from movies order by ads_status desc, ads_id desc')
        items = cursor.fetchall()
        list_movies = items
        list_new = []
        # items = list(items)
        for item in items:
            item = list(item)
            tmp = item[0].split('/')
            list_new.append(tmp[-1])

        list_new = np.array(list_new)
        list_new = list_new.flatten()
        list_new = list(list_new)
        c.commit()
        c.close()
        return list_new

@app.route('/video_feed_2')
def video_feed_2():
    while True:
        # print("Age: ",m.get_age())

        movie = pyshine_process()
        movie = ','.join(movie)
        # print(movie)
        return movie

if __name__ == '__main__':
    app.run()
