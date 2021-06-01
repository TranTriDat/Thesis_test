def x():
    while True:
        for i in range(10):

            print('-------  ')
        return 1,2,3,4

def y():
    while True:
        tmp = x()
        one=''
        two=''
        three=''
        for i in range(3):
            if i ==0:
                one = tmp[0]
                # one=next(tmp)
            elif i ==1:
                two= tmp[1]
                # two= next(tmp)
            elif i ==2:
                three = tmp[2]
                # three=next(tmp)
        # print(tmp[3])
        print(one, two, three)
        break
y()

def z():
    while True:
        tmp = x()
        print(tmp[3])
        break
z()
# import cv2
# from load import age_model, gender_model, emotion_model
# from tensorflow.keras.preprocessing.image import img_to_array
# import numpy as np
#
# age = age_model()
# gender = gender_model()
# emotion = emotion_model()
# # Load the cascade
#
# classes_gender = ['Female','Male']
# classes_age = ['0-12','13-15','16-17','Above 18']
# classes_emotion = ['Angry','Disgust','Fear','Happy','Neutral','Sad','Surprise']
#
# # To capture video from webcam.
# cap = cv2.VideoCapture(0)
# # To use a video file as input
# # cap = cv2.VideoCapture('filename.mp4')
# def x():
#     while True:
#         # Read the frame
#         _, img = cap.read()
#
#         # Convert to grayscale
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#         # Detect the faces
#         faces = face_cascade.detectMultiScale(gray, 1.1, 4)
#
#         # Draw the rectangle around each face
#         for (x, y, w, h) in faces:
#
#             # face_crop = np.copy(gray[y:h, x:w])
#             #
#             # face_crop = cv2.resize(face_crop, (224,224))
#             # face_crop = face_crop.astype('float')/255.0
#             # face_crop = img_to_array(face_crop)
#             # face_crop = np.expand_dims(face_crop, axis = 0)
#             #
#             # face_crop_age = cv2.resize(face_crop, (150,150))
#             # face_crop_age = face_crop_age.astype('float')/255.0
#             # face_crop_age = img_to_array(face_crop_age)
#             # face_crop_age = np.expand_dims(face_crop_age, axis = 0)
#             #
#             # face_crop1 = cv2.resize(face_crop, (197,197))
#             # face_crop1 = face_crop1.astype('float')/255.0
#             # face_crop1 = img_to_array(face_crop1)
#             # face_crop1 = np.expand_dims(face_crop1, axis = 0)
#
#             conf1 = age.predict(img)[0]
#             conf2 = gender.predict(img)[0]
#             conf3 = emotion.predict(img)[0]
#             idx1 = np.argmax(conf1)
#             idx2 = np.argmax(conf2)
#             idx3 = np.argmax(conf3)
#
#             label_age = classes_age[idx1]
#             label_gender = classes_gender[idx2]
#             label_emotion = classes_emotion[idx3]
#             label = "{},{},{}".format(label_gender,label_age, label_emotion)
#             Y = y - 10 if y - 10 > 10 else y + 10
#             cv2.putText(img,label, (x, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
#             yield 1
#             yield 2
#             yield 3
#
#         # Display
#         # yield img
#         cv2.imshow('img', img)
#
#         # Stop if escape key is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     #
#     # # Release the VideoCapture object
#     # cap.release()
#
# def y():
#     while True:
#         one = 0
#         two = 0
#         three = 0
#         tmp = x()
#         for i in range(3):
#             if i == 0:
#                 one = next(tmp)
#             elif i == 1:
#                 two = next(tmp)
#             elif i == 2:
#                 three = next(tmp)
#
#
#         print(one, two, three)
#         break
# y()
# x()
#
# cap.release()
