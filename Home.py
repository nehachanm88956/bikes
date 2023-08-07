import streamlit as st 
import mysql.connector 
import pandas as pd

conn=mysql.connector.connect(
 host="localhost",
 port = "3306" ,
 user = "root",
 passwd = "" ,
 db = "bikes" 
)
c=conn.cursor()
def create_usertable():
 c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT , password TEXT)')
 
def add_userdata(username,password):
 c.execute('INSERT INTO usertable(username,password) VALUES (%s,%s)',(username,password))
 conn.commit()
 
def login_user(username,password):
 c.execute('SELECT * FROM usertable WHERE username=%s AND password = %s ',(username,password))
 data = c.fetchall()
 return data
def view_all_users():
 c.execute('SELECT* FROM usertable')
 data = c.fetchall()
 
 return data 

def main():
 """login page"""
 
 
 st.title("Welcome To Bikes Sales Insights and Sentiment Analysis System 🏍️ ")
 
 st.write("This is a web app for getting the basic analytics of the bikes sales according to the features and functionality of it.📊")
 # Add text content with custom CSS class
 st.header("About Us")
 st.write("Hi There!, this is basic streamlit app which analyze the data of the bikes which is been recorded in the past few years.")
 st.write("Further in the future we will also have the feature of calculating and analyzing customers sentiments about the bikes via various social media sites ")
 
 menu = ["Home", "Login", "Signup"]
 choice = st.sidebar.selectbox("Menu", menu)
 
 if choice == "Home":
  st.subheader(" Home ")
 
 
 elif choice == "Login":
  st.subheader("Login Section")

 
 username = st.sidebar.text_input("User name")
 password = st.sidebar.text_input("Password", type="password") 
 
 if st.sidebar.checkbox("Login"):
 
    create_usertable()
 
    result= login_user(username,password)
    if result:
 
     st.success("Logged in as {}".format(username))
 
     task = st.selectbox("Task" , ["Add Post","Analytics","profiles"])
 
     if task == "Add Post":
      st.subheader("Add Your Post") 
 
     elif task == "Analytics":
      st.subheader("Analytics")
 
     elif task == "Profiles":
      st.subheader("User Profiles") 
      user_result = view_all_users()
      clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
      st.dataframe(clean_db)
 
     elif choice == "Signup":

      st.subheader("Create New Account") 
 
      new_user =st.text_input("Username")
      new_password = st.text_input("Password",type='password')
 
      if st.button("Signup"):
       create_usertable()
       add_userdata(new_user,new_password)
    st.success("You have successfully created a valid account")
    st.info("Go To Login Menu To login")
if __name__ == "__main__":
 main()