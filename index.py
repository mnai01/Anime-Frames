from numpy.core.arrayprint import str_format
import cv2
import numpy as np
from PIL import Image, ImageDraw
import time


def getAverageColorOfVideo():
    # Get image
    vidcap = cv2.VideoCapture('OnePiece.mp4')
    success, image = vidcap.read()
    count = 0
    f = open("file.txt", "a")

    # Video Fps
    fps = round(vidcap.get(cv2.CAP_PROP_FPS))

    # Removed all data from file
    f.seek(0)
    f.truncate()

    # Duration = vidcap.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    total = frame_count / fps
    seconds = 0

    # Color array
    videoColors = []

    # RGB or RGBA
    # Size of window
    # Background color
    im = Image.new('RGB', (int(frame_count / 2), 300), (255, 255, 255))

    start = time.time()
    totalTime = 0.0

    while count != frame_count:
        draw = ImageDraw.Draw(im)

        # save frame as JPEG file
        cv2.imwrite("frame.jpg", image)

        # Get Dominate color in scene
        img = cv2.imread("frame.jpg", cv2.IMREAD_UNCHANGED)
        data = np.reshape(img, (-1, 3))
        # print(data.shape)
        data = np.float32(data)
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(
            data, 1, None, criteria, 10, flags)
        b, g, r = centers[0].astype(np.int32)

        # Write RGB to file
        f.write(str(r) + ","
                + str(g) + ","
                + str(b) + "\n")

        # Append RGB object to array
        videoColors.append({r, g, b})

        count += 1

        # Calculate progress of frames left
        if((count % fps) == 0):
            seconds = (count / fps)
            print('TOTAL:', (seconds / total)*100)

        # Display how much time is left to finish every 5 frames
        if((count % 5) == 0):

            # Calculate total time to finish (rough estimate)
            if(count == 5):
                totalTime = (frame_count * (time.time() - start)) / 5

            print(totalTime)
            timeElapsed = time.time() - start
            print(str(timeElapsed) + " seconds out of " +
                  str(totalTime) + " seconds")

        # [(left_width_point, top_height_point), (right_width_point, bottom_height_point)]
        draw.rectangle([(count / 2, 0), (count / 2, 300)], fill=(r, g, b))
        im.save('pillow_imagedraw.jpg', quality=100)

        # Get next frame
        success, image = vidcap.read()
    f.close()


getAverageColorOfVideo()
