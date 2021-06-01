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
import json
import pyprocess

age = age_model()
gender = gender_model()
emotion = emotion_model()

app = Flask(__name__)


def connection():
    conn = sqlite3.connect('thesismovies.db')
    # conn.row_factory = sqlite3.Row
    return conn


# def find_trailer(path_one, name):
#     number = fuzz.ratio(path_one,name)
#     return number
#
# def play_trailer(path, name):
#     path = os.listdir(path)
#     l = []
#     for i in path:
#         tmp = find_trailer(i, name)
#         if tmp >= 40:
#             l.append(i)
#     return l
#
# def select(path):
#     list_movies = []
#     c =connection()
#     cursor = c.cursor()
#     cursor.execute('select * from movies ')
#     items = cursor.fetchall()
#     for i in items:
#         tmp = play_trailer(path, i)
#         list_movies.append(tmp)
#     c.commit()
#     c.close()
#     return list_movies

@app.route("/", methods=['GET'])
def home_page():
    return render_template('index2.html')


classes_gender = ['Female', 'Male']
classes_age = ['0-12', '13-15', '16-17', 'Above 18']
classes_emotion = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
# classes_emotion_label = [0,0,0,1,1,0,1]
# label_age = 0
# label_gender = ''
# label_emotion = ''
# label_age_glob = 0
# label_gender_glob = ''
# label_emotion_glob = ''

global label_age_glob
global label_gender_glob
global label_emotion_glob

label_age_glob = None
label_gender_glob = None
label_emotion_glob = None


