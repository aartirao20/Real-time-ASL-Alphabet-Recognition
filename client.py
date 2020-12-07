import cv2
import socket
import struct
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 9999))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 1280) #width
cam.set(4, 720) #height
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    result, frame1 = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame1, 0)
    size = len(data)
    client_socket.sendall(struct.pack(">L", size) + data)
    pred_recv = client_socket.recv(1024)
    text = pred_recv.decode("utf-8")
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, (200, 90), font, 0.75, (0, 255, 255), 2, cv2.LINE_4)
    tl_x = 175
    tl_y = 50
    br_x = 900
    br_y = 700
    cv2.rectangle(frame, (tl_x, tl_y), (br_x, br_y), (0, 255, 0), 2)
    cv2.imshow('ImageWindow', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()


