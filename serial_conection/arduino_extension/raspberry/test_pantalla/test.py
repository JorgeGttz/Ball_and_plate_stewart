import numpy as np
import cv2

wall_paper = cv2.imread('pantalla_itcg.jpg')
ctr =(500,500)
cv2.circle(wall_paper,ctr,10,(255,0,0),20)
cv2.imshow('Ball and Plate ITCG',wall_paper)
key = cv2.waitKey(0)
cv2.destroyAllWindows()
