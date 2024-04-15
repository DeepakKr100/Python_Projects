import face_recognition
import cv2
import numpy as np 
from livenessmodel import get_liveness_model
from common import get_users
font = cv2.FONT_HERSHEY_DUPLEX

model = get_liveness_model()


model.load_weights("model/model.h5")
print("Loaded model from disk")
 
known_names, known_encods = get_users()

video_capture = cv2.VideoCapture(0)
video_capture.set(3, 640)
video_capture.set(4, 480)

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
input_vid = []

while True:
    if len(input_vid) < 24:

        ret, frame = video_capture.read()

        liveimg = cv2.resize(frame, (100,100))
        liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
        input_vid.append(liveimg)
    else:
        ret, frame = video_capture.read()

        liveimg = cv2.resize(frame, (100,100))
        liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
        input_vid.append(liveimg)
        inp = np.array([input_vid[-24:]])
        inp = inp/255
        inp = inp.reshape(1,24,100,100,1)
        pred = model.predict(inp)
        input_vid = input_vid[-25:]

        if pred[0][0]> .95:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            if process_this_frame:
                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)
                name = "Unknown"
                face_names = []
                for face_encoding in face_encodings:
                    for ii in range(len(known_encods)):

                        match = face_recognition.compare_faces([known_encods[ii]], face_encoding)

                        if match[0]:
                            name = known_names[ii]

                    face_names.append(name)

            process_this_frame = not process_this_frame

            unlock = False
            for n in face_names:

                if n != 'Unknown':
                    unlock=True

            for (top, right, bottom, left), name in zip(face_locations, face_names):

                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                
        else:
            cv2.putText(frame, 'WARNING!', (frame.shape[1]//2, frame.shape[0]//2), font, 1.0, (255, 255, 255), 1) 
        cv2.putText(frame, str(pred[0][0]), (20, 20), font, 1.0, (255, 255, 0), 1)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
video_capture.release()
cv2.destroyAllWindows()