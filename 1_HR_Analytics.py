import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="HR Analytics -Institutional Dashboard", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="auto")

@st.cache(allow_output_mutation=True)
def load_hr_data():
    hran = pd.read_csv("data/hr_analytics.csv")
    return hran

hran = load_hr_data()

st.title("HR Analytics Dashboard")

st.header("Employee Demographics")
#---EMPLOYEE DEMOGRAPHICS---
no_of_staff_col, staff_mean_age_col, staff_min_age_col = st.columns(3)
with no_of_staff_col:
    st.image('images/staff.png')

# Total Number of Staff
total_staff_number = hran["Staff_Id"].nunique()
no_of_staff_col.metric("Total number of staff:", total_staff_number, label_visibility="visible")

with staff_mean_age_col:
    st.image('images/ageone.png')

# The average age of employees
average_staff_age = hran["Age"].mean()
staff_mean_age_col.metric("Average age of employees:",f"{round(average_staff_age,2)} Years" , label_visibility="visible")

with staff_min_age_col:
    st.image('images/man.png')

# The Minimum age of employee 
minimum_staff_age = hran["Age"].min()
staff_min_age_col.metric("Minimum age of employee:", f"{round(minimum_staff_age,2)} Years" , label_visibility="visible")

st.header("View Employees By")

dept_tab, stream_tab, qlf_tab, desn_tab, gen_tab, sup_tab, exp_tab = st.tabs(["Department", "Stream", "Qualification", "Designation", "Gender", "Support & Maintenance Staff", "Experience"])


with dept_tab:
    staff_department_counts = hran[~hran['Department'].isin(['Driver', 'House Keeping', 'Security'])]['Department'].value_counts()
    dept_fig = px.bar(y=staff_department_counts.index, x=staff_department_counts.values, title="Employees by Department:", orientation='h', text=staff_department_counts.values)
    dept_fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    dept_fig.update_layout(xaxis_title='Number of Employees', yaxis_title='Department')
    dept_fig.update_xaxes(showgrid=False)
    dept_fig.update_yaxes(showgrid=False)
    st.plotly_chart(dept_fig, use_container_width=True)


with stream_tab:
    staff_stream_counts = hran[~hran['Stream'].isin(['Driver', 'House Keeping', 'Security'])]['Stream'].value_counts()
    stream_fig = px.bar(x=staff_stream_counts.index, y=staff_stream_counts.values, title = "Employees by Stream:")
    stream_fig.update_traces(texttemplate='%{y}', textposition='outside')
    stream_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    stream_fig.update_xaxes(showgrid=False)
    stream_fig.update_yaxes(showgrid=False)
    st.plotly_chart(stream_fig, use_container_width=True)

with qlf_tab:
    staff_qualification_counts = hran["Qualification"].value_counts()
    qlf_fig = px.bar(x=staff_qualification_counts.index, y=staff_qualification_counts.values, title= "Employees by Qualification:")
    qlf_fig.update_traces(texttemplate='%{y}', textposition='outside')
    qlf_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    qlf_fig.update_xaxes(showgrid=False)
    qlf_fig.update_yaxes(showgrid=False)
    st.plotly_chart(qlf_fig, use_container_width=True)

with desn_tab:
    staff_designation_counts = hran[~hran["Designation"].isin(['Driver', 'House Keeping', 'Security', 'Dean', 'Principal'])]["Designation"].value_counts()
    desn_fig = px.bar(x=staff_designation_counts.index, y=staff_designation_counts.values, title= "Employees by Designation:")
    desn_fig.update_traces(texttemplate='%{y}', textposition='outside')
    desn_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    desn_fig.update_xaxes(showgrid=False)
    desn_fig.update_yaxes(showgrid=False)
    st.plotly_chart(desn_fig, use_container_width=True)

with gen_tab:
    gender_counts = hran["Gender"].value_counts()
    gen_fig = px.pie(values=gender_counts.values, names=gender_counts.index, title="Employee Ratio by Gender:")
    gen_fig.update_xaxes(showgrid=False)
    gen_fig.update_yaxes(showgrid=False)
    st.plotly_chart(gen_fig, use_container_width=True)

with sup_tab:
    support_staff_counts = hran[hran["Designation"].isin(['Driver', 'House Keeping', 'Security'])]["Designation"].value_counts()
    sup_fig = px.bar(x=support_staff_counts.index, y=support_staff_counts.values,title="Support Staff")
    sup_fig.update_traces(texttemplate='%{y}', textposition='outside')
    sup_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    sup_fig.update_xaxes(showgrid=False)
    sup_fig.update_yaxes(showgrid=False)
    st.plotly_chart(sup_fig, use_container_width=True)

