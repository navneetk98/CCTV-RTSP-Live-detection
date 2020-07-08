import time
import argparse
import numpy as np
from imutils.imutils.video import FPS, VideoStream
import cv2
class MyVideoCapture:
    def __init__(self,hell,ip,usern,passw, video_source=0,):
        # Open the video source

        self.vid = cv2.VideoCapture("rtsp://"+usern+":"+passw+"@"+ip+":554/cam/realmonitor?channel=3&subtype=0")
        # self.vid = cv2.VideoCapture("videos/airport.mp4")
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        ap = argparse.ArgumentParser()
        ap.add_argument("-p", "--prototxt", required=True,
                        help="path to Caffe 'deploy' prototxt file")
        ap.add_argument("-m", "--model", required=True,
                        help="path to Caffe pre-trained model")
        ap.add_argument("-c", "--confidence", type=float, default=0.2,
                        help="minimum probability to filter weak detections")
        self.args = vars(ap.parse_args())

        # initialize the list of class labels MobileNet SSD was trained to
        # detect, then generate a set of bounding box colors for each class
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))

        # load our serialized model from disk
        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe(self.args["prototxt"], self.args["model"])

        # initialize the video stream, allow the cammera sensor to warmup,
        # and initialize the FPS counter
        print("[INFO] starting video stream...")
        self.vs = VideoStream(src=0).start()
        time.sleep(2.0)
        self.fps = FPS().start()

        # Get video source width and height
        #  self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        #  self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # self.width=

    def get_frame(self):
        frame = self.vs.read()

        frame = cv2.resize(frame, (1280, 720))


        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        self.net.setInput(blob)
        detections = self.net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > self.args["confidence"]:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(self.CLASSES[idx],
                                             confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              self.COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)



        self.fps.update()
        # Return a boolean success flag and the current frame converted to BGR
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()