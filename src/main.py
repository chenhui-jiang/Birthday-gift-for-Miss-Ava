import threading
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# predefined variable
multiple = 10  # the multiple time of picture, use to control the size of output picture
timeDelay = 0.1  # time delay to control the speed of printing article

'''
use to draw the avatar image by the words in UTF-8 format
path: the origin file path
words: the words from file
target: target file path
'''
def drawThePicture(path, words, target):
    # define the font of word in picture
    font = ImageFont.truetype("simsun.ttc", multiple, encoding="UTF-8")
    # open the image
    avatar = Image.open(path)
    # find the RGB value of each pixel
    array = np.array(avatar)
    # create the target file, let the background color white
    target_avatar = Image.new("RGB", (len(array) * multiple, len(array[0]) * multiple), color=(255, 255, 255))
    # create the drawer
    draw = ImageDraw.Draw(target_avatar)
    # locate the word position
    word_pos = 0
    for i in range(0, len(array)):
        # print(i, '/', len(array), " done\n")
        for j in range(0, len(array[0])):
            # skip the white area
            if tuple(array[i][j]) == (255, 255, 255):
                continue
            word_pos += 1
            draw.text((multiple * j, multiple * i), words[word_pos % len(words)], font=font,
                      fill=tuple(array[i][j]))
    # save the target file
    target_avatar.save(target + '\\target.jpg')

'''
use to print the article by constant time delay, the time you can adjust in the begining of code
words: the word read from file
'''
def delayPrint(words):
    # counter for the new line
    counter = 0
    for w in words:
        time.sleep(timeDelay)
        print(w, end="")
        counter += 1
        if (counter >= 40 or w == '\n'):
            print()
            counter = 0


if __name__ == '__main__':
    # read the word from file
    article_path = '..\\input\\article\\ava.txt'  # the file path of article
    origin_image_path = '..\\input\\picture\\ava.jpg'  # the file path of origin image
    target_image_path = '..\\output'  # the file path of target image
    words = open(article_path, encoding="UTF-8").read()
    # start multithreading
    # first thread print the article by a const time delay
    t1 = threading.Thread(target=delayPrint, args=(words,))
    # second thread do the convert job and draw the target picture
    t2 = threading.Thread(target=drawThePicture, args=(origin_image_path, words, target_image_path))

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
