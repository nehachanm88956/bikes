import mysql.connector 
import streamlit as st 

#connection 

conn=mysql.connector.connect(
     host="localhost",
     port = "3306" ,
     user = "root",
     passwd = "" ,
     db = "bikes" 
)

c=conn.cursor()

#fetch data

def view_all_data():
    c.execute('select*from hero_motorbike_dataset order by Model asc')    
    data = c.fetchall()
    return data