"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import time

import cv2
from gaze_tracking import GazeTracking
import serial

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
ser = serial.Serial('COM4', 9600, timeout=1)
while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    try:
        gaze.refresh(frame)
    except:
        pass

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
        ser.write(b'S')
        time.sleep(0.5)
        pass
    elif gaze.is_right():
        text = "Looking right"
        ser.write(b'R')
        time.sleep(0.5)
        pass
    elif gaze.is_left():
        text = "Looking left"
        ser.write(b'L')
        time.sleep(0.5)
        pass
    elif gaze.is_center():
         text = "Looking center"
         ser.write(b'F')
         time.sleep(0.5)
         pass
    else:
        text = "Not looking"
        ser.write(b'S')
        time.sleep(0.5)
        pass
    print(text)



    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(33) == ord('a') :
        break
ser.close()
webcam.release()
cv2.destroyAllWindows()