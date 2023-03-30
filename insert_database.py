#!/usr/bin/python
import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insert_model(manufacturer_id, model, fuel_capacity):
    """ insert a new model into the model table """
    sql = """INSERT INTO model (manufacturer_id, model, fuel_capacity)
            VALUES (%s, %s, %s)
            RETURNING id
            ;""" 
            # % {"manufacturer_id": manufacturer_id, "model": model, "fuel_capacity":fuel_capacity}
    conn = None
    model_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (manufacturer_id, str(model), fuel_capacity))
        # get the generated id back
        model_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print(model_id)
    return model_id

def insert_model_color(color, model_id, photo_bin, photo, manufacturer_id, name, photo_thumbnail):
    """ insert a new model into the model table """
    sql = """INSERT INTO model_color (color, model_id, photo_bin, photo, manufacturer_id, name, photo_thumbnail) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            ;"""  
            # % {"color": color, "model_id": model_id, "photo_bin":photo_bin, "photo":photo, "manufacturer_id":manufacturer_id, "name":name, "photo_thumbnail":photo_thumbnail }
    print(sql)
    conn = None
    model_color_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (str(color), model_id, photo_bin, str(photo), manufacturer_id, str(name), photo_thumbnail))
        # get the generated id back
        model_color_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print(model_color_id)
    return model_color_id

# if __name__ == '__main__':
#     insert_model(15, 'Mitsubishi Zinger 1', 65)

