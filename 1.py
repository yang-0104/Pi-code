import cv2
import numpy

print('now starting to send frames...')
capture=cv2.VideoCapture(0) #VideoCapture对象，可获取摄像头设备的数据
print(capture)