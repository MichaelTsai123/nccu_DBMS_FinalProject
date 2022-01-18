from flask import Flask, g
from flask import render_template
import random
from flask import request
app = Flask(__name__)
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"
import csv
import sqlite3
import numpy as np
from flask import session


SQLITE_DB_SCHEMA = 'hot_pot_schema.sql'
SQLITE_DB_PATH = 'hot_pot.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
        
    return db

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/search', methods=['POST'])
def search():
    district=request.form['district']
    session["district"] = district
    price=request.form['price']
    session["price"] = price
    time=request.form['time']
    session["time"] = time
    db = get_db()
    if price=="$":
        price=1
    elif price=="$$":
        price=2
    elif price=="$$$":
        price=3
    if time=='7':
        time=int(time)-7
    if district!="ALL" and price!="ALL" and time!="ALL":
        with db:

            content=db.execute("select distinct(Store_name),Brand, Price_level,Avg_rating,Comment_num,Commentor1, Store.Tel from Store,Operation,Commentor where Store.Tel=Commentor.Tel and Price_level=? and District=? and Store.Tel=Operation.Tel and Open_Day=? order by Avg_rating Desc",[price,district,time])
    elif district=="ALL" and price!="ALL" and time!="ALL":
        with db:
            content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store,Operation,Commentor where Store.Tel=Commentor.Tel and  Price_level=? and Store.Tel=Operation.Tel and Open_Day=? order by Avg_rating Desc",[price,time])
    elif district=="ALL" and price=="ALL" and time!="ALL":
        with db:
            content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num,Commentor1, Store.Tel from Store,Operation,Commentor where Store.Tel=Commentor.Tel and   Store.Tel=Operation.Tel and Open_Day=? order by Avg_rating Desc",[time])
    elif district=="ALL" and price!="ALL" and time=="ALL":
        with db:
            content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store,Commentor where Store.Tel=Commentor.Tel and Price_level=? order by Avg_rating Desc",[price])
    
    elif district!="ALL" and price!="ALL" and time=="ALL":
        with db:
            content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store,Commentor where Store.Tel=Commentor.Tel and  Price_level=? and District=? order by Avg_rating Desc",[price,district])
    elif district!="ALL" and price=="ALL" and time!="ALL":
        with db:
            content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store,Operation,Commentor where Store.Tel=Commentor.Tel and  District=? and Store.Tel=Operation.Tel and Open_Day=? order by Avg_rating Desc",[district,time])
    elif district!="ALL" and price=="ALL" and time=="ALL":
        with db:
            content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store ,Commentor where Store.Tel=Commentor.Tel and District=? order by Avg_rating Desc",[district])
    elif district=="ALL" and price=="ALL" and time=="ALL":
        with db:
            content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store,Commentor where Store.Tel=Commentor.Tel order by Avg_rating Desc")

    if time==0:
        time+=7
    return render_template('result.html', content=content,district=district,price=price,time=time)
    if time==0:
        time+=7
    return render_template('result.html', content=content,district=district,price=price,time=time)

@app.route('/search/googlemap', methods=['POST'])
def aaa():
    db = get_db()
    #之前的table
    if "district" in session:
        district = session["district"]
        price = session["price"]
        time = session["time"]
        # print('district:',map_district)

    db = get_db()
    if price=="$":
        price=1
    elif price=="$$":
        price=2
    elif price=="$$$":
        price=3
    if time=='7':
        time=int(time)-7
    if district!="ALL" and price!="ALL" and time!="ALL":
        with db:

            map_content=db.execute("select distinct(Store_name),Brand, Price_level,Avg_rating,Comment_num,Commentor1, Store.Tel from Store,Operation,Commentor where Store.Tel=Commentor.Tel and Price_level=? and District=? and Store.Tel=Operation.Tel and Open_Day=? order by Avg_rating Desc",[price,district,time])
    elif district=="ALL" and price!="ALL" and time!="ALL":
        with db:
            map_content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store,Operation,Commentor where Store.Tel=Commentor.Tel and  Price_level=? and Store.Tel=Operation.Tel and Open_Day=? order by Avg_rating Desc",[price,time])
    elif district=="ALL" and price=="ALL" and time!="ALL":
        with db:
            map_content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num,Commentor1, Store.Tel from Store,Operation,Commentor where Store.Tel=Commentor.Tel and   Store.Tel=Operation.Tel and Open_Day=? order by Avg_rating Desc",[time])
    elif district=="ALL" and price!="ALL" and time=="ALL":
        with db:
            map_content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store,Commentor where Store.Tel=Commentor.Tel and Price_level=? order by Avg_rating Desc",[price])
    
    elif district!="ALL" and price!="ALL" and time=="ALL":
        with db:
            map_content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store,Commentor where Store.Tel=Commentor.Tel and  Price_level=? and District=? order by Avg_rating Desc",[price,district])
    elif district!="ALL" and price=="ALL" and time!="ALL":
        with db:
            map_content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store,Operation,Commentor where Store.Tel=Commentor.Tel and  District=? and Store.Tel=Operation.Tel and Open_Day=? order by Avg_rating Desc",[district,time])
    elif district!="ALL" and price=="ALL" and time=="ALL":
        with db:
            map_content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store ,Commentor where Store.Tel=Commentor.Tel and District=? order by Avg_rating Desc",[district])
    elif district=="ALL" and price=="ALL" and time=="ALL":
        with db:
            map_content=db.execute("select distinct(Store_name),Brand,Price_level,Avg_rating,Comment_num ,Commentor1, Store.Tel from Store,Commentor where Store.Tel=Commentor.Tel order by Avg_rating Desc")

    if time==0:
        time+=7

    map_phone = request.form.get('fname')  # 得到電話號碼
    with db:
        map_phnum = db.execute("select Service.Lng , Service.Lat from Service where Tel = ?",[map_phone])
    #經度:
    for row in map_phnum:
        map_testy = row[0] # testx = 24.9848357
        map_testx = row[1] # testy =121.5617507
    return render_template('result.html' ,content=map_content,district=district,price=price,time=time,testx = map_testx  , testy = map_testy)
    
