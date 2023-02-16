import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Campus Placement-Institutional Dashboard", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="auto")

@st.cache(allow_output_mutation=True)
def load_campus_data():
    campus = pd.read_csv("data/campus.csv")
    return campus

campus = load_campus_data()

st.title("Placement Dashboard")
def format_number(num):
    if num >= 1e9:
        return '₹ {:.1f}B'.format(num / 1e9)
    elif num >= 1e6:
        return '₹ {:.1f}M'.format(num / 1e6)
    elif num >= 1e3:
        return '₹ {:.1f}K'.format(num / 1e3)
    else:
        return '₹ {:,.0f}'.format(num)
    
#CTC Metrics
mean_ctc_col , max_ctc_col, min_ctc_col = st.columns(3)
# Find mean CTC
mean_ctc = campus['CTC'].mean()
mean_ctc_col.metric("Mean CTC", format_number(mean_ctc))
# Find maximum CTC
max_ctc = campus['CTC'].max()
max_ctc_col.metric("Maximum CTC", format_number(max_ctc))
# Find minimum CTC
min_ctc = campus['CTC'].min()
min_ctc_col.metric("Minimum CTC", format_number(min_ctc))


#---PLACEMENT GRAPH---
st.header("Student Placement Graphics")
categories = ["Department", "Company", "Company Type", "Gender","Graduation Type"]
selected_category = st.selectbox("View Placed Students By:", categories)
placement_fig = px.histogram(campus, x=selected_category, nbins=25)
placement_fig.update_layout(title=f"Placement of Students based on {selected_category}", xaxis_title=selected_category, yaxis_title="Number of Students")
placement_fig.update_traces(texttemplate='%{y}', textposition='outside')
placement_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
placement_fig.update_xaxes(showgrid=False)
placement_fig.update_yaxes(showgrid=False)
st.plotly_chart(placement_fig, use_container_width=True)