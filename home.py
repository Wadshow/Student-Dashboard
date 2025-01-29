import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu
import pickle

with st.sidebar:
    selected = option_menu(
        menu_title="Dashboard",
        options=["Home","College","Placement","Optional List","Predictions"]
    )

if selected == "Home":
    st.title("Engineering Student Dashboard")
    st.markdown('<style>div.block-container{padding-top:1rem;}<style>',unsafe_allow_html=True)

    col1, col2 = st.columns((2))

    labels = ['MHT CET', 'JEE Main', 'Others']
    sizes = [70, 20, 10]

    with col1:
        st.subheader('Examwise Admission')
        fig = px.pie(values=sizes, names=labels, template='seaborn')
        fig.update_traces(text=['MHT CET', 'JEE Main', 'Others'])
        st.plotly_chart(fig, use_container_width=True)

    data = {
        'Exam Type': ['MHT CET', 'JEE Main', 'Others'],
        'No of Students': [7000, 2000, 1000]
    }

    df = pd.DataFrame(data)

    with col2:
        st.subheader('Students Admission')
        fig = px.bar(df, x="Exam Type", y="No of Students", template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height=200)

    df = pd.read_excel('CET.xlsx')
    st.subheader('City vs Percentile')
    fig = px.scatter(df, x='City', y='Percentile', color='Branch', template='seaborn')
    st.plotly_chart(fig, use_container_width=True)


if selected == "College": 
    st.title("Information about College")

    df = pd.read_csv('CET1.csv')

    University = st.sidebar.selectbox(
        "Select University:",
        options=df["University"].unique()
    )

    College = st.sidebar.selectbox(
        "Select College name:",
        options=df["College"].unique()
    )

    df_selection = df.query(
        "University == @University & College== @College"
    )

    st.subheader("College vs Department")
    fig = px.scatter(df_selection, x='Branch', y='Percentile')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns((2))

    Branch = st.sidebar.selectbox(
        "Select Branch:",
        options=df["Branch"].unique()
    )

    df_selection1 = df.query(
        "University == @University & College == @College & Branch == @Branch & Category == 'GOPENS'"
    )

    with col1:
        st.subheader("Bar Graph")
        fig = px.bar(df_selection1, x='Year', y='Percentile', text='Percentile')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Line Chart")
        fig = px.line(df_selection1, x='Year', y='Percentile')
        st.plotly_chart(fig, use_container_width=True)

    df_selection2 = df.query(
        "University == @University & College == @College & Branch == @Branch"
    )

    with col1:
        st.subheader("Bar Graph")
        fig = px.bar(df_selection2, x='Year', y='Percentile', color='Category', text='Percentile')
        fig.update_traces(texttemplate='%{text}')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Line Chart")
        fig = px.line(df_selection2, x='Year', y='Percentile', color='Category')
        st.plotly_chart(fig, use_container_width=True)


if selected == "Placement":
    st.title(f"You have Selected {selected}")

if selected == "Optional List":
    st.title(f"{selected}")
    st.markdown('<style>div.block-container{padding-top:1rem;}<style>',unsafe_allow_html=True)

    df = pd.read_excel('CET.xlsx')

    st.sidebar.header('Please Filter Here:')
    Branch = st.sidebar.selectbox(
        "Select Branch:",
        options=df["Branch"].unique()
    )

    City = st.sidebar.selectbox(
        "Select City:",
        options=df["City"].unique()
    )

    Category = st.sidebar.selectbox(
        "Select Category:",
        options=df["Category"].unique()
    )

    Percentile = st.sidebar.number_input(
        "Enter Percentile:",
        min_value=0.0, max_value=100.0, step=0.1, value=99.0
    )

    df_selection = df.query(
        "Branch == @Branch & City == @City & Category == @Category & Percentile <= @Percentile"
    )

    df_selection_sorted = df_selection.sort_values(by='Percentile', ascending=False).head(10)
    st.write(f'<style> .dataframe tbody tr td {{ font-size: 30px; }} </style>', unsafe_allow_html=True)
    st.dataframe(df_selection_sorted)

if selected == "Predictions":
    st.title("Predictions for Admission")
    pickle_in = open("model.pkl","rb")
    model=pickle.load(pickle_in)

    def welcome():
        return "Welcome"

    def predict_clg(percentile,branch,category,seat_type,score_type):
        prediction = model.predict([[percentile,branch,category,seat_type,score_type]])
        print(prediction)
        return prediction

    def main():
        st.title("Prediction")
        percentile = st.text_input("Percentile","Type Here")
        branch = st.text_input("Branch","Type Here")
        category = st.text_input("Category","Type Here")
        seat_type = st.text_input("Seat_type","Type Here")
        score_type = st.text_input("Score_type","Type Here")

        result = ""
        if st.button("Predict"):
            result = predict_clg(percentile,branch,category,seat_type,score_type)
        st.success('The College is {}'.format(result))

    if __name__ == "main":
        main()   