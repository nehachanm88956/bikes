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

def create_conuser():
    c.execute('CREATE TABLE IF NOT EXISTS contact(name TEXT  ,message TEXT)')
    
def add_conuserdata(name,message):
    c.execute('INSERT INTO contact(name,message) VALUES (%s,%s)',(name,message))
    conn.commit()
    
def con_user():
    c.execute('SELECT * FROM contact WHERE name=%s  AND message=%s ',(name,message))
    data = c.fetchall()
    return data

def view_all_conusers():
    c.execute('SELECT* FROM contact')
    data = c.fetchall()
    
    return data      

st.title("Pin a message")

with st.form(key = "form1"):
    name = st.text_input(label="enter your name")
    
    message= st.text_input("Enter your message")
    
    
    submit = st.form_submit_button(label="Submit this form" )
    
    #st.text(number)
    
    if submit:
        add_conuserdata(name, message)
        st.success("contact form submitted successfully!")

# Optionally, display all feedback data in a separate section
if st.checkbox("View all messages"):
    all_contact = view_all_conusers()
    st.table(all_contact)
 