import cv2
import os
from os import listdir
from os.path import isfile, join
import requests
import logging
import csv




# print(cv2.__version__)

# read and show img
# img = cv2.imread('desktop.webp')
# cv2.imshow('Display Image', img)
# cv2.waitKey(0)

#show image size
# (h, w, d) = img.shape
# print("width={}, height={}, depth={}".format(w, h, d))

#resize image
# r = 300.0 / w 
# dim = (300, int(h * r))
# resized = cv2.resize(img, dim)
# (h, w, d) = resized.shape
# print("width={}, height={}, depth={}".format(w, h, d))



#download img from url
def download_image(model, color , url):
    filename = 'input_images/' + model + "_" + color
    # + url[url.rindex('/'):]
    with open(filename, 'wb') as handle:
        try:
            response = requests.get(url, stream=true, timeout=10)
        except requests.exceptions.ConnectTimeout as e:
            logging.error("Time out!")
        finally:
            # continue request here
        # response = requests.get(url, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

#download image from url list
# filename = "Crawl_xe.csv"
# with open(filename, "r") as csvfile:
#     csvreader = csv.reader(csvfile)

#     next(csvreader)

#     for row in csvreader:
#         color = row[4]
#         model = row[3]
#         image = row[5]

#         download_image(model=model, color=color, url=image)

# Getting the current work directory (cwd)
# thisdir = os.getcwd()
input_img_dir = "./input_images"
output_img_dir = "./output_images"
# r=root, d=directories, f = files
for r, d, f in os.walk(input_img_dir):
    count = 1
    for file in f:
        # if (file.endswith(".png") or file.endswith(".jpg")  or file.endswith(".jpeg")):
        # print(os.path.join(r, file))
        try:
            img = cv2.imread(os.path.join(r, file))
            (h, w, d) = img.shape
            print(count)
            print(file)
            print("width={}, height={}, depth={}".format(w, h, d))
            count = count + 1
            
            #resize img
            ratio = 150 / w 
            dim = (150, int(h * ratio))
            resized = cv2.resize(img, dim)
            (h1, w1, d1) = resized.shape
            print("width={}, height={}, depth={}".format(w1, h1, d1))
            # print(os.path.join(output_img_dir, file).replace(" ", "\\ "))
            cv2.imwrite(os.path.join(output_img_dir, file) + ".png", resized)
            
        except Exception as e:
            logging.warning('error read file ' + file)
            print(e)
            