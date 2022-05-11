from numpy.core.arrayprint import str_format
import cv2
import numpy as np
from PIL import Image, ImageDraw
import time
import numexpr as ne
import os
from imdb import Cinemagoer
import csv
import json


def DominantColor(image):
    # Get Dominate color in scene
    data = np.reshape(image, (-1, 3))
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


def ConvertVideo(video_path, imageFolder):
    parentFolder, videoName = video_path.split('\\')
    # Get image
    vidcap = cv2.VideoCapture(video_path)
    count = 0

    # Video Fps
    fps = round(vidcap.get(cv2.CAP_PROP_FPS))

    # Duration = vidcap.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

    frameWidth = 2048
    frameHeight = 2048

    # RGB or RGBA
    # Size of window
    # Background color
    im = Image.new('RGB', (frameWidth, frameHeight), (255, 255, 255))

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
        draw.rectangle(
            [((frameWidth * count) / frame_count, 0), ((frameWidth * count) / frame_count, frameHeight)], fill=(r, g, b))
    im.save(f"{os.getcwd()}\{imageFolder}\{videoName}.jpg", quality=100)
    im.close


def GetVideoInfo(imdbCode, jsonObj, imagePath):
    temp = {}
    temp['genres'] = []
    temp['directors'] = []

    ia = Cinemagoer()
    movie = ia.get_movie(str(imdbCode))
    temp['name'] = movie['title']
    try:
        for genre in movie['genres']:
            temp['genres'].append(genre)
    except KeyError:
        print(f"genre is unknown.")

    try:
        for director in movie['directors']:
            temp['directors'].append(
                # Needed for special foreign names
                # director['name'].replace('ô', "o")
                director['name'])
    except KeyError:
        print(f"director is unknown.")

    temp['rating'] = movie['rating']
    temp['plot'] = str(" ".join(movie['plot']).split('::', 1)[0])
    temp["image"] = imagePath

    print(temp)
    jsonObj.append(temp)


def WriteToCSV():
    check_dir(os.getcwd() + "\\" + 'VideoData.csv')
    with open('VideoData.csv', newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in rows:
            print(', '.join(row))


def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# HAD TO BE HARDCODED
folderName = "videos"
jsonObj = {"nft": []}

for filename in os.listdir(os.getcwd() + "\\" + folderName):
    imageFolder = folderName + "-Barcodes"
    check_dir(f"{os.getcwd()}\{imageFolder}")
    ConvertVideo(f"{folderName}\{filename}", imageFolder)

    try:
        imdbCode, season, ep = filename.split('-')
    except:
        imdbCode, extension = filename.split('.')
    GetVideoInfo(imdbCode, jsonObj['nft'],
                 f"{os.getcwd()}\{imageFolder}\{filename}.jpg")

# json_string = json.dumps(jsonObj)
with open('json_data.json', 'w') as outfile:
    json.dump(jsonObj, outfile)
