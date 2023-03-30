import csv
import insert_database as isdb
import cv2
import os
import psycopg2

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

     

# insert img into database
filename = "Crawl_xe_dev.csv"
car_image_dir = './car_images_resized_png/'
car_thumbnail_dir = './car_thumbnail_png/' 
with open(filename, "r") as csvfile:
    csvreader = csv.reader(csvfile)

    next(csvreader)
    row = next(csvreader)
    
    # for row in csvreader:
    manufacturer_id = row[0]
    model_id = row[2]
    color = row[4]
    model = row[3]
    image_url = row[5]
    fuel_capacity = row[6]
    
    filename = car_image_dir + model + "_" + color + ".png"
    car_image = cv2.imread(filename)
    _, buffer = cv2.imencode(".png", car_image)
    image_data = buffer.tobytes()
    # print(car_img_bytes)
    
    filename_thumbnail = car_thumbnail_dir + model + "_" + color + ".png"
    car_thumnail = cv2.imread(filename_thumbnail)
    _, buffer_thumb = cv2.imencode(".png", car_thumnail)
    thumb_data = buffer_thumb.tobytes()
    print(model_id)    
    #insert new model and model color
    if (model_id == ''):
        new_model_id = isdb.insert_model(manufacturer_id=manufacturer_id, model=model, fuel_capacity=fuel_capacity)
        print(new_model_id)
        
        # with open(filename, 'rb') as f:
        #     car_image = f.read()
        #     car_img_bytes = psycopg2.Binary(car_image)
        #     with open(filename_thumbnail, 'rb') as ft:
        #         car_thumnail = ft.read()
        #         car_thumb_bytes = psycopg2.Binary(car_image)
        #         print(str(color) + " " + str(new_model_id) + " " + str(image_url) + " " + str(manufacturer_id) + " " + str(model + " " + color))
        #         model_color_id = isdb.insert_model_color(color, new_model_id, car_img_bytes, image_url,manufacturer_id, model + " " + color, car_thumb_bytes)
        #         print(model_color_id)
                
        print(str(color) + " " + str(new_model_id) + " " + str(image_url) + " " + str(manufacturer_id) + " " + str(model + " " + color))
        model_color_id = isdb.insert_model_color(color, new_model_id, psycopg2.Binary(image_data), image_url,manufacturer_id, model + " " + color, psycopg2.Binary(thumb_data))
        print(model_color_id)
    #insert only model color
    else:
        print(str(color) + " " + str(model_id) + " " + str(image_url) + " " + str(manufacturer_id) + " " + str(model + " " + color))
        model_color_id = isdb.insert_model_color(color, model_id, psycopg2.Binary(image_data), image_url,manufacturer_id, model + " " + color, psycopg2.Binary(thumb_data))
        print(model_color_id)

