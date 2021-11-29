
import numpy as np
import cv2
import time

def user_register_function():

    cap = cv2.VideoCapture(0)                         # from camera
    FPS = cap.get(cv2.CAP_PROP_FPS)  # Frame Per Second
    F_Count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # frame count
    print(f'FPS : {FPS:.2f} ms, Frame_Count : {F_Count}')
    count=0
    count_limit=10#截取圖片張數
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        #frame = cv2.flip(frame, 1)  # left side right
        c = cv2.waitKey(30)  # 25 ms per frame     1/FPS


        #cv2.putText(frame, '123', (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imwrite(f'./resources/frame_{count}.jpg', frame)  # save frame as JPEG file
        print(f'save image : frame_{count}.jpg')
        count += 1
        time.sleep(0.3)
        if (not ret or c == 27 )or (count>count_limit):
            break

        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)