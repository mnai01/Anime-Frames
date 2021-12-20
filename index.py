import cv2
from colorthief import ColorThief


def getAverageColorOfVideo():
    # Get image
    vidcap = cv2.VideoCapture('OnePiece.mp4')
    success, image = vidcap.read()
    count = 0
    f = open("file.txt", "a")

    # Removed all data from file
    f.seek(0)
    f.truncate()

    frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    total = frame_count / 24
    seconds = 0

    while success:
        # Save frame as JPEG file
        cv2.imwrite("frame.jpg", image)

        # Init color theif with frame
        color_thief = ColorThief('frame.jpg')

        # Find dominant color
        dominant_color = color_thief.get_color(quality=10)
        print(dominant_color)
        r, g, b = str(dominant_color[0]), str(
            dominant_color[1]), str(dominant_color[2])

        # Write rgb to file
        f.write(r + "," + g + "," + b + "\n")
        print(r, g, b)
        count += 1

        # Calculate Progress of frames left
        if((count % 24) == 0):
            seconds = (count / 24)
            print('TOTAL:', (seconds / total)*100)

        # get image
        success, image = vidcap.read()

    f.close()
    # OnePiece.mp4


getAverageColorOfVideo()
