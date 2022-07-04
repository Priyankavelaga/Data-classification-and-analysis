from ast import Pass
from flask import Flask, render_template, request
import json
import sqlite3

conn = sqlite3.connect('eq1.db')
c= conn.cursor()

app = Flask(__name__)
@app.route('/')
def home():
   return render_template('index.html')


@app.route('/latlong', methods=['POST','GET'])
def displayquakes():
    conn = sqlite3.connect('eq1.db')
    c= conn.cursor()
    lat=str(request.form['number1'])
    long=str(request.form['number2'])
    c.execute("select time, latitude, longitude, id, place from eq  where latitude and longitude  between '"+lat+"' and '"+long+"';") 
    quakes=c.fetchall()
    return render_template('/latlon.html', q=quakes)


@app.route('/gap', methods=['POST','GET'])
def changegap():
    conn = sqlite3.connect('eq1.db')
    c= conn.cursor()
    number=str(request.form['num'])
    netvalue=str(request.form['net'])
    c.execute("select net, gap, id from eq where net ='"+netvalue+"';")
    before=c.fetchall()
    c.execute("update eq set gap = '"+number+"' where net = '"+netvalue+"';")
    c.execute("select net, gap, id from eq where net = '"+netvalue+"';")
    after=c.fetchall() 
    return render_template('/gap.html', b=before, a=after)


@app.route('/match', methods=['POST','GET'])
def matches():
    conn = sqlite3.connect('eq1.db')
    c= conn.cursor()
    gap1=str(request.form['gap1'])
    gap2=str(request.form['gap2'])
    net=str(request.form['netvalue'])
    c.execute("SELECT count(*) FROM eq WHERE cast(GAP as unsigned) BETWEEN '"+gap1+"' AND '"+gap2+"' and net = '"+net+"';")
    matches=c.fetchall()
    return render_template('/match.html', m=matches)

@app.route('/magrange', methods=['POST','GET'])
def magplace():
    conn = sqlite3.connect('eq1.db')
    c= conn.cursor()
    mag1=str(request.form['mag1'])
    mag2=str(request.form['mag2'])
    place=str(request.form['place'])
    c.execute("select time, latitude, longitude, mag, place from eq where mag between '"+mag1+"' and '"+mag2+"' and place like '" '%' +place+"' '%' ;")
    mag =c.fetchall()
    return render_template('/magrplace.html', p=mag)


@app.route('/typenet', methods=['POST','GET'])
def editkeyword():
    conn = sqlite3.connect('eq1.db')
    c= conn.cursor()
    type=str(request.form['type'])
    netv=str(request.form['nett'])
    c.execute("select count(*) from eq where type = '"+type+"' AND net = '"+netv+"';")
    nettype = c.fetchall()
    return render_template('/nettype.html', n=nettype)


@app.route('/stringchange', methods=['POST','GET'])
def changestring():
    conn = sqlite3.connect('eq1.db')
    c= conn.cursor()
    type1=str(request.form['type1'])
    type2=str(request.form['type2'])
    c.execute("select net, gap, id, type from eq where type ='"+type1+"';")
    string1=c.fetchall()
    c.execute("update eq set type = '"+type2+"' where type = '"+type1+"';")
    c.execute("select net, gap, id, type from eq where type = '"+type2+"';")
    string2=c.fetchall() 
    return render_template('/string.html', s=string1, y=string2)


if __name__ == '__main__':
    app.debug=True
    app.run()