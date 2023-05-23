import cv2
import os
from os import listdir
from os.path import isfile, join
import logging
import numpy as np

def find_white_background(imgArr, threshold=0.4):
    """remove images with transparent or white background"""
    background = np.array([255, 255, 255])
    percent = (imgArr == background[0]).sum() / imgArr.size
    if percent >= threshold:
        print(percent)
        return True
    else:
        return False

def check_color_space_and_transparent(img):
    if (len(img[0,0]) == 4 and img[0,0][3] == 0):
        return 1
    elif (len(img[0,0]) == 4 and img[0,0][0] == 255 and img[0,0][1] == 255 and img[0,0][2] == 255 and img[0,0][3] == 255 ):
        return 2
    else:
        return 3

def resize_images_in_dir(input_dir, resized_img_dir, thumbnail_dir):
    '''Resize all image in input_dir to width < 500 -> save to resized_img_dir
    then resize to ratio 0.5 -> save to thumbnail_dir'''
    for r, d, f in os.walk(input_dir):
        for file in f:
            try:
                img = cv2.imread(os.path.join(r, file), cv2.IMREAD_UNCHANGED)
                ratio = 1
                (h, w, d) = img.shape
                if w > 500:
                    ratio = 500/w
                dim = (int(w*ratio), int(h*ratio))
                resized = cv2.resize(img, dim)
                cv2.imwrite(os.path.join(resized_img_dir, file), resized)   
                
                (resized_h, resized_w, resized_d) = resized.shape
                dim = (int(resized_w*0.5), int(resized_h*0.5))
                thumb = cv2.resize(resized, dim)
                cv2.imwrite(os.path.join(thumbnail_dir, file), thumb) 
            except Exception as e:
                logging.warning('error read file ' + file)
                print(e)
                
if __name__ == '__main__':
    resize_images_in_dir('./update_car_image/input_images', './update_car_image/car_images_resized', './update_car_image/car_thumbnail')

def crop_and_resize_image(input_img_dir, resized_dir, output_img_dir):
    '''Crop and resize images in input_img_dir, then save to resized_dir.
        Then continue resizing 50%, then save to output_img_dir'''
    thisdir = os.getcwd()
    input_img_dir = "./input_images"
    resized_dir = "./car_images_resized_png"
    output_img_dir = "./car_thumbnail_png"

    # r=root, d=directories, f = files
    for r, d, f in os.walk(input_img_dir):
        count = 1
        for file in f:
            try:
                img = cv2.imread(os.path.join(r, file), cv2.IMREAD_UNCHANGED)
                #4 channel and transparent
                if (len(img[0,0]) == 4 and img[0,0][3] == 0):
                    a, b, c, img_transpraent = cv2.split(img)                
                    ret, thresh = cv2.threshold(img_transpraent, 1, 255, 0)

                    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    for c in contours:
                        rect = cv2.boundingRect(c)
                        if rect[2] < 100 or rect[3] < 100:
                            continue
                        else:
                            break
                    x, y, w, h = rect
                    dst = img[y:y+h, x:x+w]

                    #change background 
                    trans_mask = dst[:,:,3] == 0
                    dst[trans_mask] = [255, 255, 255, 50]
                    dst = cv2.cvtColor(dst, cv2.COLOR_BGRA2BGR)
                    
                    #resize
                    ratio = 1
                    (h, w, d) = dst.shape
                    if w > 500:
                        ratio = 500/w
                    dim = (int(w*ratio), int(h*ratio))
                    resized = cv2.resize(dst, dim)
                    cv2.imwrite(os.path.join(resized_dir, file), resized)   
                    
                    (resized_h, resized_w, resized_d) = resized.shape
                    dim = (int(resized_w*0.5), int(resized_h*0.5))
                    thumb = cv2.resize(resized, dim)
                    cv2.imwrite(os.path.join(output_img_dir, file), thumb) 
                #4 channel and white background
                elif (len(img[0,0]) == 4 and img[0,0][0] == 255 and img[0,0][1] == 255 and img[0,0][2] == 255 and img[0,0][3] == 255 ):
                    tmp = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
                    ret, thresh = cv2.threshold(tmp, 1, 255, 0)
                    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    for c in contours:
                        rect = cv2.boundingRect(c)
                        if rect[2] < 100 or rect[3] < 100:
                            continue
                        else:
                            break
                    x, y, w, h = rect
                    dst = img[y:y+h, x:x+w]
                    
                    #resize
                    ratio = 1
                    (h, w, d) = dst.shape
                    if w > 500:
                        ratio = 500/w
                    dim = (int(w*ratio), int(h*ratio))
                    resized = cv2.resize(dst, dim)
                    cv2.imwrite(os.path.join(resized_dir, file), resized)   
                    
                    (resized_h, resized_w, resized_d) = resized.shape
                    dim = (int(resized_w*0.5), int(resized_h*0.5))
                    thumb = cv2.resize(resized, dim)
                    cv2.imwrite(os.path.join(output_img_dir, file), thumb) 
                # 3 channels and white background
                else:                
                    tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    _,threshed = cv2.threshold(tmp,240,255,cv2.THRESH_BINARY_INV)
                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
                    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
                    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                    cnt = sorted(cnts, key=cv2.contourArea)[-1]
                    x,y,w,h = cv2.boundingRect(cnt)
                    dst = img[y:y+h, x:x+w]
                    
                    #resize
                    ratio = 1
                    (h, w, d) = dst.shape
                    if w > 500:
                        ratio = 500/w
                    dim = (int(w*ratio), int(h*ratio))
                    resized = cv2.resize(dst, dim)
                    cv2.imwrite(os.path.join(resized_dir, file), resized)   
                    
                    (resized_h, resized_w, resized_d) = resized.shape
                    dim = (int(resized_w*0.5), int(resized_h*0.5))
                    thumb = cv2.resize(resized, dim)
                    cv2.imwrite(os.path.join(output_img_dir, file), thumb) 
                
            except Exception as e:
                logging.warning('error read file ' + file)
                print(e)

