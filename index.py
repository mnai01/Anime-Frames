from numpy.core.arrayprint import str_format
import cv2
import numpy as np
from PIL import Image, ImageDraw
import time


def Progress(count, fps, frame_count, start):
    # Calculate progress of frames left
    if((count % fps) == 0):
        seconds = (count / fps)

    # Display how much time is left to finish every 5 frames
    if((count % 5) == 0):

        # Calculate total time to finish (rough estimate)
        if(count == 5):
            totalTime = (frame_count * (time.time() - start)) / 5

        timeElapsed = time.time() - start
        print(str(timeElapsed) + " seconds out of " + str(totalTime) + " seconds " +
              "PERCENTAGE COMPLETE: " + str((seconds / total)*100), end='\r')


def DominantColor(image):
    # Get Dominate color in scene
    data = np.reshape(image, (-1, 3))
    # print(data.shape)
    data = np.float32(data)
    criteria = (cv2.TERM_CRITERIA_EPS +
                cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(
        data, 1, None, criteria, 10, flags)
    b, g, r = centers[0].astype(np.int32)
    return r, g, b


def main():
    # Get image
    vidcap = cv2.VideoCapture('OnePiece.mp4')
    count = 0

    # Video Fps
    fps = round(vidcap.get(cv2.CAP_PROP_FPS))

    # Duration = vidcap.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    total = frame_count / fps
    seconds = 0

    # RGB or RGBA
    # Size of window
    # Background color
    im = Image.new('RGB', (int(frame_count / 2), 300), (255, 255, 255))

    start = time.time()
    totalTime = 0.0

    while count != frame_count:
        # Get next frame
        success, image = vidcap.read()

        draw = ImageDraw.Draw(im)

        # Get Dominant R G B
        r, g, b = DominantColor(image)

        Progress(count, fps, frame_count, start)

        count += 1

        # [(left_width_point, top_height_point), (right_width_point, bottom_height_point)]
        draw.rectangle([(count / 2, 0), (count / 2, 300)], fill=(r, g, b))
        im.save('pillow_imagedraw.jpg', quality=100)


main()
