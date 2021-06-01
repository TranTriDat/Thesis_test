import sqlite3
import numpy as np
import os,time
from fuzzywuzzy import fuzz,process
import re
conn = sqlite3.connect("thesismovies.db")
cursor = conn.cursor()

video_path = os.listdir('static/video')
# print(video_path)
# cursor.execute(""" create table movies(
#     ads_id interger not null primary key,
#     ads_name text not null,
#     ads_gender text not null,
#     ads_age_from text not null,
#     ads_type text,
#     ads_time_from text,
#     ads_time_to text,
#     ads_path text)""")

def find_path_for_name(ads_name):
    path = ads_name
    path = process.extractOne(path, video_path)
    path = list(path)
    p=path[0].split("_")
    return p[0]
# print(find_path_for_name('Gundam Hathaway'))
def find_path(ads_name):
    path = ads_name
    path = process.extractOne(path, video_path)
    path = list(path)
    return path[0]

# ads_path = find_path()
# cursor.execute('''Insert into movies values(?,?,?,?,?,?,?,?)''',
#                 (1,find_path_for_name('Gundam Hathaway'),'Male','C13','Anime','2021','2021', find_path('Gundam Hathaway')))
# path = '../statics/video/'
# name = "Gundam Hathaway"
# cursor.execute("select * from movies where ads_name like ?",('%'+name+'%',))
# cursor.execute("select max(ads_id) from movies")

# items = cursor.fetchall()
# a = list(items)
# print(type(a[0][0]))
# a[0] = list(a[0])
# print(type(a[0]),a[0][0])
# items = np.array(items)
# items = np.array_split(items,len(items))
# print(items[0], path)
# for item in items:
    # print(item)
    # print(item[0] + '\t' + item[1] + '\t' + item[2])
# b = re.sub('watch?v=','embed/',a[0][0])
# b = a[0][0].replace('watch?v=','embed/')
# print(b)
# cursor.execute("update movies set ads_status=?",(1,))
# print("Command executed successfully...")
# conn.commit()
# conn.close()

def show_all():
    # order by
    # cursor.execute("select rowid,* from customers order by rowid desc")

    # cursor.execute("select rowid,* from customers where last_name like 'Br%' and rowid=3")
    # conn.commit()

    cursor.execute("select rowid,* from movies ")

    items = cursor.fetchall()

    for item in items:
        print(item)
        # print(item[0] + '\t' + item[1] + '\t' + item[2])

    print("Command executed successfully...")
    # commit command
    conn.commit()

    # close connection
    conn.close()

def add_one(ads_id, ads_name, ads_gender, ads_age_from, ads_type, ads_time_from, ads_time_to,ads_status,ads_path):
    conn = sqlite3.connect("thesismovies.db")
    # path_new = ads_path.split('/')
    ads_path = ads_path.replace('watch?v=','embed/')
    # create cursor
    cursor = conn.cursor()
    cursor.execute("Insert into movies values(?,?,?,?,?,?,?,?,?)",
                    (ads_id, ads_name, ads_gender, ads_age_from, ads_type, ads_time_from, ads_time_to, ads_path, ads_status))
    conn.commit()
    conn.close()

def delete_one(ads_id):
    conn = sqlite3.connect("thesismovies.db")

    # create cursor
    cursor = conn.cursor()
    cursor.execute("delete from movies where ads_id=?",(ads_id,))

    # cursor.execute("delete from movies where ads_name like ?",('%'+find_path_for_name(ads_name)+'%',))
    conn.commit()
    conn.close()

def update_stt(ads_status,ads_id):
    conn = sqlite3.connect("thesismovies.db")

    # create cursor
    cursor = conn.cursor()
    cursor.execute("update movies set ads_status =? where ads_id=?",(ads_status,ads_id,))

    # cursor.execute("delete from movies where ads_name like ?",('%'+find_path_for_name(ads_name)+'%',))
    conn.commit()
    conn.close()

def update_path(ads_path,ads_id):
    conn = sqlite3.connect("thesismovies.db")
    ads_path = ads_path.replace('watch?v=','embed/')
    # create cursor
    cursor = conn.cursor()
    cursor.execute("update movies set ads_path =? where ads_id=?",(ads_path,ads_id,))

    # cursor.execute("delete from movies where ads_name like ?",('%'+find_path_for_name(ads_name)+'%',))
    conn.commit()
    conn.close()

# update_stt(2,36)
# print("Command executed successfully...")
# conn.commit()
# conn.close()
# add_one(2,'Sailor Moon Eternal','Female','C13','Anime','2021','2021')
#
# cursor.execute("select rowid,* from movies ")
#
# items = cursor.fetchall()
#
# for item in items:
    # print(item)
# print("Command executed successfully...")
#
# conn.commit()
# conn.close()
# def add_many(list):
#     conn = sqlite3.connect("customer.db")
#
#     # create cursor
#     cursor = conn.cursor()
#     cursor.executemany("insert into customers values (?,?,?)",(list))
#     conn.commit()
#     conn.close()
