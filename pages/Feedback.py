import streamlit as st
import mysql.connector 

conn=mysql.connector.connect(
     host="localhost",
     port = "3306" ,
     user = "root",
     passwd = "" ,
     db = "bikes" 
)

c=conn.cursor()

def create_feeduser():
    c.execute('CREATE TABLE IF NOT EXISTS feedback(name TEXT  ,profession , suggestion TEXT)')
    
def add_feeduserdata(name,suggestion):
    c.execute('INSERT INTO feedback(name,profession,suggestion) VALUES (%s,%s,%s)',(name,profession,suggestion))
    conn.commit()
    
def feed_user():
    c.execute('SELECT * FROM feedback WHERE name=%s ,profession=%s AND suggestion=%s ',(name,profession,suggestion))
    data = c.fetchall()
    return data

def view_all_feedusers():
    c.execute('SELECT* FROM feedback')
    data = c.fetchall()
    
    return data      

st.title("Give us ur valuable feedback")

with st.form(key = "form1"):
    name = st.text_input(label="enter your name")
    
    profession= st.text_input("Enter your profession")
    
    suggestion = st.text_input(label="enter your suggestion")
    
    submit = st.form_submit_button(label="Submit this form" )
    
    #st.text(number)
    
    if submit:
        add_feeduserdata(name, suggestion)
        st.success("Feedback submitted successfully!")

# Optionally, display all feedback data in a separate section
if st.checkbox("View all feedback"):
    all_feedback = view_all_feedusers()
    st.table(all_feedback)