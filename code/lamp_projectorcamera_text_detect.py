import cv2
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import time


def main():

    print("[INFO] starting video stream...")

    # for webcam use
    #vs = VideoStream(src=0).start()

    # for usb camera use
    vs = VideoStream(src=1).start()

    time.sleep(1.0)

    # start the FPS throughput estimator
    fps = FPS().start()

    # loop over frames from the video stream
    while True:

        # grab the current frame
        frame = vs.read()

        # check to see if we have reached the end of the stream
        if frame is None:
            break

        # resize the frame, maintaining the aspect ratio
        frame = imutils.resize(frame, width=1000)
        orig = frame.copy()

        # update the FPS counter
        fps.update()

        # show the output frame
        cv2.imshow("Text Detection", orig)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # close all windows
    cv2.destroyAllWindows()

    return


if __name__ == '__main__':
    main()