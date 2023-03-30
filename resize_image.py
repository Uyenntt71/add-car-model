import cv2
import os
from os import listdir
from os.path import isfile, join
import logging

# Getting the current work directory (cwd)
thisdir = os.getcwd()
input_img_dir = "./car_images_png"
output_img_dir = "./car_thumbnail_png"
# r=root, d=directories, f = files
for r, d, f in os.walk(input_img_dir):
    count = 1
    for file in f:
        # if (file.endswith(".png") or file.endswith(".jpg")  or file.endswith(".jpeg")):
        # print(os.path.join(r, file))
        try:
            img = cv2.imread(os.path.join(r, file), cv2.IMREAD_UNCHANGED)
            (h, w, d) = img.shape
            print(count)
            print(file)
            print("width={}, height={}, depth={}".format(w, h, d))
            count = count + 1
            
            # #crop img
            # imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # ret, thresh = cv2.threshold(imgray, 1, 255, 0)
            # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # for c in contours:
            #     rect = cv2.boundingRect(c)
            #     if rect[2] < 100 or rect[3] < 100:
            #         continue
            #     else:
            #         break
            # x, y, w, h = rect

            # cv2.rectangle(img, (rect[0], rect[1]),  (rect[0] + rect[2], rect[1] + rect[3]),  (0,255,0), 3)
            # img = img[y:y+h, x:x+w]
            # (h, w, d) = img.shape
            # print("width={}, height={}, depth={}".format(w, h, d))
           

            
            # resize img
            ratio = 0.25 
            dim = (int(w * ratio), int(h * ratio))
            resized = cv2.resize(img, dim)
            (h1, w1, d1) = resized.shape
            print("width={}, height={}, depth={}".format(w1, h1, d1))
            # print(os.path.join(output_img_dir, file).replace(" ", "\\ "))
            cv2.imwrite(os.path.join(output_img_dir, file), resized)
            
        except Exception as e:
            logging.warning('error read file ' + file)
            print(e)
            