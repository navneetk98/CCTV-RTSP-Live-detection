import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from VideoCap import MyVideoCapture
import time


# class SampleApp(tkinter.Tk):
#     def __init__(self):
#         tkinter.Tk.__init__(self)
#         self._frame = None
#         self.switch_frame(StartPage)
#
#     def switch_frame(self, frame_class):
#         new_frame = frame_class(self)
#
#         self._frame.destroy()
#         self._frame = new_frame
#         self._frame.pack()
#
# class StartPage(tkinter.Frame):
#     def __init__(self, master):
#         tkinter.Frame.__init__(self, master)
#         tkinter.Label(self, text="Start page", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
#         tkinter.Button(self, text="Go to page one",
#                   command=lambda: master.switch_frame(App(master, "CCTV object detection"))).pack()


class App:
    def __init__(self, window, window_title,ip,usern,passw, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.vid = MyVideoCapture(self.video_source,ip,usern,passw)

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

# class MyVideoCapture:
#     def __init__(self, video_source=0):
#         # Open the video source
#         self.vid = cv2.VideoCapture("rtsp://2:infrared@192.168.1.240:554/cam/realmonitor?channel=1&subtype=0")
#         if not self.vid.isOpened():
#             raise ValueError("Unable to open video source", video_source)
#         ap = argparse.ArgumentParser()
#         ap.add_argument("-p", "--prototxt", required=True,
#                         help="path to Caffe 'deploy' prototxt file")
#         ap.add_argument("-m", "--model", required=True,
#                         help="path to Caffe pre-trained model")
#         ap.add_argument("-c", "--confidence", type=float, default=0.2,
#                         help="minimum probability to filter weak detections")
#         self.args = vars(ap.parse_args())
#
#         # initialize the list of class labels MobileNet SSD was trained to
#         # detect, then generate a set of bounding box colors for each class
#         self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
#                         "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
#                         "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
#                         "sofa", "train", "tvmonitor"]
#         self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
#
#         # load our serialized model from disk
#         print("[INFO] loading model...")
#         self.net = cv2.dnn.readNetFromCaffe(self.args["prototxt"], self.args["model"])
#
#         # initialize the video stream, allow the cammera sensor to warmup,
#         # and initialize the FPS counter
#         print("[INFO] starting video stream...")
#         self.vs = VideoStream(src=0).start()
#         time.sleep(2.0)
#         self.fps = FPS().start()
#
#         # Get video source width and height
#         #  self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
#         #  self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
#         # self.width=
#
#     def get_frame(self):
#         frame = self.vs.read()
#         frame = cv2.resize(frame, (1280, 720))
#         # frame=imutils.
#         # frame = imutils.resize(frame, width=400)
#
#         # grab the frame dimensions and convert it to a blob
#         (h, w) = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
#                                      0.007843, (300, 300), 127.5)
#
#         # pass the blob through the network and obtain the detections and
#         # predictions
#         self.net.setInput(blob)
#         detections = self.net.forward()
#
#         # loop over the detections
#         for i in np.arange(0, detections.shape[2]):
#             # extract the confidence (i.e., probability) associated with
#             # the prediction
#             confidence = detections[0, 0, i, 2]
#
#             # filter out weak detections by ensuring the `confidence` is
#             # greater than the minimum confidence
#             if confidence > self.args["confidence"]:
#                 # extract the index of the class label from the
#                 # `detections`, then compute the (x, y)-coordinates of
#                 # the bounding box for the object
#                 idx = int(detections[0, 0, i, 1])
#                 box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                 (startX, startY, endX, endY) = box.astype("int")
#
#                 # draw the prediction on the frame
#                 label = "{}: {:.2f}%".format(self.CLASSES[idx],
#                                              confidence * 100)
#                 cv2.rectangle(frame, (startX, startY), (endX, endY),
#                               self.COLORS[idx], 2)
#                 y = startY - 15 if startY - 15 > 15 else startY + 15
#                 cv2.putText(frame, label, (startX, y),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)
#
#         # if the `q` key was pressed, break from the loop
#
#         self.fps.update()
#         # Return a boolean success flag and the current frame converted to BGR
#         return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#         # if self.vid.isOpened():
#         #     ret, frame = self.vid.read()
#         #     frame = cv2.resize(frame, (1920, 1080))
#         #     if ret:
#         #         # Return a boolean success flag and the current frame converted to BGR
#         #         return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#         #     else:
#         #         return (ret, None)
#         # else:
#         #     return (ret, None)
#
#     # Release the video source when the object is destroyed
#     def __del__(self):
#         if self.vid.isOpened():
#             self.vid.release()


# Create a window and pass it to the Application object

# App(tkinter.Tk(), "CCTV object detection")
class login:
    def __init__(self):
        # self.r = tkinter.Tk()
        # number1 = tkinter.StringVar()
        # self.r.title('CCTV Login')
        # w = tkinter.Label(self.r, text='Enter Details')
        # w.pack()
        # self.name_var = tkinter.StringVar()
        # name_entry = tkinter.Entry(self.r,
        #                       textvariable=self.name_var, font = ('calibre', 10, 'normal'))
        # name_entry.pack()
        # # self.fld=tkinter.Entry(self.r, text)
        # # self.fld.pack()
        self.r = tkinter.Tk()
        self.r.geometry('400x200+10+20')

        self.r.title('CCTV Login')

        self.number1 = tkinter.StringVar()
        self.number2 = tkinter.StringVar()
        self.number3 = tkinter.StringVar()

        labelNum1 = tkinter.Label(self.r, text="IP").grid(row=1, column=0)
        labelNum2 = tkinter.Label(self.r, text="Username").grid(row=2, column=0)
        labelNum3 = tkinter.Label(self.r, text="Password").grid(row=3, column=0)

        # labelResult = tkinter.Label(self.r)
        #
        # labelResult.grid(row=7, column=2)

        entryNum1 = tkinter.Entry(self.r, textvariable=self.number1).grid(row=1, column=2)
        entryNum2 = tkinter.Entry(self.r, textvariable=self.number2).grid(row=2, column=2)
        entryNum2 = tkinter.Entry(self.r, textvariable=self.number3).grid(row=3, column=2)

        # call_result = partial(call_result, labelResult, number1, number2)
        #
        # buttonCal = tk.Button(root, text="Calculate", command=call_result).grid(row=3, column=0)

        # self.r.mainloop()
        button = tkinter.Button(self.r, text='Login', width=25, command=self.dest).grid(row=4, column=0)
        # button.pack()
        self.r.mainloop()
    def dest(self):
        self.r.destroy()
        ip=self.number1.get()
        user=self.number2.get()
        passw=self.number3.get()
        print(ip)
        print(user)
        print(passw)
        App(tkinter.Tk(), "CCTV object detection",ip,user,passw)


login()