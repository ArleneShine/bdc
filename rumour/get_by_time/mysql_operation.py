# coding=utf-8
"""
    mysql_operation.py

    operation for mysql
"""

import traceback
import csv
import MySQLdb
import glob
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from configs import IP, USER, PASSWORD, DB_NAME


# connect to mysql
def connect_db():
    db = MySQLdb.connect(IP, USER, PASSWORD, DB_NAME, charset='utf8mb4')
    cursor = db.cursor()
    return db, cursor


# create the table truthorfiction
def create_table():
    db, cursor = connect_db()
    sql = "CREATE TABLE truthorfiction (" \
          "Title  VARCHAR(255) NOT NULL," \
          "Date  VARCHAR(255) DEFAULT ''," \
          "Url  VARCHAR(255) NOT NULL DEFAULT ''," \
          "Summary MEDIUMTEXT," \
          "Truth LONGTEXT," \
          "Category VARCHAR(45) DEFAULT ''" \
          ");"
    cursor.execute(sql)
    db.close()


# insert one data
def insert_one_data(title, date, url, summary, truth, category):
    if not isinstance(title, unicode):
        title = unicode(title, "utf-8")
    if not isinstance(date, unicode):
        date = unicode(date, "utf-8")
    if not isinstance(url, unicode):
        url = unicode(url, "utf-8")
    if not isinstance(summary, unicode):
        summary = unicode(summary, "utf-8")
    if not isinstance(truth, unicode):
        truth = unicode(truth, "utf-8")
    if not isinstance(category, unicode):
        category = unicode(category, "utf-8")
    db, cursor = connect_db()
    sql = 'INSERT INTO truthorfiction(Title, Date, Url, Summary, Truth, Category) VALUES ' \
          '("%s", "%s", "%s", "%s", "%s", "%s");' % \
          (title.encode("utf-8"), date.encode("utf-8"), url.encode("utf-8"), summary.encode("utf-8"), truth.encode("utf-8"), category.encode("utf-8"))
    cursor.execute(sql)
    db.commit()
    db.close()


# drop the table truthorfiction
def drop_table():
    db, cursor = connect_db()
    sql = "DROP TABLE truthorfiction;"
    cursor.execute(sql)
    db.close()


# get all the title and category from table truthorfiction
def get_title_category_from_db():
    db, cursor = connect_db()
    sql = 'SELECT Title, Category from truthorfiction;'
    count = cursor.execute(sql)
    data = cursor.fetchmany(count)
    return [[_[0], _[1]] for _ in data]


if __name__ == "__main__":
    # drop_table()  # 删除数据库的truthorfiction表
    # create_table()  # 创建数据库的truthorfiction表
    count = 0
    for filename in glob.glob(r'result/*.csv'):
        lines = csv.reader(file(filename, 'rb'))
        for index, line in enumerate(lines):
            if index != 0:
                try:
                    insert_one_data(line[0], line[1], line[2], line[3], line[4], line[5])
                except:
                    traceback.print_exc()
                    with open("input_to_db_fail.csv", 'a') as f:
                        f.write('"%s","%s","%s","%s","%s","%s"\n' % (line[0], line[1],line[2], line[3],line[4], line[5]))
                count += 1
        print "---------------- %d --------------------" % count



