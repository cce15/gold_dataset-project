import datetime

import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
import plotly.graph_objects as go
from plotly.subplots import make_subplots

full_generated_datasets= os.path.join(os.getcwd(),"full_datasets")
training_generated_datasets= os.path.join(os.getcwd(),"training_datasets")

st.set_page_config(
    page_title="Gold Dataset For ML",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

st.title('Gold Dataset For ML')
st.subheader("The Best Gold Market Historical Dataset for your Machine", divider=False)
st.divider()
st.header("About The Dataset", divider="gray")
# Create the figure
fig = go.Figure()
full_file_list = glob.glob(os.path.join(full_generated_datasets, '*'))
latest_file_full = max(full_file_list, key=os.path.getmtime)
full_dataset = pd.read_csv(latest_file_full)
full_dataset['time'] = pd.to_datetime(full_dataset['time'])

metrics_row1 = st.columns(4)
m1= metrics_row1[0].container(height=128 ,border=True)
m2= metrics_row1[1].container(height=128 ,border=True)
m3= metrics_row1[2].container(height=128 ,border=True)
m4= metrics_row1[3].container(height=128 ,border=True)

with m1:
    row= st.columns(2,gap="small",vertical_alignment="center")

    row[1].metric("Gold Price Today", "2500 $/Oz", "-8%")
    row[0].image("gold_icon.png")

with m2:
    row= st.columns(2,gap="small",vertical_alignment="center")
    row[1].metric("Oil Price Today", "102 $", "-8%")
    row[0].image("oil_icon.png")
with m3:

    row= st.columns(2,gap="small",vertical_alignment="center")
    row[1].metric("Us Dollar Index (DXY)", "102", "-8%")
    row[0].image("dxy_icon.png")

with m4:
    row= st.columns(2,gap="small",vertical_alignment="center")
    row[1].metric("BitCoin Price Today", "70000$", "8%")
    row[0].image("Bitcoin_icon.png")

metrics_row2 = st.columns(4)
m12= metrics_row2[0].container(height=128 ,border=True)
m22= metrics_row2[1].container(height=128 ,border=True)
m32= metrics_row2[2].container(height=128 ,border=True)
m42= metrics_row2[3].container(height=128 ,border=True)

with m12:
    row= st.columns(2,gap="small",vertical_alignment="center")

    row[1].metric("S&P500 Today", "2500 $", "-8%")
    row[0].image("500_icon.png")

with m22:
    row= st.columns(2,gap="small",vertical_alignment="center")
    row[1].metric("Nasdaq 100 Today", "102 $", "-8%")
    row[0].image("100_icon.png")
with m32:

    row= st.columns(2,gap="small",vertical_alignment="center")
    row[1].metric("NYSE Composite", "102", "-8%")
    row[0].image("dxy_icon.png")

with m42:
    row= st.columns(2,gap="small",vertical_alignment="center")
    row[1].metric("Crypto Market Cap", "70000$", "8%")
    row[0].image("img_5.png")



# Add the line plot


fig = go.Figure(data=[go.Candlestick(x=full_dataset['time'],
            open=full_dataset['open'],
            high=full_dataset['high'],
            low=full_dataset['low'],
            close=full_dataset['close'],name='OHLC Gold Price')])

# Add moving average
fig.add_trace(go.Scatter(x=full_dataset['time'], y=full_dataset['gold_SMA_50'], name='50-day SMA',
                         line=dict(color='blue', width=1.5)))
fig.add_trace(go.Scatter(x=full_dataset['time'], y=full_dataset['gold_SMA_200'], name='200-day SMA',
                         line=dict(color='red', width=1.5)))
# Update the layout
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Price (USD)',
    template='plotly_white',
    xaxis_rangeslider_visible=False,
)
# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)
st.caption(f"Last update {datetime.date.today()}")

st.markdown("At NiceDatasets, we specialize in the art and science of data engineering and mining, "
        "crafting high-quality datasets designed to empower data analysts across various industries. "
        "Our meticulously curated data collections are tailored to enhance analytical outcomes, "
        "fueling insights that drive business success. With a focus on precision and reliability, "
        "our datasets are also ideal for training sophisticated machine learning and deep learning models, "
        "ensuring that innovation is grounded in the best available information. Whether you're decoding market trends, "
        "improving operational efficiency, or pioneering new AI technologies, "
        "NiceDatasets provides the key to unlocking the full potential of your data-driven endeavors.")

# Use glob to find all files that start with "sample" in the directory
training_file_list = glob.glob(os.path.join(training_generated_datasets, "sample*"))
full_file_list = glob.glob(os.path.join(full_generated_datasets, "sample*"))
# Check if the list is not empty
if training_file_list and full_file_list:
    # Get the latest file by sorting the list by modification time
    latest_file_training = max(training_file_list, key=os.path.getmtime)
    latest_file_full = max(full_file_list, key=os.path.getmtime)
    traning_sample_dataset = pd.read_csv(latest_file_full)
    full_sample_dataset = pd.read_csv(latest_file_full)
    st.subheader("Labeled dataset  (6 Months Sample)")
    st.dataframe(traning_sample_dataset)
    st.caption("Sample dataset that is used for training showing the data of the last 6 months.:rotating_light:   :red[Note:] ")
    st.subheader("Complete and fresh dataset (1 Month sample) ")
    st.dataframe(full_sample_dataset)
    st.caption("Full and complete dataset (1 mounth sample) without labels which is that you need to run ML models.:rotating_light:   :red[Note:]")
