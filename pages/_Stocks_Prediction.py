import streamlit as st  
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.graph_objs as go




st.title('Stocks/Sales Comparison')

tickers =(' BAJAJ-AUTO.NS','TVSMOTOR.NS','EICHERMOT.NS','7272.T','7269.T',' HEROMOTOCO.NS')

selected_competitors = st.selectbox('Pick Your Competitors',tickers)


start = st.date_input('Start',value = pd.to_datetime('2023-01-01'))
end = st.date_input('End', value = pd.to_datetime('today'))



def relativeret(df):
    rel =df.pct_change()
    cumret = (1+rel).cumprod() -1
    cumret = cumret.fillna(0)
    return cumret


if len(selected_competitors)>0:
    #df = yf.download(dropdown,start,end)['Adj Close']
    df= relativeret(yf.download(selected_competitors,start,end)['Adj Close'])
    
    st.header('Returns of {}'.format(selected_competitors))
    
    st.line_chart(df)
    
    
    
## predicting the stocks

n_years = st.slider("Years of Prediction : ",1,4)
period = n_years*365

@st.cache

def load_data(ticker):
    data = yf.download(ticker,start,end)    
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Load Data.....")
data = load_data(selected_competitors)
data_load_state.text("Loading data...Done!")


st.subheader('Raw data')
st.write(data.tail())


def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'],name='Stock_Open'))
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'],name='Stock_Close'))

    fig.layout.update(title_text="Time Series Data" , xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
    
plot_raw_data()    


#forecasting
df_train =  data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds","Close":"y"})

m = Prophet()
m.fit(df_train)

future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail())

st.write('Forecast Data')
#fig1 = m.plot(m,forecast)
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1 )



st.write('forecast components')

fig2 = m.plot_components(forecast)
st.write(fig2)