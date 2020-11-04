import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    print('On Raspberry Pi')
    import os
    import time
    os.system("sudo modprobe bcm2835-v4l2")
    rpi = True
except ImportError:
    print('Not on Raspberry Pi')
    rpi = False

class Camera:
    def __init__(self, parent, menu, mainMenu, nextPage):
        self.camera = tk.Frame(master=parent)
        self.camera.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #camera.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
        self.camera.place(in_=parent, x=0, y=0, relwidth=1, relheight=1)
        self.mainMenu = mainMenu
        self.nextPage = nextPage
        self.menu = menu


        restart = ttk.Button(self.camera, text='Restart', command=self.hide)
        restart.grid(row=0, column=0, sticky='w')

        self.lmain = tk.Label(self.camera)
        self.lmain.grid(row=1, column=0)

        if rpi:
            print('[INFO] Loading Raspberry Pi Camera')
            self.camera_ = PiCamera()
            print('[INFO] Raspberry Pi Camera Initialized')
            #self.camera_.resolution = (464, 464)
            print('[INFO] Raspberry Pi Camera Resolution set')
            self.camera_.framerate = 32
            print('[INFO] Raspberry Pi Camera FPS set')
            self.rawCapture = PiRGBArray(self.camera_)
            print('[INFO] Raspberry Pi Camera Raw Capture set')

            '''
            print('[INFO] Loaded camera')
            self.cap = cv2.VideoCapture(0)
            print('[INFO] Setting camera resolution')
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 464)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 464)
            '''

        else:
            pass
            '''
            print('[INFO] Loaded camera')
            self.cap = cv2.VideoCapture(0)
            print('[INFO] Setting camera resolution')
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 464)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 464)

        takePicture = ttk.Button(self.camera, text='Take Picture', command=self.mainMenu.capture_image)
        takePicture.grid(row=2, column=0)
        '''
        takePicture = ttk.Button(self.camera, text='Open Camera', command=self.video_stream)
        takePicture.grid(row=2, column=0)

        self.camera.grid_columnconfigure(0, weight=1)
        self.camera.grid_rowconfigure(2, weight=1)

    def video_stream(self):
        if rpi:
            for image in self.camera_.capture_continuous(self.rawCapture, format='bgr', use_video_port=True):
                img = image.array
                self.frame = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
                cv2.imshow("Camera", self.frame)

                self.rawCapture.truncate(0)

                k = cv2.waitKey(1)
                if k % 256 == 32:
                    # SPACE pressed
                    print('Picture taken!')
                    break
            cv2.waitKey(1)
            cv2.destroyAllWindows()
            for i in range (1,5):
                cv2.waitKey(1)
            self.mainMenu.capture_image()
            return
        else:
            '''
            ok, self.frame = self.cap.read()  # read frame from video stream
            if ok:  # frame captured without any errors
                #self.frame = cv2.flip(frame, 1)
                cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
                img = Image.fromarray(cv2image)  # convert image for PIL
                img.thumbnail((464, 464), Image.ANTIALIAS)
                imgtk = ImageTk.PhotoImage(image=img)  # convert image for tkinter
                self.lmain.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
                self.lmain.configure(image=imgtk)  # show the image

            self.lmain.after(10, self.video_stream)
            '''
            print('[INFO] Loaded camera')
            self.cap = cv2.VideoCapture(0)
            print('[INFO] Setting camera resolution')
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 464)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 464)

            while True:
                ok, self.frame = self.cap.read()  # read frame from video stream
                cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Camera",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
                cv2.imshow("Camera", self.frame)
                
                
                k = cv2.waitKey(1)
                if k % 256 == 32:
                    # SPACE pressed
                    print('Picture taken!')
                    break
            cv2.waitKey(1)
            cv2.destroyAllWindows()
            for i in range (1,5):
                cv2.waitKey(1)
            self.mainMenu.capture_image()
            return

    def get_picture(self):
        return self.frame

    def show(self):
        self.camera.lift()
    
    def hide(self):
        self.menu.lift()