# global key
# key = 0
# @app.route('/video_feed')
def open_webcam():
    # def video_feed():
    # key = 1
    fpsLimit = 1
    startTime = time.time()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 60)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv2.CAP_PROP_FPS)

    while True:
        ret, frame = cap.read()

        frame = imutils.resize(frame, width=480, height=480)
        # time.sleep(3)
        # now = time.time()
        # if (int(now - startTime)) > fpsLimit:
        # cv2.imshow('trio_detection', frame

        face, confidence = cv.detect_face(frame)

        for idx, f in enumerate(face):
            # get corner points of face rectangle
            (startX, startY) = f[0], f[1]
            (endX, endY) = f[2], f[3]
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

            # crop the detected face region
            face_crop0 = np.copy(frame[startY:endY, startX:endX])
            # face_crop_age = np.copy(frame[startY:endY, startX:endX])
            # face_crop1 = np.copy(frame[startY:endY, startX:endX])

            if (face_crop0.shape[0]) < 10 or (face_crop0.shape[1]) < 10:
                continue

            # preprocessing for gender detection model
            face_crop = cv2.resize(face_crop0, (50, 50))
            face_crop = face_crop.astype('float') / 255.0
            face_crop = img_to_array(face_crop)
            face_crop = np.expand_dims(face_crop, axis=0)

            face_crop_age = cv2.resize(face_crop0, (50, 50))
            face_crop_age = face_crop_age.astype('float') / 255.0
            face_crop_age = img_to_array(face_crop_age)
            face_crop_age = np.expand_dims(face_crop_age, axis=0)

            face_crop1 = cv2.resize(face_crop0, (197, 197))
            face_crop1 = face_crop1.astype('float') / 255.0
            face_crop1 = img_to_array(face_crop1)
            face_crop1 = np.expand_dims(face_crop1, axis=0)
            # appy detection for face
            conf1 = age.predict(face_crop_age)[0]
            conf2 = gender.predict(face_crop)[0]
            conf3 = emotion.predict(face_crop1)[0]

            # get label with max accuracy
            idx1 = np.argmax(conf1)
            idx2 = np.argmax(conf2)
            idx3 = np.argmax(conf3)

            label_age = classes_age[idx1]
            label_gender = classes_gender[idx2]
            label_emotion = classes_emotion[idx3]

            # yield label_age
            # yield label_gender
            # yield label_emotion

            label_age_glob = idx1
            label_gender_glob = idx2
            label_emotion_glob = idx3
            # data = [
            #     {'Gender': str(label_gender_glob), 'Age': str(label_age_glob), 'Emotion': str(label_emotion_glob)}, ]
            # with open('data.json', 'a') as f:
            #     json.dump(data, f)

            # print(label_age_glob)
            # print(type(label_age))
            # global age_mark = label_age
            # gender_mark = label_gender
            # emotion_mark = label_emotion

            label = "{},{},{}".format(label_gender, label_age, label_emotion)
            Y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.putText(frame, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # press Q key to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # frame = (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # return Response(frame, mimetype='multipart/x-mixed-replace; boundary=frame')

        # return label_age_glob, label_gender_glob, label_emotion_glob, (b'--frame\r\n'
        #                                                                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # cap.release()
    # cv2.destroyAllWindows()


# def get_value():
#
#     # tmp = open_webcam()
#
#     # tmp = video_feed()
#     age = label_age_glob
#     gender = label_gender_glob
#     emotion = label_emotion_glob
#     # age = next(tmp)
#     # gender = next(tmp)
#     # emotion = next(tmp)
#     # frame = next(tmp)
#     return age, gender, emotion


# def pyshine_process(age, gender, emotion):
#     # while True:
#     # tmp = get_value()
#     # tmp = open_webcam()
#     # with open('data.json','r') as f:
#     #     json_read = json.load(f)
#     # json_read = json_read[-1]
#     # age = json_read['Age']
#     # gender = json_read['Gender']
#     # emotion = json_read['Emotion']
#     print("Age: ", age)
#     # for i in range(3):
#     #     if i == 0:
#     #         age = next(tmp)
#     #     elif i == 1:
#     #         gender = next(tmp)
#     #     elif i == 2:
#     #         emotion = next(tmp)
#     # print("Age: ",age)
#     # print("Gender: ",gender)
#     # print("Emotion: ",emotion)
#
#     list_movies = []
#     c = connection()
#     cursor = c.cursor()
#     # print("Age: ",label_age_glob)
#     age_mark = '0-12'
#     if age_mark == 'Above 18':
#         # if label_gender == 'Male':
#         cursor.execute("""select ads_path from movies where ads_age_from = '0-12'
#                         order by ads_status desc
#                         """)
#         items = cursor.fetchall()
#         # list_movies = items
#         list_movies = items
#         # age_mark = '16-17'
#
#     # elif age_mark == '16-17':
#     #     cursor.execute("""select ads_path from movies where ads_age_from = 'C16'
#     #                     order by ads_status desc
#     #                     """)
#     #     items = cursor.fetchall()
#     #     list_movies = items
#     #
#     #
#     # elif age_mark == '13-15':
#     #     cursor.execute("select ads_path from movies where ads_age_from = 'C13'")
#     #     items = cursor.fetchall()
#     #     list_movies = items
#     #
#     #
#     # elif age_mark == '0-12':
#     #     cursor.execute("select ads_path from movies where ads_age_from = 'P'")
#     #     items = cursor.fetchall()
#     #     list_movies = items
#     #
#     else:
#         cursor.execute("select ads_path from movies order by ads_status desc, ads_id desc")
#         items = cursor.fetchall()
#         list_movies = items
#
#     list_new = []
#     # items = list(items)
#     for item in items:
#         item = list(item)
#         tmp = item[0].split('/')
#         list_new.append(tmp[-1])
#     print('age_mark: ', age_mark)
#     # list_movies = select(path)
#     list_new = np.array(list_new)
#     list_new = list_new.flatten()
#     list_new = list(list_new)
#     c.commit()
#     # close connection
#     c.close()
#
#     return list_new


@app.route('/video_feed')
def video_feed():
    # tmp = get_value()
    # open = tmp[3]
    # params = result
    # return Response(pyshine_process(params), mimetype='multipart/x-mixed-replace; boundary=frame')
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(open_webcam(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response(open, mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/video_feed_2')
@app.route('/youtube_feed')
# def video_feed_2():
def youtube_feed():
    # global result
    while True:
        # open_webcam()
        print(label_age_glob)
        movie = pyprocess.pyshine_process(age=label_age_glob, gender=label_gender_glob, emotion=label_emotion_glob)
        movie = ','.join(movie)
        # print(movie)
        return movie
        # return """
        #         <iframe src="https://youtube.com/embed/videoseries'+'?playlist='+ movie +'?autoplay=1" width="854" height="480" frameborder="0" encrypted-media/></iframe>
        # """


# @app.route("/res", methods=['POST','GET'])
# def res():
#     global result
#     if request.method == 'POST':
#         result = request.form.to_dict()
#         return render_template("results.html", result= result)

if __name__ == '__main__':
    app.run()
    # app.run(host='192.168.1.12', debug=False,port=9999)
