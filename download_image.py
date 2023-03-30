import requests
import logging
import csv


def download_image(model, color , url):
    
    filename = 'input_images/' + model + "_" + color + ".png"
    # + url[url.rindex('/'):]
    print(url)
    print(filename)
    with open(filename, 'wb') as handle:
        try:
            response = requests.get(url, stream=True, timeout=10)
            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
        except requests.exceptions.ConnectTimeout as e:
            logging.error("Time out!")
            
filename = "Crawl_xe_dev.csv"
with open(filename, "r") as csvfile:
    csvreader = csv.reader(csvfile)

    next(csvreader)

    for row in csvreader:
        color = row[4]
        model = row[3]
        image = row[5]

        download_image(model=model, color=color, url=image)