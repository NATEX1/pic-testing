import pymysql 

# host="147.50.254.12",
# user="finorfin_pic",
# password="G5F&2!taRct9sdyv",
# database="pic_2",
# cursorclass=pymysql.cursors.DictCursor

def get_conn():
    return pymysql.connect(
        host="147.50.254.12",
        user="finorfin_pic",
        password="G5F&2!taRct9sdyv",
        database="pic_2",
        cursorclass=pymysql.cursors.DictCursor
    )
    
def query(sql, params=None):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def execute(sql, params=None):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    conn.commit()
    cursor.close()
    conn.close()

def fetch_one(sql, params=None):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row