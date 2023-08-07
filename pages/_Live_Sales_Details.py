import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 




# read csv from a github repo
def loadData():
	df = pd.read_csv("hero_sales.csv")


st.set_page_config(
    page_title = 'Live Sales Calculation Dashboard',
    page_icon = '✅',
    layout = 'wide'
)


# dashboard title

st.title("Live Sales Calculation Dashboard")

# top-level filters def loadData():
df = pd.read_csv("hero_sales.csv")
 
job_filter = st.selectbox("Select the Job", pd.unique(df['Job']))


# creating a single-element container.
placeholder = st.empty()

# dataframe filter 

def loadData():	
 df = pd.read_csv("hero_sales.csv")	
 df = df[df['Job']==job_filter]

# near real-time / live feed simulation 

for seconds in range(200):
#while True: 
    
    df['age_new'] = df['Age'] * np.random.choice(range(1,5))
    df['Model_new'] = df['Model'] * np.random.choice(range(1,5))

    # creating KPIs 
    avg_age = np.mean(df['age_new']) 

    count_loan= int(df[(df["Loan"]=='TRUE')]['Loan'].count() + np.random.choice(range(1,100)))

    PurchasePrice= np.mean(df['PurchasePrice'])

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Age ⏳", value=round(avg_age), delta= round(avg_age) - 10)
        kpi2.metric(label="Loan Count ", value= int(count_loan), delta= - 10 + count_loan)
        kpi3.metric(label="Purchase Price＄", value= f"$ {round(PurchasePrice,2)} ", delta= - round(PurchasePrice/count_loan) * 100)


        # create two columns for charts 

        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'Loan')
            st.write(fig)
        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame = df, x = 'age_new')
            st.write(fig2)
        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)
    #placeholder.empty()