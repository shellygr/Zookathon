import sqlite3

def initDB():
    try:
        conn = sqlite3.connect('photos.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE photo
            (photopath text,latitude text, longitude text, lables text)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print e.message

def insertLine(path,lat,long,lables):
    try:
        conn = sqlite3.connect('photos.db')
        c = conn.cursor()
        args = [path,str(lat),str(long),lables]
        c.execute("INSERT INTO photo VALUES (?,?,?,?)",args)
        conn.commit()
        conn.close()
    except Exception as e:
        print e.message


def selectByLable(lable):
    try:
        conn = sqlite3.connect('photos.db')
        c = conn.cursor()
        c.execute("SELECT * FROM photo WHERE lables like ?", ["%"+lable+"%"])
        print c.fetchone()
        conn.commit()
        conn.close()
    except Exception as e:
        print e.message

def clearTable():
    try:
        conn = sqlite3.connect('photos.db')
        c = conn.cursor()
        c.execute("DELETE FROM photo")
        conn.commit()
        conn.close()
    except Exception as e:
        print e.message
