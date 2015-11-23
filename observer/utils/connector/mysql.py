import MySQLdb
from django.conf import settings


class mysql():
    def __init__(self, type=''):
        self.type = type

    def open(self):
        if not self.type:
            mysql_conn = settings.MYSQL_CONN_STR_DEFAULT
            return MySQLdb.connect(
                mysql_conn['host'],
                mysql_conn['username'],
                mysql_conn['password'],
                mysql_conn['name'],
                charset='utf8')
        else:
            return MySQLdb.connect(
                    '192.168.1.101',
                    'root',
                    '123456',
                    'yqj2',
                    charset='utf8')


def query(sql, llist=[]):
    db = mysql().open()
    cursor = db.cursor()
    cursor.execute(sql, llist)
    result = cursor.fetchall()

    db.commit()
    db.close()
    return result


# return []
def query_one(sql='', llist=[], user='', confname=''):
    if not user:
        db = mysql().open()
        cursor = db.cursor()
        cursor.execute(sql, llist)
    else:
        db = mysql('conf').open()
        cursor = db.cursor()
        sql = """SELECT VALUE FROM settings WHERE user_id=(SELECT id FROM yqj_user WHERE 
            username=%s) AND NAME=%s"""
        cursor.execute(sql, [user, confname])
    result = cursor.fetchone()[0]

    db.commit()
    db.close()
    return result


# return row (int)number
def save(sql, llist=[]):
    db = mysql().open()
    cursor = db.cursor()
    try:
        result = cursor.execute(sql, llist)
        db.commit()
        return result
    except:
        print "mysql save fail"
        db.rollback()
        return None
    db.close()


# if __name__ == '__main__':
    # sql = "insert into demo value(null,%s,%s)"
    # print sql
    # query()
    # n = save(sql,["xin1","pwd1"])
    # print n
    # sql = "select * from demo where pwd = %s"
    # l = query_one(sql,["pwd1"])
    # if l:
    #     print l[0],l[1],l[2]
        # for x in range(len(l)):
        #     print l[x][0],l[x][1],l[x][2]
    # else:
    #     print l
