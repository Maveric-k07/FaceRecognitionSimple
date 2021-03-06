import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'ImagesBasic'
images = []
personName = []
myList = os.listdir(path)

for curImg in myList:
    currentImage = cv2.imread(f'{path}/{curImg}')
    images.append(currentImage)
    personName.append(os.path.splitext(curImg)[0])
print(personName)

def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}')


encodeListKnown = faceEncodings(images)
print("Encoding complete")

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurrent = face_recognition.face_locations(imgS)
    encodeCurrent = face_recognition.face_encodings(imgS, facesCurrent)

    for encodeFace, faceLoc in zip(encodeCurrent, facesCurrent):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDistance)
        matchIndex = np.argmin(faceDistance)

        if matches[matchIndex]:
            name = personName[matchIndex].upper()
            #print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35),(x2, y2), (0, 255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
