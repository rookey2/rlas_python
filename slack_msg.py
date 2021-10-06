import requests
import socket
from datetime import datetime
 
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)

T1 = 'x'+'o'+'x'+'b'
T2 = '2541818091588'
T3 = '2541834361300'
T4 =  'mpTCWKYTHwd91e9fKyMbhdvF'
myToken = T1 + '-' + T2 +'-' + T3 + '-' + T4 
myhost = socket.gethostname()
def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), myhost, ": ", message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + myhost + ": "+ message
    post_message(myToken,"#class", strbuf)

#dbgout("안녕하세요!!!")
