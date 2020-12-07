import socket
import sys
import cv2
import pickle
import numpy as np
import struct
from tensorflow import keras
model = keras.models.load_model("C:\\Users\\aarti\\OneDrive\\Desktop\\Quarter 4\\Real time intelligent systems\\asl_cnn_model")

HOST = 'localhost'
PORT = 9999
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')
s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')
conn, addr = s.accept()

data = b""
payload_size = struct.calcsize(">L")
while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    tl_x = 175
    tl_y = 50
    br_x = 900
    br_y = 700
    sign_img = frame[tl_y:br_y, tl_x:br_x]
    gray_img = cv2.cvtColor(sign_img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(gray_img, (28,28))
    img_norm = img / 255
    img_3d = img_norm.reshape(-1,28,28,1)
    prediction = model.predict_classes(img_3d)
    if prediction[0] >= 9:
        pred = prediction[0]+1
    else:
        pred = prediction[0]
    pred_letter = chr(ord('@')+(pred+1))
    text = "Predicted Letter: " + pred_letter

    conn.sendall(bytes(str(text), "utf-8"))
