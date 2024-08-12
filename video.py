import cv2

# 创建窗口
#cv2.namedWindow('Window', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
#（可自由改变大小）

cap=cv2.VideoCapture(0)
#摄像头ID号默认值为-1，表示随机选取一个摄像头。如果你运行该程序的设备有多个摄像头，则用0表示设备的第一个摄像头，1表示设备的第二个摄像头，依次类推。

i=0
while(1):
    ret ,frame = cap.read()
    k=cv2.waitKey(1)
    if k==27:           #按下ESC退出窗口
        break
    elif k==ord('s'):   #按下s保存图片
        cv2.imwrite('/home/pi/Desktop'+str(i)+'.jpg',frame)
        i+=1
    cv2.imshow("capture", frame)
cap.release()
cv2.destroyAllWindows()
