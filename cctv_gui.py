import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from VideoCap import MyVideoCapture
import time

class App:
    def __init__(self, window, window_title,ip,usern,passw, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.vid = MyVideoCapture(self.video_source,ip,usern,passw)
        self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=1280, height=720)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        frame = self.vid.get_frame()
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)
def runn(self):
    App(tkinter.Tk(), "CCTV object detection")

class login:
    def __init__(self):
        self.r = tkinter.Tk()
        self.r.geometry('400x200+10+20')

        self.r.title('CCTV Login')

        self.number1 = tkinter.StringVar()
        self.number2 = tkinter.StringVar()
        self.number3 = tkinter.StringVar()

        labelNum1 = tkinter.Label(self.r, text="IP").grid(row=1, column=0)
        labelNum2 = tkinter.Label(self.r, text="Username").grid(row=2, column=0)
        labelNum3 = tkinter.Label(self.r, text="Password").grid(row=3, column=0)


        entryNum1 = tkinter.Entry(self.r, textvariable=self.number1).grid(row=1, column=2)
        entryNum2 = tkinter.Entry(self.r, textvariable=self.number2).grid(row=2, column=2)
        entryNum2 = tkinter.Entry(self.r,show="*", textvariable=self.number3).grid(row=3, column=2)

        button = tkinter.Button(self.r, text='Login', width=25, command=self.dest).grid(row=4, column=0)
        # button.pack()
        self.r.mainloop()
    def dest(self):
        self.r.destroy()
        ip=self.number1.get()
        user=self.number2.get()
        passw=self.number3.get()

        App(tkinter.Tk(), "CCTV object detection",ip,user,passw)


login()