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
    images = []

    # RGB or RGBA
    # Size of window
    # Background color
    im = Image.new('RGB', (int(frame_count / 2), 300), (255, 255, 255))

    start = time.time()
    totalTime = 0.0

    while count != frame_count:
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

        count += 1

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

        # Create new image
        im = Image.new('RGB', (int(frame_count / 2),
                               int(frame_count / 2)), (255, 255, 255))

        # Get center
        center = int(frame_count / 2) // 2

        # Draw Image
        draw = ImageDraw.Draw(im)
        draw.ellipse((center - count / 2, center - count / 2, center +
                      count / 2, center + count / 2), fill=(r, g, b))

        # Append image to array
        images.append(im)

        # Get next frame
        success, image = vidcap.read()

    # Create gif with images array
    images[0].save('pillow_imagedraw.gif',
                   save_all=True, append_images=images[1:], optimize=True, duration=20, loop=0)


getAverageColorOfVideo()
