from tokenize import Number
import pygame ,sys
from pygame import image
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2

WINDOWSSIZEX=640
WINDOWSSIZEY=480
White=(255,255,255)
black=(0,0,0)
Red=(255,0,0)
BOUNDRYINC=5
Imagesave=False
Model=load_model("models.h5")
Labels={0:"Zero",1:"One",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine"}
#INITIALIZE OUR PYGAMES
pygame.init()
DISPLAYSURF=pygame.display.set_mode((WINDOWSSIZEX,WINDOWSSIZEY))
Font = pygame.font.Font('freesansbold.ttf', 18)
pygame.display.set_caption("Digit Board")
iswriting=False
number_xcord=[]
number_ycord=[]
image_cnt =1
PREDICT=True
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION and iswriting:
            xcord,ycord=event.pos
            pygame.draw.circle(DISPLAYSURF,White,(xcord,ycord),4,0)
            number_xcord.append(xcord)
            number_ycord.append(ycord)
        if event.type == MOUSEBUTTONDOWN:
            iswriting=True
        if event.type== MOUSEBUTTONUP:
            iswriting=False
            number_xcord=sorted(number_xcord)
            number_ycord=sorted(number_ycord)

            rect_min_x,rect_max_x=max(number_xcord[0] - BOUNDRYINC,0),min(WINDOWSSIZEX,number_xcord[-1]+BOUNDRYINC)
            rect_min_y,rect_max_y=max(number_ycord[0] - BOUNDRYINC,0),min(number_ycord[-1]+BOUNDRYINC,WINDOWSSIZEY)
            number_xcord=[]
            number_ycord=[]

            img_arr=np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x,rect_min_y:rect_max_y].T.astype(np.float32)
            if Imagesave:
                cv2.imwrite("image.png",img_arr)
                image_cnt +=1
            if PREDICT:
                image=cv2.resize(img_arr,(28,28))
                image=image/255.0
                prediction=Model.predict(image.reshape(1,28,28,1))
                Label=str(Labels[np.argmax(prediction)])
                textSurface=Font.render(Label,True,Red,White)
                textRecobj=textSurface.get_rect()
                textRecobj.left,textRecobj.bottom=rect_min_x,rect_max_y

                DISPLAYSURF.blit(textSurface,textRecobj)#bilt() is use to  display the object
            if event.type == KEYDOWN:
                if event.unicode =="n":
                    DISPLAYSURF.fill(black)
        pygame.display.update()