with exp_tab:
    # Create a new column for the experience group
    bins = [0, 2, 5, 10, 15, 20, 30, hran["Experience"].max()]
    hran["Experience_Range"] = pd.cut(hran["Experience"], bins, labels=["0-2", "3-5", "6-10", "11-15","16-20", "21-30", "Above 31"])
    experience_hist = hran["Experience_Range"].value_counts().sort_index()
    # Plot the histogram using plotly
    exp_fig = px.bar(experience_hist, x=experience_hist.index, y=experience_hist.values, title="Employees by Experience")
    exp_fig.update_traces(texttemplate='%{y}', textposition='outside')
    exp_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    exp_fig.update_xaxes(showgrid=False)
    exp_fig.update_yaxes(showgrid=False)
    st.plotly_chart(exp_fig, use_container_width=True)


st.header("Employee Experience:")

average_staff_experience_col, max_staff_experience_col, min_staff_experience_col = st.columns(3)

# Average Experience of Staff
average_staff_experience = hran[hran['Experience'] != 9999]['Experience'].mean()
average_staff_experience_col.metric("Average experience of staff:", f"{round(average_staff_experience,2)} Years")

# Maximum Experience of Staff
max_staff_experience = hran[hran['Experience'] != 9999]['Experience'].max()
max_staff_experience_col.metric("Maximum experience of staff:", f"{round(max_staff_experience, 2)} Years")

# Minimum Experience of Staff
min_staff_experience = hran[hran['Experience'] != 9999]['Experience'].min()
min_staff_experience_col.metric("Minimum experience of staff:",f"{round(min_staff_experience, 2)} Years")

st.header("Employee Salary Details")
mean_staff_salary_col, max_staff_salary_col, min_staff_salary_col = st.columns(3)
# Average Staff Salary
mean_staff_salary = hran[hran['Salary'] != 999999999]['Salary'].mean()
mean_staff_salary_col.metric("Average Staff Salary", f"₹ {round(mean_staff_salary,2)}")

# Maximum Staff Salary
max_staff_salary = hran[hran['Salary'] != 999999999]['Salary'].max()
max_staff_salary_col.metric("Maximum Staff Salary", f"₹ {max_staff_salary}")

# Minimum Staff Salary
min_staff_salary = hran[hran['Salary'] != 999999999]['Salary'].min()
min_staff_salary_col.metric("Minimum Staff Salary", f"₹ {min_staff_salary}")

st.header("Top 10 Employees By")
exp_high_tab, exp_low_tab, sal_high_tab, sal_low_tab = st.tabs(["Most Experience", "Least Experience", "Highest Salary", "Least Salary"])

# Select the top 10 employees by Experience
with exp_high_tab:
    top_10_exp = hran[hran['Experience'] != 9999].sort_values(by='Experience', ascending=False)
    top_10_exp = top_10_exp.head(10)
    top_10_exp = top_10_exp[['Staff_Id', 'Name', 'Age', 'Salary', 'Department', 'Designation', 'Qualification', 'Experience']]
    top_10_exp = top_10_exp.reset_index(drop=True)
    st.dataframe(data=top_10_exp)

# Select the Bottom 10 employees by Experience
with exp_low_tab:
    bottom_10_exp = hran[hran['Experience'] != 9999].sort_values(by='Experience', ascending=True)
    bottom_10_exp = bottom_10_exp.head(10)
    bottom_10_exp = bottom_10_exp[['Staff_Id', 'Name', 'Age', 'Salary', 'Department', 'Designation', 'Qualification', 'Experience']]
    bottom_10_exp = bottom_10_exp.reset_index(drop=True)
    st.dataframe(data=bottom_10_exp)

# Select the Top 10 employees by Salary
with sal_high_tab:
    top_10_salary = hran[hran['Salary'] != 999999999].sort_values(by='Salary', ascending=False)
    top_10_salary = top_10_salary.head(10)
    top_10_salary = top_10_salary[['Staff_Id', 'Name', 'Age', 'Salary', 'Department', 'Designation', 'Qualification', 'Experience']]
    top_10_salary = top_10_salary.reset_index(drop=True)
    st.dataframe(data=top_10_salary)


# Select the Bottom 10 employees by Salary
with sal_low_tab:
    bottom_10_salary = hran[hran['Salary'] != 999999999].sort_values(by='Salary', ascending=True)
    bottom_10_salary = bottom_10_salary.head(10)
    bottom_10_salary = bottom_10_salary[['Staff_Id', 'Name', 'Age', 'Salary', 'Department', 'Designation', 'Qualification', 'Experience']]
    bottom_10_salary = bottom_10_salary.reset_index(drop=True)
    st.dataframe(data=bottom_10_salary)