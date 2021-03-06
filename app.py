from tokenize import Number
from numpy import testing
from numpy.lib.type_check import imag
import pygame, sys
from pygame import image
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2
from tensorflow.python.keras.backend import constant

WINDOWSIZEX = 640
WINDOWSIZEY = 480
BOUNDRYINC = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

IMAGESAVE = False
MODEL = load_model('bestmodel.h5')
PREDICT = True
LABEL = {0:'0', 1:'1',
        2:'2', 3:'3',
        4:'4', 5:'5',
        6:'6', 7:'7',
        8:'8', 9:'9'}

# initialize our pygame
pygame.init()

FONT = pygame.font.Font('freesansbold.ttf', 18)
DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))
WHITE_INT = DISPLAYSURF.map_rgb(WHITE)
pygame.display.set_caption('WhiteBoard')
iswriting = False

number_xcord = []
number_ycord = []

image_cnt = 1



while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == MOUSEMOTION and iswriting:
            xcord, ycord = event.pos
            pygame.draw.circle(DISPLAYSURF, WHITE, (xcord, ycord), 4, 0)

            number_xcord.append(xcord)
            number_ycord.append(ycord)

        if event.type == MOUSEBUTTONDOWN:
            iswriting = True

        if event.type == MOUSEBUTTONUP:
            iswriting = False
            number_xcord = sorted(number_xcord)
            number_ycord = sorted(number_ycord)
            
            rect_min_x, rect_max_x = max(number_xcord[0]-BOUNDRYINC, 0), min(WINDOWSIZEX, number_xcord[-1]+BOUNDRYINC)
            rect_min_y, rect_max_y = max(0, number_ycord[0]-BOUNDRYINC), min(number_ycord[-1]+BOUNDRYINC, WINDOWSIZEY)

            number_xcord = []
            number_ycord = []

            img_arr = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)

            if IMAGESAVE:
                #cv2.imwrite('image.png')
                cv2.imwrite("images/image-{%d}.png" % image_cnt, img_arr)
                image_cnt += 1
            
            if PREDICT:
                image = cv2.resize(img_arr, (28,28))
                image = np.pad(image, (10,10), 'constant', constant_values = 0)
                image = cv2.resize(image, (28,28))/WHITE_INT

                label = str(LABEL[np.argmax(MODEL.predict(image.reshape((1,28,28,1))))]).title()

                textSurface = FONT.render(label, True, RED, WHITE)
                textRecObj = textSurface.get_rect()
                textRecObj.left, textRecObj.bottom = rect_min_x, rect_min_y

                DISPLAYSURF.blit(textSurface, textRecObj)
            
        if event.type == KEYDOWN:
            if event.unicode == 'n':
                DISPLAYSURF.fill(BLACK)

    pygame.display.update()
            
