import time
import cv2
from colorthief import ColorThief
import numpy as np


def getAverageColorOfVideo():
    # get image
    vidcap = cv2.VideoCapture('OnePiece.mp4')
    success, image = vidcap.read()
    count = 0
    f = open("file.txt", "a")

    # Removed all data from file
    f.seek(0)
    f.truncate()

    # duration = vidcap.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    total = frame_count / 24
    x = total / 100
    seconds = 0

    while success:
        # resize image (for optimization)
        # output = cv2.resize(image, (100, 100))
        # save frame as JPEG file
        cv2.imwrite("frame.jpg", image)

        # print('CALCULATING COLOR...')
        # color_thief = ColorThief('frame.jpg')

        # dominant_color = color_thief.get_color(quality=10)
        # print(dominant_color)
        # f.write(str(dominant_color[0]) + ","
        #         + str(dominant_color[1]) + ","
        #         + str(dominant_color[2]) + "\n")

        # get image
        success, image = vidcap.read()
        # print('Read a new frame: ', success)

        img = cv2.imread("frame.jpg", cv2.IMREAD_UNCHANGED)
        data = np.reshape(img, (-1, 3))
        print(data.shape)
        data = np.float32(data)

        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(
            data, 1, None, criteria, 10, flags)

        b, g, r = centers[0].astype(np.int32)

        f.write(str(r) + ","
                + str(g) + ","
                + str(b) + "\n")

        print(r, g, b)
        count += 1

        if((count % 24) == 0):
            seconds = (count / 24)
            print('TOTAL:', (seconds / total)*100)

            # print(seconds / total)
            # print(round(seconds / total, 1))

    f.close()
    # OnePiece.mp4


getAverageColorOfVideo()
