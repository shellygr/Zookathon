import sqlite3

def initDB():
    try:
        conn = sqlite3.connect('photos.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE photo
            (photopath text,latitude number, longitude number, lables text, dateTaken text)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print e.message

def insertLine(path,lat,long,lables,dateTaken):
    try:
        conn = sqlite3.connect('photos.db')
        c = conn.cursor()
        args = [path,str(lat),str(long),lables,dateTaken]
        c.execute("INSERT INTO photo VALUES (?,?,?,?,?)",args)
        conn.commit()
        conn.close()
    except Exception as e:
        print e.message


def selectByLable(lable):
    try:
        conn = sqlite3.connect('photos.db')
        c = conn.cursor()
        c.execute("SELECT * FROM photo WHERE lables like ?", ["%"+lable+"%"])
        #rows = c.fetchall()
	r = [dict((c.description[i][0], value) \
               for i, value in enumerate(row)) for row in c.fetchall()]
	#print c.fetchone()
        conn.commit()
        conn.close()
	return r
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
