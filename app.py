import cv2
from keras.models import load_model
from slack_msg import dbgout
import numpy as np

## 이미지 전처리
def preprocessing(frame):
    # 크기 조정
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)

    # 이미지 정규화
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))

    return frame_reshaped

## 학습된 모델 불러오기
model = load_model('converted_keras/keras_model.h5')

# 카메라 캡처 객체, 0=내장 카메라
capture = cv2.VideoCapture(0)

# 캡처 프레임 사이즈 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
dbgout("시작합니다")
sleep_cnt = 1 # 30초간 "졸림" 상태를 확인하기 위한 변수
while True:
    ret, frame = capture.read()
    if ret == True:
        print("read success!")

    # 이미지 뒤집기
    frame_fliped = cv2.flip(frame, 1)

    # 이미지 출력
    cv2.imshow("VideoFrame", frame_fliped)

    # 1초마다 검사하며, videoframe 창으로 아무 키나 누르게 되면 종료
    if cv2.waitKey(200) > 0:
        break

    # 데이터 전처리
    preprocessed = preprocessing(frame_fliped)

    # 예측
    prediction = model.predict(preprocessed)
    #print(prediction) # [[0.00533728 0.99466264]]
    state = "깨어있는 상태"
    message = "60초간 졸고 있네요!!!"

    if prediction[0,0] < prediction[0,1]:
        #print('졸림 상태')
        sleep_cnt += 1

        # 졸린 상태가 60초간 지속되면 소리 & 카카오톡 보내기
        if state == '깨어있는 상태' and sleep_cnt % 60 == 0:
            sleep_cnt = 1
            state = '졸림 상태'
            print(message)
            dbgout(message)
            # beepsound()
            # send_music_link()
            # break ## 1번만 알람이 오면 프로그램을 정지 시킴 (반복을 원한다면, 주석으로 막기!)
    else:
        state = "깨어있는 상태"
        print('깨어있는 상태')
        sleep_cnt = 1

# 카메라 객체 반환
capture.release()
# 화면에 나타난 윈도우 창을 종료
cv2.destroyAllWindows()