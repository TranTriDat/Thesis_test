from flask import Flask, render_template, g,Response, request,redirect
import sqlite3
import database
import numpy as np

app = Flask(__name__)

def connection():
    conn = sqlite3.connect('thesismovies.db')
    # conn.row_factory = sqlite3.Row
    return conn

def select():
    list_movies = []
    c =connection()
    cursor = c.cursor()
    cursor.execute('select ads_path from movies ')
    items = cursor.fetchall()
    for i in items:

        list_movies.append(i)
    c.commit()
    c.close()
    return list_movies

def pyshine_process():
    # c = connection()
    # path = 'static/video/'
    list_movies = select()
    list_movies = np.array(list_movies)
    list_movies = list_movies.flatten()
    list_movies = list(list_movies)
    return list_movies
    # testlist = os.listdir(path)

    # return testlist

@app.route('/add/',methods = ['POST', 'GET'])
def add():
    con = connection()
    # if request.method == 'POST':
    ads_id = request.form['ads_id']
    ads_name = request.form['ads_name']
    ads_gender = request.form['ads_gender']
    ads_age_from = request.form['ads_age_from']
    ads_type = request.form['ads_type']
    ads_time_from = request.form['ads_time_from']
    ads_time_to = request.form['ads_time_to']
    ads_status = request.form['ads_status']
    ads_path = request.form['ads_path']

    database.add_one(ads_id, ads_name, ads_gender, ads_age_from, ads_type, ads_time_from, ads_time_to, ads_status,ads_path)

    #     msg = "Record successfully added"
    #     # con.close()
    # except:
    #     con.rollback()
    #     msg = "error in insert operation"
    # finally:
        # con.close()
    return redirect('/')

@app.route('/dele/<int:id>',methods = ['POST', 'GET'])
def dele(id):
    con = connection()
    database.delete_one(id)
    return redirect('/')

@app.route('/update/<int:id>',methods = ['POST', 'GET'])
def update(id):
    con = connection()
    ads_status = request.form['ads_status1']
    database.update_stt(ads_status,id)
    return redirect('/')

@app.route('/update_path/<int:id>',methods = ['POST', 'GET'])
def update_path(id):
    con = connection()
    ads_path = request.form['ads_path1']
    database.update_path(ads_path,id)
    return redirect('/')

# @app.route('/addrec',methods = ['POST', 'GET'])
# def addrec():
#    if request.method == 'POST':
#        return render_template("add.html")

# @app.route('/delrec',methods = ['POST', 'GET'])
# def delrec():
#    if request.method == 'POST':
#        return render_template("delete.html")

@app.route('/video_feed_1')
def video_feed_1():
	# global result
    movie = pyshine_process()
    movie = ','.join(movie)
    return movie

@app.route("/")
def home_page():
    conn = connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select * from movies order by ads_status desc, ads_id desc")
    # cursor.execute("""select * from movies where ads_age_from = 'C18' and ads_gender='Male'
    #                 order by ads_status desc""")

    rows = cursor.fetchall()
    return render_template('te.html',rows=rows)


if __name__ == '__main__':
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
    # app.run(host='192.168.1.20', debug=False,port=9999)
