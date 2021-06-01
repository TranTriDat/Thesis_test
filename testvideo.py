import cv2, imutils, time
import cvlib as cv
import numpy as np
import os
import time
from load import age_model, gender_model, emotion_model
from tensorflow.keras.preprocessing.image import img_to_array
import keras.backend as K


def f1_score(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision * recall)/(precision + recall + K.epsilon())
    return f1_val

age = age_model()
# gender = gender_model()
emotion = emotion_model()

def open_webcam():
    # fpsLimit = 1
    # startTime = time.time()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS,60)
    # size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # fps = cap.get(cv2.CAP_PROP_FPS)

    classes_gender = ['Female','Male']
    classes_age = ['0-12','13-15','16-17','Above 18']
    classes_emotion = ['Angry','Disgust','Fear','Happy','Neutral','Sad','Surprise']
    classes_emotion_label = [0,0,0,1,1,0,1]
    while True:
        ret,frame = cap.read()
        # time.sleep(3)
        # now = time.time()
        # if (int(now - startTime)) > fpsLimit:
        # cv2.imshow('trio_detection', frame

        face, confidence = cv.detect_face(frame, enable_gpu= True)

        for idx, f in enumerate(face):
            # get corner points of face rectangle
            (startX, startY) = f[0], f[1]
            (endX, endY) = f[2], f[3]

            # draw rectangle over face
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0,255,0), 2)

            # crop the detected face region
            face_crop = np.copy(frame[startY:endY, startX:endX])
            face_crop1 = np.copy(frame[startY:endY, startX:endX])


            if (face_crop.shape[0]  ) < 10 or (face_crop.shape[1]) < 10:
                continue

            # preprocessing for gender detection model
            face_crop = cv2.resize(face_crop, (150,150))
            face_crop = face_crop.astype('float')/255.0
            face_crop = img_to_array(face_crop)
            face_crop = np.expand_dims(face_crop, axis = 0)

            # face_crop1 = cv2.resize(face_crop1, (197,197))
            # face_crop1 = face_crop1.astype('float')/255.0
            # face_crop1 = img_to_array(face_crop1)
            # face_crop1 = np.expand_dims(face_crop1, axis = 0)
            a = age.predict(face_crop)
            print(a)
            conf1 = age.predict(face_crop)
            # conf2 = age.predict(face_crop)[1][0]
            # conf2 = gender.predict(face_crop)[0]
            # conf3 = emotion.predict(face_crop1)[0]

            # print(conf1,conf2)

            # get label with max accuracy
            idx1 = np.argmax(conf1)
            # idx2 = np.argmax(conf2)
            # idx3 = np.argmax(conf3)

            label_age = classes_age[idx1]
            # label_gender = classes_gender[idx2]
            # label_emotion = classes_emotion[idx3]
            # label_gender = conf1
            # label_age = conf1
            # label = "{},{},{}".format(label_gender,label_age, label_emotion)
            label = "{}".format(label_age)
            Y = startY - 10 if startY - 10 > 10 else startY + 10

            # new_frame_time = time.time()
            # fps = 1/(new_frame_time-prev_frame_time)
            # prev_frame_time = new_frame_time
            # fps = int(fps)
            # fps = str(fps)
            # trailer_re = 0 if label=='man' else 1
            # write label and confidence above face rectangle
            cv2.putText(frame, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.imshow('detect',frame)
        # press Q key to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
open_webcam()
