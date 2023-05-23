import csv
import logging
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

     
def insert_new_model_color(in_file, out_file, car_image_dir, car_thumbnail_dir):
    #insert model color listed in in_file
    with open(in_file, "r") as input, open(out_file, "w") as output:
        csvreader = csv.reader(input)
        csvwriter = csv.writer(output)
        
        next(csvreader)
        for row in csvreader:
            manufacturer_id = row[0]
            model_id = row[2]
            color = row[4].strip()
            model = row[3].strip()
            image_url = row[5]
            fuel_capacity = row[6]

            filename = car_image_dir + model + "_" + color + ".png"
            car_image = cv2.imread(filename)
            _, buffer = cv2.imencode(".png", car_image)
            image_data = buffer.tobytes()
            print(filename)

            filename_thumbnail = car_thumbnail_dir + model + "_" + color + ".png"
            car_thumnail = cv2.imread(filename_thumbnail)
            _, buffer_thumb = cv2.imencode(".png", car_thumnail)
            thumb_data = buffer_thumb.tobytes()
            print(filename_thumbnail)


            model_id = isdb.query_model_id(model)
            if model_id:
                print(model)
                print(model_id)
                
                # print(str(color) + " " + str(model_id) + " " + str(image_url) + " " + str(manufacturer_id) + " " + str(model + " " + color))
                model_color_id = isdb.insert_model_color(color, model_id, psycopg2.Binary(image_data), image_url,manufacturer_id, model + " " + color, psycopg2.Binary(thumb_data))
                print(model_color_id)
                
                row[2] = model_id
                row.append(model_color_id)
                csvwriter.writerow(row)
            else:
                print(model)
                new_model_id = isdb.insert_model(manufacturer_id=manufacturer_id, model=model, fuel_capacity=fuel_capacity)
                print(new_model_id) 
                                
                model_color_id = isdb.insert_model_color(color, new_model_id, psycopg2.Binary(image_data), image_url,manufacturer_id, model + " " + color, psycopg2.Binary(thumb_data))
                print(model_color_id)
                
                row[2] = new_model_id
                row.append(model_color_id)
                csvwriter.writerow(row)
        

def update_model_color(resized_img_dir, thumbnail_dir, out_file):
    '''update photo and thumbnail use images in resized_img_dir, thumbnail_dir
    --Get model color name from image name'''
    with open(out_file, "w") as output:
        csvwriter = csv.writer(output)
        for r, d, f in os.walk(resized_img_dir):
            for file in f:
                try:
                    model_name = file.replace('_',' ')
                    model_name = model_name[:-4]

                    car_image = cv2.imread(os.path.join(r, file))
                    _, buffer = cv2.imencode(".png", car_image)
                    image_data = buffer.tobytes()
                    # print(car_img_bytes)

                    car_thumnail = cv2.imread(os.path.join(thumbnail_dir, file))
                    _, buffer_thumb = cv2.imencode(".png", car_thumnail)
                    thumb_data = buffer_thumb.tobytes()
                    
                    model_color_id = isdb.update_model_color(model_name, image_data, thumb_data)
                    csvwriter.writerow([model_name, model_color_id, 'Success']) 
                except Exception as e:
                    logging.warning('error read file ' + file)
                    print(e)
                    csvwriter.writerow([file,'', 'Fail']) 

   
if __name__ == '__main__':
    update_model_color('./update_car_image/car_images_resized', './update_car_image/car_thumbnail', './update_car_image/output.txt')
    # insert_new_model_color('./Crawl_xe_prod.csv','./result_insert_prod.csv', './car_images_resized_png/', './car_thumbnail_png/')

    # for r, d, f in os.walk('./car_images_resized_png'):
    #         for file in f:
    #             try:
    #                 model_name = file.replace('_',' ')
    #                 model_name = model_name[:-4]
    #                 print(model_name)
    #             except Exception as e:
    #                 print(e)
