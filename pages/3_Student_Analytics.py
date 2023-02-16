import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Student Dashboard-Institutional Dashboard", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="auto")

@st.cache()
def load_student_data():
    final_student_data = pd.read_csv("data/final_student_data.csv")
    student_enrollment = pd.read_csv("data/student_enrollment.csv")
    return final_student_data, student_enrollment

final_student_data, student_enrollment = load_student_data()

#---STUDENT METRICS---
st.title("Student Dashboard")
st.header("Student Metrics")
total_students_col, total_male_students_col, total_female_students_col = st.columns(3)

#Total Students
total_students = final_student_data.shape[0]
# Total number of male students
total_male_students = final_student_data[final_student_data["Gender"] == "Male"].shape[0]
# Total number of female students
total_female_students = final_student_data[final_student_data["Gender"] == "Female"].shape[0]

# Print the results
with total_students_col:
    st.image('images/students.png')
total_students_col.metric("Total Students: ", total_students)
with total_male_students_col:
    st.image('images/male-student.png')
total_male_students_col.metric("Male Students: ", total_male_students)
with total_female_students_col:
    st.image('images/female-student.png')
total_female_students_col.metric("Female Students: ", total_female_students)

#---STUDENTS CATEGORY DROPDOWN---
st.header("Student Information Graphics")
categories = ["Department", "State", "Gender", "Nationality", "Caste", "Graduation Type", "Stream Type", "Year Of Study","Hostel"]

selected_category = st.selectbox("View Students By:", categories)

hist_fig = px.histogram(final_student_data, x=selected_category, nbins=100)
hist_fig.update_layout(title=f"Distribution of Students based on {selected_category}", xaxis_title=selected_category, yaxis_title="Number of Students")
hist_fig.update_traces(texttemplate='%{y}', textposition='outside')
hist_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
hist_fig.update_xaxes(showgrid=False)
hist_fig.update_yaxes(showgrid=False)
st.plotly_chart(hist_fig, use_container_width=True)

#---STUDENT METRICS TWO
st.header("Student Info")
discontinued_col, retained_col, moved_col = st.columns(3)
discontinued = final_student_data[final_student_data["Discontinued Flag"] == 1].shape[0]
# Get the number of students who were retained
retained = final_student_data[final_student_data["Retained Flag"] == 1].shape[0]
# Get the number of students who moved between departments
moved = final_student_data[final_student_data["Moved Between Department Flag"] == 1].shape[0]

discontinued_col.metric("Discontinued Students", discontinued)
retained_col.metric("Retained Students", retained)
moved_col.metric("Department Change - Students", moved)
