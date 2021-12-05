import cv2
from colorthief import ColorThief


def getAverageColorOfVideo():
    # get image
    vidcap = cv2.VideoCapture('OnePiece.mp4')
    success, image = vidcap.read()
    count = 0
    f = open("file.txt", "a")

    # Removed all data from file
    f.seek(0)
    f.truncate()

    while success:
        # resize image (for optimization)
        # output = cv2.resize(image, (100, 100))
        # save frame as JPEG file
        cv2.imwrite("frame.jpg", image)

        print('CALCULATING COLOR...')
        color_thief = ColorThief('frame.jpg')
        dominant_color = color_thief.get_color(quality=10)
        print(dominant_color)
        f.write(str(dominant_color[0]) + ","
                + str(dominant_color[1]) + ","
                + str(dominant_color[2]) + "\n")

        # get image
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1
    f.close()


getAverageColorOfVideo()
