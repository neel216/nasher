import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    import time
    rpi = False
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
            self.camera_.resolution = (464, 464)
            print('[INFO] Raspberry Pi Camera Resolution set')
            self.camera_.framerate = 32
            print('[INFO] Raspberry Pi Camera FPS set')
            self.rawCapture = PiRGBArray(self.camera_, size=self.camera_.resolution)
            print('[INFO] Raspberry Pi Camera Raw Capture set')
        else:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 464)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 464)

        takePicture = ttk.Button(self.camera, text='Take Picture', command=self.mainMenu.capture_image)
        takePicture.grid(row=2, column=0)

        self.camera.grid_columnconfigure(0, weight=1)
        self.camera.grid_rowconfigure(2, weight=1)

        print('[INFO] Raspberry Pi Camera Camera loaded')
        self.video_stream()

    def video_stream(self):
        if rpi:
            print('[INFO] Loading Raspberry Pi Camera video stream')
            for frame in self.camera_.capture_continuous(self.rawCapture, format='bgr', use_video_port=True):
                image = frame.array
                cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                img.thumbnail((464, 464), Image.ANTIALIAS)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lmain.imgtk = imgtk
                self.lmain.configure(image=imgtk)
                self.lmain.after(10, self.video_stream)
                self.rawCapture.truncate(0)
        else:
            _, self.frame = self.cap.read()
            #self.frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            img.thumbnail((464, 464), Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lmain.imgtk = imgtk
            self.lmain.configure(image=imgtk)
            self.lmain.after(10, self.video_stream)

    def get_picture(self):
        #self.cap.release()
        #cv2.destroyAllWindows()
        return self.frame

    def show(self):
        self.camera.lift()
    
    def hide(self):
        self.menu.lift()