else:
    print("No files found starting with 'sample'.")
st.header("How You Could Use It ?", divider="gray")

left_how_to_use,righ_how_to_use=st.columns([0.5,0.5], gap="small", vertical_alignment="center")
left_how_to_use.markdown("Unlock the power of machine learning with our great dataset and achieve amazing prediction results. "
                         "In this video, "
                         "you will learn how to use the dataset "
                         "in three different machine learning models in order to achieve up to 99% accuracy in predicting the future price.")


# Display YouTube video

righ_how_to_use.video("https://www.youtube.com/watch?v=H5u_u18TrF4")

st.header("Why This Dataset ?", divider="gray")
row1 = st.columns(3)
row2 = st.columns(3)

f1= row1[0].container(height=225 ,border=True)
f1.subheader("8000 Records",divider="gray")
f1.markdown("Our dataset contains over 8000 valuable records that are based on daily information. "
            "If you're looking for reliable data to inform your business decisions in the gold market, "
            "our dataset is the perfect solution.")
f2= row1[1].container(height=225 ,border=True)
f2.subheader("Over 20 Years of Data",divider="gray")
f2.markdown("With 20 years of data available from 2000 up to the end of 2023, this data is the perfect dataset for any data-driven project.")
f3= row1[2].container(height=225 ,border=True)
f3.subheader("172 Features",divider="gray")
f3.markdown("Our dataset is the perfect choice for those who want to take their analytics to the next level. With over 172 expertly crafted features, "
            "your data analysis will be more powerful and accurate than ever before. ")
f4= row2[0].container(height=230 ,border=True)
f4.subheader("17 Technical Indicators",divider="gray")
f4.markdown("Our dataset is packed with the most important technical indicators for any data analysis. "
            "We understand that using the right set of indicators can make all the difference, which is why we've focused on using the 17 most important indicators in our feature engineering process. ")
f5= row2[1].container(height=225 ,border=True)
f5.subheader("12 Economical inducators",divider="gray")
f5.markdown("We have incorporated 12 of the most crucial economic factors to ensure that your analysis is comprehensive and complete.  ")
f6= row2[2].container(height=225 ,border=True)
f6.subheader("15 Pricing Targets",divider="gray")
f6.markdown("Our dataset is meticulously labeled with 15 distinct targets, facilitating seamless integration into any machine-learning workflow.")

###################################################################
st.header("Dataset Features", divider="gray")
featuers = st.columns(3, vertical_alignment="top")
f7=featuers[0].container(height=300)
f7.subheader("Basic Features",divider="gray")
multi = '''
* Gold Pricing Daily( OHLC) 
* NASDAQ Index Daily (OHLC)
* S&P500 Index Daily (OHLC)
* New York Stock Exchange  Index Daily (OHLC)
* Light Crude Oil Futures Daily (OHLC)
* Bitcoin Price Daily (OHLC)
* Crypto Market cap Daily (OHLC)
'''
f7.markdown(multi)

f8=featuers[1].container(height=300)
f8.subheader("Technical Indicators",divider="gray")
multi = '''
* RSI
* MACD
* Average Directional Index (ADX)
* Commodity Channel Index (CCI)
* Rate-of-Change (ROC)
* Simple Moving Average (10, 20, 50, 100, 200)
* Exponential Moving Average  (10, 20, 50, 100, 200)
'''
f8.markdown(multi)

f9=featuers[2].container(height=300)
f9.subheader("Economic Indicators",divider="gray")
multi = '''
* US dollar Index (OHLC DXY) 
* Federal Funds Effective Rate
* United States Interest Rate
* United States Inflation Rate
* United States Consumer Confidence Index
* United State Unemployment Rate
'''
f9.markdown(multi)

#################################################################
st.header("Features Description", divider="gray")
st.dataframe(pd.read_csv('features_description.csv'),use_container_width=True,hide_index=True)

#################################################################
st.header("Dataset Labels", divider="gray")
st.write("Labels and targets are crucial components in any dataset intended for supervised machine learning models. To cater to your diverse needs as a data scientist or analyst, we have included three distinct types of targets, ensuring comprehensive and versatile options for your projects.")
labels = st.columns(3, vertical_alignment="top")
l1=labels[0].container(height=500)
l1.subheader("Future Change Percentage(%)",divider="gray")

l2=labels[1].container(height=500)
l2.subheader("Future Price",divider="gray")

l3=labels[2].container(height=500)
l3.subheader("Future Price Direction Change",divider="gray")