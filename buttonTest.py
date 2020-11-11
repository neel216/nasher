import cv2

# button dimensions (y1,y2,x1,x2)
y1 = 464 - 50
y2 = y1 + 40
x1 = 116
x2 = x1 + 200
button = [y1, y2, x1, x2]

# function that handles the mousclicks
def process_click(event, x, y, flags, params):
    # check if the click is within the dimensions of the button
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseX, mouseY = x, y
        if mouseY > button[0] and mouseY < button[1] and mouseX > button[2] and mouseX < button[3]:
            print('Picture taken!')

# create a window and attach a mousecallback and a trackbar
cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', process_click)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 464) # 320
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 464) # 180

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    frame[button[0]:button[1], button[2]:button[3]] = 180
    cv2.putText(frame, 'Take Picture', (x2 - 200, y2), cv2.FONT_HERSHEY_PLAIN, 2, (0), 3)
    cv2.imshow('Camera', frame)
    
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(mouseX, mouseY)

cam.release()
cv2.destroyAllWindows()