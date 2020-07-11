import sqlite3


def establish_connection():
    # connecting to the database
    connection = sqlite3.connect("database/settings.db")
    # cursor
    crsr = connection.cursor()

    return connection, crsr


def close_connection(connection):
    # To save the changes in the files. Never skip this.
    # If we skip this, nothing will be saved in the database.
    connection.commit()

    # close the connection
    connection.close()


def create_table():

    try:
        connection, crsr = establish_connection()

        # SQL command to create a table in the database
        sql_command = """CREATE TABLE IF NOT EXISTS settings (  
        id INTEGER PRIMARY KEY,  
        source_image_path VARCHAR(250) DEFAULT '',  
        output_image_path VARCHAR(250) DEFAULT '',
        dlib_model VARCHAR (50) DEFAULT 'shape_predictor_68_face_landmarks.dat',
        output_video_path VARCHAR(250) DEFAULT '',
        save_image SMALLINT(1) DEFAULT 0, 
        save_video SMALLINT(1) DEFAULT 0, 
        settings_save_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP );"""

        # execute the statement
        crsr.execute(sql_command)
        #
        # sql_command = """INSERT OR REPLACE INTO settings
        # (id, source_image_path, output_image_path, dlib_model, output_video_path, save_image, save_video  )
        # VALUES (1, ?,?, ?, ?,?,?);"""
        #
        # crsr.execute(sql_command, ("", "", "shape_predictor_68_face_landmarks.dat", "", 0, 0))

        close_connection(connection)

        return True

    except Exception as e:
        print(e)
        return False


def create_record(face_location_path_value, image_output_dir_path_value, dlibmodel,video_output_dir_path_value,
                  saveimage, savevideo):

    try:
        connection, crsr = establish_connection()

        # SQL command to insert the data in the table
        sql_command = """INSERT OR REPLACE INTO settings
        (id, source_image_path, output_image_path, dlib_model, output_video_path, save_image, save_video  ) 
        VALUES (1, ?,?, ?, ?,?,?);"""

        crsr.execute(sql_command, (face_location_path_value, image_output_dir_path_value, dlibmodel,
                                   video_output_dir_path_value, saveimage, savevideo))

        close_connection(connection)

        return True

    except Exception as e:
        return False


def fetch_settings():
    connection, crsr = establish_connection()

    # execute the command to fetch all the data from the table emp
    crsr.execute("SELECT * FROM settings")

    # store all the fetched data in the ans variable
    result = crsr.fetchall()

    if len(result) == 0:
        print('inside')
        create_record("", "", "shape_predictor_68_face_landmarks.dat", "", 0, 0)

    crsr.execute("SELECT * FROM settings")
    result = crsr.fetchall()
    print(result)
    close_connection(connection)

    result = result[0]
    print(result)
    source_image_path, output_image_path, dlib_model, output_video_path, save_image, save_video = \
        result[1], result[2], result[3], result[4], result[5], result[6]

    print(source_image_path, output_image_path, dlib_model, output_video_path, save_image, save_video)
    return (source_image_path, output_image_path, dlib_model, output_video_path, save_image, save_video)
