from numpy.core.arrayprint import str_format
import cv2
import numpy as np
from PIL import Image, ImageDraw
import time
import numexpr as ne


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


def bincount_numexpr_app(a):
    # Alternative method NOT BEING USED
    a2D = a.reshape(-1, a.shape[-1])
    col_range = (256, 256, 256)  # generically : a2D.max(0)+1
    eval_params = {'a0': a2D[:, 0], 'a1': a2D[:, 1], 'a2': a2D[:, 2],
                   's0': col_range[0], 's1': col_range[1]}
    a1D = ne.evaluate('a0*s0*s1+a1*s0+a2', eval_params)
    return np.unravel_index(np.bincount(a1D).argmax(), col_range)


def unique_count_app(a):
    # Alternative method NOT BEING USED
    colors, count = np.unique(
        a.reshape(-1, a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]


def main():
    # Get image
    vidcap = cv2.VideoCapture('OnePiece.mp4')
    count = 0

    # Video Fps
    fps = round(vidcap.get(cv2.CAP_PROP_FPS))

    # Duration = vidcap.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

    # RGB or RGBA
    # Size of window
    # Background color
    # im = Image.new('RGB', (int(frame_count / 2), 300), (255, 255, 255))
    im = Image.new('RGB', (1920, 1080), (255, 255, 255))

    while count != frame_count:
        # Get next frame
        success, image = vidcap.read()

        # Scale image down
        scale_percent = 25  # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        draw = ImageDraw.Draw(im)

        # Get Dominant R G B
        r, g, b = DominantColor(image)

        count += 1
        print(str(count) + "/" + str(frame_count), end='\r')
        # [(left_width_point, top_height_point), (right_width_point, bottom_height_point)]
        # draw.rectangle([(count / 2, 0), (count / 2, 300)], fill=(r, g, b))
        draw.rectangle(
            [((1920 * count) / frame_count, 0), ((1920 * count) / frame_count, 1080)], fill=(r, g, b))
    im.save('pillow_imagedraw.jpg', quality=100)
    im.close


main()