@app.route('/show', methods=['POST'])
def draw():
    # Get the database connection
    db = get_db()
    if request.form.get('way') == 'Insert':
        value1 = request.form.get('phone') 
        value2 = request.form.get('address')
        value3 = request.form.get('comment_level')  
        value4 = request.form.get('cost')
        value5 = request.form.get('shop_name')
        value6 = request.form.get('brand')
        value7 = request.form.get('city')
        value8 = request.form.get('district')
        value9 = request.form.get('star')
        value10 = request.form.get('comment1')
        value11 = request.form.get('bussiness_day')
        value12 = request.form.get('open_time')
        value13 = request.form.get('close_time')
        value14 = request.form.get('latitude')
        value15 = request.form.get('longitude')
        if value3 == 'NULL' or  value3 == 'null':
            value3 = None
        if value4 == 'NULL' or  value4 == 'null':
            value4 = None
        if value9 == 'NULL' or  value9 == 'null':
            value9 = None
        #print(value1,value2,value3,value4,value5,value6,value7,value8,value9,value10,value11,value12,value13,value14,value15)
        if value1 == '':
            return '<p> 給個電話號碼好嗎？</p>'
        
        #如果沒品牌就加入該品牌入Brand的table
        if value6!='':
            try:
                with db:
                    if db.execute("SELECT Brand FROM Hot_pot Where Brand=?",[value6]).fetchall() == []:
                        db.execute("INSERT INTO Hot_pot (Brand) VALUES (?)",[value6])
            except:
                return '<p> Insert error (v6 Comment Brand type error)</p>'

        #store 
        if value2 or value3 or value4 or value5 or value6 or value7 or value8 or value9!='':
            try:
                with db:
                    db.execute("INSERT INTO Store (Tel,Addr,Comment_num,Price_level,Store_name,Brand,City,District,Avg_rating) \
                               VALUES (?,?,?,?,?,?,?,?,?)",[value1,value2,value3,value4,value5,value6,value7,value8,value9])
            except:
                return '<p> Insert error (v1~v9 type error)</p>'
            
        #comment format good;;;bad;;;i think i will eat again
        if value10!='':
            try:
                c1,c2,c3 = value10.split(';;;')
                with db:
                    db.execute("INSERT INTO Commentor (Commentor1,Commentor2,Commentor3,Tel) Values (?,?,?,?)",[c1,c2,c3,value1])
            except:
                return '<p> Insert error (v10 comment or tel type error)</p>'
            
        if value14 or value15 !='':
            try:
                with db:
                    db.execute("INSERT INTO Service (Lng,Lat,Tel) Values (?,?,?)",[value14,value15,value1])
            except:
                return '<p> Insert error (v14~v15 or tel type error)</p>'
            
        #Operation bussiness_day format 0 open_time 0000 close_time 2400
        if value11 or value12 or value13!='':
            try:
                with db:
                    db.execute("INSERT INTO Operation (Open_Day,Begin_,End_,Tel) Values (?,?,?,?)",[value11,value12,value13,value1])
            except:
                return '<p> Insert error (v11~v13 or tel type error)</p>'
               
        return render_template('index.html')
        
        
    elif request.form.get('way') == 'Update':
        if request.form.get('table')=='評論':
            value1 = request.form.get('tel')
            value2 = request.form.get('index')
            if value2 == 'NULL' or  value2 == 'null':
                value2 = None
            try:
                with db:
                    if db.execute("Update Store Set Comment_num=? Where Tel=?",[value2,value1]).rowcount == 0:
                        return '<p>Update error (no Tel)</p>'
            except:
                return '<p> Update error (Comment num type is not correct)</p>'
                    
               
        elif request.form.get('table')=='平均星數':
            value1 = request.form.get('tel')
            value2 = request.form.get('index')
            if value2 == 'NULL' or  value2 == 'null':
                value2 = None
            try:
                with db:
                    if db.execute("Update Store Set Avg_rating=? Where Tel=?",[value2,value1]).rowcount == 0:
                        return '<p>Update error (no Tel)</p>'
            except:
                return '<p> Update error (Avg_rating type is not correct)</p>'
           
    elif request.form.get('way') == 'Delete':
        need_delete_brand = False
        value1 = request.form.get('tel')
        brand_name = ''
        #如果那家店是單獨的店，代表brand只有那一家屬於該brand，所以要把brand table 的那個值也刪除
        with db:
            try:
                brand_name = db.execute("SELECT Brand FROM Store Where Tel=?",[value1]).fetchall()[0][0]
            except:
                return '<p>Delete error (no Tel)</p>'
            if len(db.execute("SELECT Brand FROM Store Where Brand=?",[brand_name]).fetchall())==1:
                need_delete_brand = True
        with db:
            c = db.execute("Delete FROM Store Where Tel=?",[value1])
        
        if need_delete_brand == True:
            with db:
                db.execute("Delete FROM Hot_pot Where Brand=?",[brand_name])
        
        return render_template('index.html')
        
    return render_template('index.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
