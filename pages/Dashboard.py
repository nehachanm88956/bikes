import streamlit as st 
import pandas as pd
import plotly.express as px 
import time
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import matplotlib.pyplot as plt
from query import *  
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


# Fetch data
result = view_all_data()
df = pd.DataFrame(result, columns=["Model","Price","SalesinMonth","BodyType","Mileage","Torque"])

# Sidebar
st.sidebar.image("data/logo1.jpg", caption="Online Analytics")

# Switchbar
st.sidebar.header("Please filter")

model= st.sidebar.multiselect(
    "Select Model",
    options=df["Model"].unique(),
    default=df["Model"].unique(),
    key="model_filter"
)

bodytype = st.sidebar.multiselect(
    "Select Body Type",
    options=df["BodyType"].unique(),
    default=df["BodyType"].unique(),
    key="body_filter"
)

price = st.sidebar.multiselect(
    "Select Price",
    options=df["Price"].unique(),
    default=df["Price"].unique(),
    key="price_filter"
)

df_selection = df.query("Model == @model & BodyType == @bodytype & Price == @price")


# Function to handle non-numeric values and calculate average torque
def calculate_average_SalesinMonth(df_selection):
    df_selection.dropna(subset=["SalesinMonth"], inplace=True)
    df_selection["SalesinMonth"] = pd.to_numeric(df_selection["SalesinMonth"], errors="coerce")
    average_Sales = df_selection["SalesinMonth"].mean()
    return average_Sales



def Price(df_selection):
    df_selection.dropna(subset=["Price"], inplace=True)
    df_selection["Price"] = pd.to_numeric(df_selection["Price"], errors="coerce")
    average_Price= df_selection["Price"].mean()
    return average_Price

# Home

def Home():
    
    with st.expander("⏰ Filteration"):
        showData=st.multiselect('Filter: ',df_selection.columns,default=["Model","Price","SalesinMonth","BodyType","Mileage","Torque"])
        st.dataframe(df_selection[showData],use_container_width=True)   
        

Home()

# Simple bar graph
SalesinMonth_by_Model = df_selection.groupby("Model")["SalesinMonth"].value_counts().sort_values()

fig_Price = px.bar(
    x= SalesinMonth_by_Model.values,
    y=SalesinMonth_by_Model.index.get_level_values(0),
    orientation="h",
    title="Sales in Month by Model ",
    color_discrete_sequence=["#0083B8"] * len(SalesinMonth_by_Model),
    template=("plotly_dark")
)

fig_Price.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

st.plotly_chart(fig_Price)

try:
    with st.expander("Tabular"):
        st.dataframe(df_selection, use_container_width=True)
        showdata = st.multiselect(
            'Filter:', df_selection.columns, default=["Model","BodyType","Year"]
        )
        st.dataframe(df_selection[showdata], use_container_width=True)

    # Convert categorical columns to numeric for model training
    df_selection['BodyType'].replace(['Commute','Cruiser','Sport','Scooter','Touring'],
        [1, 2, 3, 4, 5], inplace=True)


    X = df_selection[['Models', 'SalesinMonth']]
    y = df_selection['Mileage']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    test = clf.predict(X_test)

    y_test = y_test['Price']
    accuracy = accuracy_score(y_test, test)

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df_selection["Model"].unique(), use_container_width=True)

    with col2:
        st.write("Sales Probability:", round(accuracy, 2))
        st.title(f"{round(accuracy * 100, 1)} %")
        st.markdown("""---""")
        new_user = clf.predict([[1, 2, 3]])  # Replace with actual values from your dataset
        st.write("Recommended Company")
        st.info(",".join(new_user))
    st.plotly_chart(fig_Price, use_container_width=False, theme="streamlit")

except:
    st.info("One of the selections is required")

# Aggregations
st.subheader('Aggregations')
average_SalesinMonth = calculate_average_SalesinMonth(df_selection)
average_SalesinMonth = df_selection["SalesinMonth"].mean()
st.write('Average Sales in Month:', average_SalesinMonth)


average_Price = Price(df_selection)
average_Price = df_selection["Price"].mean()
st.write('Average Price:', average_Price)




total1,total2=st.columns(2,gap='large')
with total1:
        st.info('Average_SalesinMonth',icon="📌")
        st.metric(label="mean TZS",value=f"{average_SalesinMonth:,.0f}")


with total2:
        st.info('Average_Price',icon="📌")
        st.metric(label="mean TZS",value=f"{average_Price:,.0f}")


st.markdown("""---""")

        

def graphs():
#simple line graph
 Sales_state = df_selection.groupby(by=["Model"]).count()[["Mileage"]]
 fig_state = px.line(
    Sales_state,
    x= Sales_state.index,
    y="Mileage",
    orientation="v",
    title="Models sales in month by Mileage",
    color_discrete_sequence=["#0083B8"] * len(Sales_state),
    template=("plotly_white")
)

 fig_state.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=False)
)
 st.plotly_chart(fig_state)

#st.plotly_chart(fig_state)


#simple bar graph
SalesinMonth_by_Model = df_selection.groupby(by=["BodyType"]).count()[["Price"]]
fig_investment= px.bar(
    SalesinMonth_by_Model,
    x= "Price",
    y=SalesinMonth_by_Model.index,
    orientation="h",
    title="Price of Bikes by  BodyType",
    color_discrete_sequence=["#0083B8"] * len(SalesinMonth_by_Model),
    template=("plotly_white")
)

fig_investment.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

   


fig = px.pie(df_selection, values='Torque', names='BodyType', title='Torque by BodyType')
fig.update_layout(legend_title="Torque", legend_y=0.9)
fig.update_traces(textinfo='percent+label', textposition='inside')
#st.plotly_chart(fig, use_container_width=True)
graphs()

left,right=st.columns(2)
left.plotly_chart(fig,use_container_width=True)
right.plotly_chart(fig_investment,use_container_width=True)   

def Progressbar():
  st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True)
  target=500000
  current=df_selection["SalesinMonth"].sum()
  percent=round((current/target*100))
  mybar=st.progress(0)


  

  if percent>100:
        st.subheader("Target done !")
  else:
     st.write("you have ",percent, "% " ,"of ", (format(target, 'd')), "TZS")
     for percent_complete in range(percent):
        time.sleep(0.1)
        mybar.progress(percent_complete+1,text=" Target Percentage")


