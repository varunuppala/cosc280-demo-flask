from flask import Flask,render_template, request, redirect
import pymysql
from config import conn_details as config

conn = pymysql.connect(host = config['host'], user = config['user'],
            password = config['password'], db = config['db_name'])


app = Flask(__name__)

@app.route('/')
def mainpage():
    return render_template('mainpage.html')

@app.route('/ShowSinger')
def Singer():

    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Singer;")
    
    rows = []
    for row in cursor.fetchall():
        rows.append({"id": row[0], "FirstName": row[1], "LastName": row[2]})
    
    conn.close()
    
    return render_template('main.html',rows=rows)


@app.route('/show', methods = ['GET','POST'])
def random():
    if request.method == 'GET':
        
        return render_template("add.html")
    
    if request.method == 'POST':

        name = request.form["band_name"]

        cursor = conn.cursor()

        print(name)
        
        try:
            cursor.execute("SELECT * FROM %s"%(name))
        except:
            return Exception("Not fouund")
        
        rows = []
        for row in cursor.fetchall():
            rows.append(row)
        
        conn.close()

        return render_template('showtables.html',rows=rows)


@app.route("/addBand", methods = ['GET','POST'])
def addband():
    if request.method == 'GET':
        return render_template("add.html")
    if request.method == 'POST':
        name = request.form["band_name"]

        print(name)
        
        cursor = conn.cursor()
        
        statement = "insert into band(band_name) values ('%s');"%(name)
        cursor.execute(statement)
        
        conn.commit()
        conn.close()
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)