# img = cv2.imread("desktop.webp", cv2.IMREAD_UNCHANGED)
#             #4 channel and transparent
# if check_color_space_and_transparent(img) == 1:
#     a, b, c, img_transpraent = cv2.split(img)                
#     ret, thresh = cv2.threshold(img_transpraent, 1, 255, 0)
#     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     for c in contours:
#         rect = cv2.boundingRect(c)
#         if rect[2] < 100 or rect[3] < 100:
#             continue
#         else:
#             break
#     x, y, w, h = rect
#     dst = img[y:y+h, x:x+w]   
#     #resize
#     ratio = 1
#     (h, w, d) = dst.shape
#     if w > 500:
#         ratio = 500/w
#     dim = (int(w*ratio), int(h*ratio))
#     resized = cv2.resize(dst, dim)
    
#     trans_mask = resized[:,:,3] == 0
#     resized[trans_mask] = [252, 252, 252, 100]
#     resized = cv2.cvtColor(resized, cv2.COLOR_BGRA2BGR)

#     cv2.imwrite("desktop_out.png", resized)
    
# #4 channel and white background
# elif check_color_space_and_transparent(img) == 2:
#     print('Anh 4 gia tri '+ "Ford Ranger XLS_Black")
#     # whitePixels = np.all(img[...,:3] == (255, 255, 255), axis=-1)
#     # img[whitePixels,3] = 0
#     # alpha_channel = img[:,:,3]
#     tmp = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
#     ret, thresh = cv2.threshold(tmp, 1, 255, 0)
#     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     for c in contours:
#         rect = cv2.boundingRect(c)
#         if rect[2] < 100 or rect[3] < 100:
#             continue
#         else:
#             break
#     x, y, w, h = rect

#     dst = img[y:y+h, x:x+w]
#     # cv2.imwrite(os.path.join(resized_dir, file), dst)
    
#     #resize
#     ratio = 1
#     (h, w, d) = dst.shape
#     if w > 500:
#         ratio = 500/w
#     dim = (int(w*ratio), int(h*ratio))
#     resized = cv2.resize(dst, dim)
#     cv2.imwrite("Ford Ranger XLS_Black_out.png", resized)   
    
#     (resized_h, resized_w, resized_d) = resized.shape
#     dim = (int(resized_w*0.5), int(resized_h*0.5))
#     thumb = cv2.resize(resized, dim)
#     cv2.imwrite("Ford Ranger XLS_Black_out_thumb.png", thumb) 
# # 3 channels and white background
# else:                
#     tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     _,threshed = cv2.threshold(tmp,240,255,cv2.THRESH_BINARY_INV)
#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
#     morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
#     cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
#     cnt = sorted(cnts, key=cv2.contourArea)[-1]
#     x,y,w,h = cv2.boundingRect(cnt)
#     dst = img[y:y+h, x:x+w]
#     # cv2.imwrite(os.path.join(resized_dir, file), dst)    
    
#     #resize
#     ratio = 1
#     (h, w, d) = dst.shape
#     if w > 500:
#         ratio = 500/w
#     dim = (int(w*ratio), int(h*ratio))
#     resized = cv2.resize(dst, dim)
#     cv2.imwrite("Ford Ranger XLS_Black_out.png", resized)   
    
#     (resized_h, resized_w, resized_d) = resized.shape
#     dim = (int(resized_w*0.5), int(resized_h*0.5))
#     thumb = cv2.resize(resized, dim)
#     cv2.imwrite("Ford Ranger XLS_Black_out_thumb.png", thumb) 
            